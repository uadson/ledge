import os
from pathlib import Path
import google.generativeai as genai
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
        # Gemini Engine
        modelo_nome = "gemini-1.5-pro" if use_pro else config.get("gemini_model", "gemini-1.5-flash")
        api_key = config.get("gemini_api_key") or os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada. Use 'ledge init' ou defina no .env.")
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=modelo_nome,
            system_instruction=system_instruction
        )
        
        response = model.generate_content(prompt)
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
