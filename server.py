from flask import Flask, json, render_template
from flask_socketio import SocketIO, emit
import threading
import pyorg
import os
import time
import eventlet

eventlet.monkey_patch()

app = Flask(__name__);
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


last_changed = time.time()
def watch():
    global last_changed
    while True:
        time.sleep(2)
        new_changed = os.stat('example.org').st_mtime
        if new_changed > last_changed:
            print 'org file on server updated'
            socketio.emit("data", pyorg.parseorg('example.org'))
            last_changed = new_changed


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
def bonjour(msg):
    print 'Client connected'
    emit("data", pyorg.parseorg('example.org'))

if __name__ == "__main__":
    thread = threading.Thread(target = watch)
    thread.daemon = True
    thread.start()
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=1337)

