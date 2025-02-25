from abc import ABC, abstractmethod
from io import BytesIO


class VoiceRecognizer(ABC):
    @abstractmethod
    async def recognize_speech(self, voice_file: BytesIO):
        raise NotImplementedError