from flask import Flask, json, render_template
from flask_socketio import SocketIO, emit

import pyorg
import time
import datetime as dt

app = Flask(__name__);
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html', data=pyorg.parseorg('example.org'))

@app.route("/json")
def jsonorg():
    return json.jsonify({'data':pyorg.parseorg('example.org')})

@socketio.on('data')
def data(data):
    pyorg.makeorg(data['data'], 'example.org')
    return

@socketio.on('bonjour')
def bonjour(org):
    return

if __name__ == "__main__":
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=1337)

