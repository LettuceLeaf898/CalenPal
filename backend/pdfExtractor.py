import json
import os
import re
from PyPDF2 import PdfReader


def extract_pdf_text(file_path: str) -> str:
    """Extract text safely from a PDF."""
    try:
        reader = PdfReader(file_path)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text).strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    
def merge_json_data(new_json_str: str) -> str:
    """
    Merge new JSON events into events.json and return merged JSON as string.
    """
    events_path = os.path.join(os.path.dirname(__file__), "events.json")
    if os.path.exists(events_path):
        with open(events_path, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    new_data = json.loads(new_json_str)
    merged_data = existing_data + new_data

    with open(events_path, "w") as f:
        json.dump(merged_data, f, indent=4)

    return json.dumps(merged_data, indent=4)


def pre_parse_pdf_text(pdf_text: str):
    """
    Pre-parse PDF text into a simplified intermediate JSON structure
    for the agent to finalize.
    """
    events = []
    # Example regex to find Homework, Exam, or Class events
    for match in re.finditer(
        r"(Homework|Exam|Class)\s*(\d+)?[:.-]?\s*(.*?)(?=\nHomework|\nExam|\nClass|$)",
        pdf_text,
        re.DOTALL
    ):
        event_type, number, desc = match.groups()
        events.append({
            "title": f"{event_type} {number}" if number else event_type,
            "description": desc.strip(),
            "date": "",
            "time": "",
            "importance": "",
            "stress": ""
        })
    return events