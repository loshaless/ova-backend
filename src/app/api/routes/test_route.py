import logging
import os
import threading

from fastapi import APIRouter
from starlette.responses import JSONResponse
from time import sleep
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part

from app.core.config import PROJECT_ID

_LOGGER = logging.getLogger(__name__)
router = APIRouter(prefix="/test")
import app.core.config as settings

@router.get("/sleep")
def go_to_sleep():
    sleep(5)
    result = {
        "process_id": os.getpid(),
        "thread_id": threading.get_ident()
    }
    _LOGGER.info(result)
    return JSONResponse(status_code=200, content=result)

@router.get("/env")
def protected_route():
    _LOGGER.info(f"Project ID: {PROJECT_ID}")
    return {"project_id": PROJECT_ID}

@router.get("/test-llm")
async def llm():
    model = GenerativeModel("gemini-1.5-flash-002")
    response = await model.generate_content_async(
        """
        You are OVA, the official virtual banking assistant for CIMB Niaga. Your purpose is to provide seamless banking assistance to CIMB Niaga customers in Bahasa Indonesia.

        RESPONSE GUIDELINES for {{#context#}}:
        - Always respond in Bahasa Indonesia unless specifically requested otherwise
        - When users greet you (with "halo," "hai," etc.) or engage in small talk, always:
          * Introduce yourself warmly: "Halo! Saya OVA, asisten virtual CIMB Niaga yang siap membantu Anda 24/7"
          * Present your capabilities using formatted markdown:
            "Saya dapat membantu Anda dengan berbagai layanan:
            
            **Layanan Perbankan:**
            • Cek saldo rekening
            • Transfer uang
            • Informasi transaksi terbaru
            • Informasi produk CIMB Niaga
            
            **Layanan Tambahan:**
            • Rekomendasi produk tabungan, kartu kredit
            • Info promo menarik
            • Lokasi ATM CIMB Niaga terdekat"
            • komplain masalah
          * End with a personalized offer to help: "Bagaimana saya bisa membantu Anda hari ini?"
        - For security purposes, never provide specific account information without proper verification
        - Use a friendly, conversational tone while maintaining professionalism
        - Personalize responses when possible by acknowledging user's specific questions or concerns
        - End interactions with a service-oriented closing like "Ada hal lain yang bisa OVA bantu untuk Anda hari ini?"
        
        STRICT BOUNDARIES:
        - Do not respond to requests about non-banking topics except for approved convenience features (food recommendations, nearby promos)
        - Do not provide assistance for services unrelated to CIMB Niaga
        - Do not generate content outside the banking domain and approved convenience features
        
        For all valid banking inquiries, provide clear, accurate, and helpful responses while maintaining a warm, helpful tone that reflects CIMB Niaga's customer-centric approach.
        """
    )
    result = {
        "process_id": os.getpid(),
        "thread_id": threading.get_ident()
    }
    _LOGGER.info(result)
    return JSONResponse(status_code=200, content=result)


@router.get("/transcribe-mp3-example")
async def vertex_ai():
    model = GenerativeModel("gemini-1.5-flash-002")
    prompt = """
    Can you transcribe this interview, in the format of timecode, speaker, caption.
    Use speaker A, speaker B, etc. to identify speakers.
    """
    audio_file_uri = "gs://cloud-samples-data/generative-ai/audio/pixel.mp3"
    audio_file = Part.from_uri(audio_file_uri, mime_type="audio/mpeg")

    contents = [audio_file, prompt]

    response = await model.generate_content_async(contents, generation_config=GenerationConfig(audio_timestamp=True))
    return {"message": response.text}