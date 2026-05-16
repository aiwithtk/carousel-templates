#!/usr/bin/env python3
import argparse
import json
from PIL import Image, ImageDraw, ImageFont
import os

def load_font(font_name, size):
    font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', font_name)
    if not os.path.exists(font_path):
        fallbacks = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Cache/Arial.ttf",
            "/Library/Fonts/Arial.ttf"
        ]
        for fb in fallbacks:
            if os.path.exists(fb):
                return ImageFont.truetype(fb, size)
        return ImageFont.load_default()
    return ImageFont.truetype(font_path, size)

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0,0), test_line, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def render_slide(template_path, zones_content, zones_config, output_path):
    img = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    for zone_name, text in zones_content.items():
        zone = next((z for z in zones_config["zones"] if z["name"] == zone_name), None)
        if not zone or not text:
            continue
        font = load_font(zone["font"], zone["font_size"])
        lines = wrap_text(text, font, zone["w"], draw)
        y_offset = zone["y"]
        for line in lines:
            bbox = draw.textbbox((0,0), line, font=font)
            line_height = bbox[3] - bbox[1]
            if zone["align"] == "center":
                x = zone["x"] + (zone["w"] - (bbox[2]-bbox[0])) // 2
            elif zone["align"] == "right":
                x = zone["x"] + zone["w"] - (bbox[2]-bbox[0])
            else:
                x = zone["x"]
            draw.text((x, y_offset), line, fill=zone["color"], font=font)
            y_offset += line_height + 5
    img.save(output_path, "PNG")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", help="Chemin du fichier template PNG")
    parser.add_argument("--zones", help="JSON string des contenus par zone")
    parser.add_argument("--brief", help="Fichier JSON contenant la configuration complète")
    parser.add_argument("--output", required=True, help="Chemin de sortie de l'image générée")
    args = parser.parse_args()
    
    if args.brief:
        with open(args.brief) as f:
            brief = json.load(f)
        template_file = brief.get("template_file") or (os.path.basename(args.template) if args.template else None)
        if not template_file: return
        
        if args.template:
            template_path = os.path.join(os.path.dirname(args.template), template_file)
        else:
            template_path = os.path.join("templates", brief.get("theme", "corporate"), template_file)
            
        zones_content = brief["zones"]
        theme_dir = os.path.dirname(template_path)
        zones_config_path = os.path.join(theme_dir, "zones.json")
        with open(zones_config_path) as f:
            zones_config_all = json.load(f)
        zones_config = zones_config_all[os.path.basename(template_path)]
    else:
        template_path = args.template
        zones_content = json.loads(args.zones)
        theme_dir = os.path.dirname(template_path)
        zones_config_path = os.path.join(theme_dir, "zones.json")
        with open(zones_config_path) as f:
            zones_config_all = json.load(f)
        zones_config = zones_config_all[os.path.basename(template_path)]
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    render_slide(template_path, zones_content, zones_config, args.output)

if __name__ == "__main__":
    main()
