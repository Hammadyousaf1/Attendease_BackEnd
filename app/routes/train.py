from fastapi import APIRouter, UploadFile, Form, File, HTTPException
from app.services.face_recognition import get_embedding
from app.services.supabase_client import get_supabase_client
from app.utils.helpers import save_temp_file, delete_temp_file, normalize_embedding, raise_http_exception, log_error
import numpy as np

router = APIRouter()

@router.post("/train")
async def train(
    id: str = Form(...),
    name: str = Form(...),
    phone: str = Form(...),
    images: list[UploadFile] = File(...)
):
    supabase_client = get_supabase_client()
    embeddings = []

    for image in images:
        temp_path = save_temp_file(await image.read())
        if not temp_path:
            raise_http_exception(500, "Failed to save temporary file")

        embedding = get_embedding(temp_path)
        delete_temp_file(temp_path)

        if embedding is not None:
            embeddings.append(embedding)

    if not embeddings:
        raise_http_exception(400, "No valid embeddings generated.")

    avg_embedding = normalize_embedding(np.mean(embeddings, axis=0))

    user_data = {
        "id": id,
        "name": name,
        "phone": phone,
        "embedding": avg_embedding.tolist()
    }
    supabase_client.table("users").upsert(user_data).execute()

    return {"message": "User trained successfully!", "status": 200}