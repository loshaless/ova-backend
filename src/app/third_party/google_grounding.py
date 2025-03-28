import os
from google.cloud import aiplatform
from google import genai
from google.genai import types
from google.oauth2 import service_account
from app.core.config import get_project_id, get_creds

location = "us-central1"
aiplatform.init(project=get_project_id(), location=location)

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
creds = service_account.Credentials.from_service_account_file(get_creds(), scopes=SCOPES)

client = genai.Client(
    vertexai=True,
    project=get_project_id(),
    location=location,
    credentials=creds
)

SYSTEM_INSTRUCTION = """
You are a financial assistant named "OVA"  that provides financial information such as real-time currency exchange rates, pasardana (harga saham di pasardana.id), etc.
Your responses must be based on the latest and most accurate financial data.
Use grounded data sources to ensure precision. Answer only in Bahasa Indonesia.
You only answer the question that ask about financial information like mentioned before, for other information such as general question and other question you must not reply and said "Maaf OVA tidak bisa menjawab pertanyaan tersebut".
If the question to ambiguous like "berapa kurs hari ini?" answer it with the general information about exchange rate in table. 
"""

def get_grounding_response(question: str) -> str:
    contents = [
        types.Content(role="user", parts=[types.Part.from_text(text=question)])
    ]
    
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        system_instruction=[types.Part.from_text(text=SYSTEM_INSTRUCTION)],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash-001",
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
            response_text += chunk.text

    return response_text
