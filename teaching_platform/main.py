import yaml

from flask import Flask

from teaching_platform.users.controller import user_controller_bp
from teaching_platform.lessons.controller import lesson_controller_bp
from teaching_platform.extensions import db


with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
db_config = config["database"]

app = Flask(__name__)
app.register_blueprint(user_controller_bp)
app.register_blueprint(lesson_controller_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_config['user']}:{db_config['password']}" \
                                        f"@localhost/{db_config['dbname']}"

db.init_app(app)

with app.app_context():
    db.create_all(bind_key="__all__")

app.run()
