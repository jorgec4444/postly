from pydantic import BaseModel

class RateLimitStatus(BaseModel):
    allowed: bool
    used: int
    remaining: int
    limit: int
    reset_at: str