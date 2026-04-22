import hashlib
import json

def build_request_hash(payload: dict):
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()