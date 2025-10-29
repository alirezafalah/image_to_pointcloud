"""
Utility script to extract a fixed number of frames from all .MOV files
in a specified directory and save them as images for calibration.
"""

import cv2
import os
import glob
import math

# --- Configuration ---

# 1. Directory to search for videos
#    (Using '.' for the current directory, as in your Colab example)
VIDEO_SOURCE_DIR = '.'

# 2. Directory to save the extracted frames
#    (Matching the calibrator.py input)
OUTPUT_DIR = '../data/video_calibration'

# 3. Number of frames to extract from each video
FRAMES_TO_EXTRACT = 70

# --- End Configuration ---


def extract_frames_from_videos(video_dir, output_dir, frame_count):
    """
    Finds all .mov files in video_dir, extracts a fixed number
    of frames from each, and saves them to output_dir.
    """
    
    print(f"Starting frame extraction...")
    print(f"Searching for videos in: {os.path.abspath(video_dir)}")
    print(f"Saving frames to: {os.path.abspath(output_dir)}")
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Find all .mov files (case-insensitive)
    search_paths = [
        glob.glob(os.path.join(video_dir, '*.mov')),
        glob.glob(os.path.join(video_dir, '*.MOV'))
    ]
    video_files = sorted(list(set(sum(search_paths, []))))

    if not video_files:
        print(f"Error: No .mov or .MOV files found in '{video_dir}'.")
        return

    print(f"Found {len(video_files)} video file(s):")
    for f in video_files:
        print(f"  - {f}")

    # Process each video file
    for video_file in video_files:
        video_basename = os.path.basename(video_file)
        video_name_without_ext = os.path.splitext(video_basename)[0]
        
        cap = cv2.VideoCapture(video_file)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_file}. Skipping.")
            continue

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames <= 0:
            print(f"Warning: Video {video_file} has 0 or unreadable frames. Skipping.")
            cap.release()
            continue

        print(f"\nProcessing '{video_basename}' (Total frames: {total_frames})...")

        # Determine the number of frames to actually extract
        if total_frames < frame_count:
            print(f"  Warning: Video has fewer than {frame_count} frames. Extracting all {total_frames} frames.")
            frames_to_extract_current = total_frames
        else:
            frames_to_extract_current = frame_count

        # Calculate interval to get evenly spaced frames
        if frames_to_extract_current > 1:
            # Use math.floor to ensure we don't go past the last frame
            interval = math.floor(total_frames / frames_to_extract_current)
            # Generate indices starting from 0
            frame_indices = [min(i * interval, total_frames - 1) for i in range(frames_to_extract_current)]
        elif frames_to_extract_current == 1:
            frame_indices = [0] # Extract only the first frame
        else:
            print(f"  No frames to extract for {video_basename}. Skipping.")
            cap.release()
            continue
            
        # Ensure the last frame is included if we are extracting the max
        if frames_to_extract_current > 1 and total_frames > 1 and frame_indices[-1] < (total_frames -1):
             frame_indices[-1] = total_frames -1


        # Extract and save frames
        frames_saved = 0
        for i, frame_pos in enumerate(frame_indices):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            ret, frame = cap.read()
            
            if ret:
                # Construct a unique output filename
                output_filename = f"{video_name_without_ext}_frame_{i+1:03d}.jpg"
                output_path = os.path.join(output_dir, output_filename)
                
                cv2.imwrite(output_path, frame)
                frames_saved += 1
            else:
                print(f"  Warning: Could not read frame at position {frame_pos} from {video_file}")

        print(f"  Successfully saved {frames_saved} frames.")
        cap.release()

    print("\nFrame extraction complete. ✅")


# --- Main execution ---
if __name__ == "__main__":
    extract_frames_from_videos(
        VIDEO_SOURCE_DIR, 
        OUTPUT_DIR, 
        FRAMES_TO_EXTRACT
    )