"""
AI-powered strategic analysis using Anthropic Claude API.
Falls back to illustrative demo data when no API key is provided.
"""
from __future__ import annotations
import json
import re


# ---------------------------------------------------------------------------
# DEMO DATA (used when no API key)
# ---------------------------------------------------------------------------

DEMO_FR = {
    "etoile": {
        "milieu": {"score": 3, "obs": "Conditions agro-climatiques favorables au cacao mais accès aux routes rurales limité. Présence d'organisations paysannes actives dans la zone."},
        "perf": {"score": 2, "obs": "Rendements moyens en deçà des références régionales (500 kg/ha vs. 800 kg/ha attendus). Vieillissement des plantations, faible adoption des bonnes pratiques."},
        "moyens": {"score": 3, "obs": "Accès au foncier sécurisé pour la majorité des membres. Équipement de post-récolte insuffisant. Difficultés d'approvisionnement en intrants certifiés."},
        "politiques": {"score": 2, "obs": "Peu de soutien institutionnel direct. Programme national de réhabilitation des vergers peu opérationnel dans la zone. Fiscalité locale perçue comme lourde."},
        "marches": {"score": 3, "obs": "Accès aux marchés via la coopérative mais forte dépendance à un seul acheteur. Prix fluctuants. Certifications durables (Rainforest, UTZ) en cours pour certains membres."},
        "finances": {"score": 2, "obs": "Trésorerie tendue, faible accès au crédit agricole formel. Endettement informel fréquent en période de soudure. BFR souvent non couvert."},
        "synthesis": "L'étoile révèle des faiblesses structurelles dans les performances techniques et l'accès aux politiques publiques. Les forces résident dans les conditions pédoclimatiques et l'accès partiel aux marchés. Priorité : renforcement des capacités techniques et accès au financement.",
    },
    "swot": {
        "forces": [
            "Expérience historique de la culture cacaoyère (>20 ans)",
            "Cohésion sociale forte au sein de l'OPA",
            "Terroir favorable (sol ferrallitique, pluviométrie 1400 mm/an)",
            "Certification en cours (Rainforest Alliance) valorisant la production",
            "Réseau de collecte organisé par la coopérative",
        ],
        "faiblesses": [
            "Vieillissement des plantations (>50% des vergers >25 ans)",
            "Faibles rendements moyens (500 kg/ha vs. 800 recommandés)",
            "Accès limité aux intrants certifiés et aux équipements",
            "Faible niveau de transformation locale (vente matière brute)",
            "Gestion financière peu structurée de l'OPA",
        ],
        "opportunites": [
            "Demande mondiale soutenue et hausse des prix cacao (2023-2024)",
            "Programmes de réhabilitation des vergers financés par les partenaires",
            "Développement de la transformation artisanale (fèves, beurre, poudre)",
            "Accès aux marchés de niche (bio, équitable, terroir)",
            "Digitalisation des services agricoles (conseil, traçabilité)",
        ],
        "menaces": [
            "Changement climatique : sécheresses plus fréquentes, déforestation",
            "Volatilité des prix sur les marchés internationaux",
            "Concurrence des négociants informels fragilisant la collecte",
            "Pression foncière croissante sur les zones de production",
            "Vieillissement des producteurs et faible intégration des jeunes",
        ],
        "synthesis": "La situation appelle une stratégie SO (mobiliser les forces pour saisir les opportunités) : valoriser le terroir et la certification pour accéder aux marchés premium, et une stratégie WT (réduire les faiblesses face aux menaces) : rénover le verger et sécuriser le foncier.",
    },
    "pestel": {
        "politique": [
            "Programme national de développement du cacao (PNDC) peu opérationnel",
            "Instabilité institutionnelle affectant les subventions aux intrants",
            "Soutien des bailleurs (UE, AFD) aux coopératives certifiées",
        ],
        "economique": [
            "Flambée des prix mondiaux du cacao (2023-2024 : +150%)",
            "Inflation des coûts des intrants (engrais, pesticides)",
            "Dévaluation monétaire augmentant le coût des importations",
            "Accès limité au crédit agricole formel (taux >18%/an)",
        ],
        "social": [
            "Exode rural des jeunes vers les villes",
            "Féminisation partielle de la production mais inégalités persistantes",
            "Conflits fonciers intergénérationnels",
            "Forte tradition coopérative dans la région",
        ],
        "techno": [
            "Diffusion des smartphones facilitant le conseil agricole numérique",
            "Semences améliorées disponibles mais peu adoptées",
            "Techniques de fermentation et séchage peu maîtrisées",
            "Traçabilité numérique requise par les certifications",
        ],
        "environnement": [
            "Déforestation réduisant le couvert arboré protecteur",
            "Changement climatique : stress hydrique en hausse",
            "Pression de la maladie des cabosses noires et du swollen shoot",
            "Règlement européen sur la déforestation (EUDR) créant de nouvelles exigences",
        ],
        "legal": [
            "EUDR impose la traçabilité géo-localisée de la production",
            "Loi coopérative nationale contraignante pour la gouvernance",
            "Absence de protection légale forte des droits fonciers coutumiers",
        ],
    },
    "porter": {
        "nouveaux": {"score": 2, "comment": "Barrières à l'entrée modérées : capital foncier et apprentissage nécessaires. Risque limité de nouveaux producteurs à court terme."},
        "fournisseurs": {"score": 4, "comment": "Forte dépendance aux fournisseurs d'intrants importés (engrais, pesticides). Peu d'alternatives locales. Pouvoir de négociation élevé des distributeurs agréés."},
        "clients": {"score": 4, "comment": "Oligopsone : 2-3 grands acheteurs dominent. Fixent les prix. La certification réduit légèrement cette dépendance."},
        "substituts": {"score": 2, "comment": "Peu de substituts directs au cacao. Concurrence avec d'autres cultures de rente (café, palmier) pour l'usage des terres."},
        "rivalite": {"score": 3, "comment": "Compétition entre OPA pour les marchés certifiés. Pression des collecteurs informels concurrençant la collecte coopérative."},
        "synthesis": "La filière est dominée par un fort pouvoir des acheteurs et des fournisseurs. La stratégie recommandée est de renforcer le pouvoir de marché via la certification, la transformation locale et les alliances entre coopératives.",
    },
    "bcg": [
        {"activity": "Cacao conventionnel", "share": 0.6, "growth": 8.0, "quadrant": "Star"},
        {"activity": "Cacao certifié (Rainforest)", "share": 0.3, "growth": 15.0, "quadrant": "Question mark"},
        {"activity": "Cultures vivrières associées", "share": 0.8, "growth": 2.0, "quadrant": "Cash cow"},
        {"activity": "Services de transformation", "share": 0.1, "growth": 25.0, "quadrant": "Question mark"},
    ],
    "ansoff": {
        "penetration": [
            "Augmenter le taux d'adoption des bonnes pratiques pour améliorer les rendements",
            "Renforcer la fidélisation des membres via des services (crédit intrant, conseil)",
            "Accroître le volume de collecte via l'OPA (capter les ventes informelles)",
        ],
        "dev_produit": [
            "Développer la transformation artisanale : fèves séchées de qualité premium",
            "Produire du cacao certifié biologique pour valoriser le terroir",
            "Créer des produits dérivés : beurre de cacao, poudre, liqueur",
        ],
        "dev_marche": [
            "Accéder aux marchés à l'exportation directe (court-circuiter les intermédiaires)",
            "Développer des contrats avec les chocolatiers artisanaux européens",
            "Prospecter le marché régional (CEMAC) en développement",
        ],
        "diversification": [
            "Développer l'agroforesterie (cacao + bois, fruit, médicinal) pour de nouveaux marchés carbone",
            "Créer une marque territoriale combinant cacao et tourisme rural",
            "Lancer une activité de prestation de services agricoles pour d'autres filières",
        ],
        "synthesis": "La stratégie prioritaire est la pénétration de marché (renforcement des rendements et volumes) combinée au développement de produits (certification et transformation). La diversification est une opportunité à moyen terme.",
    },
}

