# 📋 Experimentos de Agentes de IA Aplicados ao ITIL 4

Este subdiretório contém o ciclo de vida completo da pesquisa empírica: ingestão de dados, engenharia de prompts e agentes, geração de respostas e análise estatística dos resultados.

---

## 🔬 Guia dos Notebooks

| Notebook | Objetivo | Principais Tecnologias | Arquivo de Saída |
| :--- | :--- | :--- | :--- |
| [`ColetaProcessamentoDados.ipynb`](file:///c:/Users/sirja/source/repos/mrjalves/Agentes/AGENTE_ITIL/ColetaProcessamentoDados.ipynb) | Carga dos datasets multilíngues de tickets, filtragem para Português (PT-BR), limpeza de textos e amostragem estratificada. | Pandas, Seaborn, Scikit-Learn | `df_tickets.csv`, `amostra.xlsx` |
| [`itil_chat.ipynb`](file:///c:/Users/sirja/source/repos/mrjalves/Agentes/AGENTE_ITIL/itil_chat.ipynb) | Implementação de Baseline com Google Gemini (Zero-shot com prompt estruturado em modo padrão e streaming). | `google-genai` (`gemini-2.5-flash`) | `resposta_chat.md`, `resposta_chat_stream.md` |
| [`itil_rag.ipynb`](file:///c:/Users/sirja/source/repos/mrjalves/Agentes/AGENTE_ITIL/itil_rag.ipynb) | RAG padrão aumentado com vetorização de trechos do manual do ITIL 4 via ChromaDB. | LangChain, ChromaDB, Google Embeddings | `resposta_agent_rag.md` |
| [`itil_rag_adaptativo.ipynb`](file:///c:/Users/sirja/source/repos/mrjalves/Agentes/AGENTE_ITIL/itil_rag_adaptativo.ipynb) | Agente RAG adaptativo com roteamento condicional (banco vetorial local vs Tavily Web Search) e auto-correção com graders de alucinação. | LangChain, Tavily API, ChromaDB | `resposta_agent_rag_adaptativo.md` |
| [`itil_planejar_executar.ipynb`](file:///c:/Users/sirja/source/repos/mrjalves/Agentes/AGENTE_ITIL/itil_planejar_executar.ipynb) | Agente cognitivo Plan-and-Solve construído sobre LangGraph, decompondo cada ticket em análise, diagnóstico e resolução estruturada em lote. | LangGraph, LangChain, Google GenAI | `resposta_planejar_executar.md` |
| [`itil_planejar_executar_avaliar.ipynb`](file:///c:/Users/sirja/source/repos/mrjalves/Agentes/AGENTE_ITIL/itil_planejar_executar_avaliar.ipynb) | Extensão do Plan-and-Solve com nó avaliador que julga a coerência da resposta e aciona replanejamento caso necessário. | LangGraph, LangChain | `resposta_itil_agent_plan_exec_avaliar.md` |
| [`AnaliseRespostas.ipynb`](file:///c:/Users/sirja/source/repos/mrjalves/Agentes/AGENTE_ITIL/AnaliseRespostas.ipynb) | Parser automatizado de tabelas markdown geradas pelos agentes, consolidação de predições, cálculo de métricas de concordância e atualização do Excel. | Pandas, OpenpyXL, Matplotlib | `analise_resposta.xlsx` |

---

## 📊 Estrutura da Planilha Consolidada (`analise_resposta.xlsx`)

A planilha reúne as saídas de todos os modelos para comparação lado a lado:
- **Aba `analise_resposta`**: Matriz principal onde cada linha representa um ticket da amostra com as práticas principal e auxiliar classificadas por cada agente.
- **Aba `amostra_tickets`**: Metadados originais dos chamados (Ticket ID, assunto, descrição).
- **Aba `respostas_tickets`**: Diagnósticos e textos completos de resolução recomendados pelos agentes.
- **Aba `respostas`**: Registro bruto de tabelas extraídas das saídas em Markdown.

---

## 📁 Pasta `respostas/`

O diretório [`respostas/`](file:///c:/Users/sirja/source/repos/mrjalves/Agentes/AGENTE_ITIL/respostas) armazena o histórico sincronizado das execuções em lote dos agentes:
- `resposta_chat.md`
- `resposta_chat_stream.md`
- `resposta_agent_rag.md`
- `resposta_agent_rag_adaptativo.md`
- `resposta_itil_agent_plan_exec.md`
- `resposta_itil_agent_plan_exec_avaliar.md`

Todas as tabelas geradas seguem o formato:
```markdown
| Ticket Associado | Prática Principal | Prática Auxiliar |
| :--------------- | :---------------- | :--------------- |
| 1                | Incident Management | Knowledge Management |
```

---

## ⚙️ Variáveis de Ambiente

Crie o arquivo `.env` dentro desta pasta com base no template [`.env.example`](file:///c:/Users/sirja/source/repos/mrjalves/Agentes/AGENTE_ITIL/.env.example):
```ini
GEMINI_API_KEY_CHAT=sua_chave_aqui
GEMINI_API_KEY_CHAT_STREAM=sua_chave_aqui
GEMINI_API_KEY_RAG=sua_chave_aqui
GEMINI_API_KEY_RAG_ADAPTATIVO=sua_chave_aqui
GEMINI_API_KEY_PLAN_EXEC=sua_chave_aqui
GEMINI_API_KEY_PLAN_EXEC_AVALIAR=sua_chave_aqui
TAVILY_API_KEY=sua_chave_aqui
```
