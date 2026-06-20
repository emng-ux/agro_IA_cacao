const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, Header, Footer, TableOfContents, LevelFormat,
  PageBreak
} = require("docx");
const fs = require("fs");

// ── Couleurs ──────────────────────────────────────────────
const VERT_FONCE  = "1B5E20";
const VERT_CLAIR  = "E8F5E9";
const VERT_MOY    = "2E7D32";
const ROUGE_FONCE = "B71C1C";
const ROUGE_CLAIR = "FFEBEE";
const BLEU_CLAIR  = "E3F2FD";
const JAUNE_CLAIR = "FFF8E1";
const GRIS_CLAIR  = "F5F5F5";
const GRIS_ENTETE = "37474F";
const BLANC       = "FFFFFF";
const ORANGE_C    = "FFF3E0";

// ── Bordures tableau ──────────────────────────────────────
const brd = (color = "CCCCCC") => ({ style: BorderStyle.SINGLE, size: 1, color });
const borders = (c = "CCCCCC") => ({ top: brd(c), bottom: brd(c), left: brd(c), right: brd(c) });
const noBorders = () => ({
  top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
});

// ── Helpers ───────────────────────────────────────────────
const sp = (before = 0, after = 0) => ({ spacing: { before, after } });
const shade = (fill) => ({ fill, type: ShadingType.CLEAR });
const cm = { top: 80, bottom: 80, left: 120, right: 120 };

function cell(text, opts = {}) {
  const {
    fill = BLANC, bold = false, color = "000000", colspan = 1,
    align = AlignmentType.LEFT, fontSize = 20, borders: b = borders()
  } = opts;
  return new TableCell({
    columnSpan: colspan,
    borders: b,
    shading: shade(fill),
    margins: cm,
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: align,
      children: [new TextRun({ text: String(text), bold, color, size: fontSize, font: "Arial" })]
    })]
  });
}

function headerRow(texts, fill = GRIS_ENTETE, widths) {
  return new TableRow({
    tableHeader: true,
    children: texts.map((t, i) => cell(t, {
      fill, bold: true, color: BLANC, fontSize: 20,
      align: AlignmentType.CENTER,
    }))
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    ...sp(320, 160),
    children: [new TextRun({ text, bold: true, color: VERT_MOY, font: "Arial", size: 32 })]
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    ...sp(240, 120),
    children: [new TextRun({ text, bold: true, color: VERT_FONCE, font: "Arial", size: 26 })]
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    ...sp(160, 80),
    children: [new TextRun({ text, bold: true, color: "1A237E", font: "Arial", size: 22 })]
  });
}

function para(text, opts = {}) {
  const { bold = false, color = "222222", size = 20, before = 60, after = 60 } = opts;
  return new Paragraph({
    ...sp(before, after),
    children: [new TextRun({ text, bold, color, size, font: "Arial" })]
  });
}

function bullet(text, fill = "222222") {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    ...sp(40, 40),
    children: [new TextRun({ text, color: fill, size: 20, font: "Arial" })]
  });
}

function synthBox(text, fill = VERT_CLAIR, borderColor = VERT_MOY) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({ children: [new TableCell({
      borders: {
        top: brd(borderColor), bottom: brd(borderColor),
        left: { style: BorderStyle.SINGLE, size: 6, color: borderColor },
        right: brd(borderColor),
      },
      shading: shade(fill),
      margins: { top: 120, bottom: 120, left: 180, right: 120 },
      children: [
        new Paragraph({ children: [new TextRun({ text: "Synthèse", bold: true, color: borderColor, size: 20, font: "Arial" })] }),
        new Paragraph({ ...sp(60, 0), children: [new TextRun({ text, color: "333333", size: 19, font: "Arial" })] }),
      ]
    })] })]
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ════════════════════════════════════════════════════════════
// CONTENU DU DOCUMENT
// ════════════════════════════════════════════════════════════
const children = [];

