## Objetivo
- Manter os rótulos do eixo X como estão no gráfico “Top Produtos por Vendas”, mas exibir o nome completo do produto ao passar o cursor.
- Preparar commit/push apenas após você testar o preview, garantindo que a data do commit não ultrapasse março/2023.
- Revisar arquivos da raiz e propor organização/remoção do que não for profissional.

## Alterações no Dashboard de Vendas
- Local do gráfico: `dashboard/dashboard_vendas.html` na criação de `topProductsChart` (aprox. 847–898).
- Implementação:
  - Definir `const fullProductNames = topProducts.map(item => item[0]);` antes de instanciar o gráfico.
  - Manter `labels` atuais (sem alterar o eixo X).
  - Adicionar `plugins.tooltip.callbacks` para mostrar o nome completo:
    - `title`: usar `fullProductNames[items[0].dataIndex]` como título do tooltip.
    - `label`: manter `Vendas (R$): <valor>` formatado.
- Resultado: eixo X continua compacto e o hover revela o nome verdadeiro do produto.

## Testes e Validação (sem commit)
- Iniciar preview local e verificar:
  - O gráfico “Top Produtos por Vendas” mantém rótulos do eixo X.
  - Tooltips mostram nomes completos dos produtos (inclui casos com nomes longos reais, ex.: "Bush Somerset Collection Bookcase").
  - Exportações CSV/PDF seguem funcionando.

## Commit/Push (após aprovação)
- Após você confirmar o preview:
  - Fazer commit único com `--date` anterior a março/2023 (ex.: `2023-03-15T10:00:00`).
  - Mensagem objetiva (ex.: "feat: tooltips com nomes completos no Top Produtos").
  - Push para GitHub.

## Limpeza/Organização da Raiz
- Arquivos atuais na raiz: `.artifactignore`, `.gitattributes`, `.gitignore`, `LICENSE.md`, `README.md`, `preview_readme.html`, `requirements.txt`, `t --count HEAD`.
- Propostas:
  - `t --count HEAD`: remover (exibe histórico de commits, não é profissional expor). Alternativa: mover para `tools/dev/` se você preferir manter internamente.
  - `preview_readme.html`: mover para `dashboard/` ou `docs/` caso seja material de apoio/landing. Se não for consumido por GitHub Pages, remover.
  - Manter: `.gitignore`, `.gitattributes`, `.artifactignore`, `LICENSE.md`, `README.md`, `requirements.txt`.

## Observações de MCP context7
- Implementação mínima, sem comentários no código.
- Alterações restritas ao front-end (`dashboard_vendas.html`), sem alterar dados fonte.
- Não executar commits ou alterações de estado até sua aprovação.

## Confirmação
- Posso aplicar as mudanças no gráfico com tooltips, preparar a limpeza da raiz conforme proposto e abrir o preview para você validar antes do commit/push?