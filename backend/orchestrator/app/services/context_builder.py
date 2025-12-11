from typing import Dict, Any, Optional
from app.schemas.query_request import QueryRequest
import os, sqlite3, json
from datetime import datetime, timezone


class ContextBuilder:
    def __init__(self, prompt_sqlite_path: Optional[str] = None):
        self.prompt_sqlite_path = prompt_sqlite_path or os.getenv("PROMPT_SQLITE_PATH", None)

    def _now_iso(self):
        return datetime.now(timezone.utc).isoformat()

    def build(self, req: QueryRequest) -> Dict[str, Any]:
        base = {
            "user_id": req.user_id,
            "session_id": req.session_id,
            "timestamp": self._now_iso(),
            "query_text": req.text,
            "features": req.features or {},
        }
        if req.memory:
            base["memory_snippet"] = req.memory

        # optional read-only prompt index sample
        if self.prompt_sqlite_path:
            try:
                conn = sqlite3.connect(self.prompt_sqlite_path, uri=True, check_same_thread=False)
                cur = conn.cursor()
                cur.execute("SELECT prompt_id, version, metadata FROM prompts_index LIMIT 3")
                rows = cur.fetchall()
                sample = []
                for pid, ver, meta in rows:
                    try:
                        meta_parsed = json.loads(meta) if meta else {}
                    except Exception:
                        meta_parsed = {}
                    sample.append({"prompt_id": pid, "version": ver, "meta": meta_parsed})
                base["prompt_index_sample"] = sample
                conn.close()
            except Exception:
                pass

        return base
