from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
import logging
from ..core.script_generator import ScriptGenerator
from ..core.character_generator import CharacterGenerator
from ..core.video_generator import VideoGenerator
from ..core.youtube_integration import YouTubeIntegration
from ..database import get_db
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Initialize core components
script_generator = ScriptGenerator()
character_generator = CharacterGenerator()
video_generator = VideoGenerator()
youtube_integration = YouTubeIntegration()

# Pydantic models for request/response
class SeriesConfig(BaseModel):
    title: str
    genre: str
    description: str
    total_episodes: int
    target_audience: str
    tone: str
    themes: List[str]

class EpisodeRequest(BaseModel):
    series_id: str
    episode_number: int

class VideoRequest(BaseModel):
    series_id: str
    episode_number: int
    script: Dict

class UploadRequest(BaseModel):
    series_id: str
    episode_number: int
    video_data: Dict

# API Routes
@router.post("/series/create")
async def create_series(
    config: SeriesConfig,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new drama series"""
    try:
        # Generate series data
        series_data = script_generator.create_new_series(config.dict())
        
        # Generate character profiles
        characters = character_generator.create_character_profiles(series_data)
        
        # Store in database
        # TODO: Implement database storage
        
        return {
            "status": "success",
            "message": "Series created successfully",
            "data": {
                "series_id": series_data["series_id"],
                "title": config.title,
                "characters": characters
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to create series: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create series: {str(e)}"
        )

@router.post("/episode/generate")
async def generate_episode(
    request: EpisodeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate a new episode"""
    try:
        # Generate episode script
        script = script_generator.generate_episode_script(
            request.series_id,
            request.episode_number
        )
        
        # Store in database
        # TODO: Implement database storage
        
        return {
            "status": "success",
            "message": "Episode generated successfully",
            "data": {
                "series_id": request.series_id,
                "episode_number": request.episode_number,
                "script": script
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate episode: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate episode: {str(e)}"
        )

@router.post("/video/generate")
async def generate_video(
    request: VideoRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate video for an episode"""
    try:
        # Get character data
        characters = character_generator.get_characters(request.series_id)
        
        # Generate video
        video_data = video_generator.generate_episode_video(
            request.script,
            characters
        )
        
        # Store in database
        # TODO: Implement database storage
        
        return {
            "status": "success",
            "message": "Video generated successfully",
            "data": {
                "series_id": request.series_id,
                "episode_number": request.episode_number,
                "video_data": video_data
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate video: {str(e)}"
        )

@router.post("/video/upload")
async def upload_video(
    request: UploadRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Upload video to YouTube"""
    try:
        # Get series data
        series_data = script_generator.get_series(request.series_id)
        
        # Upload to YouTube
        upload_data = youtube_integration.upload_episode(
            request.video_data,
            series_data
        )
        
        # Store in database
        # TODO: Implement database storage
        
        return {
            "status": "success",
            "message": "Video uploaded successfully",
            "data": {
                "series_id": request.series_id,
                "episode_number": request.episode_number,
                "upload_data": upload_data
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to upload video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload video: {str(e)}"
        )

@router.get("/series/{series_id}")
async def get_series(
    series_id: str,
    db: Session = Depends(get_db)
):
    """Get series information"""
    try:
        # Get series data
        series_data = script_generator.get_series(series_id)
        
        # Get character data
        characters = character_generator.get_characters(series_id)
        
        return {
            "status": "success",
            "data": {
                "series": series_data,
                "characters": characters
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get series: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get series: {str(e)}"
        )

@router.get("/episode/{series_id}/{episode_number}")
async def get_episode(
    series_id: str,
    episode_number: int,
    db: Session = Depends(get_db)
):
    """Get episode information"""
    try:
        # Get episode data
        episode_data = script_generator.get_episode(
            series_id,
            episode_number
        )
        
        return {
            "status": "success",
            "data": episode_data
        }
        
    except Exception as e:
        logger.error(f"Failed to get episode: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get episode: {str(e)}"
        )

@router.get("/video/{series_id}/{episode_number}")
async def get_video(
    series_id: str,
    episode_number: int,
    db: Session = Depends(get_db)
):
    """Get video information"""
    try:
        # Get video data
        video_data = video_generator.get_video(
            series_id,
            episode_number
        )
        
        return {
            "status": "success",
            "data": video_data
        }
        
    except Exception as e:
        logger.error(f"Failed to get video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get video: {str(e)}"
        )

@router.get("/youtube/{series_id}")
async def get_youtube_data(
    series_id: str,
    db: Session = Depends(get_db)
):
    """Get YouTube channel data"""
    try:
        # Get channel data
        channel_data = youtube_integration.get_channel_data(series_id)
        
        return {
            "status": "success",
            "data": channel_data
        }
        
    except Exception as e:
        logger.error(f"Failed to get YouTube data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get YouTube data: {str(e)}"
        ) 