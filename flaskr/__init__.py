import os

from flask import Flask
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .helpers import error_message

db =SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://wwdshzwaaqvose:8e07fc4a7675638df62c26930d39edd4e21c919a548a9cc9de3ca61b2b0b6aee@ec2-3-218-71-191.compute-1.amazonaws.com:5432/datrghjavahhuq') or \
            'sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Ensure responses aren't cached
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # check if the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import application
    app.register_blueprint(application.bp)

    #from . import db
    #db.init_app(app)

    def errorhandler(e):
        """Handle error"""
        if not isinstance(e, HTTPException):
            e = InternalServerError()
        return error_message(e.name, e.code)

    # Listen for errors
    for code in default_exceptions:
        app.errorhandler(code)(errorhandler)
    
    return app