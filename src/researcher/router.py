from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseAdditionalFields
from src.researcher.schemas import ResearchProfile
from sqlalchemy.orm import Session
from . import service
from src.database import get_db
import time
import jwt

router = APIRouter()
security = HTTPBearer()
SECRET_KEY = "test"  # Your secret key

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# Test endpoint
@router.get("/test")
async def test_endpoint(token_data: dict = Depends(verify_token)):
    """Test endpoint to verify API is running and JWT auth is working"""
    return {
        "status": "success", 
        "message": "API is running with JWT auth",
        "token_data": token_data
    }

@router.get("/researchers", response_model=CustomizedPage[
    Page[ResearchProfile],
    UseAdditionalFields(
        link=str,
    ),
])
async def get_all_researchers(db: Session = Depends(get_db)):
    
    profiles = service.get_all_research_profiles(db)
    
    link_header = []
    page = profiles.page
    size = profiles.size
    pages = profiles.pages

    if page > 1:
        prev_page = page - 1
        link_header.append(
            f'<{router.url_path_for("get_all_researchers")}?page={prev_page}&size={size}>; rel="prev"'
        )

    if page < pages:
        next_page = page + 1
        link_header.append(
            f'<{router.url_path_for("get_all_researchers")}?page={next_page}&size={size}>; rel="next"'
        )

    if link_header:
        profiles.link = ", ".join(link_header)

    return profiles

# Add token verification to other endpoints...
@router.get("/researcher/{user_id}")
async def get_researcher_by_id(
    user_id: str,
    db: Session = Depends(get_db)
):
    researcher = service.get_research_profile_by_id(db, user_id)
    if not researcher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Researcher profile with ID {user_id} not found"
        )
    return researcher

@router.delete("/researcher/{user_id}")
async def delete_researcher_by_id(
    user_id: str,
    db: Session = Depends(get_db)
):
    result = service.delete_research_profile_by_id(db, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Researcher profile with ID {user_id} not found"
        )
    return {"message": "Profile deleted successfully"}

@router.post("/researcher", status_code=201)
async def creat_new_researcher(research_profile: ResearchProfile,
                               db: Session = Depends(get_db)):
    
    response = service.create_research_profile(db, research_profile)
    return {'link': f"{router.url_path_for('get_researcher_by_id', user_id = response.user_id)}; rel='self'"}

@router.post("/background_add_researcher", status_code=202)
async def background_add_new_researcher(research_profile: ResearchProfile, background_tasks: BackgroundTasks,
                               db: Session = Depends(get_db)):
    
    background_tasks.add_task(time.sleep, 30)
    background_tasks.add_task(service.create_research_profile, db, research_profile)
    return {'message': 'Research profile creation in progress.'}


@router.put("/researcher/{user_id}")
async def update_researcher(
    user_id: str,
    researcher: ResearchProfile,
    db: Session = Depends(get_db)
):
    """Update a researcher's information"""
    updated_researcher = service.update_research_profile(
        db, 
        user_id, 
        researcher.model_dump(exclude_unset=True)
    )
    if not updated_researcher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Researcher profile with ID {user_id} not found"
        )
    return updated_researcher
