from loguru import logger
import os
from datetime import datetime

def setup_logger():
    log_dir = "data/logs"
    os.makedirs(log_dir, exist_ok=True)

    log_path = f"{log_dir}/{datetime.now().strftime('%Y-%m-%d')}.log"

    logger.add(
        log_path,
        rotation="1 day",
        retention="30 days",
        encoding="utf-8",
        level="INFO"
    )

    return logger
