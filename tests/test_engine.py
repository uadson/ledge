import pytest
from ledge.core.engine import get_engine_response, salvar_historico_json

def test_get_engine_response_gemini(mocker):
    # Mock load_config
    mocker.patch("ledge.core.engine.load_config", return_value={
        "gemini_api_key": "fake_key",
        "gemini_model": "gemini-1.5-flash"
    })
    
    # Mock genai Client
    mock_genai = mocker.patch("ledge.core.engine.genai")
    mock_client = mock_genai.Client.return_value
    mock_response = mock_client.models.generate_content.return_value
    mock_response.text = "Gemini Response"
    
    response = get_engine_response("prompt", "system", use_local=False)
    
    assert response == "Gemini Response"
    mock_genai.Client.assert_called_with(api_key="fake_key")
    mock_client.models.generate_content.assert_called()

def test_get_engine_response_ollama(mocker):
    mocker.patch("ledge.core.engine.load_config", return_value={
        "ollama_model": "llama3"
    })
    
    mock_ollama = mocker.patch("ledge.core.engine.ollama")
    mock_ollama.chat.return_value = {
        "message": {"content": "Ollama Response"}
    }
    
    response = get_engine_response("prompt", "system", use_local=True)
    
    assert response == "Ollama Response"
    mock_ollama.chat.assert_called()
    call_args = mock_ollama.chat.call_args[1]
    assert call_args["model"] == "llama3"

def test_salvar_historico(tmp_path):
    # Test history saving
    salvar_historico_json(tmp_path, "tarefa", "resposta")
    history_file = tmp_path / ".codex_history.json"
    assert history_file.exists()
