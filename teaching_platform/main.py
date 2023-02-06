import logging

import yaml
import jsonpickle
from flask import Flask

from teaching_platform.users.controller import user_controller_bp
from teaching_platform.lessons.controller import lesson_controller_bp
from teaching_platform.projects.controller import project_controller_bp
from teaching_platform.extensions import db


with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
db_config = config["database"]
log_config = config["logging"]

logging.basicConfig(level=log_config["logging_lvl"], filemode="w", filename="../logs.log")
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

app = Flask(__name__)
app.register_blueprint(user_controller_bp)
app.register_blueprint(lesson_controller_bp)
app.register_blueprint(project_controller_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_config['user']}:{db_config['password']}" \
                                        f"@localhost:{db_config['port']}/{db_config['dbname']}"

db.init_app(app)

with app.app_context():
    db.create_all(bind_key="__all__")

app.run()