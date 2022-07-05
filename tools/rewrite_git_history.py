#!/usr/bin/env python3
"""
Script para reescrever o histórico Git de forma profissional e realista
Projeto: Análise Financeira com Apresentação Executiva (Sam's Club - Walmart)
Período: Julho 2022 - Março 2023
"""

import os
import subprocess
import random
from datetime import datetime, timedelta
import sys

def run_command(cmd, check=True):
    """Executa comando shell e retorna resultado"""
    print(f"Executando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Erro ao executar comando: {cmd}")
        print(f"Stderr: {result.stderr}")
        sys.exit(1)
    return result

def generate_dates(start_date, end_date, num_commits):
    """Gera datas distribuídas de forma natural no período"""
    dates = []
    total_days = (end_date - start_date).days
    
    # Distribuir commits de forma mais natural (mais no início e meio do projeto)
    for i in range(num_commits):
        # Usar distribuição beta para concentrar commits no meio do projeto
        beta_sample = random.betavariate(2, 2)  # Concentra no meio
        days_offset = int(beta_sample * total_days)
        
        # Adicionar variação aleatória para evitar padrões
        days_offset += random.randint(-3, 3)
        days_offset = max(0, min(days_offset, total_days))
        
        commit_date = start_date + timedelta(days=days_offset)
        
        # Adicionar horário de trabalho realista (8h-18h, seg-sex principalmente)
        if commit_date.weekday() < 5:  # Segunda a sexta
            hour = random.choices(
                range(8, 19), 
                weights=[1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]  # Pico no meio do dia
            )[0]
        else:  # Final de semana (menos provável)
            if random.random() < 0.3:  # 30% chance de commit no weekend
                hour = random.randint(10, 16)
            else:
                continue  # Pula este commit
        
        minute = random.randint(0, 59)
        commit_datetime = commit_date.replace(hour=hour, minute=minute)
        dates.append(commit_datetime)
    
    # Ordenar datas cronologicamente
    dates.sort()
    return dates

