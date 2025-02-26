import cv2
import dlib
import numpy as np
import joblib
import os

# Load Pre-Trained Models
MODEL_PATH = "utils/ai_models/"
models = {
    "calm": joblib.load(os.path.join(MODEL_PATH, "Did he appear calm. (Calm).pkl")),
    "eye_contact": joblib.load(
        os.path.join(
            MODEL_PATH, "Did he maintained proper eye contact. (Eye Contact).pkl"
        )
    ),
    "excitement": joblib.load(
        os.path.join(MODEL_PATH, "Did he seem excited. (Excitement).pkl")
    ),
    "focus": joblib.load(
        os.path.join(MODEL_PATH, "Did he seem focused. (Focused).pkl")
    ),
    "friendliness": joblib.load(
        os.path.join(MODEL_PATH, "Did he seem Friendly. (Friendliness).pkl")
    ),
    "smile": joblib.load(
        os.path.join(MODEL_PATH, "Did he smile appropriately. (Smile).pkl")
    ),
    "engagement": joblib.load(
        os.path.join(MODEL_PATH, "Did he use engaging tone. (Engagement).pkl")
    ),
}

# Face Detector
face_detector = dlib.get_frontal_face_detector()


def extract_facial_features(face_img):
    """Extracts facial features from an image (Simple Placeholder)"""
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (64, 64))  # Resize for model compatibility
    return resized.flatten()  # Convert to 1D feature vector


def analyze_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)

    results = []
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        face_img = frame[y : y + h, x : x + w]

        try:
            features = extract_facial_features(face_img)
            engagement_scores = {
                metric: model.predict([features])[0] for metric, model in models.items()
            }

            # Determine if engaged based on specific models
            engaged = (
                engagement_scores["eye_contact"] > 0.5
                and engagement_scores["focus"] > 0.5
                and engagement_scores["smile"] > 0.5
            )

            results.append(
                {
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h,
                    "scores": engagement_scores,
                    "engaged": engaged,
                }
            )
        except Exception as e:
            results.append({"error": str(e)})

    return {"faces_detected": len(faces), "engagement_analysis": results}
