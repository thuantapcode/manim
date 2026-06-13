"""Small manim-voiceover compatibility layer used by Part 4 and Part 5."""

from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import av
from manim.scene.scene import Scene


def _audio_duration(path: str) -> float:
    with av.open(path) as container:
        if container.duration is not None:
            return float(container.duration / av.time_base)

        stream = next(s for s in container.streams if s.type == "audio")
        if stream.duration is not None:
            return float(stream.duration * stream.time_base)

    raise RuntimeError(f"Cannot determine audio duration: {path}")


class VoiceoverScene(Scene):
    """VoiceoverScene subset required by manim/part4.py and manim/part5.py."""

    def set_speech_service(self, speech_service):
        self.speech_service = speech_service

    @contextmanager
    def voiceover(self, text: str, **kwargs):
        if not hasattr(self, "speech_service"):
            raise RuntimeError("Call set_speech_service(...) before voiceover(...).")

        result = self.speech_service.generate_from_text(text, **kwargs)
        audio_path = Path(result["original_audio"])
        if not audio_path.is_absolute():
            audio_path = Path(self.speech_service.cache_dir) / audio_path

        duration = _audio_duration(str(audio_path))
        self.add_sound(str(audio_path))
        yield SimpleNamespace(duration=duration)


__all__ = ["VoiceoverScene"]
