from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    user_passw: str


class DataUser(BaseModel):
    username: str
    user_passw: str