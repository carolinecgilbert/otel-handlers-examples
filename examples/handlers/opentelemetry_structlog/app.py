from random import randint
from flask import Flask, request
import structlog
import sys
sys.path.insert(0, '../../..')
from handlers.opentelemetry_structlog.src.exporter import StructlogHandler

app = Flask(__name__)


# Create a Structlog logger
structlog.configure(logger_factory=structlog.PrintLoggerFactory())
logger = structlog.get_logger()

# Create an instance of the StructlogHandler
handler = StructlogHandler(service_name="flask-structlog-demo", server_hostname="instance-1", exporter=None)

# Set the logger to use the StructlogHandler
logger.bind(handler=handler)



@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(roll())
    logger.warning("Hello World from Structlog Handler!")
    if player:
        logger.warning("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return result


def roll():
    return randint(1, 6)

