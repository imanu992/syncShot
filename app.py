from flask import Flask, request, jsonify

app = Flask(__name__)

# Variabile per salvare l'ultima immagine caricata
last_uploaded_image = None

@app.route("/upload", methods=["POST"])
def upload():
    global last_uploaded_image
    image_url = request.json.get("image_url")  # Ricevi URL immagine da frontend
    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    last_uploaded_image = image_url  # Salva l'immagine
    return jsonify({"message": "Image uploaded successfully", "image_url": last_uploaded_image})

@app.route("/latest", methods=["GET"])
def latest():
    if last_uploaded_image:
        return jsonify({"latest_image": last_uploaded_image})
    return jsonify({"message": "No image uploaded yet"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
