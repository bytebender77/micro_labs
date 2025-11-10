"""Tests for red flag detection"""
import pytest
from app.red_flags import check_red_flags, get_red_flag_response


def test_chest_pain_red_flag():
    """Test detection of chest pain red flag"""
    result = check_red_flags("I have chest pain and fever")
    assert result == "chest pain or pressure"


def test_breathing_difficulty_red_flag():
    """Test detection of breathing difficulty red flag"""
    result = check_red_flags("I can't breathe properly")
    assert result == "severe difficulty breathing"


def test_seizure_red_flag():
    """Test detection of seizure red flag"""
    result = check_red_flags("I had a seizure")
    assert result == "seizure"


def test_no_red_flag():
    """Test that normal symptoms don't trigger red flags"""
    result = check_red_flags("I have a mild fever and feel tired")
    assert result is None


def test_dehydration_red_flag():
    """Test detection of dehydration red flag"""
    result = check_red_flags("I haven't urinated for 8 hours")
    assert result == "severe dehydration"


def test_red_flag_response():
    """Test red flag response generation"""
    response = get_red_flag_response("chest pain or pressure")
    assert "URGENT" in response
    assert "emergency" in response.lower()
    assert "chest pain" in response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

