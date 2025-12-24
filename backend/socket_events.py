from flask_socketio import join_room
from flask_jwt_extended import decode_token
from flask import request
from extensions import socketio

@socketio.on("connect")
def handle_connect():
    print("Socket connect attempt")

    token = request.cookies.get("access_token_cookie")
    if not token:
        print("No JWT cookie, rejecting socket")
        return False

    decoded = decode_token(token)
    user_id = decoded["sub"]

    print(f"Socket connected for user {user_id}")
    join_room(f"user_{user_id}")

