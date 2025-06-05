from typing import Dict, List, Optional
import openai
import json
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScriptGenerator:
    """Script generation system for AI drama series"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.story_memory = StoryMemory()
        self.character_tracker = CharacterTracker()
    
    def create_new_series(self, series_config: Dict) -> Dict:
        """Create a new drama series"""
        try:
            # Generate series plot
            series_plot = self.generate_series_plot(series_config)
            
            # Create character profiles
            characters = self.create_character_profiles(series_config)
            
            # Generate episode outlines
            episode_outlines = self.generate_episode_outlines(
                series_plot,
                series_config["total_episodes"]
            )
            
            # Create story arc
            story_arc = self.create_story_arc(series_plot)
            
            # Prepare series data
            series_data = {
                "series_id": self.generate_uuid(),
                "config": series_config,
                "plot": series_plot,
                "characters": characters,
                "episode_outlines": episode_outlines,
                "story_arc": story_arc
            }
            
            # Save to story memory
            self.story_memory.save_series(series_data)
            
            return series_data
            
        except Exception as e:
            logger.error(f"Failed to create new series: {str(e)}")
            raise
    
    def generate_episode_script(self, series_id: str, episode_number: int) -> Dict:
        """Generate script for a specific episode"""
        try:
            # Load series information
            series = self.story_memory.get_series(series_id)
            
            # Get previous episodes
            previous_episodes = self.story_memory.get_previous_episodes(
                series_id,
                episode_number
            )
            
            # Build episode context
            context = self.build_episode_context(
                series,
                episode_number,
                previous_episodes
            )
            
            # Generate script
            script = self.generate_script_with_context(context)
            
            # Validate continuity
            self.validate_continuity(script, context)
            
            # Update story memory
            self.story_memory.update_episode(series_id, episode_number, script)
            
            return script
            
        except Exception as e:
            logger.error(f"Failed to generate episode script: {str(e)}")
            raise
    
    def build_episode_context(self, series: Dict, episode_num: int, previous: List) -> Dict:
        """Build context for episode generation"""
        return {
            "series_info": series["config"],
            "overall_plot": series["plot"],
            "current_episode_outline": series["episode_outlines"][episode_num - 1],
            "character_states": self.character_tracker.get_current_states(series["series_id"]),
            "previous_events": self.summarize_previous_events(previous),
            "unresolved_plots": self.get_unresolved_plots(previous),
            "relationships": self.character_tracker.get_relationship_status(series["series_id"]),
            "story_progress": self.calculate_story_progress(
                episode_num,
                series["config"]["total_episodes"]
            )
        }
    
    def generate_script_with_context(self, context: Dict) -> Dict:
        """Generate script using GPT-4 with context"""
        try:
            prompt = self.create_script_prompt(context)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional drama script writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            script = json.loads(response.choices[0].message.content)
            return self.validate_and_format_script(script)
            
        except Exception as e:
            logger.error(f"Failed to generate script: {str(e)}")
            raise
    
    def create_script_prompt(self, context: Dict) -> str:
        """Create prompt for script generation"""
        return f"""
        Create a drama script for episode {context['current_episode_outline']['episode_number']}.
        
        Series Information:
        - Title: {context['series_info']['title']}
        - Genre: {context['series_info']['genre']}
        - Total Episodes: {context['series_info']['total_episodes']}
        
        Previous Events:
        {context['previous_events']}
        
        Unresolved Plots:
        {context['unresolved_plots']}
        
        Character States:
        {json.dumps(context['character_states'], indent=2)}
        
        Current Episode Outline:
        {json.dumps(context['current_episode_outline'], indent=2)}
        
        Story Progress: {context['story_progress']}%
        
        Requirements:
        1. Maintain character consistency
        2. Advance the main plot
        3. Include character development
        4. Create engaging dialogue
        5. End with a cliffhanger
        6. Duration: 10 minutes
        
        Format the response as a JSON object with the following structure:
        {{
            "episode_title": "string",
            "summary": "string",
            "scenes": [
                {{
                    "scene_number": integer,
                    "location": "string",
                    "time": "string",
                    "dialogues": [
                        {{
                            "character": "string",
                            "text": "string",
                            "emotion": "string"
                        }}
                    ]
                }}
            ],
            "character_developments": {{
                "character_name": "development description"
            }},
            "plot_progressions": {{
                "main_plot": "progression description",
                "sub_plots": ["progression description"]
            }},
            "cliffhanger": "string"
        }}
        """
    
    def validate_and_format_script(self, script: Dict) -> Dict:
        """Validate and format the generated script"""
        required_fields = [
            "episode_title", "summary", "scenes",
            "character_developments", "plot_progressions", "cliffhanger"
        ]
        
        for field in required_fields:
            if field not in script:
                raise ValueError(f"Missing required field: {field}")
        
        return script
    
    def validate_continuity(self, script: Dict, context: Dict) -> bool:
        """Validate script continuity"""
        # Implement continuity validation logic
        return True
    
    def generate_uuid(self) -> str:
        """Generate unique ID for series"""
        return datetime.utcnow().strftime("%Y%m%d%H%M%S")
    
    def calculate_story_progress(self, current_episode: int, total_episodes: int) -> float:
        """Calculate story progress percentage"""
        return (current_episode / total_episodes) * 100

class StoryMemory:
    """Story memory system for maintaining continuity"""
    
    def __init__(self):
        # Initialize database connection
        pass
    
    def save_series(self, series_data: Dict):
        """Save series data to database"""
        pass
    
    def get_series(self, series_id: str) -> Dict:
        """Get series data from database"""
        pass
    
    def get_previous_episodes(self, series_id: str, current_episode: int) -> List[Dict]:
        """Get previous episodes data"""
        pass
    
    def update_episode(self, series_id: str, episode_number: int, script: Dict):
        """Update episode data"""
        pass

class CharacterTracker:
    """Character tracking system"""
    
    def __init__(self):
        # Initialize database connection
        pass
    
    def get_current_states(self, series_id: str) -> Dict:
        """Get current character states"""
        pass
    
    def get_relationship_status(self, series_id: str) -> Dict:
        """Get character relationship status"""
        pass 