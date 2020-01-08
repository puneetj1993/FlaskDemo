from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
#app.secret_key = b'\_5#y2L"F4Q8z\n\xec]/'
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config.from_object("config.DevelopmentConfig")


db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#The below statement will redirect the user to /login page and is invoked by @login_required decorator in /post func
login_manager.login_view = 'login' #'login' is the name of login function

from flask_package import views

