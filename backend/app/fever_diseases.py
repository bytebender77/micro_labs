"""Disease-specific fever detection and pattern matching"""
from typing import Dict, List, Optional


FEVER_PATTERNS = {
    "dengue": {
        "keywords": ["rash", "joint pain", "eye pain", "bleeding gums", "platelet", "petechiae", "bleeding"],
        "duration": "5-7 days",
        "symptoms": ["high fever", "severe headache", "pain behind eyes", "muscle pain", "bone pain"],
        "alert": "Monitor platelet count, watch for bleeding signs. Seek medical attention if bleeding occurs.",
        "severity": "high"
    },
    "malaria": {
        "keywords": ["chills", "sweating", "cyclic fever", "shivering", "rigor"],
        "duration": "2-3 days cycles",
        "symptoms": ["fever with chills", "headache", "nausea", "muscle pain", "fatigue"],
        "alert": "Requires antimalarial treatment within 48 hours. Can be life-threatening if untreated.",
        "severity": "high"
    },
    "typhoid": {
        "keywords": ["step-ladder fever", "rose spots", "abdominal pain", "constipation", "diarrhea"],
        "duration": "7-14 days",
        "symptoms": ["prolonged fever", "weakness", "stomach pain", "headache", "loss of appetite"],
        "alert": "Requires antibiotic treatment. Can cause complications if untreated.",
        "severity": "high"
    },
    "viral": {
        "keywords": ["cold", "cough", "sore throat", "runny nose", "body ache"],
        "duration": "3-5 days",
        "symptoms": ["mild fever", "body ache", "fatigue", "headache"],
        "alert": "Usually self-limiting, supportive care recommended. Rest and hydration.",
        "severity": "low"
    },
    "flu": {
        "keywords": ["influenza", "body ache", "fatigue", "cough", "sore throat"],
        "duration": "5-7 days",
        "symptoms": ["fever", "chills", "body ache", "fatigue", "cough"],
        "alert": "Rest, hydration, and symptomatic treatment. Antiviral medication may help if started early.",
        "severity": "medium"
    },
    "covid": {
        "keywords": ["covid", "coronavirus", "loss of taste", "loss of smell", "shortness of breath"],
        "duration": "7-14 days",
        "symptoms": ["fever", "cough", "shortness of breath", "fatigue", "loss of taste or smell"],
        "alert": "Isolate immediately. Monitor oxygen levels. Seek medical attention if breathing difficulties occur.",
        "severity": "high"
    }
}


def identify_fever_type(symptoms: str, temperature: Optional[float] = None) -> Dict:
    """
    Identify likely fever type based on symptoms and temperature
    
    Args:
        symptoms: String containing symptoms description
        temperature: Optional temperature in Fahrenheit
    
    Returns:
        Dictionary with likely disease type, confidence, and information
    """
    symptoms_lower = symptoms.lower()
    scores = {}
    
    # Score each disease pattern
    for disease, pattern in FEVER_PATTERNS.items():
        score = 0
        keyword_matches = []
        
        # Check keyword matches
        for keyword in pattern["keywords"]:
            if keyword in symptoms_lower:
                score += 1
                keyword_matches.append(keyword)
        
        # Check symptom matches
        for symptom in pattern["symptoms"]:
            if symptom in symptoms_lower:
                score += 2  # Symptoms are weighted higher than keywords
                keyword_matches.append(symptom)
        
        # Temperature-based scoring
        if temperature:
            if disease == "dengue" and temperature > 103:
                score += 1
            elif disease == "malaria" and 100 < temperature < 104:
                score += 1
            elif disease == "typhoid" and temperature > 102:
                score += 1
        
        if score > 0:
            scores[disease] = {
                "score": score,
                "matches": keyword_matches,
                "pattern": pattern
            }
    
    # Determine most likely disease
    if not scores:
        # Default to viral if no matches
        likely_disease = "viral"
        confidence = 0.3
        info = FEVER_PATTERNS["viral"]
    else:
        likely_disease = max(scores, key=lambda x: scores[x]["score"])
        max_score = scores[likely_disease]["score"]
        total_possible = len(FEVER_PATTERNS[likely_disease]["keywords"]) + len(FEVER_PATTERNS[likely_disease]["symptoms"])
        confidence = min(max_score / total_possible, 1.0)
        info = scores[likely_disease]["pattern"]
    
    return {
        "likely_type": likely_disease,
        "confidence": round(confidence, 2),
        "info": info,
        "all_scores": {k: v["score"] for k, v in scores.items()} if scores else {}
    }


def get_disease_recommendations(disease_type: str) -> List[str]:
    """Get specific recommendations for a disease type"""
    if disease_type not in FEVER_PATTERNS:
        return []
    
    pattern = FEVER_PATTERNS[disease_type]
    recommendations = [
        f"Likely condition: {disease_type.upper()}",
        f"Typical duration: {pattern['duration']}",
        f"Alert: {pattern['alert']}"
    ]
    
    if pattern["severity"] == "high":
        recommendations.append("⚠️ Seek medical attention promptly")
    elif pattern["severity"] == "medium":
        recommendations.append("Monitor symptoms closely")
    else:
        recommendations.append("Continue supportive care at home")
    
    return recommendations

