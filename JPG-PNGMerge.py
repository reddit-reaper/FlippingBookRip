from PIL import Image
import os
import shutil  # Import shutil for file copying

# Setup output directory
output_dir = 'output2'
os.makedirs(output_dir, exist_ok=True)

def composite_images(png_path, jpg_path, output_path):
    # Load the JPG image
    img_jpg = Image.open(jpg_path).convert('RGBA')

    # Load the PNG image and resize it to match the JPG dimensions
    img_png = Image.open(png_path).resize(img_jpg.size).convert('RGBA')

    # Composite the PNG over the JPG
    combined = Image.alpha_composite(img_jpg, img_png)

    # Convert back to RGB and save the output
    combined.convert('RGB').save(output_path, 'JPEG')

# Process each JPG and corresponding PNG in the directory
for jpg_file in filter(lambda f: f.lower().endswith('.jpg'), os.listdir('.')):
    png_file = f"{jpg_file.rsplit('.', 1)[0]}.png"
    output_path = os.path.join(output_dir, jpg_file)
    
    if os.path.exists(png_file):
        composite_images(png_file, jpg_file, output_path)
        print(f"Processed and merged: {jpg_file} with {png_file}")
    else:
        # If no corresponding PNG exists, copy the JPG to the output directory
        shutil.copy(os.path.join('.', jpg_file), os.path.join(output_dir, jpg_file))
        print(f"Copied {jpg_file} to {output_dir}")
