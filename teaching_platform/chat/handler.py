import logging

from teaching_platform.chat.extensions import socket

from flask_socketio import send

@socket.on("message")
def handle_message(message):
    logging.info(f"Recived message: {message}")
    send(message, broadcast=True)