// ── PAGE DE TITRE ─────────────────────────────────────────
children.push(
  new Paragraph({ ...sp(2000, 200), alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "🌱", size: 72, font: "Segoe UI Emoji" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, ...sp(200, 100),
    children: [new TextRun({ text: "RAPPORT D'ANALYSE STRATÉGIQUE", bold: true, color: VERT_MOY, size: 40, font: "Arial" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, ...sp(100, 400),
    children: [new TextRun({ text: "GIC JEPROCUVI — Mbanga, Cameroun", bold: true, color: GRIS_ENTETE, size: 32, font: "Arial" })] }),
  new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [9360],
    rows: [new TableRow({ children: [new TableCell({
      borders: borders(VERT_MOY), shading: shade(VERT_CLAIR), margins: cm,
      children: [
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Groupement d'Initiative Commune", bold: true, color: VERT_FONCE, size: 24, font: "Arial" })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Légalisé en Mai 2013 · 10 membres · 15 ha de cacao · Affilié à GRIMBA", color: "444444", size: 20, font: "Arial" })] }),
      ]
    })] })]
  }),
  new Paragraph({ ...sp(400, 100), alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Date du rapport : Juin 2026", color: "555555", size: 20, font: "Arial" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, ...sp(60, 60),
    children: [new TextRun({ text: "Analyste : Agent IA Stratégique OPA/EFA", color: "555555", size: 20, font: "Arial" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, ...sp(60, 2000),
    children: [new TextRun({ text: "Outils : Étoile du Conseil · SWOT · PESTEL · 5 Forces de Porter · BCG · Ansoff", color: "888888", size: 18, font: "Arial" })] }),
  pageBreak(),
);

// ── TABLE DES MATIÈRES ────────────────────────────────────
children.push(
  new Paragraph({ heading: HeadingLevel.HEADING_1, ...sp(0, 200),
    children: [new TextRun({ text: "Table des matières", bold: true, color: VERT_MOY, size: 32, font: "Arial" })] }),
  new TableOfContents("Table des matières", { hyperlink: true, headingStyleRange: "1-3" }),
  pageBreak(),
);

// ── INTRODUCTION ──────────────────────────────────────────
children.push(
  h1("Introduction"),
  para("Le GIC JEPROCUVI (Groupement d'Initiative Commune) est une organisation paysanne créée en octobre 2009 et légalisée en mai 2013, basée à Mbanga, Cameroun. Il regroupe 10 membres (8 hommes, 2 femmes) dont l'activité principale est la production de cacao sur 15 hectares au total, pour une production annuelle d'environ 15 tonnes."),
  para("Ce rapport présente l'analyse stratégique complète du GIC, réalisée à partir du diagnostic organisationnel, à l'aide de six outils complémentaires : l'Étoile du Conseil, le SWOT, le PESTEL, les 5 Forces de Porter, la Matrice BCG et la Matrice d'Ansoff."),
  new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [2000, 7360],
    rows: [
      headerRow(["Information", "Détail"], VERT_MOY),
      ...[
        ["Nom", "GIC JEPROCUVI"],
        ["Localisation", "Mbanga, Cameroun"],
        ["Création", "Octobre 2009 · Légalisé Mai 2013"],
        ["Membres", "10 (8 hommes, 2 femmes)"],
        ["Activité principale", "Production de cacao — 15 ha — ~15 t/an"],
        ["Activités secondaires", "Élevage porcin (2 truies + 1 verrat) · Épargne-crédit interne"],
        ["Affiliation", "GRIMBA (Union de GICs) pour commercialisation et séchage"],
        ["Marché principal", "Marché périodique de Mbanga (1 025 FCFA/kg)"],
      ].map((r, i) => new TableRow({ children: [
        cell(r[0], { fill: i % 2 === 0 ? GRIS_CLAIR : BLANC, bold: true }),
        cell(r[1], { fill: i % 2 === 0 ? GRIS_CLAIR : BLANC }),
      ]}))
    ]
  }),
  pageBreak(),
);

// ════════════════════════════════════════════════════════════
// 1. ÉTOILE DU CONSEIL
// ════════════════════════════════════════════════════════════
children.push(h1("1. Étoile du Conseil"));
children.push(para("L'Étoile du Conseil est un outil de diagnostic multidimensionnel à 6 branches permettant d'évaluer la situation globale du GIC sur une échelle de 1 (très faible) à 5 (excellent).", { before: 60, after: 120 }));

const etoileData = [
  ["⭐ Dimension", "Score", "Observations", "fill"],
  ["Moyens de production",          "2/5", "Pas de terres propres (location 200 000 FCFA/ha/an). Matériel rudimentaire (machette/houe). Aucun four de séchage collectif. Pas de siège social.", ROUGE_CLAIR],
  ["Performances technico-écon.",   "2/5", "Rendement ~1 t/ha (15 t sur 15 ha). Plantations vieillissantes (~50 ans). Faible maîtrise des itinéraires techniques. Séchage externalisé à GRIMBA (−10%).", ROUGE_CLAIR],
  ["Finances",                      "2/5", "Pas de compte bancaire. Fonds gérés par le trésorier. Cotisations faibles (2 000–5 000 FCFA/mois). Crédit interne à 4%. Aucun fond de roulement.", ROUGE_CLAIR],
  ["Milieu local",                  "3/5", "Climat favorable. Axe Douala-Bafoussam avantageux. Présence MINADER/MINEPIA. Enclavement partiel. Maladies cacao présentes.", VERT_CLAIR],
  ["Politiques publiques",          "2/5", "Appui technique d'un seul technicien. Structures d'État peu opérationnelles. Absence de subventions directes identifiées.", ROUGE_CLAIR],
  ["Marchés / Filières",            "3/5", "Marché périodique de Mbanga (1 025 FCFA/kg). Commercialisation via GRIMBA. Un seul débouché. Proximité Douala non exploitée.", VERT_CLAIR],
];

children.push(new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: [3200, 900, 5260],
  rows: [
    new TableRow({ tableHeader: true, children: [
      cell("Dimension", { fill: VERT_MOY, bold: true, color: BLANC }),
      cell("Score",     { fill: VERT_MOY, bold: true, color: BLANC, align: AlignmentType.CENTER }),
      cell("Observations", { fill: VERT_MOY, bold: true, color: BLANC }),
    ]}),
    ...etoileData.slice(1).map(([dim, score, obs, fill]) => new TableRow({ children: [
      cell(dim,   { fill, bold: true, fontSize: 19 }),
      cell(score, { fill, bold: true, align: AlignmentType.CENTER, color: score.startsWith("2") ? ROUGE_FONCE : VERT_FONCE }),
      cell(obs,   { fill, fontSize: 19 }),
    ]}))
  ]
}));

