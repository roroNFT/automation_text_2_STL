#!/usr/bin/env python3
"""Test rapide des clés API."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Charger .env
env_file = Path(__file__).parent.parent / ".env"
if not env_file.exists():
    print("❌ Fichier .env introuvable!")
    print(f"Cherché à: {env_file}")
    sys.exit(1)

load_dotenv(env_file)

print("=" * 70)
print("TEST DES CLÉS API")
print("=" * 70)

# Test Claude/Anthropic
print("\n1️⃣  TEST CLAUDE API")
print("-" * 70)

anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()

if not anthropic_key or anthropic_key == "your_claude_api_key_here":
    print("❌ Clé Anthropic non configurée dans .env")
    print("\nVeuillez éditer le fichier .env et ajouter:")
    print("ANTHROPIC_API_KEY=sk-ant-api03-VOTRE_CLE_ICI")
    sys.exit(1)

print(f"Clé trouvée: {anthropic_key[:20]}...{anthropic_key[-10:]}")
print(f"Longueur: {len(anthropic_key)} caractères")

if not anthropic_key.startswith("sk-ant-api03-"):
    print("⚠️  Format de clé suspect!")
    print("Les clés Claude commencent normalement par 'sk-ant-api03-'")
    print("\nVérifiez que vous avez copié la bonne clé depuis:")
    print("https://console.anthropic.com/settings/keys")
else:
    print("✓ Format de clé correct")

# Tester la clé avec un appel API
print("\nTest de connexion à l'API Claude...")
try:
    import anthropic

    client = anthropic.Anthropic(api_key=anthropic_key)

    # Test simple avec un prompt minimal
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=50,
        messages=[
            {"role": "user", "content": "Répondez juste 'OK' si vous recevez ce message."}
        ]
    )

    response = message.content[0].text
    print(f"✓ Connexion réussie!")
    print(f"Réponse de Claude: {response}")

except ImportError:
    print("❌ Module 'anthropic' non installé")
    print("Exécutez: pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"❌ Erreur de connexion: {e}")
    print("\nPossibles causes:")
    print("1. Clé API invalide ou expirée")
    print("2. Compte Claude Pro non actif")
    print("3. Problème de connexion Internet")
    print("\nActions à faire:")
    print("- Vérifiez votre clé API sur https://console.anthropic.com/settings/keys")
    print("- Créez une nouvelle clé si nécessaire")
    print("- Vérifiez que votre compte est actif")
    sys.exit(1)

# Test Meshy AI
print("\n2️⃣  TEST MESHY AI")
print("-" * 70)

meshy_key = os.getenv("MESHY_API_KEY", "").strip()

if not meshy_key or meshy_key == "your_meshy_api_key_here":
    print("⚠️  Clé Meshy non configurée")
    print("(Requis uniquement pour générer des modèles 3D)")
else:
    print(f"Clé trouvée: {meshy_key[:10]}...{meshy_key[-5:]}")
    print(f"Longueur: {len(meshy_key)} caractères")

    if not meshy_key.startswith("msy_"):
        print("⚠️  Format de clé Meshy suspect (devrait commencer par 'msy_')")
    else:
        print("✓ Format de clé correct")

    print("\nTest de connexion Meshy AI...")
    try:
        import requests

        headers = {
            "Authorization": f"Bearer {meshy_key}"
        }

        # Test avec un endpoint simple (list tasks ou similar)
        response = requests.get(
            "https://api.meshy.ai/v2/text-to-3d",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print("✓ Connexion Meshy AI réussie!")
        elif response.status_code == 401:
            print("❌ Clé Meshy AI invalide")
            print("Vérifiez votre clé sur: https://app.meshy.ai/api-keys")
        else:
            print(f"⚠️  Réponse inattendue: {response.status_code}")

    except Exception as e:
        print(f"⚠️  Impossible de tester Meshy: {e}")

# Résumé
print("\n" + "=" * 70)
print("RÉSUMÉ")
print("=" * 70)
print("\n✓ Claude API : Fonctionne!")
print(f"{'✓' if meshy_key and meshy_key != 'your_meshy_api_key_here' else '⚠️ '} Meshy AI : {'Configurée' if meshy_key and meshy_key != 'your_meshy_api_key_here' else 'Non configurée (requis pour modèles 3D)'}")
print("\nVous pouvez maintenant lancer:")
print("  python main.py --mode ideas --num-ideas 3")
print("\n" + "=" * 70)
