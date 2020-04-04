import logging
import os

from mongolog.handlers import MongoHandler


# Add API logger instance
log = logging.getLogger("api_log")
log.setLevel(logging.INFO)
log.addHandler(
    MongoHandler.to(
        collection=os.getenv("API_LOG_COLLECTION", "request"),
        db=os.getenv("API_LOG_DB", "api_log"),
        host=os.getenv("API_LOG_HOST", "localhost"),
        port=os.getenv("API_LOG_PORT", None),
        username=os.getenv("API_LOG_USERNAME", None),
        password=os.getenv("API_LOG_PASSWORD", None)
    )
)
