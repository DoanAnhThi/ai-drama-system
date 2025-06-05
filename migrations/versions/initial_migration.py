"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-03-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create series table
    op.create_table(
        'series',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('genre', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('total_episodes', sa.Integer, nullable=False),
        sa.Column('target_audience', sa.String(100), nullable=False),
        sa.Column('tone', sa.String(100), nullable=False),
        sa.Column('themes', postgresql.JSON, nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # Create episodes table
    op.create_table(
        'episodes',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('series_id', sa.String(50), sa.ForeignKey('series.id'), nullable=False),
        sa.Column('episode_number', sa.Integer, nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('script', postgresql.JSON, nullable=False),
        sa.Column('summary', sa.Text, nullable=False),
        sa.Column('key_events', postgresql.JSON, nullable=False),
        sa.Column('character_developments', postgresql.JSON, nullable=False),
        sa.Column('relationship_changes', postgresql.JSON, nullable=False),
        sa.Column('unresolved_plots', postgresql.JSON, nullable=False),
        sa.Column('cliffhanger', sa.Text, nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # Create characters table
    op.create_table(
        'characters',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('series_id', sa.String(50), sa.ForeignKey('series.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('age', sa.Integer, nullable=False),
        sa.Column('occupation', sa.String(100), nullable=False),
        sa.Column('personality', postgresql.JSON, nullable=False),
        sa.Column('background', sa.Text, nullable=False),
        sa.Column('goals', postgresql.JSON, nullable=False),
        sa.Column('secrets', postgresql.JSON, nullable=False),
        sa.Column('avatar_id', sa.String(100), nullable=True),
        sa.Column('voice_id', sa.String(100), nullable=True),
        sa.Column('profile', postgresql.JSON, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # Create character_states table
    op.create_table(
        'character_states',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('series_id', sa.String(50), sa.ForeignKey('series.id'), nullable=False),
        sa.Column('episode_id', sa.String(50), sa.ForeignKey('episodes.id'), nullable=False),
        sa.Column('character_id', sa.String(50), sa.ForeignKey('characters.id'), nullable=False),
        sa.Column('emotional_state', sa.String(100), nullable=False),
        sa.Column('location', sa.String(200), nullable=False),
        sa.Column('active_goals', postgresql.JSON, nullable=False),
        sa.Column('resolved_goals', postgresql.JSON, nullable=False),
        sa.Column('new_traits', postgresql.JSON, nullable=False),
        sa.Column('current_situation', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # Create videos table
    op.create_table(
        'videos',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('episode_id', sa.String(50), sa.ForeignKey('episodes.id'), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('duration', sa.Integer, nullable=False),
        sa.Column('scenes', postgresql.JSON, nullable=False),
        sa.Column('metadata', postgresql.JSON, nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='processing'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # Create youtube_data table
    op.create_table(
        'youtube_data',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('series_id', sa.String(50), sa.ForeignKey('series.id'), nullable=False),
        sa.Column('channel_id', sa.String(100), nullable=False),
        sa.Column('playlist_id', sa.String(100), nullable=False),
        sa.Column('channel_name', sa.String(200), nullable=False),
        sa.Column('channel_description', sa.Text, nullable=False),
        sa.Column('subscriber_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('view_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('video_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # Create youtube_uploads table
    op.create_table(
        'youtube_uploads',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('video_id', sa.String(50), sa.ForeignKey('videos.id'), nullable=False),
        sa.Column('channel_id', sa.String(50), sa.ForeignKey('youtube_data.id'), nullable=False),
        sa.Column('youtube_video_id', sa.String(100), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('tags', postgresql.JSON, nullable=False),
        sa.Column('view_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('like_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('comment_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('published_at', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # Create indexes
    op.create_index('ix_series_title', 'series', ['title'])
    op.create_index('ix_episodes_series_id', 'episodes', ['series_id'])
    op.create_index('ix_episodes_episode_number', 'episodes', ['episode_number'])
    op.create_index('ix_characters_series_id', 'characters', ['series_id'])
    op.create_index('ix_character_states_episode_id', 'character_states', ['episode_id'])
    op.create_index('ix_character_states_character_id', 'character_states', ['character_id'])
    op.create_index('ix_videos_episode_id', 'videos', ['episode_id'])
    op.create_index('ix_youtube_data_series_id', 'youtube_data', ['series_id'])
    op.create_index('ix_youtube_uploads_video_id', 'youtube_uploads', ['video_id'])
    op.create_index('ix_youtube_uploads_channel_id', 'youtube_uploads', ['channel_id'])

def downgrade():
    # Drop indexes
    op.drop_index('ix_youtube_uploads_channel_id')
    op.drop_index('ix_youtube_uploads_video_id')
    op.drop_index('ix_youtube_data_series_id')
    op.drop_index('ix_videos_episode_id')
    op.drop_index('ix_character_states_character_id')
    op.drop_index('ix_character_states_episode_id')
    op.drop_index('ix_characters_series_id')
    op.drop_index('ix_episodes_episode_number')
    op.drop_index('ix_episodes_series_id')
    op.drop_index('ix_series_title')
    
    # Drop tables
    op.drop_table('youtube_uploads')
    op.drop_table('youtube_data')
    op.drop_table('videos')
    op.drop_table('character_states')
    op.drop_table('characters')
    op.drop_table('episodes')
    op.drop_table('series') 