import json
import redis
from loguru import logger
from configs import settings
from src.models.workflow_state import WorkflowState
from src.models.paper import Paper

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

def save_state(run_id: str, state: dict, ttl: int = 3600):
    try:
        state_dict = state.copy()
        if 'papers' in state_dict and state_dict['papers']:
            state_dict['papers'] = [p.dict() if isinstance(p, Paper) else p for p in state_dict['papers']]
        
        redis_client.setex(f"research:{run_id}", ttl, json.dumps(state_dict))
        logger.info(f"Saved state to Redis for run_id {run_id}")
    except Exception as e:
        logger.error(f"Failed to save state to Redis: {e}")

def load_state(run_id: str) -> dict:
    try:
        data = redis_client.get(f"research:{run_id}")
        if data:
            state_dict = json.loads(data)
            if 'papers' in state_dict and state_dict['papers']:
                state_dict['papers'] = [Paper(**p) for p in state_dict['papers']]
            logger.info(f"Loaded state from Redis for run_id {run_id}")
            return state_dict
    except Exception as e:
        logger.error(f"Failed to load state from Redis: {e}")
    return {}

def update_state(run_id: str, state_updates: dict, ttl: int = 3600):
    current = load_state(run_id) or {}
    current.update(state_updates)
    save_state(run_id, current, ttl)
