from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

clients = {}  # Dictionary to hold client sid and their nickname
admin_sids = []  # List of admin session IDs

@app.route('/')
def index():
    return render_template('index.html')

# Handle new messages
@socketio.on('message')
def handle_message(msg):
    if msg.startswith("NICK"):
        # Set the nickname for the client
        nickname = msg.split(" ", 1)[1]
        clients[request.sid] = nickname
        send(f"Nickname set to {nickname}", room=request.sid)
    elif msg.startswith("NAMES"):
        # Send the list of connected clients' nicknames
        names = " ".join(clients.values())
        send(f"[server] Connected users: {names}", room=request.sid)
    elif msg.startswith("BYEBYE"):
        # Handle client disconnecting with a goodbye message
        nickname = clients.get(request.sid, "Unknown")
        send(f"[server] {nickname} has left the chat", broadcast=True)
        socketio.emit('disconnect', room=request.sid)
        clients.pop(request.sid, None)
    elif msg.startswith("REMOVE"):
        # Admin command to remove a specific client
        if request.sid in admin_sids:  # Check if the user is an admin
            target_nickname = msg.split(" ", 1)[1]
            target_sid = None
            for sid, nickname in clients.items():
                if nickname == target_nickname:
                    target_sid = sid
                    break
            if target_sid:
                send(f"[server] {target_nickname} has been removed by an admin", broadcast=True)
                socketio.emit('disconnect', room=target_sid)
                clients.pop(target_sid, None)
            else:
                send(f"[server] No user with nickname {target_nickname} found.", room=request.sid)
        else:
            send(f"[server] You are not an admin and cannot remove users.", room=request.sid)
    else:
        # Broadcast the message to all clients with the sender's nickname
        sender_nick = clients.get(request.sid, "Unknown")
        send(f"[{sender_nick}] {msg}", broadcast=True)

# Handle disconnections
@socketio.on('disconnect')
def handle_disconnect():
    nickname = clients.get(request.sid, "Unknown")
    print(f"{nickname} disconnected")
    send(f"[server] {nickname} has left the chat", broadcast=True)
    clients.pop(request.sid, None)

if __name__ == '__main__':
    socketio.run(app, debug=True)
