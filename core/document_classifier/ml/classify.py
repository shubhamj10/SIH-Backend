from keras.models import load_model
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

# Pre-load the model and labels once to improve performance
MODEL_PATH = "models/keras_model.h5"
LABELS_PATH = "models/labels.txt"

model = load_model(MODEL_PATH, compile=False)

with open(LABELS_PATH, "r") as file:
    class_names = [line.strip()[2:] for line in file]  # Strip label indices safely


def preprocess_document(image_path):
    """Preprocess the input image to the required model format."""
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    try:
        image = Image.open(image_path).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array
        return data
    except Exception as e:
        raise ValueError(f"Error processing image {image_path}: {e}")


def classify_document(image_path):
    """Classify the document using the pre-loaded model."""
    try:
        data = preprocess_document(image_path)
        prediction = model.predict(data)
        
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        return class_name, confidence_score
    except Exception as e:
        return {"error": str(e)}