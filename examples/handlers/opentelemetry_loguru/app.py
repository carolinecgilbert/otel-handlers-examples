from random import randint
from flask import Flask, request
from loguru import logger
import sys
sys.path.insert(0, '../../..')
from handlers.opentelemetry_loguru.src.exporter import LoguruHandler

app = Flask(__name__)


# Replace the standard logging configuration with Loguru
loguru_handler = LoguruHandler()  # Create an instance of the LoguruHandler
logger.remove()  # Remove the default logger
logger.add(loguru_handler.sink)  # Add  LoguruHandler to the logger

@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(roll())
    if player:
        logger.warning("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return result


def roll():
    return randint(1, 6)

