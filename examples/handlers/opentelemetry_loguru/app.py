from random import randint
from flask import Flask, request
from loguru import logger as loguru_logger
import sys
sys.path.insert(0, '../../..')
from handlers.opentelemetry_loguru.src.exporter import LoguruHandler

app = Flask(__name__)


# Replace the standard logging configuration with Loguru
loguru_handler = LoguruHandler()  # Create an instance of the LoguruHandler
loguru_logger.remove()  # Remove the default logger
loguru_logger.add(loguru_handler.sink)  # Add  LoguruHandler to the logger

@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(roll())
    if player:
        loguru_logger.info("Player is rolling the dice: num")
    else:
        loguru_logger.info("Anonymous player is rolling the dice: num")
    return result


def roll():
    return randint(1, 6)

