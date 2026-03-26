from pydantic import BaseModel
from typing import Any


class UploadResponse(BaseModel):
    filename: str
    file_url: str
    file_size: int
    file_type: str
    
    model_config = {"from_attributes": True}
