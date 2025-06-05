from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class DramaSeries(Base):
    """Drama series model"""
    __tablename__ = "drama_series"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    genre = Column(String(50))
    description = Column(Text)
    total_episodes = Column(Integer, default=100)
    status = Column(String(20), default='active')
    series_plot = Column(JSON)  # Overall series plot
    story_arc = Column(JSON)    # Story arc information
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    episodes = relationship("Episode", back_populates="series")
    characters = relationship("Character", back_populates="series")

class Episode(Base):
    """Episode model"""
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("drama_series.id"))
    episode_number = Column(Integer, nullable=False)
    title = Column(String(200))
    script = Column(JSON)
    summary = Column(Text)
    key_events = Column(JSON)              # Major events
    character_developments = Column(JSON)   # Character developments
    relationship_changes = Column(JSON)     # Relationship changes
    unresolved_plots = Column(JSON)        # Unresolved plots
    cliffhanger = Column(Text)             # Next episode preview
    status = Column(String(20), default='pending')
    youtube_id = Column(String(50))
    youtube_url = Column(String(500))
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime)

    # Relationships
    series = relationship("DramaSeries", back_populates="episodes")
    character_states = relationship("CharacterState", back_populates="episode")

class Character(Base):
    """Character model"""
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("drama_series.id"))
    name = Column(String(100), nullable=False)
    role = Column(String(50))
    age = Column(Integer)
    occupation = Column(String(100))
    personality = Column(JSON)
    background = Column(Text)
    goals = Column(JSON)
    secrets = Column(JSON)
    avatar_id = Column(String(100))
    voice_id = Column(String(100))
    profile = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    series = relationship("DramaSeries", back_populates="characters")
    states = relationship("CharacterState", back_populates="character")

class CharacterState(Base):
    """Character state tracking model"""
    __tablename__ = "character_states"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("drama_series.id"))
    episode_id = Column(Integer, ForeignKey("episodes.id"))
    character_name = Column(String(100))
    emotional_state = Column(String(50))
    location = Column(String(100))
    active_goals = Column(JSON)
    resolved_goals = Column(JSON)
    new_traits = Column(JSON)
    current_situation = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    episode = relationship("Episode", back_populates="character_states")
    character = relationship("Character", back_populates="states") 