"""Entry point for this repo: starts the roadmap wording editor.

    python3 main.py            # same as: python3 wording_server.py
    python3 main.py --help     # options (port, --no-browser, --export-md)

Standard library only; see wording_server.py and CLAUDE.md for details.
"""
from wording_server import main

if __name__ == "__main__":
    main()
