from flask import Flask
from flask_socketio import SocketIO, join_room, emit, send

app = Flask(__name__)
socketio = SocketIO(app)

from app import views