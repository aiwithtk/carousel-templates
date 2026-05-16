#!/usr/bin/env python3
"""
Usage: python render.py --brief brief.json --output_dir output/
"""
import argparse
import json
import os
from PIL import Image, ImageDraw, ImageFont

def load_font(font_name, size):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    font_path = os.path.join(base_dir, "fonts", font_name)
    if not os.path.exists(font_path):
        # Fallback to system font if local font not found
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
        line_height = zone.get("line_height", zone["font_size"] + 10)
        max_width = zone["w"]
        
        # Gestion des listes à puces
        if "bullet_char" in zone:
            items = text.split('\n')
            y_offset = zone["y"]
            for item in items:
                if not item.strip():
                    continue
                bullet_text = f"{zone['bullet_char']} {item.strip()}"
                lines = wrap_text(bullet_text, font, max_width - 30, draw)
                for line in lines:
                    bbox = draw.textbbox((0,0), line, font=font)
                    line_h = bbox[3] - bbox[1]
                    x = zone["x"] + 30
                    draw.text((x, y_offset), line, fill=zone["color"], font=font)
                    y_offset += line_h + 5
        else:
            # Texte normal avec retour à la ligne automatique
            lines = wrap_text(text, font, max_width, draw)
            y_offset = zone["y"]
            for line in lines:
                bbox = draw.textbbox((0,0), line, font=font)
                line_h = bbox[3] - bbox[1]
                if zone.get("align") == "center":
                    x = zone["x"] + (zone["w"] - (bbox[2]-bbox[0])) // 2
                elif zone.get("align") == "right":
                    x = zone["x"] + zone["w"] - (bbox[2]-bbox[0])
                else:  # left
                    x = zone["x"]
                draw.text((x, y_offset), line, fill=zone["color"], font=font)
                y_offset += line_h + 5
    
    img.save(output_path, "PNG")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True, help="Fichier JSON du brief (conforme au schema)")
    parser.add_argument("--output_dir", required=True, help="Dossier de sortie pour les slides générées")
    args = parser.parse_args()
    
    with open(args.brief) as f:
        brief = json.load(f)
    
    theme = brief["theme"]
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Charger les zones.json du thème
    zones_config_path = os.path.join(os.path.dirname(__file__), "..", "templates", theme, "zones.json")
    with open(zones_config_path) as f:
        zones_all = json.load(f)
    
    for idx, slide in enumerate(brief["slides"]):
        template_file = slide["template"]
        template_path = os.path.join(os.path.dirname(__file__), "..", "templates", theme, template_file)
        if not os.path.exists(template_path):
            print(f"Erreur : template {template_path} introuvable")
            continue
        
        zones_config = zones_all.get(template_file, {"zones": []})
        output_path = os.path.join(args.output_dir, f"slide_{idx+1:02d}.png")
        render_slide(template_path, slide["zones"], zones_config, output_path)
        print(f"Généré : {output_path}")

if __name__ == "__main__":
    main()
