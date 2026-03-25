# Arquitetura do Projeto

## Stack Tecnológica
- **Linguagem**: Python 3.12+
- **CLI Framework**: [Typer](https://typer.tiangolo.com/)
- **IA SDKs**: 
  - `google-generativeai` (Gemini)
  - `ollama` (Local LLMs)
- **Infraestrutura**: 
  - Docker & Docker Compose
  - DevContainers (VSCode)

## Fluxo de Dados
1. **Input**: O usuário fornece uma tarefa via `shell.py ask`.
2. **Contextualização**: O script lê `/docs/*.md` (Diretrizes) e `/src/**/*.py` (Código).
3. **Prompt Building**: Montagem de um "Super-Prompt" consolidado.
4. **Processamento**: Envio para a API selecionada (Cloud ou Local).
5. **Output**: A resposta da IA é exibida no terminal.

## Padrões de Design
- **Single Source of Truth**: As diretrizes em `/docs` mandam no comportamento da IA.
- **Portabilidade**: Tudo deve rodar dentro do container para garantir paridade entre ambientes.
