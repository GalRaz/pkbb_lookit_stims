import ffmpeg
import os
from pathlib import Path

def trim_video(input_path, output_path, trim_duration=15):
    # Get the duration of the video
    probe = ffmpeg.probe(input_path)
    duration = float(probe['format']['duration'])
    
    # Calculate the new duration to trim the last 15 seconds
    new_duration = duration - trim_duration if duration > trim_duration else 0
    
    # Execute FFmpeg command to trim the video
    ffmpeg.input(input_path, ss=0, t=new_duration).output(output_path, c='copy').run(overwrite_output=True)

def process_videos(input_folder, output_folder, trim_duration=15):
    input_folder_path = Path(input_folder)
    output_folder_path = Path(output_folder)
    
    # Create the output folder if it does not exist
    output_folder_path.mkdir(parents=True, exist_ok=True)
    
    # Walk through the input folder to find video files
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                input_path = Path(root) / file
                relative_path = input_path.relative_to(input_folder_path)
                output_path = output_folder_path / relative_path
                
                # Create output directory if it does not exist
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                print(f'Trimming {input_path} and saving to {output_path}')
                try:
                    trim_video(str(input_path), str(output_path), trim_duration)
                except ffmpeg.Error as e:
                    print(f'Error processing {input_path}: {e}')

if __name__ == '__main__':
    input_folder = 'lookit_unity_stims'
    output_folder = 'trimmed_stims'
    
    process_videos(input_folder, output_folder)
