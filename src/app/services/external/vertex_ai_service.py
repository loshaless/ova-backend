from google import genai
from google.genai import types
from google.oauth2 import service_account
from app.schemas.external.vertex_ai_schema import GenerateContentRequest

class VertexAIService:
    """
    Service for interacting with Google Vertex AI and Generative AI
    """

    def __init__(
        self,
        project_id: str,
        credentials_path: str,
        location: str = "us-central1"
    ):
        self.location = location
        SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=SCOPES
        )

        # Create Generative AI client
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=self.location,
            credentials=creds
        )

    def generate_content_stream(
        self,
        question: str,
        generate_content_request: GenerateContentRequest
    ) -> str:
        contents = [
            types.Content(role="user", parts=[types.Part.from_text(text=question)])
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=generate_content_request.temperature,
            top_p=generate_content_request.top_p,
            max_output_tokens=generate_content_request.max_tokens,
            response_modalities=["TEXT"],
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
            ],
            system_instruction=[types.Part.from_text(text=generate_content_request.prompt_text)],
        )

        response_text = ""
        for chunk in self.client.models.generate_content_stream(
                model=generate_content_request.model_name,
                contents=contents,
                config=generate_content_config,
        ):
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                response_text += chunk.text

        return response_text

    def generate_content(
            self,
            question: str,
            generate_content_request: GenerateContentRequest
    ) -> str:
        """
        Generate content without streaming
        """
        contents = [
            types.Content(role="user", parts=[types.Part.from_text(text=question)])
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=generate_content_request.temperature,
            top_p=generate_content_request.top_p,
            max_output_tokens=generate_content_request.max_tokens,
            response_modalities=["TEXT"],
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
            ],
            system_instruction=[types.Part.from_text(text=generate_content_request.prompt_text)],
        )

        response = self.client.models.generate_content(
            model=generate_content_request.model_name,
            contents=contents,
            config=generate_content_config,
        )

        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text

        return ""
