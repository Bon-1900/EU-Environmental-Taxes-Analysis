# Aly Nour & Isabella Dube-Miglioli

"""Flask config class."""
from pathlib import Path
import os


class Config(object):
    """Sets the Flask base configuration that is common to all environments"""
    DEBUG = False
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_PATH = Path( '../data' )
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('user.sqlite'))
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("static").joinpath("img")


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

