"""Database setup and session management"""
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from typing import Optional, List
import json

from app.config import settings

Base = declarative_base()


class ConversationSession(Base):
    """Database model for conversation sessions"""
    __tablename__ = "conversations"
    
    session_id = Column(String, primary_key=True, index=True)
    messages = Column(JSON, default=list)
    triage_level = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    red_flag_detected = Column(String, nullable=True)
    
    # Relationship to temperature logs
    temperature_logs = relationship("TemperatureLog", back_populates="session", cascade="all, delete-orphan")


class TemperatureLog(Base):
    """Database model for temperature tracking"""
    __tablename__ = "temperature_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("conversations.session_id"), nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    unit = Column(String, default="F")  # 'F' or 'C'
    recorded_at = Column(DateTime, default=datetime.now, index=True)
    notes = Column(Text, nullable=True)
    
    # Relationship to conversation session
    session = relationship("ConversationSession", back_populates="temperature_logs")


# Create database engine
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def save_conversation(db: Session, session_id: str, messages: list, triage_level: Optional[str] = None, 
                     summary: Optional[str] = None, red_flag: Optional[str] = None):
    """Save or update conversation session"""
    session = db.query(ConversationSession).filter(ConversationSession.session_id == session_id).first()
    
    if session:
        session.messages = messages
        session.triage_level = triage_level
        session.summary = summary
        session.red_flag_detected = red_flag
        session.updated_at = datetime.now()
    else:
        session = ConversationSession(
            session_id=session_id,
            messages=messages,
            triage_level=triage_level,
            summary=summary,
            red_flag_detected=red_flag
        )
        db.add(session)
    
    db.commit()
    return session


def get_conversation(db: Session, session_id: str) -> Optional[ConversationSession]:
    """Get conversation session by ID"""
    return db.query(ConversationSession).filter(ConversationSession.session_id == session_id).first()


def save_temperature(db: Session, session_id: str, temperature: float, unit: str = "F", notes: Optional[str] = None) -> TemperatureLog:
    """Save temperature reading to database"""
    temp_log = TemperatureLog(
        session_id=session_id,
        temperature=temperature,
        unit=unit,
        notes=notes,
        recorded_at=datetime.now()
    )
    db.add(temp_log)
    db.commit()
    db.refresh(temp_log)
    return temp_log


def get_temperature_history(db: Session, session_id: str, limit: int = 50) -> List[TemperatureLog]:
    """Get temperature history for a session"""
    return db.query(TemperatureLog).filter(
        TemperatureLog.session_id == session_id
    ).order_by(
        TemperatureLog.recorded_at.desc()
    ).limit(limit).all()

