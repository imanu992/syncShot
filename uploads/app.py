from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

user_images = {}

@app.route('/upload', methods=['POST'])
def upload_photo():
    user_id = request.form.get('user_id')  # L'ID dell'utente che sta caricando la foto

    if not user_id:
        return jsonify({"error": "ID utente mancante"}), 400

    if 'photo' not in request.files:
        return jsonify({"error": "Nessuna foto inviata"}), 400

    file = request.files['photo']
    file_path = os.path.join(UPLOAD_FOLDER, f"{user_id}.jpg")
    file.save(file_path)

    # Salviamo nel dizionario chi ha caricato cosa
    user_images[user_id] = file_path

    return jsonify({"message": "Foto caricata con successo!"}), 200

@app.route('/get_photo', methods=['GET'])
def get_photo():
    user_id = request.args.get('user_id')  # ID dell'utente che richiede la foto

    if not user_id:
        return jsonify({"error": "ID utente mancante"}), 400

    # Trova l'ultima immagine dell'altro utente
    other_user_photo = None

    for uid, path in user_images.items():
        if uid != user_id:
            other_user_photo = path
            break

    if not other_user_photo or not os.path.exists(other_user_photo):
        return jsonify({"error": "Nessuna immagine disponibile"}), 404

    return send_file(other_user_photo, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
