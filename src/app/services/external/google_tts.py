import base64
import logging
from google.cloud import texttospeech
from app.core.config import TTS_PITCH, TTS_SPEAKING_RATE, TTS_GENDER, TTS_LANGUAGE_CODE

logger = logging.getLogger(__name__)
client = texttospeech.TextToSpeechClient()


class TTSService:
    # Map string gender to enum
    gender_map = {
        "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
        "MALE": texttospeech.SsmlVoiceGender.MALE,
        "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL
    }

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
        speaking_rate=float(TTS_SPEAKING_RATE),
        pitch=float(TTS_PITCH),
    )

    voice = texttospeech.VoiceSelectionParams(
        language_code=TTS_LANGUAGE_CODE,
        ssml_gender=gender_map.get(
            TTS_GENDER,
            texttospeech.SsmlVoiceGender.FEMALE
        ),
    )

    @classmethod
    def synthesize_speech(cls, text: str) -> str:
        """
        Convert text to speech and return base64 encoded audio

        Args:
            text: The text to convert to speech

        Returns:
            Base64 encoded audio content
        """
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=cls.voice,
                audio_config=cls.audio_config
            )

            # Convert audio content to base64
            audio_content_b64 = base64.b64encode(response.audio_content).decode('utf-8')
            return audio_content_b64

        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            raise