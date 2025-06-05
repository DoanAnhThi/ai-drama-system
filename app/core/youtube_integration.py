from typing import Dict, List, Optional
import os
import logging
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeIntegration:
    """YouTube integration system for AI drama series"""
    
    def __init__(self):
        self.youtube = self.initialize_youtube_client()
        self.channel_memory = ChannelMemory()
    
    def initialize_youtube_client(self):
        """Initialize YouTube API client"""
        try:
            credentials = self.get_credentials()
            return build('youtube', 'v3', credentials=credentials)
        except Exception as e:
            logger.error(f"Failed to initialize YouTube client: {str(e)}")
            raise
    
    def get_credentials(self) -> Credentials:
        """Get YouTube API credentials"""
        try:
            creds = None
            token_path = 'token.json'
            
            # Load existing credentials
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_info(
                    json.loads(open(token_path).read()),
                    ['https://www.googleapis.com/auth/youtube']
                )
            
            # Refresh or create new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'client_secrets.json',
                        ['https://www.googleapis.com/auth/youtube']
                    )
                    creds = flow.run_local_server(port=0)
                
                # Save credentials
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            
            return creds
            
        except Exception as e:
            logger.error(f"Failed to get credentials: {str(e)}")
            raise
    
    def upload_episode(self, video_data: Dict, series_data: Dict) -> Dict:
        """Upload episode to YouTube"""
        try:
            # Prepare video metadata
            video_metadata = self.prepare_video_metadata(video_data, series_data)
            
            # Upload video file
            video_id = self.upload_video_file(
                video_data["video_path"],
                video_metadata
            )
            
            # Update video details
            self.update_video_details(video_id, video_metadata)
            
            # Create playlist if needed
            playlist_id = self.ensure_series_playlist(series_data)
            
            # Add video to playlist
            self.add_to_playlist(video_id, playlist_id)
            
            # Prepare upload data
            upload_data = {
                "video_id": video_id,
                "playlist_id": playlist_id,
                "title": video_metadata["title"],
                "description": video_metadata["description"],
                "tags": video_metadata["tags"],
                "published_at": datetime.utcnow().isoformat()
            }
            
            # Save to channel memory
            self.channel_memory.save_upload(upload_data)
            
            return upload_data
            
        except Exception as e:
            logger.error(f"Failed to upload episode: {str(e)}")
            raise
    
    def prepare_video_metadata(self, video_data: Dict, series_data: Dict) -> Dict:
        """Prepare video metadata for upload"""
        try:
            # Generate title
            title = f"{series_data['title']} - Episode {video_data['metadata']['episode_number']}: {video_data['metadata']['title']}"
            
            # Generate description
            description = self.generate_video_description(video_data, series_data)
            
            # Generate tags
            tags = self.generate_video_tags(video_data, series_data)
            
            return {
                "title": title,
                "description": description,
                "tags": tags,
                "category_id": "22",  # People & Blogs
                "privacy_status": "public",
                "notify_subscribers": True
            }
            
        except Exception as e:
            logger.error(f"Failed to prepare video metadata: {str(e)}")
            raise
    
    def upload_video_file(self, video_path: str, metadata: Dict) -> str:
        """Upload video file to YouTube"""
        try:
            request_body = {
                "snippet": {
                    "title": metadata["title"],
                    "description": metadata["description"],
                    "tags": metadata["tags"],
                    "categoryId": metadata["category_id"]
                },
                "status": {
                    "privacyStatus": metadata["privacy_status"],
                    "selfDeclaredMadeForKids": False
                }
            }
            
            media = MediaFileUpload(
                video_path,
                mimetype='video/mp4',
                resumable=True
            )
            
            request = self.youtube.videos().insert(
                part=",".join(request_body.keys()),
                body=request_body,
                media_body=media
            )
            
            response = request.execute()
            return response["id"]
            
        except Exception as e:
            logger.error(f"Failed to upload video file: {str(e)}")
            raise
    
    def update_video_details(self, video_id: str, metadata: Dict):
        """Update video details after upload"""
        try:
            request_body = {
                "id": video_id,
                "snippet": {
                    "title": metadata["title"],
                    "description": metadata["description"],
                    "tags": metadata["tags"],
                    "categoryId": metadata["category_id"]
                },
                "status": {
                    "privacyStatus": metadata["privacy_status"],
                    "selfDeclaredMadeForKids": False
                }
            }
            
            self.youtube.videos().update(
                part=",".join(request_body.keys()),
                body=request_body
            ).execute()
            
        except Exception as e:
            logger.error(f"Failed to update video details: {str(e)}")
            raise
    
    def ensure_series_playlist(self, series_data: Dict) -> str:
        """Ensure series playlist exists"""
        try:
            # Check if playlist exists
            playlist_id = self.channel_memory.get_playlist_id(series_data["series_id"])
            
            if not playlist_id:
                # Create new playlist
                request_body = {
                    "snippet": {
                        "title": f"{series_data['title']} - Full Series",
                        "description": series_data["description"]
                    },
                    "status": {
                        "privacyStatus": "public"
                    }
                }
                
                response = self.youtube.playlists().insert(
                    part=",".join(request_body.keys()),
                    body=request_body
                ).execute()
                
                playlist_id = response["id"]
                
                # Save playlist ID
                self.channel_memory.save_playlist(
                    series_data["series_id"],
                    playlist_id
                )
            
            return playlist_id
            
        except Exception as e:
            logger.error(f"Failed to ensure series playlist: {str(e)}")
            raise
    
    def add_to_playlist(self, video_id: str, playlist_id: str):
        """Add video to playlist"""
        try:
            request_body = {
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
            
            self.youtube.playlistItems().insert(
                part=",".join(request_body.keys()),
                body=request_body
            ).execute()
            
        except Exception as e:
            logger.error(f"Failed to add video to playlist: {str(e)}")
            raise
    
    def generate_video_description(self, video_data: Dict, series_data: Dict) -> str:
        """Generate video description"""
        try:
            description = f"""
            {video_data['metadata']['title']}
            
            Episode {video_data['metadata']['episode_number']} of {series_data['title']}
            
            {video_data['metadata']['summary']}
            
            Series Description:
            {series_data['description']}
            
            Characters in this episode:
            {', '.join(video_data['metadata']['characters'])}
            
            Locations:
            {', '.join(video_data['metadata']['locations'])}
            
            #AIDrama #AI #Drama #Series
            """
            
            return description.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate video description: {str(e)}")
            raise
    
    def generate_video_tags(self, video_data: Dict, series_data: Dict) -> List[str]:
        """Generate video tags"""
        try:
            tags = [
                "AIDrama",
                "AI",
                "Drama",
                "Series",
                series_data["title"],
                f"Episode{video_data['metadata']['episode_number']}",
                *video_data["metadata"]["characters"],
                *video_data["metadata"]["locations"]
            ]
            
            return list(set(tags))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Failed to generate video tags: {str(e)}")
            raise

class ChannelMemory:
    """Channel memory system for maintaining YouTube data"""
    
    def __init__(self):
        # Initialize database connection
        pass
    
    def save_upload(self, upload_data: Dict):
        """Save upload data to database"""
        pass
    
    def get_playlist_id(self, series_id: str) -> Optional[str]:
        """Get playlist ID for series"""
        pass
    
    def save_playlist(self, series_id: str, playlist_id: str):
        """Save playlist data to database"""
        pass 