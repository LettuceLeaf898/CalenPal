
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import json

load_dotenv()


def events_reader() -> dict:
    """
    Reads the JSON file and returns its content as a dictionary.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'config.json')
    events_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'events.json'))
    events_path = os.path.abspath(events_path)
    with open(events_path, 'r') as file:
        return json.load(file)

class responseContent(BaseModel):
    subject: str = Field(
        description="Calander"
    )
    body: str = Field(
        description="Awnser what ever question was aksed about the calander"
    )

Chat_Agent = LlmAgent(
    name="Chat_Agent",
    # https://ai.google.dev/gemini-api/docs/models
    model="gemini-2.0-flash",
    description="Calander Assiatant meant to awnser any questions about the calander",
    instruction="""
    No matter what the user says return a json fileCreate an appropriate subject that sums up the prompt in one word
    You are a helpful and calming assitant that wants to provide the helpful awnsers about the calandar json file

    Use the tool `events_reader` to read the events.json file and that is the clander you will be basing all your awnsers off of

    THe Stress_lvl is out of 10 with 10 being the most stressed

    PLease try your best to awnser any questions related to the events

    IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "A calming and not freindly message to user about the calendar question asked try to keep it consise and to the point",
        }

    if cant read Json file then out put
    {
    "subject": "Error",
    "body": "I am sorry but I am unable to read the calendar file at the moment. Please try again later."
    }

    IF YOU ARE UNSURE RETURN:
    {
    "subject": "Unsure",
    "body": "I am not sure how to help with that. Please ask a different question or provide more details so I can assist you better."
    }
    DO NOT include any explanations or additional text outside the JSON response.
        
    """,
    #input_schema=InputSchema,
    output_schema=responseContent,
    output_key="response",
    tools=[events_reader]
)

