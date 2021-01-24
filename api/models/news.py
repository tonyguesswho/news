from pydantic import BaseModel
from typing import Optional


class News(BaseModel):
    headline: str
    link: str
