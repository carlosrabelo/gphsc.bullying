MAKEFLAGS += --no-print-directory

.DEFAULT_GOAL := ajuda

.PHONY: ajuda atualizar configurar iniciar limpar-dados parar

ajuda: ## Mostra os alvos disponíveis
	@echo "bullying.gphsc - Alvos disponíveis"
	@echo ""
	@grep -hE '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*## "} {printf "  %-15s %s\n", $$1, $$2}'

configurar: ## Cria .venv e instala dependências
	@./configurar.sh

iniciar: ## Inicia o Jupyter Notebook com mascaramento.ipynb
	@./iniciar.sh

parar: ## Para o Jupyter Notebook
	@./parar.sh

limpar-dados: ## Formata e padroniza dados/original.csv (local)
	@./.venv/bin/python limpar-dados.py

atualizar: ## Copia o CSV mascarado para o projeto irmão
	@./atualizar.sh
