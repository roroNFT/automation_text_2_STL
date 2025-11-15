# Automatisation de Génération et Publication d'Objets 3D

Système d'automatisation complet pour générer des idées d'objets 3D, créer les modèles avec Meshy AI, et les préparer pour publication sur Printables et MakerWorld.

## 🎯 Objectif

Ce projet automatise le processus complet de création de contenu 3D :
1. **Génération d'idées** - Utilise Claude API pour créer des idées créatives et populaires
2. **Création de modèles 3D** - Convertit les idées en modèles 3D avec Meshy AI
3. **Préparation pour publication** - Crée des packages prêts à publier sur Printables et MakerWorld

## 💰 Optimisation des Coûts

Le système est conçu pour minimiser les coûts tout en maintenant une haute qualité :

- **Claude API** : Utilise Haiku (modèle le moins cher) par défaut pour la génération d'idées
- **Meshy AI** : Mode "preview" par défaut (plus rapide et moins cher)
- **Génération par lots** : Traitez plusieurs idées en une seule session
- **Modularité** : Générez uniquement ce dont vous avez besoin (idées seules, modèles seuls, etc.)

### Estimation des Coûts

**Claude API (avec compte Pro)** :
- Haiku : ~$0.25 par million de tokens d'entrée / $1.25 par million de tokens de sortie
- 5 idées détaillées : ~$0.01-0.03

**Meshy AI** :
- Mode Preview : ~10-20 crédits par modèle
- Mode Refine : ~50-100 crédits par modèle
- Vérifiez votre plan Meshy pour les tarifs actuels

## 📋 Prérequis

- Python 3.8+
- Compte Claude Pro (API key)
- Compte Meshy AI (API key)
- Comptes Printables et/ou MakerWorld (pour publication)

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone <votre-repo>
cd automation_text_2_STL
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copiez le fichier d'exemple et ajoutez vos clés API :

```bash
cp .env.example .env
```

Éditez `.env` et ajoutez vos clés API :

```env
ANTHROPIC_API_KEY=sk-ant-...
MESHY_API_KEY=msy_...
PRINTABLES_API_KEY=...  # Optionnel
MAKERWORLD_API_KEY=...  # Optionnel
```

**Où trouver vos clés API :**

- **Claude/Anthropic** : https://console.anthropic.com/settings/keys
- **Meshy AI** : https://app.meshy.ai/api-keys
- **Printables/MakerWorld** : Consultez leurs documentations respectives

## 📖 Utilisation

### Mode Complet (Recommandé pour commencer)

Génère des idées, crée les modèles, et prépare les uploads :

```bash
cd src
python main.py --mode full --num-ideas 3 --quality medium
```

### Mode Idées Uniquement (Sans coût Meshy)

Parfait pour tester ou générer beaucoup d'idées d'abord :

```bash
python main.py --mode ideas --num-ideas 10 --category "practical"
```

Catégories suggérées :
- `practical` - Objets utiles du quotidien
- `gaming` - Accessoires de jeu et miniatures
- `decorative` - Objets décoratifs
- `organization` - Solutions de rangement
- `gifts` - Idées cadeaux

### Mode Modèles Uniquement

Générer des modèles 3D pour des idées existantes :

```bash
python main.py --mode models --ideas-file ../data/ideas/ideas_20241115_120000.json --quality medium
```

Niveaux de qualité :
- `low` - Rapide et économique (tests)
- `medium` - Bon équilibre qualité/prix (recommandé)
- `high` - Meilleure qualité (plus cher)

### Options Avancées

```bash
# Générer 5 idées gaming de haute qualité pour Printables seulement
python main.py --mode full --num-ideas 5 --category gaming --quality high --platforms printables

# Générer 10 idées pratiques (sans modèles)
python main.py --mode ideas --num-ideas 10 --category practical
```

## 📁 Structure du Projet

```
automation_text_2_STL/
├── src/                          # Code source
│   ├── config.py                 # Configuration et paramètres
│   ├── idea_generator.py         # Génération d'idées avec Claude
│   ├── model_generator.py        # Génération de modèles avec Meshy AI
│   ├── uploader_printables.py   # Upload vers Printables
│   ├── uploader_makerworld.py   # Upload vers MakerWorld
│   └── main.py                   # Script principal
├── data/                         # Données générées
│   ├── ideas/                    # Idées au format JSON
│   ├── models/                   # Modèles 3D (.glb, .stl)
│   └── uploads/                  # Packages prêts à publier
├── logs/                         # Logs du système
├── .env                          # Configuration (NE PAS COMMITER)
├── .env.example                  # Template de configuration
├── requirements.txt              # Dépendances Python
└── README.md                     # Cette documentation
```

## 📤 Publication sur les Plateformes

### Printables

Après l'exécution, vous trouverez dans `data/uploads/printables/` :
- `metadata.json` - Métadonnées structurées
- `description.md` - Description formatée
- `UPLOAD_INSTRUCTIONS.txt` - Instructions détaillées

