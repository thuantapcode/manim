# voice_generator.py
import sys
import asyncio
import edge_tts
import os
import argparse
from script_data import VOICEOVER_SCRIPT

sys.stdout.reconfigure(encoding='utf-8')

# Available Vietnamese voices on Edge TTS:
# - vi-VN-NamMinhNeural (Male)
# - vi-VN-HoaiMyNeural (Female)
DEFAULT_VOICE = "vi-VN-NamMinhNeural"

async def generate_audio(voice_name, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Using voice: {voice_name}")
    print(f"Output directory: {output_dir}")
    print("-" * 50)
    
    for segment in VOICEOVER_SCRIPT:
        file_id = segment["id"]
        text = segment["text"]
        output_file = os.path.join(output_dir, f"{file_id}.mp3")
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"-> File {file_id}.mp3 already exists, skipping.\n")
            continue
            
        print(f"Generating voice for: {file_id}.mp3...")
        print(f"Text: \"{text[:60]}...\"")
        
        max_retries = 5
        success = False
        for attempt in range(1, max_retries + 1):
            try:
                communicate = edge_tts.Communicate(text, voice_name)
                await communicate.save(output_file)
                print(f"-> Saved to {output_file}\n")
                success = True
                break
            except Exception as e:
                print(f"-> [Attempt {attempt}/{max_retries}] Error generating {file_id}: {e}")
                if attempt < max_retries:
                    wait_time = attempt * 2
                    print(f"   Waiting {wait_time}s before retrying...")
                    await asyncio.sleep(wait_time)
        if not success:
            print(f"-> Failed to generate {file_id} after {max_retries} attempts.\n")
        else:
            await asyncio.sleep(0.5)

def main():
    parser = argparse.ArgumentParser(description="Generate voiceover using edge-tts.")
    parser.add_argument(
        "--voice", 
        type=str, 
        default=DEFAULT_VOICE, 
        choices=["vi-VN-NamMinhNeural", "vi-VN-HoaiMyNeural"],
        help="TTS Voice name (vi-VN-NamMinhNeural or vi-VN-HoaiMyNeural)"
    )
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default=r"assets/audio", 
        help="Path to output directory"
    )
    args = parser.parse_args()
    
    asyncio.run(generate_audio(args.voice, args.output_dir))

if __name__ == "__main__":
    main()
