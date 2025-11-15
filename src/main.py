"""Main automation script for 3D model generation and upload."""
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from config import Config
from idea_generator import IdeaGenerator
from model_generator import ModelGenerator
from uploader_printables import PrintablesUploader
from uploader_makerworld import MakerWorldUploader


class AutomationPipeline:
    """Main pipeline for automating 3D model creation and upload."""

    def __init__(self):
        """Initialize the automation pipeline."""
        self.idea_generator = IdeaGenerator()
        self.model_generator = ModelGenerator()
        self.printables_uploader = PrintablesUploader()
        self.makerworld_uploader = MakerWorldUploader()

    def run_full_pipeline(self, num_ideas: int = 5, category: str = None,
                         quality: str = "medium", platforms: List[str] = None):
        """
        Run the complete automation pipeline.

        Args:
            num_ideas: Number of ideas to generate
            category: Optional category for ideas
            quality: Model quality (low/medium/high)
            platforms: List of platforms to upload to
        """
        if platforms is None:
            platforms = ["printables", "makerworld"]

        print("=" * 60)
        print("3D MODEL AUTOMATION PIPELINE")
        print("=" * 60)
        print(f"\nConfiguration:")
        print(f"  - Ideas to generate: {num_ideas}")
        print(f"  - Category: {category or 'All'}")
        print(f"  - Model quality: {quality}")
        print(f"  - Target platforms: {', '.join(platforms)}")
        print("\n" + "=" * 60 + "\n")

        try:
            # Step 1: Generate ideas
            print("STEP 1: Generating Ideas")
            print("-" * 60)
            ideas = self.idea_generator.generate_ideas(num_ideas, category)
            ideas_file = self.idea_generator.save_ideas(ideas)
            print(f"✓ Generated {len(ideas)} ideas")
            print(f"✓ Saved to: {ideas_file}\n")

            # Display generated ideas
            for idx, idea in enumerate(ideas, 1):
                print(f"{idx}. {idea['title']}")
                print(f"   {idea['description'][:80]}...")

            print("\n" + "=" * 60 + "\n")

            # Step 2: Generate 3D models
            print("STEP 2: Generating 3D Models")
            print("-" * 60)
            print("⚠ This will use Meshy AI credits!")

            for idx, idea in enumerate(ideas, 1):
                print(f"\n[{idx}/{len(ideas)}] Processing: {idea['title']}")

                try:
                    model_result = self.model_generator.generate_model(idea, quality)
                    idea['model_generated'] = True
                    idea['model_path'] = model_result['model_path']
                    idea['model_data'] = model_result
                    print(f"✓ Model generated: {model_result['model_path']}")

                except Exception as e:
                    print(f"✗ Failed to generate model: {e}")
                    idea['model_generated'] = False
                    idea['generation_error'] = str(e)

            print("\n" + "=" * 60 + "\n")

            # Step 3: Upload to platforms
            print("STEP 3: Preparing Uploads")
            print("-" * 60)

            for idx, idea in enumerate(ideas, 1):
                if not idea.get('model_generated', False):
                    print(f"\n[{idx}/{len(ideas)}] Skipping {idea['title']} (no model)")
                    continue

                print(f"\n[{idx}/{len(ideas)}] Uploading: {idea['title']}")
                model_path = Path(idea['model_path'])

                # Upload to each platform
                if "printables" in platforms:
                    try:
                        result = self.printables_uploader.upload_model(idea, model_path)
                        idea['uploaded_printables'] = True
                        idea['printables_data'] = result
                        print(f"✓ Printables package: {result['package_dir']}")
                    except Exception as e:
                        print(f"✗ Printables upload failed: {e}")
                        idea['uploaded_printables'] = False

                if "makerworld" in platforms:
                    try:
                        result = self.makerworld_uploader.upload_model(idea, model_path)
                        idea['uploaded_makerworld'] = True
                        idea['makerworld_data'] = result
                        print(f"✓ MakerWorld package: {result['package_dir']}")
                    except Exception as e:
                        print(f"✗ MakerWorld upload failed: {e}")
                        idea['uploaded_makerworld'] = False

            print("\n" + "=" * 60 + "\n")

            # Save final results
            self._save_results(ideas)

            # Print summary
            self._print_summary(ideas)

        except Exception as e:
            print(f"\n✗ Pipeline error: {e}")
            raise

    def run_ideas_only(self, num_ideas: int = 5, category: str = None):
        """Generate ideas without creating models."""
        print("Generating ideas only...\n")

        ideas = self.idea_generator.generate_ideas(num_ideas, category)
        ideas_file = self.idea_generator.save_ideas(ideas)

        print(f"\n✓ Generated {len(ideas)} ideas")
        print(f"✓ Saved to: {ideas_file}\n")

        for idx, idea in enumerate(ideas, 1):
            print(f"{idx}. {idea['title']}")
            print(f"   {idea['description']}")
            print(f"   Keywords: {', '.join(idea['keywords'])}\n")

    def run_models_only(self, ideas_file: str, quality: str = "medium"):
        """Generate models from existing ideas."""
        print(f"Generating models from: {ideas_file}\n")

        ideas = self.idea_generator.load_ideas(ideas_file)
        pending = [i for i in ideas if not i.get('model_generated', False)]

        print(f"Found {len(pending)} ideas without models\n")

        for idx, idea in enumerate(pending, 1):
            print(f"[{idx}/{len(pending)}] {idea['title']}")
            try:
                model_result = self.model_generator.generate_model(idea, quality)
                idea['model_generated'] = True
                idea['model_path'] = model_result['model_path']
                print(f"✓ Generated: {model_result['model_path']}\n")
            except Exception as e:
                print(f"✗ Failed: {e}\n")

        self.idea_generator.save_ideas(ideas, ideas_file)

    def _save_results(self, ideas: List[Dict]):
        """Save pipeline results."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = Config.DATA_DIR / f"pipeline_results_{timestamp}.json"

        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(ideas, f, indent=2, ensure_ascii=False)

        print(f"✓ Results saved to: {results_file}")

    def _print_summary(self, ideas: List[Dict]):
        """Print pipeline summary."""
        print("PIPELINE SUMMARY")
        print("=" * 60)

        total = len(ideas)
        models_generated = sum(1 for i in ideas if i.get('model_generated', False))
        printables_ready = sum(1 for i in ideas if i.get('uploaded_printables', False))
        makerworld_ready = sum(1 for i in ideas if i.get('uploaded_makerworld', False))

        print(f"\nTotal ideas: {total}")
        print(f"Models generated: {models_generated}/{total}")
        print(f"Printables ready: {printables_ready}/{total}")
        print(f"MakerWorld ready: {makerworld_ready}/{total}")

        print("\n" + "=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automate 3D model generation and upload"
    )

    parser.add_argument(
        "--mode",
        choices=["full", "ideas", "models", "upload"],
        default="full",
        help="Pipeline mode: full, ideas-only, models-only, or upload-only"
    )

    parser.add_argument(
        "--num-ideas",
        type=int,
        default=5,
        help="Number of ideas to generate (default: 5)"
    )

    parser.add_argument(
        "--category",
        type=str,
        help="Category for idea generation (e.g., 'practical', 'gaming', 'decorative')"
    )

    parser.add_argument(
        "--quality",
        choices=["low", "medium", "high"],
        default="medium",
        help="Model generation quality (affects cost)"
    )

    parser.add_argument(
        "--platforms",
        nargs="+",
        choices=["printables", "makerworld"],
        default=["printables", "makerworld"],
        help="Platforms to upload to"
    )

    parser.add_argument(
        "--ideas-file",
        type=str,
        help="Path to existing ideas file (for models/upload modes)"
    )

    args = parser.parse_args()

    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("\nPlease set up your .env file with required API keys.")
        print("See .env.example for reference.")
        sys.exit(1)

    # Run pipeline
    pipeline = AutomationPipeline()

    try:
        if args.mode == "full":
            pipeline.run_full_pipeline(
                num_ideas=args.num_ideas,
                category=args.category,
                quality=args.quality,
                platforms=args.platforms
            )

        elif args.mode == "ideas":
            pipeline.run_ideas_only(
                num_ideas=args.num_ideas,
                category=args.category
            )

        elif args.mode == "models":
            if not args.ideas_file:
                print("✗ --ideas-file required for 'models' mode")
                sys.exit(1)
            pipeline.run_models_only(
                ideas_file=args.ideas_file,
                quality=args.quality
            )

        print("\n✓ Pipeline completed successfully!")

    except KeyboardInterrupt:
        print("\n\n✗ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
