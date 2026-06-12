"""Custom Edge TTS service for manim-voiceover with retry + throttle."""
import asyncio
import time
import random
from pathlib import Path
from manim import logger
from manim_voiceover.services.base import SpeechService


class EdgeTTSService(SpeechService):
    """Speech service using Microsoft Edge TTS via edge-tts library.

    Includes:
      * Pre-request random throttle (0.8–2.5 s) to avoid rate-limiting
        when many voiceover blocks are synthesised back-to-back.
      * Exponential-backoff retry (up to max_retries attempts).
    """

    def __init__(self, voice: str = "vi-VN-NamMinhNeural",
                 rate: str = "-5%", volume: str = "+0%",
                 max_retries: int = 8, throttle_min: float = 0.8,
                 throttle_max: float = 2.5, **kwargs):
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.max_retries = max_retries
        self.throttle_min = throttle_min
        self.throttle_max = throttle_max
        SpeechService.__init__(self, global_speed=1.0, **kwargs)

    def generate_from_text(self, text: str, cache_dir=None, path: str = None) -> dict:
        if cache_dir is None:
            cache_dir = self.cache_dir

        input_data = {
            "input_text": text,
            "service": "edge_tts",
            "voice": self.voice,
            "rate": self.rate,
        }

        # Return cached audio instantly if it exists
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached

        audio_path = (path if path else self.get_audio_basename(input_data) + ".mp3")
        full_path = str(Path(cache_dir) / audio_path)

        # Pre-request throttle — only for un-cached texts
        sleep_t = random.uniform(self.throttle_min, self.throttle_max)
        logger.info(f"Edge TTS: throttle {sleep_t:.1f}s before synthesis…")
        time.sleep(sleep_t)

        async def _synth_with_retry():
            import edge_tts
            last_exc = None
            for attempt in range(self.max_retries):
                try:
                    communicate = edge_tts.Communicate(
                        text=text,
                        voice=self.voice,
                        rate=self.rate,
                        volume=self.volume,
                    )
                    await communicate.save(full_path)
                    return                              # success ✓
                except Exception as exc:
                    last_exc = exc
                    wait = 5 + 2 ** attempt            # 6, 7, 9, 13, 21, 37 …
                    logger.warning(
                        f"Edge TTS attempt {attempt + 1}/{self.max_retries} failed "
                        f"({type(exc).__name__}: {exc}). Retrying in {wait}s…"
                    )
                    await asyncio.sleep(wait)
            raise RuntimeError(
                f"Edge TTS failed after {self.max_retries} attempts."
            ) from last_exc

        asyncio.run(_synth_with_retry())

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }
