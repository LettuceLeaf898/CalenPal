import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from Client_agent import Client_agent


session_service = InMemorySessionService()
runner = Runner(
    app_name="CalenPal",
    agent=root_agent,
    session_service=session_service
)

user_id = "test_user"           # or generate dynamically
session_id = str(uuid.uuid4())   # unique session ID for each request
new_message = types.Content(
    role="users", parts=[types.Part(text=prompt)]
)  # matches your agent input schema

events= runner.run(
    user_id=user_id,
    session_id=session_id,
    new_message=new_message
)


final_response_content = None
for event in events:
    if event.is_final_response():
         # The final response content is typically found in event.content.parts[0].text
        final_response_content = event.content.parts[0].text
        break  # Exit the loop once the final response is found

if final_response_content:
    print("Agent Response:", final_response_content)
else:
    print("No final response found in the events.")
# Extract JSON output