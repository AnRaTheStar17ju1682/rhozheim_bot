import json
from vosk import Model, KaldiRecognizer
import soundfile as sf
from io import BytesIO
from src.voice.voice_recognzer_interface import VoiceRecognizer

import multiprocessing
import asyncio

# Глобальный пул процессов




class LocalRecognizer(VoiceRecognizer):
    def __init__(self, model_path, num_processes):
        self.model = Model(model_path)
        #self.process_pool = multiprocessing.Pool(num_processes)
        self.queue_manager = multiprocessing.Manager()
    
    
    async def recognize_speech(self, buffer):
        text = self.queue_manager.dict()
        is_done = self.queue_manager.Event()
        multiprocessing.Process(target=self._recognize_speech_sync, args=(buffer, text, is_done)).start()
        #res = self.process_pool.apply(self._recognize_speech_sync, buffer, queue)
        #res.get()
        
        while not is_done.is_set():
            await asyncio.sleep(1)
            if t := text.get("value"):
                yield t
            else:
                print("!!!") 

    
    def _recognize_speech_sync(self, buffer: BytesIO, text, is_done):
        data, samplerate = sf.read(buffer, dtype="int16")
        recognizer = KaldiRecognizer(self.model, samplerate)
        chunk_size = 16000
        
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size].tobytes()
            recognizer.AcceptWaveform(chunk)
            partial = json.loads(recognizer.PartialResult())["partial"]
            text["value"] = partial
        else:
            is_done.set()