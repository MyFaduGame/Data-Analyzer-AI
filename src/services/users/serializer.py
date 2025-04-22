
from pydantic import BaseModel
from typing import Optional


# Input model
class QuestionInput(BaseModel):
    key : str
    question : Optional[str] = None