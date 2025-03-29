from google.cloud import aiplatform
from google import genai
from google.genai import types
from google.oauth2 import service_account


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
        """
        Initialize Vertex AI and Generative AI clients

        Args:
            project_id (str): Google Cloud Project ID
            credentials_path (str): Path to service account credentials
            location (str, optional): Google Cloud region. Defaults to "us-central1".
        """
        self.location = location

        # Initialize AI Platform
        aiplatform.init(project=project_id, location=self.location)

        # Setup credentials
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

        # Default system instruction
        self.SYSTEM_INSTRUCTION = """
        You are a financial assistant named "OVA" that provides financial information 
        such as real-time currency exchange rates, pasardana (harga saham di pasardana.id), etc.
        Your responses must be based on the latest and most accurate financial data.
        Use grounded data sources to ensure precision. Answer only in Bahasa Indonesia.
        You only answer questions about financial information like mentioned before. 
        For other information, respond with "Maaf OVA tidak bisa menjawab pertanyaan tersebut".
        If the question is too ambiguous like "berapa kurs hari ini?", 
        answer with general information about exchange rates in a table.
        """

    def generate_content(
            self,
            question: str,
            model: str = "gemini-2.0-flash-001",
            temperature: float = 1.0,
            max_tokens: int = 8192
    ) -> str:
        """
        Generate content based on the given question

        Args:
            question (str): Input question or prompt
            model (str, optional): AI model to use. Defaults to "gemini-2.0-flash-001".
            temperature (float, optional): Sampling temperature. Defaults to 1.0.
            max_tokens (int, optional): Maximum output tokens. Defaults to 8192.

        Returns:
            str: Generated response
        """
        contents = [
            types.Content(role="user", parts=[types.Part.from_text(text=question)])
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            top_p=0.95,
            max_output_tokens=max_tokens,
            response_modalities=["TEXT"],
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
            ],
            system_instruction=[types.Part.from_text(text=self.SYSTEM_INSTRUCTION)],
        )

        response_text = ""
        for chunk in self.client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
        ):
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                response_text += chunk.text

        return response_text