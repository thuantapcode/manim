"""Rebuild and replace the FullVideo audio track without rerendering video."""

from pathlib import Path
import wave

import av
import numpy as np


ROOT = Path(__file__).resolve().parent
VIDEO = ROOT / "media/videos/main/1080p60/FullVideo.mp4"
OUTPUT = VIDEO.with_name("FullVideo_audio_fixed.mp4")
MASTER_WAV = ROOT / "media/FullVideo_master_audio.wav"

SAMPLE_RATE = 48_000
CHANNELS = 2

# Start times measured from the rendered FullVideo timeline.
S1_START = 0.0
S2_START = 141.9987
S3_START = 429.261789

TRACKS = [
    (S1_START, [
        ("s0_00_models.mp3", 0.0), ("s0_01_power.mp3", 10.8),
        ("s0_02_open_api.mp3", 14.6), ("s0_03_industry.mp3", 32.4),
        ("s0_04_university_question.mp3", 45.4), ("s0_05_lecture.mp3", 52.7),
        ("s0_06_reports.mp3", 74.1), ("s0_07_redaction.mp3", 86.4),
        ("s0_08_rare_papers.mp3", 94.2), ("s0_09_aspiration.mp3", 105.6),
        ("s0_10_compute_barrier.mp3", 116.9),
    ]),
    (S2_START, [
        ("s1_00_creativity.mp3", 0.0), ("s1_01_student_question.mp3", 13.3),
        ("s1_02_own_path.mp3", 26.6), ("s1_03_why_irreplaceable.mp3", 41.0),
        ("s1_04_why_it_runs.mp3", 55.7), ("s1_05_swe_bench.mp3", 73.9),
        ("s1_06_evaluation_tools.mp3", 113.9),
        ("s1_07_reverse_engineering.mp3", 135.6),
        ("s1_08_research_opportunities.mp3", 167.4),
        ("s1_09_barrier_compute.mp3", 206.8),
        ("s1_10_barrier_infrastructure.mp3", 258.5),
        ("s1_11_barrier_data.mp3", 268.7),
    ]),
    (S3_START, [
        ("s3_00_slms_pillar.mp3", 0.0), ("s3_01_why_slms.mp3", 10.1),
        ("s3_02_no_budget.mp3", 15.1), ("s3_03_easy_to_run.mp3", 19.6),
        ("s3_04_downloads_llama.mp3", 28.3), ("s3_05_llama1_gpt3.mp3", 40.9),
        ("s3_06_ask_academic.mp3", 51.3), ("s3_07_gpu_hours_cost.mp3", 58.2),
        ("s3_08_be_smarter.mp3", 68.9), ("s3_09_sheared_llama_princeton.mp3", 77.4),
        ("s3_10_how_it_works.mp3", 81.6), ("s3_11_two_steps.mp3", 93.6),
        ("s3_12_step_one_pruning.mp3", 96.0), ("s3_13_pruning_details.mp3", 105.5),
        ("s3_14_constrained_optimization.mp3", 117.5),
        ("s3_15_lagrange.mp3", 121.8), ("s3_16_resources_split.mp3", 130.5),
        ("s3_17_what_data.mp3", 143.6), ("s3_18_red_pyjama.mp3", 148.7),
        ("s3_19_random_data.mp3", 159.1), ("s3_20_failure.mp3", 163.3),
        ("s3_21_loss_imbalance.mp3", 165.7), ("s3_22_c4_vs_github.mp3", 174.3),
        ("s3_23_scaling_laws.mp3", 183.7),
        ("s3_24_predict_reference_loss.mp3", 192.3),
        ("s3_25_optimal_mixtures.mp3", 200.9), ("s3_26_gained_fruits.mp3", 211.3),
        ("s3_27_cheap_resource.mp3", 222.2), ("s3_28_sota.mp3", 236.1),
        ("s3_29_downloads_hf.mp3", 247.3), ("s3_30_industry_adopted.mp3", 256.0),
        ("s3_31_qwen_limit.mp3", 273.8),
    ]),
]


def decode_audio(path: Path) -> np.ndarray:
    container = av.open(str(path))
    stream = next(s for s in container.streams if s.type == "audio")
    resampler = av.AudioResampler(format="s16", layout="stereo", rate=SAMPLE_RATE)
    chunks = []
    for frame in container.decode(stream):
        for converted in resampler.resample(frame):
            chunks.append(converted.to_ndarray().reshape(CHANNELS, -1).T)
    for converted in resampler.resample(None):
        chunks.append(converted.to_ndarray().reshape(CHANNELS, -1).T)
    return np.concatenate(chunks).astype(np.int32)


def build_master(duration: float) -> None:
    mix = np.zeros((int(duration * SAMPLE_RATE) + 1, CHANNELS), dtype=np.int32)
    audio_dir = ROOT / "assets/audio"
    for scene_start, clips in TRACKS:
        for name, offset in clips:
            clip = decode_audio(audio_dir / name)
            start = int((scene_start + offset) * SAMPLE_RATE)
            end = min(start + len(clip), len(mix))
            mix[start:end] += clip[: end - start]

    pcm = np.clip(mix, -32768, 32767).astype("<i2")
    MASTER_WAV.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(MASTER_WAV), "wb") as wav:
        wav.setnchannels(CHANNELS)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm.tobytes())


def replace_audio() -> None:
    source = av.open(str(VIDEO))
    audio = av.open(str(MASTER_WAV))
    output = av.open(str(OUTPUT), "w")

    source_video = next(s for s in source.streams if s.type == "video")
    source_audio = next(s for s in audio.streams if s.type == "audio")
    out_video = output.add_stream_from_template(source_video)
    out_audio = output.add_stream("aac", rate=SAMPLE_RATE)
    out_audio.layout = "stereo"

    for packet in source.demux(source_video):
        if packet.dts is not None:
            packet.stream = out_video
            output.mux(packet)

    for frame in audio.decode(source_audio):
        frame.pts = None
        for packet in out_audio.encode(frame):
            output.mux(packet)
    for packet in out_audio.encode(None):
        output.mux(packet)

    output.close()
    source.close()
    audio.close()
    VIDEO.replace(VIDEO.with_name("FullVideo_silent_backup.mp4"))
    OUTPUT.replace(VIDEO)


if __name__ == "__main__":
    with av.open(str(VIDEO)) as container:
        duration = float(container.duration / av.time_base)
    build_master(duration)
    replace_audio()
    print(VIDEO)
