from PIL import Image, ImageDraw, ImageFont

# Tamanho da imagem (thumbnail)
WIDTH, HEIGHT = 1200, 630  # proporção de compartilhamento (OpenGraph-like)

# Paleta
BG = (15, 15, 18)           # #0f0f12
CARD = (21, 21, 27)         # #15151b
TEXT = (234, 234, 234)      # #eaeaea
MUTED = (168, 168, 179)     # #a8a8b3
PRIMARY = (77, 171, 245)    # #4dabf5
ACCENT = (51, 154, 240)     # #339af0
BORDER = (42, 42, 51)       # #2a2a33

img = Image.new("RGB", (WIDTH, HEIGHT), BG)
draw = ImageDraw.Draw(img)

# Card central
pad = 40
card_rect = (pad, pad, WIDTH - pad, HEIGHT - pad)
draw.rounded_rectangle(card_rect, radius=24, fill=CARD, outline=BORDER, width=2)

# Logo quadrado com DV
logo_x = pad + 30
logo_y = pad + 30
logo_size = 80
logo_rect = (logo_x, logo_y, logo_x + logo_size, logo_y + logo_size)
draw.rounded_rectangle(logo_rect, radius=14, fill=(31, 36, 48))

font_title = ImageFont.load_default()
font_sub = ImageFont.load_default()
font_small = ImageFont.load_default()

# Letra "DV" no logo
dv_text = "DV"
# Pillow 10+: usar textbbox para medir o texto
bbox = draw.textbbox((0, 0), dv_text, font=font_title)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
draw.text((logo_x + (logo_size - tw) / 2, logo_y + (logo_size - th) / 2), dv_text, fill=PRIMARY, font=font_title)

# Título e descrição
title = "Dashboard de Vendas"
subtitle = "Clique para abrir o dashboard interativo"

title_x = logo_x + logo_size + 24
title_y = logo_y + 8
draw.text((title_x, title_y), title, fill=TEXT, font=font_title)
draw.text((title_x, title_y + 26), subtitle, fill=MUTED, font=font_sub)

# Métricas (cards pequenos)
metric_top = logo_y + logo_size + 32
metric_left = pad + 30
metric_w = 320
metric_h = 90
gap = 24

metrics = [
    ("Visualizações", "Tempo real"),
    ("Filtros", "Ano, Região, Segmento"),
    ("Exportação", "CSV e PDF"),
]

for i, (label, value) in enumerate(metrics):
    x = metric_left + i * (metric_w + gap)
    y = metric_top
    rect = (x, y, x + metric_w, y + metric_h)
    draw.rounded_rectangle(rect, radius=14, fill=(26, 26, 33), outline=(36, 36, 43))
    draw.text((x + 16, y + 16), label, fill=MUTED, font=font_small)
    draw.text((x + 16, y + 46), value, fill=(223, 230, 239), font=font_title)

# Placeholder de gráficos (linhas/barras)
chart_top = metric_top + metric_h + 36
chart_left = pad + 30
chart_w = WIDTH - chart_left - pad - 30
chart_h = 220
chart_rect = (chart_left, chart_top, chart_left + chart_w, chart_top + chart_h)
draw.rounded_rectangle(chart_rect, radius=14, fill=(26, 26, 33), outline=(36, 36, 43))

# Desenhar linhas de tendência
line_y = chart_top + chart_h // 2
for x in range(chart_left + 20, chart_left + chart_w - 20, 40):
    draw.line((x, line_y - 30, x + 20, line_y - 10), fill=PRIMARY, width=3)
    draw.line((x + 20, line_y - 10, x + 40, line_y - 22), fill=ACCENT, width=3)

# Botão "Abrir Dashboard"
btn_w, btn_h = 260, 56
btn_x = WIDTH - pad - btn_w - 30
btn_y = chart_top + chart_h + 24
btn_rect = (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h)
draw.rounded_rectangle(btn_rect, radius=12, fill=PRIMARY)
draw.text((btn_x + 24, btn_y + 18), "Abrir Dashboard", fill=(11, 27, 42), font=font_title)

# Rodapé
footer = "Sam's Club - Walmart • Projeto de Análise Financeira"
draw.text((pad + 30, HEIGHT - pad - 28), footer, fill=MUTED, font=font_small)

# Salvar em dashboard/preview.png
output_path = "dashboard/preview.png"
img.save(output_path, format="PNG", optimize=True)
print(f"Gerado: {output_path}")