import os
import tempfile
import numpy as np
from datetime import datetime
from fastapi import HTTPException
from typing import Optional, List, Dict, Any
import re

# File Handling
def save_temp_file(file: bytes, suffix: str = ".jpg") -> Optional[str]:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(file)
            return temp_file.name
    except Exception as e:
        print(f"Error saving temporary file: {e}")
        return None

def delete_temp_file(file_path: str) -> bool:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting temporary file: {e}")
        return False

# Timestamp Utilities
def parse_timestamp(timestamp: str) -> Optional[datetime]:
    try:
        timestamp = timestamp.rstrip("Z")
        return datetime.fromisoformat(timestamp)
    except ValueError as e:
        print(f"Error parsing timestamp: {e}")
        return None

def format_timestamp(dt: datetime) -> str:
    return dt.isoformat() + "Z"

# Embedding Utilities
def normalize_embedding(embedding: np.ndarray) -> np.ndarray:
    return embedding / np.linalg.norm(embedding)

def calculate_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    return np.dot(embedding1, embedding2)

# Dynamic Threshold
def calculate_dynamic_threshold(similarities: np.ndarray) -> float:
    return max(0.4, min(0.7, np.mean(similarities) + 0.1))

# Error Handling
def raise_http_exception(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)

def log_error(error: Exception, context: str = ""):
    print(f"Error in {context}: {error}")

# Validation
def validate_phone_number(phone: str) -> bool:
    pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
    return bool(pattern.match(phone))

def validate_image_file(file: bytes) -> bool:
    try:
        from PIL import Image
        from io import BytesIO
        Image.open(BytesIO(file)).verify()
        return True
    except Exception:
        return False

# Database Utilities
def fetch_all_users(supabase_client) -> List[Dict[str, Any]]:
    response = supabase_client.table("users").select("*").execute()
    return response.data

def fetch_user_by_id(supabase_client, user_id: str) -> Optional[Dict[str, Any]]:
    response = supabase_client.table("users").select("*").eq("id", user_id).execute()
    return response.data[0] if response.data else None