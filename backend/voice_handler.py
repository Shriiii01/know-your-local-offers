import os
import io
from openai import OpenAI
import httpx
from gtts import gTTS

class VoiceHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.eleven_key = os.getenv("ELEVENLABS_API_KEY")
        # path to Google creds set in GOOGLE_APPLICATION_CREDENTIALS env   

    async def transcribe(self, audio_bytes: bytes) -> str:
        try:
            file_obj = io.BytesIO(audio_bytes)
            file_obj.name = "audio.wav"
            
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=file_obj,
                language="en"
            )
            return response.text
        except Exception as e:
            print(f"[VoiceHandler:transcribe] {e}")
            return "Could not transcribe audio."

    async def synthesize(self, text: str, language: str) -> bytes:
        # English via ElevenLabs, else gTTS
        if language == "en" and self.eleven_key:
            return await self._eleven_tts(text)
        return await self._gtts_tts(text, language)

    async def _eleven_tts(self, text: str) -> bytes:
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        headers = {
            "Accept":        "audio/mpeg",
            "Content-Type":  "application/json",
            "xi-api-key":    self.eleven_key,
        }
        json_data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability":0.5, "similarity_boost":0.5}
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=json_data, headers=headers)
        r.raise_for_status()
        return r.content

    async def _gtts_tts(self, text: str, language: str) -> bytes:
        lang_map = {"en":"en"}
        tts   = gTTS(text=text, lang=lang_map.get(language, "en"), slow=False)
        buf   = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()