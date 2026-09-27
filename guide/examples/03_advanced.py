"""Offline ASR stream reducer: this is not the TTS NDJSON wire format."""
from dataclasses import dataclass, field


@dataclass
class Transcript:
    session_id: str | None = None
    partial: str = ""
    utterances: list[str] = field(default_factory=list)
    summary: str | None = None
    finished: bool = False
    failed: bool = False

    def accept(self, event):
        if not isinstance(event, dict):
            raise ValueError("Event must be an object")
        if self.finished:
            raise ValueError("Session is already terminal")
        kind = event.get("type")
        sid = event.get("session_id")
        if kind == "session.started":
            if self.session_id is not None or not isinstance(sid, str) or not sid:
                raise ValueError("Invalid or repeated session start")
            self.session_id = sid
            return
        if self.session_id is None or sid != self.session_id:
            raise ValueError("Missing start or mismatched session")
        if kind == "error":
            self.failed = self.finished = True
            self.partial = ""
            raise RuntimeError("Stream failed; transcript must not be treated as successful")
        if kind == "status":
            return
        if kind not in {"partial", "final"}:
            raise ValueError("Unknown event type")
        value = event.get("text")
        if not isinstance(value, str):
            raise ValueError("Transcript text must be a string")
        if kind == "partial":
            self.partial = value
        elif event.get("final_kind") == "utterance":
            self.utterances.append(value)
            self.partial = ""
        elif event.get("final_kind") == "summary":
            self.summary = value
            self.partial = ""
            self.finished = True
        else:
            raise ValueError("Unknown final kind")

    def text(self):
        if self.failed:
            raise RuntimeError("Failed session has no successful transcript")
        # An empty summary is still authoritative; do not append it to utterances.
        return self.summary if self.summary is not None else " ".join(self.utterances)


def demo():
    state = Transcript()
    for event in [
        {"type": "session.started"},
        {"type": "partial", "text": "Hello"},
        {"type": "final", "final_kind": "utterance", "text": "Hello world."},
        {"type": "final", "final_kind": "summary", "text": "Hello world."},
    ]:
        state.accept({**event, "session_id": "offline-demo"})
    print(state.text())
    print(f"finished={state.finished}; utterances={len(state.utterances)}")


if __name__ == "__main__":
    demo()