children.push(
  new Paragraph({ ...sp(160, 80) }),
  synthBox("Le GIC JEPROCUVI présente de fortes faiblesses structurelles dans ses moyens de production, ses performances techniques et l'accès aux politiques publiques (scores 2/5). Le milieu local et les marchés offrent un potentiel réel (3/5) insuffisamment valorisé. Priorité absolue : sécurisation foncière, réhabilitation des vergers vieillissants, structuration financière et renforcement des services rendus aux membres."),
  pageBreak(),
);

// ════════════════════════════════════════════════════════════
// 2. SWOT
// ════════════════════════════════════════════════════════════
children.push(h1("2. Analyse SWOT"));

const swotData = {
  forces: [
    "Existence de statuts et règlement intérieur légalisés (2013)",
    "Cohésion sociale forte entre les 10 membres",
    "Réunions mensuelles régulières et transparence financière",
    "Achat groupé d'intrants (engrais, pesticides) avec crédit interne à 4%",
    "Appartenance à GRIMBA (union de GICs) pour la commercialisation",
    "Expérience de la culture cacaoyère transmise sur 50 ans",
    "Diversification des activités des membres (moto-taxi, commerce, élevage)",
  ],
  faiblesses: [
    "Pas de terres propres — location précaire à 200 000 FCFA/ha/an",
    "Plantations vieillissantes (~50 ans, héritées des parents)",
    "Faible rendement (~1 t/ha au lieu de 2–3 t/ha recommandés)",
    "Pas de compte bancaire, pas de siège social",
    "Faible maîtrise de la gestion administrative et comptable",
    "Matériel rudimentaire, aucun four de séchage propre",
    "Registres non tenus à jour, rapports d'activités irréguliers",
    "Peu de services rendus aux membres (faible valeur ajoutée du GIC)",
    "Proximité élevage/habitations (risque sanitaire)",
  ],
  opportunites: [
    "Marché local de Mbanga à fort potentiel et proximité de Douala",
    "Axe Douala-Bafoussam facilitant l'approvisionnement et l'écoulement",
    "Présence de structures d'appui MINADER/MINEPIA",
    "Possibilité de transformation locale (séchage, valorisation du cacao)",
    "Demande mondiale soutenue et prix cacao en hausse (2023-2024)",
    "Réhabilitation des vergers possible via programmes partenaires",
    "Développement de l'élevage porcin comme source de revenu complémentaire",
    "Production de rejets améliorés pour diversifier les revenus",
  ],
  menaces: [
    "Maladies cacao : capsides, pourriture brune, autres nuisibles",
    "Peste porcine africaine récurrente dans la zone",
    "Enclavement des zones de production",
    "Vols des récoltes et du bétail",
    "Pesticides et engrais de mauvaise qualité sur le marché local",
    "Dépendance à un seul acheteur (GRIMBA retient 10% + 15 FCFA/kg)",
    "Volatilité des prix sur le marché mondial du cacao",
  ],
};

