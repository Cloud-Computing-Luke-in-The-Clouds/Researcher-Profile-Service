from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

# currently not used
class ResearchPaper(BaseModel):
    paper_title: Optional[str] = None
    paper_link: Optional[str] = None
    demo_video_link: Optional[str] = None
    project_website: Optional[str] = None

class ResearchProfile(BaseModel):
    image_url: Optional[str] = None
    google_scholar_link: Optional[str] = None
    personal_website_link: Optional[str] = None
    organization: Optional[str] = None
    title: Optional[str] = None