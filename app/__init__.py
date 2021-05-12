#the __init__creates an instance of the class Flask

#from module flask inport the class Flask
from flask import Flask
#from the module config import the class Config
from config import Config
#from module flask_sqlalchemy import class SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
#from module flask_migrate import class Migrate
from flask_migrate import Migrate


#when we call "app" we will be creating an instance of Flask
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

#This has to happen after instantiating the Flask class
#this import it needed to connect the routes to the app
from app import routes, models
