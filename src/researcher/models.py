from sqlalchemy import Column, Integer, String, Text, JSON
from src.database import Base

class ResearchProfile(Base):
    __tablename__ = "ResearchProfile"
    user_id = Column(String(255), primary_key=True)
    image_url = Column(String(255), nullable=True)
    google_scholar_link = Column(String(255), nullable=True)
    personal_website_link = Column(String(255), nullable=True)
    organization = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)