import os

from flask import Flask

app = Flask(__name__)

DEBUG = True
PORT = 8000

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)