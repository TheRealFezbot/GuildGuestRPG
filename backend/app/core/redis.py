import redis
import json
from uuid import UUID
from app.core.config import settings
from datetime import datetime, timezone

r = redis.from_url(settings.redis_url, decode_responses=True)

def set_stamina(character_id: UUID, stamina: int, updated_at: datetime):
    key = f"stamina:{character_id}"
    value = json.dumps({"stamina": stamina, "updated_at": updated_at.isoformat()})
    r.setex(key, 86400, value)

def get_stamina(character_id: UUID) -> dict | None:
    key = f"stamina:{character_id}"
    data = r.get(key)
    if data is None:
        return None
    return json.loads(data)