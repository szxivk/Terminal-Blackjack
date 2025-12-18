import json
import os
import glob
import random
from typing import List, Dict, Optional, Tuple

class TriviaManager:
    def __init__(self, custom_dir: str = "questions"):
        # Resolve path relative to the current working directory or package
        self.custom_dir = os.path.abspath(custom_dir)
        
        self.general_questions = [
            {
                "question": "What fits in a minute, twice in a moment, but never in a 1000 years?",
                "options": ["The letter M", "Time", "Sand", "Water"],
                "correct_index": 0
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct_index": 1
            },
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Madrid", "Paris"],
                "correct_index": 3
            },
            {
                "question": "Who painted the Mona Lisa?",
                "options": ["Van Gogh", "Picasso", "Da Vinci", "Rembrandt"],
                "correct_index": 2
            },
            {
                "question": "What acts as the powerhouse of the cell?",
                "options": ["Nucleus", "Mitochondria", "Ribosome", "Lysosome"],
                "correct_index": 1
            },
            {
                "question": "Which element has the chemical symbol 'O'?",
                "options": ["Gold", "Silver", "Oxygen", "Iron"],
                "correct_index": 2
            },
            {
                "question": "How many continents are there?",
                "options": ["5", "6", "7", "8"],
                "correct_index": 2
            }
        ]

    def get_next_question(self, questions: List[Dict], history_indices: List[int]) -> Tuple[Dict, int]:
        """
        Get a random question that hasn't been asked recently.
        Returns (question_dict, index).
        """
        if not questions:
            return None, -1
            
        total = len(questions)
        # Don't repeat the last N questions, where N is roughly half the deck or max 5
        max_history = min(total // 2, 5)
        
        # If history is too long (should be managed by caller, but safety check)
        valid_history = history_indices[-max_history:] if max_history > 0 else []
        
        available_indices = [i for i in range(total) if i not in valid_history]
        
        # Fallback if somehow empty (shouldn't happen with logic above unless total=0)
        if not available_indices:
            available_indices = range(total)
            
        selected_idx = random.choice(available_indices)
        return questions[selected_idx], selected_idx

    def get_custom_topics(self) -> List[Tuple[str, str]]:
        """
        Scan the directory for valid JSONs.
        Returns a list of (topic_name, file_path).
        """
        topics = []
        if not os.path.exists(self.custom_dir):
            try:
                os.makedirs(self.custom_dir)
            except OSError:
                pass
                
        json_pattern = os.path.join(self.custom_dir, "*.json")
        for filepath in glob.glob(json_pattern):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Basic validation
                    if "questions" in data and isinstance(data["questions"], list):
                        topic_name = data.get("topic", os.path.basename(filepath))
                        topics.append((topic_name, filepath))
            except (json.JSONDecodeError, IOError):
                continue
                
        return topics

    def load_custom_questions(self, filepath: str) -> List[Dict]:
        """Load questions from a specific JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("questions", [])
        except Exception:
            return []
