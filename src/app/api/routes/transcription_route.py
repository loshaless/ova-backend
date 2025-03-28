import logging
from fastapi import APIRouter
from starlette.responses import JSONResponse
from google.cloud import texttospeech
import base64

_LOGGER = logging.getLogger(__name__)
router = APIRouter(prefix="/transcript")

client = texttospeech.TextToSpeechClient()
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
    speaking_rate=1.2,
    pitch=3.0,
)
voice = texttospeech.VoiceSelectionParams(
    language_code="id-ID",  # Bahasa Indonesia language code
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)

@router.post("/text-to-speech")
def transcribe_text_to_speech_via_tts(text: str):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Convert audio content to base64
    audio_content_b64 = base64.b64encode(response.audio_content).decode('utf-8')

    # Return the audio content to file for testing
    # with open("output.ogg", "wb") as out:
    #     out.write(response.audio_content)

    return JSONResponse(
        content={
            "success": True,
            "message": "Transcription successful",
            "data": {
                "audio_content": audio_content_b64,
            }
        }
    )



