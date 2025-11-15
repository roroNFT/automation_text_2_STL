"""Generate 3D printable object ideas using Claude API."""
import json
import anthropic
from datetime import datetime
from typing import List, Dict
from pathlib import Path
from config import Config


class IdeaGenerator:
    """Generate creative ideas for 3D printable objects using Claude."""

    def __init__(self):
        """Initialize the idea generator with Claude client."""
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.CLAUDE_MODEL

    def generate_ideas(self, num_ideas: int = 5, category: str = None) -> List[Dict]:
        """
        Generate ideas for 3D printable objects.

        Args:
            num_ideas: Number of ideas to generate
            category: Optional category filter (e.g., "practical", "decorative", "gaming")

        Returns:
            List of idea dictionaries with title, description, and metadata
        """
        category_prompt = f" in the category '{category}'" if category else ""

        prompt = f"""Generate {num_ideas} creative and practical ideas for 3D printable objects{category_prompt}.

For each idea, provide:
1. A catchy title (max 60 characters)
2. A detailed description (2-3 sentences)
3. Target audience
4. Difficulty level (beginner/intermediate/advanced)
5. Estimated print time
6. Main use case
7. Keywords for search optimization (5-7 keywords)

Focus on:
- Popular and trending items
- Practical everyday objects
- Gift-worthy items
- Organization solutions
- Gaming and hobby accessories

Format your response as a JSON array with objects containing: title, description, target_audience, difficulty, print_time, use_case, keywords

Return ONLY the JSON array, no other text."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.8,  # Higher creativity
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            ideas = json.loads(response_text)

            # Add metadata to each idea
            timestamp = datetime.now().isoformat()
            for idx, idea in enumerate(ideas):
                idea['id'] = f"{timestamp}_{idx}"
                idea['created_at'] = timestamp
                idea['status'] = 'pending'
                idea['model_generated'] = False
                idea['uploaded_printables'] = False
                idea['uploaded_makerworld'] = False

            return ideas

        except Exception as e:
            print(f"Error generating ideas: {e}")
            raise

    def save_ideas(self, ideas: List[Dict], filename: str = None) -> Path:
        """
        Save generated ideas to a JSON file.

        Args:
            ideas: List of idea dictionaries
            filename: Optional custom filename

        Returns:
            Path to the saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ideas_{timestamp}.json"

        filepath = Config.IDEAS_DIR / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(ideas, f, indent=2, ensure_ascii=False)

        print(f"Ideas saved to: {filepath}")
        return filepath

    def load_ideas(self, filename: str) -> List[Dict]:
        """Load ideas from a JSON file."""
        filepath = Config.IDEAS_DIR / filename

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_pending_ideas(self) -> List[Dict]:
        """Get all ideas that haven't been processed yet."""
        pending = []

        for filepath in Config.IDEAS_DIR.glob("*.json"):
            ideas = self.load_ideas(filepath.name)
            pending.extend([idea for idea in ideas if not idea.get('model_generated', False)])

        return pending


if __name__ == "__main__":
    # Test the idea generator
    Config.validate()

    generator = IdeaGenerator()
    print("Generating ideas...")

    ideas = generator.generate_ideas(num_ideas=3)

    print(f"\nGenerated {len(ideas)} ideas:")
    for idea in ideas:
        print(f"\n- {idea['title']}")
        print(f"  {idea['description']}")

    filepath = generator.save_ideas(ideas)
    print(f"\nSaved to: {filepath}")
