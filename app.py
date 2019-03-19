from flask import Flask, g
from flask import render_template, flash, redirect, url_for
# This gains access to our models
import models
from forms import
from forms import

app = Flask(__name__)
app.secret_key = 'lkasmdf.lksajmflkalfgj.klsdnfaj'

DEBUG = True
PORT = 8000


@app.before_request
def before_request():
    # connect to the DB before each request
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    # close the db connection after each request
    g.db.close()
    return response


@app.route('/')
# @app.route('/movies', methods=['GET'])
# def index():
# @app.route('/')
# def hello_world():
#     return 'Hello World'
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
