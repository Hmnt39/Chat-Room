from flask import render_template, redirect, url_for
from flask_socketio import join_room, emit, send
from app import app, socketio
import json
import uuid

## Room Details
ROOMS = {}

@socketio.on('create')
def on_create(data):
    print("Creating Room");
    roomId = str(uuid.uuid4())
    data['room']['id'] = roomId
    ROOMS[roomId] = {
        'users': [data['user']],
        'size': data['size'],
        'room': data['room']
    }
    join_room(roomId)
    emit('redirect', {'url': url_for('chat')})


@socketio.on('message')
def message(data):
    send(data, room='123')

@socketio.on('join')
def on_join(data):
    roomId = data['roomId']
    userId = data['userId']
    if roomId in ROOMS:
        ROOMS[roomId]['users'].append(userId)
        join_room(roomId)
        msg = str(userId) + 'joined'
        emit('join_room', msg)
    else:
        emit('error', {'error': 'Unable to join room. Room does not exist.'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')