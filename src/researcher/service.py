from sqlalchemy import select
from sqlalchemy.orm import Session
from src.researcher.models import ResearchProfile
from fastapi_pagination.ext.sqlalchemy import paginate

def get_research_profile_by_id(db: Session, user_id: str):
    return (db.query(ResearchProfile)
            .filter(ResearchProfile.user_id == user_id).first())

def get_all_research_profiles(db: Session, skip: int = 0, limit: int = 100):
    return paginate(db, select(ResearchProfile).order_by(ResearchProfile.user_id), additional_data={
            "link": ""
        })

def create_research_profile(db: Session, research_profile: ResearchProfile):
    new_research_profile = ResearchProfile(
       user_id=research_profile.user_id,
       google_scholar_link=research_profile.google_scholar_link,
       personal_website_link=research_profile.personal_website_link,
       organization=research_profile.organization,
       title=research_profile.title,
       image_url=research_profile.image_url
    )
    db.add(new_research_profile)
    db.commit()
    db.refresh(new_research_profile)
    return new_research_profile

def delete_research_profile_by_id(db: Session, user_id: str):
    """Delete a researcher profile by ID"""
    researcher = (db.query(ResearchProfile)
                 .filter(ResearchProfile.user_id == user_id).first())
    if researcher:
        db.delete(researcher)
        db.commit()
        return True
    return False

def update_research_profile(db: Session, user_id: str, update_data: dict):
    """Update researcher profile information"""
    researcher = get_research_profile_by_id(db, user_id)
    if not researcher:
        return None
    
    for key, value in update_data.items():
        if hasattr(researcher, key):
            setattr(researcher, key, value)
    
    db.commit()
    db.refresh(researcher)
    return researcher