from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load model ONCE at startup
model = tf.keras.models.load_model("cipher10_cnn_augmented.keras")

CLASS_NAMES = [
    "Airplane",
    "Automobile",
    "Bird",
    "Cat",
    "Deer",
    "Dog",
    "Frog",
    "Horse",
    "Ship",
    "Truck"
]

def preprocess_image(image):
    image = image.resize((32, 32))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["file"]
    image = Image.open(file).convert("RGB")

    processed = preprocess_image(image)
    predictions = model.predict(processed)
    class_index = int(np.argmax(predictions))

    return jsonify({
        "prediction": CLASS_NAMES[class_index],
        "confidence": f"This is an image of a {CLASS_NAMES[class_index]} with confidence {float(np.max(predictions))}"
    })

if __name__ == "__main__":
    app.run(debug=True)