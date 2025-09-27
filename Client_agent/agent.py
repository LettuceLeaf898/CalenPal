
import uuid
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import json

load_dotenv()

#class InputSchema(BaseModel):
    #text: str

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
    #input_schema=InputSchema,
    output_schema=responseContent,
    output_key="response",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

