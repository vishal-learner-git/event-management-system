import os
import logging
from flask import Flask, render_template, redirect, url_for, session
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_moment import Moment
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
moment = Moment(app)    
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Register blueprints
from auth import auth_bp
from student.routes import student_bp
from organizer.routes import organizer_bp
from admin.routes import admin_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(organizer_bp, url_prefix='/organizer')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.template_filter('strftime')
def datetime_filter(value, format='%B %d, %Y at %I:%M %p'):
    """Template filter to safely format datetime objects"""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('base.html', title='Server Error'), 500

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)