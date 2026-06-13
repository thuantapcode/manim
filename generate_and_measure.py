# generate_and_measure.py
import sys
import os
import asyncio
from pydub import AudioSegment
from script_data import VOICEOVER_SCRIPT

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    voice = "vi-VN-NamMinhNeural"
    output_dir = "assets/audio"
    
    # Import generate_audio function from voice_generator
    from voice_generator import generate_audio
    
    print("Step 1: Generating audio files...")
    await generate_audio(voice, output_dir)
    
    print("\nStep 2: Measuring durations using pydub...")
    total_time = 0.0
    results = []
    
    for segment in VOICEOVER_SCRIPT:
        file_id = segment["id"]
        file_path = os.path.join(output_dir, f"{file_id}.mp3")
        
        if not os.path.exists(file_path):
            print(f"Error: {file_path} does not exist!")
            continue
            
        try:
            audio = AudioSegment.from_mp3(file_path)
            duration = len(audio) / 1000.0 # in seconds
            results.append((file_id, duration, total_time))
            print(f"- {file_id}.mp3: duration = {duration:.2f}s, start_time = {total_time:.2f}s")
            total_time += duration
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    print("\n" + "="*50)
    print("VOICEOVER TIMING CONFIGURATION FOR main.py:")
    print("="*50)
    for file_id, duration, start_time in results:
        print(f'            ("assets/audio/{file_id}.mp3", {start_time:.1f}),  # duration: {duration:.1f}s')

if __name__ == "__main__":
    asyncio.run(main())
