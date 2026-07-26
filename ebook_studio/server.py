"""Dev entrypoint: `python3 server.py` and open http://127.0.0.1:8000"""

import os
from wsgiref.simple_server import make_server

from app.wsgi_app import app

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    print(f"properebooks.com ebook studio running on http://{host}:{port}")
    make_server(host, port, app).serve_forever()
