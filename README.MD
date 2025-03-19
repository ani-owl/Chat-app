# Chat Application

This project is a real-time chat application built using Flask and Flask-SocketIO. It allows users to register, log in, and participate in chat rooms. Users can also chat anonymously without registering. The application supports real-time messaging and includes features like user sessions and logout functionality.

This project is an expanded version of the `serverChat.py` project, which allowed communication between clients via TCP on the terminal. The current version builds upon that concept by introducing a web-based interface and real-time communication using WebSockets.

## Features

- **User Registration and Login**: Users can register with a nickname and password, log in, and participate in chat rooms.
- **Anonymous Chat**: Users can join the chat anonymously without registering.
- **Real-Time Messaging**: Messages are broadcast to all connected users in real-time using Flask-SocketIO.
- **Session Management**: User sessions are managed to maintain state across requests.
- **Logout with Goodbye Message**: Users can log out and optionally leave a goodbye message that is broadcast to other users.

## Installation

### Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO

### Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd chat
   ```

2. Install the required dependencies:

   ```bash
   pip install flask flask-socketio
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000`.

## Usage

### Home Page

The home page provides three options:

- **Register**: Create a new account.
- **Login**: Log in with an existing account.
- **Chat Anonymously**: Join the chat without registering.

### Registration

- Navigate to the `/register` route.
- Enter a nickname and password to create an account.

### Login

- Navigate to the `/login` route.
- Enter your registered nickname and password to log in.

### Chat

- After logging in, you will be redirected to the chat room.
- Anonymous users can join the chat directly from the home page.

### Logout

- Click the "Logout" button to end your session.
- You will be prompted to leave a goodbye message, which will be broadcast to other users.

## Real-Time Messaging

The application uses Flask-SocketIO to handle real-time messaging. Messages are broadcast to all connected users, and the sender's nickname is displayed alongside the message.

### Example Message Handling

- **Broadcast Message**: Messages are sent to all connected users.
- **Goodbye Message**: When a user logs out, their goodbye message is broadcast to all users.

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.