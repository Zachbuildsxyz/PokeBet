import json
import uuid
import datetime
from pathlib import Path


class EventLogger:
    """
    Structured JSON event logger.
    All execution decisions pass through here.
    """

    def __init__(self, log_dir="logs"):
        self.run_id = str(uuid.uuid4())
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.log_file = self.log_dir / f"{self.run_id}.jsonl"

    def _timestamp(self):
        return datetime.datetime.utcnow().isoformat()

    def log_event(self, event_type, reason=None, symbol=None, risk=None, meta=None):
        event = {
            "ts": self._timestamp(),
            "run_id": self.run_id,
            "event": event_type,
            "reason": reason,
            "symbol": symbol,
            "risk": risk,
            "meta": meta or {},
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")

        return event
