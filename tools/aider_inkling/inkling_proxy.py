import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "http://127.0.0.1:11434"
MODEL = "inkling-2-mini-aider"

ROLES = {
    "system": "system",
    "user": "user",
    "assistant": "model",
}


class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def upstream(self, path, data=None):
        body = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(
            UPSTREAM + path,
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=3600) as res:
            return json.load(res)

    def do_GET(self):
        try:
            self.send_json(self.upstream(self.path))
        except Exception as exc:
            self.send_json({"error": str(exc)}, 502)

    def do_POST(self):
        try:
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length))

            if self.path != "/api/chat":
                self.send_json(self.upstream(self.path, data))
                return

            if data.get("stream") or data.get("tools"):
                self.send_json(
                    {"error": "Only non-streaming text chat is supported"},
                    400,
                )
                return

            if data.get("model", "").removesuffix(":latest") != MODEL:
                self.send_json({"error": "Unsupported model"}, 400)
                return

            prompt = (
                "<|message_system|><|content_text|>"
                "Thinking effort level: 0<|end_message|>"
            )

            for msg in data["messages"]:
                role = ROLES[msg["role"]]
                content = msg["content"]
                if not isinstance(content, str):
                    raise ValueError("Text messages only")
                prompt += (
                    f"<|message_{role}|><|content_text|>"
                    f"{content}<|end_message|>"
                )

            prompt += "<|message_model|><|content_text|>"

            result = self.upstream("/api/generate", {
                "model": MODEL,
                "prompt": prompt,
                "raw": True,
                "stream": False,
                "keep_alive": "10m",
                "options": {
                    "num_ctx": 65536,
                    "num_batch": 128,
                    "num_predict": 8192,
                    "temperature": 0.2,
                },
            })

            if "error" in result:
                self.send_json(result, 502)
                return

            result["message"] = {
                "role": "assistant",
                "content": result.pop("response", ""),
            }

            print(
                "Input:", result.get("prompt_eval_count"),
                "Output:", result.get("eval_count"),
                "Reason:", result.get("done_reason"),
                flush=True,
            )

            self.send_json(result)

        except Exception as exc:
            self.send_json({"error": str(exc)}, 502)


ThreadingHTTPServer(
    ("127.0.0.1", 11435), Handler
).serve_forever()
