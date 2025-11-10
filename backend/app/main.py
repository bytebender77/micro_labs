"""Main FastAPI application for HealthGuide"""
from fastapi import FastAPI, HTTPException, Depends  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from fastapi.responses import JSONResponse  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from typing import List
import uuid
from datetime import datetime

from app.config import settings
from app.models import (
    ConversationRequest, ConversationResponse, TriageResult, TriageLevel,
    ProviderRequest, Provider, SummaryResponse, Message
)
from app.database import get_db, init_db, save_conversation, get_conversation, save_temperature, get_temperature_history
from app.llm_service import get_llm_service
from app.red_flags import check_red_flags, get_red_flag_response
from app.providers import get_providers
from app.fever_diseases import identify_fever_type, get_disease_recommendations


def normalize_message_dict(msg_dict: dict) -> dict:
    """Normalize a message dictionary to ensure all values are JSON serializable"""
    normalized = {}
    for key, value in msg_dict.items():
        if isinstance(value, datetime):
            # Convert datetime objects to ISO format strings
            normalized[key] = value.isoformat()
        else:
            normalized[key] = value
    return normalized


# Initialize FastAPI app
app = FastAPI(
    title="HealthGuide - Fever Helpline API",
    description="AI-powered fever triage and guidance system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()


# Health check endpoint
@app.get("/")
async def root():
    return {"message": "HealthGuide API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "HealthGuide API"}


# Triage endpoint
@app.post("/api/triage", response_model=ConversationResponse)
async def triage(
    request: ConversationRequest,
    db: Session = Depends(get_db)
):
    """
    Main triage endpoint that processes user messages and provides guidance.
    """
    try:
        # Initialize LLM service with provider from request (or default)
        provider = request.llm_provider or settings.llm_provider
        llm_service = get_llm_service(provider=provider)
        
        # Enhance message with structured symptom data if provided
        enhanced_message = request.message
        if request.symptom_data:
            symptom_data = request.symptom_data
            # If emergency symptoms detected in structured data, prioritize that
            if symptom_data.emergency_detected:
                enhanced_message = f"EMERGENCY SYMPTOMS DETECTED: {request.message}"
            # Add structured symptom information to message for better context
            if symptom_data.symptoms:
                symptom_list = ", ".join(symptom_data.symptoms)
                enhanced_message = f"{request.message}\n\nSelected symptoms: {symptom_list}"
        
        # Check for red flags FIRST (before any other processing)
        # Check both the original message and enhanced message
        red_flag = check_red_flags(request.message) or check_red_flags(enhanced_message)
        
        # Also check structured symptom data for emergency indicators
        if request.symptom_data and request.symptom_data.emergency_detected:
            red_flag = red_flag or "Emergency symptoms selected via symptom selector"
        if red_flag:
            # Save conversation with red flag
            # Convert conversation history to dictionaries (handle Message objects, dicts, etc.)
            conversation_dicts = []
            for msg in request.conversation_history:
                if isinstance(msg, dict):
                    # Normalize dictionary to ensure datetime objects are converted to strings
                    conversation_dicts.append(normalize_message_dict(msg))
                elif isinstance(msg, Message):
                    timestamp = getattr(msg, "timestamp", None)
                    if isinstance(timestamp, datetime):
                        timestamp = timestamp.isoformat()
                    elif timestamp is None:
                        timestamp = datetime.now().isoformat()
                    conversation_dicts.append({
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": timestamp
                    })
                else:
                    timestamp = getattr(msg, "timestamp", None)
                    if isinstance(timestamp, datetime):
                        timestamp = timestamp.isoformat()
                    elif timestamp is None:
                        timestamp = datetime.now().isoformat()
                    conversation_dicts.append({
                        "role": getattr(msg, "role", "user"),
                        "content": getattr(msg, "content", ""),
                        "timestamp": timestamp
                    })
            
            messages = conversation_dicts + [
                {"role": "user", "content": request.message, "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": get_red_flag_response(red_flag), "timestamp": datetime.now().isoformat()}
            ]
            save_conversation(
                db=db,
                session_id=request.session_id,
                messages=messages,
                triage_level=TriageLevel.EMERGENCY.value,
                red_flag=red_flag
            )
            
            return ConversationResponse(
                session_id=request.session_id,
                message=get_red_flag_response(red_flag),
                triage_result=TriageResult(
                    triage_level=TriageLevel.EMERGENCY,
                    escalate=True,
                    summary=f"Red flag symptom detected: {red_flag}",
                    recommended_next_steps=[
                        "Call emergency services immediately",
                        "Go to the nearest emergency room",
                        "Do not delay seeking medical attention"
                    ],
                    red_flag_detected=True,
                    red_flag_symptom=red_flag
                ),
                conversation_complete=True
            )
        
        # Convert conversation history to Message objects
        messages = []
        for msg in request.conversation_history:
            if isinstance(msg, dict):
                # If it's a dictionary, extract role and content
                messages.append(Message(
                    role=msg.get("role", "user"),
                    content=msg.get("content", "")
                ))
            elif isinstance(msg, Message):
                # If it's already a Message object, use it directly
                messages.append(msg)
            else:
                # Fallback: try to access as object attributes
                messages.append(Message(
                    role=getattr(msg, "role", "user"),
                    content=getattr(msg, "content", "")
                ))
        
        messages.append(Message(role="user", content=request.message))
        
        # Assess triage level
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        # Use enhanced message for triage assessment if symptom data is provided
        triage_message = enhanced_message if request.symptom_data else request.message
        triage_result = llm_service.assess_triage(conversation_history, triage_message)
        
        # Disease-specific fever detection
        disease_analysis = identify_fever_type(triage_message)
        if disease_analysis["confidence"] > 0.3:
            # Add disease-specific recommendations to triage result
            disease_recommendations = get_disease_recommendations(disease_analysis["likely_type"])
            if disease_recommendations:
                triage_result.recommended_next_steps = disease_recommendations + triage_result.recommended_next_steps
                triage_result.summary = f"{triage_result.summary} (Possible {disease_analysis['likely_type'].upper()} - {disease_analysis['confidence']*100:.0f}% confidence)"
        
        # Generate response
        if triage_result.red_flag_detected:
            response_message = get_red_flag_response(triage_result.red_flag_symptom or "red flag symptom")
            conversation_complete = True
        else:
            # Generate LLM response
            response_message = llm_service.generate_response(messages, conversation_history)
            if triage_result.next_question:
                response_message += f"\n\n{triage_result.next_question}"
            conversation_complete = triage_result.next_question is None
        
        # Save conversation to database
        # Convert conversation history to dictionaries (handle Message objects, dicts, etc.)
        conversation_dicts = []
        for msg in request.conversation_history:
            if isinstance(msg, dict):
                # Normalize dictionary to ensure datetime objects are converted to strings
                conversation_dicts.append(normalize_message_dict(msg))
            elif isinstance(msg, Message):
                timestamp = getattr(msg, "timestamp", None)
                if isinstance(timestamp, datetime):
                    timestamp = timestamp.isoformat()
                elif timestamp is None:
                    timestamp = datetime.now().isoformat()
                conversation_dicts.append({
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": timestamp
                })
            else:
                timestamp = getattr(msg, "timestamp", None)
                if isinstance(timestamp, datetime):
                    timestamp = timestamp.isoformat()
                elif timestamp is None:
                    timestamp = datetime.now().isoformat()
                conversation_dicts.append({
                    "role": getattr(msg, "role", "user"),
                    "content": getattr(msg, "content", ""),
                    "timestamp": timestamp
                })
        
        updated_messages = conversation_dicts + [
            {"role": "user", "content": request.message, "timestamp": datetime.now().isoformat()},
            {"role": "assistant", "content": response_message, "timestamp": datetime.now().isoformat()}
        ]
        save_conversation(
            db=db,
            session_id=request.session_id,
            messages=updated_messages,
            triage_level=triage_result.triage_level.value,
            summary=triage_result.summary,
            red_flag=triage_result.red_flag_symptom
        )
        
        return ConversationResponse(
            session_id=request.session_id,
            message=response_message,
            triage_result=triage_result,
            conversation_complete=conversation_complete
        )
    
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"❌ ERROR in /api/triage:")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing triage request: {str(e)}"
        )


