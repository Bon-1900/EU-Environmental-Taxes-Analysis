# Aly Nour & Isabella Dube-Miglioli

from flask import Flask
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
photos = UploadSet('photos', IMAGES)


def create_app(config_classname):
    """
    Initialise and configure the Flask application
    :tupe config_classname: Specifies the configuration class
    :rtupe: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_classname)

    register_dash_apps(app)
    register_extensions(app)
    register_blueprints(app)

    configure_uploads(app, photos)

    csrf.exempt('dash.dash.dispatch')

    return app


def register_extensions(app):
    # Initialise the SQLAlchemy object for the Flask app instance
    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from my_app.models import User, Profile, Blog
        db.create_all()


def register_blueprints(app):
    from my_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from my_app.community.routes import community_bp
    app.register_blueprint(community_bp)

    from my_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)


def register_dash_apps(app):
    with app.app_context():
        from dash_apps.app_eu import DashAppEU
        from dash_apps.app_s_eu import DashAppSEU
        from dash_apps.app_italy import DashAppItaly

        dash_app1 = DashAppEU(app)
        dash_app1.setup()
        _protect_dash_views(dash_app1.app)
        dash_app2 = DashAppSEU(app)
        dash_app2.setup()
        _protect_dash_views(dash_app2.app)
        dash_app3 = DashAppItaly(app)
        dash_app3.setup()
        _protect_dash_views(dash_app3.app)


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
