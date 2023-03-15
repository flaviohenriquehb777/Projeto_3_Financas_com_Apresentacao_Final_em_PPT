#!/usr/bin/env python3
"""
Script para criar uma miniatura preview.png idêntica ao dashboard real
Substitui o "DV" pelo logo_miniatura.png na posição correta
"""

import os
from PIL import Image, ImageDraw, ImageFont
import sys
import math

def create_dashboard_preview():
    """Cria uma miniatura idêntica ao dashboard com logo_miniatura.png"""
    
    # Caminhos dos arquivos
    dashboard_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dashboard')
    logo_path = os.path.join(dashboard_dir, 'logo_miniatura.png')
    preview_path = os.path.join(dashboard_dir, 'preview.png')
    
    try:
        # Carrega o logo
        logo = Image.open(logo_path)
        print(f"Logo carregado: {logo.size}")
        
        # Dimensões da miniatura (proporção do dashboard real)
        width, height = 1200, 675
        
        # Cores do dashboard
        bg_color = '#1a1a1a'  # Fundo principal
        card_color = '#2a2a2a'  # Cor dos cards
        text_primary = '#ffffff'  # Texto principal
        text_secondary = '#b0b0b0'  # Texto secundário
        accent_blue = '#4dabf5'  # Azul do dashboard
        accent_yellow = '#fbbf24'  # Amarelo
        accent_green = '#10b981'  # Verde
        accent_red = '#ef4444'  # Vermelho
        accent_orange = '#f97316'  # Laranja
        
        # Cria fundo
        background = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(background)
        
        # Fontes
        try:
            font_large = ImageFont.truetype("arial.ttf", 36)
            font_medium = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 18)
            font_tiny = ImageFont.truetype("arial.ttf", 14)
            font_bold = ImageFont.truetype("arialbd.ttf", 28)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_tiny = ImageFont.load_default()
            font_bold = ImageFont.load_default()
        
        # Logo no canto superior esquerdo (substituindo DV)
        logo_size = 60
        logo_resized = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        logo_x, logo_y = 30, 30
        
        if logo_resized.mode == 'RGBA':
            background.paste(logo_resized, (logo_x, logo_y), logo_resized)
        else:
            background.paste(logo_resized, (logo_x, logo_y))
        
        # Título principal
        title_x = logo_x + logo_size + 20
        draw.text((title_x, 35), "Dashboard de Vendas", fill=text_primary, font=font_large)
        draw.text((title_x, 75), "Clique para abrir o dashboard interativo", fill=text_secondary, font=font_small)
        
        # Métricas superiores (linha horizontal)
        metrics_y = 130
        metric_width = 280
        metric_spacing = 300
        
        metrics = [
            ("Total de Vendas", "R$ 2,4M", accent_blue),
            ("Pedidos", "18.254", accent_blue),
            ("Ticket Médio", "R$ 132,10", accent_blue)
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            x = 50 + (i * metric_spacing)
            # Card de fundo
            draw.rectangle([x-10, metrics_y-10, x+metric_width-10, metrics_y+60], fill=card_color, outline='#3a3a3a')
            # Texto
            draw.text((x, metrics_y), label, fill=text_secondary, font=font_tiny)
            draw.text((x, metrics_y+25), value, fill=color, font=font_medium)
        
        # Cards de KPIs (segunda linha)
        kpi_y = 230
        kpi_width = 250
        kpi_spacing = 280
        
        kpis = [
            ("Clientes únicos", "8.432", accent_blue),
            ("Itens/pedido", "2,4", accent_yellow),
            ("Crescimento", "+7,8%", accent_green)
        ]
        
        for i, (label, value, color) in enumerate(kpis):
            x = 50 + (i * kpi_spacing)
            # Card de fundo
            draw.rectangle([x-10, kpi_y-10, x+kpi_width-10, kpi_y+80], fill=card_color, outline='#3a3a3a')
            # Texto
            draw.text((x, kpi_y), label, fill=text_secondary, font=font_tiny)
            draw.text((x, kpi_y+30), value, fill=color, font=font_bold)
        
        # Definir área inferior para centralização dos gráficos
        bottom_area_start = 300  # Início da área inferior
        bottom_area_height = 280  # Altura da área inferior
        bottom_center_y = bottom_area_start + (bottom_area_height // 2)
        
        # Margem padrão das bordas
        margin = 50
        
        # Gráfico de barras expandido (lado esquerdo) - MAIOR E CENTRALIZADO
        chart_x = margin
        bar_width = 40
        bar_spacing = 50
        max_bar_height = 200
        chart_y = bottom_center_y - (max_bar_height // 2)  # Centralizado verticalmente
        
        bar_heights = [120, 160, 140, 180, 150, 170, 130, 190]  # Alturas maiores
        bar_colors = [accent_blue, accent_blue, accent_green, accent_blue, accent_yellow, accent_blue, accent_orange, accent_blue]
        
        for i, (height, color) in enumerate(zip(bar_heights, bar_colors)):
            x = chart_x + i * bar_spacing
            y = chart_y + max_bar_height - height
            draw.rectangle([x, y, x + bar_width, chart_y + max_bar_height], fill=color)
        
        # Gráfico de pizza (lado direito) - CENTRALIZADO E SIMÉTRICO
        pie_radius = 140
        pie_center_x = width - margin - pie_radius  # Mesma distância da borda direita
        pie_center_y = bottom_center_y  # Centralizado verticalmente
        
        # Desenha círculo base
        pie_bbox = [pie_center_x - pie_radius, pie_center_y - pie_radius, 
                    pie_center_x + pie_radius, pie_center_y + pie_radius]
        
        # Cores das fatias
        pie_colors = [accent_orange, accent_green, accent_blue, accent_yellow]
        angles = [0, 90, 180, 270, 360]
        
        # Desenhar fatias da pizza
        for i, color in enumerate(pie_colors):
            start_angle = angles[i]
            end_angle = angles[i + 1]
            draw.pieslice(pie_bbox, start_angle, end_angle, fill=color)
        
        # Adicionar indicadores de performance no canto inferior esquerdo
        perf_x = 50
        perf_y = 540
        
        # Indicador 1: Seta para cima (crescimento)
        arrow_points = [(perf_x, perf_y + 20), (perf_x + 10, perf_y), (perf_x + 20, perf_y + 20), (perf_x + 15, perf_y + 20), (perf_x + 15, perf_y + 30), (perf_x + 5, perf_y + 30), (perf_x + 5, perf_y + 20)]
        draw.polygon(arrow_points, fill=accent_green)
        
        # Texto do indicador
        draw.text((perf_x + 30, perf_y + 10), "Vendas ↗", fill=text_secondary, font=font_small)
        
        # Removido o texto do rodapé para limpar a visualização
        
        # Botão "Abrir Dashboard" (canto inferior direito)
        button_x = width - 250
        button_y = height - 80
        button_width = 200
        button_height = 40
        
        # Fundo do botão
        draw.rectangle([button_x, button_y, button_x + button_width, button_y + button_height], 
                      fill=accent_blue, outline=accent_blue)
        
        # Texto do botão
        button_text = "Abrir Dashboard"
        text_bbox = draw.textbbox((0, 0), button_text, font=font_small)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = button_x + (button_width - text_width) // 2
        text_y = button_y + (button_height - text_height) // 2
        draw.text((text_x, text_y), button_text, fill='#ffffff', font=font_small)
        
        # Salva a imagem
        background.save(preview_path, 'PNG', optimize=True)
        print(f"Nova miniatura salva em: {preview_path}")
        print(f"Dimensões: {background.size}")
        
        return True
        
    except Exception as e:
        print(f"Erro ao criar miniatura: {e}")
        return False

if __name__ == "__main__":
    success = create_dashboard_preview()
    if success:
        print("✅ Miniatura atualizada com sucesso!")
        sys.exit(0)
    else:
        print("❌ Erro ao atualizar miniatura")
        sys.exit(1)