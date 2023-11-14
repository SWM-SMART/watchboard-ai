import os, json
import librosa
import soundfile as sf

from app.schemas.context import Segment, SpeechText

class STTController:
    def __init__(self):
        pass

    def convert_to_wav(self, prefix):
        output_path = f'app/static/{prefix}.wav'        
        y, sr = librosa.load(f'app/static/{prefix}.m4a', sr=16000)
        sf.write(output_path, y, sr)

    def speech_to_text(self, prefix):
        os.system(f'./app/whisper/main -m ./app/whisper/models/ggml-medium.bin -l "ko" -f ./app/static/{prefix}.wav -oj')

    def get_speech_text(self, prefix):
        with open(f'app/static/{prefix}.wav.json', 'r') as json_file:
            json_data = json.load(json_file)

        text = ""
        segments = []
        for segment in json_data['transcription']:
            here_segment = Segment(
                start=segment['offsets']['from'],
                end=segment['offsets']['to'],
                text=segment['text']
            )
            segments.append(here_segment)
            text += segment['text']
        return SpeechText(segments=segments, text=text)