const maxSwot = Math.max(...Object.values(swotData).map(a => a.length));

children.push(new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: [4680, 4680],
  rows: [
    new TableRow({ children: [
      cell("💪 FORCES", { fill: VERT_MOY, bold: true, color: BLANC, align: AlignmentType.CENTER }),
      cell("⚠️ FAIBLESSES", { fill: ROUGE_FONCE, bold: true, color: BLANC, align: AlignmentType.CENTER }),
    ]}),
    new TableRow({ children: [
      new TableCell({ borders: borders(), shading: shade(VERT_CLAIR), margins: cm, children: swotData.forces.map(t => bullet(t, VERT_FONCE)) }),
      new TableCell({ borders: borders(), shading: shade(ROUGE_CLAIR), margins: cm, children: swotData.faiblesses.map(t => bullet(t, ROUGE_FONCE)) }),
    ]}),
    new TableRow({ children: [
      cell("🌱 OPPORTUNITÉS", { fill: "1565C0", bold: true, color: BLANC, align: AlignmentType.CENTER }),
      cell("⚡ MENACES", { fill: "E65100", bold: true, color: BLANC, align: AlignmentType.CENTER }),
    ]}),
    new TableRow({ children: [
      new TableCell({ borders: borders(), shading: shade(BLEU_CLAIR), margins: cm, children: swotData.opportunites.map(t => bullet(t, "1565C0")) }),
      new TableCell({ borders: borders(), shading: shade(JAUNE_CLAIR), margins: cm, children: swotData.menaces.map(t => bullet(t, "E65100")) }),
    ]}),
  ]
}));

children.push(
  new Paragraph({ ...sp(160, 80) }),
  synthBox("Stratégie SO — Mobiliser la cohésion sociale et l'appartenance à GRIMBA pour accéder aux programmes de réhabilitation des vergers et valoriser la proximité de Douala. Stratégie WT — Renforcer la gestion administrative, sécuriser le foncier et diversifier les sources de revenus (élevage, transformation) pour réduire la vulnérabilité."),
  pageBreak(),
);

// ════════════════════════════════════════════════════════════
// 3. PESTEL
// ════════════════════════════════════════════════════════════
children.push(h1("3. Analyse PESTEL"));

