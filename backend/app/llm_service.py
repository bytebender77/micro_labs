"""LLM service for HealthGuide triage"""
import json
import os
from typing import List, Dict, Optional
from openai import OpenAI  # pyright: ignore[reportMissingImports]
import google.generativeai as genai  # pyright: ignore[reportMissingImports]

from app.config import settings
from app.models import Message, TriageResult, TriageLevel
from app.red_flags import check_red_flags, get_red_flag_response


def load_prompt_template(file_path: str) -> str:
    """Load prompt template from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def get_system_prompt() -> str:
    """Get system prompt for HealthGuide"""
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "system_prompt_healthguide.txt")
    prompt = load_prompt_template(prompt_path)
    if not prompt:
        # Fallback prompt
        prompt = """You are HealthGuide, a compassionate and cautious AI assistant for the Fever Helpline.

Core Principles:
1. Safety First - always prioritize user safety
2. Empathy - show care and understanding
3. Clarity - use simple, non-medical jargon
4. Action-Oriented - end each response with a clear next step

You are NOT a doctor and cannot provide a diagnosis. You only provide triage-level guidance.

Always ask one question at a time. Be empathetic and clear."""
    return prompt


def get_triage_prompt() -> str:
    """Get triage prompt template"""
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "triage_prompt.txt")
    prompt = load_prompt_template(prompt_path)
    if not prompt:
        # Fallback prompt
        prompt = """Based on the conversation history, assess the situation and provide:
1. Triage level (EMERGENCY, URGENT, SELF_CARE, or FOLLOW_UP)
2. Whether to escalate to emergency care
3. A brief summary
4. Recommended next steps
5. Next question to ask (if conversation not complete)

