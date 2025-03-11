from flask import Flask, request, jsonify

app = Flask(__name__)

# Variabili per tenere traccia dell'ultima immagine caricata e dell'uploader
last_uploaded_image = None
last_uploader = None

@app.route("/upload", methods=["POST"])
def upload():
    global last_uploaded_image, last_uploader
    data = request.json
    image_url = data.get("image_url")
    uploader = data.get("uploader")  # Nome di chi carica l'immagine
    
    if not image_url or not uploader:
        return jsonify({"error": "Missing image URL or uploader"}), 400

    last_uploaded_image = image_url
    last_uploader = uploader
    
    return jsonify({"message": "Image uploaded", "image_url": last_uploaded_image, "uploader": last_uploader})

@app.route("/latest", methods=["GET"])
def latest():
    if last_uploaded_image:
        return jsonify({"latest_image": last_uploaded_image, "uploader": last_uploader})
    return jsonify({"message": "No image uploaded yet"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
