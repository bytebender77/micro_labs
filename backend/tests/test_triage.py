"""Tests for triage logic"""
import pytest
from app.models import TriageLevel
from app.llm_service import MockLLMService


def test_mock_llm_service():
    """Test mock LLM service"""
    service = MockLLMService()
    
    # Test normal conversation
    result = service.assess_triage([], "I have a mild fever")
    assert result.triage_level in [TriageLevel.SELF_CARE, TriageLevel.FOLLOW_UP]
    assert not result.red_flag_detected
    
    # Test high fever
    result = service.assess_triage([], "I have a very high fever, 104 degrees")
    assert result.triage_level == TriageLevel.URGENT
    assert result.escalate is True
    
    # Test red flag
    result = service.assess_triage([], "I have chest pain")
    assert result.triage_level == TriageLevel.EMERGENCY
    assert result.red_flag_detected is True


def test_conversation_flow():
    """Test conversation flow"""
    service = MockLLMService()
    
    conversation = [
        {"role": "user", "content": "I have a fever"},
        {"role": "assistant", "content": "What's your temperature?"}
    ]
    
    result = service.assess_triage(conversation, "101 degrees")
    assert result is not None
    assert result.triage_level is not None
    assert len(result.recommended_next_steps) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

