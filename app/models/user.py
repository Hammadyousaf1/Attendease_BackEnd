from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    phone: str
    embedding: list[float]