"""
Base de données locale des références technico-économiques du cacao.
Local database of cocoa technical-economic references (Edge-compatible, no Internet needed).

Ces valeurs sont indicatives et doivent être ajustées avec les données de terrain
réelles collectées via Kobo Toolbox / l'observatoire des EFA.
"""

# Typologies de parcelles de cacao (selon le document de référence)
COCOA_PLOT_TYPES = [
    "Cacaoyer + culture annuelle en production",
    "Cacaoyer + culture pérenne en production",
    "Cacaoyer sous ombrage en production",
    "Cacaoyer plein en production",
    "Cacaoyer jeune",
    "Cacaoyer jeune sous ombrage",
]

# Fiches technico-économiques de référence par typologie de parcelle
# (rendement kg/ha, prix moyen FCFA/kg, charges opérationnelles de référence FCFA/ha)
REFERENCE_SHEETS = [
    {
        "typology": "Cacaoyer + culture annuelle en production",
        "yield_kg_ha": 650,
        "price_fcfa_kg": 1200,
        "operational_costs_fcfa_ha": 280000,
        "labor_hj_ha": 145,
        "notes_fr": "Association avec cultures vivrières annuelles (igname, maïs, arachide).",
        "notes_en": "Intercropped with annual food crops (yam, maize, groundnut).",
    },
    {
        "typology": "Cacaoyer + culture pérenne en production",
        "yield_kg_ha": 700,
        "price_fcfa_kg": 1200,
        "operational_costs_fcfa_ha": 300000,
        "labor_hj_ha": 150,
        "notes_fr": "Association avec cultures pérennes (palmier, fruitiers).",
        "notes_en": "Intercropped with perennial crops (oil palm, fruit trees).",
    },
    {
        "typology": "Cacaoyer sous ombrage en production",
        "yield_kg_ha": 550,
        "price_fcfa_kg": 1250,
        "operational_costs_fcfa_ha": 250000,
        "labor_hj_ha": 135,
        "notes_fr": "Conduite agroforestière, ombrage diversifié favorable à la durabilité.",
        "notes_en": "Agroforestry management, diversified shade favorable to sustainability.",
    },
    {
        "typology": "Cacaoyer plein en production",
        "yield_kg_ha": 850,
        "price_fcfa_kg": 1200,
        "operational_costs_fcfa_ha": 350000,
        "labor_hj_ha": 160,
        "notes_fr": "Verger en plein soleil, forte intensification, charges plus élevées.",
        "notes_en": "Full-sun orchard, higher intensification, higher costs.",
    },
    {
        "typology": "Cacaoyer jeune",
        "yield_kg_ha": 150,
        "price_fcfa_kg": 1200,
        "operational_costs_fcfa_ha": 200000,
        "labor_hj_ha": 120,
        "notes_fr": "Plantation en phase d'installation, rendement faible, entretien important.",
        "notes_en": "Young plantation, low yield, significant establishment maintenance.",
    },
    {
        "typology": "Cacaoyer jeune sous ombrage",
        "yield_kg_ha": 120,
        "price_fcfa_kg": 1250,
        "operational_costs_fcfa_ha": 180000,
        "labor_hj_ha": 115,
        "notes_fr": "Jeune plantation agroforestière, croissance progressive du rendement.",
        "notes_en": "Young agroforestry plantation, gradually increasing yield.",
    },
]

# Itinéraire technique de référence (Homme-jour / ha) pour une parcelle "plein en production"
REFERENCE_ITINERARY = {
    "operations": [
        "Défrichage",
        "Récolte sanitaire",
        "Taille de restauration",
        "Taille d'entretien",
        "Fertilisation",
        "Traitement fongique",
        "Traitement insecticide",
        "Récolte des cabosses",
        "Écabossage",
        "Fermentation",
        "Transport des fèves",
        "Séchage",
        "Conditionnement",
    ],
    "operations_en": [
        "Land clearing",
        "Sanitary harvest",
        "Rehabilitation pruning",
        "Maintenance pruning",
        "Fertilization",
        "Fungicide treatment",
        "Insecticide treatment",
        "Pod harvest",
        "Pod breaking",
        "Fermentation",
        "Bean transport",
        "Drying",
        "Packaging",
    ],
    # Répartition mensuelle indicative (Homme-jour / ha), 12 valeurs Jan->Déc
    "monthly_hj": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],     # Défrichage
        [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     # Récolte sanitaire
        [0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],     # Taille de restauration
        [0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0],     # Taille d'entretien
        [0, 6, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],     # Fertilisation
        [0, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0],     # Traitement fongique
        [0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0],     # Traitement insecticide
        [10, 10, 5, 0, 0, 0, 0, 5, 10, 12, 12, 8], # Récolte des cabosses
        [8, 8, 4, 0, 0, 0, 0, 4, 8, 10, 10, 6],   # Écabossage
        [6, 6, 3, 0, 0, 0, 0, 3, 6, 7, 7, 4],     # Fermentation
        [3, 3, 2, 0, 0, 0, 0, 2, 3, 4, 4, 2],     # Transport des fèves
        [6, 6, 3, 0, 0, 0, 0, 3, 6, 7, 7, 4],     # Séchage
        [3, 3, 1, 0, 0, 0, 0, 1, 3, 3, 3, 2],     # Conditionnement
    ],
}

# Pays / régions pré-renseignés (exemple Cameroun - filière cacao)
COUNTRIES = ["Cameroun", "Côte d'Ivoire", "Ghana", "Nigeria", "Togo", "Autre / Other"]

PRODUCTION_SYSTEMS = [
    "Cacao dominant",
    "Cacao + cultures vivrières",
    "Cacao + cultures pérennes associées",
    "Cacao + élevage",
    "Polyculture diversifiée",
    "Autre / Other",
]


def get_reference_for_typology(typology: str):
    """Return the reference factsheet dict matching a given plot typology."""
    for sheet in REFERENCE_SHEETS:
        if sheet["typology"] == typology:
            return sheet
    return None
