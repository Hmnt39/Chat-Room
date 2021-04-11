from flask import render_template, redirect, url_for, request
from flask_socketio import join_room, emit, send
from app import app, socketio
import json
import uuid

## Room Details
ROOMS = {}

@socketio.on('create')
def on_create(data):
    print("Creating Room");
    roomId = "123"
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


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        result = request.form
        id = "123"
        room = {
            'id' : id,
            'room_name': result.get('room_name'),
            'description': result.get('description')
        }
        user = {
            'name': result.get('name')
        }
        ROOMS[id] = {
            'users': [user],
            'room': room
        }
        join_room(id)
        return render_template("chat.html", result=ROOMS[id])
    return render_template('index.html')

@app.route('/join', methods = ['POST', 'GET'])
def join():
    if request.method == 'POST':
        result = request.form
        id =  result.get('room_id').lower()
        if id in ROOMS:
            ROOMS[id]['users'].append(
                {
                    'name': result.get('name')
                })
            return render_template("chat.html", result=ROOMS[id])
    return render_template('join.html')
