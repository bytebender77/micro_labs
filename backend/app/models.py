"""Data models for HealthGuide"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from datetime import datetime
from enum import Enum


class TriageLevel(str, Enum):
    """Triage level classification"""
    EMERGENCY = "EMERGENCY"
    URGENT = "URGENT"
    SELF_CARE = "SELF_CARE"
    FOLLOW_UP = "FOLLOW_UP"


class Message(BaseModel):
    """Chat message model"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class TriageResult(BaseModel):
    """Triage assessment result"""
    triage_level: TriageLevel
    escalate: bool
    summary: str
    recommended_next_steps: List[str]
    next_question: Optional[str] = None
    red_flag_detected: bool = False
    red_flag_symptom: Optional[str] = None


class SymptomData(BaseModel):
    """Structured symptom data from symptom selector"""
    symptoms: List[str] = []
    by_category: Optional[Dict[str, List[str]]] = None
    emergency_detected: bool = False
    total_selected: int = 0
    language: Optional[str] = "en"


class ConversationRequest(BaseModel):
    """Request model for triage endpoint"""
    session_id: str
    message: str
    conversation_history: List[Message] = []
    llm_provider: Optional[str] = "openai"  # openai or gemini
    symptom_data: Optional[SymptomData] = None  # Optional structured symptom data


class ConversationResponse(BaseModel):
    """Response model for triage endpoint"""
    session_id: str
    message: str
    triage_result: Optional[TriageResult] = None
    conversation_complete: bool = False


class Provider(BaseModel):
    """Healthcare provider model"""
    id: str
    name: str
    type: str  # clinic, pharmacy, hospital
    address: str
    phone: str
    distance: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ProviderRequest(BaseModel):
    """Request model for providers endpoint"""
    latitude: float
    longitude: float
    radius: int = 5  # km
    provider_type: Optional[str] = None  # clinic, pharmacy, hospital


class SummaryResponse(BaseModel):
    """Response model for summary endpoint"""
    session_id: str
    summary: str
    triage_level: TriageLevel
    recommended_next_steps: List[str]
    conversation_count: int

