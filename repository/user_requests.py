from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRequest(BaseModel):
    first_name: str = Field(
        None, title="First Name", max_length=1000
    )
    last_name: str = Field(
        None, title="Last Name", max_length=1000
    )
    created_by: int = Field(None, title="User Id")

class UserUpdateRequest(BaseModel):
    user_id: int
    first_name: str = Field(
        None, title="User Name", max_length=1000
    )
    last_name: str = Field(
        None, title="User Name", max_length=1000
    )
    updated_by: int = Field(None, title="Updater Id")