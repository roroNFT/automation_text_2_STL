"""Upload 3D models to Printables.com."""
import json
import requests
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path
from config import Config


class PrintablesUploader:
    """Upload and manage 3D models on Printables.com."""

    def __init__(self):
        """Initialize the Printables uploader."""
        self.api_key = Config.PRINTABLES_API_KEY
        # Note: Printables may not have a public API yet
        # This is a template structure for when/if they do
        self.base_url = "https://www.printables.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def upload_model(self, idea: Dict, model_path: Path, images: List[Path] = None) -> Dict:
        """
        Upload a 3D model to Printables.

        Args:
            idea: Idea dictionary with metadata
            model_path: Path to the 3D model file
            images: Optional list of image paths for the model

        Returns:
            Upload result with URL and status
        """
        print(f"\nUploading to Printables: {idea['title']}")

        # Prepare the model metadata
        metadata = self._prepare_metadata(idea)

        try:
            # Note: This is a template. Printables might require web scraping
            # or manual upload if they don't have a public API.
            # For now, we'll save the metadata for manual upload.

            result = self._save_for_manual_upload(idea, model_path, metadata, images)

            print(f"Upload prepared for: {idea['title']}")
            return result

        except Exception as e:
            print(f"Error uploading to Printables: {e}")
            raise

    def _prepare_metadata(self, idea: Dict) -> Dict:
        """Prepare metadata for Printables upload."""
        # Map our idea format to Printables format
        metadata = {
            "title": idea['title'],
            "description": self._format_description(idea),
            "category": self._determine_category(idea),
            "tags": idea.get('keywords', []),
            "license": "CC BY-NC-SA 4.0",  # Creative Commons default
            "print_settings": {
                "difficulty": idea.get('difficulty', 'intermediate'),
                "estimated_time": idea.get('print_time', 'Unknown'),
            },
            "summary": idea['description']
        }

        return metadata

    def _format_description(self, idea: Dict) -> str:
        """Format a rich description for Printables."""
        description = f"# {idea['title']}\n\n"
        description += f"{idea['description']}\n\n"
        description += f"## Details\n\n"
        description += f"- **Target Audience**: {idea.get('target_audience', 'General')}\n"
        description += f"- **Difficulty**: {idea.get('difficulty', 'Intermediate')}\n"
        description += f"- **Estimated Print Time**: {idea.get('print_time', 'Varies')}\n"
        description += f"- **Use Case**: {idea.get('use_case', 'General purpose')}\n\n"
        description += "## Printing Tips\n\n"
        description += "- Use standard PLA or PETG filament\n"
        description += "- 0.2mm layer height recommended\n"
        description += "- 20% infill should be sufficient\n\n"
        description += "*Generated with AI-powered automation*\n"

        return description

    def _determine_category(self, idea: Dict) -> str:
        """Determine the best category based on keywords and description."""
        keywords = [k.lower() for k in idea.get('keywords', [])]
        use_case = idea.get('use_case', '').lower()

        # Map keywords to Printables categories
        category_map = {
            "organizer": "Home & Garden",
            "desk": "Home & Garden",
            "office": "Home & Garden",
            "game": "Games & Toys",
            "gaming": "Games & Toys",
            "toy": "Games & Toys",
            "tool": "Tools",
            "holder": "Home & Garden",
            "gadget": "Gadgets",
            "decoration": "Art & Design",
            "miniature": "Games & Toys",
            "model": "Art & Design"
        }

        for keyword in keywords:
            if keyword in category_map:
                return category_map[keyword]

        # Default category
        return "Other"

    def _save_for_manual_upload(self, idea: Dict, model_path: Path,
                                 metadata: Dict, images: List[Path] = None) -> Dict:
        """
        Save all data needed for manual upload to Printables.
        Since Printables may not have a public API, we create a package
        that can be manually uploaded.
        """
        # Create upload package directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in idea['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')

        package_dir = Config.UPLOADS_DIR / "printables" / f"{safe_title}_{timestamp}"
        package_dir.mkdir(parents=True, exist_ok=True)

        # Save metadata
        metadata_path = package_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Save description as markdown
        desc_path = package_dir / "description.md"
        with open(desc_path, 'w', encoding='utf-8') as f:
            f.write(metadata['description'])

        # Create upload instructions
        instructions_path = package_dir / "UPLOAD_INSTRUCTIONS.txt"
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write("PRINTABLES UPLOAD INSTRUCTIONS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Title: {metadata['title']}\n")
            f.write(f"Category: {metadata['category']}\n")
            f.write(f"Tags: {', '.join(metadata['tags'])}\n")
            f.write(f"License: {metadata['license']}\n\n")
            f.write(f"Model File: {model_path.name}\n")
            f.write(f"Model Location: {model_path}\n\n")
            f.write("Description:\n")
            f.write("-" * 50 + "\n")
            f.write(metadata['description'] + "\n\n")
            f.write("Steps to upload:\n")
            f.write("1. Go to https://www.printables.com/upload\n")
            f.write("2. Upload the model file from the location above\n")
            f.write("3. Copy the title and description from this file\n")
            f.write("4. Select the category and add tags\n")
            f.write("5. Upload any images (if available)\n")
            f.write("6. Review and publish\n")

        result = {
            "idea_id": idea['id'],
            "platform": "printables",
            "package_dir": str(package_dir),
            "model_path": str(model_path),
            "metadata_path": str(metadata_path),
            "status": "ready_for_manual_upload",
            "prepared_at": datetime.now().isoformat()
        }

        # Save result
        result_path = package_dir / "upload_result.json"
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)

        return result


if __name__ == "__main__":
    # Test the uploader
    test_idea = {
        "id": "test_001",
        "title": "Hexagonal Desk Organizer",
        "description": "A modular hexagonal organizer for pens, pencils, and small office supplies.",
        "target_audience": "Office workers and students",
        "difficulty": "beginner",
        "print_time": "4-6 hours",
        "use_case": "Desk organization",
        "keywords": ["organizer", "desk", "office", "hexagonal", "modular"]
    }

    uploader = PrintablesUploader()
    # result = uploader.upload_model(test_idea, Path("test_model.stl"))
    print("Printables uploader ready")
