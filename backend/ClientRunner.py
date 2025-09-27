import uuid
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from Client_agent.agent import root_agent

load_dotenv()
def agent_response(prompt: str):
    session_service_stateful = InMemorySessionService()

    initial_state = {
        "user_name": "Stressed User",
        "user_preferences": """
            I like to have a ordlerly scedule that helps me manage my time.
            I like to calclate the stress of all events I do
            I need 8 hours of sleep every night I go to bed around 11PM
            I hvae a hard time balanceing work and friends
        """,
    }


    APP_NAME = "CalenPal"
    USER_ID = "Stressed Human"
    SESSION_ID = str(uuid.uuid4())

    stateful_session = asyncio.run(session_service_stateful.create_session(
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
            # or generate dynamically  # unique session ID for each request
    new_message = types.Content(
        role="user", parts=[types.Part(text=prompt)]
    )  # matches your agent input schema

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                response = event.content.parts[0].text

    print("==== Session Event Exploration ====")

    return response

