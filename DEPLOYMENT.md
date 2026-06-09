# Deployment

This project can be deployed from GitHub with Streamlit Community Cloud or any Docker-compatible platform.

## Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open Streamlit Community Cloud and create a new app from the repository.
3. Set the main file path to `app.py`.
4. Add secrets or environment variables:

```toml
OPENAI_API_KEY = "your-openai-api-key"
DEFAULT_LLM_PROVIDER = "openai"
OPENAI_CHAT_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
```

For Ollama or Xinference, use externally reachable endpoints. A local `localhost` endpoint will not work from Streamlit Cloud.

## Docker

```bash
docker build -t rag-customer-service .
docker run --rm -p 8501:8501 --env-file .env rag-customer-service
```

Then open `http://localhost:8501`.

## Data Persistence

The app writes uploaded files, Chroma data, and metadata under `data/`. On ephemeral hosting, these files may disappear when the app restarts. For production, mount `data/` as a persistent volume or replace the local metadata store with a managed database.
