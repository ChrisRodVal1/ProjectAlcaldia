from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, User, Destination, History
from flask_socketio import SocketIO, send
from threading import Thread 
import time
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Your Telegram Bot Token and Chat ID (admin's Telegram ID)
TELEGRAM_BOT_TOKEN = 'REPLACE_WITH_YOUR_TELEGRAM_TOKEN'
TELEGRAM_CHAT_ID = 'REPLACE_WITH_YOUR_TELEGRAM_CHATID'

# Import database config
app.config.from_object('config.Config')
db.init_app(app)

# Function to send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Error sending message to Telegram: {response.status_code} - {response.text}")
    return response

# Function to receive messages from Telegram
def receive_telegram_message():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error receiving messages from Telegram: {response.status_code} - {response.text}")
        return None
    
    # Return the JSON response which contains the updates/messages
    return response.json()

# Background task to check for new Telegram messages
def telegram_message_listener():
    last_update_id = None  # To keep track of the last update processed
    while True:
        updates = receive_telegram_message()
        if updates and 'result' in updates:
            for update in updates['result']:
                if 'message' in update:
                    message = update['message']
                    # Check if the message has the 'text' field
                    if 'text' in message:
                        text_message = message['text']
                        update_id = update['update_id']
                        if last_update_id is None or update_id > last_update_id:
                            last_update_id = update_id
                            print(f"Received message from Telegram: {text_message}")
                            # Emit the message to all connected clients via Socket.IO
                            socketio.emit('telegram_message', text_message)
        time.sleep(5)  # Wait for a few seconds before checking again


# Start the listener in a separate thread
thread = Thread(target=telegram_message_listener)
thread.start()

# Handle incoming messages from clients
@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    # Send message to Telegram
    response = send_telegram_message(msg)
    if response.status_code == 200:
        print("Message sent to Telegram successfully.")
        # Emit the message back to all connected clients
        socketio.emit('telegram_message', msg, to='*')  # Broadcast to all connected clients
    else:
        print(f"Failed to send message to Telegram: {response.text}")
    
# Routes for User
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'nombre': user.complete_name,
        'contraseña': user.password,  # Included the password
        'correo': user.email,
        'fecha_creacion': user.date_registered
    } for user in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'nombre': user.complete_name,
        'contraseña': user.password,  # Included the password
        'correo': user.email,
        'fecha_creacion': user.date_registered
    }), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get_or_404(user_id)
    user.complete_name = data.get('nombre', user.complete_name)
    user.password = data.get('contraseña', user.password)
    user.email = data.get('correo', user.email)
    user.date_registered = data.get('fecha_creacion', user.date_registered)
    db.session.commit()
    send_telegram_message(f'User {user.complete_name} (ID: {user.id}) was updated.')
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        user_name = user.complete_name  # Store name for the message before deletion

        # Now delete the user
        db.session.delete(user)
        db.session.commit()

        # Send Telegram notification
        send_telegram_message(f'User {user_name} (ID: {user.id}) was deleted.')

        return jsonify({'message': 'User deleted successfully'}), 204

    except Exception as e:
        # Handle any exception that occurs
        return jsonify({'message': 'An error occurred while deleting the user', 'error': str(e)}), 500




# Routes for Destination
@app.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([{
        'id': dest.id,
        'id_usuario': dest.user_id,
        'ubicacion_inicial': dest.departure,
        'ubicacion_final': dest.destination,
        'duracion_estimada_minutos': dest.duration,
        'fecha_creacion': dest.date_registered,
        'medio_esperado': dest.transportation
    } for dest in destinations]), 200

@app.route('/destinations/<int:dest_id>', methods=['GET'])
def get_destination(dest_id):
    dest = Destination.query.get_or_404(dest_id)
    return jsonify({
        'id': dest.id,
        'id_usuario': dest.user_id,
        'ubicacion_inicial': dest.departure,
        'ubicacion_final': dest.destination,
        'duracion_estimada_minutos': dest.duration,
        'fecha_creacion': dest.date_registered,
        'medio_esperado': dest.transportation
    }), 200

