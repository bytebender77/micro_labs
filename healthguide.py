"""
HealthGuide - Fever Helpline AI Assistant
A compassionate and cautious triage tool for fever-related concerns.
"""

import re
from typing import List, Dict, Optional

# Red flag symptoms that require immediate emergency care
RED_FLAG_SYMPTOMS = {
    "severe difficulty breathing": [
        "severe difficulty breathing", "can't breathe", "cannot breathe", 
        "trouble breathing", "difficulty breathing", "shortness of breath",
        "struggling to breathe", "hard to breathe", "breathing problems"
    ],
    "chest pain or pressure": [
        "chest pain", "chest pressure", "chest tightness", "chest discomfort",
        "pressure in chest", "pain in chest", "tight chest"
    ],
    "confusion or inability to stay awake": [
        "confusion", "confused", "can't stay awake", "cannot stay awake",
        "unable to stay awake", "drowsy", "unconscious", "passed out",
        "disoriented", "mental confusion"
    ],
    "bluish lips or face": [
        "blue lips", "bluish lips", "blue face", "bluish face", "cyanosis",
        "lips turning blue", "face turning blue", "blue skin"
    ],
    "severe dehydration": [
        "no urine", "no urination", "haven't urinated", "no urine for",
        "sunken eyes", "severe dehydration", "severely dehydrated",
        "8 hours", "8+ hours", "no urine for 8"
    ],
    "seizure": [
        "seizure", "seizures", "convulsion", "convulsions", "fitting",
        "having a seizure", "had a seizure"
    ],
    "severe headache or stiff neck with light sensitivity": [
        "severe headache", "stiff neck", "light sensitivity", "photophobia",
        "sensitive to light", "neck stiffness", "severe head pain",
        "stiff neck and light"
    ],
    "rash that does not fade under pressure": [
        "rash that does not fade", "rash doesn't fade", "non-blanching rash",
        "petechiae", "rash that won't fade", "rash that doesn't fade under pressure"
    ]
}

DISCLAIMER = (
    "I am an AI assistant, not a medical professional. My advice is for informational "
    "purposes only and is not a substitute for professional medical diagnosis or treatment. "
    "Always consult a human doctor for serious symptoms."
)


