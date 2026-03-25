import json
import os
from pathlib import Path
from ledge.config import load_config, save_config, CONFIG_FILE, CONFIG_DIR

def test_load_config_default(tmp_path, mocker):
    # Mock CONFIG_FILE to a temp path
    mocker.patch("ledge.config.CONFIG_FILE", tmp_path / "config.json")
    mocker.patch("ledge.config.CONFIG_DIR", tmp_path)
    
    config = load_config()
    assert config["gemini_model"] == "gemini-1.5-flash"
    assert config["ollama_model"] == "llama3"

def test_save_and_load_config(tmp_path, mocker):
    mock_file = tmp_path / "config.json"
    mocker.patch("ledge.config.CONFIG_FILE", mock_file)
    mocker.patch("ledge.config.CONFIG_DIR", tmp_path)
    
    new_config = {
        "gemini_api_key": "test_key",
        "gemini_model": "test-model",
        "ollama_host": "http://test:11434",
        "ollama_model": "test-ollama"
    }
    
    save_config(new_config)
    assert mock_file.exists()
    
    loaded = load_config()
    assert loaded["gemini_api_key"] == "test_key"
    assert loaded["gemini_model"] == "test-model"
