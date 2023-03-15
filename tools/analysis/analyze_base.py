import pandas as pd
from pathlib import Path

def pick(columns, options):
    for o in options:
        if o in columns:
            return o
    return None

def main():
    path = Path('dashboard/baseLimpa.xlsx')
    if not path.exists():
        print('Arquivo não encontrado:', path)
        return
    df = pd.read_excel(path)
    cols = df.columns.tolist()

    col_date = pick(cols, ['Order Date','Data do Pedido','Data','OrderDate'])
    col_sales = pick(cols, ['Sales','Vendas','Sales Amount','Valor'])
    col_cat = pick(cols, ['Category','Categoria','Category Name'])
    col_prod = pick(cols, ['Product Name','Produto','Nome do Produto'])
    col_year = pick(cols, ['Ano','Year'])

    if col_year:
        df['Ano'] = pd.to_numeric(df[col_year], errors='coerce')
    else:
        if not col_date:
            print('Coluna de data não encontrada. Colunas disponíveis:', cols)
            return
        df['Ano'] = pd.to_datetime(df[col_date], errors='coerce').dt.year

    if not col_sales:
        print('Coluna de vendas não encontrada. Colunas disponíveis:', cols)
        return
    df['Sales'] = pd.to_numeric(df[col_sales], errors='coerce').fillna(0)
    if col_cat:
        df['Category'] = df[col_cat]
    if col_prod:
        df['Product Name'] = df[col_prod]

    # Limpa linhas sem ano válido
    df = df[pd.notnull(df['Ano'])]

    anos = sorted(df['Ano'].unique())
    cats = sorted(df['Category'].dropna().unique())

    print('Anos presentes na base:', anos)
    print('Número de categorias:', len(cats))

    # Somas por categoria/ano
    pivot = df.pivot_table(index='Category', columns='Ano', values='Sales', aggfunc='sum', fill_value=0)
    print('\nSoma de vendas por Categoria x Ano (R$):')
    print(pivot.round(2).to_string())

    zero_counts = (pivot == 0).sum(axis=1)
    print('\nQuantidade de anos com zero por categoria:')
    print(zero_counts.to_string())

    # Top 10 por total
    top10 = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
    print('\nTop 10 produtos por vendas totais:')
    print(top10.round(2).to_string())

    print('\nVendas por ano para cada produto do Top 10:')
    for name in top10.index:
        s = df[df['Product Name'] == name].groupby('Ano')['Sales'].sum()
        vals = [s.get(a, 0.0) for a in anos]
        print(f"- {name}: " + ' | '.join([f"{a}: R$ {v:,.2f}" for a, v in zip(anos, vals)]))

if __name__ == '__main__':
    main()