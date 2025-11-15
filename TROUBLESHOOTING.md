# Guide de Dépannage

## ❌ Erreur: "invalid x-api-key" (Error 401)

Cette erreur signifie que votre clé API Claude n'est pas valide. Voici comment la résoudre :

### Étape 1 : Vérifier votre configuration

```bash
cd src
python check_config.py
```

Ce script va vérifier toutes vos clés API et identifier les problèmes.

### Étape 2 : Obtenir la bonne clé API Claude

1. **Allez sur** : https://console.anthropic.com/settings/keys
2. **Connectez-vous** avec votre compte Claude Pro
3. **Créez une nouvelle clé** (bouton "Create Key")
4. **Copiez la clé** - Elle commence par `sk-ant-api03-`

⚠️ **Important** :
- La clé commence TOUJOURS par `sk-ant-api03-`
- Elle fait environ 100+ caractères
- Ne partagez JAMAIS cette clé

### Étape 3 : Configurer correctement le fichier .env

Le fichier `.env` doit être à la **racine du projet** (pas dans `src/`).

```bash
# Depuis la racine du projet
nano .env
```

**Format correct** :

```env
ANTHROPIC_API_KEY=sk-ant-api03-VOTRE_CLE_ICI_SANS_GUILLEMETS_NI_ESPACES
MESHY_API_KEY=msy_VOTRE_CLE_MESHY_ICI

# Laissez ces lignes vides ou avec des valeurs par défaut
PRINTABLES_API_KEY=
MAKERWORLD_API_KEY=

# Paramètres
MAX_IDEAS_PER_RUN=5
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

### Erreurs Courantes

#### ❌ Mauvais : Guillemets
```env
ANTHROPIC_API_KEY="sk-ant-api03-..."  # NE PAS FAIRE ÇA
```

#### ❌ Mauvais : Espaces
```env
ANTHROPIC_API_KEY = sk-ant-api03-...  # Pas d'espaces autour du =
```

#### ❌ Mauvais : Saut de ligne dans la clé
```env
ANTHROPIC_API_KEY=sk-ant-api03-
    le_reste_de_la_cle...  # Tout sur UNE ligne
```

#### ✅ Bon : Format correct
```env
ANTHROPIC_API_KEY=sk-ant-api03-abcdefghijklmnopqrstuvwxyz...
```

### Étape 4 : Tester à nouveau

```bash
# Vérifier la configuration
cd src
python check_config.py

# Si tout est OK, tester avec des idées seulement
python main.py --mode ideas --num-ideas 1
```

---

## ❌ Erreur: "No such file or directory: main.py"

**Problème** : Vous êtes dans le mauvais dossier.

**Solution** :
```bash
# Allez dans le dossier src/
cd src

# OU depuis la racine utilisez le script
./run.sh --mode ideas --num-ideas 3
```

---

## ❌ Erreur Meshy AI: "Task failed" ou "Invalid API key"

### Solution :

1. **Vérifiez vos crédits Meshy** : https://app.meshy.ai/
2. **Vérifiez votre clé API** : https://app.meshy.ai/api-keys
3. **Format de la clé** : Doit commencer par `msy_`

```bash
# Tester juste la génération d'idées (sans Meshy)
python main.py --mode ideas --num-ideas 3
```

---

## ❌ Erreur: "Module not found"

**Problème** : Dépendances non installées.

**Solution** :
```bash
# Activer l'environnement virtuel
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

---

## 🔍 Vérification Complète de l'Installation

```bash
# 1. Vérifier que vous êtes dans le bon dossier
pwd
# Devrait afficher: .../automation_text_2_STL

# 2. Vérifier que .env existe
ls -la .env
# Devrait montrer le fichier .env

# 3. Vérifier le contenu (attention : ne partagez pas la sortie!)
head -n 3 .env
# Devrait montrer vos clés API

# 4. Vérifier l'environnement virtuel
which python
# Devrait afficher: .../automation_text_2_STL/venv/bin/python

# 5. Vérifier les dépendances
pip list | grep anthropic
# Devrait afficher: anthropic 0.39.0 (ou plus récent)

# 6. Vérifier la configuration
cd src
python check_config.py
```

---

## 💡 Commandes de Test Utiles

### Test Minimal (quasi-gratuit)
```bash
cd src
python main.py --mode ideas --num-ideas 1
```
**Coût** : ~$0.002-0.005

### Test avec Vérification
```bash
# D'abord vérifier la config
python check_config.py

# Si OK, générer 1 idée
python main.py --mode ideas --num-ideas 1
```

### Mode Debug
```bash
# Activer le mode verbose Python
python -v main.py --mode ideas --num-ideas 1
```

---

## 🔑 Où Trouver Vos Clés API

### Claude (Anthropic)
- URL : https://console.anthropic.com/settings/keys
- Format : `sk-ant-api03-...` (100+ caractères)
- Requis : Compte Claude Pro

### Meshy AI
- URL : https://app.meshy.ai/api-keys
- Format : `msy_...`
- Requis : Compte Meshy (gratuit ou payant)

### Printables / MakerWorld
- **Optionnels** pour l'instant
- Laissez vide ou commentez les lignes

---

## 📞 Besoin d'Aide Supplémentaire ?

Si le problème persiste :

1. **Exécutez** :
```bash
cd src
python check_config.py > config_check.txt 2>&1
cat config_check.txt
```

2. **Partagez la sortie** (SANS les clés API!) dans une issue GitHub

3. **Vérifiez** que vous avez bien :
   - Python 3.8+
   - Un compte Claude Pro actif
   - Des crédits Meshy AI disponibles

---

## ✅ Test de Succès

Si tout fonctionne, vous devriez voir :

```
============================================================
3D MODEL AUTOMATION PIPELINE
============================================================

Configuration:
  - Ideas to generate: 1
  - Category: All
  - Model quality: medium
  - Target platforms: printables, makerworld

============================================================

STEP 1: Generating Ideas
------------------------------------------------------------
✓ Generated 1 ideas
✓ Saved to: ../data/ideas/ideas_20241115_xxxxx.json

1. [Titre de l'objet 3D]
   [Description...]
```

**C'est bon !** Vous pouvez maintenant augmenter le nombre d'idées ou générer des modèles 3D.
