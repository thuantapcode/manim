"""SpeechService subset required by the project's custom EdgeTTSService."""

import hashlib
import json
from pathlib import Path


class SpeechService:
    def __init__(self, global_speed=1.0, cache_dir=None, **kwargs):
        self.global_speed = global_speed
        self.cache_dir = str(
            Path(cache_dir or "media/voiceovers").resolve()
        )
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_audio_basename(input_data):
        payload = json.dumps(input_data, ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def get_cached_result(self, input_data, cache_dir=None):
        cache_dir = Path(cache_dir or self.cache_dir)
        audio_name = self.get_audio_basename(input_data) + ".mp3"
        audio_file = cache_dir / audio_name
        if audio_file.exists() and audio_file.stat().st_size > 0:
            return {
                "input_text": input_data.get("input_text", ""),
                "input_data": input_data,
                "original_audio": audio_name,
            }
        return None
