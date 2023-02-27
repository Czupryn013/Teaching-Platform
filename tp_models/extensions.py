from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_mail import Mail

db = SQLAlchemy()
auth = HTTPBasicAuth()
mail = Mail()