"""
AI-powered strategic analysis.
Supports three backends:
  1. Anthropic Claude API  (api_key provided)
  2. Ollama local LLM      (ollama_url + model provided, no api_key)
  3. Demo mode             (no api_key, no ollama_url)
"""
from __future__ import annotations
import json
import re


# ---------------------------------------------------------------------------
# DEMO DATA
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
        "politique": ["Programme national de développement du cacao peu opérationnel", "Soutien des bailleurs (UE, AFD) aux coopératives certifiées"],
        "economique": ["Flambée des prix mondiaux du cacao (2023-2024)", "Inflation des coûts des intrants", "Accès limité au crédit agricole formel (taux >18%/an)"],
        "social": ["Exode rural des jeunes", "Forte tradition coopérative dans la région"],
        "techno": ["Diffusion des smartphones facilitant le conseil numérique", "Semences améliorées disponibles mais peu adoptées"],
        "environnement": ["Changement climatique : stress hydrique en hausse", "Pression des maladies (capsides, pourriture brune)"],
        "legal": ["Règlement européen sur la déforestation (EUDR)", "Loi coopérative nationale contraignante pour la gouvernance"],
    },
    "porter": {
        "nouveaux": {"score": 2, "comment": "Barrières à l'entrée modérées : capital foncier et apprentissage nécessaires."},
        "fournisseurs": {"score": 4, "comment": "Forte dépendance aux fournisseurs d'intrants importés. Pouvoir de négociation élevé."},
        "clients": {"score": 4, "comment": "Oligopsone : 2-3 grands acheteurs dominent. Fixent les prix."},
        "substituts": {"score": 2, "comment": "Peu de substituts directs au cacao."},
        "rivalite": {"score": 3, "comment": "Compétition entre OPA pour les marchés certifiés."},
        "synthesis": "La filière est dominée par un fort pouvoir des acheteurs et des fournisseurs. Stratégie : certification, transformation locale et alliances entre coopératives.",
    },
    "bcg": [
        {"activity": "Cacao conventionnel", "share": 0.6, "growth": 8.0, "quadrant": "Star"},
        {"activity": "Cacao certifié", "share": 0.3, "growth": 15.0, "quadrant": "Question mark"},
        {"activity": "Cultures vivrières associées", "share": 0.8, "growth": 2.0, "quadrant": "Cash cow"},
        {"activity": "Services de transformation", "share": 0.1, "growth": 25.0, "quadrant": "Question mark"},
    ],
    "ansoff": {
        "penetration": ["Augmenter le taux d'adoption des bonnes pratiques", "Renforcer la fidélisation des membres"],
        "dev_produit": ["Développer la transformation artisanale", "Produire du cacao certifié biologique"],
        "dev_marche": ["Accéder aux marchés d'exportation directe", "Développer des contrats avec les chocolatiers artisanaux"],
        "diversification": ["Développer l'agroforesterie (cacao + bois, fruit)", "Créer une marque territoriale"],
        "synthesis": "Stratégie prioritaire : pénétration de marché combinée au développement de produits. La diversification est une opportunité à moyen terme.",
    },
}

DEMO_EN = {
    "etoile": {
        "milieu": {"score": 3, "obs": "Favorable agro-climatic conditions for cocoa, but limited rural road access."},
        "perf": {"score": 2, "obs": "Average yields below regional benchmarks. Aging plantations, low adoption of good practices."},
        "moyens": {"score": 3, "obs": "Secured land access for most members. Insufficient post-harvest equipment."},
        "politiques": {"score": 2, "obs": "Limited direct institutional support. National programs poorly operational."},
        "marches": {"score": 3, "obs": "Market access through cooperative but single buyer dependence."},
        "finances": {"score": 2, "obs": "Tight cash flow, limited formal credit access. Working capital often uncovered."},
        "synthesis": "Structural weaknesses in technical performance and public policy access. Strengths in agro-climatic conditions. Priority: capacity building and finance access.",
    },
    "swot": {
        "forces": ["Historical cocoa farming experience (>20 years)", "Strong social cohesion", "Favorable terroir"],
        "faiblesses": ["Aging plantations", "Low average yields", "Limited certified input access"],
        "opportunites": ["Sustained global cocoa demand", "Orchard rehabilitation programs", "Artisanal processing development"],
        "menaces": ["Climate change", "International price volatility", "Informal trader competition"],
        "synthesis": "SO strategy: leverage strengths for market opportunities. WT strategy: reduce weaknesses against threats.",
    },
    "pestel": {
        "politique": ["National cocoa program poorly operational", "Donor support to certified cooperatives"],
        "economique": ["Global cocoa price surge", "Rising input costs"],
        "social": ["Rural youth exodus", "Strong cooperative tradition"],
        "techno": ["Smartphone penetration enabling digital advisory", "Improved seeds available"],
        "environnement": ["Climate change: increasing water stress", "Black pod disease pressure"],
        "legal": ["EU Deforestation Regulation (EUDR)", "National cooperative law constraining governance"],
    },
    "porter": {
        "nouveaux": {"score": 2, "comment": "Moderate entry barriers: land capital and learning curve required."},
        "fournisseurs": {"score": 4, "comment": "High dependence on imported inputs. High bargaining power."},
        "clients": {"score": 4, "comment": "Oligopsony: 2-3 large buyers dominate and set prices."},
        "substituts": {"score": 2, "comment": "Few direct substitutes for cocoa."},
        "rivalite": {"score": 3, "comment": "Competition among OPAs for certified markets."},
        "synthesis": "Value chain dominated by strong buyer and supplier power. Recommended strategy: certification, local processing, cooperative alliances.",
    },
    "bcg": [
        {"activity": "Conventional cocoa", "share": 0.6, "growth": 8.0, "quadrant": "Star"},
        {"activity": "Certified cocoa", "share": 0.3, "growth": 15.0, "quadrant": "Question mark"},
        {"activity": "Associated food crops", "share": 0.8, "growth": 2.0, "quadrant": "Cash cow"},
        {"activity": "Processing services", "share": 0.1, "growth": 25.0, "quadrant": "Question mark"},
    ],
    "ansoff": {
        "penetration": ["Increase adoption of good agricultural practices", "Strengthen member loyalty"],
        "dev_produit": ["Develop artisanal processing", "Produce organic-certified cocoa"],
        "dev_marche": ["Access direct export markets", "Develop contracts with artisan chocolatiers"],
        "diversification": ["Develop agroforestry", "Create territorial brand"],
        "synthesis": "Priority: market penetration + product development. Diversification is a medium-term opportunity.",
    },
}