DEMO_EN = {
    "etoile": {
        "milieu": {"score": 3, "obs": "Favorable agro-climatic conditions for cocoa, but limited access to rural roads. Active farmer organizations present in the area."},
        "perf": {"score": 2, "obs": "Average yields below regional benchmarks (500 kg/ha vs. 800 kg/ha expected). Aging plantations, low adoption of good agricultural practices."},
        "moyens": {"score": 3, "obs": "Secured land access for most members. Insufficient post-harvest equipment. Difficulties sourcing certified inputs."},
        "politiques": {"score": 2, "obs": "Limited direct institutional support. National orchard rehabilitation program poorly operational in the area. Local taxation perceived as burdensome."},
        "marches": {"score": 3, "obs": "Market access through cooperative but strong dependence on a single buyer. Fluctuating prices. Sustainability certifications (Rainforest, UTZ) underway for some members."},
        "finances": {"score": 2, "obs": "Tight cash flow, limited access to formal agricultural credit. Frequent informal debt during lean season. Working capital often uncovered."},
        "synthesis": "The star reveals structural weaknesses in technical performance and access to public policies. Strengths lie in agro-climatic conditions and partial market access. Priority: technical capacity building and access to finance.",
    },
    "swot": {
        "forces": [
            "Historical experience in cocoa farming (>20 years)",
            "Strong social cohesion within the OPA",
            "Favorable terroir (ferrallitic soil, 1400 mm/year rainfall)",
            "Ongoing certification (Rainforest Alliance) adding value to production",
            "Organized collection network through the cooperative",
        ],
        "faiblesses": [
            "Aging plantations (>50% of orchards >25 years old)",
            "Low average yields (500 kg/ha vs. 800 recommended)",
            "Limited access to certified inputs and equipment",
            "Little local processing (sale as raw material only)",
            "Poorly structured financial management of the OPA",
        ],
        "opportunites": [
            "Sustained global demand and rising cocoa prices (2023-2024)",
            "Orchard rehabilitation programs funded by development partners",
            "Development of artisanal processing (beans, butter, powder)",
            "Access to niche markets (organic, fair trade, terroir)",
            "Digitalization of agricultural services (advisory, traceability)",
        ],
        "menaces": [
            "Climate change: more frequent droughts, deforestation",
            "Volatility of international commodity prices",
            "Competition from informal traders weakening cooperative collection",
            "Growing land pressure in production zones",
            "Aging farmer population, low youth integration",
        ],
        "synthesis": "The situation calls for an SO strategy (leverage strengths to seize opportunities): promote terroir and certification to access premium markets; and a WT strategy (reduce weaknesses against threats): renovate orchards and secure land rights.",
    },
    "pestel": {
        "politique": [
            "National cocoa development program (PNDC) poorly operational",
            "Institutional instability affecting input subsidies",
            "Donor support (EU, AFD) to certified cooperatives",
        ],
        "economique": [
            "Global cocoa price surge (2023-2024: +150%)",
            "Rising input costs (fertilizers, pesticides)",
            "Currency depreciation increasing import costs",
            "Limited access to formal agricultural credit (rates >18%/year)",
        ],
        "social": [
            "Rural exodus of youth to urban areas",
            "Partial feminization of production but persistent inequalities",
            "Inter-generational land conflicts",
            "Strong cooperative tradition in the region",
        ],
        "techno": [
            "Smartphone penetration enabling digital agricultural advisory",
            "Improved seeds available but little adopted",
            "Fermentation and drying techniques not well mastered",
            "Digital traceability required by certifications",
        ],
        "environnement": [
            "Deforestation reducing protective tree cover",
            "Climate change: increasing water stress",
            "Pressure from black pod disease and swollen shoot virus",
            "EU Deforestation Regulation (EUDR) creating new requirements",
        ],
        "legal": [
            "EUDR requires geo-located production traceability",
            "National cooperative law constraining governance",
            "Weak legal protection of customary land rights",
        ],
    },
    "porter": {
        "nouveaux": {"score": 2, "comment": "Moderate entry barriers: land capital and learning curve required. Limited risk of new entrants in the short term."},
        "fournisseurs": {"score": 4, "comment": "High dependence on imported inputs (fertilizers, pesticides). Few local alternatives. High bargaining power of licensed distributors."},
        "clients": {"score": 4, "comment": "Oligopsony: 2-3 large buyers dominate. They set prices. Certification slightly reduces this dependence."},
        "substituts": {"score": 2, "comment": "Few direct substitutes for cocoa. Competition with other cash crops (coffee, palm oil) for land use."},
        "rivalite": {"score": 3, "comment": "Competition among OPAs for certified markets. Pressure from informal traders competing with cooperative collection."},
        "synthesis": "The value chain is dominated by strong buyer and supplier power. The recommended strategy is to build market power through certification, local processing, and cooperative alliances.",
    },
    "bcg": [
        {"activity": "Conventional cocoa", "share": 0.6, "growth": 8.0, "quadrant": "Star"},
        {"activity": "Certified cocoa (Rainforest)", "share": 0.3, "growth": 15.0, "quadrant": "Question mark"},
        {"activity": "Associated food crops", "share": 0.8, "growth": 2.0, "quadrant": "Cash cow"},
        {"activity": "Processing services", "share": 0.1, "growth": 25.0, "quadrant": "Question mark"},
    ],
    "ansoff": {
        "penetration": [
            "Increase adoption rate of good agricultural practices to improve yields",
            "Strengthen member loyalty through services (input credit, advisory)",
            "Increase collection volume through OPA (capture informal sales)",
        ],
        "dev_produit": [
            "Develop artisanal processing: premium quality dried beans",
            "Produce organic-certified cocoa to leverage terroir",
            "Create derivative products: cocoa butter, powder, liqueur",
        ],
        "dev_marche": [
            "Access direct export markets (bypass intermediaries)",
            "Develop contracts with European artisan chocolatiers",
            "Prospect the growing regional market (CEMAC)",
        ],
        "diversification": [
            "Develop agroforestry (cocoa + timber, fruit, medicinal) for carbon markets",
            "Create a territorial brand combining cocoa and rural tourism",
            "Launch an agricultural service provision activity for other value chains",
        ],
        "synthesis": "Priority strategy is market penetration (yield and volume improvement) combined with product development (certification and processing). Diversification is a medium-term opportunity.",
    },
}


