"""Generate 3D models using Meshy AI API."""
import json
import time
import requests
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
from config import Config


class ModelGenerator:
    """Generate 3D models from text descriptions using Meshy AI."""

    def __init__(self):
        """Initialize the model generator with Meshy API."""
        self.api_key = Config.MESHY_API_KEY
        self.base_url = "https://api.meshy.ai/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_model(self, idea: Dict, quality: str = "medium") -> Dict:
        """
        Generate a 3D model from an idea description.

        Args:
            idea: Idea dictionary with title and description
            quality: Quality level - "low", "medium", "high" (affects cost)

        Returns:
            Dictionary with model data and file path
        """
        print(f"\nGenerating 3D model for: {idea['title']}")

        # Prepare the prompt for Meshy AI
        prompt = self._create_meshy_prompt(idea)

        try:
            # Step 1: Create the text-to-3D task
            task_id = self._create_task(prompt, quality)
            print(f"Task created: {task_id}")

            # Step 2: Poll for completion
            model_data = self._wait_for_completion(task_id)
            print("Model generation completed!")

            # Step 3: Download the model
            model_path = self._download_model(model_data, idea)

            result = {
                "idea_id": idea['id'],
                "task_id": task_id,
                "model_path": str(model_path),
                "download_url": model_data.get('model_url'),
                "thumbnail_url": model_data.get('thumbnail_url'),
                "generated_at": datetime.now().isoformat(),
                "quality": quality
            }

            return result

        except Exception as e:
            print(f"Error generating model: {e}")
            raise

    def _create_meshy_prompt(self, idea: Dict) -> str:
        """Create an optimized prompt for Meshy AI."""
        # Combine title and description for better results
        prompt = f"{idea['title']}. {idea['description']}"

        # Add technical hints for better 3D printing
        prompt += " Optimized for 3D printing, solid design, printable without supports."

        return prompt

    def _create_task(self, prompt: str, quality: str) -> str:
        """Create a text-to-3D generation task."""
        # Map quality to Meshy AI parameters
        quality_settings = {
            "low": {"art_style": "realistic", "resolution": "low"},
            "medium": {"art_style": "realistic", "resolution": "medium"},
            "high": {"art_style": "realistic", "resolution": "high"}
        }

        settings = quality_settings.get(quality, quality_settings["medium"])

        payload = {
            "mode": "preview",  # Use preview mode for faster/cheaper generation
            "prompt": prompt,
            "art_style": settings["art_style"],
            "negative_prompt": "low quality, blurry, distorted, unusable for 3D printing"
        }

        response = requests.post(
            f"{self.base_url}/text-to-3d",
            headers=self.headers,
            json=payload
        )

        response.raise_for_status()
        data = response.json()

        return data['result']

    def _wait_for_completion(self, task_id: str, timeout: int = 600) -> Dict:
        """Poll the API until the model is ready."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            response = requests.get(
                f"{self.base_url}/text-to-3d/{task_id}",
                headers=self.headers
            )

            response.raise_for_status()
            data = response.json()

            status = data.get('status')
            progress = data.get('progress', 0)

            print(f"Status: {status} - Progress: {progress}%")

            if status == 'SUCCEEDED':
                return data

            if status == 'FAILED':
                raise Exception(f"Model generation failed: {data.get('error')}")

            # Wait before next poll (reduce API calls)
            time.sleep(10)

        raise TimeoutError(f"Model generation timed out after {timeout} seconds")

    def _download_model(self, model_data: Dict, idea: Dict) -> Path:
        """Download the generated 3D model."""
        model_url = model_data.get('model_urls', {}).get('glb') or model_data.get('model_url')

        if not model_url:
            raise ValueError("No model URL found in response")

        # Create filename based on idea
        safe_title = "".join(c for c in idea['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')
        filename = f"{safe_title}_{idea['id']}.glb"

        filepath = Config.MODELS_DIR / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Download the model
        print(f"Downloading model to: {filepath}")
        response = requests.get(model_url)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"Model saved: {filepath}")
        return filepath

    def refine_model(self, task_id: str) -> Dict:
        """
        Refine a preview model to higher quality.
        Note: This costs more credits but improves quality.
        """
        payload = {"mode": "refine"}

        response = requests.post(
            f"{self.base_url}/text-to-3d/{task_id}/refine",
            headers=self.headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    # Test the model generator
    Config.validate()

    # Create a test idea
    test_idea = {
        "id": "test_001",
        "title": "Hexagonal Desk Organizer",
        "description": "A modular hexagonal organizer for pens, pencils, and small office supplies. Features multiple compartments.",
        "keywords": ["organizer", "desk", "office", "hexagonal", "modular"]
    }

    generator = ModelGenerator()
    print("Testing model generation...")
    print("Note: This will use Meshy AI credits!")

    # Uncomment to test:
    # result = generator.generate_model(test_idea, quality="medium")
    # print(f"\nGeneration result: {result}")
