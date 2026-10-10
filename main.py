import argparse
import sys
from loguru import logger
from src.utils.logging_config import setup_logging
from src.orchestration.workflow import run_workflow
from src.services.redis_service import redis_client, load_state
from src.output.markdown_writer import write_markdown_report
from src.output.bibtex_writer import write_bibtex_file

def check_redis():
    try:
        redis_client.ping()
        logger.info("Connected to Redis successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        sys.exit(1)

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Multi-Agent Research Assistant")
    parser.add_argument("--topic", required=True, help="Research topic to review")
    args = parser.parse_args()
    
    check_redis()
    
    logger.info(f"Starting workflow for topic: {args.topic}")
    try:
        run_id = run_workflow(args.topic)
        final_state = load_state(run_id)
        
        write_markdown_report(final_state)
        write_bibtex_file(final_state)
        
        logger.info("Workflow completed successfully.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
