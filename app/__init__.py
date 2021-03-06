import os

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restplus import Api
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from csv_to_db import Immigration

# app
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.getenv('SECRET_KEY')

# database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
manager.add_command("immigrate", Immigration)

# api routing
from app.router import namespace
api = Api(app, version='1.0', title='Company Search API', description='RESTful API for coding test')
api.add_namespace(namespace, path='/api')
