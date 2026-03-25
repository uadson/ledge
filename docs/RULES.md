# Regras de Desenvolvimento

## Padrões de Código
- **Idioma**: Docstrings, comentários e logs devem ser em **Português do Brasil (pt-br)**.
- **Estilo**: Seguir PEP-8 para Python.
- **Tipagem**: Uso obrigatório de `typing` hints em novas funções.

## Segurança
- **Segredos**: Nunca versionar o arquivo `.env`. Usar o `.env.example` como template.
- **API Keys**: Validar chaves antes de chamadas custosas.

## Fluxo de Trabalho
- **Commits**: Seguir o padrão de Conventional Commits (ex: `feat:`, `fix:`, `docs:`).
- **Testes**: Todo novo comando na CLI deve vir acompanhado de uma validação manual documentada ou teste unitário.
