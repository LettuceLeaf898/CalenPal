import uuid
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import PyPDF2

from PDF_Reader_Agent.agent import root_agent

load_dotenv()
def agent_rep(pdf_text: str):
    session_service_stateful = InMemorySessionService()

    initial_state = {
        "user_name": "Stressed User",
        "user_preferences": """
            I like to have an orderly schedule that helps me manage my time.
            I like to calculate the stress of all events I do.
            I need 8 hours of sleep every night I go to bed around 11PM.
            I have a hard time balancing work and friends.
        """,
    }

    APP_NAME = "CalenPal"
    USER_ID = "Stressed Human"
    SESSION_ID = str(uuid.uuid4())

    asyncio.run(session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    ))

    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service_stateful,
    )

    # Send PDF **text**, not file path
    new_message = types.Content(
        role="user", parts=[types.Part(text=pdf_text)]
    )

    response = None
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                response = event.content.parts[0].text

    # Cleanup markdown-style json if present
    if response:
        response = response.strip()
        if response.startswith("```json"):
            response = response[len("```json"):].strip()
        if response.startswith("```"):
            response = response[len("```"):].strip()
        if response.endswith("```"):
            response = response[:-3].strip()

    return response