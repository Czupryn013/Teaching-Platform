import logging

from tp_chat.extensions import socket

from flask_socketio import send
from flask import Blueprint, render_template


chat_controller_bp = Blueprint("chat_controller_bp", __name__)

@socket.on("message")
def handle_message(message):
    logging.info(f"Recived message: {message}")
    if message == "User connected.":
        send(message, broadcast=False)
        return
    send(message, broadcast=True)



@chat_controller_bp.route("/chat")
def chat():
    return render_template("chat.html")

