from fastapi import APIRouter, Depends

from app.schemas.context import Audio, SpeechText
from app.controller.stt import STTController
from app.api.deps import get_s3_controller, get_stt_controller
import botocore

from app.core.config import (
    AUDIO_S3_PREFIX,
    S3_BUCKET_NAME
)

router = APIRouter()

@router.post("/stt", response_model=None)
def get_speech_to_text(
    audio: Audio,
    stt_controller: STTController = Depends(get_stt_controller),
    s3_controller: botocore.client = Depends(get_s3_controller)
    ) -> SpeechText:

    prefix = '.'.join(audio.key.split('.')[:-1])
    s3_controller.download_file(S3_BUCKET_NAME, AUDIO_S3_PREFIX + audio.key, f'stt/static/{audio.key}')

    stt_controller.convert_to_wav(prefix)
    stt_controller.speech_to_text(prefix)
    return stt_controller.get_speech_text(prefix)