@app.route('/destinations/<int:dest_id>', methods=['PUT'])
def update_destination(dest_id):
    try:
        data = request.json
        dest = Destination.query.get_or_404(dest_id)

        # Update destination attributes
        dest.departure = data.get('ubicacion_inicial', dest.departure)
        dest.destination = data.get('ubicacion_final', dest.destination)
        dest.duration = data.get('duracion_estimada_minutos', dest.duration)
        dest.date_registered = data.get('fecha_creacion', dest.date_registered)
        dest.transportation = data.get('medio_esperado', dest.transportation)

        # Save changes to the database
        db.session.commit()

        # Send Telegram notification
        send_telegram_message(
            f"Destination (ID: {dest.id}) for User ID {dest.user_id} was updated."
        )

        return jsonify({'message': 'Destination updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred while updating the destination', 'error': str(e)}), 500


@app.route('/destinations/<int:dest_id>', methods=['DELETE'])
def delete_destination(dest_id):
    try:
        # Fetch the destination using the provided ID
        dest = Destination.query.get_or_404(dest_id)
        departure = dest.departure  # Save departure location before deletion
        destination = dest.destination  # Save destination location before deletion
        user_id = dest.user_id  # Save user ID associated with the destination

        # Option 1: If you want to delete associated histories:
        for hist in dest.histories:
            db.session.delete(hist)

        # Option 2: If you want to keep the histories but set the foreign key to NULL:
        # for hist in dest.histories:
        #     hist.destination_id = None  # or set to some default value if needed

        # Now delete the destination
        db.session.delete(dest)
        db.session.commit()

        # Send Telegram notification
        send_telegram_message(f'Destination from {departure} to {destination} (ID: {dest.id}) for User ID {user_id} was deleted.')

        return jsonify({'message': 'Destination deleted successfully'}), 204

    except Exception as e:
        return jsonify({'message': 'An error occurred while deleting the destination', 'error': str(e)}), 500



# Routes for History
@app.route('/histories', methods=['GET'])
def get_histories():
    histories = History.query.all()
    return jsonify([{
        'id': hist.id,
        'id_ruta': hist.destination_id,
        'id_usuario': hist.user_id,
        'hora_inicio': hist.start_time,
        'hora_fin': hist.finish_time,
        'distanciakm': hist.distance,
        'camino': hist.path,
        'medio_usado': hist.transportation
    } for hist in histories]), 200

@app.route('/histories/<int:hist_id>', methods=['GET'])
def get_history(hist_id):
    hist = History.query.get_or_404(hist_id)
    return jsonify({
        'id': hist.id,
        'id_ruta': hist.destination_id,
        'id_usuario': hist.user_id,
        'hora_inicio': hist.start_time,
        'hora_fin': hist.finish_time,
        'distanciakm': hist.distance,
        'camino': hist.path,
        'medio_usado': hist.transportation
    }), 200

@app.route('/histories/<int:hist_id>', methods=['PUT'])
def update_history(hist_id):
    data = request.json
    hist = History.query.get_or_404(hist_id)
    hist.start_time = data.get('hora_inicio', hist.start_time)
    hist.finish_time = data.get('hora_fin', hist.finish_time)
    hist.distance = data.get('distanciakm', hist.distance)
    hist.path = data.get('camino', hist.path)
    hist.transportation = data.get('medio_usado', hist.transportation)
    db.session.commit()
    return jsonify({'message': 'History updated successfully'}), 200

@app.route('/histories/<int:hist_id>', methods=['DELETE'])
def delete_history(hist_id):
    hist = History.query.get_or_404(hist_id)
    db.session.delete(hist)
    db.session.commit()
    return jsonify({'message': 'History deleted successfully'}), 204


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)

