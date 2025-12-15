MediCare Plus Triage Chatbot

An AI assistant for MediCare Plus Clinic that answers patient questions, checks basic account and appointment details, and hands off to a human when needed.
The bot is stateless. Each request rebuilds context from the inputs you send in.

========================================================================================================================================================================================
Overview

The MediCare Plus Triage Bot is designed to be:

- Safe
- Predictable
- Easy to integrate into an API

It always:

- Runs safety checks before calling the model
- Uses only patient data and FAQs that you pass in
- Admits when it does not know the answer instead of guessing

========================================================================================================================================================================================
Key capabilities

- Emergency detection
  - Spots high-risk phrases such as “chest pain” or “unconscious” and immediately escalates instead of chatting.

- Sentiment handling
  - Detects strong frustration or anger and routes the user to a human agent.

- Context awareness
  - Uses conversation history to resolve follow-ups, for example
    - "What is his specialty?" -> "Dr Fernandez".

- Data grounding

- Answers are built only from:

  - patient profile data (JSON)

  - clinic FAQs

- Hallucination control

  - If the answer is not in the context, the bot says it cannot find the information and offers a human, rather than making something up.


========================================================================================================================================================================================
Architecture

The logic follows a fixed sequence on every call to generate_response:

1. Safety guardrails
   - Check for emergency language.
   - Check for strong negative sentiment.
   - If either triggers, return a safe message and set "escalate_to_human" to True.

2. Escalation check

   - If the last bot turn asked "Would you like to speak to a human agent?", treat the current message as a yes/no.

   - "Yes" -> transfer to a human.

   - "No" -> stay with the bot.

   - Anything else → treat as a new question and continue.

3. Context aggregation

   - Load patient data from "PATIENTS_DB" using "user_id".

   - Flatten all "CLINIC_FAQS" into a single text block.

   - Add both into the system prompt.

4. LLM call

   - Call "gpt-3.5-turbo" with temperature = 0.

   - Include conversation history so the model can see previous turns.

5. Fallback logic

   - If the model reply contains "cannot find", replace it with a fixed message that admits uncertainty and offers a human agent.

   - Wait for the user’s "yes" or "no" before escalating.

========================================================================================================================================================================================
Installation and setup

1. Prerequisites

   - Python 3.8 or higher

   - An OpenAI API key


2. Install

   - pip install -r requirements.txt


3. Configuration

   - Create or edit a .env file in the project root:

      - OPENAI_API_KEY="sk-your-openai-api-key-here"

======================================================================================================================================================================================== 
Usage

Running the live chat

- Start an interactive session in the terminal:

   - python GIMO_MediCare_Plus_Clinic_Chatbot_Live.py


Default user is "P001" (Maria Garcia).

Example questions:

"Who is my doctor?"

"Do I owe money?"

Type "quit" or "exit" to stop.


Running the tests

- Run the scenario tests (happy path, emergency, memory, etc.):

    - python test_bot.py


You should see "PASS" for all defined scenarios.