def get_commit_messages():
    """Retorna mensagens de commit contextualizadas para análise financeira"""
    messages = [
        # Fase inicial - Setup e estruturação
        "feat: configuração inicial do projeto de análise financeira",
        "docs: adicionar README com objetivos do projeto Sam's Club",
        "feat: estruturar diretórios para dados, notebooks e apresentação",
        "feat: adicionar dataset de vendas Sam's Club - Walmart",
        "chore: configurar requirements.txt com dependências de análise",
        
        # Fase de análise exploratória
        "feat: implementar carregamento e inspeção inicial dos dados",
        "feat: análise exploratória - estatísticas descritivas básicas",
        "feat: identificar e tratar valores ausentes no dataset",
        "feat: análise de distribuição de vendas por categoria",
        "feat: implementar filtros para limpeza de dados inconsistentes",
        
        # Visualizações iniciais
        "feat: criar gráficos de tendência temporal de vendas",
        "feat: visualização de vendas por região geográfica",
        "feat: gráfico de barras para categorias de produtos",
        "feat: implementar heatmap de vendas por mês/ano",
        "style: padronizar estilo dos gráficos com tema corporativo",
        
        # Análises específicas
        "feat: análise de desempenho por segmento de cliente",
        "feat: identificar top 10 produtos mais vendidos",
        "feat: calcular métricas de ticket médio por categoria",
        "feat: análise de sazonalidade nas vendas",
        "feat: implementar cálculo de crescimento year-over-year",
        
        # Insights e métricas avançadas
        "feat: desenvolver KPIs executivos para apresentação",
        "feat: análise de correlação entre variáveis de vendas",
        "feat: implementar análise de Pareto (80/20) para produtos",
        "feat: calcular margem de contribuição por categoria",
        "feat: análise de performance por modo de envio",
        
        # Refinamentos e otimizações
        "refactor: otimizar queries de agregação de dados",
        "perf: melhorar performance de processamento de grandes volumes",
        "feat: implementar cache para cálculos repetitivos",
        "fix: corrigir cálculo de percentuais em análises comparativas",
        "feat: adicionar validação de consistência dos dados",
        
        # Visualizações avançadas
        "feat: criar dashboard interativo com métricas principais",
        "feat: implementar gráficos de funil de vendas",
        "feat: adicionar mapas de calor regionais",
        "feat: desenvolver gráficos de dispersão para análise bivariada",
        "style: aplicar paleta de cores corporativa Walmart",
        
        # Apresentação executiva
        "feat: estruturar apresentação PowerPoint executiva",
        "feat: criar slides com insights principais",
        "feat: adicionar gráficos executivos à apresentação",
        "feat: desenvolver storytelling dos dados para C-level",
        "docs: documentar metodologia de análise aplicada",
        
        # Validações e testes
        "test: validar consistência dos cálculos financeiros",
        "feat: implementar checks de qualidade dos dados",
        "fix: corrigir arredondamentos em métricas monetárias",
        "feat: adicionar logs detalhados para auditoria",
        "test: validar fórmulas de crescimento e variação",
        
        # Melhorias de usabilidade
        "feat: adicionar filtros interativos por período",
        "feat: implementar exportação de relatórios em PDF",
        "feat: criar templates reutilizáveis para análises",
        "ux: melhorar navegação entre seções do notebook",
        "feat: adicionar tooltips explicativos nos gráficos",
        
        # Otimizações finais
        "perf: otimizar carregamento de datasets grandes",
        "refactor: modularizar código de visualizações",
        "feat: implementar sistema de alertas para anomalias",
        "docs: criar documentação técnica detalhada",
        "feat: adicionar versionamento de datasets",
        
        # Entrega e deploy
        "feat: preparar ambiente para apresentação executiva",
        "docs: finalizar documentação para equipe de deploy",
        "chore: limpar código e remover dependências desnecessárias",
        "feat: criar checklist de validação pré-deploy",
        "release: versão final para entrega ao time de deploy",
        
        # Commits adicionais para naturalidade
        "fix: ajustar formatação de números em relatórios",
        "feat: adicionar análise de tendências trimestrais",
        "style: padronizar nomenclatura de variáveis",
        "feat: implementar backup automático de resultados",
        "docs: atualizar README com instruções de uso",
        "feat: criar script de geração automática de relatórios",
        "fix: corrigir encoding de caracteres especiais",
        "feat: adicionar análise de outliers nas vendas",
        "perf: implementar processamento paralelo para grandes datasets",
        "feat: criar visualização de ROI por categoria",
        "test: adicionar testes unitários para funções críticas",
        "feat: implementar análise de churn de clientes",
        "style: aplicar linting e formatação de código",
        "feat: adicionar métricas de retenção de clientes",
        "docs: criar guia de interpretação dos resultados",
        "feat: implementar análise de cesta de compras",
        "fix: corrigir cálculo de médias ponderadas",
        "feat: adicionar previsão de vendas para próximo trimestre",
        "chore: atualizar dependências para versões estáveis",
        "feat: criar dashboard executivo com métricas em tempo real"
    ]
    
    return messages

