from PIL import Image, ImageDraw, ImageFont
import os

# Tamanho da imagem (thumbnail)
WIDTH, HEIGHT = 1200, 630  # proporção OpenGraph

# Paleta
BG = (15, 15, 18)
SURFACE = (23, 23, 29)
SURFACE_2 = (28, 28, 34)
TEXT = (234, 234, 234)
MUTED = (165, 165, 175)
PRIMARY = (77, 171, 245)
PRIMARY_DARK = (33, 128, 210)
GREEN = (66, 196, 143)
ORANGE = (255, 176, 67)
RED = (236, 98, 99)
BORDER = (40, 40, 48)
GRID = (35, 35, 42)


def load_font(size: int):
    """Tenta carregar uma fonte moderna (Segoe UI/Arial), com fallback."""
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


img = Image.new("RGB", (WIDTH, HEIGHT), BG)
draw = ImageDraw.Draw(img)

# Card base
pad = 36
card_rect = (pad, pad, WIDTH - pad, HEIGHT - pad)
draw.rounded_rectangle(card_rect, radius=24, fill=SURFACE, outline=BORDER, width=2)

# Cabeçalho com logo e título
logo_x = pad + 28
logo_y = pad + 26
logo_size = 88
draw.rounded_rectangle((logo_x, logo_y, logo_x + logo_size, logo_y + logo_size), radius=16, fill=SURFACE_2)

font_title = load_font(36)
font_sub = load_font(20)
font_small = load_font(18)
font_chip = load_font(16)
font_btn = load_font(22)

def find_logo_path():
    candidates = [
        "dashboard/logo_fh.png",
        "dashboard/brand.png",
        "dashboard/logo.png",
        "dashboard/brand.jpg",
        "dashboard/logo.jpg",
    ]
    return next((p for p in candidates if os.path.exists(p)), None)

