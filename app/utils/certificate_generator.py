"""
Certificate generator using Pillow (PIL)
Overlays text dynamically on the premium certificate template.
"""
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from flask import current_app

def _get_font(font_name, size):
    """Safely load a font from the template folder or fallback to default."""
    font_path = os.path.join(current_app.root_path, '..', 'certificate_template', 'fonts', font_name)
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()

def _draw_centered_text(draw, text, image_width, y_pos, font, fill=(0, 0, 0)):
    """Draw text horizontally centered at a specific Y coordinate."""
    # Get bounding box for the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    # Calculate X position to center the text
    x_pos = (image_width - text_width) / 2
    
    # Draw the text
    draw.text((x_pos, y_pos), text, font=font, fill=fill)

def generate_certificate(student_name, course_title, date_issued, certificate_uid):
    """
    Generate a high-quality certificate image and save it to the static folder.
    Returns the generated filename.
    """
    # Define paths
    template_path = os.path.join(current_app.root_path, '..', 'certificate_template', 'base.png')
    filename = f"{certificate_uid}.png"
    save_path = os.path.join(current_app.root_path, 'static', 'certificates', filename)
    
    # Load base template
    try:
        img = Image.open(template_path)
    except IOError:
        # Fallback to a blank image if template is missing
        img = Image.new('RGB', (1024, 1024), color=(255, 255, 255))
        
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Load fonts
    font_name = _get_font("GreatVibes-Regular.ttf", int(width * 0.08))
    font_course = _get_font("Roboto-Medium.ttf", int(width * 0.03))
    font_small = _get_font("Roboto-Regular.ttf", int(width * 0.015))
    
    # --- Draw Text Overlays ---
    
    # 1. Student Name (Large elegant cursive font)
    # The template has a large blank area. We center it vertically roughly at 45% of the height
    _draw_centered_text(draw, student_name.title(), width, int(height * 0.40), font=font_name, fill=(28, 40, 51))
    
    # 2. Description Text
    _draw_centered_text(draw, "has successfully completed the course", width, int(height * 0.52), font=font_small, fill=(86, 101, 115))
    
    # 3. Course Title
    _draw_centered_text(draw, course_title.upper(), width, int(height * 0.57), font=font_course, fill=(20, 90, 160))
    
    # 4. Date and Signatures
    # The template has signature lines near the bottom. 
    # Left line: "PRESIDENT / DEAN"
    # Right line: "DIRECTOR / FACULTY"
    # We will just fill in the dates below those lines.
    
    date_str = date_issued.strftime("%B %d, %Y")
    
    # Position for Date (Left)
    draw.text((int(width * 0.42), int(height * 0.84)), date_str, font=font_small, fill=(0, 0, 0))
    
    # Position for Date (Right)
    draw.text((int(width * 0.69), int(height * 0.84)), date_str, font=font_small, fill=(0, 0, 0))
    
    # 5. Certificate Verification UID
    uid_text = f"Certificate ID: {certificate_uid}"
    _draw_centered_text(draw, uid_text, width, int(height * 0.92), font=font_small, fill=(128, 128, 128))
    
    # Ensure directory exists and save
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save(save_path, quality=95)
    
    return filename
