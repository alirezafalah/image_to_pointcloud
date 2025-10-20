from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
import math

def create_checkered_pdf_with_margins(output_filename, boxes_across_width=12, margin_cm=1.5):
    """
    Generates an A4 PDF with a high-contrast black and white checkered pattern.
    A margin is added to all sides to ensure the grid is within the
    printer's printable area, preventing cutoff squares.
    """
    
    # --- MODIFIED: Use high-contrast black and white ---
    color1 = colors.black
    color2 = colors.white
    # ---
    
    # Get the dimensions of an A4 page
    page_width, page_height = A4
    
    # Define the margin size
    MARGIN_SIZE = margin_cm * cm
    print(f"Using a {margin_cm:.1f} cm margin on all sides.")
    
    # Calculate the 'drawable' area inside the margins
    drawable_width = page_width - (2 * MARGIN_SIZE)
    drawable_height = page_height - (2 * MARGIN_SIZE)
    
    # Calculate the perfect square size based on the drawable area
    box_size = drawable_width / boxes_across_width
    
    # Calculate how many full rows of this size fit on the drawable height
    num_boxes_x = boxes_across_width
    num_boxes_y = math.floor(drawable_height / box_size)
    
    # Report the calculated size
    box_size_in_cm = box_size / cm
    print(f"To fit {num_boxes_x} squares perfectly, each square will be {box_size_in_cm:.2f} cm.")
    print(f"Generating PDF with a uniform grid of {num_boxes_x}x{num_boxes_y} squares...")
    
    c = canvas.Canvas(output_filename, pagesize=A4)
    
    # Loop through each row and column to draw the checkered pattern
    for row in range(num_boxes_y):
        for col in range(num_boxes_x):
            if (row + col) % 2 == 0:
                c.setFillColor(color1)
            else:
                c.setFillColor(color2)
            
            # Offset the x and y coordinates by the margin
            x = MARGIN_SIZE + (col * box_size)
            y = MARGIN_SIZE + (row * box_size)
            
            c.rect(x, y, box_size, box_size, stroke=0, fill=1)
            
    c.save()
    print(f"Successfully created '{output_filename}' with margins! ✅")

if __name__ == "__main__":
    # You can still control the number of boxes
    # For your 10x15 grid (9x14 internal), you'd set this to 10.
    NUMBER_OF_BOXES_WIDE = 10 
    
    # You can also change the margin size here if needed
    MARGIN_IN_CM = 1.5 
    
    create_checkered_pdf_with_margins(
        "checkered_a4_bw.pdf", 
        NUMBER_OF_BOXES_WIDE, 
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