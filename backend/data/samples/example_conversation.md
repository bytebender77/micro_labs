# Example Conversation - HealthGuide

## Scenario: Mild Fever

### Conversation Flow

**User**: I have a fever and feel really tired

**HealthGuide**: Hello! I'm HealthGuide, your AI assistant for the Fever Helpline. I understand you're concerned about a fever. Can you tell me about your symptoms? What are you experiencing right now?

**User**: I have a fever and feel really tired

**HealthGuide**: Thank you for that information. To better assess your situation, do you know your current body temperature? If you have a thermometer, what reading did you get?

**User**: It's 101.5 degrees Fahrenheit

**HealthGuide**: Thank you. How long have you been experiencing this fever?

**User**: About 2 days now

**HealthGuide**: I see. To provide appropriate guidance, may I ask which age group applies to you?

**User**: I'm an adult

**HealthGuide**: Thank you. Are you experiencing any other symptoms?

**User**: Just a headache and some body aches

**HealthGuide**: Based on the information you've provided:

**Summary**: Moderate fever (101.5°F) persisting for 2 days in an adult with headache and body aches. No red flag symptoms detected.

**Triage Level**: SELF_CARE

**Recommended Next Steps**:
- Rest and stay hydrated
- Take fever-reducing medication if needed (if not allergic)
- Monitor your temperature
- If your fever persists beyond 3 days or worsens, consult a healthcare provider

---

## Scenario: Red Flag - Chest Pain

### Conversation Flow

**User**: I have a fever and chest pain

**HealthGuide**: ⚠️ URGENT: I've detected a potential red flag symptom: chest pain or pressure.

**This may be serious. Please call emergency services or go to the nearest emergency department now. I am not a doctor.**

- Call your local emergency number (e.g., 911, 999, 112)
- Go to the nearest emergency room
- Do not delay seeking medical attention

---

## Scenario: High Fever

### Conversation Flow

**User**: I have a very high fever

**HealthGuide**: Hello! I'm HealthGuide, your AI assistant for the Fever Helpline. I understand you're concerned about a fever. Can you tell me about your symptoms? What are you experiencing right now?

**User**: I have a very high fever

**HealthGuide**: Thank you for that information. To better assess your situation, do you know your current body temperature?

**User**: 104 degrees

**HealthGuide**: ⚠️ Your temperature is quite high. This requires urgent attention.

**Triage Level**: URGENT

**Recommended Next Steps**:
- Take fever-reducing medication as directed (if not allergic)
- Stay hydrated by drinking plenty of fluids
- Rest in a cool, comfortable environment
- Monitor your symptoms closely
- **Consult a healthcare provider immediately**

---

## Scenario: Infant Fever

### Conversation Flow

**User**: My baby has a fever

**HealthGuide**: Hello! I'm HealthGuide, your AI assistant for the Fever Helpline. I understand you're concerned about a fever. Can you tell me about your symptoms? What are you experiencing right now?

**User**: My baby has a fever

**HealthGuide**: Thank you for that information. To better assess your situation, do you know your baby's current body temperature?

**User**: 100.8 degrees

**HealthGuide**: How long has your baby been experiencing this fever?

**User**: Since this morning

**HealthGuide**: ⚠️ For infants and children, fevers can be more concerning. It's especially important to monitor closely and consult with a pediatrician if symptoms persist or worsen.

**Triage Level**: FOLLOW_UP

**Recommended Next Steps**:
- Monitor your baby's temperature closely
- Keep your baby hydrated
- Consult with a pediatrician if the fever persists or worsens
- Watch for any red flag symptoms

---

## Triage Level Examples

### EMERGENCY
- Red flag symptoms present
- Requires immediate emergency care
- Examples: Chest pain, difficulty breathing, seizure

### URGENT
- High fever (>103°F)
- Persistent symptoms
- Concerning factors
- Examples: High fever, severe symptoms, multiple days

### SELF_CARE
- Mild symptoms
- Low-grade fever
- Can be managed at home
- Examples: Mild fever, no red flags, good overall condition

### FOLLOW_UP
- Symptoms to monitor
- May require follow-up
- Examples: Persistent low-grade fever, mild symptoms

