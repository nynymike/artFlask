from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.name = "artFlask"

'''
Configurations to conect to testArt Mongo Database
Must created by manual throw mongo shell:
> use testArt
> db.addUser("tester1", "123456")
'''

app.config['MONGO_DBNAME'] = 'testArt'
app.config.from_pyfile('conf.py')

# app.config['MONGO_USERNAME'] = 'tester1'
# app.config['MONGO_PASSWORD'] = '123456'

mongo = PyMongo(app)