"""Read-only speech discovery; offline fixture unless --live is supplied."""
import argparse
import json
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, build_opener

PROTOCOL = "voicestudio.speech.v1"
FIXTURE = {
    "schema": "voicestudio.speech-capabilities",
    "protocol": PROTOCOL,
    "endpoints": {
        "batch_transcription": {"path": "/v1/audio/transcriptions", "transport": "http"},
        "streaming_transcription": {
            "path": "/v1/audio/transcriptions/stream", "transport": "websocket"
        },
        "mcp_stdio": {"path": "python -m backend.mcp_shim", "transport": "mcp-stdio"},
    },
}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Redirects are not allowed in this local-only example")


def local_base(base):
    url = urlsplit(base)
    if (url.scheme != "http" or url.hostname not in {"127.0.0.1", "::1"}
            or url.username or url.password or url.query or url.fragment
            or url.path not in {"", "/"}):
        raise ValueError("Use an HTTP loopback IP origin, without credentials or a path")
    if url.port is not None and not 0 < url.port <= 65535:
        raise ValueError("Invalid port")
    return base.rstrip("/")


def discover(base):
    target = local_base(base) + "/.well-known/voicestudio-speech"
    opener = build_opener(ProxyHandler({}), NoRedirect())
    with opener.open(target, timeout=5) as response:
        raw = response.read(256 * 1024 + 1)
    if len(raw) > 256 * 1024:
        raise ValueError("Discovery response exceeds the example's size limit")
    return json.loads(raw)


def summarize(document):
    if not isinstance(document, dict) or document.get("protocol") != PROTOCOL:
        raise ValueError("Unsupported speech protocol")
    endpoints = document.get("endpoints")
    if not isinstance(endpoints, dict) or not endpoints:
        raise ValueError("Missing endpoints")
    rows = []
    for name, endpoint in sorted(endpoints.items()):
        if not isinstance(endpoint, dict):
            raise ValueError("Endpoint must be an object")
        path, transport = endpoint.get("path"), endpoint.get("transport")
        if not isinstance(path, str) or not path:
            raise ValueError("Endpoint path must be a nonempty string")
        if transport not in {"http", "websocket", "mcp-streamable-http", "mcp-stdio"}:
            raise ValueError("Unknown transport")
        # Display the contract only: never execute stdio commands or follow URLs.
        rows.append(f"{name}: {transport} {path}")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", metavar="LOOPBACK_ORIGIN")
    args = parser.parse_args()
    try:
        document = discover(args.live) if args.live else FIXTURE
        print("Mode: " + ("live read-only" if args.live else "offline teaching fixture"))
        print("\n".join(summarize(document)))
    except (OSError, URLError, ValueError) as exc:
        parser.exit(1, f"Discovery failed: {exc}\n")


if __name__ == "__main__":
    main()
