#! /usr/bin/python
# -*- encoding: utf-8 -*-
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='templates', static_url_path='/static/', static_folder='static')
socket = SocketIO(app)

players = {}

@app.route('/')
def index():
    return render_template('index.html')

@socket.on('connect')
def conn():
    player = {
        'x': 350,
        'y': 450
    }
    players[request.sid] = player
    return emit('bootstrap', players)

@socket.on('disconnect')
def disconnect():
    del players[request.sid]
    emit('playerDisconnected', request.sid, broadcast=True)

@socket.on('playerUpdate')
def playerUpdate(playerData):
    players[request.sid] = playerData
    emit('gameUpdate', players, broadcast=True)

if __name__ == '__main__':
    socket.run(app, debug=True)