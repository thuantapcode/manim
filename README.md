# Training LLMs in Academia - Manim Video

This repository renders one continuous video containing Parts 1 through 5.

## Included

- `main.py`: Parts 1-3 and the unified `FullVideo` scene.
- `part4.py`, `part5.py`: Parts 4 and 5.
- `edge_service.py`: Edge TTS speech service.
- `manim_voiceover/`: Local compatibility layer used by Parts 4-5.
- `assets/audio/`: Pre-generated narration for Parts 1-3.

## Install

Use Python 3.12, then install:

```powershell
python -m pip install -r requirements.txt
```

Parts 4-5 use Edge TTS and require an Internet connection on the first render.

## Render

Quick preview:

```powershell
python main.py
```

Full HD 1080p:

```powershell
$env:MANIM_QUALITY="-qh"
python main.py
```

The final file is written to:

```text
media/videos/main/1080p60/FullVideo.mp4
```
