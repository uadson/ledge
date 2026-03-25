import os
import typer
import json
from pathlib import Path
from ledge.config import save_config, load_config
from ledge.core.context import carregar_blueprint, mapear_codigo_fonte
from ledge.core.engine import get_engine_response, salvar_historico_json
import ollama

app = typer.Typer(
    help="🚀 Ledge: Assistente Codex Global",
    rich_markup_mode="rich"
)

@app.command()
def init():
    """Configura as credenciais globais do Ledge"""
    typer.secho("🔧 Configuração Inicial do Ledge", fg=typer.colors.MAGENTA, bold=True)
    
    config = load_config()
    
    api_key = typer.prompt("Gemini API Key", default=config.get("gemini_api_key", ""), hide_input=True)
    model = typer.prompt("Modelo Gemini Padrão", default=config.get("gemini_model", "gemini-1.5-flash"))
    
    config["gemini_api_key"] = api_key
    config["gemini_model"] = model
    
    save_config(config)
    typer.secho("✅ Configuração salva com sucesso em ~/.ledge/config.json", fg=typer.colors.GREEN)

@app.command()
def ask(
    tarefa: str = typer.Argument(..., help="Descreva o que deseja codar ou analisar"),
    path: Path = typer.Option(Path("."), "--path", "-p", help="Caminho do projeto (workspace)"),
    local: bool = typer.Option(False, "--local", "-l", help="Usa Ollama em vez do Gemini"),
    pro: bool = typer.Option(False, "--pro", help="Usa Gemini 1.5 Pro")
):
    """Analisa um workspace usando IA com base no contexto de diretrizes e código"""
    base_path = path.resolve()
    if not base_path.exists():
        typer.secho(f"❌ Erro: O caminho {base_path} não existe.", fg=typer.colors.RED)
        raise typer.Exit(1)

    blueprint = carregar_blueprint(base_path)
    codigo = mapear_codigo_fonte(base_path)
    
    system_prompt = (
        "Você é o Ledge (anteriormente Codex), um Arquiteto e Engenheiro de Software Sênior. "
        f"Workspace atual: {base_path}\n"
        "Use o [BLUEPRINT] e o [CÓDIGO FONTE] para responder tecnicamente.\n\n"
        f"{blueprint}"
    )

    try:
        resposta = get_engine_response(codigo + f"\n\n[SOLICITAÇÃO]: {tarefa}", system_prompt, local, pro)
        typer.echo(f"\n{resposta}")
        salvar_historico_json(base_path, tarefa, resposta)
    except Exception as e:
        typer.secho(f"\n❌ ERRO: {str(e)}", fg=typer.colors.RED, bold=True)

@app.command()
def pull(model_name: str = typer.Argument(..., help="Nome do modelo Ollama para baixar")):
    """Baixa um modelo do Ollama"""
    typer.secho(f"📥 Baixando modelo: {model_name}...", fg=typer.colors.CYAN)
    try:
        ollama.pull(model_name)
        typer.secho(f"✅ Modelo {model_name} baixado com sucesso!", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"❌ Erro ao baixar modelo: {e}", fg=typer.colors.RED)

@app.command(name="list")
def list_models():
    """Lista modelos disponíveis (Ollama e Gemini)"""
    typer.secho("🤖 Modelos Disponíveis", fg=typer.colors.MAGENTA, bold=True)
    
    # Ollama
    try:
        models = ollama.list()
        typer.secho("\n🏠 Ollama (Locais):", fg=typer.colors.GREEN, bold=True)
        for m in models['models']:
            typer.echo(f"  - {m['name']}")
    except:
        typer.secho("\n🏠 Ollama: Não disponível ou não instalado.", fg=typer.colors.YELLOW)

    # Gemini (Configurado)
    config = load_config()
    typer.secho("\n🚀 Gemini (Nuvem):", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"  - {config.get('gemini_model')} (Padrão)")
    typer.echo("  - gemini-1.5-pro")
    typer.echo("  - gemini-1.5-flash")

@app.command()
def history(
    path: Path = typer.Option(Path("."), "--path", "-p", help="Caminho do projeto (workspace)")
):
    """Mostra o histórico de interações do workspace"""
    base_path = path.resolve()
    history_file = base_path / ".codex_history.json"
    
    if not history_file.exists():
        typer.echo("Nenhum histórico encontrado neste workspace.")
        return
    
    with open(history_file, "r") as f:
        historico = json.load(f)
        for item in historico:
            typer.secho(f"\n🗓  {item['timestamp']}", fg=typer.colors.YELLOW)
            typer.echo(f"❓ {item['tarefa']}")
            typer.echo("-" * 20)

if __name__ == "__main__":
    app()
