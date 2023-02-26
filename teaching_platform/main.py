import logging
import os

import yaml
import jsonpickle
from dotenv import load_dotenv
from flask import Flask

from teaching_platform.models.users.controller import user_controller_bp
from teaching_platform.models.lessons.controller import lesson_controller_bp
from teaching_platform.models.projects.controller import project_controller_bp
from teaching_platform.chat.controller import chat_controller_bp
from teaching_platform.models.extensions import db
from teaching_platform.chat.extensions import socket

load_dotenv()
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
db_config, log_config = config["database"], config["logging"]
db_password, secret_key = os.getenv("db_password") ,os.getenv("secret_key")

logging.basicConfig(level=log_config["logging_lvl"], filemode="w", filename="../logs.log")
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

app = Flask(__name__)
app.register_blueprint(user_controller_bp)
app.register_blueprint(lesson_controller_bp)
app.register_blueprint(project_controller_bp)
app.register_blueprint(chat_controller_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_config['user']}:{db_password}" \
                                        f"@localhost:{db_config['port']}/{db_config['dbname']}"
app.config["SECRET"] = secret_key


db.init_app(app)
socket.init_app(app)

with app.app_context():
    db.create_all(bind_key="__all__")

# app.run()
socket.run(app, host="127.0.0.1", allow_unsafe_werkzeug=True)