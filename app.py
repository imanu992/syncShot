from flask import Flask, request, jsonify

app = Flask(__name__)

# Dizionario per tenere traccia delle immagini per ogni utente
user_images = {}

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json
    image_url = data.get("image_url")
    uploader = data.get("uploader")  # Nome di chi carica l'immagine
    receiver = data.get("receiver")  # Nome di chi deve vedere l'immagine
    
    if not image_url or not uploader or not receiver:
        return jsonify({"error": "Missing image URL, uploader, or receiver"}), 400

    # Salviamo l'immagine solo per il destinatario
    user_images[receiver] = image_url
    
    return jsonify({"message": "Image uploaded", "image_url": image_url, "receiver": receiver})

@app.route("/latest/<username>", methods=["GET"])
def latest(username):
    image = user_images.get(username)
    
    if image:
        return jsonify({"latest_image": image})
    return jsonify({"message": "No image uploaded yet"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)