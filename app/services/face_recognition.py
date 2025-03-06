import numpy as np
import cv2
from insightface.app import FaceAnalysis

face_analysis = FaceAnalysis(name="buffalo_l")
face_analysis.prepare(ctx_id=0)

def get_embedding(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = face_analysis.get(image)

    if not faces:
        return None

    best_face = max(faces, key=lambda f: f.det_score)
    return best_face.normed_embedding