const pestelData = [
  { label: "🏛️ Politique",       fill: "FCE4EC", items: ["Présence MINADER/MINEPIA avec appui technique", "Légalisation du GIC assurée (2013)", "Faible opérationnalisation des programmes d'appui aux coopératives", "Absence de subventions directes aux intrants identifiées"] },
  { label: "💰 Économique",      fill: "FFF3E0", items: ["Prix cacao à 1 025 FCFA/kg (marché Mbanga)", "Coût de location des terres élevé : 200 000 FCFA/ha/an", "Cotisations membres faibles (2 000–5 000 FCFA/mois)", "Hausse mondiale des prix cacao (opportunité de valorisation)"] },
  { label: "👥 Social",          fill: VERT_CLAIR, items: ["10 membres (8H/2F) — cohésion sociale forte", "Plantations héritées, savoir-faire familial sur 50 ans", "Femmes sous-représentées dans le bureau exécutif", "Transmission intergénérationnelle du métier à renforcer"] },
  { label: "⚙️ Technologique",   fill: BLEU_CLAIR, items: ["Matériel rudimentaire (machette, houe)", "Absence de four de séchage propre — séchage externalisé à GRIMBA (−10%)", "Techniques de production des rejets non maîtrisées", "Pulvérisateurs individuels utilisés collectivement"] },
  { label: "🌿 Environnemental", fill: "F1F8E9", items: ["Climat favorable aux cultures (cacao, bananier, manioc)", "Maladies cacao : capsides, pourriture brune", "Peste porcine africaine récurrente", "Pesticides de qualité douteuse sur le marché local"] },
  { label: "⚖️ Légal",           fill: "EDE7F6", items: ["GIC légalisé avec statuts et règlement intérieur", "Affiliation à GRIMBA (union légale reconnue)", "Absence de compte bancaire formel (risque légal)", "Registres non tenus à jour — pas de titre foncier"] },
];

children.push(new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: [2000, 7360],
  rows: [
    headerRow(["Facteur", "Éléments identifiés"], VERT_MOY),
    ...pestelData.map(({ label, fill, items }) => new TableRow({ children: [
      cell(label, { fill, bold: true, fontSize: 19 }),
      new TableCell({ borders: borders(), shading: shade(fill), margins: cm, children: items.map(t => bullet(t)) }),
    ]}))
  ]
}));

children.push(
  new Paragraph({ ...sp(160, 80) }),
  synthBox("L'environnement présente un potentiel réel (climat favorable, proximité Douala, prix cacao en hausse) mais le GIC est insuffisamment armé pour en tirer parti : fragilité juridique (pas de compte bancaire, registres non tenus), dépendance technologique (séchage externalisé), et exposition aux risques phytosanitaires et de vol."),
  pageBreak(),
);

// ════════════════════════════════════════════════════════════
// 4. PORTER
// ════════════════════════════════════════════════════════════
children.push(h1("4. Les 5 Forces de Porter"));
children.push(para("Évaluation de l'intensité concurrentielle de la filière cacao à Mbanga selon le modèle de Porter (1 = faible, 5 = très élevée).", { before: 60, after: 120 }));

const porterData = [
  ["🚪 Menace de nouveaux entrants",    "2/5", VERT_CLAIR,  VERT_FONCE,  "Barrières modérées : foncier, savoir-faire cacaoyer, appartenance à GRIMBA. Peu de nouveaux entrants à court terme dans la zone de Mbanga."],
  ["🏭 Pouvoir des fournisseurs",        "4/5", ROUGE_CLAIR, ROUGE_FONCE, "Forte dépendance aux fournisseurs d'intrants de Douala/Mbanga. Pesticides de qualité douteuse. Peu d'alternatives locales certifiées. Prix imposés par les distributeurs."],
  ["🛒 Pouvoir des acheteurs",           "4/5", ROUGE_CLAIR, ROUGE_FONCE, "Monopsone de fait : GRIMBA est le seul débouché organisé (retient 10% + 15 FCFA/kg). Marché de Mbanga comme seule alternative directe. Prix fixés par l'acheteur."],
  ["🔄 Menace des produits substituts", "2/5", VERT_CLAIR,  VERT_FONCE,  "Peu de substituts directs au cacao. Concurrence des autres cultures de rente (bananier, manioc) pour l'usage des terres, mais cacao reste dominant dans la zone."],
  ["⚔️ Rivalité entre concurrents",     "3/5", JAUNE_CLAIR, "E65100",    "Autres producteurs de cacao de Mbanga concurrents directs. Vente au même marché périodique. Différenciation quasi nulle (pas de certification, même débouché GRIMBA)."],
];

children.push(new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: [3200, 800, 5360],
  rows: [
    headerRow(["Force", "Score", "Analyse"], VERT_MOY),
    ...porterData.map(([force, score, fill, scoreColor, analyse]) => new TableRow({ children: [
      cell(force,   { fill, bold: true, fontSize: 19 }),
      cell(score,   { fill, bold: true, color: scoreColor, align: AlignmentType.CENTER }),
      cell(analyse, { fill, fontSize: 19 }),
    ]}))
  ]
}));

