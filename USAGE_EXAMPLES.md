# Exemples d'Utilisation

Guide pratique avec des exemples concrets pour démarrer rapidement.

## 🚀 Démarrage Rapide (Linux/Mac)

```bash
# Rendre le script exécutable
chmod +x run.sh

# Générer 3 idées seulement (test gratuit)
./run.sh --mode ideas --num-ideas 3

# Générer 3 idées et leurs modèles 3D
./run.sh --mode full --num-ideas 3 --quality medium
```

## 🪟 Démarrage Rapide (Windows)

```cmd
# Générer 3 idées seulement
run.bat --mode ideas --num-ideas 3

# Générer 3 idées et leurs modèles
run.bat --mode full --num-ideas 3 --quality medium
```

## 📝 Scénarios d'Usage

### Scénario 1 : Premier Test (Gratuit)

**Objectif** : Tester le système sans coûts Meshy AI

```bash
# Générer 5 idées d'objets pratiques
./run.sh --mode ideas --num-ideas 5 --category practical
```

**Résultat** : 5 idées dans `data/ideas/` au format JSON
**Coût** : ~$0.01 (Claude API seulement)

### Scénario 2 : Production Hebdomadaire

**Objectif** : Publier 10 nouveaux objets par semaine

```bash
# Lundi : Générer 20 idées variées
./run.sh --mode ideas --num-ideas 20

# Mardi : Sélectionner manuellement les 10 meilleures dans le JSON

# Mercredi-Vendredi : Générer les modèles (par batch de 3-4)
./run.sh --mode models --ideas-file ../data/ideas/ideas_selected.json --quality medium

# Weekend : Publier sur Printables/MakerWorld
```

**Résultat** : 10 objets 3D de qualité
**Coût estimé** : ~$1-3 (20 idées + 10 modèles medium)

### Scénario 3 : Focus Gaming/Miniatures

**Objectif** : Créer une collection thématique

```bash
# Générer des idées gaming
./run.sh --mode ideas --num-ideas 15 --category gaming

# Créer les modèles en haute qualité
./run.sh --mode models --ideas-file ../data/ideas/ideas_TIMESTAMP.json --quality high
```

**Résultat** : 15 modèles gaming haute qualité
**Coût estimé** : ~$5-8 (qualité haute)

### Scénario 4 : Automation Complète

**Objectif** : Pipeline automatique du début à la fin

```bash
# Tout en une commande : idées → modèles → uploads
./run.sh --mode full --num-ideas 5 --category organization --quality medium --platforms printables makerworld
```

**Résultat** : 5 objets complets avec packages d'upload prêts
**Coût estimé** : ~$1-2

## 🎯 Par Cas d'Usage

### Pour les Débutants

```bash
# Commencer simple : 3 idées pratiques
./run.sh --mode ideas --num-ideas 3 --category practical

# Examiner le JSON généré dans data/ideas/

# Si satisfait, générer UN modèle de test
# Éditer le JSON pour ne garder qu'une idée, puis :
./run.sh --mode models --ideas-file ../data/ideas/ideas_TIMESTAMP.json --quality low
```

### Pour les Créateurs Réguliers

```bash
# Script hebdomadaire automatisé
./run.sh --mode full --num-ideas 7 --quality medium --category gifts
```

### Pour la Qualité Premium

```bash
# Workflow en 2 étapes pour contrôle qualité
./run.sh --mode ideas --num-ideas 30 --category decorative
# → Sélection manuelle des meilleures idées
./run.sh --mode models --ideas-file ../data/ideas/curated.json --quality high
```

## 📊 Optimisation des Coûts

### Budget Minimum (~$2/mois)

```bash
# 1 batch par semaine : 4 objets/mois
# Semaine 1
./run.sh --mode ideas --num-ideas 10
# → Sélection manuelle
./run.sh --mode models --ideas-file ../data/ideas/selected_week1.json --quality medium

# Répéter chaque semaine
```

**Résultat** : ~16 objets/mois
**Coût** : ~$2-3/mois

### Budget Moyen (~$10/mois)

```bash
# 2 batchs par semaine : 8 objets/semaine
# Lundi & Jeudi
./run.sh --mode full --num-ideas 4 --quality medium
```

**Résultat** : ~32 objets/mois
**Coût** : ~$8-12/mois

### Production Intensive (~$30/mois)

