from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

PDF_Reader_Agent = LlmAgent(
    name="PDF_Reader_Agent",
    model="gemini-2.0-flash",
    description="Agent that can read and extract information from PDF documents",
    instruction="""
    You are a PDF Reader Agent that extracts text from PDF documents.
    Submit it all as a single string in the 'body' field of the response.
    Your response MUST be valid JSON matching this structure:
    {
        "subject": "PDF Content",
        "body": "Extracted text from the PDF document."
    }
    """,
)