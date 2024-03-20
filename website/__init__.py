from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

#creates app, using flask 


#database
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld' #registers just key
    #database init
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin_view import admin_views
    from .opportunity_maker import opportunity_maker

    app.register_blueprint(views, url_prefix = '/') #registers blueprint from views.py
    app.register_blueprint(auth, url_prefix= '/') #registers blueprint from auth.py
    app.register_blueprint(admin_views, url_prefix= '/')
    app.register_blueprint(opportunity_maker, url_prefix= '/')
#-----------------------------------
    from .models import User

    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
            email = "admin@ucu.edu.ua"
            username = None
            password = "secret_admin"
            program = None
            faculty = None
            total_hours = None
            done_hours = None
            admin = User.query.filter_by(email=email).first()
            if admin is None:
                admin = User(email=email, 
                            username=username, 
                            password=generate_password_hash(password, method='scrypt'), 
                            program=program,
                            faculty=faculty,
                            total_hours=total_hours,
                            done_hours=done_hours,
                            is_admin = True)
            db.session.add(admin)
            db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

#-----------------------------------
    return app