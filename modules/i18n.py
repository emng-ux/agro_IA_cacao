"""
Module d'internationalisation (FR/EN) pour l'agent IA agropastoral cacao.
Bilingual (FR/EN) translation module for the cocoa agro-pastoral AI agent.
"""

TRANSLATIONS = {
    "fr": {
        "app_title": "Agent IA Agropastoral - Filière Cacao",
        "tagline": "Diagnostic, analyse stratégique et financière des exploitations cacaoyères",
        "nav_home": "Accueil",
        "nav_collecte": "Collecte de données (EFA)",
        "nav_financier": "Diagnostic financier",
        "nav_strategique": "Analyse stratégique",
        "nav_references": "Références technico-économiques",
        "nav_plan": "Plan stratégique & opérationnel",
        "nav_about": "À propos",
        "offline_mode": "Mode Edge (hors-ligne)",
        "online_mode": "Mode connecté (en ligne)",
        "language": "Langue",

        # Home
        "welcome_title": "Bienvenue dans l'Agent IA Agropastoral Cacao",
        "welcome_text": (
            "Cet outil aide les conseillers agropastoraux à accompagner les producteurs "
            "de cacao dans le diagnostic, l'analyse stratégique et financière de leurs "
            "exploitations familiales agropastorales (EFA). Il fonctionne en ligne ou "
            "en mode Edge (sans connexion Internet), avec une base de données locale "
            "des références technico-économiques du cacao."
        ),
        "quickstart": "Démarrage rapide",
        "step1": "1. Renseignez les informations générales et de l'EFA dans 'Collecte de données'.",
        "step2": "2. Consultez le 'Diagnostic financier' pour les marges, EBE, VA, trésorerie...",
        "step3": "3. Utilisez 'Analyse stratégique' pour SWOT, étoile du conseil, PESTEL, etc.",
        "step4": "4. Générez un plan stratégique et opérationnel à valider avec le conseiller.",
        "saved_efas": "EFA enregistrées",
        "no_efa": "Aucune EFA enregistrée pour le moment.",

        # Collecte
        "collecte_title": "Collecte de données - Fiche EFA",
        "section_identification": "Identification",
        "section_efa": "Exploitation Familiale Agropastorale (EFA)",
        "section_cacao": "Activité cacao",
        "country": "Pays",
        "region": "Région",
        "department": "Département",
        "arrondissement": "Arrondissement",
        "locality": "Localité",
        "code_region": "Code Région",
        "code_department": "Code Département",
        "code_arrondissement": "Code Arrondissement",
        "production_system": "Système de production",
        "activity": "Activité",
        "code_system": "Code système de production",
        "code_activity": "Code activité",
        "code_efa": "Code EFA",
        "code_op": "Code OP",
        "op_member": "Membre de l'OP",
        "yes": "Oui",
        "no": "Non",

        "surface_ha": "Surface (ha)",
        "surface_owned": "Surface dont propriété (ha)",
        "surface_used": "Surface utilisée (ha)",
        "uth_exploitant": "UTH exploitant",
        "uth_salarie": "UTH salarié",

        "cacao_typology": "Typologie des parcelles de cacao",
        "cacao_surface": "Surface cacao (ha)",
        "qty_total": "Quantité totale (kg) - produit brut",
        "qty_sold_op": "Quantité vendue à l'OP (kg)",
        "qty_sold_third": "Quantité vendue aux tiers (kg)",
        "yield_ha": "Rendement (kg/ha)",
        "price_op": "Prix moyen de vente OP (FCFA/kg)",
        "price_third": "Prix moyen de vente tiers (FCFA/kg)",

        "save_efa": "Enregistrer la fiche EFA",
        "efa_saved": "Fiche EFA enregistrée avec succès.",
        "load_efa": "Charger une EFA enregistrée",
        "select_efa": "Sélectionner une EFA",

        # Financier
        "financier_title": "Diagnostic financier de l'exploitation",
        "no_data_warning": "Veuillez d'abord saisir ou charger une fiche EFA dans 'Collecte de données'.",
        "produit_brut_section": "Produits bruts",
        "charges_op_section": "Charges opérationnelles",
        "charges_structure_section": "Charges de structure",
        "bilan_section": "Bilan (actif / passif)",
        "results_section": "Résultats calculés",

        "pb_vegetal": "Produit brut végétal (FCFA)",
        "pb_animal": "Produit brut animal (FCFA)",
        "pb_acs": "Produit brut ACS (FCFA)",
        "pb_immo": "Production immobilisée (FCFA)",
        "subventions": "Subventions d'exploitation (FCFA)",
        "indemnites": "Indemnités d'exploitation (FCFA)",
        "autres_produits": "Autres produits d'exploitation (FCFA)",

        "engrais": "Engrais (FCFA)",
        "semences": "Semences et plants (FCFA)",
        "phyto": "Produits de défense des végétaux (FCFA)",
        "aliments_betail": "Aliments du bétail (FCFA)",
        "veto": "Produits vétérinaires (FCFA)",
        "energie": "Combustible / énergie (FCFA)",
        "emballages": "Emballages et plastiques (FCFA)",
        "autres_matieres": "Autres matières premières (FCFA)",
        "travaux_tiers_veg": "Travaux par tiers - végétal (FCFA)",
        "travaux_tiers_ani": "Travaux par tiers - animal (FCFA)",
        "location_animaux": "Location/achat animaux (FCFA)",

        "services_exterieurs": "Services extérieurs",
        "approvisionnements": "Approvisionnements",
        "eau_gaz": "Eau, gaz, électricité (FCFA)",
        "petits_equip": "Petits équipements (FCFA)",
        "autres_fournitures": "Autres fournitures (FCFA)",
        "credit_bail": "Crédit-bail (FCFA)",
        "locations": "Locations et charges locatives (FCFA)",
        "entretien": "Entretien et réparation (FCFA)",
        "assurances": "Primes d'assurance (FCFA)",
        "cotisations": "Cotisations professionnelles (FCFA)",
        "transport": "Transports et déplacements (FCFA)",
        "autres_services": "Autres services extérieurs (FCFA)",
        "impots": "Impôts et taxes (FCFA)",

        "remuneration": "Rémunération du personnel (FCFA)",
        "charges_sociales_pers": "Charges sociales du personnel (FCFA)",
        "charges_sociales_exploit": "Charges sociales exploitant (FCFA)",
        "amortissements": "Amortissements (FCFA)",
        "interets": "Intérêts et emprunts (FCFA)",
        "autres_agios": "Autres agios et frais financiers (FCFA)",

        "actif_circulant_label": "Actif circulant (FCFA)",
        "dettes_ct": "Dettes financières court terme (FCFA)",
        "stocks": "Total des stocks et en-cours (FCFA)",
        "creances": "Total des valeurs réalisables (FCFA)",
        "tresorerie_actif": "Banque + Caisse (FCFA)",
        "capitaux_propres": "Capitaux propres (FCFA)",
        "dettes_lmt": "Dettes financières long et moyen terme (FCFA)",
        "actif_immobilise": "Total immobilisations (FCFA)",

        "calc_button": "Calculer les indicateurs",

        # Result labels
        "res_produit_brut_total": "Produit brut total",
        "res_charges_op_total": "Total charges opérationnelles",
        "res_marge_brute": "Marge brute globale (avant main d'œuvre)",
        "res_cout_kg": "Coût de production du kg de cacao",
        "res_prix_revient_kg": "Prix de revient du kg de cacao",
        "res_seuil_rentabilite": "Seuil de rentabilité (ligne rouge) (FCFA/kg)",
        "res_charges_structure": "Total charges de structure",
        "res_amortissements": "Dotations aux amortissements",
        "res_valeur_ajoutee": "Valeur ajoutée (VA)",
        "res_va_ha": "VA par hectare",
        "res_va_uth": "VA par UTH exploitant",
        "res_ebe": "Excédent Brut d'Exploitation (EBE)",
        "res_ebe_ha": "EBE par hectare",
        "res_ebe_uth": "EBE par UTH exploitant",
        "res_charges_mo": "Charges de main d'œuvre",
        "res_charges_mo_ha": "Charges de main d'œuvre par ha",
        "res_amort_ha": "Amortissements par ha",
        "res_charges_financieres": "Charges financières",
        "res_resultat_courant": "Résultat courant",
        "res_resultat_ha": "Résultat courant par ha",
        "res_resultat_uth": "Résultat courant par UTH exploitant",
        "res_services_ext_total": "Total services extérieurs",
        "res_services_ext_ha": "Services extérieurs par ha",
        "res_approvisionnements_total": "Total approvisionnements",
        "res_approvisionnements_ha": "Approvisionnements par ha",
        "res_fdr": "Fonds de roulement (FDR)",
        "res_bfr": "Besoin en fonds de roulement (BFR)",
        "res_tresorerie": "Trésorerie",
        "res_actif_circulant": "Actif circulant",
        "res_ratio_liquidite": "Ratio de liquidité (actif circulant / dettes CT)",

        "interpretation_title": "Interprétation automatique",
        "interpretation_good": "Situation favorable : la marge brute couvre les charges et le résultat courant est positif.",
        "interpretation_warning": "Situation fragile : le résultat courant est faible ou négatif. Une analyse approfondie est recommandée.",
        "interpretation_below_threshold": "Attention : le coût de production dépasse le seuil de rentabilité (ligne rouge). La parcelle de cacao n'est pas rentable au prix de vente actuel.",
        "interpretation_above_threshold": "Le prix de vente couvre le coût de production : la parcelle est rentable.",
        "interpretation_liquidity_good": "Le ratio de liquidité est satisfaisant (>1).",
        "interpretation_liquidity_bad": "Le ratio de liquidité est inférieur à 1 : risque de tension de trésorerie à court terme.",

        # Stratégique
        "strategique_title": "Analyse stratégique de l'exploitation",
        "tool_select": "Choisir l'outil d'analyse",
        "etoile_conseil": "Étoile du conseil",
        "swot": "SWOT (FFOM)",
        "pestel": "PESTEL",
        "porter": "5 forces de Porter",
        "bcg": "Matrice BCG",
        "ansoff": "Matrice Ansoff",

        "etoile_intro": "Évaluez chaque branche de 1 (très faible) à 5 (très fort).",
        "etoile_moyens": "Moyens de production",
        "etoile_perf": "Performances technico-économiques",
        "etoile_finances": "Finances",
        "etoile_milieu": "Milieu local",
        "etoile_politiques": "Politiques publiques",
        "etoile_marches": "Marchés / filières",
        "generate_radar": "Générer le diagramme radar",

        "swot_intro": "Listez les éléments du diagnostic SWOT (un par ligne).",
        "swot_forces": "Forces",
        "swot_faiblesses": "Faiblesses",
        "swot_opportunites": "Opportunités",
        "swot_menaces": "Menaces",

        "pestel_intro": "Analysez les facteurs externes (un par ligne).",
        "pestel_politique": "Politique",
        "pestel_economique": "Économique",
        "pestel_social": "Socioculturel",
        "pestel_techno": "Technologique",
        "pestel_environnement": "Environnemental",
        "pestel_legal": "Légal",

        "porter_intro": "Évaluez l'intensité de chaque force (1 = faible, 5 = forte) et commentez.",
        "porter_nouveaux": "Menace des nouveaux entrants",
        "porter_fournisseurs": "Pouvoir de négociation des fournisseurs",
        "porter_clients": "Pouvoir de négociation des clients",
        "porter_substituts": "Menace des produits de substitution",
        "porter_rivalite": "Intensité de la rivalité concurrentielle",

        "bcg_intro": "Positionnez chaque activité de l'EFA selon sa part de marché relative et la croissance du marché.",
        "bcg_activity": "Activité",
        "bcg_part_marche": "Part de marché relative (0-1)",
        "bcg_croissance": "Taux de croissance du marché (%)",
        "bcg_add_row": "Ajouter une activité",
        "bcg_generate": "Générer la matrice BCG",

        "ansoff_intro": "Définissez les options de croissance de l'exploitation selon la matrice Ansoff.",
        "ansoff_penetration": "Pénétration de marché (produits actuels, marchés actuels)",
        "ansoff_developpement_marche": "Développement de marché (produits actuels, nouveaux marchés)",
        "ansoff_developpement_produit": "Développement de produit (nouveaux produits, marchés actuels)",
        "ansoff_diversification": "Diversification (nouveaux produits, nouveaux marchés)",

        # References
        "references_title": "Références technico-économiques du cacao",
        "ref_intro": (
            "Base de données locale des fiches technico-économiques de production du cacao "
            "et des références régionales (rendements, prix, itinéraires techniques, charges)."
        ),
        "ref_filter_system": "Filtrer par typologie de parcelle",
        "ref_table_title": "Fiches de référence",
        "ref_itinerary_title": "Itinéraire technique de référence (Homme-jour / ha)",

        # Plan
        "plan_title": "Plan stratégique et plan opérationnel",
        "plan_intro": (
            "Sur la base du diagnostic, l'agent IA propose un projet de plan stratégique "
            "et un plan opérationnel. Ces propositions doivent être validées par le "
            "conseiller agropastoral avant transmission au producteur."
        ),
        "plan_objectifs": "Objectifs stratégiques proposés",
        "plan_actions": "Actions opérationnelles proposées",
        "plan_generate": "Générer une proposition de plan",
        "plan_validate": "Valider ce plan (conseiller agropastoral)",
        "plan_validated": "Plan validé par le conseiller. Il peut être transmis au producteur.",
        "plan_not_validated": "Ce plan est une proposition de l'agent IA et n'a pas encore été validé.",
        "plan_export": "Exporter le plan (texte)",

        # About
        "about_title": "À propos de cet agent IA",
        "about_text": (
            "Prototype d'agent IA agentique bilingue (français-anglais), conçu pour "
            "fonctionner en ligne et en mode Edge Computing (hors connexion), destiné "
            "aux conseillers agropastoraux accompagnant les producteurs de cacao en "
            "Afrique. Il intègre une base de données technico-économique locale, des "
            "outils de diagnostic stratégique et un module de diagnostic financier "
            "complet, conformément aux référentiels filière cacao."
        ),
        "about_disclaimer": (
            "Ce prototype est un outil d'aide à la décision. Toute proposition générée "
            "par l'agent IA doit être validée par le conseiller agropastoral avant "
            "transmission au producteur."
        ),
        "data_local_note": "Toutes les données saisies sont stockées localement (mode Edge compatible).",
        "footer_note": "Agent IA Agropastoral Cacao — Prototype fonctionnel",
    },

    "en": {
        "app_title": "Agro-Pastoral AI Agent - Cocoa Sector",
        "tagline": "Diagnosis, strategic and financial analysis of cocoa farms",
        "nav_home": "Home",
        "nav_collecte": "Data Collection (Farm)",
        "nav_financier": "Financial Diagnosis",
        "nav_strategique": "Strategic Analysis",
        "nav_references": "Technical-Economic References",
        "nav_plan": "Strategic & Operational Plan",
        "nav_about": "About",
        "offline_mode": "Edge Mode (offline)",
        "online_mode": "Connected Mode (online)",
        "language": "Language",

        # Home
        "welcome_title": "Welcome to the Cocoa Agro-Pastoral AI Agent",
        "welcome_text": (
            "This tool helps agro-pastoral advisors support cocoa farmers with the "
            "diagnosis, strategic and financial analysis of their family agro-pastoral "
            "farms (FAF). It works online or in Edge mode (without an Internet "
            "connection), with a local database of cocoa technical-economic references."
        ),
        "quickstart": "Quick start",
        "step1": "1. Enter general and farm information under 'Data Collection'.",
        "step2": "2. Review 'Financial Diagnosis' for margins, EBE, VA, cash position...",
        "step3": "3. Use 'Strategic Analysis' for SWOT, advisory star, PESTEL, etc.",
        "step4": "4. Generate a strategic and operational plan for advisor validation.",
        "saved_efas": "Saved farms",
        "no_efa": "No farm record saved yet.",

        # Collecte
        "collecte_title": "Data Collection - Farm Record",
        "section_identification": "Identification",
        "section_efa": "Family Agro-Pastoral Farm (FAF)",
        "section_cacao": "Cocoa activity",
        "country": "Country",
        "region": "Region",
        "department": "Department",
        "arrondissement": "District",
        "locality": "Locality",
        "code_region": "Region code",
        "code_department": "Department code",
        "code_arrondissement": "District code",
        "production_system": "Production system",
        "activity": "Activity",
        "code_system": "Production system code",
        "code_activity": "Activity code",
        "code_efa": "Farm code",
        "code_op": "Producer organization code",
        "op_member": "Member of producer organization",
        "yes": "Yes",
        "no": "No",

        "surface_ha": "Area (ha)",
        "surface_owned": "Area owned (ha)",
        "surface_used": "Area used (ha)",
        "uth_exploitant": "Family labor units",
        "uth_salarie": "Hired labor units",

        "cacao_typology": "Cocoa plot typology",
        "cacao_surface": "Cocoa area (ha)",
        "qty_total": "Total quantity (kg) - gross output",
        "qty_sold_op": "Quantity sold to PO (kg)",
        "qty_sold_third": "Quantity sold to third parties (kg)",
        "yield_ha": "Yield (kg/ha)",
        "price_op": "Average sale price to PO (FCFA/kg)",
        "price_third": "Average sale price to third parties (FCFA/kg)",

        "save_efa": "Save farm record",
        "efa_saved": "Farm record saved successfully.",
        "load_efa": "Load a saved farm",
        "select_efa": "Select a farm",

        # Financier
        "financier_title": "Financial Diagnosis of the Farm",
        "no_data_warning": "Please first enter or load a farm record in 'Data Collection'.",
        "produit_brut_section": "Gross outputs",
        "charges_op_section": "Operating costs",
        "charges_structure_section": "Structural costs",
        "bilan_section": "Balance sheet (assets / liabilities)",
        "results_section": "Computed indicators",

        "pb_vegetal": "Crop gross output (FCFA)",
        "pb_animal": "Livestock gross output (FCFA)",
        "pb_acs": "Trade/service gross output (FCFA)",
        "pb_immo": "Capitalized production (FCFA)",
        "subventions": "Operating subsidies (FCFA)",
        "indemnites": "Operating compensation (FCFA)",
        "autres_produits": "Other operating income (FCFA)",

        "engrais": "Fertilizers (FCFA)",
        "semences": "Seeds and seedlings (FCFA)",
        "phyto": "Crop protection products (FCFA)",
        "aliments_betail": "Animal feed (FCFA)",
        "veto": "Veterinary products (FCFA)",
        "energie": "Fuel / energy (FCFA)",
        "emballages": "Packaging materials (FCFA)",
        "autres_matieres": "Other raw materials (FCFA)",
        "travaux_tiers_veg": "Outsourced crop work (FCFA)",
        "travaux_tiers_ani": "Outsourced livestock work (FCFA)",
        "location_animaux": "Animal rental/purchase (FCFA)",

        "services_exterieurs": "External services",
        "approvisionnements": "Supplies",
        "eau_gaz": "Water, gas, electricity (FCFA)",
        "petits_equip": "Small equipment (FCFA)",
        "autres_fournitures": "Other supplies (FCFA)",
        "credit_bail": "Leasing (FCFA)",
        "locations": "Rentals and lease charges (FCFA)",
        "entretien": "Maintenance and repairs (FCFA)",
        "assurances": "Insurance premiums (FCFA)",
        "cotisations": "Professional dues (FCFA)",
        "transport": "Transport and travel (FCFA)",
        "autres_services": "Other external services (FCFA)",
        "impots": "Taxes and duties (FCFA)",

        "remuneration": "Staff remuneration (FCFA)",
        "charges_sociales_pers": "Staff social charges (FCFA)",
        "charges_sociales_exploit": "Farmer's social charges (FCFA)",
        "amortissements": "Depreciation (FCFA)",
        "interets": "Loan interest (FCFA)",
        "autres_agios": "Other financial charges (FCFA)",

        "actif_circulant_label": "Current assets (FCFA)",
        "dettes_ct": "Short-term financial debts (FCFA)",
        "stocks": "Total inventories and WIP (FCFA)",
        "creances": "Total receivables (FCFA)",
        "tresorerie_actif": "Bank + cash (FCFA)",
        "capitaux_propres": "Equity (FCFA)",
        "dettes_lmt": "Long/medium-term financial debts (FCFA)",
        "actif_immobilise": "Total fixed assets (FCFA)",

        "calc_button": "Compute indicators",

        # Result labels
        "res_produit_brut_total": "Total gross output",
        "res_charges_op_total": "Total operating costs",
        "res_marge_brute": "Overall gross margin (before labor)",
        "res_cout_kg": "Production cost per kg of cocoa",
        "res_prix_revient_kg": "Full cost per kg of cocoa",
        "res_seuil_rentabilite": "Profitability threshold (red line) (FCFA/kg)",
        "res_charges_structure": "Total structural costs",
        "res_amortissements": "Depreciation allowances",
        "res_valeur_ajoutee": "Value added (VA)",
        "res_va_ha": "VA per hectare",
        "res_va_uth": "VA per family labor unit",
        "res_ebe": "Gross Operating Surplus (EBE)",
        "res_ebe_ha": "EBE per hectare",
        "res_ebe_uth": "EBE per family labor unit",
        "res_charges_mo": "Labor costs",
        "res_charges_mo_ha": "Labor costs per ha",
        "res_amort_ha": "Depreciation per ha",
        "res_charges_financieres": "Financial charges",
        "res_resultat_courant": "Current result",
        "res_resultat_ha": "Current result per ha",
        "res_resultat_uth": "Current result per family labor unit",
        "res_services_ext_total": "Total external services",
        "res_services_ext_ha": "External services per ha",
        "res_approvisionnements_total": "Total supplies",
        "res_approvisionnements_ha": "Supplies per ha",
        "res_fdr": "Working capital (FDR)",
        "res_bfr": "Working capital requirement (BFR)",
        "res_tresorerie": "Cash position",
        "res_actif_circulant": "Current assets",
        "res_ratio_liquidite": "Liquidity ratio (current assets / short-term debt)",

        "interpretation_title": "Automatic interpretation",
        "interpretation_good": "Favorable situation: the gross margin covers costs and the current result is positive.",
        "interpretation_warning": "Fragile situation: the current result is low or negative. Further analysis is recommended.",
        "interpretation_below_threshold": "Warning: production cost exceeds the profitability threshold (red line). The cocoa plot is not profitable at the current sale price.",
        "interpretation_above_threshold": "The sale price covers the production cost: the plot is profitable.",
        "interpretation_liquidity_good": "The liquidity ratio is satisfactory (>1).",
        "interpretation_liquidity_bad": "The liquidity ratio is below 1: short-term cash flow risk.",

        # Stratégique
        "strategique_title": "Strategic Analysis of the Farm",
        "tool_select": "Choose an analysis tool",
        "etoile_conseil": "Advisory star",
        "swot": "SWOT",
        "pestel": "PESTEL",
        "porter": "Porter's 5 forces",
        "bcg": "BCG matrix",
        "ansoff": "Ansoff matrix",

        "etoile_intro": "Rate each branch from 1 (very weak) to 5 (very strong).",
        "etoile_moyens": "Production resources",
        "etoile_perf": "Technical-economic performance",
        "etoile_finances": "Finances",
        "etoile_milieu": "Local environment",
        "etoile_politiques": "Public policies",
        "etoile_marches": "Markets / value chains",
        "generate_radar": "Generate radar chart",

        "swot_intro": "List the SWOT elements (one per line).",
        "swot_forces": "Strengths",
        "swot_faiblesses": "Weaknesses",
        "swot_opportunites": "Opportunities",
        "swot_menaces": "Threats",

        "pestel_intro": "Analyze external factors (one per line).",
        "pestel_politique": "Political",
        "pestel_economique": "Economic",
        "pestel_social": "Social",
        "pestel_techno": "Technological",
        "pestel_environnement": "Environmental",
        "pestel_legal": "Legal",

        "porter_intro": "Rate the intensity of each force (1 = low, 5 = high) and comment.",
        "porter_nouveaux": "Threat of new entrants",
        "porter_fournisseurs": "Bargaining power of suppliers",
        "porter_clients": "Bargaining power of buyers",
        "porter_substituts": "Threat of substitute products",
        "porter_rivalite": "Intensity of competitive rivalry",

        "bcg_intro": "Position each farm activity according to relative market share and market growth.",
        "bcg_activity": "Activity",
        "bcg_part_marche": "Relative market share (0-1)",
        "bcg_croissance": "Market growth rate (%)",
        "bcg_add_row": "Add an activity",
        "bcg_generate": "Generate BCG matrix",

        "ansoff_intro": "Define the farm's growth options using the Ansoff matrix.",
        "ansoff_penetration": "Market penetration (current products, current markets)",
        "ansoff_developpement_marche": "Market development (current products, new markets)",
        "ansoff_developpement_produit": "Product development (new products, current markets)",
        "ansoff_diversification": "Diversification (new products, new markets)",

        # References
        "references_title": "Cocoa Technical-Economic References",
        "ref_intro": (
            "Local database of cocoa production technical-economic factsheets and "
            "regional references (yields, prices, technical itineraries, costs)."
        ),
        "ref_filter_system": "Filter by plot typology",
        "ref_table_title": "Reference factsheets",
        "ref_itinerary_title": "Reference technical itinerary (Man-day / ha)",

        # Plan
        "plan_title": "Strategic and Operational Plan",
        "plan_intro": (
            "Based on the diagnosis, the AI agent proposes a draft strategic plan and "
            "operational plan. These proposals must be validated by the agro-pastoral "
            "advisor before being shared with the producer."
        ),
        "plan_objectifs": "Proposed strategic objectives",
        "plan_actions": "Proposed operational actions",
        "plan_generate": "Generate a plan proposal",
        "plan_validate": "Validate this plan (agro-pastoral advisor)",
        "plan_validated": "Plan validated by the advisor. It can be shared with the producer.",
        "plan_not_validated": "This plan is an AI agent proposal and has not yet been validated.",
        "plan_export": "Export plan (text)",

        # About
        "about_title": "About this AI agent",
        "about_text": (
            "Prototype of a bilingual (French-English) agentic AI agent, designed to "
            "work online and in Edge Computing mode (offline), for agro-pastoral "
            "advisors supporting cocoa farmers in Africa. It integrates a local "
            "technical-economic database, strategic diagnosis tools and a complete "
            "financial diagnosis module aligned with cocoa sector references."
        ),
        "about_disclaimer": (
            "This prototype is a decision-support tool. Any proposal generated by the "
            "AI agent must be validated by the agro-pastoral advisor before being "
            "shared with the producer."
        ),
        "data_local_note": "All entered data is stored locally (Edge-mode compatible).",
        "footer_note": "Cocoa Agro-Pastoral AI Agent — Functional prototype",
    },
}


def t(key: str, lang: str = "fr") -> str:
    """Return the translation for `key` in the given language, fallback to FR then key."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["fr"])
    return lang_dict.get(key, TRANSLATIONS["fr"].get(key, key))
