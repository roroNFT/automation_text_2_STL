#!/usr/bin/env python3
"""Convertir les fichiers GLB en STL."""
import sys
from pathlib import Path

try:
    import trimesh
except ImportError:
    print("❌ Module 'trimesh' requis pour la conversion")
    print("\nInstallez-le avec:")
    print("  pip install trimesh")
    sys.exit(1)


def convert_glb_to_stl(glb_path: Path, stl_path: Path = None):
    """
    Convertir un fichier GLB en STL.

    Args:
        glb_path: Chemin vers le fichier GLB
        stl_path: Chemin de sortie STL (optionnel)
    """
    if not glb_path.exists():
        print(f"❌ Fichier introuvable: {glb_path}")
        return False

    if stl_path is None:
        stl_path = glb_path.with_suffix('.stl')

    try:
        print(f"Conversion: {glb_path.name} → {stl_path.name}")

        # Charger le modèle GLB
        mesh = trimesh.load(str(glb_path))

        # Si c'est une scène avec plusieurs meshes, les fusionner
        if isinstance(mesh, trimesh.Scene):
            # Fusionner tous les meshes de la scène
            meshes = []
            for geometry in mesh.geometry.values():
                if isinstance(geometry, trimesh.Trimesh):
                    meshes.append(geometry)

            if meshes:
                mesh = trimesh.util.concatenate(meshes)
            else:
                print("⚠️  Aucun mesh trouvé dans la scène")
                return False

        # Exporter en STL
        mesh.export(str(stl_path))

        print(f"✓ Conversion réussie: {stl_path}")
        print(f"  Triangles: {len(mesh.faces)}")
        print(f"  Vertices: {len(mesh.vertices)}")

        return True

    except Exception as e:
        print(f"❌ Erreur lors de la conversion: {e}")
        return False


def convert_all_glb_in_directory(directory: Path):
    """Convertir tous les fichiers GLB d'un dossier."""
    glb_files = list(directory.glob("*.glb"))

    if not glb_files:
        print(f"Aucun fichier GLB trouvé dans: {directory}")
        return

    print(f"Trouvé {len(glb_files)} fichier(s) GLB")
    print("=" * 60)

    success = 0
    failed = 0

    for glb_file in glb_files:
        if convert_glb_to_stl(glb_file):
            success += 1
        else:
            failed += 1
        print()

    print("=" * 60)
    print(f"Résumé: {success} réussies, {failed} échouées")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convertir des fichiers GLB en STL"
    )

    parser.add_argument(
        "input",
        help="Fichier GLB ou dossier contenant des GLB"
    )

    parser.add_argument(
        "-o", "--output",
        help="Fichier STL de sortie (si input est un fichier unique)"
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"❌ Chemin introuvable: {input_path}")
        sys.exit(1)

    if input_path.is_file():
        # Convertir un seul fichier
        output_path = Path(args.output) if args.output else None
        if convert_glb_to_stl(input_path, output_path):
            sys.exit(0)
        else:
            sys.exit(1)

    elif input_path.is_dir():
        # Convertir tous les GLB du dossier
        convert_all_glb_in_directory(input_path)

    else:
        print(f"❌ Chemin invalide: {input_path}")
        sys.exit(1)
