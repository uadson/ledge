from pathlib import Path

def carregar_blueprint(base_path: Path) -> str:
    """Lê os arquivos de definição mestre do projeto (.md)"""
    docs_dir = base_path / "docs"
    arquivos_mestre = ["PROJECT.md", "ARCHITECTURE.md", "RULES.md", "SKILL.md"]
    blueprint = f"### [DIRETRIZES MESTRE DO PROJETO EM: {base_path}] ###\n"
    
    if not docs_dir.exists():
        return blueprint + "(Pasta /docs não encontrada neste workspace)\n"

    for arq in arquivos_mestre:
        caminho = docs_dir / arq
        if caminho.exists():
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    blueprint += f"\n-- {arq} --\n{f.read()}\n"
            except Exception as e:
                blueprint += f"\n-- {arq} -- (Erro ao ler arquivo: {e})\n"
        else:
            blueprint += f"\n-- {arq} -- (Arquivo não definido ainda)\n"
    return blueprint

def mapear_codigo_fonte(base_path: Path) -> str:
    """Escaneia recursivamente a pasta /src em busca de arquivos .py"""
    contexto = "\n### [ESTADO ATUAL DO CÓDIGO FONTE (src/)] ###\n"
    src_dir = base_path / "src"
    
    if not src_dir.exists():
        return contexto + "Diretório /src não encontrado neste workspace."

    python_files = list(src_dir.rglob("*.py"))
    if not python_files:
        return contexto + "Nenhum arquivo .py encontrado em /src."

    for path in python_files:
        if "__pycache__" in str(path) or ".git" in str(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                relative_path = path.relative_to(base_path)
                contexto += f"\n--- ARQUIVO: {relative_path} ---\n{f.read()}\n"
        except Exception as e:
            contexto += f"\n--- ARQUIVO: {path} --- (Falha na leitura: {e})\n"
    return contexto