def paste_logo_in_box(img, box_x, box_y, box_size):
    path = find_logo_path()
    if not path:
        # fallback: monograma DV
        dv_text = "DV"
        bbox = draw.textbbox((0, 0), dv_text, font=font_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((box_x + (box_size - tw) / 2, box_y + (box_size - th) / 2), dv_text, fill=PRIMARY, font=font_title)
        return

    try:
        logo = Image.open(path).convert("RGBA")
    except Exception:
        # fallback: monograma DV se a imagem estiver corrompida ou inválida
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

paste_logo_in_box(img, logo_x, logo_y, logo_size)

title = "Dashboard de Vendas"
subtitle = "Clique para abrir o dashboard interativo"
title_x = logo_x + logo_size + 24
title_y = logo_y + 8
draw.text((title_x, title_y), title, fill=TEXT, font=font_title)
draw.text((title_x, title_y + 38), subtitle, fill=MUTED, font=font_sub)

# Chips informativos
chips = [
    ("Total de Vendas", "R$ 2,4M", GREEN),
    ("Pedidos", "18.254", PRIMARY),
    ("Ticket Médio", "R$ 132,10", ORANGE),
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

# Cards de métricas resumidas
metric_top = logo_y + logo_size + 32
metric_left = pad + 28
metric_w = 280
metric_h = 96
gap = 22
metrics = [
    ("Clientes únicos", "8.432", PRIMARY),
    ("Itens/pedido", "2,4", ORANGE),
    ("Crescimento", "+7,8%", GREEN),
]
for i, (label, value, color) in enumerate(metrics):
    x = metric_left + i * (metric_w + gap)
    y = metric_top
    draw.rounded_rectangle((x, y, x + metric_w, y + metric_h), radius=16, fill=SURFACE_2, outline=BORDER)
    draw.text((x + 18, y + 16), label, fill=MUTED, font=font_small)
    draw.text((x + 18, y + 50), value, fill=color, font=font_title)

# Área de gráficos
chart_top = metric_top + metric_h + 32
chart_left = pad + 28
chart_w = WIDTH - chart_left - pad - 28
chart_h = 240
draw.rounded_rectangle((chart_left, chart_top, chart_left + chart_w, chart_top + chart_h), radius=16, fill=SURFACE_2, outline=BORDER)

# Grid horizontal
for i in range(1, 5):
    y = chart_top + i * chart_h // 5
    draw.line((chart_left + 16, y, chart_left + chart_w - 16, y), fill=GRID, width=1)

# Série de barras (Top Produtos)
bar_base_y = chart_top + chart_h - 30
bar_w = 28
bar_gap = 18
categories = [
    ("A", 110), ("B", 160), ("C", 90), ("D", 200), ("E", 140), ("F", 180)
]
bx = chart_left + 26
for label, value in categories:
    h = int(value)
    draw.rounded_rectangle((bx, bar_base_y - h, bx + bar_w, bar_base_y), radius=8, fill=PRIMARY)
    bx += bar_w + bar_gap

# (Removido) Série de linha para não cruzar as barras e poluir visual

# Mini pizza (segmentos)
pie_x = chart_left + chart_w - 170
pie_y = chart_top + 120  # baixar mais o gráfico de pizza para ficar dentro da área
r = 60
draw.ellipse((pie_x - r, pie_y - r, pie_x + r, pie_y + r), fill=SURFACE)
pie_slices = [(GREEN, 140), (PRIMARY, 120), (ORANGE, 60), (RED, 40)]
start = 0
for color, angle in pie_slices:
    draw.pieslice((pie_x - r, pie_y - r, pie_x + r, pie_y + r), start, start + angle, fill=color)
    start += angle

# Botão CTA
btn_w, btn_h = 280, 56
btn_x = WIDTH - pad - btn_w - 32
btn_y = chart_top + chart_h + 28
draw.rounded_rectangle((btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), radius=12, fill=PRIMARY)
draw.text((btn_x + 24, btn_y + 16), "Abrir Dashboard", fill=(11, 27, 42), font=font_btn)

# Rodapé
footer = "Sam's Club - Walmart • Projeto de Análise Financeira"
draw.text((pad + 28, HEIGHT - pad - 28), footer, fill=MUTED, font=font_small)

# Salvar
output_path = "dashboard/preview.png"
img.save(output_path, format="PNG", optimize=True)
print(f"Gerado: {output_path}")

def generate_favicon_from_logo():
    """Gera favicon em múltiplas resoluções (PNG + ICO) a partir da logo, com fallback."""
    FAV_SIZE = 512
    favicon_png_path = "dashboard/favicon.png"
    favicon_ico_path = "dashboard/favicon.ico"
    sizes = [16, 32, 48, 64, 128, 256, 512]
    logo_path = find_logo_path()
    if logo_path:
        try:
            base = Image.open(logo_path).convert("RGBA")
        except Exception:
            logo_path = None
        # PNG 512x512
        canvas = Image.new("RGBA", (FAV_SIZE, FAV_SIZE), (0, 0, 0, 0))
        margin = 16
        target = FAV_SIZE - margin * 2
        w, h = base.size
        scale = target / max(w, h)
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        resized = base.resize(new_size, Image.LANCZOS)
        x = (FAV_SIZE - new_size[0]) // 2
        y = (FAV_SIZE - new_size[1]) // 2
        canvas.paste(resized, (x, y), resized)
        canvas.save(favicon_png_path, format="PNG", optimize=True)
        # ICO multiresolução
        ico_base = Image.new("RGBA", (FAV_SIZE, FAV_SIZE), (0, 0, 0, 0))
        ico_base.paste(resized, (x, y), resized)
        ico_base.save(favicon_ico_path, sizes=[(s, s) for s in sizes])
        # PNGs por tamanho
        for s in sizes:
            canvas_s = canvas.resize((s, s), Image.LANCZOS)
            canvas_s.save(f"dashboard/favicon-{s}.png", format="PNG", optimize=True)
        print(f"Gerado: {favicon_png_path}, {favicon_ico_path} e variações PNG (from {logo_path})")
        return

    # Fallback: ícone minimalista se a logo não estiver presente
    fav = Image.new("RGBA", (FAV_SIZE, FAV_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fav)
    # base sutil
    draw.ellipse((8, 8, FAV_SIZE - 8, FAV_SIZE - 8), fill=(23, 23, 29, 255))
    # monograma DV
    font_logo = load_font(220)
    logo_text = "DV"
    bbox_logo = draw.textbbox((0, 0), logo_text, font=font_logo)
    ltw = bbox_logo[2] - bbox_logo[0]
    lth = bbox_logo[3] - bbox_logo[1]
    draw.text(((FAV_SIZE - ltw) / 2, (FAV_SIZE - lth) / 2 - 6), logo_text, fill=PRIMARY, font=font_logo)
    fav.save(favicon_png_path, format="PNG", optimize=True)
    # também gerar um ICO simples
    fav_rgb = fav.convert("RGB")
    fav_rgb.save(favicon_ico_path, sizes=[(s, s) for s in sizes])
    print(f"Gerado: {favicon_png_path} e {favicon_ico_path} (fallback)")


# Executa geração de favicon ao final
generate_favicon_from_logo()

# Salvar a miniatura/preview
img.save("dashboard/preview.png", format="PNG", optimize=True)