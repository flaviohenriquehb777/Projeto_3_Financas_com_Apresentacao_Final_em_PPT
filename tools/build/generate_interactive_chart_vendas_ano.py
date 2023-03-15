import os
import pandas as pd
import plotly.graph_objects as go
import json


def format_mil_br(v: float) -> str:
    return f"{(v/1000):.2f}".replace('.', ',') + " Mil"


def format_currency_br(v: float) -> str:
    s = f"{v:,.2f}"
    return "R$ " + s.replace(',', 'X').replace('.', ',').replace('X', '.')


def main():
    # Caminho da base
    base_path = os.path.join('dashboard', 'baseLimpa.xlsx')
    if not os.path.exists(base_path):
        base_path = 'baseLimpa.xlsx'

    # Lê planilha
    df = pd.read_excel(base_path, engine='openpyxl')

    # Normaliza Ano corretamente
    if 'Ano' in df.columns:
        df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')
    else:
        if 'Order Date' in df.columns:
            dt = pd.to_datetime(df['Order Date'], errors='coerce')
        elif 'Data do Pedido' in df.columns:
            dt = pd.to_datetime(df['Data do Pedido'], errors='coerce')
        elif 'order_date' in df.columns:
            dt = pd.to_datetime(df['order_date'], errors='coerce')
        elif 'OrderDate' in df.columns:
            dt = pd.to_datetime(df['OrderDate'], errors='coerce')
        else:
            dt = pd.to_datetime(None)
        df['Ano'] = dt.dt.year

    # Coluna de vendas
    sales_col = None
    for c in ['Sales', 'Vendas', 'Sales Amount', 'Valor']:
        if c in df.columns:
            sales_col = c
            break
    if sales_col is None:
        raise RuntimeError('Não foi possível localizar a coluna de vendas na base.')
    df['Sales'] = pd.to_numeric(df[sales_col], errors='coerce').fillna(0)

    # Agrupa por ano
    g = df.groupby('Ano', dropna=True)['Sales'].sum().sort_index()

    # Ordena por 2015–2018 se existir
    anos_target = [2015, 2016, 2017, 2018]
    if all(a in g.index for a in anos_target):
        g = g.loc[anos_target]

    # Figura Plotly
    x_vals = g.index.astype(str).tolist()
    y_vals = g.values.tolist()
    text_vals = [format_mil_br(v) for v in y_vals]
    hover_vals = [f"{ano}: {format_currency_br(v)}" for ano, v in zip(g.index.tolist(), y_vals)]
    bar_colors = ['#2c35b8'] * len(y_vals)

    fig = go.Figure(
        data=[
            go.Bar(
                x=x_vals,
                y=y_vals,
                marker=dict(color=bar_colors),
                text=text_vals,
                textposition='outside',
                textfont=dict(color='white', size=12),
                hovertext=hover_vals,
                hovertemplate='%{hovertext}<extra></extra>',
            )
        ]
    )

    fig.update_layout(
        title=dict(text='Vendas por Ano', x=0.5, font=dict(size=22, color='#ffffff', family='Segoe UI, Arial, sans-serif')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False,
        xaxis=dict(showline=False, tickfont=dict(size=12, color='#ffffff')),
        yaxis=dict(visible=False),
        hoverlabel=dict(bgcolor='#2c35b8', font=dict(color='white')),
    )

    # Saída: HTML autônomo com fundo transparente
    out_dir = os.path.join('dashboard', 'interactive_charts')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'vendas_por_ano.html')

    # Incluir Plotly inline para evitar dependência de rede/CDN
    div_html = fig.to_html(include_plotlyjs=True, full_html=False, div_id='chartVendasAno')
    
    html = """
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      html, body {{ background: transparent; margin: 0; }}
      #chartVendasAno {{ width: 100%; height: 500px; }}
    </style>
  </head>
  <body>
    """ + div_html + """
    <script>
      (function(){
        var gd = document.getElementById('chartVendasAno');
        var defaultColor = '#2c35b8';
        var dimColor = 'rgba(255,255,255,0.18)';
        var selectedYear = null;

        function resetColors(){
          var n = gd.data[0].x.length;
          var colors = Array(n).fill(defaultColor);
          var opacities = Array(n).fill(1);
          Plotly.restyle(gd, {'marker.color': [colors], 'marker.opacity': [opacities]});
        }

        gd.on('plotly_click', function(ev){
          try {
            var year = ev.points[0].x;
            var xs = gd.data[0].x;
            var idx = xs.indexOf(year);
            // toggle: se clicar novamente no mesmo ano, desfaz seleção
            if (selectedYear === year) {
              selectedYear = null;
              resetColors();
              if (window.parent) {
                window.parent.postMessage({type: 'selectYear', year: null}, '*');
              }
              return;
            }
            selectedYear = year;
            var colors = xs.map(function(){return dimColor;});
            var opacities = xs.map(function(){return 1;});
            if (idx >= 0) {
              colors[idx] = '#ffffff';
              opacities = xs.map(function(){return 0.18;});
              opacities[idx] = 1;
            }
            Plotly.restyle(gd, {'marker.color': [colors], 'marker.opacity': [opacities]});
            if (window.parent) {
              window.parent.postMessage({type: 'selectYear', year: year}, '*');
            }
          } catch(e) { console.warn(e); }
        });

        gd.on('plotly_doubleclick', function(){
          resetColors();
          if (window.parent) {
            window.parent.postMessage({type: 'selectYear', year: null}, '*');
          }
          selectedYear = null;
        });

        resetColors();
      })();
    </script>
  </body>
</html>
"""

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Gerado: {out_path}')


if __name__ == '__main__':
    main()