class HealthGuide:
    """AI Assistant for Fever Helpline Triage"""
    
    def __init__(self):
        self.user_responses = {}
        self.red_flag_detected = False
        
    def check_red_flags(self, user_input: str) -> Optional[str]:
        """
        Check if user input contains any red flag symptoms.
        Returns the red flag symptom if found, None otherwise.
        This check is performed FIRST before any other processing.
        """
        user_input_lower = user_input.lower()
        
        # Check each red flag symptom category
        for symptom, keywords in RED_FLAG_SYMPTOMS.items():
            for keyword in keywords:
                if keyword.lower() in user_input_lower:
                    return symptom
        return None
    
    def greet_user(self) -> str:
        """Initial greeting with disclaimer"""
        greeting = (
            f"{DISCLAIMER}\n\n"
            "Hello! I'm HealthGuide, your AI assistant for the Fever Helpline. "
            "I'm here to help you understand your symptoms and guide you on what to do next.\n\n"
            "I understand you're concerned about a fever. Let me ask you a few questions to better understand your situation.\n\n"
            "First, can you tell me about your symptoms? What are you experiencing right now?"
        )
        return greeting
    
    def handle_red_flag(self, symptom: str) -> str:
        """Handle detection of red flag symptom"""
        self.red_flag_detected = True
        response = (
            f"\n⚠️  URGENT: I've detected a potential red flag symptom: {symptom}.\n\n"
            "**Please seek emergency medical care immediately.**\n\n"
            "• Call your local emergency number (e.g., 911, 999, 112)\n"
            "• Go to the nearest emergency room\n"
            "• Do not delay seeking medical attention\n\n"
            f"{DISCLAIMER}\n"
        )
        return response
    
    def ask_temperature(self) -> str:
        """Ask about body temperature"""
        return (
            "\nThank you for that information. To better assess your situation, "
            "do you know your current body temperature? If you have a thermometer, "
            "what reading did you get? (Please share the number in Fahrenheit or Celsius)"
        )
    
    def ask_duration(self) -> str:
        """Ask about duration of fever"""
        return (
            "\nHow long have you been experiencing this fever? "
            "(For example: a few hours, 1 day, 2 days, etc.)"
        )
    
    def ask_age_group(self) -> str:
        """Ask about age group"""
        return (
            "\nTo provide appropriate guidance, may I ask which age group applies to you?\n"
            "• Infant (under 1 year)\n"
            "• Child (1-12 years)\n"
            "• Teenager (13-17 years)\n"
            "• Adult (18-64 years)\n"
            "• Senior (65+ years)"
        )
    
    def ask_additional_symptoms(self) -> str:
        """Ask about additional symptoms"""
        return (
            "\nAre you experiencing any other symptoms? For example:\n"
            "• Cough\n"
            "• Sore throat\n"
            "• Body aches\n"
            "• Fatigue\n"
            "• Nausea or vomiting\n"
            "• Diarrhea\n"
            "• Chills\n"
            "• Sweating\n\n"
            "Please describe any other symptoms you're having."
        )
    
    def provide_guidance(self, temperature: Optional[float] = None, 
                        age_group: Optional[str] = None,
                        duration: Optional[str] = None) -> str:
        """
        Provide guidance based on collected information.
        This is a simplified version - in a real system, this would be more comprehensive.
        """
        guidance = "\n\nBased on the information you've provided:\n\n"
        
        # Temperature-based guidance
        if temperature:
            if temperature >= 103.0:  # Fahrenheit (38.3°C)
                guidance += (
                    "⚠️ Your temperature is quite high. It's important to:\n"
                    "• Take fever-reducing medication as directed (if not allergic)\n"
                    "• Stay hydrated by drinking plenty of fluids\n"
                    "• Rest in a cool, comfortable environment\n"
                    "• Monitor your symptoms closely\n\n"
                )
            elif temperature >= 100.4:  # Fahrenheit (38°C)
                guidance += (
                    "You have a fever. Consider:\n"
                    "• Resting and staying hydrated\n"
                    "• Taking fever-reducing medication if needed (if not allergic)\n"
                    "• Monitoring your symptoms\n\n"
                )
            else:
                guidance += (
                    "Your temperature is within normal range, but you're experiencing symptoms. "
                    "It's still important to monitor and rest.\n\n"
                )
        
        # Age-specific guidance
        if age_group:
            if age_group.lower() in ["infant", "child"]:
                guidance += (
                    "⚠️ For infants and children, fevers can be more concerning. "
                    "It's especially important to monitor closely and consult with a pediatrician "
                    "if symptoms persist or worsen.\n\n"
                )
            elif age_group.lower() == "senior":
                guidance += (
                    "⚠️ For seniors, fevers may require closer monitoring. "
                    "Please consult with a healthcare provider, especially if symptoms persist.\n\n"
                )
        
        # Duration-based guidance
        if duration:
            duration_lower = duration.lower()
            if "day" in duration_lower and any(char.isdigit() for char in duration):
                days = [int(s) for s in duration.split() if s.isdigit()]
                if days and days[0] >= 3:
                    guidance += (
                        "⚠️ Since your fever has persisted for several days, "
                        "it's advisable to consult with a healthcare provider.\n\n"
                    )
            elif "week" in duration_lower:
                guidance += (
                    "⚠️ Since your symptoms have persisted for a week or more, "
                    "it's important to consult with a healthcare provider.\n\n"
                )
        
        guidance += (
            "**Next Steps:**\n"
            "• Continue monitoring your symptoms\n"
            "• Stay well-hydrated\n"
            "• Get plenty of rest\n"
            "• If symptoms worsen or persist, contact a healthcare provider\n"
            "• If you develop any red flag symptoms, seek emergency care immediately\n\n"
        )
        
        # Note: Disclaimer will be added at the end of first interaction in main()
        
        return guidance
    
    def extract_temperature(self, user_input: str) -> Optional[float]:
        """Extract temperature from user input"""
        # Try various temperature patterns
        patterns = [
            r'(\d+\.?\d*)\s*(?:degrees?|°)\s*(?:F|fahrenheit)',
            r'(\d+\.?\d*)\s*(?:degrees?|°)\s*(?:C|celsius)',
            r'(\d+\.?\d*)\s*(?:F|fahrenheit)',
            r'(\d+\.?\d*)\s*(?:C|celsius)',
            r'(\d+\.?\d*)\s*(?:degrees?|°)',
            r'(\d+\.?\d*)',  # Just a number, assume Fahrenheit
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                temp_value = float(match.group(1))
                # If Celsius, convert to Fahrenheit
                if 'c' in pattern.lower() or 'celsius' in user_input.lower():
                    temp_value = (temp_value * 9/5) + 32
                return temp_value
        return None
    
    def extract_age_group(self, user_input: str) -> Optional[str]:
        """Extract age group from user input"""
        user_input_lower = user_input.lower()
        if any(word in user_input_lower for word in ['infant', 'baby', 'newborn']):
            return 'infant'
        elif any(word in user_input_lower for word in ['child', 'kid', 'children']):
            return 'child'
        elif any(word in user_input_lower for word in ['teen', 'teenager', 'adolescent']):
            return 'teenager'
        elif any(word in user_input_lower for word in ['adult', 'grown']):
            return 'adult'
        elif any(word in user_input_lower for word in ['senior', 'elderly', 'old']):
            return 'senior'
        return None
    
    def process_user_input(self, user_input: str, conversation_stage: str = "initial") -> tuple:
        """
        Process user input and determine appropriate response.
        Returns (response_text, should_end, next_stage)
        """
        # ALWAYS check for red flags FIRST - this is critical
        red_flag = self.check_red_flags(user_input)
        if red_flag:
            self.red_flag_detected = True
            return self.handle_red_flag(red_flag), True, None
        
        # If red flag was already detected, don't continue
        if self.red_flag_detected:
            return "", True, None
        
        # Extract information from user input
        temp = self.extract_temperature(user_input)
        if temp is not None:
            self.user_responses['temperature'] = temp
        
        age = self.extract_age_group(user_input)
        if age is not None:
            self.user_responses['age_group'] = age
        
        # Store duration if mentioned
        if any(word in user_input.lower() for word in ['hour', 'day', 'week', 'minute']):
            self.user_responses['duration'] = user_input
        
        # Determine next question based on conversation stage
        if conversation_stage == "initial":
            # Store initial symptoms
            self.user_responses['initial_symptoms'] = user_input
            return self.ask_temperature(), False, "temperature"
        
        elif conversation_stage == "temperature":
            # If temperature not extracted, ask again
            if 'temperature' not in self.user_responses:
                return (
                    "\nI didn't catch your temperature. Could you please share it? "
                    "For example: '101 degrees' or '38.5 Celsius'",
                    False, "temperature"
                )
            return self.ask_duration(), False, "duration"
        
        elif conversation_stage == "duration":
            if 'duration' not in self.user_responses:
                self.user_responses['duration'] = user_input
            return self.ask_age_group(), False, "age"
        
        elif conversation_stage == "age":
            if 'age_group' not in self.user_responses:
                # Try to extract from input
                age = self.extract_age_group(user_input)
                if age:
                    self.user_responses['age_group'] = age
                else:
                    return (
                        "\nI didn't catch your age group. Please select one: "
                        "Infant, Child, Teenager, Adult, or Senior",
                        False, "age"
                    )
            return self.ask_additional_symptoms(), False, "symptoms"
        
        elif conversation_stage == "symptoms":
            # Store additional symptoms
            self.user_responses['additional_symptoms'] = user_input
            # Provide final guidance
            response_text = self.provide_guidance(
                temperature=self.user_responses.get('temperature'),
                age_group=self.user_responses.get('age_group'),
                duration=self.user_responses.get('duration')
            )
            return response_text, True, None
        
        return "", False, conversation_stage


def main():
    """Main function to run the HealthGuide assistant"""
    print("=" * 70)
    print("HealthGuide - Fever Helpline AI Assistant")
    print("=" * 70)
    print()
    
    guide = HealthGuide()
    is_first_complete_interaction = True
    
    # Initial greeting
    print(guide.greet_user())
    print()
    
    conversation_stage = "initial"
    conversation_ended = False
    
    while not conversation_ended:
        # Get user input
        user_input = input("You: ").strip()
        
        if not user_input:
            print("\nPlease provide some information so I can help you.")
            continue
        
        # Process input
        response, should_end, next_stage = guide.process_user_input(user_input, conversation_stage)
        
        if response:
            print(f"\nHealthGuide: {response}\n")
        
        if should_end:
            conversation_ended = True
            # Add disclaimer at the end of first complete interaction (if not already in response)
            if is_first_complete_interaction and not guide.red_flag_detected and DISCLAIMER not in response:
                print(f"\n{DISCLAIMER}\n")
            break
        
        # Update conversation stage
        if next_stage:
            conversation_stage = next_stage
        elif conversation_stage == "initial":
            conversation_stage = "temperature"
        elif conversation_stage == "temperature":
            conversation_stage = "duration"
        elif conversation_stage == "duration":
            conversation_stage = "age"
        elif conversation_stage == "age":
            conversation_stage = "symptoms"
        elif conversation_stage == "symptoms":
            conversation_ended = True
    
    print("\n" + "=" * 70)
    print("Thank you for using HealthGuide. Take care!")
    print("=" * 70)


if __name__ == "__main__":
    main()

