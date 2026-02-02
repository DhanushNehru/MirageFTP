import logging
import json
import sys
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        # Add extra fields if they exist
        if hasattr(record, "client_ip"):
            log_record["client_ip"] = record.client_ip
        if hasattr(record, "user"):
            log_record["user"] = record.user
        if hasattr(record, "command"):
            log_record["command"] = record.command

        return json.dumps(log_record)

def setup_logger():
    logger = logging.getLogger("MirageFTP")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    return logger

logger = setup_logger()
