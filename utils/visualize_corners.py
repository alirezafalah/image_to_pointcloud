import cv2
import numpy as np
import glob
import os
import math

# --- Configuration ---

# CRITICAL: Set this to your grid's INTERNAL corner count.
#
GRID_WIDTH = 9  # (squares - 1)
GRID_HEIGHT = 13 # (squares - 1)
CHESSBOARD_SIZE = (GRID_WIDTH, GRID_HEIGHT)

# --- File Paths ---
IMAGE_DIR = 'data/video_calibration'  # Directory containing calibration images
OUTPUT_DIR = 'data/verification_images/video_method_verification'



def find_and_visualize_corners(image_dir, output_dir, grid_size):
    """
    Loads images, finds chessboard corners, and saves visualized results.
    """
    print(f"Starting corner detection for grid size: {grid_size}")
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Find all jpg and png images (case-insensitive)
    all_paths = []
    extensions = ['*.jpg', '*.JPG', '*.png', '*.PNG']
    for ext in extensions:
        all_paths.extend(glob.glob(os.path.join(image_dir, ext)))

    # Use a set to remove duplicates, then convert back to a sorted list
    image_paths = sorted(list(set(all_paths)))

    if not image_paths:
        print(f"Error: No images found in '{image_dir}'. Searched for .jpg/.png")
        return

    print(f"Found {len(image_paths)} images. Processing...")

    # --- Criteria for corner refinement ---
    # This is not used for finding, but for making the found corners more precise.
    # We will use this in the *next* script, but it's good to define it.
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    for image_path in image_paths:
        img_name = os.path.basename(image_path)
        img = cv2.imread(image_path)
        
        if img is None:
            print(f"Warning: Could not read image {img_name}. Skipping.")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- NEW DEBUG CODE STARTS HERE ---
        
        # 1. Save the grayscale image
        # gray_output_path = os.path.join(output_dir, f"gray_{img_name}")
        # cv2.imwrite(gray_output_path, gray)

        # 2. Apply and save a global threshold
        # You can change '110' to any value you want to test
        # GLOBAL_THRESHOLD_VALUE = 110
        # ret_thresh, thresh_global = cv2.threshold(gray, GLOBAL_THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        # global_path = os.path.join(output_dir, f"thresh_global_{img_name}")
        # cv2.imwrite(global_path, thresh_global)
        
        # 3. Apply and save an adaptive threshold
        # This shows what the algorithm *tries* to do internally
        # You can tune '15' (block size) and '2' (constant)
        # thresh_adaptive = cv2.adaptiveThreshold(gray, 255, 
        #                                        cv2.ADAPTIVE_THRESH_MEAN_C, 
        #                                        cv2.THRESH_BINARY, 15, 2)
        # adaptive_path = os.path.join(output_dir, f"thresh_adaptive_{img_name}")
        # cv2.imwrite(adaptive_path, thresh_adaptive)
        
        # --- NEW DEBUG CODE ENDS HERE ---


        # Find the chessboard corners
        # This is the main function you were asking about
        ret, corners = cv2.findChessboardCorners(gray, grid_size, None)

        # If corners are found, draw them
        if ret == True:
            print(f"  [SUCCESS] Found corners in {img_name}")
            
            # --- Optional refinement ---
            # You can uncomment this to get slightly more precise corners,
            # but it's not strictly necessary for just visualization.
            corners_refined = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            # ---
            
            # This is the visualization function you wanted:
            # It draws the detected corners on the original color image
            cv2.drawChessboardCorners(img, grid_size, corners, ret)
            output_path = os.path.join(output_dir, f"detected_{img_name}")
        
        else:
            # If no corners are found, save the original image with a 'failed' prefix
            print(f"  [FAILURE] Could not find corners in {img_name}")
            output_path = os.path.join(output_dir, f"failed_{img_name}")

        # Save the visualization image
        cv2.imwrite(output_path, img)
        
    print(f"\nProcessing complete. Check the '{output_dir}' folder to verify detections.")


# --- Main execution ---
if __name__ == "__main__":
    find_and_visualize_corners(IMAGE_DIR, OUTPUT_DIR, CHESSBOARD_SIZE)