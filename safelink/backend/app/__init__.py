from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from app.routes import auth, ai, resources, users, cases
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(ai.bp, url_prefix='/api/ai')
    app.register_blueprint(resources.bp, url_prefix='/api/resources')
    app.register_blueprint(users.bp, url_prefix='/api/users')
    app.register_blueprint(cases.bp, url_prefix='/api/cases')

    @app.route('/api/health')
    def health():
        return {'status': 'ok'}

    return app 