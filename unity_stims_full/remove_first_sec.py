import os
from moviepy.editor import VideoFileClip
from moviepy.audio.fx.all import volumex

def process_video(file_path):
    # Load the video file
    video = VideoFileClip(file_path)
    
    # Apply audio transformation to make the first second quiet
    # This applies a volume multiplier of 0 (silence) to the first second
    new_audio = video.audio.fx(volumex, 0, 0, 1)
    video = video.set_audio(new_audio)
    
    # Write the changes back to the original file
    video.write_videofile(file_path, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)

def process_directory(directory):
    # Loop through all files in the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check for video file extensions
            if file.lower().endswith(('.mp4', '.mkv', '.avi')):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")
                try:
                    process_video(file_path)
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")

# Specify the directory containing your video files
SEARCH_DIR = 'fam8_copy'
process_directory(SEARCH_DIR)
