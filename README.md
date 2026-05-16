# Carousel Templates Engine 🎨

Engine for generating social media carousels with MultiCA integration.

## 📁 Structure
```text
carousel-templates/
├── fonts/                      # Polices de caractères (Montserrat, Playfair Display)
├── templates/                  # Thèmes et zones de texte
├── schemas/                    # Validation des briefs
├── scripts/                    # Logique de rendu et export
└── output/                     # Résultats générés
```

## 🔡 Fonts
Le moteur supporte l'utilisation de polices personnalisées stockées dans le dossier `fonts/`.
Actuellement incluses :
- **Montserrat** : Moderne et lisible, idéal pour le corps de texte.
- **Playfair Display** : Élégant, parfait pour les titres (headlines).

Pour utiliser une police dans `zones.json`, spécifiez le chemin relatif depuis le dossier `fonts/` (ex: `Montserrat/Montserrat-Bold.ttf`).

## 🔧 Usage
```bash
python scripts/render.py --brief brief.json --output output/slide_01.png
```
