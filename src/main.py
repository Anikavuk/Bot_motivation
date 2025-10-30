from src.app.core.config_run import run_app
from src.app.core.logger import get_logger


logger = get_logger(name=__name__)


if __name__ == "__main__":
    logger.info("Starting...")
    run_app()
    logger.info("Stopping...")
# if __name__ == "__main__":
#     logger.info("Starting...")
#     uvicorn.run(
#         web_app,
#         host="0.0.0.0",
#         port=8000,
#         log_level="info",
#     )
#     logger.info("Stopping...")
