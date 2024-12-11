import asyncio
from typing import List, AsyncGenerator
import strawberry
from strawberry import Schema

from src.researcher.models import ResearchProfile as ResearchProfileModel
from src.database import get_db

@strawberry.type
class ResearchProfileType:
    user_id: str
    image_url: str
    google_scholar_link: str
    personal_website_link: str
    organization: str
    title: str

@strawberry.type
class Query:
    @strawberry.field
    async def research_profile(self) -> List[ResearchProfileType]:
        db = next(get_db())
        research_profiles = db.query(ResearchProfileModel).all()
        return [ResearchProfileType(user_id = r.user_id, image_url=r.image_url, google_scholar_link=r.google_scholar_link, personal_website_link=r.personal_website_link, organization=r.organization, title=r.title) for r in research_profiles]

schema = strawberry.Schema(Query)