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

class CharacterGenerator:
    """Character generation system for AI drama series"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.character_memory = CharacterMemory()
    
    def create_character_profiles(self, series_config: Dict) -> List[Dict]:
        """Create character profiles for a series"""
        try:
            # Generate main characters
            main_characters = self.generate_main_characters(series_config)
            
            # Generate supporting characters
            supporting_characters = self.generate_supporting_characters(
                series_config,
                main_characters
            )
            
            # Generate character relationships
            relationships = self.generate_character_relationships(
                main_characters,
                supporting_characters
            )
            
            # Create character arcs
            character_arcs = self.create_character_arcs(
                main_characters,
                series_config["total_episodes"]
            )
            
            # Prepare character data
            characters = {
                "main_characters": main_characters,
                "supporting_characters": supporting_characters,
                "relationships": relationships,
                "character_arcs": character_arcs
            }
            
            # Save to character memory
            self.character_memory.save_characters(series_config["series_id"], characters)
            
            return characters
            
        except Exception as e:
            logger.error(f"Failed to create character profiles: {str(e)}")
            raise
    
    def generate_main_characters(self, series_config: Dict) -> List[Dict]:
        """Generate main character profiles"""
        try:
            prompt = self.create_main_character_prompt(series_config)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional character writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            characters = json.loads(response.choices[0].message.content)
            return self.validate_and_format_characters(characters)
            
        except Exception as e:
            logger.error(f"Failed to generate main characters: {str(e)}")
            raise
    
    def generate_supporting_characters(self, series_config: Dict, main_characters: List[Dict]) -> List[Dict]:
        """Generate supporting character profiles"""
        try:
            prompt = self.create_supporting_character_prompt(series_config, main_characters)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional character writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            characters = json.loads(response.choices[0].message.content)
            return self.validate_and_format_characters(characters)
            
        except Exception as e:
            logger.error(f"Failed to generate supporting characters: {str(e)}")
            raise
    
    def generate_character_relationships(self, main_characters: List[Dict], supporting_characters: List[Dict]) -> Dict:
        """Generate character relationships"""
        try:
            prompt = self.create_relationship_prompt(main_characters, supporting_characters)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional relationship writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            relationships = json.loads(response.choices[0].message.content)
            return self.validate_and_format_relationships(relationships)
            
        except Exception as e:
            logger.error(f"Failed to generate character relationships: {str(e)}")
            raise
    
    def create_character_arcs(self, characters: List[Dict], total_episodes: int) -> Dict:
        """Create character development arcs"""
        try:
            prompt = self.create_character_arc_prompt(characters, total_episodes)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional character arc writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            arcs = json.loads(response.choices[0].message.content)
            return self.validate_and_format_arcs(arcs)
            
        except Exception as e:
            logger.error(f"Failed to create character arcs: {str(e)}")
            raise
    
    def create_main_character_prompt(self, series_config: Dict) -> str:
        """Create prompt for main character generation"""
        return f"""
        Create main character profiles for a {series_config['genre']} drama series titled "{series_config['title']}".
        
        Requirements:
        1. Create 3-5 main characters
        2. Each character should have:
           - Name
           - Age
           - Occupation
           - Personality traits
           - Background story
           - Goals and motivations
           - Internal conflicts
           - External conflicts
           - Character arc potential
        
        Format the response as a JSON array of character objects:
        [
            {{
                "name": "string",
                "age": integer,
                "occupation": "string",
                "personality": ["string"],
                "background": "string",
                "goals": ["string"],
                "internal_conflicts": ["string"],
                "external_conflicts": ["string"],
                "arc_potential": "string"
            }}
        ]
        """
    
    def create_supporting_character_prompt(self, series_config: Dict, main_characters: List[Dict]) -> str:
        """Create prompt for supporting character generation"""
        return f"""
        Create supporting character profiles for a {series_config['genre']} drama series titled "{series_config['title']}".
        
        Main Characters:
        {json.dumps(main_characters, indent=2)}
        
        Requirements:
        1. Create 5-8 supporting characters
        2. Each character should have:
           - Name
           - Age
           - Occupation
           - Relationship to main characters
           - Personality traits
           - Background story
           - Role in the story
        
        Format the response as a JSON array of character objects:
        [
            {{
                "name": "string",
                "age": integer,
                "occupation": "string",
                "relationships": {{
                    "main_character_name": "relationship description"
                }},
                "personality": ["string"],
                "background": "string",
                "story_role": "string"
            }}
        ]
        """
    
    def create_relationship_prompt(self, main_characters: List[Dict], supporting_characters: List[Dict]) -> str:
        """Create prompt for relationship generation"""
        return f"""
        Create character relationships for a drama series.
        
        Main Characters:
        {json.dumps(main_characters, indent=2)}
        
        Supporting Characters:
        {json.dumps(supporting_characters, indent=2)}
        
        Requirements:
        1. Define relationships between all characters
        2. Include:
           - Relationship type
           - History
           - Current status
           - Potential conflicts
           - Development opportunities
        
        Format the response as a JSON object:
        {{
            "relationships": [
                {{
                    "character1": "string",
                    "character2": "string",
                    "type": "string",
                    "history": "string",
                    "current_status": "string",
                    "conflicts": ["string"],
                    "development": "string"
                }}
            ]
        }}
        """
    
    def create_character_arc_prompt(self, characters: List[Dict], total_episodes: int) -> str:
        """Create prompt for character arc generation"""
        return f"""
        Create character development arcs for a {total_episodes}-episode drama series.
        
        Characters:
        {json.dumps(characters, indent=2)}
        
        Requirements:
        1. Create development arcs for each character
        2. Include:
           - Starting point
           - Key development moments
           - Character growth
           - Final state
           - Episode milestones
        
        Format the response as a JSON object:
        {{
            "character_arcs": {{
                "character_name": {{
                    "starting_point": "string",
                    "development_moments": [
                        {{
                            "episode": integer,
                            "description": "string"
                        }}
                    ],
                    "growth": "string",
                    "final_state": "string"
                }}
            }}
        }}
        """
    
    def validate_and_format_characters(self, characters: List[Dict]) -> List[Dict]:
        """Validate and format character profiles"""
        required_fields = [
            "name", "age", "occupation", "personality",
            "background", "goals", "internal_conflicts",
            "external_conflicts", "arc_potential"
        ]
        
        for character in characters:
            for field in required_fields:
                if field not in character:
                    raise ValueError(f"Missing required field in character: {field}")
        
        return characters
    
    def validate_and_format_relationships(self, relationships: Dict) -> Dict:
        """Validate and format character relationships"""
        required_fields = [
            "character1", "character2", "type",
            "history", "current_status", "conflicts",
            "development"
        ]
        
        for relationship in relationships["relationships"]:
            for field in required_fields:
                if field not in relationship:
                    raise ValueError(f"Missing required field in relationship: {field}")
        
        return relationships
    
    def validate_and_format_arcs(self, arcs: Dict) -> Dict:
        """Validate and format character arcs"""
        required_fields = [
            "starting_point", "development_moments",
            "growth", "final_state"
        ]
        
        for character, arc in arcs["character_arcs"].items():
            for field in required_fields:
                if field not in arc:
                    raise ValueError(f"Missing required field in character arc: {field}")
        
        return arcs

class CharacterMemory:
    """Character memory system for maintaining character data"""
    
    def __init__(self):
        # Initialize database connection
        pass
    
    def save_characters(self, series_id: str, characters: Dict):
        """Save character data to database"""
        pass
    
    def get_characters(self, series_id: str) -> Dict:
        """Get character data from database"""
        pass
    
    def update_character_state(self, series_id: str, character_name: str, state: Dict):
        """Update character state"""
        pass 