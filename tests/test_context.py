import pytest
from pathlib import Path
from ledge.core.context import carregar_blueprint, mapear_codigo_fonte

def test_carregar_blueprint_missing_docs(tmp_path):
    blueprint = carregar_blueprint(tmp_path)
    assert "Pasta /docs não encontrada" in blueprint

def test_carregar_blueprint_with_files(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    project_md = docs_dir / "PROJECT.md"
    project_md.write_text("Test Project Content")
    
    blueprint = carregar_blueprint(tmp_path)
    assert "-- PROJECT.md --" in blueprint
    assert "Test Project Content" in blueprint

def test_mapear_codigo_fonte_no_src(tmp_path):
    contexto = mapear_codigo_fonte(tmp_path)
    assert "Diretório /src não encontrado" in contexto

def test_mapear_codigo_fonte_with_files(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    main_py = src_dir / "main.py"
    main_py.write_text("print('hello')")
    
    # Nested file
    sub_dir = src_dir / "utils"
    sub_dir.mkdir()
    utils_py = sub_dir / "helper.py"
    utils_py.write_text("# helper")
    
    contexto = mapear_codigo_fonte(tmp_path)
    assert "--- ARQUIVO: src/main.py ---" in contexto
    assert "print('hello')" in contexto
    assert "--- ARQUIVO: src/utils/helper.py ---" in contexto
    assert "# helper" in contexto
