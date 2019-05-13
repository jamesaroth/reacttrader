from flask import Flask, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "Please Work"
from flask_app import routes