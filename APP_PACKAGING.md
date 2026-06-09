# Windows App Packaging

This project can be packaged as a Windows desktop app with PyInstaller.

The packaged app starts a local Streamlit server on `127.0.0.1`, opens the browser automatically, and stores runtime data beside the executable under `data/`.

## Build

Run from PowerShell:

```powershell
cd G:\code\rag-system
.\scripts\build_windows_app.ps1
```

The executable will be generated at:

```text
dist\RAGCustomerService\RAGCustomerService.exe
```

## Configure

Place a `.env` file beside `RAGCustomerService.exe` before running the app:

```env
OPENAI_API_KEY=your-openai-api-key
DEFAULT_LLM_PROVIDER=openai
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

For Ollama or Xinference, the packaged app can connect to services running on the same machine or reachable network endpoints.

## Notes

- The executable is a folder-based app, not a single-file executable. This is more reliable for Streamlit, Chroma, and LangChain dependencies.
- If Windows Defender scans the app on first launch, startup may take longer.
- Chroma data, uploaded files, and metadata are stored under the app folder's `data/` directory.
