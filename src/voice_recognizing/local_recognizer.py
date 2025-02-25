import json
from io import BytesIO

from vosk import Model, KaldiRecognizer
import soundfile as sf

from src.voice_recognizing.voice_recognzer_interface import VoiceRecognizer


class LocalRecognizer(VoiceRecognizer):
    def __init__(self, model_path):
        self.model = Model(model_path)
    
    
    async def recognize_speech(self, buffer: BytesIO):
        data, samplerate = sf.read(buffer, dtype="int16")
        recognizer = KaldiRecognizer(self.model, samplerate)
        chunk_size = 16000  # Размер чанка в сэмплах
        
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size].tobytes()
            recognizer.AcceptWaveform(chunk)
            partial = json.loads(recognizer.PartialResult())["partial"]
            if partial:
                yield partial