from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import wordpress_catalog


class _Response:
    headers = {"Content-Length": "2"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def geturl(self):
        return "https://now0930.pe.kr/wordpress/"

    def read(self, _size=-1):
        return b"ok"


def test_wordpress_request_uses_extended_timeout(monkeypatch):
    observed = {}

    def fake_urlopen(request, timeout):
        observed["url"] = request.full_url
        observed["timeout"] = timeout
        return _Response()

    monkeypatch.setattr(wordpress_catalog, "urlopen", fake_urlopen)
    payload, _headers = wordpress_catalog._request(
        "https://now0930.pe.kr/wordpress/"
    )

    assert payload == b"ok"
    assert observed["timeout"] == 120
