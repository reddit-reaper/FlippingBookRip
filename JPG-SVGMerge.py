import cairosvg
from PIL import Image
import os
import shutil

# Setup output directory
output_dir = 'output2'
os.makedirs(output_dir, exist_ok=True)

def svg_to_png(svg_path, png_path):
    # Convert SVG to PNG
    cairosvg.svg2png(url=svg_path, write_to=png_path)

def composite_images(svg_path, jpg_path, output_path):
    temp_png_path = svg_path.rsplit('.', 1)[0] + '_temp.png'
    # Convert SVG to PNG
    svg_to_png(svg_path, temp_png_path)

    # Now, proceed as before with the temp PNG
    with Image.open(jpg_path).convert('RGBA') as img_jpg, Image.open(temp_png_path).resize(img_jpg.size).convert('RGBA') as img_png:
        # Composite the PNG over the JPG
        combined = Image.alpha_composite(img_jpg, img_png)
        # Convert back to RGB and save the output
        combined.convert('RGB').save(output_path, 'JPEG')

    # Remove the temporary PNG file
    os.remove(temp_png_path)

def flatten_svg(svg_path, output_path):
    temp_png_path = svg_path.rsplit('.', 1)[0] + '_temp.png'
    # Convert SVG to PNG
    svg_to_png(svg_path, temp_png_path)

    # Flatten the PNG as before
    with Image.open(temp_png_path).convert('RGBA') as img_png:
        background = Image.new('RGBA', img_png.size, (255, 255, 255, 255))
        flattened = Image.alpha_composite(background, img_png)
        flattened.convert('RGB').save(output_path, 'JPEG')

    # Remove the temporary PNG file
    os.remove(temp_png_path)

# Process each JPG and corresponding SVG in the directory
jpg_files = {f.rsplit('.', 1)[0] for f in os.listdir('.') if f.lower().endswith('.jpg')}
svg_files = {f.rsplit('.', 1)[0] for f in os.listdir('.') if f.lower().endswith('.svg')}

for base_name in jpg_files:
    jpg_file = base_name + '.jpg'
    svg_file = base_name + '.svg'
    output_path = os.path.join(output_dir, jpg_file)
    
    if os.path.exists(svg_file):
        composite_images(svg_file, jpg_file, output_path)
        print(f"Processed and merged: {jpg_file} with {svg_file}")
        svg_files.discard(base_name)
    else:
        shutil.copy(os.path.join('.', jpg_file), os.path.join(output_dir, jpg_file))
        print(f"Copied {jpg_file} to {output_dir}")

# Process remaining SVGs without a corresponding JPG
for base_name in svg_files:
    svg_file = base_name + '.svg'
    output_path = os.path.join(output_dir, base_name + '.jpg')
    flatten_svg(svg_file, output_path)
    print(f"Flattened and copied {svg_file} to {output_dir}")
