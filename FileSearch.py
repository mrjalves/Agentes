import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carrega variáveis de ambiente a partir do arquivo .env (se existir)
load_dotenv()

# Obtém a chave da API do Gemini via variável de ambiente
CHAVE_API = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY_CHAT")

if not CHAVE_API:
    raise ValueError(
        "Chave de API do Gemini não configurada! "
        "Defina a variável GEMINI_API_KEY no arquivo .env ou nas variáveis de ambiente do sistema."
    )

client = genai.Client(api_key=CHAVE_API)

# Cria um store para indexação do arquivo
store_name = "itil-manual-store"
file_search_store = client.file_search_stores.create(config={'display_name': store_name})

# Faz upload e indexação do manual ITIL
operation = client.file_search_stores.upload_to_file_search_store(
    file='itil_manual.pdf',
    file_search_store_name=file_search_store.name,
    config={
        'display_name': 'itil_manual.pdf',
    }
)

print("Indexando manual ITIL...")
while not operation.done:
    time.sleep(3)
    operation = client.operations.get(operation)

print("Manual indexado com sucesso. Executando consulta...")

# Consulta o modelo com a ferramenta de busca de arquivos
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Quais são as principais práticas de gerenciamento de serviços no ITIL 4 e como elas se dividem?",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[file_search_store.name]
                )
            )
        ]
    )
)

print("\n=== RESPOSTA GERADA ===")
print(response.text)

# Limpeza do store após a consulta
client.file_search_stores.delete(name=file_search_store.name)
print("\nStore temporário removido.")