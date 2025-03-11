from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

# Cartella in cui salvare le immagini caricate
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'Nessuna foto inviata'}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({'error': 'Nessun file selezionato'}), 400

    if file and allowed_file(file.filename):
        # Creiamo un nome univoco basato sulla data e ora
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Se desideri avere un URL costante (es. sempre 'latest') potresti aggiornare un link simbolico
        latest_path = os.path.join(UPLOAD_FOLDER, 'latest.' + ext)
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(filename, latest_path)

        # Costruiamo l'URL per accedere alla foto
        photo_url = request.url_root + 'uploads/' + filename
        return jsonify({'message': 'Foto caricata con successo', 'url': photo_url}), 200

    return jsonify({'error': 'Tipo di file non consentito'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
