from loguru import logger as loguru_logger
import sys
sys.path.insert(0, '../../..')
from handlers.opentelemetry_loguru.src.exporter import LoguruHandler

# Create an instance of LoguruHandler
loguru_handler = LoguruHandler()

# Add LoguruHandler to Loguru logger
loguru_logger.add(loguru_handler.sink)

# Now you can use loguru_logger for logging in your application
loguru_logger.info("This is an info message")
loguru_logger.warning("This is a warning message")
loguru_logger.error("This is an error message")
