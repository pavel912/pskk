from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("App")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # replace it later for safety issues
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd()) + '\db\pskk_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
