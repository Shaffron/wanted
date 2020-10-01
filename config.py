import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG = True
TESTING = True
SQLALCHEMY_DATABASE_URI = os.getenv('DEFAULT_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
