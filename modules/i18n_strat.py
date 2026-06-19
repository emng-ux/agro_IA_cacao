"""
Translations for the Strategic Analysis AI Agent (OPA / EFA)
"""

TRANSLATIONS = {
    "fr": {
        # App
        "app_title": "Agent IA · Analyse Stratégique OPA / EFA",
        "tagline": "Analyse stratégique intelligente des organisations de producteurs et des exploitations familiales agricoles",
        "language": "Langue / Language",
        "footer": "Agent IA Agropastoral · Bilingue FR/EN · Données locales",

        # Sidebar
        "nav_home": "🏠 Accueil",
        "nav_import": "📂 Import du Diagnostic",
        "nav_etoile": "⭐ Étoile du Conseil",
        "nav_swot": "🔲 SWOT",
        "nav_pestel": "🌐 PESTEL",
        "nav_porter": "⚔️ 5 Forces de Porter",
        "nav_bcg": "📦 Matrice BCG",
        "nav_ansoff": "🚀 Matrice d'Ansoff",
        "nav_rapport": "📄 Rapport Synthèse",
        "org_type": "Type d'organisation",
        "org_opa": "OPA (Organisation de Producteurs)",
        "org_efa": "EFA (Exploitation Familiale)",
        "api_key_label": "Clé API Anthropic (Claude)",
        "api_key_help": "Laissez vide pour utiliser le mode démo avec des analyses illustratives.",
        "api_key_set": "✅ Clé API configurée",
        "api_key_missing": "🔎 Mode démo (sans IA)",
        "demo_mode_info": "Mode démo activé. Les analyses sont illustratives. Entrez une clé API Claude pour des analyses générées par IA.",

        # Home
        "home_title": "Bienvenue sur l'Agent IA d'Analyse Stratégique",
        "home_intro": """
Cet agent IA vous accompagne dans l'**analyse stratégique** de votre organisation de producteurs (OPA)
ou de votre exploitation familiale agricole (EFA).

**Outils d'analyse disponibles :**
- ⭐ **Étoile du Conseil** – Diagnostic multidimensionnel (6 branches)
- 🔲 **SWOT** – Forces, Faiblesses, Opportunités, Menaces
- 🌐 **PESTEL** – Environnement macro-économique
- ⚔️ **5 Forces de Porter** – Compétitivité de la filière
- 📦 **Matrice BCG** – Portefeuille d'activités
- 🚀 **Matrice d'Ansoff** – Stratégies de croissance
        """,
        "home_steps": "Comment utiliser l'agent ?",
        "step1": "📂 **Importer** votre diagnostic (Word ou PDF) dans l'onglet *Import du Diagnostic*",
        "step2": "🤖 **Lancer l'analyse IA** pour remplir automatiquement chaque outil stratégique",
        "step3": "✏️ **Valider et ajuster** les résultats dans chaque onglet",
        "step4": "📄 **Exporter** le rapport de synthèse complet",
        "home_status": "État du diagnostic",
        "no_doc": "Aucun document importé. Commencez par l'onglet *Import du Diagnostic*.",
        "doc_loaded": "Document chargé",
        "doc_chars": "caractères extraits",
        "analyses_done": "Analyses générées",

        # Import
        "import_title": "Import du Diagnostic",
        "import_intro": "Importez votre document de diagnostic (Word .docx ou PDF). L'agent IA en extraira le texte pour alimenter les outils d'analyse.",
        "upload_label": "Glissez-déposez ou cliquez pour importer",
        "upload_types": "Formats acceptés : PDF, DOCX",
        "extract_btn": "📖 Extraire le texte",
        "extract_success": "Texte extrait avec succès",
        "extract_chars": "caractères",
        "extract_pages": "pages/sections",
        "extract_error": "Erreur lors de l'extraction",
        "text_preview": "Aperçu du texte extrait",
        "text_preview_note": "Les 2000 premiers caractères",
        "analyze_all_btn": "🤖 Analyser avec l'IA (tous les outils)",
        "analyze_all_help": "Lance l'analyse IA pour tous les outils stratégiques en une fois",
        "analyze_running": "Analyse en cours…",
        "analyze_done": "Analyse complète ! Consultez chaque outil dans le menu.",
        "manual_text": "Ou saisissez / collez le texte du diagnostic ici",
        "manual_placeholder": "Collez ici le texte de votre diagnostic…",
        "use_manual": "Utiliser ce texte",

        # Étoile du Conseil
        "etoile_title": "Étoile du Conseil",
        "etoile_intro": """
L'**Étoile du Conseil** est un outil de diagnostic multidimensionnel à 6 branches :
- **Milieu local** : conditions pédoclimatiques, infrastructures, contexte territorial
- **Performances technico-économiques** : rendements, productivité, efficience
- **Moyens de production** : accès au foncier, équipement, intrants
- **Politiques publiques** : soutien de l'État, réglementations, programmes
- **Marchés / Filières** : accès aux marchés, prix, organisation de la filière
- **Finances** : trésorerie, accès au crédit, rentabilité
        """,
        "etoile_score": "Score (1 = très faible, 5 = excellent)",
        "etoile_milieu": "Milieu local",
        "etoile_perf": "Performances technico-économiques",
        "etoile_moyens": "Moyens de production",
        "etoile_politiques": "Politiques publiques",
        "etoile_marches": "Marchés / Filières",
        "etoile_finances": "Finances",
        "etoile_obs": "Observations",
        "etoile_generate": "Générer le radar",
        "etoile_ai_btn": "🤖 Analyser avec l'IA",
        "etoile_no_doc": "Importez un diagnostic pour utiliser l'analyse IA.",
        "etoile_radar_title": "Radar Étoile du Conseil",
        "etoile_synthesis": "Synthèse",

        # SWOT
        "swot_title": "Analyse SWOT",
        "swot_intro": "Identifiez les **Forces**, **Faiblesses**, **Opportunités** et **Menaces** de l'organisation ou de l'exploitation.",
        "swot_forces": "💪 Forces (Strengths)",
        "swot_faiblesses": "⚠️ Faiblesses (Weaknesses)",
        "swot_opportunites": "🌱 Opportunités (Opportunities)",
        "swot_menaces": "⚡ Menaces (Threats)",
        "swot_ai_btn": "🤖 Analyser avec l'IA",
        "swot_generate": "Générer la matrice SWOT",
        "swot_placeholder": "Saisissez un élément par ligne…",
        "swot_synthesis": "Synthèse stratégique SWOT",

        # PESTEL
        "pestel_title": "Analyse PESTEL",
        "pestel_intro": "Identifiez les facteurs macro-environnementaux influençant l'organisation.",
        "pestel_politique": "🏛️ Politique",
        "pestel_economique": "💰 Économique",
        "pestel_social": "👥 Social",
        "pestel_techno": "⚙️ Technologique",
        "pestel_environnement": "🌿 Environnemental",
        "pestel_legal": "⚖️ Légal",
        "pestel_ai_btn": "🤖 Analyser avec l'IA",
        "pestel_impact": "Impact",
        "pestel_high": "Élevé",
        "pestel_medium": "Moyen",
        "pestel_low": "Faible",
        "pestel_placeholder": "Facteurs clés identifiés, un par ligne…",
        "pestel_table_title": "Tableau de synthèse PESTEL",

        # Porter
        "porter_title": "5 Forces de Porter",
        "porter_intro": "Évaluez l'intensité concurrentielle de la filière selon le modèle de Porter.",
        "porter_nouveaux": "Menace de nouveaux entrants",
        "porter_fournisseurs": "Pouvoir des fournisseurs",
        "porter_clients": "Pouvoir des acheteurs / clients",
        "porter_substituts": "Menace des produits de substitution",
        "porter_rivalite": "Rivalité entre concurrents existants",
        "porter_ai_btn": "🤖 Analyser avec l'IA",
        "porter_score_label": "Intensité (1 = faible, 5 = très élevée)",
        "porter_comment_label": "Commentaire",
        "porter_generate": "Générer le graphique",
        "porter_synthesis": "Synthèse concurrentielle",

        # BCG
        "bcg_title": "Matrice BCG",
        "bcg_intro": "Classez les activités de l'organisation selon leur part de marché relative et leur taux de croissance.",
        "bcg_activity": "Activité / Produit",
        "bcg_share": "Part de marché relative",
        "bcg_growth": "Taux de croissance (%)",
        "bcg_add": "➕ Ajouter une activité",
        "bcg_generate": "Générer la matrice BCG",
        "bcg_ai_btn": "🤖 Analyser avec l'IA",
        "bcg_quadrant_info": "🌟 Étoiles | ❓ Dilemmes | 🐄 Vaches à lait | 🐕 Poids morts",
        "bcg_stars": "Étoiles (Stars)",
        "bcg_questions": "Dilemmes (Question marks)",
        "bcg_cows": "Vaches à lait (Cash cows)",
        "bcg_dogs": "Poids morts (Dogs)",

        # Ansoff
        "ansoff_title": "Matrice d'Ansoff",
        "ansoff_intro": "Identifiez les stratégies de croissance selon les marchés (existants/nouveaux) et les produits (existants/nouveaux).",
        "ansoff_penetration": "📈 Pénétration de marché\n(Produits existants · Marchés existants)",
        "ansoff_dev_produit": "🆕 Développement de produits\n(Nouveaux produits · Marchés existants)",
        "ansoff_dev_marche": "🌍 Développement de marchés\n(Produits existants · Nouveaux marchés)",
        "ansoff_diversification": "🔀 Diversification\n(Nouveaux produits · Nouveaux marchés)",
        "ansoff_ai_btn": "🤖 Analyser avec l'IA",
        "ansoff_placeholder": "Stratégies identifiées, une par ligne…",
        "ansoff_generate": "Générer la matrice Ansoff",
        "ansoff_existing_products": "Produits existants",
        "ansoff_new_products": "Nouveaux produits",
        "ansoff_existing_markets": "Marchés existants",
        "ansoff_new_markets": "Nouveaux marchés",

        # Rapport
        "rapport_title": "Rapport de Synthèse Stratégique",
        "rapport_intro": "Ce rapport consolide les résultats de tous les outils d'analyse stratégique.",
        "rapport_org_name": "Nom de l'organisation / exploitation",
        "rapport_date": "Date du diagnostic",
        "rapport_analyst": "Analyste",
        "rapport_generate": "📄 Générer le rapport",
        "rapport_export_md": "⬇️ Télécharger (Markdown)",
        "rapport_no_data": "Complétez au moins un outil d'analyse avant de générer le rapport.",
        "rapport_section_etoile": "Étoile du Conseil",
        "rapport_section_swot": "Analyse SWOT",
        "rapport_section_pestel": "Analyse PESTEL",
        "rapport_section_porter": "5 Forces de Porter",
        "rapport_section_bcg": "Matrice BCG",
        "rapport_section_ansoff": "Matrice d'Ansoff",
        "rapport_recommandations": "Recommandations Stratégiques",

        # Misc
        "ai_analysis": "Analyse IA",
        "manual_entry": "Saisie manuelle",
        "save": "Sauvegarder",
        "reset": "Réinitialiser",
        "no_text_warning": "Importez d'abord un document dans l'onglet *Import du Diagnostic*.",
        "generating": "Génération en cours…",
        "done": "Terminé !",
        "error_api": "Erreur API. Vérifiez votre clé API ou passez en mode démo.",
        "tab_ai": "🤖 Analyse IA",
        "tab_manual": "✏️ Saisie manuelle",
    },
    "en": {
        # App
        "app_title": "AI Agent · Strategic Analysis OPA / EFA",
        "tagline": "Intelligent strategic analysis of producer organizations and family farms",
        "language": "Language / Langue",
        "footer": "Agro-Pastoral AI Agent · Bilingual FR/EN · Local Data",

        # Sidebar
        "nav_home": "🏠 Home",
        "nav_import": "📂 Import Diagnostic",
        "nav_etoile": "⭐ Advisory Star",
        "nav_swot": "🔲 SWOT",
        "nav_pestel": "🌐 PESTEL",
        "nav_porter": "⚔️ Porter's 5 Forces",
        "nav_bcg": "📦 BCG Matrix",
        "nav_ansoff": "🚀 Ansoff Matrix",
        "nav_rapport": "📄 Summary Report",
        "org_type": "Organization type",
        "org_opa": "OPA (Producer Organization)",
        "org_efa": "EFA (Family Farm)",
        "api_key_label": "Anthropic API Key (Claude)",
        "api_key_help": "Leave empty to use demo mode with illustrative analyses.",
        "api_key_set": "✅ API key configured",
        "api_key_missing": "🔎 Demo mode (no AI)",
        "demo_mode_info": "Demo mode active. Analyses are illustrative. Enter a Claude API key for AI-generated analyses.",

        # Home
        "home_title": "Welcome to the Strategic Analysis AI Agent",
        "home_intro": """
This AI agent guides you through the **strategic analysis** of your producer organization (OPA)
or your family farm (EFA).

**Available analysis tools:**
- ⭐ **Advisory Star** – Multidimensional diagnostic (6 branches)
- 🔲 **SWOT** – Strengths, Weaknesses, Opportunities, Threats
- 🌐 **PESTEL** – Macro-economic environment
- ⚔️ **Porter's 5 Forces** – Value chain competitiveness
- 📦 **BCG Matrix** – Activity portfolio
- 🚀 **Ansoff Matrix** – Growth strategies
        """,
        "home_steps": "How to use the agent?",
        "step1": "📂 **Import** your diagnostic document (Word or PDF) in the *Import Diagnostic* tab",
        "step2": "🤖 **Run AI analysis** to automatically populate each strategic tool",
        "step3": "✏️ **Validate and adjust** results in each tab",
        "step4": "📄 **Export** the complete synthesis report",
        "home_status": "Diagnostic status",
        "no_doc": "No document imported. Start with the *Import Diagnostic* tab.",
        "doc_loaded": "Document loaded",
        "doc_chars": "characters extracted",
        "analyses_done": "Analyses generated",

        # Import
        "import_title": "Import Diagnostic",
        "import_intro": "Import your diagnostic document (Word .docx or PDF). The AI agent will extract text to feed the analysis tools.",
        "upload_label": "Drag and drop or click to import",
        "upload_types": "Accepted formats: PDF, DOCX",
        "extract_btn": "📖 Extract text",
        "extract_success": "Text extracted successfully",
        "extract_chars": "characters",
        "extract_pages": "pages/sections",
        "extract_error": "Extraction error",
        "text_preview": "Preview of extracted text",
        "text_preview_note": "First 2000 characters",
        "analyze_all_btn": "🤖 Analyze with AI (all tools)",
        "analyze_all_help": "Run AI analysis for all strategic tools at once",
        "analyze_running": "Analysis in progress…",
        "analyze_done": "Analysis complete! Check each tool in the menu.",
        "manual_text": "Or type / paste diagnostic text here",
        "manual_placeholder": "Paste your diagnostic text here…",
        "use_manual": "Use this text",

        # Advisory Star
        "etoile_title": "Advisory Star",
        "etoile_intro": """
The **Advisory Star** is a multidimensional diagnostic tool with 6 branches:
- **Local environment**: soil/climate conditions, infrastructure, territorial context
- **Technical-economic performance**: yields, productivity, efficiency
- **Production means**: land access, equipment, inputs
- **Public policies**: government support, regulations, programs
- **Markets / Value chains**: market access, prices, chain organization
- **Finances**: cash flow, credit access, profitability
        """,
        "etoile_score": "Score (1 = very weak, 5 = excellent)",
        "etoile_milieu": "Local environment",
        "etoile_perf": "Technical-economic performance",
        "etoile_moyens": "Production means",
        "etoile_politiques": "Public policies",
        "etoile_marches": "Markets / Value chains",
        "etoile_finances": "Finances",
        "etoile_obs": "Observations",
        "etoile_generate": "Generate radar",
        "etoile_ai_btn": "🤖 Analyze with AI",
        "etoile_no_doc": "Import a diagnostic to use AI analysis.",
        "etoile_radar_title": "Advisory Star Radar",
        "etoile_synthesis": "Synthesis",

        # SWOT
        "swot_title": "SWOT Analysis",
        "swot_intro": "Identify the **Strengths**, **Weaknesses**, **Opportunities** and **Threats** of the organization or farm.",
        "swot_forces": "💪 Strengths",
        "swot_faiblesses": "⚠️ Weaknesses",
        "swot_opportunites": "🌱 Opportunities",
        "swot_menaces": "⚡ Threats",
        "swot_ai_btn": "🤖 Analyze with AI",
        "swot_generate": "Generate SWOT matrix",
        "swot_placeholder": "Enter one item per line…",
        "swot_synthesis": "SWOT strategic synthesis",

        # PESTEL
        "pestel_title": "PESTEL Analysis",
        "pestel_intro": "Identify macro-environmental factors influencing the organization.",
        "pestel_politique": "🏛️ Political",
        "pestel_economique": "💰 Economic",
        "pestel_social": "👥 Social",
        "pestel_techno": "⚙️ Technological",
        "pestel_environnement": "🌿 Environmental",
        "pestel_legal": "⚖️ Legal",
        "pestel_ai_btn": "🤖 Analyze with AI",
        "pestel_impact": "Impact",
        "pestel_high": "High",
        "pestel_medium": "Medium",
        "pestel_low": "Low",
        "pestel_placeholder": "Key factors identified, one per line…",
        "pestel_table_title": "PESTEL synthesis table",

        # Porter
        "porter_title": "Porter's 5 Forces",
        "porter_intro": "Assess the competitive intensity of the value chain using Porter's model.",
        "porter_nouveaux": "Threat of new entrants",
        "porter_fournisseurs": "Supplier bargaining power",
        "porter_clients": "Buyer bargaining power",
        "porter_substituts": "Threat of substitutes",
        "porter_rivalite": "Rivalry among existing competitors",
        "porter_ai_btn": "🤖 Analyze with AI",
        "porter_score_label": "Intensity (1 = low, 5 = very high)",
        "porter_comment_label": "Comment",
        "porter_generate": "Generate chart",
        "porter_synthesis": "Competitive synthesis",

        # BCG
        "bcg_title": "BCG Matrix",
        "bcg_intro": "Classify activities by relative market share and growth rate.",
        "bcg_activity": "Activity / Product",
        "bcg_share": "Relative market share",
        "bcg_growth": "Growth rate (%)",
        "bcg_add": "➕ Add activity",
        "bcg_generate": "Generate BCG matrix",
        "bcg_ai_btn": "🤖 Analyze with AI",
        "bcg_quadrant_info": "🌟 Stars | ❓ Question marks | 🐄 Cash cows | 🐕 Dogs",
        "bcg_stars": "Stars",
        "bcg_questions": "Question marks",
        "bcg_cows": "Cash cows",
        "bcg_dogs": "Dogs",

        # Ansoff
        "ansoff_title": "Ansoff Matrix",
        "ansoff_intro": "Identify growth strategies by market (existing/new) and product (existing/new).",
        "ansoff_penetration": "📈 Market penetration\n(Existing products · Existing markets)",
        "ansoff_dev_produit": "🆕 Product development\n(New products · Existing markets)",
        "ansoff_dev_marche": "🌍 Market development\n(Existing products · New markets)",
        "ansoff_diversification": "🔀 Diversification\n(New products · New markets)",
        "ansoff_ai_btn": "🤖 Analyze with AI",
        "ansoff_placeholder": "Identified strategies, one per line…",
        "ansoff_generate": "Generate Ansoff matrix",
        "ansoff_existing_products": "Existing products",
        "ansoff_new_products": "New products",
        "ansoff_existing_markets": "Existing markets",
        "ansoff_new_markets": "New markets",

        # Rapport
        "rapport_title": "Strategic Synthesis Report",
        "rapport_intro": "This report consolidates the results from all strategic analysis tools.",
        "rapport_org_name": "Organization / farm name",
        "rapport_date": "Diagnostic date",
        "rapport_analyst": "Analyst",
        "rapport_generate": "📄 Generate report",
        "rapport_export_md": "⬇️ Download (Markdown)",
        "rapport_no_data": "Complete at least one analysis tool before generating the report.",
        "rapport_section_etoile": "Advisory Star",
        "rapport_section_swot": "SWOT Analysis",
        "rapport_section_pestel": "PESTEL Analysis",
        "rapport_section_porter": "Porter's 5 Forces",
        "rapport_section_bcg": "BCG Matrix",
        "rapport_section_ansoff": "Ansoff Matrix",
        "rapport_recommandations": "Strategic Recommendations",

        # Misc
        "ai_analysis": "AI Analysis",
        "manual_entry": "Manual entry",
        "save": "Save",
        "reset": "Reset",
        "no_text_warning": "First import a document in the *Import Diagnostic* tab.",
        "generating": "Generating…",
        "done": "Done!",
        "error_api": "API error. Check your API key or switch to demo mode.",
        "tab_ai": "🤖 AI Analysis",
        "tab_manual": "✏️ Manual entry",
    },
}


def t(key: str, lang: str = "fr") -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS["fr"]).get(key, key)
