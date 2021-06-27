from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    username: Optional[str] = None
    message: str
    public_key: Optional[dict] = None
    private_key: Optional[dict] = None

