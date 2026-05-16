# Carousel Templates Engine 🎨

Engine for generating social media carousels with MultiCA integration.

## 📁 Structure du dépôt
```text
carousel-templates/
├── README.md                          # Instructions pour l'agent
├── schemas/
│   └── brief_schema.json              # Format attendu du brief (ce que l'agent envoie)
├── templates/
│   └── lessons/                       # Thème correspondant à vos exemples
│       ├── slide_intro.png            # Image de fond pour l’accroche
│       ├── slide_paragraph.png        # Fond pour paragraphe (titre + texte)
│       ├── slide_bullets.png          # Fond pour liste à puces
│       ├── slide_cta.png              # Fond pour appel à l’action
│       └── zones.json                 # Définition des zones de texte (coordonnées, polices, etc.)
├── fonts/                             # Polices utilisées
│   ├── PlayfairDisplay-Bold.ttf
│   ├── PlayfairDisplay-Regular.ttf
│   ├── Montserrat-Bold.ttf
│   ├── Montserrat-Regular.ttf
│   └── Montserrat-Italic.ttf
├── scripts/
│   ├── render.py                      # Superposition du texte sur l’image
│   ├── export.py                      # Redimensionnement pour Instagram / LinkedIn
│   └── utils/
│       └── text_wrap.py               # Gestion des retours à la ligne / puces
├── examples/                          # Briefs d’exemple (pour tester)
│   ├── lessons_7.json                 # Exemple basé sur votre slide 12.png
│   └── trend_2026.json
├── output/                            # Dossier de sortie (ignoré par Git)
│   ├── instagram/
│   └── linkedin/
├── requirements.txt                   # Pillow, etc.
└── .gitignore
```

## 🔡 Fonts
Le moteur supporte l'utilisation de polices personnalisées stockées dans le dossier `fonts/`.
Actuellement incluses :
- **Montserrat** : Moderne et lisible.
- **Playfair Display** : Élégant pour les titres.

## 🔧 Usage
```bash
# 1. Générer les slides brutes
python scripts/render.py --brief examples/lessons_7.json --output_dir output/

# 2. Exporter pour Instagram
python scripts/export.py --input output/ --output final/instagram --platform instagram

# 3. Exporter pour LinkedIn
python scripts/export.py --input output/ --output final/linkedin --platform linkedin
```
