from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
import math

def create_checkered_pdf_with_margins(output_filename, box_size_mm=18, margin_cm=1.5):
    """
    Generates an A4 PDF with a checkered pattern using dark colors (high contrast to white).
    Four corner squares have unique colors for orientation tracking.
    A margin is added to all sides for printer compatibility.
    """
    
    # --- Checkered pattern colors (high contrast to white for easy masking) ---
    # Using distinct hues for easy HSV segmentation
    color1 = colors.HexColor('#8B0000')  # Dark red (H~0)
    color2 = colors.HexColor('#00008B')  # Dark blue (H~240)
    
    # --- Corner marker colors (all different, easy to distinguish) ---
    top_left_color = colors.HexColor('#FFD700')  # Gold/Yellow
    top_right_color = colors.HexColor('#00FF00')  # Bright green
    bottom_left_color = colors.HexColor('#FF00FF')  # Magenta
    bottom_right_color = colors.HexColor('#00FFFF')  # Cyan
    # ---
    
    # Get the dimensions of an A4 page
    page_width, page_height = A4
    
    # Define the margin size
    MARGIN_SIZE = margin_cm * cm
    print(f"Using a {margin_cm:.1f} cm margin on all sides.")
    
    # Calculate the 'drawable' area inside the margins
    drawable_width = page_width - (2 * MARGIN_SIZE)
    drawable_height = page_height - (2 * MARGIN_SIZE)
    
    # Convert box size from mm to points
    box_size = (box_size_mm / 10) * cm  # mm to cm, then to points
    
    # Calculate how many boxes fit in each dimension
    num_boxes_x = math.floor(drawable_width / box_size)
    num_boxes_y = math.floor(drawable_height / box_size)
    
    # Report the calculated size
    box_size_in_cm = box_size / cm
    print(f"Box size: {box_size_mm} mm ({box_size_in_cm:.2f} cm)")
    print(f"Generating PDF with a grid of {num_boxes_x}x{num_boxes_y} squares...")
    print(f"Corner squares colored for orientation tracking.")
    
    c = canvas.Canvas(output_filename, pagesize=A4)
    
    # Loop through each row and column to draw the checkered pattern
    for row in range(num_boxes_y):
        for col in range(num_boxes_x):
            current_color = None
            
            # Check if this is one of the four corner squares
            if row == 0 and col == 0:  # Bottom-left corner
                current_color = bottom_left_color
            elif row == 0 and col == num_boxes_x - 1:  # Bottom-right corner
                current_color = bottom_right_color
            elif row == num_boxes_y - 1 and col == 0:  # Top-left corner
                current_color = top_left_color
            elif row == num_boxes_y - 1 and col == num_boxes_x - 1:  # Top-right corner
                current_color = top_right_color
            else:
                # Standard checkered pattern
                if (row + col) % 2 == 0:
                    current_color = color1
                else:
                    current_color = color2
            
            c.setFillColor(current_color)
            c.setStrokeColor(current_color)  # Set stroke to same color to prevent white lines
            
            # Offset the x and y coordinates by the margin
            x = MARGIN_SIZE + (col * box_size)
            y = MARGIN_SIZE + (row * box_size)
            
            c.rect(x, y, box_size, box_size, stroke=1, fill=1)
            
    c.save()
    print(f"Successfully created '{output_filename}' with colored corners! ✅")

if __name__ == "__main__":
    # Box size in millimeters (18mm provides good calibration accuracy)
    BOX_SIZE_MM = 18
    
    # Margin size in centimeters (for printer compatibility)
    MARGIN_IN_CM = 1.5 
    
    create_checkered_pdf_with_margins(
        "checkered_calibration.pdf", 
        BOX_SIZE_MM, 
        MARGIN_IN_CM
    )


# Colored Version BELOW

# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import cm
# from reportlab.lib import colors
# import math

# def create_checkered_pdf_with_orientation_markers(output_filename, boxes_across_width=12, margin_cm=1.5):
#     """
#     Generates an A4 PDF with a high-contrast black and white checkered pattern,
#     with four distinctively colored corner squares for orientation cues.
#     """
    
#     # --- Base colors (black and white for high contrast) ---
#     base_color1 = colors.black
#     base_color2 = colors.white

#     # --- NEW: Orientation marker colors ---
#     top_left_color = colors.red
#     top_right_color = colors.blue
#     bottom_left_color = colors.green
#     bottom_right_color = colors.yellow
#     # ---
    
#     page_width, page_height = A4
    
#     MARGIN_SIZE = margin_cm * cm
#     print(f"Using a {margin_cm:.1f} cm margin on all sides.")
    
#     drawable_width = page_width - (2 * MARGIN_SIZE)
#     drawable_height = page_height - (2 * MARGIN_SIZE)
    
#     box_size = drawable_width / boxes_across_width
    
#     num_boxes_x = boxes_across_width
#     num_boxes_y = math.floor(drawable_height / box_size)
    
#     box_size_in_cm = box_size / cm
#     print(f"To fit {num_boxes_x} squares perfectly, each square will be {box_size_in_cm:.2f} cm.")
#     print(f"Generating PDF with a uniform grid of {num_boxes_x}x{num_boxes_y} squares...")
#     print(f"Adding unique colors to the corner squares for orientation.")
    
#     c = canvas.Canvas(output_filename, pagesize=A4)
    
#     # Loop through each row and column to draw the checkered pattern
#     for row in range(num_boxes_y):
#         for col in range(num_boxes_x):
#             current_color = None

#             # Check if this is one of the four corner squares
#             if row == 0 and col == 0: # Bottom-left corner square
#                 current_color = bottom_left_color
#             elif row == 0 and col == num_boxes_x - 1: # Bottom-right corner square
#                 current_color = bottom_right_color
#             elif row == num_boxes_y - 1 and col == 0: # Top-left corner square
#                 current_color = top_left_color
#             elif row == num_boxes_y - 1 and col == num_boxes_x - 1: # Top-right corner square
#                 current_color = top_right_color
#             else:
#                 # If not a special corner, use the base checkered pattern
#                 if (row + col) % 2 == 0:
#                     current_color = base_color1
#                 else:
#                     current_color = base_color2
            
#             c.setFillColor(current_color)
            
#             x = MARGIN_SIZE + (col * box_size)
#             y = MARGIN_SIZE + (row * box_size)
            
#             c.rect(x, y, box_size, box_size, stroke=0, fill=1)
            
#     c.save()
#     print(f"Successfully created '{output_filename}' with colored corners! ✨")

# if __name__ == "__main__":
#     NUMBER_OF_BOXES_WIDE = 10 
#     MARGIN_IN_CM = 1.5 
    
#     create_checkered_pdf_with_orientation_markers(
#         "checkered_a4_colored_corners.pdf", 
#         NUMBER_OF_BOXES_WIDE, 
#         MARGIN_IN_CM
#     )