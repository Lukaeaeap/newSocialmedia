from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SeCReT key that no one knows'
    # The sqlite database is stored at a certain location the f before it gives the option to add a variable like the (global variable) DB_NAME to it:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    # The slash means no prefix, prefix /luuk/ would give for example www.website.com/luuk/partofsite/
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # import the classes from models
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    # the login field can be gotten at the location of auth.login
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # How flask should load the user, they can get the user with their id (the primary key of a user)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # if the database exists, do not create a new one
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
