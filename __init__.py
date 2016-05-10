__author__ = "Jeremy Nelson"

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config["SECRET_KEY"] = "abdfg"

from views import *