children.push(
  new Paragraph({ ...sp(160, 80) }),
  synthBox("La filière est dominée par un fort pouvoir des acheteurs et des fournisseurs (4/5). Le GIC est en position de faiblesse structurelle. Recommandation : renforcer le pouvoir de marché via la diversification des débouchés (vente directe à Douala), l'acquisition d'un four de séchage propre et la recherche de fournisseurs d'intrants agréés."),
  pageBreak(),
);

// ════════════════════════════════════════════════════════════
// 5. BCG
// ════════════════════════════════════════════════════════════
children.push(h1("5. Matrice BCG — Portefeuille d'activités"));

const bcgData = [
  ["Cacao conventionnel (via GRIMBA)", "Élevée",  "Faible",     "🐄 Vache à lait", BLEU_CLAIR,  "Maintenir et améliorer les rendements. Base financière du GIC."],
  ["Élevage porcin",                   "Faible",  "Forte",      "❓ Dilemme",       JAUNE_CLAIR, "Investir si maîtrise sanitaire assurée (prévention peste porcine africaine)."],
  ["Séchage / transformation cacao",   "Nulle",   "Très forte", "❓ Dilemme",       JAUNE_CLAIR, "Acquérir un four collectif pour reprendre le séchage et capturer la valeur ajoutée."],
  ["Manioc / Bananier plantain",       "Nulle",   "Nulle",      "🐕 Poids mort",    ROUGE_CLAIR, "Abandonnés depuis 2010-2013. Ne pas relancer sans sécurisation foncière préalable."],
];

children.push(new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: [2700, 1200, 1200, 1400, 2860],
  rows: [
    headerRow(["Activité", "Part marché", "Croissance", "Quadrant", "Stratégie"], VERT_MOY),
    ...bcgData.map(([act, pdm, cro, quad, fill, strat]) => new TableRow({ children: [
      cell(act,  { fill, bold: true, fontSize: 19 }),
      cell(pdm,  { fill, align: AlignmentType.CENTER, fontSize: 19 }),
      cell(cro,  { fill, align: AlignmentType.CENTER, fontSize: 19 }),
      cell(quad, { fill, bold: true, align: AlignmentType.CENTER, fontSize: 18 }),
      cell(strat,{ fill, fontSize: 18 }),
    ]}))
  ]
}));

children.push(
  new Paragraph({ ...sp(160, 80) }),
  synthBox("Le cacao conventionnel est la « vache à lait » du GIC mais à faible rentabilité (rendements bas, dépendance à GRIMBA). La transformation (séchage) et l'élevage porcin sont des « dilemmes » à fort potentiel si le GIC investit dans les capacités techniques et sanitaires nécessaires."),
  pageBreak(),
);

// ════════════════════════════════════════════════════════════
// 6. ANSOFF
// ════════════════════════════════════════════════════════════
children.push(h1("6. Matrice d'Ansoff — Stratégies de croissance"));

const ansoffData = [
  {
    label: "📈 Pénétration de marché", sub: "Produits existants · Marchés existants", fill: "C8E6C9", color: "1B5E20",
    items: [
      "Améliorer les rendements cacao par la réhabilitation des vergers vieillissants",
      "Adopter les itinéraires techniques recommandés (fertilisation, traitement capsides/pourriture brune)",
      "Augmenter le volume vendu via GRIMBA en améliorant la qualité de fermentation/séchage",
      "Renforcer la tenue des registres pour mieux suivre les performances",
      "Constituer un fond de roulement collectif pour sécuriser les intrants de qualité",
    ]
  },
  {
    label: "🆕 Développement de produits", sub: "Nouveaux produits · Marchés existants", fill: "B3E5FC", color: "01579B",
    items: [
      "Acquérir un four de séchage collectif pour proposer du cacao séché de qualité premium",
      "Maîtriser la production de rejets améliorés à vendre aux membres et producteurs voisins",
      "Développer l'élevage porcin avec maîtrise de la formulation des aliments (PIF)",
      "Proposer des services aux membres : conseil technique, approvisionnement intrants certifiés",
    ]
  },
  {
    label: "🌍 Développement de marchés", sub: "Produits existants · Nouveaux marchés", fill: "FFF9C4", color: "F57F17",
    items: [
      "Exploiter la proximité de Douala pour une vente directe aux acheteurs/transformateurs",
      "Diversifier les acheteurs au-delà de GRIMBA (contrats avec négociants agréés)",
      "Accéder aux marchés des organisations d'appui (certifications, labels qualité)",
      "Vendre le cacao séché directement sur le marché de Douala à prix supérieur",
    ]
  },
  {
    label: "🔀 Diversification", sub: "Nouveaux produits · Nouveaux marchés", fill: "F8BBD0", color: "880E4F",
    items: [
      "Développer l'élevage porcin intensif (truies reproductrices, porcelets) pour les marchés urbains",
      "Explorer l'agroforesterie cacao + cultures associées valorisées (macabo, taro)",
      "Ouvrir une activité de prestation de séchage pour les autres producteurs de la zone",
      "Envisager à terme une épargne-crédit formalisée (caisse rurale) pour les membres",
    ]
  },
];

