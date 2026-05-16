#!/usr/bin/env python3
"""
Usage: python export.py --input output/ --output final/ --platform instagram
"""
import argparse
import os
from PIL import Image

SIZES = {
    "instagram": (1080, 1350),
    "linkedin": (1080, 1350),
    "square": (1080, 1080)
}

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        target_w, target_h = size
        img_ratio = img.width / img.height
        target_ratio = target_w / target_h
        
        if img_ratio > target_ratio:
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        else:
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))
        
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Dossier contenant les slides originales (output/)")
    parser.add_argument("--output", required=True, help="Dossier de destination")
    parser.add_argument("--platform", choices=["instagram", "linkedin", "square"], required=True)
    args = parser.parse_args()
    
    size = SIZES[args.platform]
    os.makedirs(args.output, exist_ok=True)
    
    for fname in sorted(os.listdir(args.input)):
        if fname.endswith(".png"):
            input_path = os.path.join(args.input, fname)
            output_path = os.path.join(args.output, fname)
            resize_image(input_path, output_path, size)
            print(f"Exported {fname} to {args.platform}")

if __name__ == "__main__":
    main()
