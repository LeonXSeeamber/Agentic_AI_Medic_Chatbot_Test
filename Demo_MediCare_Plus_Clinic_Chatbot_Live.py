import os
import json
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

chat = ChatOpenAI(
                  model="gpt-3.5-turbo", 
                  temperature=0, 
                  openai_api_key=os.getenv("OPENAI_API_KEY")
                  )

# Sentiment Analyzer Initialization
analyzer = SentimentIntensityAnalyzer()

#========================================================================================================================================================
#========================================================================================================================================================
# Patient Database & Clinic FAQ Knowledge Base

PATIENTS_DB = {
    "P001": {
        "name": "María García",
        "email": "maria.garcia@email.com",
        "phone": "+34 612 345 678",
        "date_of_birth": "1985-03-15",
        "membership_type": "Premium",
        "balance_due": 45.00,
        "upcoming_appointments": [
            {
                "date": "2024-02-15",
                "time": "10:30",
                "doctor": "Dr. Fernández",
                "specialty": "General Medicine",
                "status": "confirmed"
            },
            {
                "date": "2024-03-01",
                "time": "16:00",
                "doctor": "Dr. López",
                "specialty": "Dermatology",
                "status": "pending_confirmation"
            }
        ],
        "last_visit": "2024-01-20",
        "primary_doctor": "Dr. Fernández",
        "allergies": ["Penicillin"],
        "insurance_provider": "Sanitas"
    },
    "P002": {
        "name": "Carlos Rodríguez",
        "email": "carlos.r@email.com",
        "phone": "+34 698 765 432",
        "date_of_birth": "1972-11-28",
        "membership_type": "Basic",
        "balance_due": 0.00,
        "upcoming_appointments": [],
        "last_visit": "2023-11-05",
        "primary_doctor": "Dr. Martín",
        "allergies": [],
        "insurance_provider": "Adeslas"
    },
    "P003": {
        "name": "Ana Belén Torres",
        "email": "anabelen.t@email.com",
        "phone": "+34 655 123 789",
        "date_of_birth": "1990-07-22",
        "membership_type": "Premium",
        "balance_due": 120.50,
        "upcoming_appointments": [
            {
                "date": "2024-02-10",
                "time": "09:00",
                "doctor": "Dr. Sánchez",
                "specialty": "Gynecology",
                "status": "confirmed"
            }
        ],
        "last_visit": "2024-01-28",
        "primary_doctor": "Dr. Sánchez",
        "allergies": ["Ibuprofen", "Latex"],
        "insurance_provider": "Mapfre"
    }
}


