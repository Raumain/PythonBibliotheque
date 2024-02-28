from flask import Flask
import sqlite3
from flask import g

DATABASE = 'db/database.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    cur = get_db().cursor()
    return "<p>Je suis homo.. sapiens LOL !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!</p>"

