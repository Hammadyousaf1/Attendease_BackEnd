from fastapi import APIRouter, UploadFile, Form, File, HTTPException
from app.services.face_recognition import get_embedding
from app.services.supabase_client import get_supabase_client
from app.utils.helpers import (
    save_temp_file, delete_temp_file, normalize_embedding,
    calculate_dynamic_threshold,
    raise_http_exception,
)
import numpy as np
from datetime import datetime, timedelta
from app.models.attendance import Attendance

router = APIRouter()

def mark_attendance(user_id, user_name, timestamp):
    supabase_client = get_supabase_client()
    attendance_time = datetime.fromisoformat(timestamp.rstrip("Z"))

    response = supabase_client.table("attendance")\
        .select("timestamp")\
        .eq("user_id", user_id)\
        .order("timestamp", desc=True)\
        .limit(1)\
        .execute()

    if response.data:
        last_attendance_time = datetime.fromisoformat(response.data[0]["timestamp"].rstrip("Z"))
        if attendance_time - last_attendance_time < timedelta(minutes=2):
            print(f"{user_name} is already present")
            return

    # Convert datetime to string before inserting
    attendance_data = {
        "user_id": user_id,
        "user_name": user_name,
        "timestamp": attendance_time.isoformat()  # Ensure JSON serializability
    }
    print(f"Attendance marked for {user_name}")
    supabase_client.table("attendance").insert(attendance_data).execute()

@router.post("/recognize")
async def recognize(
    image: UploadFile = File(...),
    timestamp: str = Form(...)
):
    supabase_client = get_supabase_client()
    response = supabase_client.table("users").select("id, name, embedding").execute()
    users = response.data

    if not users:
        print("No stored embeddings available.")
        raise_http_exception(500, "No stored embeddings available.")

    ids, names, stored_embeddings = [], [], []
    for user in users:
        embedding = np.array(user["embedding"], dtype=np.float32)
        if embedding.shape == (512,):
            ids.append(user["id"])
            names.append(user["name"])
            stored_embeddings.append(embedding)

    if not stored_embeddings:
        print("No valid embeddings available.")
        raise_http_exception(500, "No valid embeddings available.")

    stored_embeddings = np.array(stored_embeddings)

    temp_path = save_temp_file(await image.read())
    if not temp_path:
        raise_http_exception(500, "Failed to save temporary file")

    embedding = get_embedding(temp_path)
    delete_temp_file(temp_path)

    if embedding is None:
        print("No face detected!")
        raise_http_exception(400, "No face detected!")
    

    embedding = normalize_embedding(embedding.reshape(1, -1))
    similarities = np.dot(stored_embeddings, embedding.T).flatten()
    recognized_index = np.argmax(similarities)
    recognized_name = names[recognized_index]
    max_similarity = similarities[recognized_index]

    threshold = calculate_dynamic_threshold(similarities)
    if max_similarity < threshold:
        return {"recognized_name": "Unknown", "similarity": float(max_similarity), "status": 200}

    recognized_user_id = ids[recognized_index]
    mark_attendance(recognized_user_id, recognized_name, timestamp)

    return {"recognized_name": recognized_name, "similarity": float(max_similarity), "attendance_marked": True, "status": 200}