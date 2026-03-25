.PHONY: help install test ask list pull config

help:
	@echo "Ledge: Assistente de IA para Desenvolvedores"
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make install      Instala as dependências e o pacote localmente via uv"
	@echo "  make test         Executa a suíte de testes (pytest)"
	@echo "  make ask          Executa uma tarefa via Gemini (TASK=\"...\")"
	@echo "  make ask-local    Executa uma tarefa via Ollama (TASK=\"...\")"
	@echo "  make list         Lista modelos disponíveis"
	@echo "  make config       Executa a configuração inicial (ledge init)"

install:
	uv pip install -e .

test:
	uv run pytest

config:
	ledge init

ask:
	ledge ask "$(TASK)"

ask-pro:
	ledge ask "$(TASK)" --pro

ask-local:
	ledge ask "$(TASK)" --local

list:
	ledge list

pull:
	ledge pull $(MODEL)