# ---------------------------------------------------------------------------
# PROMPT BUILDER
# ---------------------------------------------------------------------------

def _build_prompt(text: str, tool: str, lang: str, org_type: str) -> str:
    org_label = ("organisation de producteurs agricoles (OPA)" if lang == "fr"
                 else "agricultural producer organization (OPA)")
    if org_type == "efa":
        org_label = ("exploitation familiale agricole (EFA)" if lang == "fr"
                     else "family farm (EFA)")

    if lang == "fr":
        base = (
            f"Tu es un expert en développement agricole et en analyse stratégique des {org_label}.\n"
            f"Analyse le diagnostic suivant et extrais les informations pertinentes.\n"
            f"Réponds UNIQUEMENT en JSON valide, sans texte additionnel.\n\n"
            f"DIAGNOSTIC :\n{text[:6000]}\n\n"
        )
    else:
        base = (
            f"You are an expert in agricultural development and strategic analysis of {org_label}.\n"
            f"Analyze the following diagnostic and extract relevant information.\n"
            f"Respond ONLY with valid JSON, no additional text.\n\n"
            f"DIAGNOSTIC:\n{text[:6000]}\n\n"
        )

    schemas = {
        "etoile": (
            'Return JSON with keys: "milieu","perf","moyens","politiques","marches","finances".\n'
            'Each maps to {"score":<int 1-5>,"obs":"<string>"}. Also include "synthesis":"<string>".'
        ),
        "swot": (
            'Return JSON: {"forces":[...],"faiblesses":[...],"opportunites":[...],"menaces":[...],"synthesis":"<string>"}.'
        ),
        "pestel": (
            'Return JSON: {"politique":[...],"economique":[...],"social":[...],"techno":[...],"environnement":[...],"legal":[...]}.'
        ),
        "porter": (
            'Return JSON with keys "nouveaux","fournisseurs","clients","substituts","rivalite".\n'
            'Each maps to {"score":<int 1-5>,"comment":"<string>"}. Also include "synthesis":"<string>".'
        ),
        "bcg": (
            'Return JSON: a list of objects: {"activity":"<name>","share":<float 0-2>,"growth":<float>,"quadrant":"<Star|Question mark|Cash cow|Dog>"}.'
        ),
        "ansoff": (
            'Return JSON: {"penetration":[...],"dev_produit":[...],"dev_marche":[...],"diversification":[...],"synthesis":"<string>"}.'
        ),
    }
    return base + schemas.get(tool, "")


def _parse_json(raw: str) -> dict | list:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


# ---------------------------------------------------------------------------
# BACKENDS
# ---------------------------------------------------------------------------

def _call_claude(prompt: str, api_key: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key.strip())
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def _call_ollama(prompt: str, ollama_url: str, ollama_model: str) -> str:
    import urllib.request
    payload = json.dumps({
        "model": ollama_model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 2048},
    }).encode()
    url = ollama_url.rstrip("/") + "/api/generate"
    req = urllib.request.Request(url, data=payload,
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    return result.get("response", "")


# ---------------------------------------------------------------------------
# PUBLIC API
# ---------------------------------------------------------------------------

def analyze(text: str, tool: str, lang: str, org_type: str,
            api_key: str = "", ollama_url: str = "", ollama_model: str = "llama3") -> dict | list:
    """
    Analyze text with strategic tool using the best available backend.
    Priority: Claude API > Ollama > Demo data.
    """
    if not text:
        return _demo_data(tool, lang)

    prompt = _build_prompt(text, tool, lang, org_type)

    # 1. Claude API
    if api_key and api_key.strip():
        try:
            raw = _call_claude(prompt, api_key)
            return _parse_json(raw)
        except Exception as e:
            raise RuntimeError(f"Claude API error: {e}")

    # 2. Ollama (local)
    if ollama_url and ollama_url.strip():
        try:
            raw = _call_ollama(prompt, ollama_url, ollama_model)
            return _parse_json(raw)
        except Exception as e:
            raise RuntimeError(f"Ollama error: {e}")

    # 3. Demo
    return _demo_data(tool, lang)


def analyze_all(text: str, lang: str, org_type: str,
                api_key: str = "", ollama_url: str = "", ollama_model: str = "llama3") -> dict:
    tools = ["etoile", "swot", "pestel", "porter", "bcg", "ansoff"]
    return {t: analyze(text, t, lang, org_type, api_key, ollama_url, ollama_model)
            for t in tools}


def list_ollama_models(ollama_url: str) -> list[str]:
    """Return available Ollama models from the local server."""
    try:
        import urllib.request
        url = ollama_url.rstrip("/") + "/api/tags"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


def _demo_data(tool: str, lang: str) -> dict | list:
    data = DEMO_EN if lang == "en" else DEMO_FR
    return data.get(tool, {})
