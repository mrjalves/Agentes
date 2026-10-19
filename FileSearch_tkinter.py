import os
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carrega variáveis de ambiente de .env se existir
load_dotenv()

# ==========================================
# ETAPA 1: INICIALIZAÇÃO DO CLIENTE & API KEY
# ==========================================
CHAVE_API = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY_CHAT")

root = tk.Tk()
root.withdraw()  # Esconde a janela principal do Tkinter
root.attributes('-topmost', True)  # Força janelas de diálogo a ficarem em primeiro plano

if not CHAVE_API:
    CHAVE_API = simpledialog.askstring(
        "Configuração de API",
        "Variável GEMINI_API_KEY não encontrada no ambiente.\nPor favor, informe sua chave de API do Google Gemini:",
        parent=root
    )

if not CHAVE_API or not CHAVE_API.strip():
    messagebox.showerror("Erro", "Chave de API não informada. O programa será encerrado.")
    sys.exit(1)

client = genai.Client(api_key=CHAVE_API.strip())
print("Iniciando a simulação do File Search Tool...")

# ==========================================
# ETAPA 2: CRIAR O ARMAZENAMENTO (STORE)
# ==========================================
print("\n1. Criando o File Search Store no servidor...")
store = client.file_search_stores.create(
    config={"display_name": "meu-workspace-local"}
)
print(f"   ✓ Store criado com sucesso! (ID interno: {store.name})")

# ==========================================
# ETAPA 3: SELEÇÃO NATIVA DE ARQUIVO
# ==========================================
print("\n2. Aguardando a seleção do arquivo...")

arquivo_local = filedialog.askopenfilename(
    title="Selecione o arquivo para a IA analisar",
    filetypes=[
        ("Documentos suportados", "*.pdf *.txt *.md *.csv"),
        ("Todos os arquivos", "*.*")
    ]
)

# Verifica se o usuário selecionou um arquivo ou cancelou a janela
if not arquivo_local:
    print("   ❌ Nenhuma seleção foi feita. Encerrando o programa.")
    client.file_search_stores.delete(name=store.name)
    sys.exit()

print(f"   ✓ Arquivo selecionado: {arquivo_local}")

# ==========================================
# ETAPA 4: FAZER UPLOAD E INDEXAR O ARQUIVO
# ==========================================
print("\n3. Fazendo upload e indexando o arquivo...")
operacao_upload = client.file_search_stores.upload_to_file_search_store(
    file_search_store_name=store.name,
    file=arquivo_local,
    config={"display_name": os.path.basename(arquivo_local)}
)

print("   Aguardando o processamento do arquivo", end="")
while not operacao_upload.done:
    print(".", end="", flush=True)
    time.sleep(3)
    operacao_upload = client.operations.get(operacao_upload)

print("\n   ✓ Arquivo indexado e pronto para busca semântica!")

# ==========================================
# ETAPA 5: CONSULTAR COM A FERRAMENTA
# ==========================================
pergunta = "Avalie este documento e extraia um resumo das informações mais importantes."
print("\n4. Consultando o modelo...")
print(f"   Sua pergunta: '{pergunta}'")

resposta = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=pergunta,
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[store.name]
                )
            )
        ]
    )
)

# ==========================================
# ETAPA 6: EXIBIR RESULTADOS E CITAÇÕES
# ==========================================
print("\n=== RESPOSTA GERADA ===")
print(resposta.text)
print("=======================\n")

print("=== FONTES UTILIZADAS (Citações) ===")
if resposta.candidates and resposta.candidates[0].grounding_metadata:
    chunks = resposta.candidates[0].grounding_metadata.grounding_chunks
    for i, chunk in enumerate(chunks, 1):
        if hasattr(chunk, 'retrieved_context') and chunk.retrieved_context:
            fonte = chunk.retrieved_context.title
            print(f"[{i}] {fonte}")
else:
    print("Nenhuma citação extraída diretamente.")

# ==========================================
# ETAPA 7: LIMPEZA DOS DADOS
# ==========================================
print("\n5. Iniciando limpeza...")
client.file_search_stores.delete(name=store.name)
print("   ✓ O File Search Store foi deletado. Simulação concluída.")
