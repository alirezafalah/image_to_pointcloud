import cv2
import numpy as np
import glob
import os

# --- Configuration ---

# 1. CRITICAL: Set this to your grid's INTERNAL corner count.
GRID_WIDTH = 9
GRID_HEIGHT = 13
CHESSBOARD_SIZE = (GRID_WIDTH, GRID_HEIGHT)

# 2. CRITICAL: Set the physical size of one square.
#    Measure one square on your printed checkerboard.
#    This is the *most important* value for getting a real-world scale.
SQUARE_SIZE_CM = 1.8  # <--- !!! UPDATE THIS VALUE !!!

IMAGE_DIR = 'data/video_calibration'
OUTPUT_FILE = 'data/video_calibration_data.npz'

# --- End Configuration ---


def calibrate_camera(image_dir, grid_size, square_size):
    """
    Performs camera calibration using checkerboard images.
    """
    print(f"Starting calibration...")
    print(f"Grid size: {grid_size}, Square size: {square_size} cm")
    
    # Termination criteria for cornerSubPix
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # 3D points in real-world space (in cm)
    # We create a perfect grid (z=0)
    objp = np.zeros((grid_size[0] * grid_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:grid_size[0], 0:grid_size[1]].T.reshape(-1, 2)
    objp = objp * square_size # Scale by our measured square size

    # Lists to store 3D object points and 2D image points from all images
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane

    # Find all jpg and png images (case-insensitive)
    all_paths = []
    extensions = ['*.jpg', '*.JPG', '*.png', '*.PNG']
    for ext in extensions:
        all_paths.extend(glob.glob(os.path.join(image_dir, ext)))
    image_paths = sorted(list(set(all_paths)))

    if not image_paths:
        print(f"Error: No images found in '{image_dir}'.")
        return

    print(f"Found {len(image_paths)} images. Detecting corners...")
    
    successful_detections = 0
    image_shape = None

    for image_path in image_paths:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Warning: Could not read {image_path}. Skipping.")
            continue
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        if image_shape is None:
            image_shape = gray.shape[::-1] # Get (width, height)

        # 1. Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, grid_size, None)

        # 2. If found, add to our lists
        if ret == True:
            successful_detections += 1
            print(f"  [SUCCESS] Found corners in {os.path.basename(image_path)}")
            
            # Add the "ground truth" 3D points
            objpoints.append(objp)

            # 3. Refine the corner locations (as you discovered)
            corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            
            # Add the refined 2D points
            imgpoints.append(corners_refined)
        else:
            print(f"  [FAILURE] Could not find corners in {os.path.basename(image_path)}")

    print(f"\nCalibration complete. Used {successful_detections} successful detections.")
    
    if successful_detections == 0:
        print("Error: No images with successful detections. Cannot calibrate.")
        return

    # --- 4. Run the final calibration ---
    # This is the function that solves the linear algebra problem
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, image_shape, None, None
    )

    if not ret:
        print("Error: Calibration failed.")
        return

    print("\n--- Calibration Results ---")
    print("Camera Matrix (K):")
    print(mtx)
    print("\nDistortion Coefficients (k1, k2, p1, p2, k3):")
    print(dist)

    # --- 5. Calculate and report reprojection error ---
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        total_error += error

    mean_error = total_error / len(objpoints)
    print(f"\nMean Reprojection Error: {mean_error:.4f} pixels")
    print("----------------------------")
    if mean_error < 0.5:
        print("This is a high-quality calibration. 🎯")
    elif mean_error < 1.0:
        print("This is a decent calibration. 👍")
    else:
        print("This calibration quality is low. Consider retaking photos. ⚠️")

    # --- 6. Save the results ---
    print(f"\nSaving calibration data to '{OUTPUT_FILE}'...")
    np.savez(
        OUTPUT_FILE, 
        mtx=mtx, 
        dist=dist, 
        rvecs=rvecs, 
        tvecs=tvecs
    )
    print("Done.")


# --- Main execution ---
if __name__ == "__main__":
    calibrate_camera(IMAGE_DIR, CHESSBOARD_SIZE, SQUARE_SIZE_CM)