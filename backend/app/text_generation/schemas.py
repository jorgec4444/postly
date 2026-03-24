from pydantic import BaseModel
from typing import Optional

class SaveGenerationRequest(BaseModel):
    original_text: str
    selected_text: str
    style: str
    client_id: Optional[int] = None