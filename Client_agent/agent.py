import asyncio
import uuid
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import json

load_dotenv()

class responseContent(BaseModel):
    subject: str = Field(
        description="Title to summerize what user is asking in one word"
    )
    body: str = Field(
        description="The main content should be relavant to the prompt"
    )

root_agent = LlmAgent(
    name="Client_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model="gemini-2.0-flash",
    description="assistant",
    instruction="""
    No matter what the user says return a json fileCreate an appropriate subject that sums up the prompt in one word
    Body should be written in a formal tone always ending witha goodbye and a thank you.
    IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting",
        }

        DO NOT include any explanations or additional text outside the JSON response.
    """,
    output_schema=responseContent,
    output_key="response",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

def get_agent_response(prompt: str):
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="CalenPal",
        agent=root_agent,
        session_service=session_service
    )

    user_id = "test_user"           # or generate dynamically
    session_id = str(uuid.uuid4())   # unique session ID for each request
    new_message = {"query": prompt}  # matches your agent input schema

    raw_response = runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=new_message
    )


    # Extract JSON output
    print(raw_response)
    return raw_response