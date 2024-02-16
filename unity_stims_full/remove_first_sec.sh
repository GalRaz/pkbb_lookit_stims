#!/bin/bash

# Directory containing your video files
SEARCH_DIR="fam8_copy"

# Loop through all video files (.mp4, .mkv, .avi) in the directory and its subdirectories
find "$SEARCH_DIR" -type f \( -iname \*.mp4 -o -iname \*.mkv -o -iname \*.avi \) -print0 | while IFS= read -r -d '' file; do
    echo "Processing file: $file"
    
    # Create a temporary file for the edited video, ensuring it's in the same directory as the original
    temp_file="$(mktemp "${file%.*}_tempXXXXXX.${file##*.}")"

    # Use FFmpeg to edit the first second of audio to be quiet, with -y to overwrite temp files if necessary
    ffmpeg -y -i "$file" -filter_complex "[0:a]volume=enable='between(t,0,1)':volume=0[out]" -map 0:v -map "[out]" -c:v copy "$temp_file"

    # Check if FFmpeg operation was successful before replacing
    if [ $? -eq 0 ]; then
        # Replace the original file with the edited video
        mv -f "$temp_file" "$file"
        echo "Successfully processed: $file"
    else
        echo "Error processing file: $file"
        # Remove the temporary file if FFmpeg failed
        rm -f "$temp_file"
    fi
done
