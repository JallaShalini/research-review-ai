from loguru import logger
import sys
import os

def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    
    os.makedirs("output", exist_ok=True)
    logger.add(
        "output/agent_run.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO"
    )
