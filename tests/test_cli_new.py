import pytest
from typer.testing import CliRunner
from ledge.main import app

runner = CliRunner()

def test_pull_command_fails_without_args():
    result = runner.invoke(app, ["pull"])
    # Should fail if model is required, or show help
    assert result.exit_code != 0

def test_list_command_exists():
    result = runner.invoke(app, ["list"])
    # This might fail now because the command doesn't exist yet (TDD!)
    assert result.exit_code == 0
    assert "Modelos" in result.stdout or "Ollama" in result.stdout
