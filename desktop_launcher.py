from __future__ import annotations

import os
import socket
import sys
import time
import webbrowser
from pathlib import Path

from streamlit.web import cli as streamlit_cli


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def find_free_port(start: int = 8501, end: int = 8599) -> int:
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise RuntimeError("No free port found for the local Streamlit server.")


def main() -> int:
    root = app_root()
    port = find_free_port()
    os.environ["PYTHONPATH"] = str(root)

    url = f"http://127.0.0.1:{port}"
    time.sleep(2)
    webbrowser.open(url)

    sys.argv = [
        "streamlit",
        "run",
        str(root / "app.py"),
        "--server.address=127.0.0.1",
        f"--server.port={port}",
        "--server.headless=true",
    ]
    return streamlit_cli.main()


if __name__ == "__main__":
    raise SystemExit(main())
