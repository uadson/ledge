import os
from pathlib import Path
from google import genai
from google.genai import types
import ollama
from typing import Optional
from ledge.config import load_config

def get_engine_response(
    prompt: str, 
    system_instruction: str, 
    use_local: bool = False, 
    use_pro: bool = False
) -> str:
    config = load_config()
    
    if not use_local:
        # Gemini Engine (New SDK)
        modelo_nome = "gemini-1.5-pro" if use_pro else config.get("gemini_model", "gemini-1.5-flash")
        api_key = config.get("gemini_api_key") or os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada. Use 'ledge init' ou defina no .env.")
            
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=modelo_nome,
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=system_instruction)
        )
        return response.text
    else:
        # Ollama Engine
        full_local_prompt = f"{system_instruction}\n\n{prompt}"
        res = ollama.chat(
            model=config.get("ollama_model", "llama3"), 
            messages=[{'role': 'user', 'content': full_local_prompt}]
        )
        return res['message']['content']
    
def salvar_historico_json(base_path: Path, tarefa: str, resposta: str):
    import json
    from datetime import datetime
    history_file = base_path / ".codex_history.json"
    interacao = {
        "timestamp": datetime.now().isoformat(),
        "tarefa": tarefa,
        "resposta": resposta[:500] + "..." if len(resposta) > 500 else resposta
    }
    historico = []
    if history_file.exists():
        try:
            with open(history_file, "r") as f:
                historico = json.load(f)
        except:
            pass
    
    historico.append(interacao)
    try:
        with open(history_file, "w") as f:
            json.dump(historico[-10:], f, indent=2)
    except:
        pass
