from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Series(Base):
    """Drama series model"""
    __tablename__ = "series"
    
    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    genre = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    total_episodes = Column(Integer, nullable=False)
    target_audience = Column(String(100), nullable=False)
    tone = Column(String(100), nullable=False)
    themes = Column(JSON, nullable=False)
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    episodes = relationship("Episode", back_populates="series")
    characters = relationship("Character", back_populates="series")
    youtube_data = relationship("YouTubeData", back_populates="series", uselist=False)

class Episode(Base):
    """Episode model"""
    __tablename__ = "episodes"
    
    id = Column(String(50), primary_key=True)
    series_id = Column(String(50), ForeignKey("series.id"), nullable=False)
    episode_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    script = Column(JSON, nullable=False)
    summary = Column(Text, nullable=False)
    key_events = Column(JSON, nullable=False)
    character_developments = Column(JSON, nullable=False)
    relationship_changes = Column(JSON, nullable=False)
    unresolved_plots = Column(JSON, nullable=False)
    cliffhanger = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="draft")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    series = relationship("Series", back_populates="episodes")
    video = relationship("Video", back_populates="episode", uselist=False)
    character_states = relationship("CharacterState", back_populates="episode")

class Character(Base):
    """Character model"""
    __tablename__ = "characters"
    
    id = Column(String(50), primary_key=True)
    series_id = Column(String(50), ForeignKey("series.id"), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)  # main or supporting
    age = Column(Integer, nullable=False)
    occupation = Column(String(100), nullable=False)
    personality = Column(JSON, nullable=False)
    background = Column(Text, nullable=False)
    goals = Column(JSON, nullable=False)
    secrets = Column(JSON, nullable=False)
    avatar_id = Column(String(100), nullable=True)
    voice_id = Column(String(100), nullable=True)
    profile = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    series = relationship("Series", back_populates="characters")
    states = relationship("CharacterState", back_populates="character")

class CharacterState(Base):
    """Character state model for tracking development"""
    __tablename__ = "character_states"
    
    id = Column(String(50), primary_key=True)
    series_id = Column(String(50), ForeignKey("series.id"), nullable=False)
    episode_id = Column(String(50), ForeignKey("episodes.id"), nullable=False)
    character_id = Column(String(50), ForeignKey("characters.id"), nullable=False)
    emotional_state = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    active_goals = Column(JSON, nullable=False)
    resolved_goals = Column(JSON, nullable=False)
    new_traits = Column(JSON, nullable=False)
    current_situation = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    episode = relationship("Episode", back_populates="character_states")
    character = relationship("Character", back_populates="states")

class Video(Base):
    """Video model"""
    __tablename__ = "videos"
    
    id = Column(String(50), primary_key=True)
    episode_id = Column(String(50), ForeignKey("episodes.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    duration = Column(Integer, nullable=False)  # in seconds
    scenes = Column(JSON, nullable=False)
    metadata = Column(JSON, nullable=False)
    status = Column(String(50), nullable=False, default="processing")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    episode = relationship("Episode", back_populates="video")
    youtube_upload = relationship("YouTubeUpload", back_populates="video", uselist=False)

class YouTubeData(Base):
    """YouTube channel data model"""
    __tablename__ = "youtube_data"
    
    id = Column(String(50), primary_key=True)
    series_id = Column(String(50), ForeignKey("series.id"), nullable=False)
    channel_id = Column(String(100), nullable=False)
    playlist_id = Column(String(100), nullable=False)
    channel_name = Column(String(200), nullable=False)
    channel_description = Column(Text, nullable=False)
    subscriber_count = Column(Integer, nullable=False, default=0)
    view_count = Column(Integer, nullable=False, default=0)
    video_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    series = relationship("Series", back_populates="youtube_data")
    uploads = relationship("YouTubeUpload", back_populates="channel")

class YouTubeUpload(Base):
    """YouTube video upload model"""
    __tablename__ = "youtube_uploads"
    
    id = Column(String(50), primary_key=True)
    video_id = Column(String(50), ForeignKey("videos.id"), nullable=False)
    channel_id = Column(String(50), ForeignKey("youtube_data.id"), nullable=False)
    youtube_video_id = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    tags = Column(JSON, nullable=False)
    view_count = Column(Integer, nullable=False, default=0)
    like_count = Column(Integer, nullable=False, default=0)
    comment_count = Column(Integer, nullable=False, default=0)
    published_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    video = relationship("Video", back_populates="youtube_upload")
    channel = relationship("YouTubeData", back_populates="uploads") 