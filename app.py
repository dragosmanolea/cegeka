from flask import Flask
from lib.cv_api import cv_blueprint

app = Flask(__name__)
app.register_blueprint(cv_blueprint)


app.run(host='0.0.0.0', port=13031)