**Étapes** :
1. Allez sur https://www.printables.com/upload
2. Uploadez le modèle 3D
3. Copiez-collez le titre et la description
4. Ajoutez les tags et catégorie indiqués
5. Publiez !

### MakerWorld

Similaire à Printables, les packages sont dans `data/uploads/makerworld/`.

**Note** : Ces plateformes peuvent nécessiter un upload manuel car elles n'offrent pas toujours d'API publique.

## 🎨 Exemples de Workflows

### Workflow 1 : Production Rapide (5 objets/jour)

```bash
# Matin : Générer des idées
python main.py --mode ideas --num-ideas 10

# Après-midi : Créer les 5 meilleures
python main.py --mode models --ideas-file ../data/ideas/ideas_latest.json --quality medium

# Soir : Préparer les uploads (automatique si mode full)
```

### Workflow 2 : Qualité Premium (1-2 objets/jour)

```bash
# Générer beaucoup d'idées, choisir les meilleures manuellement
python main.py --mode ideas --num-ideas 20 --category decorative

# Éditer le JSON pour garder les meilleures idées

# Générer en haute qualité
python main.py --mode models --ideas-file ../data/ideas/curated_ideas.json --quality high
```

### Workflow 3 : Test et Validation (Gratuit)

```bash
# Générer des idées uniquement (coût minimal)
python main.py --mode ideas --num-ideas 50

# Analyser les idées, valider la qualité
# Ne générer des modèles que pour les idées validées
```

## 🔧 Personnalisation

### Modifier les Prompts de Génération

Éditez `src/idea_generator.py:40-60` pour ajuster le prompt Claude selon vos besoins.

### Ajouter de Nouvelles Plateformes

Créez un nouveau fichier `src/uploader_PLATFORM.py` en utilisant les templates existants.

### Ajuster les Paramètres Meshy

Modifiez `src/model_generator.py:60-80` pour changer les paramètres de génération.

## 💡 Conseils et Astuces

### Minimiser les Coûts

1. **Générez beaucoup d'idées d'abord** (mode `ideas` uniquement)
2. **Sélectionnez manuellement** les meilleures idées
3. **Utilisez quality=medium** pour la plupart des modèles
4. **Testez avec 1-2 modèles** avant de lancer une batch complète

### Maximiser la Qualité

1. **Utilisez des catégories spécifiques** pour des idées plus ciblées
2. **Éditez le JSON des idées** pour affiner les descriptions avant génération
3. **Utilisez quality=high** pour les modèles destinés à être populaires
4. **Ajoutez des images de rendu** depuis Meshy pour les uploads

### Augmenter les Téléchargements

1. **Titres accrocheurs** : Les idées générées incluent des titres optimisés SEO
2. **Tags pertinents** : Les keywords sont automatiquement générés
3. **Descriptions détaillées** : Templates professionnels inclus
4. **Publication régulière** : Utilisez le mode `ideas` pour planifier à l'avance

## 🐛 Dépannage

### Erreur "API key missing"

Vérifiez que votre fichier `.env` existe et contient les clés correctes.

### Erreur Meshy "Task failed"

- Vérifiez vos crédits Meshy AI
- Essayez de simplifier la description de l'idée
- Utilisez quality=low pour tester

### Modèle non généré

- Vérifiez la connexion Internet
- Augmentez le timeout dans `model_generator.py` si nécessaire
- Vérifiez les logs dans `logs/`

## 📊 Suivi et Analyse

Tous les résultats sont sauvegardés dans :
- `data/ideas/*.json` - Idées générées avec statuts
- `data/pipeline_results_*.json` - Résultats complets de chaque exécution

Vous pouvez analyser ces fichiers pour :
- Suivre quelles idées ont été transformées en modèles
- Identifier les catégories les plus populaires
- Optimiser vos workflows futurs

## 🔐 Sécurité

- ⚠️ **Ne commitez JAMAIS votre fichier `.env`**
- Les clés API sont sensibles - gardez-les secrètes
- Le `.gitignore` est configuré pour protéger vos données

## 📝 Licence

[Ajoutez votre licence ici]

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📞 Support

Pour des questions ou problèmes :
- Ouvrez une issue sur GitHub
- Consultez la documentation des APIs utilisées
- Vérifiez les logs dans `logs/`

## 🎉 Bon à Savoir

- Le système utilise **Claude Haiku** par défaut pour minimiser les coûts
- Les modèles sont générés en **mode preview** pour économiser des crédits Meshy
- Vous pouvez **éditer les idées** avant de générer les modèles
- Les uploads sont **semi-automatiques** (packages prêts à l'emploi)
- Tout est **sauvegardé localement** pour référence future

---

**Créé avec ❤️ pour automatiser la création de contenu 3D de qualité à moindre coût**
