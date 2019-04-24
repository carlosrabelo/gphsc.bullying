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

## Instalação

```bash
git clone https://github.com/carlosrabelo/bullying.gphsc.git
cd bullying.gphsc
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Início Rápido

```bash
source .venv/bin/activate
jupyter notebook mascaramento.ipynb
```

Execute todas as células em ordem. No final, o notebook grava `dados/bullying.csv`.

## Uso

### 1. Entenda a entrada

As respostas originais estão em:

```
dados/original.csv
```

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
dados/              # Dados da pesquisa (entrada original; saída gerada fica fora do Git)
mascaramento.ipynb       # Notebook guiado de anonimização
atualizar.sh         # Copia o CSV mascarado para um projeto irmão
requirements.txt    # Dependências Python do notebook
```

## Desenvolvimento

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook mascaramento.ipynb   # Editar e reexecutar o fluxo de mascaramento
./atualizar.sh                    # Atualizar a cópia no projeto destino
```

O arquivo gerado `dados/bullying.csv` fica de fora do Git de propósito: regenere-o a partir do notebook sempre que as regras de mascaramento mudarem.

## Licença

Ainda não há arquivo de licença neste repositório. Inclua uma antes de redistribuir o material fora da sua turma ou grupo de pesquisa.
