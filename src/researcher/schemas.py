from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

class ResearchProfile(BaseModel):
    user_id: Optional[str] = None
    image_url: Optional[str] = None
    google_scholar_link: Optional[str] = None
    personal_website_link: Optional[str] = None
    organization: Optional[str] = None
    title: Optional[str] = None