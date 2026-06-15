# 🍫 Agro IA Cacao — Agent IA Agropastoral (Filière Cacao)

Prototype fonctionnel et interactif d'un **agent IA agentique bilingue (français/anglais)**,
conçu pour fonctionner **en ligne** et **en mode Edge Computing (hors connexion Internet)**.

Il aide les conseillers agropastoraux à accompagner les producteurs de cacao dans :

- la **collecte de données** des exploitations familiales agropastorales (EFA), inspirée
  des formulaires Kobo Toolbox ;
- le **diagnostic financier** complet (produit brut, charges opérationnelles, marge brute,
  valeur ajoutée, EBE, résultat courant, FDR, BFR, trésorerie, ratio de liquidité, coût de
  production et prix de revient du kg de cacao avec seuil de rentabilité) ;
- l'**analyse stratégique** avec l'étoile du conseil (6 branches), SWOT (FFOM), PESTEL,
  les 5 forces de Porter, la matrice BCG et la matrice Ansoff ;
- la consultation d'une **base de données locale de références technico-économiques** du
  cacao (rendements, prix, charges, itinéraires techniques par typologie de parcelle) ;
- la génération (avec **validation obligatoire du conseiller**) d'un **plan stratégique et
  opérationnel**.

## 🚀 Démarrage rapide / Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

L'application s'ouvre dans le navigateur à l'adresse `http://localhost:8501`.

## 📂 Structure du projet

```
agro_IA_cacao/
├── app.py                  # Application Streamlit principale
├── requirements.txt
├── .streamlit/config.toml  # Thème
├── data/                    # Base SQLite locale (créée automatiquement, mode Edge)
└── modules/
    ├── i18n.py              # Dictionnaire de traduction FR/EN
    ├── reference_data.py    # Références technico-économiques cacao
    ├── financial_engine.py  # Moteur de calculs financiers
    └── storage.py           # Stockage local SQLite (Edge / offline)
```

## 🌐 Mode en ligne / Mode Edge

Un bouton dans la barre latérale permet de basculer entre **mode connecté** et
**mode Edge (hors-ligne)**. Toutes les données saisies sont enregistrées localement dans
`data/agro_ia_cacao.db` (SQLite), ce qui permet une utilisation complète sans connexion
Internet — adapté au terrain en zones rurales.

## 🧮 Indicateurs financiers calculés

- Produit brut total, charges opérationnelles, marge brute globale (avant main d'œuvre)
- Coût de production et prix de revient du kg de cacao, seuil de rentabilité ("ligne rouge")
- Charges de structure, amortissements, charges financières
- Valeur ajoutée (VA), VA/ha, VA/UTH
- Excédent Brut d'Exploitation (EBE), EBE/ha, EBE/UTH
- Résultat courant, résultat courant/ha, résultat courant/UTH
- Total et ratio par ha des services extérieurs et des approvisionnements
- Fonds de roulement (FDR), besoin en fonds de roulement (BFR), trésorerie
- Actif circulant et ratio de liquidité

## 🧭 Outils d'analyse stratégique

- **Étoile du conseil** (6 branches : moyens de production, performances
  technico-économiques, finances, milieu local, politiques publiques, marchés/filières)
- **SWOT / FFOM**
- **PESTEL**
- **5 forces de Porter**
- **Matrice BCG**
- **Matrice Ansoff**

## ⚠️ Avertissement

Ce prototype est un **outil d'aide à la décision**. Toute proposition (plan stratégique,
plan opérationnel) générée par l'agent IA doit être **validée par le conseiller
agropastoral** avant transmission au producteur.

## 📦 Déploiement

Compatible avec [Streamlit Community Cloud](https://streamlit.io/cloud) : connectez ce
dépôt GitHub et déployez `app.py` directement.
