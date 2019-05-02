# Bullying GPHSC

Projeto educacional para anonimizar dados de questionário escolar sobre bullying no contexto da pesquisa GPHSC, permitindo estudar as respostas sem expor estudantes.

## Destaques

- Percorre um fluxo real de anonimização de pesquisa em um notebook Jupyter
- Remove ou renomeia campos que poderiam identificar um estudante
- Mantém apenas as variáveis úteis para analisar padrões de bullying
- Exporta um CSV limpo pronto para uso em aulas e pesquisas
- Usa nomes de colunas em português após o mascaramento, facilitando a discussão em sala
- Inclui um script pequeno para copiar o arquivo anonimizado para um projeto irmão

## Visão Geral

Este repositório ensina uma etapa prática de privacidade que costuma vir antes da análise: o **mascaramento**. A planilha original vem de um questionário escolar sobre bullying. Algumas colunas são úteis para pesquisa (faixa etária, ano escolar, tipo de agressão). Outras são arriscadas de compartilhar (códigos de acesso, relatos em texto livre, bairro).

O notebook `mascaramento.ipynb` carrega o arquivo original, inspeciona cada coluna, remove ou renomeia campos sensíveis e grava um conjunto de dados mais seguro. Os alunos podem seguir as células de cima para baixo e entender por que cada decisão protege os respondentes.

## Pré-requisitos

- **Python 3** — usado para executar o notebook
- **pip** — para instalar os pacotes listados em `requirements.txt`
- **Jupyter** — instalado pelas dependências do projeto
- **dados/original.csv** — arquivo local com as respostas (não vai para o GitHub)

## Instalação

```bash
git clone https://github.com/carlosrabelo/bullying.gphsc.git
cd bullying.gphsc
make configurar
```

Copie o CSV completo para `dados/original.csv` (o repositório só versiona o cabeçalho em `dados/original.csv.exemplo`).

## Início Rápido

```bash
make limpar-dados   # formata o CSV local (opcional, mas recomendado)
make iniciar          # abre o Jupyter com mascaramento.ipynb
make parar           # encerra o Jupyter
```

Execute todas as células em ordem. No final, o notebook grava `dados/bullying.csv`.

## Uso

### 1. Entenda a entrada

As respostas originais ficam **apenas na sua máquina**:

```
dados/original.csv
```

O esquema (só cabeçalho) está em `dados/original.csv.exemplo`. Antes de analisar, rode `make limpar-dados` para padronizar espaços, idades e categorias sem apagar respostas.

Abra o notebook e execute as primeiras células para carregar o arquivo e listar os nomes das colunas. Pergunte-se: quais campos poderiam identificar uma pessoa, mesmo de forma indireta?

### 2. Siga os passos de mascaramento

No `mascaramento.ipynb` você vai:

1. Importar o pandas
2. Carregar `dados/original.csv`
3. Inspecionar valores das colunas com `value_counts`
4. Remover ou manter campos conforme a necessidade de privacidade
5. Renomear as colunas mantidas para nomes curtos em português (`local`, `idade`, `questao_01`, ...)
6. Exportar apenas as colunas seguras para `dados/bullying.csv`

### 3. Enviar o arquivo anonimizado para outro projeto

Se você também mantém um repositório irmão que consome o dataset limpo:

```bash
make atualizar    # Copia o CSV mascarado para o projeto irmão
./atualizar.sh
```

Isso copia `dados/bullying.csv` para `../bullying/csv/original.csv`.

## Estrutura do Projeto

```
dados/original.csv.exemplo  # Cabeçalho do esquema (versionado)
dados/original.csv          # Respostas completas (local, fora do Git)
mascaramento.ipynb               # Notebook guiado de anonimização
atualizar.sh                 # Copia o CSV mascarado para um projeto irmão
requirements.txt            # Dependências Python do notebook
Makefile                    # Atalhos make configurar / iniciar / parar / limpar-dados / atualizar
configurar.sh iniciar.sh parar.sh   # Scripts usados pelo Makefile
limpar-dados.py          # Formatação local de dados/original.csv
```

## Desenvolvimento

```bash
make configurar         # Cria .venv e instala dependências
make limpar-dados  # Formata e padroniza dados/original.csv
make iniciar         # Inicia o Jupyter Notebook com mascaramento.ipynb
make parar          # Para o Jupyter Notebook
make ajuda          # Lista os alvos disponíveis
make atualizar    # Copia o CSV mascarado para o projeto irmão
./atualizar.sh
```

O ambiente local fica em `.venv/` (ignorado pelo Git). Os arquivos `dados/original.csv`, `dados/original.csv.bak` e `dados/bullying.csv` também ficam de fora do Git.

## Licença

Ainda não há arquivo de licença neste repositório. Inclua uma antes de redistribuir o material fora da sua turma ou grupo de pesquisa.
