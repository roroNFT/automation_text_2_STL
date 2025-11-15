# Guide Crédits Meshy AI

## ❌ Erreur 402 : Payment Required

Cette erreur signifie que votre compte Meshy AI n'a pas (ou plus) de crédits disponibles.

## 🔍 Vérifier Vos Crédits

1. **Connectez-vous** : https://app.meshy.ai/
2. **Dashboard** : Vos crédits sont affichés en haut à droite
3. **Historique** : Voir vos générations précédentes

## 💰 Plans Meshy AI

### Plan Gratuit (Free)
- **200 crédits** offerts à l'inscription
- Parfait pour tester (~10-20 modèles)
- **Qualité** : Preview mode (~10-20 crédits/modèle)
- **Renouvellement** : Non, crédits uniques

### Plan Starter (~$16/mois)
- **1000 crédits/mois**
- ~50-100 modèles en preview mode
- ~10-20 modèles en refine mode
- Idéal pour démarrer une production régulière

### Plan Professional (~$40/mois)
- **3000 crédits/mois**
- ~150-300 modèles en preview
- ~30-60 modèles en refine
- Pour production intensive

### Crédits à la Carte
- Possibilité d'acheter des crédits supplémentaires
- Vérifiez les tarifs sur : https://app.meshy.ai/pricing

## 📊 Consommation de Crédits

### Mode Preview (Par défaut dans notre système)
- **Coût** : ~10-20 crédits par modèle
- **Temps** : 2-4 minutes
- **Qualité** : Bonne, suffisante pour 90% des cas
- **Recommandé** : ✓ Oui, meilleur rapport qualité/prix

### Mode Refine (Haute qualité)
- **Coût** : ~50-100 crédits par modèle
- **Temps** : 5-10 minutes
- **Qualité** : Excellente, détails fins
- **Recommandé** : Uniquement pour modèles premium

## 🎯 Optimiser Vos Crédits

### 1. Générez d'abord les Idées
```bash
# Génère 20 idées pour ~$0.05 (Claude API)
python main.py --mode ideas --num-ideas 20
```

### 2. Sélectionnez Manuellement les Meilleures
- Ouvrez le fichier JSON généré
- Gardez uniquement les 5-10 meilleures idées
- Supprimez ou commentez les autres

### 3. Générez Uniquement les Modèles Sélectionnés
```bash
# Génère les modèles pour les idées sélectionnées
python main.py --mode models --ideas-file ../data/ideas/selected_ideas.json --quality medium
```

### 4. Utilisez Preview Mode (Par défaut)
Notre système utilise déjà le preview mode pour économiser les crédits.

## 💡 Stratégies Économiques

### Budget Serré (~200 crédits gratuits)
```bash
# Générer 50 idées
python main.py --mode ideas --num-ideas 50

# Sélectionner manuellement les 10 meilleures

# Générer 10 modèles en preview
python main.py --mode models --ideas-file selected.json --quality medium

# Résultat : 10 objets 3D prêts à publier
# Coût : ~100-200 crédits Meshy + ~$0.10 Claude
```

### Budget Moyen (Plan Starter - 1000 crédits/mois)
```bash
# Batch hebdomadaire : 10-12 objets/semaine

# Lundi : 30 idées
python main.py --mode ideas --num-ideas 30

# Mardi-Jeudi : 10 modèles/semaine
python main.py --mode models --ideas-file weekly_selection.json

# Résultat : ~40 objets/mois
# Coût : ~800-1000 crédits + ~$2 Claude = ~$18/mois total
```

### Production Intensive (Plan Pro - 3000 crédits/mois)
```bash
# 2-3 objets/jour

# Daily batch
python main.py --mode full --num-ideas 3 --quality medium

# Résultat : ~70 objets/mois
# Coût : ~1400-2100 crédits + ~$5 Claude = ~$45/mois total
```

## 🆓 Alternatives Gratuites/Moins Chères

Si vous ne voulez pas payer Meshy AI :

### 1. Tripo AI
- **Site** : https://www.tripo3d.ai/
- **Gratuit** : Crédits gratuits à l'inscription
- **Qualité** : Comparable à Meshy
- **API** : Disponible

### 2. Luma AI Genie
- **Site** : https://lumalabs.ai/genie
- **Gratuit** : Limité mais disponible
- **Qualité** : Bonne
- **API** : Limitée

### 3. Shap-E (OpenAI)
- **Site** : https://github.com/openai/shap-e
- **Gratuit** : 100% gratuit (open source)
- **Qualité** : Moyenne
- **API** : Local, nécessite GPU

### 4. Génération Manuelle
Utilisez uniquement la génération d'idées et créez les modèles avec :
- **Blender** (gratuit)
- **Fusion 360** (gratuit pour hobbyistes)
- **Tinkercad** (gratuit, en ligne)

## 📝 Workflow Idéal

### Phase 1 : Exploration (Gratuit)
```bash
# Générer beaucoup d'idées
python main.py --mode ideas --num-ideas 100

# Coût : ~$0.20 Claude API
# Temps : 2 minutes
```

### Phase 2 : Sélection (Manuel)
- Lire les 100 idées
- Identifier les 20 meilleures
- Créer un nouveau JSON avec uniquement ces 20

### Phase 3 : Production (Avec crédits)
```bash
# Générer les 20 modèles
python main.py --mode models --ideas-file top20.json --quality medium

# Coût : ~200-400 crédits Meshy
# Temps : ~1 heure
```

### Phase 4 : Publication
Les packages d'upload sont créés automatiquement dans `data/uploads/`

## ❓ FAQ

### J'ai utilisé mes 200 crédits gratuits, que faire ?

**Options** :
1. Acheter un plan payant si vous êtes satisfait
2. Utiliser une alternative (Tripo AI, Luma)
3. Créer les modèles manuellement avec Blender
4. Générer uniquement des idées et vendre les concepts

### Combien coûte réellement 1 objet publié ?

**Avec Meshy Preview** :
- Idée : ~$0.002 (Claude)
- Modèle 3D : ~15 crédits Meshy (~$0.24 avec plan Starter)
- **Total : ~$0.25/objet**

**Avec Meshy Refine** :
- Idée : ~$0.002
- Modèle 3D : ~75 crédits (~$1.20)
- **Total : ~$1.20/objet**

### Est-ce rentable ?

**Si vous monétisez sur Printables/MakerWorld** :
- Objets populaires : 100-1000+ téléchargements
- Donations moyennes : $0.50-5/objet
- Avec 10-20 objets populaires : ROI positif
- Avec 50+ objets : Revenus réguliers possibles

### Puis-je mixer plusieurs services ?

**Oui !** Vous pouvez :
- Générer les idées avec notre système (Claude)
- Créer certains modèles avec Meshy
- Créer d'autres avec Tripo AI
- Créer d'autres manuellement

## 🔗 Liens Utiles

- **Meshy AI Dashboard** : https://app.meshy.ai/
- **Meshy AI Pricing** : https://app.meshy.ai/pricing
- **Meshy AI Documentation** : https://docs.meshy.ai/
- **API Status** : https://status.meshy.ai/

## 🆘 Support

Besoin d'aide ?
- Consultez TROUBLESHOOTING.md
- Ouvrez une issue sur GitHub
- Contactez le support Meshy : https://app.meshy.ai/

---

**Astuce** : Commencez avec le plan gratuit (200 crédits) pour tester, puis passez au plan Starter si vous êtes satisfait des résultats.