children.push(new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: [4680, 4680],
  rows: [
    new TableRow({ children: [
      cell("", { fill: GRIS_CLAIR, bold: true }),
      cell("Marchés existants", { fill: VERT_MOY, bold: true, color: BLANC, align: AlignmentType.CENTER }),
      // note: only 2 cols shown; ansoff rendered as 2x2 below
    ]}),
    ...[[0,1],[2,3]].map(([a, b]) => new TableRow({ children: [
      new TableCell({ borders: borders(), shading: shade(ansoffData[a].fill), margins: { top: 120, bottom: 120, left: 140, right: 120 }, children: [
        new Paragraph({ children: [new TextRun({ text: ansoffData[a].label, bold: true, color: ansoffData[a].color, size: 21, font: "Arial" })] }),
        new Paragraph({ ...sp(40, 80), children: [new TextRun({ text: ansoffData[a].sub, color: "555555", size: 17, font: "Arial", italics: true })] }),
        ...ansoffData[a].items.map(t => bullet(t)),
      ]}),
      new TableCell({ borders: borders(), shading: shade(ansoffData[b].fill), margins: { top: 120, bottom: 120, left: 140, right: 120 }, children: [
        new Paragraph({ children: [new TextRun({ text: ansoffData[b].label, bold: true, color: ansoffData[b].color, size: 21, font: "Arial" })] }),
        new Paragraph({ ...sp(40, 80), children: [new TextRun({ text: ansoffData[b].sub, color: "555555", size: 17, font: "Arial", italics: true })] }),
        ...ansoffData[b].items.map(t => bullet(t)),
      ]}),
    ]}))
  ]
}));

children.push(
  new Paragraph({ ...sp(160, 80) }),
  synthBox("La priorité immédiate est la pénétration de marché (amélioration des rendements et de la qualité) et le développement de produits (four de séchage, rejets améliorés, élevage porcin). Le développement de marchés vers Douala est un objectif à moyen terme. La diversification (agroforesterie, caisse rurale) est une vision à long terme à construire dès maintenant."),
  pageBreak(),
);

// ════════════════════════════════════════════════════════════
// 7. RECOMMANDATIONS
// ════════════════════════════════════════════════════════════
children.push(h1("7. Recommandations stratégiques prioritaires"));

