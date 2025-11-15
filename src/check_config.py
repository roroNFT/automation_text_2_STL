#!/usr/bin/env python3
"""Script de vérification de la configuration."""
import os
from pathlib import Path
from dotenv import load_dotenv

def check_config():
    """Vérifie la configuration et les clés API."""
    print("=" * 60)
    print("VÉRIFICATION DE LA CONFIGURATION")
    print("=" * 60)

    # Vérifier que .env existe
    env_file = Path(".env")
    if not env_file.exists():
        env_file = Path("../.env")

    if not env_file.exists():
        print("\n❌ Fichier .env introuvable!")
        print("\nCréez un fichier .env à la racine du projet:")
        print("  cp .env.example .env")
        print("\nPuis éditez-le et ajoutez vos clés API.")
        return False

    print(f"\n✓ Fichier .env trouvé: {env_file.absolute()}")

    # Charger les variables d'environnement
    load_dotenv(env_file)

    # Vérifier chaque clé API
    print("\n" + "-" * 60)
    print("CLÉS API")
    print("-" * 60)

    checks = {
        "ANTHROPIC_API_KEY": {
            "required": True,
            "prefix": "sk-ant-api03-",
            "description": "Claude API (Anthropic)"
        },
        "MESHY_API_KEY": {
            "required": True,
            "prefix": "msy_",
            "description": "Meshy AI"
        },
        "PRINTABLES_API_KEY": {
            "required": False,
            "prefix": None,
            "description": "Printables (optionnel)"
        },
        "MAKERWORLD_API_KEY": {
            "required": False,
            "prefix": None,
            "description": "MakerWorld (optionnel)"
        }
    }

    all_good = True

    for key, info in checks.items():
        value = os.getenv(key, "").strip()

        if not value or value == f"your_{key.lower()}_here":
            if info["required"]:
                print(f"\n❌ {key}")
                print(f"   {info['description']}")
                print(f"   Status: MANQUANTE (requis)")
                all_good = False
            else:
                print(f"\n⚠️  {key}")
                print(f"   {info['description']}")
                print(f"   Status: Non configurée (optionnel)")
        else:
            # Vérifier le préfixe si spécifié
            prefix_ok = True
            if info["prefix"]:
                if not value.startswith(info["prefix"]):
                    prefix_ok = False
                    print(f"\n⚠️  {key}")
                    print(f"   {info['description']}")
                    print(f"   Status: Format incorrect (devrait commencer par '{info['prefix']}')")
                    print(f"   Valeur actuelle: {value[:20]}...")
                    all_good = False
                else:
                    print(f"\n✓ {key}")
                    print(f"   {info['description']}")
                    print(f"   Status: OK (commence par '{info['prefix']}')")
                    print(f"   Longueur: {len(value)} caractères")
            else:
                print(f"\n✓ {key}")
                print(f"   {info['description']}")
                print(f"   Status: Configurée")
                print(f"   Longueur: {len(value)} caractères")

    print("\n" + "=" * 60)

    if all_good:
        print("\n✓ Configuration valide!")
        print("\nVous pouvez maintenant lancer:")
        print("  python main.py --mode ideas --num-ideas 3")
        return True
    else:
        print("\n❌ Problèmes de configuration détectés")
        print("\nCorrigez les erreurs ci-dessus avant de continuer.")
        return False

if __name__ == "__main__":
    check_config()
