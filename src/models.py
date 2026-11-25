from pydantic import BaseModel


# -------------------------
# REQUEST MODEL
# -------------------------

class User(BaseModel):
    name: str
    email: str


# -------------------------
# RESPONSE MODELS
# -------------------------

class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class MessageResponse(BaseModel):
    message: str