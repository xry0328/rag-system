# RAG Intelligent Customer Service

DDD-style RAG customer service system built with Streamlit, LangGraph, Chroma, and pluggable LLM providers.

## Features

- Knowledge base management: create knowledge bases, upload Markdown files, split text, embed chunks, and persist vectors in Chroma.
- Customer service chat: select multiple knowledge bases, retrieve context through a LangGraph tool step, stream answers, and display tool events.
- Model providers: OpenAI, Ollama, and Xinference through an OpenAI-compatible endpoint. Embedding defaults to OpenAI.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

Set `OPENAI_API_KEY` in `.env` before using OpenAI embeddings.

## Windows App Packaging

Build a folder-based Windows desktop app:

```powershell
.\scripts\build_windows_app.ps1
```

See `APP_PACKAGING.md` for details.
