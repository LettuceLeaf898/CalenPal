from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel, Field

from .SUB_AGENTS.Chat_Agent.agent import Chat_Agent
from .SUB_AGENTS.PDF_Reader_Agent.agent import PDF_Reader_Agent

class responseContent(BaseModel):
    subject: str = Field(
        description="Calander"
    )
    body: str = Field(
        description="Awnser what ever question was aksed about the calander"
    )

root_agent = Agent(
    name="Organizer_Agent",
    model="gemini-2.0-flash",
    description="Finds out which Agent is best for taking care of the Task",
    instruction="""
    You are an organizer agent that helps to determine which specialized agent is best suited to handle a given task.

    ALL OUTPUTS ARE TO BE IN JSON FORMAT:
    {
        "subject": "Title",
        "body": "Information",
    }   
    The title and information will be determined using tools below

    You have access t6o the following tools:
    1. Chat_Agent: An agent that can answer questions about the user's calendar and events.
    2. PDF_Reader_Agent: An agent that can read and extract information from PDF documents.

    IF you ever are ever inputed with a PDF file you MUST use the PDF_Reader_Agent to extract the text from the PDF and then use that text to help awnser any questions about the PDF
    IF you are ever inputed with a question about the calander or events you MUST use the Chat_Agent to awnser those questions

    IF you dont know what to post post this do not at any circumstances post nothing
    {
        "subject": "Unsure",
        "body": "I am not sure how to help with that. Please ask a different question or provide more details so I can assist you better."
    }
    """,
    output_schema=responseContent,
    output_key="response",
     tools=[
        AgentTool(Chat_Agent),
        AgentTool(PDF_Reader_Agent),
    ],

)