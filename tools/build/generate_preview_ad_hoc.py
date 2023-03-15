from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 1200, 630
BG = (15, 15, 18)
SURFACE = (23, 23, 29)
SURFACE_2 = (28, 28, 34)
TEXT = (234, 234, 234)
MUTED = (165, 165, 175)
PRIMARY = (77, 171, 245)
GREEN = (66, 196, 143)
ORANGE = (255, 176, 67)
RED = (236, 98, 99)
BORDER = (40, 40, 48)
GRID = (35, 35, 42)

def load_font(size: int):
    candidates = [
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

def find_logo_path():
    candidates = [
        "dashboard/logo_fh.png",
        "dashboard/brand.png",
        "dashboard/logo.png",
        "dashboard/brand.jpg",
        "dashboard/logo.jpg",
        "dashboard/logo_miniatura.png",
    ]
    return next((p for p in candidates if os.path.exists(p)), None)

def paste_logo_in_box(img, draw, box_x, box_y, box_size, font_title):
    path = find_logo_path()
    if not path:
        dv_text = "DV"
        bbox = draw.textbbox((0, 0), dv_text, font=font_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((box_x + (box_size - tw) / 2, box_y + (box_size - th) / 2), dv_text, fill=PRIMARY, font=font_title)
        return
    try:
        logo = Image.open(path).convert("RGBA")
    except Exception:
        dv_text = "DV"
        bbox = draw.textbbox((0, 0), dv_text, font=font_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((box_x + (box_size - tw) / 2, box_y + (box_size - th) / 2), dv_text, fill=PRIMARY, font=font_title)
        return
    margin = 12
    target = box_size - margin * 2
    w, h = logo.size
    scale = target / max(w, h)
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    logo_resized = logo.resize(new_size, Image.LANCZOS)
    x = box_x + (box_size - new_size[0]) // 2
    y = box_y + (box_size - new_size[1]) // 2
    img.paste(logo_resized, (x, y), logo_resized)

def generate():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    pad = 36
    card_rect = (pad, pad, WIDTH - pad, HEIGHT - pad)
    draw.rounded_rectangle(card_rect, radius=24, fill=SURFACE, outline=BORDER, width=2)

    logo_x = pad + 28
    logo_y = pad + 26
    logo_size = 88
    draw.rounded_rectangle((logo_x, logo_y, logo_x + logo_size, logo_y + logo_size), radius=16, fill=SURFACE_2)

    font_title = load_font(36)
    font_sub = load_font(20)
    font_small = load_font(18)
    font_chip = load_font(16)
    font_btn = load_font(22)

    paste_logo_in_box(img, draw, logo_x, logo_y, logo_size, font_title)

    title = "Dashboard Análise ad hoc"
    subtitle = "Clique para abrir o dashboard de análise ad hoc"
    title_x = logo_x + logo_size + 24
    title_y = logo_y + 8
    draw.text((title_x, title_y), title, fill=TEXT, font=font_title)
    draw.text((title_x, title_y + 38), subtitle, fill=MUTED, font=font_sub)

    chips = [
        ("Vendas/Ano", "R$ 2,4M", GREEN),
        ("Top Produtos", "Top 10", PRIMARY),
        ("Categorias/Ano", "3", ORANGE),
    ]
    chip_x = title_x
    chip_y = title_y + 74
    for label, value, color in chips:
        w = 260
        h = 44
        draw.rounded_rectangle((chip_x, chip_y, chip_x + w, chip_y + h), radius=12, fill=SURFACE_2, outline=BORDER)
        draw.text((chip_x + 16, chip_y + 10), label, fill=MUTED, font=font_chip)
        draw.text((chip_x + w - 16 - draw.textlength(value, font=font_chip), chip_y + 10), value, fill=color, font=font_chip)
        chip_x += w + 16

    metric_top = logo_y + logo_size + 32
    metric_left = pad + 28
    metric_w = 280
    metric_h = 96
    gap = 22
    metrics = [
        ("Anos", "2019–2022", PRIMARY),
        ("Média/Mês", "R$ 200k", ORANGE),
        ("Categorias", "4", GREEN),
    ]
    for i, (label, value, color) in enumerate(metrics):
        x = metric_left + i * (metric_w + gap)
        y = metric_top
        draw.rounded_rectangle((x, y, x + metric_w, y + metric_h), radius=16, fill=SURFACE_2, outline=BORDER)
        draw.text((x + 18, y + 16), label, fill=MUTED, font=font_small)
        draw.text((x + 18, y + 50), value, fill=color, font=font_title)

    chart_top = metric_top + metric_h + 32
    chart_left = pad + 28
    chart_w = WIDTH - chart_left - pad - 28
    chart_h = 240
    draw.rounded_rectangle((chart_left, chart_top, chart_left + chart_w, chart_top + chart_h), radius=16, fill=SURFACE_2, outline=BORDER)

    for i in range(1, 5):
        y = chart_top + i * chart_h // 5
        draw.line((chart_left + 16, y, chart_left + chart_w - 16, y), fill=GRID, width=1)

    # barras simbolizando agrupamentos
    bar_base_y = chart_top + chart_h - 30
    bar_w = 28
    bar_gap = 18
    categories = [("Ano", 160), ("Mês", 120), ("Cat", 200), ("Top", 180), ("Prod", 140)]
    bx = chart_left + 26
    for label, value in categories:
        h = int(value)
        draw.rounded_rectangle((bx, bar_base_y - h, bx + bar_w, bar_base_y), radius=8, fill=PRIMARY)
        bx += bar_w + bar_gap

    # mini pizza
    pie_x = chart_left + chart_w - 170
    pie_y = chart_top + 120
    r = 60
    draw.ellipse((pie_x - r, pie_y - r, pie_x + r, pie_y + r), fill=SURFACE)
    pie_slices = [(GREEN, 140), (PRIMARY, 120), (ORANGE, 60), (RED, 40)]
    start = 0
    for color, angle in pie_slices:
        draw.pieslice((pie_x - r, pie_y - r, pie_x + r, pie_y + r), start, start + angle, fill=color)
        start += angle

    # CTA
    btn_w, btn_h = 280, 56
    btn_x = WIDTH - pad - btn_w - 32
    btn_y = chart_top + chart_h + 28
    draw.rounded_rectangle((btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), radius=12, fill=PRIMARY)
    draw.text((btn_x + 24, btn_y + 16), "Abrir Dashboard", fill=(11, 27, 42), font=font_btn)

    footer = "Sam's Club - Walmart • Projeto de Análise Financeira"
    draw.text((pad + 28, HEIGHT - pad - 28), footer, fill=MUTED, font=font_small)

    output_path = "dashboard/preview_ad_hoc.png"
    img.save(output_path, format="PNG", optimize=True)
    print(f"Gerado: {output_path}")

if __name__ == "__main__":
    generate()