Respond in JSON format."""
    return prompt


class LLMService:
    """LLM service for HealthGuide"""
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or settings.llm_provider
        if self.provider == "openai":
            # Check if API key is valid (not empty or placeholder)
            if not settings.openai_api_key or settings.openai_api_key in ["", "your_key_here", "your-api-key"]:
                raise ValueError("OpenAI API key not found or invalid")
            self.client = OpenAI(api_key=settings.openai_api_key)
        elif self.provider == "gemini":
            if not settings.gemini_api_key or settings.gemini_api_key in ["", "your_key_here", "your-api-key"]:
                raise ValueError("Gemini API key not found or invalid")
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def generate_response(self, messages: List[Message], conversation_history: List[Dict]) -> str:
        """Generate response using LLM"""
        if self.provider == "openai":
            return self._generate_openai_response(messages, conversation_history)
        elif self.provider == "gemini":
            return self._generate_gemini_response(messages, conversation_history)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _generate_openai_response(self, messages: List[Message], conversation_history: List[Dict]) -> str:
        """Generate response using OpenAI"""
        system_prompt = get_system_prompt()
        
        # Format messages for OpenAI
        formatted_messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation_history:
            formatted_messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current message
        if messages:
            formatted_messages.append({
                "role": messages[-1].role,
                "content": messages[-1].content
            })
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Please try again. Error: {str(e)}"
    
    def _generate_gemini_response(self, messages: List[Message], conversation_history: List[Dict]) -> str:
        """Generate response using Gemini"""
        system_prompt = get_system_prompt()
        
        # Build conversation context
        context = system_prompt + "\n\nConversation History:\n"
        for msg in conversation_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            context += f"{role}: {content}\n"
        
        if messages:
            context += f"\nUser: {messages[-1].content}\n\nAssistant:"
        
        try:
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Please try again. Error: {str(e)}"
    
    def assess_triage(self, conversation_history: List[Dict], current_message: str) -> TriageResult:
        """Assess triage level and generate recommendations"""
        # Check for red flags first
        red_flag = check_red_flags(current_message)
        if red_flag:
            return TriageResult(
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
            )
        
        # Use LLM for triage assessment
        try:
            # Build context from conversation
            context = "Conversation History:\n"
            for msg in conversation_history:
                context += f"{msg.get('role', 'user')}: {msg.get('content', '')}\n"
            context += f"\nCurrent message: {current_message}\n\n"
            context += get_triage_prompt()
            
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": get_system_prompt()},
                        {"role": "user", "content": context}
                    ],
                    temperature=0.7,
                    response_format={"type": "json_object"}
                )
                result_json = json.loads(response.choices[0].message.content)
            else:  # gemini
                prompt = get_system_prompt() + "\n\n" + context + "\n\nRespond in JSON format only."
                response = self.model.generate_content(prompt)
                result_json = json.loads(response.text)
            
            # Parse JSON response
            triage_level = TriageLevel(result_json.get("triage_level", "FOLLOW_UP"))
            return TriageResult(
                triage_level=triage_level,
                escalate=result_json.get("escalate", False),
                summary=result_json.get("summary", "Fever-related symptoms detected"),
                recommended_next_steps=result_json.get("recommended_next_steps", []),
                next_question=result_json.get("next_question"),
                red_flag_detected=False
            )
        except Exception as e:
            # Fallback to safe default
            return TriageResult(
                triage_level=TriageLevel.FOLLOW_UP,
                escalate=False,
                summary="Fever symptoms reported. Please consult with a healthcare provider.",
                recommended_next_steps=[
                    "Monitor your symptoms",
                    "Stay hydrated",
                    "Get plenty of rest",
                    "Consult a healthcare provider if symptoms persist or worsen"
                ],
                next_question="Is there anything else you'd like to tell me about your symptoms?",
                red_flag_detected=False
            )


# Initialize LLM service (lazy loading with provider support)
_llm_services: Dict[str, LLMService] = {}


def get_llm_service(provider: Optional[str] = None) -> LLMService:
    """Get LLM service instance for the specified provider"""
    # Use provider from parameter, or fall back to settings default
    provider = provider or settings.llm_provider
    
    # Check if we already have a service instance for this provider
    if provider in _llm_services:
        return _llm_services[provider]
    
    # Try to create a new service instance for this provider
    try:
        service = LLMService(provider=provider)
        _llm_services[provider] = service
        print(f"✅ Initialized LLM service with provider: {provider}")
        return service
    except ValueError as e:
        print(f"⚠️  Warning: {e}. Using mock LLM service for provider: {provider}")
        # Use mock service if API key is not configured
        _llm_services[provider] = MockLLMService()
        return _llm_services[provider]


class MockLLMService:
    """Mock LLM service for testing without API keys"""
    
    def generate_response(self, messages: List[Message], conversation_history: List[Dict]) -> str:
        """Generate mock response"""
        return "I understand you're concerned about a fever. Let me help you assess your situation. Can you tell me your current body temperature?"
    
    def assess_triage(self, conversation_history: List[Dict], current_message: str) -> TriageResult:
        """Assess triage with mock logic"""
        red_flag = check_red_flags(current_message)
        if red_flag:
            return TriageResult(
                triage_level=TriageLevel.EMERGENCY,
                escalate=True,
                summary=f"Red flag symptom detected: {red_flag}",
                recommended_next_steps=[
                    "Call emergency services immediately",
                    "Go to the nearest emergency room"
                ],
                red_flag_detected=True,
                red_flag_symptom=red_flag
            )
        
        # Simple rule-based triage
        message_lower = current_message.lower()
        if any(word in message_lower for word in ["high", "very hot", "103", "104", "105"]):
            return TriageResult(
                triage_level=TriageLevel.URGENT,
                escalate=True,
                summary="High fever detected",
                recommended_next_steps=[
                    "Take fever-reducing medication if not allergic",
                    "Stay hydrated",
                    "Consult a healthcare provider soon"
                ],
                next_question="How long have you been experiencing this fever?"
            )
        
        return TriageResult(
            triage_level=TriageLevel.SELF_CARE,
            escalate=False,
            summary="Mild fever symptoms",
            recommended_next_steps=[
                "Rest and stay hydrated",
                "Monitor your temperature",
                "Consult a doctor if symptoms persist"
            ],
            next_question="Are you experiencing any other symptoms?"
        )

