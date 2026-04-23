"""
Configuration settings for the Aursikho application.
"""
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aursikho-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'aursikho.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    CERTIFICATE_FOLDER = os.path.join(basedir, 'app', 'static', 'certificates')
    CERTIFICATE_TEMPLATE = os.path.join(basedir, 'certificate_template', 'template.png')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size

    # Application settings
    COURSES_PER_PAGE = 9
    APP_NAME = 'Aursikho'