# ---------------------------------------------------------------------------
# AI ANALYSIS
# ---------------------------------------------------------------------------

def _build_prompt(text: str, tool: str, lang: str, org_type: str) -> str:
    org_label = "organisation de producteurs agricoles (OPA)" if lang == "fr" else "agricultural producer organization (OPA)"
    if org_type == "efa":
        org_label = "exploitation familiale agricole (EFA)" if lang == "fr" else "family farm (EFA)"

    if lang == "fr":
        base = f"""Tu es un expert en développement agricole et en analyse stratégique des {org_label}.
Analyse le diagnostic suivant et extrais les informations pertinentes pour l'outil {tool}.
Réponds UNIQUEMENT en JSON valide, sans texte additionnel.

DIAGNOSTIC :
{text[:6000]}

"""
    else:
        base = f"""You are an expert in agricultural development and strategic analysis of {org_label}.
Analyze the following diagnostic and extract relevant information for the {tool} tool.
Respond ONLY with valid JSON, no additional text.

DIAGNOSTIC:
{text[:6000]}

"""
    prompts = {
        "etoile": (
            base + (
                'Return JSON with keys: "milieu", "perf", "moyens", "politiques", "marches", "finances".\n'
                'Each key maps to {"score": <int 1-5>, "obs": "<string>"}.\n'
                'Also include "synthesis": "<string>".\n'
                'Example: {"milieu": {"score": 3, "obs": "..."}, ..., "synthesis": "..."}'
            )
        ),
        "swot": (
            base + (
                'Return JSON with keys: "forces", "faiblesses", "opportunites", "menaces" (each a list of strings), '
                'and "synthesis": "<string>".\n'
                'Example: {"forces": ["...", "..."], "faiblesses": [...], "opportunites": [...], "menaces": [...], "synthesis": "..."}'
            )
        ),
        "pestel": (
            base + (
                'Return JSON with keys: "politique", "economique", "social", "techno", "environnement", "legal".\n'
                'Each key maps to a list of strings.\n'
                'Example: {"politique": ["...", "..."], "economique": [...], ...}'
            )
        ),
        "porter": (
            base + (
                'Return JSON with keys: "nouveaux", "fournisseurs", "clients", "substituts", "rivalite".\n'
                'Each key maps to {"score": <int 1-5>, "comment": "<string>"}.\n'
                'Also include "synthesis": "<string>".\n'
                'Example: {"nouveaux": {"score": 2, "comment": "..."}, ..., "synthesis": "..."}'
            )
        ),
        "bcg": (
            base + (
                'Return JSON: a list of activity objects.\n'
                'Each object: {"activity": "<name>", "share": <float 0-2>, "growth": <float>, "quadrant": "<Star|Question mark|Cash cow|Dog>"}\n'
                'Example: [{"activity": "Cacao", "share": 0.6, "growth": 8.0, "quadrant": "Star"}, ...]'
            )
        ),
        "ansoff": (
            base + (
                'Return JSON with keys: "penetration", "dev_produit", "dev_marche", "diversification" (each a list of strings), '
                'and "synthesis": "<string>".\n'
                'Example: {"penetration": ["...", "..."], "dev_produit": [...], "dev_marche": [...], "diversification": [...], "synthesis": "..."}'
            )
        ),
    }
    return prompts.get(tool, base)


def analyze(text: str, tool: str, lang: str, org_type: str, api_key: str) -> dict:
    """
    Call Claude API to analyze text with the given strategic tool.
    Returns a dict with the parsed result.
    """
    if not api_key or not api_key.strip():
        return _demo_data(tool, lang)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key.strip())
        prompt = _build_prompt(text, tool, lang, org_type)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        # Strip markdown code blocks if present
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        return json.loads(raw)
    except Exception as e:
        raise RuntimeError(f"AI analysis failed: {e}")


def analyze_all(text: str, lang: str, org_type: str, api_key: str) -> dict:
    """Run all 6 strategic tools and return combined results dict."""
    tools = ["etoile", "swot", "pestel", "porter", "bcg", "ansoff"]
    results = {}
    for tool in tools:
        results[tool] = analyze(text, tool, lang, org_type, api_key)
    return results


def _demo_data(tool: str, lang: str) -> dict:
    data = DEMO_EN if lang == "en" else DEMO_FR
    return data.get(tool, {})
