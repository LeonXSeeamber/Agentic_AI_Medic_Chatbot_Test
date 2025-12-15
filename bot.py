import sys
import os

# ------------------ IMPORT THE FUNCTION TO TEST ------------------
try:
    from GIMO_MediCare_Plus_Clinic_Chatbot_Live import generate_response
except ImportError:
    print("❌ ERROR: Could not import 'generate_response'.")
    print("Make sure 'GIMO_MediCare_Plus_Clinic_Chatbot_Live.py' is in the same folder.")
    sys.exit(1)
# ------------------------------------------------------------------

if __name__ == "__main__":

    print("\n------------------------------------------------")
    print("       STARTING MEDI-CARE BOT TEST SUITE       ")
    print("------------------------------------------------\n")

    # ==================================================================================
    # TEST 1: The Happy Path
    # User P001 asks "How do I pay?" -> Bot answers using FAQ004
    # ==================================================================================
    print("TEST 1: Happy Path (Payment FAQ)")
    input_text = "How do I pay?"
    print(f"User Input: {input_text}")

    result = generate_response("P001", input_text, [])
    print(f"Bot Response: {result['response']}")

    # Check for correct FAQ citation (FAQ004 or FAQ005 depending on your DB) or keyword
    assert "FAQ" in result['response'] or "cash" in result['response'].lower()
    assert result['escalate_to_human'] is False
    print("✅ PASS\n")

    # ==================================================================================
    # TEST 2: The Personal Query
    # User P003 asks "Do I owe anything?" -> Bot checks balance -> "Hi Ana... €120.50"
    # ==================================================================================
    print("TEST 2: Personal Query (Balance)")
    input_text = "Do I owe anything?"
    print(f"User Input: {input_text}")

    result = generate_response("P003", input_text, [])
    print(f"Bot Response: {result['response']}")

    assert "120.50" in result['response']
    assert "Ana" in result['response'] # Checks if personalization is working
    print("✅ PASS\n")

    # ==================================================================================
    # TEST 3: The Emergency
    # User P002 says "I'm having severe chest pain." -> Bot triggers escalation
    # ==================================================================================
    print("TEST 3: Emergency Check")
    input_text = "I'm having severe chest pain."
    print(f"User Input: {input_text}")

    result = generate_response("P002", input_text, [])
    print(f"Bot Response: {result['response']}")
    print(f"Escalated: {result['escalate_to_human']}")

    assert result['escalate_to_human'] is True
    assert "medical emergency" in result['response'].lower() or "transferring" in result['response'].lower()
    print("✅ PASS\n")

    # ==================================================================================
    # TEST 4: The Hallucination Trap
    # User asks "Do you do liver transplants?" -> Bot admits ignorance & offers agent
    # ==================================================================================
    print("TEST 4: Hallucination Trap")
    input_text = "Do you do liver transplants?"
    print(f"User Input: {input_text}")

    result = generate_response("P001", input_text, [])
    print(f"Bot Response: {result['response']}")

    # Must contain the fallback phrase "cannot find"
    assert "cannot find" in result['response'].lower()
    # Must NOT escalate immediately (waits for Yes/No)
    assert result['escalate_to_human'] is False
    print("✅ PASS\n")

    # ==================================================================================
    # TEST 5: Memory (Contextual Follow-up)
    # Turn 1: "Who is my primary doctor?" -> Turn 2: "What is his specialty?"
    # ==================================================================================
    print("TEST 5: Memory (Contextual Follow-up)")
    
    # Simulate previous turn
    history = [
        {"role": "user", "content": "Who is my primary doctor?"},
        {"role": "bot", "content": "Your primary doctor is Dr. Fernández."}
    ]

    input_text = "What is his specialty?"
    print(f"User Input (Turn 2): {input_text}")

    result = generate_response("P001", input_text, history)
    print(f"Bot Response: {result['response']}")

    # Dr. Fernandez is 'General Medicine' in P001's profile
    assert "general medicine" in result['response'].lower()
    assert result['escalate_to_human'] is False
    print("✅ PASS\n")

    # ==================================================================================
    # Completion Message
    # ==================================================================================
    print("------------------------------------------------")
    print("       ALL TESTS COMPLETED SUCCESSFULLY        ")
    print("------------------------------------------------\n")