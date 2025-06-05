from typing import Dict, List, Optional
import openai
import json
import logging
from datetime import datetime
import os
from dotenv import load_dotenv
import moviepy.editor as mp
from elevenlabs import generate, set_api_key
import ffmpeg

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoGenerator:
    """Video generation system for AI drama series"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        set_api_key(os.getenv("ELEVENLABS_API_KEY"))
        self.video_memory = VideoMemory()
    
    def generate_episode_video(self, script: Dict, characters: Dict) -> Dict:
        """Generate video for an episode"""
        try:
            # Generate scene descriptions
            scene_descriptions = self.generate_scene_descriptions(script)
            
            # Generate character visuals
            character_visuals = self.generate_character_visuals(characters)
            
            # Generate background visuals
            background_visuals = self.generate_background_visuals(scene_descriptions)
            
            # Generate character voices
            character_voices = self.generate_character_voices(script, characters)
            
            # Compose video scenes
            video_scenes = self.compose_video_scenes(
                scene_descriptions,
                character_visuals,
                background_visuals,
                character_voices
            )
            
            # Add music and sound effects
            audio_enhanced_scenes = self.add_audio_effects(video_scenes)
            
            # Render final video
            final_video = self.render_final_video(audio_enhanced_scenes)
            
            # Prepare video data
            video_data = {
                "video_path": final_video,
                "duration": self.get_video_duration(final_video),
                "scenes": video_scenes,
                "metadata": {
                    "title": script["episode_title"],
                    "characters": list(characters.keys()),
                    "locations": [scene["location"] for scene in script["scenes"]],
                    "created_at": datetime.utcnow().isoformat()
                }
            }
            
            # Save to video memory
            self.video_memory.save_video(video_data)
            
            return video_data
            
        except Exception as e:
            logger.error(f"Failed to generate episode video: {str(e)}")
            raise
    
    def generate_scene_descriptions(self, script: Dict) -> List[Dict]:
        """Generate detailed scene descriptions"""
        try:
            prompt = self.create_scene_description_prompt(script)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional scene director."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            descriptions = json.loads(response.choices[0].message.content)
            return self.validate_and_format_scene_descriptions(descriptions)
            
        except Exception as e:
            logger.error(f"Failed to generate scene descriptions: {str(e)}")
            raise
    
    def generate_character_visuals(self, characters: Dict) -> Dict:
        """Generate character visual representations"""
        try:
            prompt = self.create_character_visual_prompt(characters)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional character designer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            visuals = json.loads(response.choices[0].message.content)
            return self.validate_and_format_character_visuals(visuals)
            
        except Exception as e:
            logger.error(f"Failed to generate character visuals: {str(e)}")
            raise
    
    def generate_background_visuals(self, scene_descriptions: List[Dict]) -> Dict:
        """Generate background visuals for scenes"""
        try:
            prompt = self.create_background_visual_prompt(scene_descriptions)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional set designer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            visuals = json.loads(response.choices[0].message.content)
            return self.validate_and_format_background_visuals(visuals)
            
        except Exception as e:
            logger.error(f"Failed to generate background visuals: {str(e)}")
            raise
    
    def generate_character_voices(self, script: Dict, characters: Dict) -> Dict:
        """Generate character voice lines"""
        try:
            voice_lines = {}
            
            for scene in script["scenes"]:
                for dialogue in scene["dialogues"]:
                    character = dialogue["character"]
                    text = dialogue["text"]
                    emotion = dialogue["emotion"]
                    
                    # Generate voice with appropriate emotion
                    voice = generate(
                        text=text,
                        voice=characters[character]["voice_id"],
                        model="eleven_monolingual_v1"
                    )
                    
                    if character not in voice_lines:
                        voice_lines[character] = []
                    
                    voice_lines[character].append({
                        "text": text,
                        "emotion": emotion,
                        "audio": voice
                    })
            
            return voice_lines
            
        except Exception as e:
            logger.error(f"Failed to generate character voices: {str(e)}")
            raise
    
    def compose_video_scenes(self, scene_descriptions: List[Dict], character_visuals: Dict, background_visuals: Dict, character_voices: Dict) -> List[Dict]:
        """Compose video scenes from components"""
        try:
            video_scenes = []
            
            for scene in scene_descriptions:
                # Create scene video
                scene_video = self.create_scene_video(
                    scene,
                    character_visuals,
                    background_visuals,
                    character_voices
                )
                
                video_scenes.append({
                    "scene_number": scene["scene_number"],
                    "video": scene_video,
                    "duration": self.get_video_duration(scene_video)
                })
            
            return video_scenes
            
        except Exception as e:
            logger.error(f"Failed to compose video scenes: {str(e)}")
            raise
    
    def add_audio_effects(self, video_scenes: List[Dict]) -> List[Dict]:
        """Add music and sound effects to scenes"""
        try:
            enhanced_scenes = []
            
            for scene in video_scenes:
                # Add background music
                scene_with_music = self.add_background_music(scene)
                
                # Add sound effects
                scene_with_effects = self.add_sound_effects(scene_with_music)
                
                enhanced_scenes.append(scene_with_effects)
            
            return enhanced_scenes
            
        except Exception as e:
            logger.error(f"Failed to add audio effects: {str(e)}")
            raise
    
    def render_final_video(self, scenes: List[Dict]) -> str:
        """Render final video from scenes"""
        try:
            # Concatenate scene videos
            final_video = mp.concatenate_videoclips([
                mp.VideoFileClip(scene["video"])
                for scene in scenes
            ])
            
            # Add transitions
            final_video = self.add_transitions(final_video)
            
            # Export final video
            output_path = f"output/episode_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.mp4"
            final_video.write_videofile(output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to render final video: {str(e)}")
            raise
    
    def create_scene_description_prompt(self, script: Dict) -> str:
        """Create prompt for scene description generation"""
        return f"""
        Create detailed scene descriptions for a drama episode.
        
        Episode Title: {script['episode_title']}
        
        Scenes:
        {json.dumps(script['scenes'], indent=2)}
        
        Requirements:
        1. Create detailed descriptions for each scene
        2. Include:
           - Camera angles
           - Lighting
           - Character positioning
           - Action sequences
           - Emotional atmosphere
        
        Format the response as a JSON array:
        [
            {{
                "scene_number": integer,
                "camera_angles": ["string"],
                "lighting": "string",
                "character_positions": {{
                    "character_name": "position description"
                }},
                "actions": ["string"],
                "atmosphere": "string"
            }}
        ]
        """
    
    def create_character_visual_prompt(self, characters: Dict) -> str:
        """Create prompt for character visual generation"""
        return f"""
        Create visual descriptions for drama characters.
        
        Characters:
        {json.dumps(characters, indent=2)}
        
        Requirements:
        1. Create visual descriptions for each character
        2. Include:
           - Physical appearance
           - Clothing style
           - Facial expressions
           - Body language
           - Visual effects
        
        Format the response as a JSON object:
        {{
            "character_name": {{
                "appearance": "string",
                "clothing": "string",
                "expressions": ["string"],
                "body_language": "string",
                "effects": ["string"]
            }}
        }}
        """
    
    def create_background_visual_prompt(self, scene_descriptions: List[Dict]) -> str:
        """Create prompt for background visual generation"""
        return f"""
        Create background visual descriptions for drama scenes.
        
        Scene Descriptions:
        {json.dumps(scene_descriptions, indent=2)}
        
        Requirements:
        1. Create visual descriptions for each scene background
        2. Include:
           - Setting details
           - Props
           - Lighting
           - Atmosphere
           - Special effects
        
        Format the response as a JSON object:
        {{
            "scene_number": {{
                "setting": "string",
                "props": ["string"],
                "lighting": "string",
                "atmosphere": "string",
                "effects": ["string"]
            }}
        }}
        """
    
    def validate_and_format_scene_descriptions(self, descriptions: List[Dict]) -> List[Dict]:
        """Validate and format scene descriptions"""
        required_fields = [
            "scene_number", "camera_angles", "lighting",
            "character_positions", "actions", "atmosphere"
        ]
        
        for description in descriptions:
            for field in required_fields:
                if field not in description:
                    raise ValueError(f"Missing required field in scene description: {field}")
        
        return descriptions
    
    def validate_and_format_character_visuals(self, visuals: Dict) -> Dict:
        """Validate and format character visuals"""
        required_fields = [
            "appearance", "clothing", "expressions",
            "body_language", "effects"
        ]
        
        for character, visual in visuals.items():
            for field in required_fields:
                if field not in visual:
                    raise ValueError(f"Missing required field in character visual: {field}")
        
        return visuals
    
    def validate_and_format_background_visuals(self, visuals: Dict) -> Dict:
        """Validate and format background visuals"""
        required_fields = [
            "setting", "props", "lighting",
            "atmosphere", "effects"
        ]
        
        for scene, visual in visuals.items():
            for field in required_fields:
                if field not in visual:
                    raise ValueError(f"Missing required field in background visual: {field}")
        
        return visuals
    
    def get_video_duration(self, video_path: str) -> float:
        """Get duration of a video file"""
        try:
            probe = ffmpeg.probe(video_path)
            return float(probe['streams'][0]['duration'])
        except Exception as e:
            logger.error(f"Failed to get video duration: {str(e)}")
            raise

class VideoMemory:
    """Video memory system for maintaining video data"""
    
    def __init__(self):
        # Initialize database connection
        pass
    
    def save_video(self, video_data: Dict):
        """Save video data to database"""
        pass
    
    def get_video(self, video_id: str) -> Dict:
        """Get video data from database"""
        pass
    
    def update_video_metadata(self, video_id: str, metadata: Dict):
        """Update video metadata"""
        pass 