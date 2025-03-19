from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages and session handling
socketio = SocketIO(app)

clients = {}
users_db = {}  # Store registered users (in-memory)

# Home page with options to Register, Login, or Chat Anonymously
@app.route('/')
def home():
    return render_template('home.html')

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']

        # Check if the user already exists
        if nickname in users_db:
            flash("User already exists!", "danger")
            return redirect(url_for('register'))

        # Store the user
        users_db[nickname] = password
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']

        # Check credentials
        if nickname in users_db and users_db[nickname] == password:
            flash("Login successful!", "success")
            session['nickname'] = nickname  # Store the nickname in the session
            return redirect(url_for('chat', nickname=nickname))

        flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html')

# Chat Route with Nickname (requires login or anonymous chat)
@app.route('/chat/<nickname>', methods=['GET'])
def chat(nickname):
    return render_template('chat.html', nickname=nickname)

# Anonymous Chat Route
@app.route('/chat/anonymous')
def chat_anonymous():
    session['nickname'] = "Anonymous"  # Set the nickname in the session to "Anonymous"
    return render_template('chat.html', nickname="Anonymous")

# SocketIO functionality for handling chat messages
@socketio.on('message')
def handle_message(msg):
    nickname = session.get('nickname', "Anonymous")  # Get nickname from session or default to "Anonymous"
    send(f"[{nickname}] {msg}", broadcast=True)

# Logout Route to end the session
@app.route('/logout')
def logout():
    session.pop('nickname', None)  # Remove nickname from session
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