CLINIC_FAQS = {
    "FAQ001": {
        "category": "Appointments",
        "question": "How can I schedule an appointment?",
        "answer": "You can schedule an appointment through our online portal at medicare-plus.com/appointments, by calling our reception at +34 911 234 567 (Monday to Friday, 8:00-20:00), or through this chat by requesting to speak with our scheduling team."
    },
    "FAQ002": {
        "category": "Appointments",
        "question": "What is the cancellation policy?",
        "answer": "Appointments must be cancelled at least 24 hours in advance to avoid a €20 cancellation fee. Premium members can cancel up to 12 hours before without penalty. To cancel, use our online portal or call reception."
    },
    "FAQ003": {
        "category": "Appointments",
        "question": "How early should I arrive for my appointment?",
        "answer": "Please arrive 15 minutes before your scheduled appointment time. First-time patients should arrive 30 minutes early to complete registration paperwork."
    },
    "FAQ004": {
        "category": "Payments",
        "question": "What payment methods do you accept?",
        "answer": "We accept cash, credit/debit cards (Visa, Mastercard, American Express), bank transfers, and payment through major insurance providers (Sanitas, Adeslas, Mapfre, DKV, Asisa). Payment plans are available for treatments exceeding €500."
    },
    "FAQ005": {
        "category": "Payments",
        "question": "How can I check my balance or pay outstanding bills?",
        "answer": "You can view and pay your balance through our patient portal at medicare-plus.com/billing, by phone at +34 911 234 568 (billing department), or in person at our reception desk. We send monthly statements via email for any outstanding balances."
    },
    "FAQ006": {
        "category": "Insurance",
        "question": "Which insurance providers do you work with?",
        "answer": "We work with Sanitas, Adeslas, Mapfre, DKV, and Asisa. Coverage varies by plan. Please bring your insurance card to every visit. We recommend calling your insurance provider to verify coverage before specialized procedures."
    },
    "FAQ007": {
        "category": "Services",
        "question": "What medical specialties are available at the clinic?",
        "answer": "MediCare Plus offers: General Medicine, Pediatrics, Gynecology, Dermatology, Cardiology, Traumatology, Psychology, and Nutrition. Some specialists are only available on specific days. Contact reception for specialist schedules."
    },
    "FAQ008": {
        "category": "Services",
        "question": "Do you offer telemedicine consultations?",
        "answer": "Yes, we offer video consultations for General Medicine, Psychology, Nutrition, and follow-up appointments. Telemedicine is available for Premium members at no extra cost. Basic members pay €15 per video consultation. Book through our portal or call reception."
    },
    "FAQ009": {
        "category": "Hours & Location",
        "question": "What are the clinic's operating hours?",
        "answer": "Regular hours: Monday to Friday 8:00-20:00, Saturday 9:00-14:00. Closed on Sundays and public holidays. Extended hours available by appointment for Premium members."
    },
    "FAQ010": {
        "category": "Hours & Location",
        "question": "Where is the clinic located?",
        "answer": "We are located at Calle Serrano 125, 28006 Madrid. Nearest metro: Núñez de Balboa (Line 5, 9). Paid parking available at Parking Serrano (2-minute walk). Wheelchair accessible entrance on Calle Claudio Coello."
    },
    "FAQ011": {
        "category": "Emergencies",
        "question": "Do you handle medical emergencies?",
        "answer": "MediCare Plus is NOT an emergency facility. For medical emergencies, call 112 or go to the nearest hospital emergency room. For urgent but non-emergency same-day care, Premium members can request urgent appointments subject to availability."
    },
    "FAQ012": {
        "category": "Membership",
        "question": "What is the difference between Basic and Premium membership?",
        "answer": "Basic membership: Standard appointment scheduling, access to all specialists, email support. Premium membership (€29/month): Priority scheduling, 12-hour cancellation policy, free telemedicine, extended hours access, dedicated phone support line, and 10% discount on non-covered services."
    },
    "FAQ013": {
        "category": "Medical Records",
        "question": "How can I access my medical records?",
        "answer": "Access your records through our patient portal at medicare-plus.com/records. You can also request printed copies at reception (€5 processing fee, ready within 48 hours). For records to be sent to another provider, submit a signed authorization form."
    },
    "FAQ014": {
        "category": "Prescriptions",
        "question": "How do I request prescription refills?",
        "answer": "Prescription refills can be requested through the patient portal or by calling your doctor's office directly. Please allow 48-72 hours for processing. Controlled substances require an in-person appointment."
    },
    "FAQ015": {
        "category": "COVID-19",
        "question": "What COVID-19 protocols are in place?",
        "answer": "Masks are optional but recommended in waiting areas. Hand sanitizer stations are available throughout the clinic. If you have COVID-19 symptoms, please call before your visit to arrange appropriate care. Telemedicine is recommended for patients with respiratory symptoms."
    }
}
#========================================================================================================================================================
#========================================================================================================================================================

# emergency_checker - Function to detect emergency keywords in user input

def emergency_checker(text: str) -> bool:
    """
    Keyword check for immediate escalation
    """
    emergency_keywords = ["chest pain", "heart attack", "breathing", "unconscious", "emergency", "111", "999", "severe", "danger", "urgent","dying"]
    text_lower = text.lower()
    
    return any(k in text_lower for k in emergency_keywords)

#========================================================================================================================================================
#========================================================================================================================================================

# sentiment_checker - Function to detect high negative sentiment in user input

def sentiment_checker(text: str) -> bool:
    """
    Uses VADER to detect high negative sentiment (Anger/Frustration).
    Returns True if the score is below -0.5 (Highly Negative).
    """
    # Calculate polarity scores
    scores = analyzer.polarity_scores(text)
    
    # 'compound' is the overall score: -1 (Most Negative) to +1 (Most Positive)
    # A score below -0.5 typically indicates strong negative emotion/anger.
    if scores['compound'] < -0.47:
        return True
    
    return False

#========================================================================================================================================================
#========================================================================================================================================================

# generate_response - This is the main function that generates the chatbot response