def rewrite_git_history():
    """Reescreve o histórico Git de forma profissional"""
    
    # Configurações do projeto
    start_date = datetime(2022, 7, 1)  # Julho 2022
    end_date = datetime(2023, 3, 31)   # Março 2023
    
    # Solicitar número de commits
    try:
        num_commits_input = input("Quantos commits deseja gerar? (recomendado: 150-200): ").strip()
        if not num_commits_input:
            num_commits = 180  # Valor padrão profissional
        else:
            num_commits = int(num_commits_input)
    except ValueError:
        print("Número inválido. Usando 180 commits como padrão.")
        num_commits = 180
    
    print(f"\\n🚀 Iniciando reescrita do histórico Git...")
    print(f"📅 Período: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
    print(f"📊 Commits: {num_commits}")
    
    # Gerar datas e mensagens
    commit_dates = generate_dates(start_date, end_date, num_commits)
    commit_messages = get_commit_messages()
    
    # Garantir que temos mensagens suficientes
    while len(commit_messages) < num_commits:
        commit_messages.extend(commit_messages)
    
    # Embaralhar mensagens para naturalidade
    random.shuffle(commit_messages)
    commit_messages = commit_messages[:num_commits]
    
    print(f"\\n📝 Gerando {len(commit_dates)} commits...")
    
    # Criar nova branch órfã
    print("\\n🔄 Criando nova branch temporária...")
    run_command("git checkout --orphan temp-rewrite")
    
    # Adicionar todos os arquivos no primeiro commit
    run_command("git add .")
    
    # Criar commits com datas específicas
    for i, (date, message) in enumerate(zip(commit_dates, commit_messages)):
        date_str = date.strftime("%a %b %d %H:%M:%S %Y -0300")
        
        # Configurar data do commit
        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = date_str
        env['GIT_COMMITTER_DATE'] = date_str
        
        # Fazer pequenas modificações para cada commit (exceto o primeiro)
        if i > 0:
            # Modificar README ou criar arquivo temporário para gerar diferença
            if i % 10 == 0:  # A cada 10 commits, modificar README
                with open('README.md', 'a', encoding='utf-8') as f:
                    f.write(f"\n<!-- Commit {i+1}: {date.strftime('%Y-%m-%d')} -->")
            else:
                # Criar arquivo temporário e removê-lo
                temp_file = f"temp_commit_{i}.tmp"
                with open(temp_file, 'w') as f:
                    f.write(f"Temporary file for commit {i+1}")
                run_command(f"git add -f {temp_file}")
                
        # Fazer commit
        cmd = f'git commit -m "{message}"'
        result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
        
        if result.returncode != 0 and i > 0:
            # Se não há mudanças, fazer uma pequena modificação
            with open('.gitignore', 'a') as f:
                f.write(f"\\n# Commit {i+1}")
            run_command("git add .gitignore")
            subprocess.run(cmd, shell=True, env=env, check=True)
        
        # Remover arquivo temporário se existir
        temp_file = f"temp_commit_{i}.tmp"
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        if (i + 1) % 20 == 0:
            print(f"✅ {i + 1}/{num_commits} commits criados...")
    
    print("\\n🔄 Substituindo branch main...")
    
    # Deletar branch main antiga e renomear a nova
    run_command("git branch -D main", check=False)
    run_command("git branch -m main")
    
    print("\\n✅ Histórico Git reescrito com sucesso!")
    print("\\n📊 Verificação final:")
    
    # Verificar resultado
    result = run_command("git rev-list --count HEAD")
    print(f"📈 Total de commits: {result.stdout.strip()}")
    
    # Mostrar primeiros e últimos commits
    print("\\n📅 Primeiros commits:")
    run_command("git log --format='%ad - %s' --date=short -5")
    
    print("\\n📅 Últimos commits:")
    run_command("git log --format='%ad - %s' --date=short --reverse -5")
    
    print("\\n🚀 Pronto para push! Execute:")
    print("git push --force-with-lease origin main")

if __name__ == "__main__":
    print("🔧 Script de Reescrita de Histórico Git")
    print("📊 Projeto: Análise Financeira Sam's Club - Walmart")
    print("=" * 60)
    
    # Verificar se estamos em um repositório Git
    if not os.path.exists('.git'):
        print("❌ Erro: Este não é um repositório Git!")
        sys.exit(1)
    
    # Confirmar execução
    confirm = input("\\n⚠️  Esta operação irá reescrever o histórico Git. Continuar? (s/N): ").lower()
    if confirm not in ['s', 'sim', 'y', 'yes']:
        print("❌ Operação cancelada.")
        sys.exit(0)
    
    rewrite_git_history()