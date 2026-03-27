from pydantic import BaseModel, Field, Field, field_validator


class FeedbackRequest(BaseModel):
    feedback: str = Field(..., min_length=1, max_length=2000, description="User feedback text")

    @field_validator("feedback")
    @classmethod
    def feedback_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Feedback cannot be blank")
        return v.strip()