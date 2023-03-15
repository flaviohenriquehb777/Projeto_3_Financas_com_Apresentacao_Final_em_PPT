import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def format_mil(v: float) -> str:
    # Converte para milhares com duas casas e vírgula decimal
    return f"{(v/1000):.2f}".replace('.', ',') + " Mil"


def main():
    base_path = os.path.join('dashboard', 'baseLimpa.xlsx')
    if not os.path.exists(base_path):
        # fallback: raiz
        base_path = 'baseLimpa.xlsx'

    # Lê a planilha (primeira aba)
    df = pd.read_excel(base_path, engine='openpyxl')

    # Normaliza colunas usuais
    # Tenta diversas convenções comuns
    if 'Order Date' in df.columns:
        dt = pd.to_datetime(df['Order Date'], errors='coerce')
    elif 'Data do Pedido' in df.columns:
        dt = pd.to_datetime(df['Data do Pedido'], errors='coerce')
    elif 'order_date' in df.columns:
        dt = pd.to_datetime(df['order_date'], errors='coerce')
    elif 'OrderDate' in df.columns:
        dt = pd.to_datetime(df['OrderDate'], errors='coerce')
    else:
        dt = pd.to_datetime(df.get('Ano', pd.Series(index=df.index)), errors='coerce')

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

    # Se existir o intervalo 2015–2018, fixa nessa ordem
    anos_target = [2015, 2016, 2017, 2018]
    if all(a in g.index for a in anos_target):
        g = g.loc[anos_target]

    # Estilo
    sns.set_theme(style='white')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    fig.patch.set_facecolor('#f5f5f5')
    ax.set_facecolor('#f5f5f5')

    # Barras em azul sólido
    blue = '#2c35b8'
    ax.bar(g.index.astype(str), g.values, color=blue, width=0.6)

    # Labels acima das barras
    for x, v in zip(g.index.astype(str), g.values):
        ax.text(x, v, format_mil(v), ha='center', va='bottom', fontsize=12, color=blue, fontweight='bold')

    # Título centralizado
    ax.set_title('Vendas por Ano', fontsize=22, color=blue, pad=20, fontweight='bold')

    # Eixo Y sem ticks/linha para ficar limpo
    ax.yaxis.set_ticks([])
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

    # Margem superior para labels
    ax.margins(y=0.15)

    # Caminho de saída
    out_dir = os.path.join('dashboard', 'static_charts')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'vendas_por_ano.png')
    plt.tight_layout()
    fig.savefig(out_path, facecolor=fig.get_facecolor())
    print(f'Gerado: {out_path}')


if __name__ == '__main__':
    main()