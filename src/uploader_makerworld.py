"""Upload 3D models to MakerWorld."""
import json
import requests
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path
from config import Config


class MakerWorldUploader:
    """Upload and manage 3D models on MakerWorld."""

    def __init__(self):
        """Initialize the MakerWorld uploader."""
        self.api_key = Config.MAKERWORLD_API_KEY
        # Note: MakerWorld API details - adjust based on actual API
        self.base_url = "https://makerworld.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def upload_model(self, idea: Dict, model_path: Path, images: List[Path] = None) -> Dict:
        """
        Upload a 3D model to MakerWorld.

        Args:
            idea: Idea dictionary with metadata
            model_path: Path to the 3D model file
            images: Optional list of image paths

        Returns:
            Upload result with URL and status
        """
        print(f"\nUploading to MakerWorld: {idea['title']}")

        metadata = self._prepare_metadata(idea)

        try:
            # Similar to Printables, this might require manual upload
            # or web scraping if no public API is available
            result = self._save_for_manual_upload(idea, model_path, metadata, images)

            print(f"Upload prepared for: {idea['title']}")
            return result

        except Exception as e:
            print(f"Error uploading to MakerWorld: {e}")
            raise

    def _prepare_metadata(self, idea: Dict) -> Dict:
        """Prepare metadata for MakerWorld upload."""
        metadata = {
            "title": idea['title'],
            "description": self._format_description(idea),
            "category": self._determine_category(idea),
            "tags": idea.get('keywords', []),
            "difficulty_level": idea.get('difficulty', 'intermediate'),
            "print_time": idea.get('print_time', 'Unknown'),
            "license_type": "Creative Commons Attribution-NonCommercial-ShareAlike"
        }

        return metadata

    def _format_description(self, idea: Dict) -> str:
        """Format a rich description for MakerWorld."""
        description = f"# {idea['title']}\n\n"
        description += f"{idea['description']}\n\n"
        description += f"## Specifications\n\n"
        description += f"- **Target Users**: {idea.get('target_audience', 'All makers')}\n"
        description += f"- **Skill Level**: {idea.get('difficulty', 'Intermediate')}\n"
        description += f"- **Print Duration**: {idea.get('print_time', 'Varies by printer')}\n"
        description += f"- **Primary Use**: {idea.get('use_case', 'Multipurpose')}\n\n"
        description += "## Recommended Print Settings\n\n"
        description += "- **Material**: PLA, PETG, or ABS\n"
        description += "- **Layer Height**: 0.2mm\n"
        description += "- **Infill**: 15-20%\n"
        description += "- **Supports**: Check model preview\n"
        description += "- **Build Plate Adhesion**: Brim recommended\n\n"
        description += "## About This Model\n\n"
        description += "This model was created using AI-powered design automation "
        description += "to bring you innovative and practical 3D printable objects.\n"

        return description

    def _determine_category(self, idea: Dict) -> str:
        """Determine the best category for MakerWorld."""
        keywords = [k.lower() for k in idea.get('keywords', [])]

        category_map = {
            "organizer": "Organization",
            "desk": "Office & Organization",
            "office": "Office & Organization",
            "game": "Toys & Games",
            "gaming": "Hobbies & Games",
            "toy": "Toys & Games",
            "tool": "Tools & Utilities",
            "holder": "Organization",
            "gadget": "Electronics & Gadgets",
            "decoration": "Home Decor",
            "miniature": "Models & Miniatures",
            "model": "Models & Miniatures"
        }

        for keyword in keywords:
            if keyword in category_map:
                return category_map[keyword]

        return "Other"

    def _save_for_manual_upload(self, idea: Dict, model_path: Path,
                                 metadata: Dict, images: List[Path] = None) -> Dict:
        """Save all data needed for manual upload to MakerWorld."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in idea['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')

        package_dir = Config.UPLOADS_DIR / "makerworld" / f"{safe_title}_{timestamp}"
        package_dir.mkdir(parents=True, exist_ok=True)

        # Save metadata
        metadata_path = package_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Save description
        desc_path = package_dir / "description.md"
        with open(desc_path, 'w', encoding='utf-8') as f:
            f.write(metadata['description'])

        # Create upload instructions
        instructions_path = package_dir / "UPLOAD_INSTRUCTIONS.txt"
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write("MAKERWORLD UPLOAD INSTRUCTIONS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Title: {metadata['title']}\n")
            f.write(f"Category: {metadata['category']}\n")
            f.write(f"Tags: {', '.join(metadata['tags'])}\n")
            f.write(f"Difficulty: {metadata['difficulty_level']}\n")
            f.write(f"Print Time: {metadata['print_time']}\n\n")
            f.write(f"Model File: {model_path.name}\n")
            f.write(f"Model Location: {model_path}\n\n")
            f.write("Description:\n")
            f.write("-" * 50 + "\n")
            f.write(metadata['description'] + "\n\n")
            f.write("Upload Steps:\n")
            f.write("1. Visit MakerWorld and log in\n")
            f.write("2. Navigate to 'Upload Model' or 'Create'\n")
            f.write("3. Upload the model file from the location above\n")
            f.write("4. Fill in the title, description, and metadata\n")
            f.write("5. Select category and add tags\n")
            f.write("6. Upload preview images (if available)\n")
            f.write("7. Set print settings and difficulty level\n")
            f.write("8. Review and publish\n")

        result = {
            "idea_id": idea['id'],
            "platform": "makerworld",
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
    print("MakerWorld uploader ready")