const recos = [
  {
    horizon: "Court terme (0–12 mois)", fill: ROUGE_CLAIR, color: ROUGE_FONCE,
    items: [
      "Ouvrir un compte bancaire collectif et formaliser la comptabilité du GIC",
      "Renforcer les capacités en gestion administrative et comptable (registres, PV, rapports)",
      "Former les membres aux itinéraires techniques cacao (traitement capsides, pourriture brune, fertilisation)",
      "Identifier des fournisseurs d'intrants certifiés et agréés (éviter les produits de qualité douteuse)",
      "Constituer un fond de roulement à partir des cotisations et des revenus de la campagne",
    ]
  },
  {
    horizon: "Moyen terme (1–3 ans)", fill: JAUNE_CLAIR, color: "E65100",
    items: [
      "Acquérir un four de séchage collectif (construction ou achat groupé via GRIMBA)",
      "Engager un processus de sécurisation foncière (acquisition ou bail longue durée)",
      "Réhabiliter les vergers vieillissants (greffage, replantation avec variétés améliorées)",
      "Développer l'élevage porcin avec formation en techniques d'élevage et formulation alimentaire",
      "Diversifier les débouchés commerciaux (contacts directs avec acheteurs à Douala)",
    ]
  },
  {
    horizon: "Long terme (3–5 ans)", fill: VERT_CLAIR, color: VERT_FONCE,
    items: [
      "Construire un siège social du GIC (base de travail collectif)",
      "Accéder à la certification qualité pour valoriser le cacao sur les marchés premium",
      "Créer une épargne-crédit formalisée (caisse rurale ou tontine structurée)",
      "Développer une activité de prestation de séchage pour les autres producteurs de la zone",
      "Explorer l'agroforesterie et les marchés carbone comme sources de revenus additionnels",
    ]
  },
];

children.push(new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: [2400, 6960],
  rows: [
    headerRow(["Horizon", "Actions prioritaires"], VERT_MOY),
    ...recos.map(({ horizon, fill, color, items }) => new TableRow({ children: [
      cell(horizon, { fill, bold: true, color, align: AlignmentType.CENTER }),
      new TableCell({ borders: borders(), shading: shade(fill), margins: cm, children: items.map((t, i) => new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        ...sp(40, 40),
        children: [new TextRun({ text: t, color: "222222", size: 19, font: "Arial" })]
      })) }),
    ]}))
  ]
}));

children.push(pageBreak());

// ── CONCLUSION ────────────────────────────────────────────
children.push(
  h1("Conclusion"),
  para("Le GIC JEPROCUVI dispose d'une base solide : cohésion sociale, expérience cacaoyère multigénérationnelle et accès à un marché local dynamique via GRIMBA. Cependant, des faiblesses structurelles majeures — absence de terres propres, plantations vieillissantes, faible capacité de gestion et dépendance à un seul acheteur — limitent fortement sa performance et sa résilience."),
  para("La stratégie de développement recommandée s'articule en trois temps : renforcer les bases (gestion, formation, fonds de roulement) à court terme, puis investir dans les équipements et la sécurisation foncière à moyen terme, et enfin diversifier et valoriser à long terme. Chaque étape construit sur la précédente pour transformer progressivement le GIC en une organisation productive, financièrement solide et autonome."),
  para("Ce rapport constitue un outil d'aide à la décision. Les propositions formulées devront être validées et adaptées par le conseiller agropastoral en concertation avec les membres du GIC.", { color: "666666" }),
  new Paragraph({ ...sp(400, 200), alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "— Rapport généré par l'Agent IA Stratégique OPA/EFA · Juin 2026 —", color: "999999", size: 18, italics: true, font: "Arial" })] }),
);

// ════════════════════════════════════════════════════════════
// ASSEMBLAGE DU DOCUMENT
// ════════════════════════════════════════════════════════════
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•",
          alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] },
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: VERT_MOY, font: "Arial" },
        paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, color: VERT_FONCE, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, color: "1A237E", font: "Arial" },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 } },
    ]
  },
  sections: [{
    properties: {
      page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 } }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: VERT_MOY, space: 4 } },
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "Rapport Stratégique — GIC JEPROCUVI · Juin 2026", color: "888888", size: 16, font: "Arial" })]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: VERT_MOY, space: 4 } },
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "Agent IA Stratégique OPA/EFA  ·  Page ", color: "888888", size: 16, font: "Arial" }),
          new TextRun({ children: [PageNumber.CURRENT], color: "888888", size: 16, font: "Arial" }),
          new TextRun({ text: " / ", color: "888888", size: 16, font: "Arial" }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], color: "888888", size: 16, font: "Arial" }),
        ]
      })] })
    },
    children,
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("Rapport_Strategique_GIC_JEPROCUVI.docx", buf);
  console.log("OK: rapports/Rapport_Strategique_GIC_JEPROCUVI.docx");
}).catch(e => { console.error("ERREUR:", e.message); process.exit(1); });