```bash
# Daily automation : 1-2 objets/jour haute qualité
# Chaque jour
./run.sh --mode full --num-ideas 2 --quality high --category rotating
```

**Résultat** : ~60 objets/mois
**Coût** : ~$25-35/mois

## 🔄 Workflows Avancés

### A. Test & Validation

```bash
# 1. Générer beaucoup d'idées
./run.sh --mode ideas --num-ideas 50

# 2. Analyser les idées (voir JSON)
cat data/ideas/ideas_latest.json | jq '.[] | {title, keywords}'

# 3. Créer un JSON filtré manuellement avec les meilleures

# 4. Générer modèles seulement pour les validées
./run.sh --mode models --ideas-file ../data/ideas/validated.json --quality medium
```

### B. Pipeline Multiplateforme

```bash
# Printables seulement
./run.sh --mode full --num-ideas 5 --platforms printables

# MakerWorld seulement
./run.sh --mode full --num-ideas 5 --platforms makerworld

# Les deux
./run.sh --mode full --num-ideas 5 --platforms printables makerworld
```

### C. Catégories Multiples

```bash
# Générer différentes catégories
./run.sh --mode ideas --num-ideas 5 --category practical
./run.sh --mode ideas --num-ideas 5 --category gaming
./run.sh --mode ideas --num-ideas 5 --category decorative

# Fusionner les JSONs manuellement ou avec jq
# Puis générer tous les modèles
./run.sh --mode models --ideas-file ../data/ideas/all_categories.json
```

## 📁 Gestion des Fichiers Générés

### Trouver vos Fichiers

```bash
# Dernières idées générées
ls -lt data/ideas/ | head

# Derniers modèles
ls -lt data/models/ | head

# Packages d'upload Printables
ls -lt data/uploads/printables/ | head

# Packages d'upload MakerWorld
ls -lt data/uploads/makerworld/ | head
```

### Nettoyer les Anciens Fichiers

```bash
# Sauvegarder les anciens résultats (optionnel)
mkdir archive
mv data/ideas/ideas_old_*.json archive/

# Garder seulement les 10 derniers fichiers
cd data/ideas
ls -t | tail -n +11 | xargs rm
```

## 🐍 Usage Python Direct

Si vous préférez scripter en Python :

```python
from src.idea_generator import IdeaGenerator
from src.model_generator import ModelGenerator

# Générer des idées
generator = IdeaGenerator()
ideas = generator.generate_ideas(num_ideas=5, category="gaming")
filepath = generator.save_ideas(ideas)

# Générer les modèles
model_gen = ModelGenerator()
for idea in ideas:
    result = model_gen.generate_model(idea, quality="medium")
    print(f"Model created: {result['model_path']}")
```

## 🔧 Personnalisation

### Modifier les Prompts

Éditez `src/idea_generator.py` ligne 40 pour changer le prompt de génération d'idées :

```python
prompt = f"""Generate {num_ideas} innovative 3D printable objects for {your_niche}.

Focus on:
- Your specific requirements
- Your target audience
- Your unique style

[...]
"""
```

### Créer un Script Personnalisé

```bash
#!/bin/bash
# mon_workflow.sh

# Votre workflow personnalisé
./run.sh --mode ideas --num-ideas 10 --category practical
./run.sh --mode ideas --num-ideas 10 --category gaming

# Attendre validation manuelle
echo "Review ideas and press Enter to continue..."
read

# Générer modèles pour les idées validées
./run.sh --mode models --ideas-file ../data/ideas/my_selection.json --quality high
```

## ❓ FAQ

**Q : Combien d'idées puis-je générer gratuitement ?**
R : Les idées utilisent uniquement Claude API (~$0.01 pour 5-10 idées). C'est très économique.

**Q : Quel mode qualité choisir ?**
R : `medium` pour 90% des cas. `high` pour les objets destinés à devenir très populaires.

**Q : Comment éditer les idées avant de générer les modèles ?**
R : Ouvrez le JSON dans `data/ideas/`, éditez-le, sauvegardez, puis utilisez `--mode models`.

**Q : Puis-je régénérer un modèle raté ?**
R : Oui, dans le JSON, mettez `"model_generated": false` pour l'idée concernée, puis relancez le mode `models`.

**Q : Combien de temps prend la génération ?**
R : Idées : ~30 secondes. Modèles 3D : 2-5 minutes chacun (Meshy AI).

---

**Besoin d'aide ?** Consultez le README.md principal ou ouvrez une issue sur GitHub.
