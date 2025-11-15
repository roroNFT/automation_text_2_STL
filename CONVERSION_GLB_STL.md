# Conversion GLB vers STL

## 📋 Format des Fichiers

**Meshy AI génère des fichiers GLB**, pas STL. Voici pourquoi et comment convertir :

### Pourquoi GLB ?

- **GLB** (GL Transmission Format Binary) : Format moderne, compact, supporte textures et couleurs
- **STL** (STereoLithography) : Format ancien, universellement supporté par les slicers 3D

### Compatibilité

La plupart des slicers modernes supportent **les deux** :
- ✓ **PrusaSlicer** : GLB et STL
- ✓ **Cura** : GLB et STL
- ✓ **Bambu Studio** : GLB et STL
- ✓ **Simplify3D** : GLB et STL

**Vous n'avez probablement pas besoin de convertir !**

## 🔄 Conversion Automatique

Si vous avez vraiment besoin de STL, utilisez le script fourni :

### Installation

```bash
# Installer la dépendance pour la conversion
pip install trimesh
```

### Utilisation

#### Convertir un seul fichier

```bash
cd src
python convert_glb_to_stl.py ../data/models/mon_modele.glb
```

Cela créera `mon_modele.stl` dans le même dossier.

#### Convertir avec un nom de sortie spécifique

```bash
python convert_glb_to_stl.py ../data/models/input.glb -o ../data/models/output.stl
```

#### Convertir TOUS les GLB d'un dossier

```bash
python convert_glb_to_stl.py ../data/models/
```

Cela créera un fichier STL pour chaque fichier GLB trouvé.

### Exemple Complet

```bash
# 1. Générer des modèles 3D
python main.py --mode full --num-ideas 3 --quality medium

# 2. Attendre que les modèles soient générés
# Les GLB seront dans: ../data/models/

# 3. Convertir tous les GLB en STL
python convert_glb_to_stl.py ../data/models/

# Résultat:
# data/models/
#   ├── Organizer_001.glb
#   ├── Organizer_001.stl  ← Nouveau!
#   ├── Phone_Stand_002.glb
#   └── Phone_Stand_002.stl  ← Nouveau!
```

## 🛠️ Alternatives de Conversion

### 1. Blender (Open Source)

```bash
# Installer Blender
sudo apt install blender  # Linux
brew install --cask blender  # Mac
# Windows: télécharger depuis blender.org

# Ouvrir Blender → File → Import → glTF 2.0 (.glb)
# Puis: File → Export → STL (.stl)
```

### 2. Outils en Ligne (Gratuits)

- https://products.aspose.app/3d/conversion/glb-to-stl
- https://imagetostl.com/convert/file/glb/to/stl
- https://anyconv.com/glb-to-stl-converter/
- https://convertio.co/glb-stl/

### 3. MeshLab (Open Source)

```bash
# Installer MeshLab
sudo apt install meshlab

# Utilisation
meshlab mon_modele.glb
# File → Export Mesh As → STL
```

## 📊 Comparaison des Formats

| Caractéristique | GLB | STL |
|----------------|-----|-----|
| Support des couleurs | ✓ Oui | ✗ Non |
| Support des textures | ✓ Oui | ✗ Non |
| Taille de fichier | Plus petit | Plus grand |
| Support slicer | Moderne | Universel |
| Format | Binaire | Texte ou binaire |

## ❓ FAQ

### Puis-je imprimer directement un GLB ?

**Oui !** La plupart des slicers modernes acceptent les GLB. Testez d'abord avec votre slicer avant de convertir.

### La conversion perd-elle de la qualité ?

**Non**, la géométrie 3D est préservée. Seules les textures et couleurs sont perdues (STL ne les supporte pas).

### Quel format poster sur Printables/MakerWorld ?

Les deux plateformes acceptent **GLB et STL**. GLB est préférable car :
- Fichiers plus petits
- Meilleur rendu des previews
- Supporte les couleurs

### Mon slicer ne lit pas les GLB, que faire ?

Utilisez le script de conversion fourni ou mettez à jour votre slicer vers une version récente.

## 🔧 Intégration au Pipeline

Vous pouvez automatiser la conversion en modifiant `src/model_generator.py` pour convertir automatiquement après chaque génération.

Exemple d'ajout (ligne 120 environ) :

```python
# Dans model_generator.py, après le téléchargement
def _download_model(self, model_data: Dict, idea: Dict) -> Path:
    # ... code existant ...

    # Conversion automatique vers STL
    try:
        import trimesh
        stl_path = filepath.with_suffix('.stl')
        mesh = trimesh.load(str(filepath))
        mesh.export(str(stl_path))
        print(f"✓ STL créé: {stl_path}")
    except Exception as e:
        print(f"⚠️  Conversion STL échouée: {e}")

    return filepath
```

## 📝 Notes Importantes

- Les fichiers GLB de Meshy AI sont **optimisés pour l'impression 3D**
- La conversion ne modifie pas la géométrie, seulement le format
- STL est un format plus ancien mais plus universel
- GLB est recommandé pour les uploads sur les plateformes modernes

---

**Besoin d'aide ?** Consultez TROUBLESHOOTING.md ou ouvrez une issue.
