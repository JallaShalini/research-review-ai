import os
import requests
import redis
from configs import settings

def check_connections():
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        r.ping()
        print("Redis connection SUCCESS")
    except Exception as e:
        print(f"Redis connection FAILED: {e}")
        
    try:
        res = requests.get(settings.OLLAMA_BASE_URL)
        print("Ollama connection SUCCESS")
    except Exception as e:
        print(f"Ollama connection FAILED: {e}")

if __name__ == "__main__":
    check_connections()
