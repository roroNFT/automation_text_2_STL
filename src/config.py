"""Configuration management for the 3D automation project."""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for API keys and settings."""

    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MESHY_API_KEY = os.getenv("MESHY_API_KEY")
    PRINTABLES_API_KEY = os.getenv("PRINTABLES_API_KEY")
    MAKERWORLD_API_KEY = os.getenv("MAKERWORLD_API_KEY")

    # Claude settings - Using Haiku for cost optimization
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-20241022")

    # Generation settings
    MAX_IDEAS_PER_RUN = int(os.getenv("MAX_IDEAS_PER_RUN", "5"))

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    IDEAS_DIR = DATA_DIR / "ideas"
    MODELS_DIR = DATA_DIR / "models"
    UPLOADS_DIR = DATA_DIR / "uploads"
    LOGS_DIR = BASE_DIR / "logs"

    @classmethod
    def validate(cls):
        """Validate that required API keys are present."""
        required = {
            "ANTHROPIC_API_KEY": cls.ANTHROPIC_API_KEY,
            "MESHY_API_KEY": cls.MESHY_API_KEY,
        }

        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(f"Missing required API keys: {', '.join(missing)}")

        return True
