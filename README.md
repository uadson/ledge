# 🚀 Ledge: Assistente de Desenvolvimento Assistido por IA

O **Ledge** é um assistente de IA projetado para arquitetos e engenheiros de software. Ele lê diretrizes mestres (Blueprints) em arquivos Markdown e analisa o código fonte do projeto para fornecer sugestões, implementações e análises contextuais de alta qualidade.

## ✨ Funcionalidades

- 🧠 **Context Awareness**: Lê arquivos em `/docs` (PROJECT.md, ARCHITECTURE.md, etc.) para entender as regras do projeto.
- 🐍 **Source Mapping**: Analisa recursivamente o diretório `/src` para contextualizar as respostas.
- 🤖 **Multi-Engine**: Suporte nativo ao **Google Gemini** (Nuvem) e **Ollama** (Local).
- 📥 **Gerenciamento de Modelos**: Baixe (`pull`) e liste (`list`) modelos diretamente via CLI.
- 📦 **Instalação Global**: Pode ser instalado via `uv` ou `pip` para uso em qualquer diretório.
- 🐳 **Containerizado**: Pronto para rodar via Docker para um ambiente isolado.

## 🚀 Instalação

### Pré-requisitos
- Python 3.12 ou superior
- [uv](https://github.com/astral-sh/uv) (recomendado) ou pip

### Instalação Local
```bash
# Clone o repositório
git clone https://github.com/uadson/ledge.git
cd ledge

# Instale em modo editável
uv pip install -e .
# ou
pip install -e .
```

### Configuração Inicial
```bash
ledge init
```
Forneça sua **Gemini API Key** e escolha o modelo padrão.

## 🛠️ Uso

### Consultar o Assistente
```bash
# Usando o modelo padrão (Gemini)
ledge ask "Crie um novo módulo de autenticação"

# Usando Ollama local
ledge ask "Explique o código atual" --local

# Usando Gemini 1.5 Pro
ledge ask "Analise a performance deste módulo" --pro
```

### Gerenciamento de Modelos
```bash
# Listar modelos locais e sugeridos
ledge list

# Baixar um novo modelo para o Ollama
ledge pull llama3
```

## 🐳 Docker

Para rodar o Ledge e o Ollama via container:

```bash
cd infra
docker-compose up -d

# Executar comandos através do container
docker-compose run app ask "Analise o projeto"
```

## 📦 Publicação (PyPI)

Para publicar uma nova versão do **Ledge** no PyPI usando o `uv`:

1.  **Atualize a versão**: Altere o campo `version` em `pyproject.toml`.
2.  **Gere o Build**:
    ```bash
    uv build
    ```
3.  **Publique**:
    ```bash
    uv publish
    ```
    *Nota: Você precisará de um Token de API do PyPI configurado.*

## 🤝 Colaboração

Contribuições são muito bem-vindas! Siga os passos abaixo:

1. **Fork** o projeto.
2. Crie uma **Branch** para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Siga a metodologia **TDD**: escreva testes para sua nova funcionalidade antes da implementação.
4. Execute os testes existentes:
   ```bash
   uv run pytest
   ```
5. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`).
6. **Push** para a branch (`git push origin feature/nova-funcionalidade`).
7. Abra um **Pull Request**.

### Padrões de Código
- Use `typer` para novos comandos CLI.
- Documente novas funções e mantenha a consistência com o `src/ledge`.
- Mantenha os arquivos Docker organizados em `infra/`.

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

---
Desenvolvido por [Uadson](https://github.com/uadson)