def generate_response(user_id: str, current_message: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
    
    # 0. Emergency Check - 
    # Checks if the current message indicates an emergency
    # Abort chatbot immediately if it's an emergency 

    if emergency_checker(current_message):
        return {
            "response": "I have detected a possible medical emergency, transferring you to a human agent.",
            "escalate_to_human": True
        }
    
 #===================================================================================================================  
 
    # 0b. Sentiment Check -
    # Checks if the current message indicates high frustration/anger
    # Escalate immediately if detected
    if sentiment_checker(current_message):
            return {
                "response": "I apologize for the frustration. I am transferring you to a human manager immediately to resolve this.",
                "escalate_to_human": True
            }
 
 #===================================================================================================================   
    
    # 1. Check pending escalation (Yes / No / New Question)
    # This section checks if the bot previously asked the user if they want to escalate
    if conversation_history:
        last_turn = conversation_history[-1]
        
        # Look at if the system was the last to speak and it made an offer to escalate to human
        if last_turn["role"] == "bot" and "speak to a human agent" in last_turn["content"]:
            user_text = current_message.lower()
            
            # User says YES
            if any(w in user_text for w in ["yes", "yeah", "sure", "ok", "please", "do it"]):
                return {
                    "response": "Understood. Transferring you to a human agent now...", 
                    "escalate_to_human": True
                }
            
            # User says NO
            if any(w in user_text for w in ["no", "nope", "nah", "cancel", "don't"]):
                return {
                    "response": "Okay, I understand. I will not transfer you. Is there anything else I can help with?", 
                    "escalate_to_human": False
                }
            
            # CASE C: User ignores the question (e.g., "Where is the clinic?")
            # We do nothing here. The code simply continues down to the AI 
            # so it can answer the new question.

#===================================================================================================================

    # 2. Content manager
    # Collect and prepare context for LLM

    # 2a. Collect Specific User Profile from PATIENTS_DB

    patient_data = PATIENTS_DB.get(user_id)

    if patient_data:
        patient_context_str = json.dumps(patient_data, indent=2)
    else:
        patient_context_str = "User ID not found, transferring you to a human agent."
        return {
                    "response": patient_context_str,
                    "escalate_to_human": True
                }

    # 2b. Format the Clinic FAQs for LLM 
    # Dictionary --> clean string list for the LLM to read

    faq_context_str = "" # Initialize empty string

    for faq_id, data in CLINIC_FAQS.items():
        faq_context_str += f"ID: {faq_id} | Q: {data['question']} | A: {data['answer']}\n"

#===================================================================================================================

    # 3. Build LLM Prompt with Context and History
    
    # 3a. System Instructions with Context

    system_prompt = f"""
    You are the MediCare Plus Triage Bot.
    
    YOUR GOAL: 
    Answer the user's question using ONLY the provided context.
    
    1.  PATIENT PROFILE -
    {patient_context_str}
    
    2. CLINIC FAQs (KNOWLEDGE BASE) -
    {faq_context_str}
    
    INSTRUCTIONS:
    - Use the Conversation History to resolve pronouns (e.g., if user says "his specialty", check history to see who "he" is).
    - If the answer is in the FAQs, cite the ID like this: [Source: FAQxxx] .
    - If the answer is in the Patient Profile, use their name and details .
    - Format all currency/financial amounts to exactly two decimal places (e.g., €120.50, not €120.5).
    - If the answer is NOT in the context above, strictly say: "I cannot find information about [specific topic] in your records or our FAQ. 
    Would you like to speak with our team? They can help with: 
    [relevant service if determinable]"
    - Never invent medical facts.
    """
 #===================================================================================================================   

    # 4. Initialize Memory (Conversation History)
    
    messages = [SystemMessage(content=system_prompt)]

    # Add History (Contextual Memory) 
    for turn in conversation_history:
        if turn["role"] == "user":
            messages.append(HumanMessage(content=turn["content"]))
        elif turn["role"] == "bot":
            messages.append(AIMessage(content=turn["content"]))

    # Add the latest user question
    messages.append(HumanMessage(content=current_message))

#===================================================================================================================

    # 5. Call LLM
    
    try:
        response = chat.invoke(messages)
        answer_text = response.content
    except Exception as e:
        # Fallback for API errors
        return {"response": "System error. Please contact support.",
                 "escalate_to_human": True}

#===================================================================================================================

   # 6.  Fallback logic for escalation
    escalate = False
    
    # If LLM doesn't know, we don't escalate yet. We ask the user.
    if "cannot find" in answer_text.lower():
        answer_text = "I cannot find information about [specific topic] in your records or our FAQ. \nWould you like to speak with our team? They can help with: \n" \
        "[relevant service if determinable]"
        escalate = False # Wait for the user's "Yes" in the next turn

    return {
        "response": answer_text,
        "escalate_to_human": escalate
    }


#===================================================================================================================
# Main Loop - Live Chat Simulation

if __name__ == "__main__":
    # 1. Setup State
    history = []
    current_user_id = "P001" # Maria Garcia
    
    print("MEDI-CARE CHATBOT STARTED")
    print(f"Logged in as: {current_user_id}")
    print("Type 'quit' to exit.\n")

    print("Medi-Care Agent: Hello! Welcome to MediCare Plus Clinic. How can I assist you today?")

    # 2. Start Infinite Loop
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                print("Exiting...")
                break
            
            # 3. Call the Logic Function
            result = generate_response(current_user_id, user_input, history)
            
            # 4. Print Response
            print(f"Medi-Care Agent: {result['response']}")
            
            # 5. Update History (CRITICAL: This allows memory to work)
            history.append({"role": "user", "content": user_input})
            history.append({"role": "bot", "content": result['response']})

            # 6. Check Escalation & EXIT
            if result['escalate_to_human']:
                print("\n>> [SYSTEM]: TICKET CREATED FOR HUMAN AGENT. TRANSFERRING NOW...")
                print(">> [SYSTEM]: ENDING AUTOMATED CHAT SESSION.")
                break  # <--- Stops the loop and ends the chat

        except KeyboardInterrupt:
            break
    
