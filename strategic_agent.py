"""
Agent IA Stratégique OPA / EFA — Bilingual FR/EN
Strategic AI Agent for Producer Organizations and Family Farms

Run:  streamlit run strategic_agent.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

from modules.i18n_strat import t
from modules import ai_strat, doc_extractor

# ─────────────────────────────────────────────
# PAGE CONFIG & CUSTOM CSS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Agent IA · Analyse Stratégique OPA/EFA",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* Top gradient banner */
[data-testid="stAppViewContainer"] > .main::before {
    content: "";
    display: block;
    height: 5px;
    background: linear-gradient(90deg, #2e7d32, #66bb6a, #a5d6a7);
    margin-bottom: 0;
}

/* Card-like metric containers */
div[data-testid="metric-container"] {
    background: #f1f8e9;
    border-left: 4px solid #66bb6a;
    border-radius: 6px;
    padding: 8px 12px;
}

/* SWOT quadrant-like text areas */
.swot-box {
    border-radius: 8px;
    padding: 10px;
    min-height: 160px;
}

/* Tool selector pills */
div[data-testid="stRadio"] > div {
    gap: 6px;
}

/* Section headers */
h2 { color: #2e7d32; }
h3 { color: #388e3c; }

/* Sidebar branding */
section[data-testid="stSidebar"] {
    background: #f9fbe7;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
DEFAULTS = {
    "lang": "fr",
    "org_type": "opa",
    "api_key": "",
    "ollama_url": "http://localhost:11434",
    "ollama_model": "llama3",
    "backend": "demo",   # "claude" | "ollama" | "demo"
    "doc_text": "",
    "doc_name": "",
    "doc_pages": 0,
    # per-tool AI results
    "res_etoile": {},
    "res_swot": {},
    "res_pestel": {},
    "res_porter": {},
    "res_bcg": [],
    "res_ansoff": {},
    # manual overrides
    "etoile_scores": {"milieu": 3, "perf": 3, "moyens": 3, "politiques": 3, "marches": 3, "finances": 3},
    "etoile_obs": {"milieu": "", "perf": "", "moyens": "", "politiques": "", "marches": "", "finances": ""},
    "swot_manual": {"forces": "", "faiblesses": "", "opportunites": "", "menaces": ""},
    "pestel_manual": {"politique": "", "economique": "", "social": "", "techno": "", "environnement": "", "legal": ""},
    "porter_scores": {"nouveaux": 3, "fournisseurs": 3, "clients": 3, "substituts": 3, "rivalite": 3},
    "porter_comments": {"nouveaux": "", "fournisseurs": "", "clients": "", "substituts": "", "rivalite": ""},
    "bcg_rows": [{"activity": "Cacao", "share": 0.6, "growth": 5.0}],
    "ansoff_manual": {"penetration": "", "dev_produit": "", "dev_marche": "", "diversification": ""},
    "rapport_org": "",
    "rapport_analyst": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def _t(key):
    return t(key, st.session_state.lang)


def _has_results() -> bool:
    return any([
        st.session_state.res_etoile,
        st.session_state.res_swot,
        st.session_state.res_pestel,
        st.session_state.res_porter,
        st.session_state.res_bcg,
        st.session_state.res_ansoff,
    ])


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/1f33f.svg", width=48)
    st.markdown("## 🌱 Agent IA Stratégique")
    st.caption(_t("tagline"))
    st.divider()

    # Language
    lang_choice = st.radio(
        _t("language"),
        options=["fr", "en"],
        format_func=lambda x: "🇫🇷 Français" if x == "fr" else "🇬🇧 English",
        index=0 if st.session_state.lang == "fr" else 1,
        horizontal=True,
        key="lang_radio",
    )
    st.session_state.lang = lang_choice

    # Org type
    org_choice = st.radio(
        _t("org_type"),
        options=["opa", "efa"],
        format_func=lambda x: _t("org_opa") if x == "opa" else _t("org_efa"),
        index=0 if st.session_state.org_type == "opa" else 1,
        horizontal=True,
    )
    st.session_state.org_type = org_choice

    st.divider()

    # Navigation
    page = st.radio(
        "Navigation",
        options=["home", "import", "etoile", "swot", "pestel", "porter", "bcg", "ansoff", "rapport"],
        format_func=lambda x: _t(f"nav_{x}"),
        label_visibility="collapsed",
    )

    st.divider()

    # ── Backend selector ──────────────────────────
    backend = st.radio(
        "🧠 Moteur IA / AI Engine",
        options=["claude", "ollama", "demo"],
        format_func=lambda x: {
            "claude": "☁️ Claude API (Anthropic)",
            "ollama": "🖥️ Ollama (local / Edge)",
            "demo":   "🔎 Mode démo (sans IA)",
        }[x],
        index=["claude", "ollama", "demo"].index(st.session_state.backend),
    )
    st.session_state.backend = backend

    if backend == "claude":
        with st.expander("🔑 " + _t("api_key_label"), expanded=True):
            api_input = st.text_input(
                _t("api_key_label"),
                value=st.session_state.api_key,
                type="password",
                help=_t("api_key_help"),
                label_visibility="collapsed",
            )
            st.session_state.api_key = api_input
        if st.session_state.api_key:
            st.success(_t("api_key_set"))
        else:
            st.warning("Entrez votre clé API Claude.")

    elif backend == "ollama":
        with st.expander("🖥️ Configuration Ollama", expanded=True):
            ollama_url = st.text_input(
                "URL Ollama",
                value=st.session_state.ollama_url,
                help="Ex: http://localhost:11434",
            )
            st.session_state.ollama_url = ollama_url

            # Try to list available models
            models = ai_strat.list_ollama_models(ollama_url)
            if models:
                st.session_state.ollama_model = st.selectbox(
                    "Modèle", options=models,
                    index=models.index(st.session_state.ollama_model)
                    if st.session_state.ollama_model in models else 0,
                )
                st.success(f"✅ Ollama connecté — {len(models)} modèle(s)")
            else:
                st.session_state.ollama_model = st.text_input(
                    "Modèle (manuel)", value=st.session_state.ollama_model
                )
                st.warning("Ollama non détecté. Vérifiez qu'il est lancé.")

    else:
        st.info(_t("api_key_missing"))

    st.divider()
    st.caption(_t("footer"))


# ─────────────────────────────────────────────
# HELPER : run AI for one tool
# ─────────────────────────────────────────────
def _ai_kwargs() -> dict:
    """Return kwargs for ai_strat.analyze / analyze_all based on selected backend."""
    b = st.session_state.backend
    return {
        "api_key":      st.session_state.api_key      if b == "claude" else "",
        "ollama_url":   st.session_state.ollama_url   if b == "ollama" else "",
        "ollama_model": st.session_state.ollama_model if b == "ollama" else "llama3",
    }


def run_ai(tool: str) -> dict | list:
    text = st.session_state.doc_text
    if not text:
        st.warning(_t("no_text_warning"))
        return {}
    backend_label = {"claude": "Claude API", "ollama": "Ollama local", "demo": "Mode démo"}
    with st.spinner(f"{_t('generating')} ({backend_label.get(st.session_state.backend, '')})"):
        try:
            result = ai_strat.analyze(
                text, tool,
                st.session_state.lang,
                st.session_state.org_type,
                **_ai_kwargs(),
            )
            return result
        except Exception as e:
            st.error(f"{_t('error_api')} — {e}")
            return {}


def run_all_ai():
    text = st.session_state.doc_text
    if not text:
        st.warning(_t("no_text_warning"))
        return
    backend_label = {"claude": "Claude API", "ollama": "Ollama local", "demo": "Mode démo"}
    with st.spinner(f"{_t('analyze_running')} ({backend_label.get(st.session_state.backend, '')})"):
        try:
            all_results = ai_strat.analyze_all(
                text,
                st.session_state.lang,
                st.session_state.org_type,
                **_ai_kwargs(),
            )
            st.session_state.res_etoile = all_results.get("etoile", {})
            st.session_state.res_swot = all_results.get("swot", {})
            st.session_state.res_pestel = all_results.get("pestel", {})
            st.session_state.res_porter = all_results.get("porter", {})
            st.session_state.res_bcg = all_results.get("bcg", [])
            st.session_state.res_ansoff = all_results.get("ansoff", {})
            st.success(_t("analyze_done"))
        except Exception as e:
            st.error(f"{_t('error_api')} — {e}")


# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
if page == "home":
    st.title(_t("home_title"))
    st.markdown(_t("home_intro"))

    st.divider()
    st.subheader(_t("home_steps"))
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info(_t("step1"))
    with c2:
        st.info(_t("step2"))
    with c3:
        st.info(_t("step3"))
    with c4:
        st.info(_t("step4"))

    st.divider()
    st.subheader(_t("home_status"))
    s1, s2, s3 = st.columns(3)
    with s1:
        if st.session_state.doc_text:
            st.metric(_t("doc_loaded"), st.session_state.doc_name or "—")
            st.caption(f"{len(st.session_state.doc_text):,} {_t('doc_chars')}")
        else:
            st.warning(_t("no_doc"))
    with s2:
        analyses = sum([
            bool(st.session_state.res_etoile),
            bool(st.session_state.res_swot),
            bool(st.session_state.res_pestel),
            bool(st.session_state.res_porter),
            bool(st.session_state.res_bcg),
            bool(st.session_state.res_ansoff),
        ])
        st.metric(_t("analyses_done"), f"{analyses} / 6")
    with s3:
        if not st.session_state.api_key:
            st.info(_t("demo_mode_info"))
        else:
            st.success(_t("api_key_set"))


# ─────────────────────────────────────────────
# PAGE: IMPORT
# ─────────────────────────────────────────────
elif page == "import":
    st.title(_t("import_title"))
    st.markdown(_t("import_intro"))

    tab_upload, tab_paste = st.tabs([
        f"📎 {_t('upload_label')}",
        f"📝 {_t('manual_text')}",
    ])

    with tab_upload:
        uploaded = st.file_uploader(
            _t("upload_label"),
            type=["pdf", "docx"],
            help=_t("upload_types"),
            label_visibility="collapsed",
        )
        if uploaded:
            if st.button(_t("extract_btn"), type="primary"):
                with st.spinner(_t("generating")):
                    try:
                        text, pages = doc_extractor.extract_text_from_file(uploaded)
                        st.session_state.doc_text = text
                        st.session_state.doc_name = uploaded.name
                        st.session_state.doc_pages = pages
                        st.success(f"✅ {_t('extract_success')} — {len(text):,} {_t('extract_chars')}, {pages} {_t('extract_pages')}")
                    except Exception as e:
                        st.error(f"{_t('extract_error')}: {e}")

    with tab_paste:
        manual_text = st.text_area(
            _t("manual_placeholder"),
            height=300,
            placeholder=_t("manual_placeholder"),
            label_visibility="collapsed",
        )
        if st.button(_t("use_manual"), type="primary"):
            if manual_text.strip():
                st.session_state.doc_text = manual_text.strip()
                st.session_state.doc_name = "texte_manuel"
                st.session_state.doc_pages = 1
                st.success(f"✅ {len(manual_text):,} {_t('extract_chars')}")

    if st.session_state.doc_text:
        st.divider()
        with st.expander(f"👁 {_t('text_preview')} ({_t('text_preview_note')})"):
            st.text(st.session_state.doc_text[:2000])

        st.divider()
        if not st.session_state.api_key:
            st.info(_t("demo_mode_info"))

        if st.button(
            _t("analyze_all_btn"),
            type="primary",
            help=_t("analyze_all_help"),
            use_container_width=True,
        ):
            run_all_ai()


# ─────────────────────────────────────────────
# PAGE: ÉTOILE DU CONSEIL
# ─────────────────────────────────────────────
elif page == "etoile":
    st.title(_t("etoile_title"))
    st.markdown(_t("etoile_intro"))

    BRANCHES = ["milieu", "perf", "moyens", "politiques", "marches", "finances"]

    tab_ai, tab_manual = st.tabs([_t("tab_ai"), _t("tab_manual")])

    with tab_ai:
        if st.button(_t("etoile_ai_btn"), type="primary"):
            result = run_ai("etoile")
            if result:
                st.session_state.res_etoile = result
                # push scores to manual sliders too
                for b in BRANCHES:
                    if b in result:
                        st.session_state.etoile_scores[b] = result[b].get("score", 3)
                        st.session_state.etoile_obs[b] = result[b].get("obs", "")

        r = st.session_state.res_etoile
        if r:
            scores = {b: r.get(b, {}).get("score", 3) for b in BRANCHES}
            labels = [_t(f"etoile_{b}") for b in BRANCHES]
            vals = [scores[b] for b in BRANCHES]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=labels + [labels[0]],
                fill="toself",
                fillcolor="rgba(76, 175, 80, 0.25)",
                line=dict(color="#2e7d32", width=2),
                name=_t("etoile_radar_title"),
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(size=11))),
                showlegend=False,
                height=450,
                margin=dict(l=60, r=60, t=40, b=40),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader(_t("etoile_synthesis"))
            st.info(r.get("synthesis", "—"))

            st.subheader(_t("etoile_obs"))
            cols = st.columns(3)
            for i, b in enumerate(BRANCHES):
                with cols[i % 3]:
                    bdata = r.get(b, {})
                    score = bdata.get("score", "—")
                    obs = bdata.get("obs", "—")
                    color = "#e8f5e9" if isinstance(score, int) and score >= 3 else "#fff3e0"
                    st.markdown(
                        f"""<div style="background:{color};border-radius:8px;padding:10px;margin-bottom:8px;">
                        <b>{_t(f'etoile_{b}')}</b><br>
                        Score : <b>{score}/5</b><br>
                        <small>{obs}</small></div>""",
                        unsafe_allow_html=True,
                    )
        else:
            st.info("👈 " + _t("etoile_no_doc"))

    with tab_manual:
        st.caption(_t("etoile_score"))
        scores = st.session_state.etoile_scores
        obs = st.session_state.etoile_obs
        cols = st.columns(3)
        for i, b in enumerate(BRANCHES):
            with cols[i % 3]:
                scores[b] = st.slider(
                    _t(f"etoile_{b}"), 1, 5, scores[b], key=f"slider_{b}"
                )
                obs[b] = st.text_area(
                    _t("etoile_obs"), value=obs[b], height=80, key=f"obs_{b}",
                    label_visibility="collapsed",
                )

        if st.button(_t("etoile_generate"), type="secondary"):
            labels = [_t(f"etoile_{b}") for b in BRANCHES]
            vals = [scores[b] for b in BRANCHES]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=labels + [labels[0]],
                fill="toself",
                fillcolor="rgba(76, 175, 80, 0.25)",
                line=dict(color="#2e7d32", width=2),
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=False,
                height=420,
                margin=dict(l=60, r=60, t=30, b=30),
            )
            st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE: SWOT
# ─────────────────────────────────────────────
elif page == "swot":
    st.title(_t("swot_title"))
    st.markdown(_t("swot_intro"))

    tab_ai, tab_manual = st.tabs([_t("tab_ai"), _t("tab_manual")])

    SWOT_KEYS = ["forces", "faiblesses", "opportunites", "menaces"]
    SWOT_COLORS = {"forces": "#e8f5e9", "faiblesses": "#ffebee", "opportunites": "#e3f2fd", "menaces": "#fff8e1"}

    def _render_swot(data: dict):
        c1, c2 = st.columns(2)
        for idx, key in enumerate(SWOT_KEYS):
            col = c1 if idx % 2 == 0 else c2
            with col:
                items = data.get(key, [])
                if isinstance(items, list):
                    content = "".join(f"<li>{i}</li>" for i in items)
                else:
                    content = "".join(f"<li>{line}</li>" for line in str(items).splitlines() if line.strip())
                st.markdown(
                    f"""<div style="background:{SWOT_COLORS[key]};border-radius:10px;padding:14px;margin-bottom:10px;min-height:160px;">
                    <b style="font-size:1.05rem">{_t(f'swot_{key}')}</b>
                    <ul style="margin-top:8px;padding-left:16px">{content}</ul></div>""",
                    unsafe_allow_html=True,
                )
        if data.get("synthesis"):
            st.divider()
            st.subheader(_t("swot_synthesis"))
            st.info(data["synthesis"])

    with tab_ai:
        if st.button(_t("swot_ai_btn"), type="primary"):
            result = run_ai("swot")
            if result:
                st.session_state.res_swot = result
                for key in SWOT_KEYS:
                    items = result.get(key, [])
                    st.session_state.swot_manual[key] = "\n".join(items) if isinstance(items, list) else str(items)

        if st.session_state.res_swot:
            _render_swot(st.session_state.res_swot)
        else:
            st.info("👈 " + _t("no_text_warning"))

    with tab_manual:
        manual = st.session_state.swot_manual
        c1, c2 = st.columns(2)
        for idx, key in enumerate(SWOT_KEYS):
            col = c1 if idx % 2 == 0 else c2
            with col:
                manual[key] = st.text_area(
                    _t(f"swot_{key}"),
                    value=manual[key],
                    height=160,
                    placeholder=_t("swot_placeholder"),
                    key=f"swot_ta_{key}",
                )

        if st.button(_t("swot_generate"), type="secondary"):
            manual_data = {
                key: [l for l in manual[key].splitlines() if l.strip()]
                for key in SWOT_KEYS
            }
            _render_swot(manual_data)


# ─────────────────────────────────────────────
# PAGE: PESTEL
# ─────────────────────────────────────────────
elif page == "pestel":
    st.title(_t("pestel_title"))
    st.markdown(_t("pestel_intro"))

    PESTEL_KEYS = ["politique", "economique", "social", "techno", "environnement", "legal"]
    PESTEL_COLORS = {
        "politique": "#fce4ec", "economique": "#fff3e0", "social": "#e8f5e9",
        "techno": "#e3f2fd", "environnement": "#f1f8e9", "legal": "#ede7f6",
    }

    tab_ai, tab_manual = st.tabs([_t("tab_ai"), _t("tab_manual")])

    with tab_ai:
        if st.button(_t("pestel_ai_btn"), type="primary"):
            result = run_ai("pestel")
            if result:
                st.session_state.res_pestel = result
                for k in PESTEL_KEYS:
                    items = result.get(k, [])
                    st.session_state.pestel_manual[k] = "\n".join(items) if isinstance(items, list) else str(items)

        p = st.session_state.res_pestel
        if p:
            st.subheader(_t("pestel_table_title"))
            rows = []
            for k in PESTEL_KEYS:
                items = p.get(k, [])
                if isinstance(items, list):
                    for item in items:
                        rows.append({"Facteur": _t(f"pestel_{k}"), "Élément": item})
                elif items:
                    rows.append({"Facteur": _t(f"pestel_{k}"), "Élément": str(items)})
            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True, height=450)

            st.divider()
            cols = st.columns(3)
            for i, k in enumerate(PESTEL_KEYS):
                with cols[i % 3]:
                    items = p.get(k, [])
                    content = "".join(f"<li>{item}</li>" for item in (items if isinstance(items, list) else []))
                    st.markdown(
                        f"""<div style="background:{PESTEL_COLORS[k]};border-radius:8px;padding:12px;margin-bottom:8px;min-height:100px;">
                        <b>{_t(f'pestel_{k}')}</b>
                        <ul style="margin-top:6px;padding-left:14px;font-size:0.9rem">{content}</ul></div>""",
                        unsafe_allow_html=True,
                    )
        else:
            st.info("👈 " + _t("no_text_warning"))

    with tab_manual:
        manual = st.session_state.pestel_manual
        cols = st.columns(2)
        for i, k in enumerate(PESTEL_KEYS):
            with cols[i % 2]:
                manual[k] = st.text_area(
                    _t(f"pestel_{k}"), value=manual[k], height=120,
                    placeholder=_t("pestel_placeholder"), key=f"pestel_ta_{k}",
                )

        if st.button("Générer / Generate", type="secondary"):
            rows = []
            for k in PESTEL_KEYS:
                for line in manual[k].splitlines():
                    if line.strip():
                        rows.append({"Facteur": _t(f"pestel_{k}"), "Élément": line.strip()})
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# PAGE: PORTER
# ─────────────────────────────────────────────
elif page == "porter":
    st.title(_t("porter_title"))
    st.markdown(_t("porter_intro"))

    PORTER_KEYS = ["nouveaux", "fournisseurs", "clients", "substituts", "rivalite"]
    PORTER_ICONS = ["🚪", "🏭", "🛒", "🔄", "⚔️"]

    tab_ai, tab_manual = st.tabs([_t("tab_ai"), _t("tab_manual")])

    def _render_porter(scores: dict, comments: dict, synthesis: str = ""):
        labels = [_t(f"porter_{k}") for k in PORTER_KEYS]
        vals = [scores.get(k, 3) for k in PORTER_KEYS]
        colors = ["#ef5350" if v >= 4 else "#ffa726" if v == 3 else "#66bb6a" for v in vals]

        fig = go.Figure(go.Bar(
            x=labels,
            y=vals,
            marker_color=colors,
            text=vals,
            textposition="outside",
        ))
        fig.update_layout(
            yaxis=dict(range=[0, 5.5], title=_t("porter_score_label")),
            xaxis=dict(tickangle=-15),
            height=400,
            margin=dict(t=20, b=60),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(_t("porter_comment_label") + "s")
        cols = st.columns(len(PORTER_KEYS))
        for i, k in enumerate(PORTER_KEYS):
            with cols[i]:
                score = scores.get(k, 3)
                bg = "#ffebee" if score >= 4 else "#fff8e1" if score == 3 else "#e8f5e9"
                cmt = comments.get(k, "—")
                st.markdown(
                    f"""<div style="background:{bg};border-radius:8px;padding:10px;min-height:120px;font-size:0.88rem">
                    <b>{PORTER_ICONS[i]} {_t(f'porter_{k}')}</b><br>
                    <span style="font-size:1.2rem;font-weight:bold">{score}/5</span><br>
                    {cmt}</div>""",
                    unsafe_allow_html=True,
                )

        if synthesis:
            st.divider()
            st.subheader(_t("porter_synthesis"))
            st.info(synthesis)

    with tab_ai:
        if st.button(_t("porter_ai_btn"), type="primary"):
            result = run_ai("porter")
            if result:
                st.session_state.res_porter = result
                for k in PORTER_KEYS:
                    if k in result:
                        st.session_state.porter_scores[k] = result[k].get("score", 3)
                        st.session_state.porter_comments[k] = result[k].get("comment", "")

        p = st.session_state.res_porter
        if p:
            scores = {k: p.get(k, {}).get("score", 3) for k in PORTER_KEYS}
            comments = {k: p.get(k, {}).get("comment", "") for k in PORTER_KEYS}
            _render_porter(scores, comments, p.get("synthesis", ""))
        else:
            st.info("👈 " + _t("no_text_warning"))

    with tab_manual:
        scores = st.session_state.porter_scores
        comments = st.session_state.porter_comments
        for k in PORTER_KEYS:
            c1, c2 = st.columns([1, 3])
            with c1:
                scores[k] = st.slider(_t(f"porter_{k}"), 1, 5, scores[k], key=f"porter_sl_{k}")
            with c2:
                comments[k] = st.text_input(
                    "", value=comments[k], key=f"porter_cmt_{k}",
                    placeholder=_t("porter_comment_label"),
                    label_visibility="collapsed",
                )

        if st.button(_t("porter_generate"), type="secondary"):
            _render_porter(scores, comments)


# ─────────────────────────────────────────────
# PAGE: BCG
# ─────────────────────────────────────────────
elif page == "bcg":
    st.title(_t("bcg_title"))
    st.markdown(_t("bcg_intro"))
    st.caption(_t("bcg_quadrant_info"))

    tab_ai, tab_manual = st.tabs([_t("tab_ai"), _t("tab_manual")])

    QUADRANT_COLORS = {
        "Star": "#66bb6a", "Stars": "#66bb6a",
        "Question mark": "#ffa726", "Question marks": "#ffa726", "Dilemme": "#ffa726",
        "Cash cow": "#42a5f5", "Vache à lait": "#42a5f5",
        "Dog": "#ef5350", "Poids mort": "#ef5350",
    }

    def _render_bcg(rows: list):
        if not rows:
            return
        df = pd.DataFrame(rows)
        if "activity" not in df.columns:
            return
        df["color"] = df.get("quadrant", pd.Series(["Star"] * len(df))).map(
            lambda q: QUADRANT_COLORS.get(q, "#90a4ae")
        )
        fig = px.scatter(
            df,
            x="share", y="growth",
            text="activity",
            color="quadrant" if "quadrant" in df.columns else None,
            color_discrete_map=QUADRANT_COLORS,
            labels={"share": _t("bcg_share"), "growth": _t("bcg_growth"), "quadrant": ""},
            size_max=40,
        )
        fig.add_vline(x=1.0, line_dash="dash", line_color="gray", annotation_text="PDM = 1")
        fig.add_hline(y=10.0, line_dash="dash", line_color="gray", annotation_text="Croissance 10%")
        fig.update_traces(textposition="top center", marker=dict(size=28, opacity=0.75))
        fig.update_layout(
            height=520,
            xaxis=dict(title=_t("bcg_share"), range=[0, max(df["share"].max() * 1.3, 2.2)]),
            yaxis=dict(title=_t("bcg_growth")),
            margin=dict(t=20),
        )

        # Quadrant labels
        x_max = df["share"].max() * 1.3 or 2.2
        y_max = df["growth"].max() * 1.2 or 30
        for label, x, y in [
            ("⭐ " + _t("bcg_stars"), x_max * 0.85, y_max * 0.9),
            ("❓ " + _t("bcg_questions"), 0.15, y_max * 0.9),
            ("🐄 " + _t("bcg_cows"), x_max * 0.85, -5),
            ("🐕 " + _t("bcg_dogs"), 0.15, -5),
        ]:
            fig.add_annotation(x=x, y=y, text=label, showarrow=False,
                               font=dict(size=12, color="gray"))

        st.plotly_chart(fig, use_container_width=True)

    with tab_ai:
        if st.button(_t("bcg_ai_btn"), type="primary"):
            result = run_ai("bcg")
            if isinstance(result, list) and result:
                st.session_state.res_bcg = result
                st.session_state.bcg_rows = [
                    {"activity": r.get("activity", ""), "share": r.get("share", 0.5), "growth": r.get("growth", 5.0)}
                    for r in result
                ]

        if st.session_state.res_bcg:
            _render_bcg(st.session_state.res_bcg)
            st.subheader("Détail / Details")
            df_show = pd.DataFrame(st.session_state.res_bcg)
            if not df_show.empty:
                st.dataframe(df_show, use_container_width=True, hide_index=True)
        else:
            st.info("👈 " + _t("no_text_warning"))

    with tab_manual:
        rows = st.session_state.bcg_rows
        for idx, row in enumerate(rows):
            c1, c2, c3 = st.columns(3)
            with c1:
                row["activity"] = st.text_input(_t("bcg_activity"), value=row["activity"], key=f"bcg_a_{idx}")
            with c2:
                row["share"] = st.number_input(_t("bcg_share"), 0.0, 3.0, value=float(row["share"]), step=0.05, key=f"bcg_s_{idx}")
            with c3:
                row["growth"] = st.number_input(_t("bcg_growth"), -50.0, 100.0, value=float(row["growth"]), step=1.0, key=f"bcg_g_{idx}")

        if st.button(_t("bcg_add"), type="secondary"):
            st.session_state.bcg_rows.append({"activity": "", "share": 0.5, "growth": 5.0})
            st.rerun()

        if st.button(_t("bcg_generate"), type="primary"):
            _render_bcg(rows)


# ─────────────────────────────────────────────
# PAGE: ANSOFF
# ─────────────────────────────────────────────
elif page == "ansoff":
    st.title(_t("ansoff_title"))
    st.markdown(_t("ansoff_intro"))

    ANSOFF_KEYS = ["penetration", "dev_produit", "dev_marche", "diversification"]
    ANSOFF_COLORS = {
        "penetration": "#c8e6c9",
        "dev_produit": "#b3e5fc",
        "dev_marche": "#fff9c4",
        "diversification": "#f8bbd0",
    }

    tab_ai, tab_manual = st.tabs([_t("tab_ai"), _t("tab_manual")])

    def _render_ansoff(data: dict):
        c1, c2 = st.columns(2)
        for idx, key in enumerate(ANSOFF_KEYS):
            col = c1 if idx % 2 == 0 else c2
            with col:
                items = data.get(key, [])
                if isinstance(items, list):
                    content = "".join(f"<li>{i}</li>" for i in items)
                else:
                    content = "".join(f"<li>{l}</li>" for l in str(items).splitlines() if l.strip())
                header = _t(f"ansoff_{key}").replace("\n", "<br>")
                st.markdown(
                    f"""<div style="background:{ANSOFF_COLORS[key]};border-radius:10px;padding:14px;margin-bottom:10px;min-height:160px;">
                    <b>{header}</b>
                    <ul style="margin-top:8px;padding-left:16px;font-size:0.9rem">{content}</ul></div>""",
                    unsafe_allow_html=True,
                )
        if data.get("synthesis"):
            st.divider()
            st.info(data["synthesis"])

    with tab_ai:
        if st.button(_t("ansoff_ai_btn"), type="primary"):
            result = run_ai("ansoff")
            if result:
                st.session_state.res_ansoff = result
                for k in ANSOFF_KEYS:
                    items = result.get(k, [])
                    st.session_state.ansoff_manual[k] = "\n".join(items) if isinstance(items, list) else str(items)

        if st.session_state.res_ansoff:
            _render_ansoff(st.session_state.res_ansoff)
        else:
            st.info("👈 " + _t("no_text_warning"))

    with tab_manual:
        manual = st.session_state.ansoff_manual
        c1, c2 = st.columns(2)
        for idx, key in enumerate(ANSOFF_KEYS):
            col = c1 if idx % 2 == 0 else c2
            with col:
                manual[key] = st.text_area(
                    _t(f"ansoff_{key}").split("\n")[0],
                    value=manual[key],
                    height=150,
                    placeholder=_t("ansoff_placeholder"),
                    key=f"ansoff_ta_{key}",
                )

        if st.button(_t("ansoff_generate"), type="secondary"):
            manual_data = {
                k: [l for l in manual[k].splitlines() if l.strip()]
                for k in ANSOFF_KEYS
            }
            _render_ansoff(manual_data)


# ─────────────────────────────────────────────
# PAGE: RAPPORT
# ─────────────────────────────────────────────
elif page == "rapport":
    st.title(_t("rapport_title"))
    st.markdown(_t("rapport_intro"))

    c1, c2, c3 = st.columns(3)
    with c1:
        org_name = st.text_input(_t("rapport_org_name"), value=st.session_state.rapport_org)
        st.session_state.rapport_org = org_name
    with c2:
        diag_date = st.date_input(_t("rapport_date"), value=date.today())
    with c3:
        analyst = st.text_input(_t("rapport_analyst"), value=st.session_state.rapport_analyst)
        st.session_state.rapport_analyst = analyst

    if not _has_results():
        st.warning(_t("rapport_no_data"))
    else:
        if st.button(_t("rapport_generate"), type="primary", use_container_width=True):
            st.session_state["show_report"] = True

        if st.session_state.get("show_report"):
            st.divider()

            # Header
            st.markdown(f"# {org_name or '—'}")
            st.markdown(f"**{_t('rapport_date')} :** {diag_date} &nbsp;|&nbsp; **{_t('rapport_analyst')} :** {analyst or '—'}")
            st.markdown(f"**{_t('org_type')} :** {_t('org_opa') if st.session_state.org_type == 'opa' else _t('org_efa')}")
            st.divider()

            # Étoile
            if st.session_state.res_etoile:
                st.subheader(f"⭐ {_t('rapport_section_etoile')}")
                r = st.session_state.res_etoile
                BRANCHES = ["milieu", "perf", "moyens", "politiques", "marches", "finances"]
                scores_df = pd.DataFrame([
                    {"Dimension": _t(f"etoile_{b}"), "Score": r.get(b, {}).get("score", "—"), "Observations": r.get(b, {}).get("obs", "")}
                    for b in BRANCHES
                ])
                st.dataframe(scores_df, use_container_width=True, hide_index=True)
                if r.get("synthesis"):
                    st.info(r["synthesis"])
                st.divider()

            # SWOT
            if st.session_state.res_swot:
                st.subheader(f"🔲 {_t('rapport_section_swot')}")
                r = st.session_state.res_swot
                SWOT_KEYS = ["forces", "faiblesses", "opportunites", "menaces"]
                for key in SWOT_KEYS:
                    items = r.get(key, [])
                    if items:
                        st.markdown(f"**{_t(f'swot_{key}')}**")
                        for item in (items if isinstance(items, list) else [items]):
                            st.markdown(f"- {item}")
                if r.get("synthesis"):
                    st.info(r["synthesis"])
                st.divider()

            # PESTEL
            if st.session_state.res_pestel:
                st.subheader(f"🌐 {_t('rapport_section_pestel')}")
                p = st.session_state.res_pestel
                PESTEL_KEYS = ["politique", "economique", "social", "techno", "environnement", "legal"]
                rows = []
                for k in PESTEL_KEYS:
                    for item in (p.get(k, []) if isinstance(p.get(k), list) else []):
                        rows.append({"Facteur": _t(f"pestel_{k}"), "Élément": item})
                if rows:
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
                st.divider()

            # Porter
            if st.session_state.res_porter:
                st.subheader(f"⚔️ {_t('rapport_section_porter')}")
                p = st.session_state.res_porter
                PORTER_KEYS = ["nouveaux", "fournisseurs", "clients", "substituts", "rivalite"]
                rows = [
                    {"Force": _t(f"porter_{k}"), "Score": p.get(k, {}).get("score", "—"), "Commentaire": p.get(k, {}).get("comment", "")}
                    for k in PORTER_KEYS
                ]
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
                if p.get("synthesis"):
                    st.info(p["synthesis"])
                st.divider()

            # BCG
            if st.session_state.res_bcg:
                st.subheader(f"📦 {_t('rapport_section_bcg')}")
                st.dataframe(pd.DataFrame(st.session_state.res_bcg), use_container_width=True, hide_index=True)
                st.divider()

            # Ansoff
            if st.session_state.res_ansoff:
                st.subheader(f"🚀 {_t('rapport_section_ansoff')}")
                a = st.session_state.res_ansoff
                ANSOFF_KEYS = ["penetration", "dev_produit", "dev_marche", "diversification"]
                for key in ANSOFF_KEYS:
                    items = a.get(key, [])
                    if items:
                        st.markdown(f"**{_t(f'ansoff_{key}').split(chr(10))[0]}**")
                        for item in (items if isinstance(items, list) else [items]):
                            st.markdown(f"- {item}")
                if a.get("synthesis"):
                    st.info(a["synthesis"])

            # Export
            st.divider()
            _export = _build_markdown_report(
                org_name, str(diag_date), analyst,
                st.session_state.org_type, st.session_state.lang,
            )
            st.download_button(
                _t("rapport_export_md"),
                data=_export,
                file_name=f"rapport_strategique_{org_name or 'opa'}.md",
                mime="text/markdown",
                type="secondary",
            )


def _build_markdown_report(org, diag_date, analyst, org_type, lang) -> str:
    lines = [
        f"# Rapport d'Analyse Stratégique — {org}",
        f"",
        f"**Date :** {diag_date}  |  **Analyste :** {analyst}  |  **Type :** {org_type.upper()}",
        "",
        "---",
        "",
    ]
    BRANCHES = ["milieu", "perf", "moyens", "politiques", "marches", "finances"]
    SWOT_KEYS = ["forces", "faiblesses", "opportunites", "menaces"]
    PESTEL_KEYS = ["politique", "economique", "social", "techno", "environnement", "legal"]
    PORTER_KEYS = ["nouveaux", "fournisseurs", "clients", "substituts", "rivalite"]
    ANSOFF_KEYS = ["penetration", "dev_produit", "dev_marche", "diversification"]

    r = st.session_state.res_etoile
    if r:
        lines += ["## ⭐ Étoile du Conseil", ""]
        for b in BRANCHES:
            d = r.get(b, {})
            lines.append(f"- **{t(f'etoile_{b}', lang)}** : {d.get('score','—')}/5 — {d.get('obs','')}")
        if r.get("synthesis"):
            lines += ["", f"> {r['synthesis']}"]
        lines.append("")

    r = st.session_state.res_swot
    if r:
        lines += ["## 🔲 SWOT", ""]
        for k in SWOT_KEYS:
            items = r.get(k, [])
            if items:
                lines.append(f"### {t(f'swot_{k}', lang)}")
                for item in (items if isinstance(items, list) else [items]):
                    lines.append(f"- {item}")
                lines.append("")
        if r.get("synthesis"):
            lines += [f"> {r['synthesis']}", ""]

    r = st.session_state.res_pestel
    if r:
        lines += ["## 🌐 PESTEL", ""]
        for k in PESTEL_KEYS:
            items = r.get(k, [])
            if items:
                lines.append(f"### {t(f'pestel_{k}', lang)}")
                for item in (items if isinstance(items, list) else [items]):
                    lines.append(f"- {item}")
                lines.append("")

    r = st.session_state.res_porter
    if r:
        lines += ["## ⚔️ Porter", ""]
        for k in PORTER_KEYS:
            d = r.get(k, {})
            lines.append(f"- **{t(f'porter_{k}', lang)}** : {d.get('score','—')}/5 — {d.get('comment','')}")
        if r.get("synthesis"):
            lines += ["", f"> {r['synthesis']}"]
        lines.append("")

    r = st.session_state.res_bcg
    if r:
        lines += ["## 📦 BCG", ""]
        for item in r:
            lines.append(f"- **{item.get('activity','')}** : PDM {item.get('share','')} | Croissance {item.get('growth','')}% | {item.get('quadrant','')}")
        lines.append("")

    r = st.session_state.res_ansoff
    if r:
        lines += ["## 🚀 Ansoff", ""]
        for k in ANSOFF_KEYS:
            items = r.get(k, [])
            if items:
                lines.append(f"### {t(f'ansoff_{k}', lang).split(chr(10))[0]}")
                for item in (items if isinstance(items, list) else [items]):
                    lines.append(f"- {item}")
                lines.append("")
        if r.get("synthesis"):
            lines += [f"> {r['synthesis']}", ""]

    lines += ["---", "", "*Généré par Agent IA Stratégique OPA/EFA*"]
    return "\n".join(lines)
