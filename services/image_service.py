import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from config import Config

def generate_summary_image(total, top_countries, last_refreshed_at_iso):
    """
    total: int
    top_countries: list of dicts [{"name":..., "estimated_gdp":..., "flag_url":...}, ...]
    last_refreshed_at_iso: ISO string
    """
    os.makedirs(Config.CACHE_DIR, exist_ok=True)
    img_w, img_h = 1200, 700
    background = (255, 255, 255)
    title_color = (20, 20, 20)
    text_color = (40, 40, 40)

    img = Image.new("RGB", (img_w, img_h), color=background)
    draw = ImageDraw.Draw(img)

    # Load default font
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        font_text = ImageFont.truetype("DejaVuSans.ttf", 20)
    except Exception:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # Title
    draw.text((40, 30), "Countries Refresh Summary", font=font_title, fill=title_color)
    draw.text((40, 80), f"Total countries: {total}", font=font_text, fill=text_color)
    draw.text((40, 105), f"Last refresh: {last_refreshed_at_iso}", font=font_text, fill=text_color)

    # Table header
    draw.text((40, 150), "Top 5 Countries by Estimated GDP", font=font_text, fill=title_color)

    y = 190
    for i, c in enumerate(top_countries, start=1):
        name = c.get("name")
        gdp = c.get("estimated_gdp")
        gdp_str = f"{gdp:,.2f}" if gdp is not None else "N/A"
        draw.text((60, y), f"{i}. {name}", font=font_text, fill=text_color)
        draw.text((400, y), gdp_str, font=font_text, fill=text_color)
        y += 32

    # Save
    out_path = os.path.join(Config.CACHE_DIR, "summary.png")
    img.save(out_path)
    return out_path