# Summary endpoint
@app.get("/api/summary/{session_id}", response_model=SummaryResponse)
async def get_summary(session_id: str, db: Session = Depends(get_db)):
    """Get conversation summary for a session"""
    conversation = get_conversation(db, session_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get triage result from conversation
    triage_level = TriageLevel(conversation.triage_level) if conversation.triage_level else TriageLevel.FOLLOW_UP
    
    # Extract recommended steps from messages (simplified)
    recommended_steps = [
        "Monitor your symptoms",
        "Stay hydrated",
        "Get plenty of rest",
        "Consult a healthcare provider if symptoms persist"
    ]
    
    return SummaryResponse(
        session_id=session_id,
        summary=conversation.summary or "Fever-related symptoms discussed",
        triage_level=triage_level,
        recommended_next_steps=recommended_steps,
        conversation_count=len(conversation.messages) if conversation.messages else 0
    )


# Providers endpoint
@app.post("/api/providers", response_model=List[Provider])
async def get_healthcare_providers(request: ProviderRequest):
    """Get nearby healthcare providers"""
    try:
        providers = get_providers(request)
        return providers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching providers: {str(e)}")


# Create new session endpoint
@app.post("/api/session")
async def create_session():
    """Create a new conversation session"""
    session_id = str(uuid.uuid4())
    return {"session_id": session_id, "message": "New session created"}


# Get available LLM providers endpoint
@app.get("/api/llm-providers")
async def get_llm_providers():
    """Get list of available LLM providers and their status"""
    providers = []
    
    # Check OpenAI
    openai_available = bool(settings.openai_api_key and 
                           settings.openai_api_key not in ["", "your_key_here", "your-api-key"])
    providers.append({
        "id": "openai",
        "name": "OpenAI (GPT-4o Mini)",
        "available": openai_available
    })
    
    # Check Gemini
    gemini_available = bool(settings.gemini_api_key and 
                            settings.gemini_api_key not in ["", "your_key_here", "your-api-key"])
    providers.append({
        "id": "gemini",
        "name": "Google Gemini 2.0 Flash",
        "available": gemini_available
    })
    
    return {
        "providers": providers,
        "default": settings.llm_provider
    }


# Debug endpoint to check API key status (without exposing keys)
@app.get("/api/debug/keys")
async def debug_api_keys():
    """Debug endpoint to check API key configuration status"""
    import os
    env_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    
    return {
        "openai_configured": bool(settings.openai_api_key and 
                                 settings.openai_api_key not in ["", "your_key_here", "your-api-key"]),
        "openai_key_length": len(settings.openai_api_key) if settings.openai_api_key else 0,
        "gemini_configured": bool(settings.gemini_api_key and 
                                  settings.gemini_api_key not in ["", "your_key_here", "your-api-key"]),
        "gemini_key_length": len(settings.gemini_api_key) if settings.gemini_api_key else 0,
        "env_file_path": env_file_path,
        "env_file_exists": os.path.exists(env_file_path),
        "openai_key_preview": f"{settings.openai_api_key[:10]}..." if settings.openai_api_key and len(settings.openai_api_key) > 10 else "Not set",
        "gemini_key_preview": f"{settings.gemini_api_key[:10]}..." if settings.gemini_api_key and len(settings.gemini_api_key) > 10 else "Not set"
    }


# Temperature tracking endpoints
@app.post("/api/temperature")
async def log_temperature(
    session_id: str,
    temperature: float,
    unit: str = "F",
    notes: str = None,
    db: Session = Depends(get_db)
):
    """Log a temperature reading for a session"""
    try:
        temp_log = save_temperature(db, session_id, temperature, unit, notes)
        return {
            "id": temp_log.id,
            "session_id": temp_log.session_id,
            "temperature": temp_log.temperature,
            "unit": temp_log.unit,
            "recorded_at": temp_log.recorded_at.isoformat(),
            "notes": temp_log.notes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging temperature: {str(e)}")


@app.get("/api/temperature/{session_id}")
async def get_temperature_history_endpoint(session_id: str, db: Session = Depends(get_db)):
    """Get temperature history for a session"""
    try:
        temp_logs = get_temperature_history(db, session_id)
        return {
            "session_id": session_id,
            "temperatures": [
                {
                    "id": log.id,
                    "temperature": log.temperature,
                    "unit": log.unit,
                    "recorded_at": log.recorded_at.isoformat(),
                    "notes": log.notes
                }
                for log in temp_logs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching temperature history: {str(e)}")


if __name__ == "__main__":
    import uvicorn  # pyright: ignore[reportMissingImports]
    uvicorn.run(app, host=settings.host, port=settings.port)

