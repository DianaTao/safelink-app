"""
SafeLink App - Flask Application Factory
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app.config.from_object(f'app.config.{config_name.capitalize()}Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from app.routes import auth, ai, resources, alerts, users, cases
    
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(ai.bp, url_prefix='/ai')
    app.register_blueprint(resources.bp, url_prefix='/resources')
    app.register_blueprint(alerts.bp, url_prefix='/alerts')
    app.register_blueprint(users.bp, url_prefix='/users')
    app.register_blueprint(cases.bp, url_prefix='/cases')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'SafeLink App is running'}
    
    return app 