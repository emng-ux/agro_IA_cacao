"""
Agent IA Agropastoral - Filière Cacao
Cocoa Agro-Pastoral AI Agent

Prototype fonctionnel et interactif (bilingue FR/EN), conçu pour fonctionner
en ligne ou en mode Edge Computing (hors connexion Internet).

Run: streamlit run app.py
"""

import streamlit as st

from modules.i18n import t
from modules import reference_data as ref
from modules import storage
from modules.financial_engine import FarmFinancials

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# ----------------------------------------------------------------------
# CONFIG & SESSION STATE
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Agro IA Cacao",
    page_icon="🍫",
    layout="wide",
)

if "lang" not in st.session_state:
    st.session_state.lang = "fr"
if "offline" not in st.session_state:
    st.session_state.offline = True
if "efa_data" not in st.session_state:
    st.session_state.efa_data = {}
if "plan_validated" not in st.session_state:
    st.session_state.plan_validated = False
if "generated_plan" not in st.session_state:
    st.session_state.generated_plan = None


def _t(key):
    return t(key, st.session_state.lang)


# ----------------------------------------------------------------------
# SIDEBAR : LANGUAGE, MODE, NAVIGATION
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🍫 Agro IA Cacao")

    lang_choice = st.radio(
        _t("language"),
        options=["fr", "en"],
        format_func=lambda x: "Français" if x == "fr" else "English",
        index=0 if st.session_state.lang == "fr" else 1,
        horizontal=True,
    )
    st.session_state.lang = lang_choice

    mode = st.toggle(
        f"{_t('offline_mode')} / {_t('online_mode')}",
        value=st.session_state.offline,
        help=_t("data_local_note"),
    )
    st.session_state.offline = mode
    mode_label = _t("offline_mode") if st.session_state.offline else _t("online_mode")
    st.caption(f"📡 {mode_label}")

    st.divider()

    page = st.radio(
        "Navigation",
        options=[
            "home",
            "collecte",
            "financier",
            "strategique",
            "references",
            "plan",
            "about",
        ],
        format_func=lambda x: {
            "home": _t("nav_home"),
            "collecte": _t("nav_collecte"),
            "financier": _t("nav_financier"),
            "strategique": _t("nav_strategique"),
            "references": _t("nav_references"),
            "plan": _t("nav_plan"),
            "about": _t("nav_about"),
        }[x],
    )

    st.divider()
    st.caption(_t("footer_note"))


# ----------------------------------------------------------------------
# PAGE: HOME
# ----------------------------------------------------------------------
if page == "home":
    st.title(_t("welcome_title"))
    st.markdown(_t("tagline"))
    st.info(_t("welcome_text"))

    st.subheader(_t("quickstart"))
    st.markdown(f"- {_t('step1')}")
    st.markdown(f"- {_t('step2')}")
    st.markdown(f"- {_t('step3')}")
    st.markdown(f"- {_t('step4')}")

    st.divider()
    st.subheader(_t("saved_efas"))
    codes = storage.list_efa_codes()
    if codes:
        st.write(", ".join(codes))
    else:
        st.warning(_t("no_efa"))


# ----------------------------------------------------------------------
# PAGE: COLLECTE DE DONNEES (EFA)
# ----------------------------------------------------------------------
elif page == "collecte":
    st.title(_t("collecte_title"))

    # Load existing EFA
    codes = storage.list_efa_codes()
    if codes:
        with st.expander(f"📂 {_t('load_efa')}"):
            sel = st.selectbox(_t("select_efa"), options=["—"] + codes)
            if sel != "—":
                loaded = storage.load_efa(sel)
                if loaded:
                    st.session_state.efa_data = loaded
                    st.success(f"{sel} ✓")

    data = st.session_state.efa_data

    with st.form("efa_form"):
        st.subheader(_t("section_identification"))
        c1, c2, c3 = st.columns(3)
        with c1:
            country = st.selectbox(_t("country"), options=ref.COUNTRIES,
                                    index=ref.COUNTRIES.index(data.get("country", ref.COUNTRIES[0]))
                                    if data.get("country") in ref.COUNTRIES else 0)
            region = st.text_input(_t("region"), value=data.get("region", ""))
            department = st.text_input(_t("department"), value=data.get("department", ""))
        with c2:
            arrondissement = st.text_input(_t("arrondissement"), value=data.get("arrondissement", ""))
            locality = st.text_input(_t("locality"), value=data.get("locality", ""))
            code_region = st.text_input(_t("code_region"), value=data.get("code_region", ""))
        with c3:
            code_department = st.text_input(_t("code_department"), value=data.get("code_department", ""))
            code_arrondissement = st.text_input(_t("code_arrondissement"), value=data.get("code_arrondissement", ""))
            production_system = st.selectbox(
                _t("production_system"), options=ref.PRODUCTION_SYSTEMS,
                index=ref.PRODUCTION_SYSTEMS.index(data.get("production_system", ref.PRODUCTION_SYSTEMS[0]))
                if data.get("production_system") in ref.PRODUCTION_SYSTEMS else 0,
            )

        c4, c5, c6 = st.columns(3)
        with c4:
            activity = st.text_input(_t("activity"), value=data.get("activity", "Cacao"))
            code_system = st.text_input(_t("code_system"), value=data.get("code_system", ""))
        with c5:
            code_activity = st.text_input(_t("code_activity"), value=data.get("code_activity", ""))
            code_efa = st.text_input(_t("code_efa") + " *", value=data.get("code_efa", ""))
        with c6:
            code_op = st.text_input(_t("code_op"), value=data.get("code_op", ""))
            op_member = st.radio(_t("op_member"), options=[_t("yes"), _t("no")], horizontal=True,
                                  index=0 if data.get("op_member", True) else 1)

        st.subheader(_t("section_efa"))
        c7, c8, c9 = st.columns(3)
        with c7:
            surface_ha = st.number_input(_t("surface_ha"), min_value=0.0, value=float(data.get("surface_ha", 0.0)))
            surface_owned = st.number_input(_t("surface_owned"), min_value=0.0, value=float(data.get("surface_owned", 0.0)))
        with c8:
            surface_used = st.number_input(_t("surface_used"), min_value=0.0, value=float(data.get("surface_used", 0.0)))
            uth_exploitant = st.number_input(_t("uth_exploitant"), min_value=0.0, value=float(data.get("uth_exploitant", 1.0)))
        with c9:
            uth_salarie = st.number_input(_t("uth_salarie"), min_value=0.0, value=float(data.get("uth_salarie", 0.0)))

        st.subheader(_t("section_cacao"))
        c10, c11, c12 = st.columns(3)
        with c10:
            cacao_typology = st.selectbox(
                _t("cacao_typology"), options=ref.COCOA_PLOT_TYPES,
                index=ref.COCOA_PLOT_TYPES.index(data.get("cacao_typology", ref.COCOA_PLOT_TYPES[0]))
                if data.get("cacao_typology") in ref.COCOA_PLOT_TYPES else 0,
            )
            cacao_surface_ha = st.number_input(_t("cacao_surface"), min_value=0.0, value=float(data.get("cacao_surface_ha", 0.0)))
        with c11:
            cacao_qty_kg = st.number_input(_t("qty_total"), min_value=0.0, value=float(data.get("cacao_qty_kg", 0.0)))
            cacao_qty_sold_op = st.number_input(_t("qty_sold_op"), min_value=0.0, value=float(data.get("cacao_qty_sold_op", 0.0)))
        with c12:
            cacao_qty_sold_third = st.number_input(_t("qty_sold_third"), min_value=0.0, value=float(data.get("cacao_qty_sold_third", 0.0)))
            cacao_price_op = st.number_input(_t("price_op"), min_value=0.0, value=float(data.get("cacao_price_op", 1200.0)))

        cacao_price_third = st.number_input(_t("price_third"), min_value=0.0, value=float(data.get("cacao_price_third", 1200.0)))

        submitted = st.form_submit_button(f"💾 {_t('save_efa')}")

    if submitted:
        if not code_efa:
            st.error(_t("code_efa") + " - " + ("requis / required"))
        else:
            yield_ha = (cacao_qty_kg / cacao_surface_ha) if cacao_surface_ha > 0 else 0.0
            new_data = {
                "country": country, "region": region, "department": department,
                "arrondissement": arrondissement, "locality": locality,
                "code_region": code_region, "code_department": code_department,
                "code_arrondissement": code_arrondissement,
                "production_system": production_system, "activity": activity,
                "code_system": code_system, "code_activity": code_activity,
                "code_efa": code_efa, "code_op": code_op,
                "op_member": (op_member == _t("yes")),
                "surface_ha": surface_ha, "surface_owned": surface_owned,
                "surface_used": surface_used,
                "uth_exploitant": uth_exploitant, "uth_salarie": uth_salarie,
                "cacao_typology": cacao_typology, "cacao_surface_ha": cacao_surface_ha,
                "cacao_qty_kg": cacao_qty_kg, "cacao_qty_sold_op": cacao_qty_sold_op,
                "cacao_qty_sold_third": cacao_qty_sold_third,
                "cacao_price_op": cacao_price_op, "cacao_price_third": cacao_price_third,
                "yield_ha": yield_ha,
                # preserve financial inputs if already present
                **{k: v for k, v in data.items() if k.startswith("fin_")},
            }
            st.session_state.efa_data = new_data
            storage.save_efa(code_efa, new_data)
            st.success(_t("efa_saved"))


# ----------------------------------------------------------------------
# PAGE: DIAGNOSTIC FINANCIER
# ----------------------------------------------------------------------
elif page == "financier":
    st.title(_t("financier_title"))

    data = st.session_state.efa_data
    if not data or not data.get("code_efa"):
        st.warning(_t("no_data_warning"))
    else:
        st.caption(f"EFA: **{data.get('code_efa')}** — {data.get('locality', '')}")

        fin = data.get("fin_inputs", {})

        with st.form("financial_form"):
            st.subheader(_t("produit_brut_section"))
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                pb_vegetal = st.number_input(_t("pb_vegetal"), value=float(fin.get("pb_vegetal", 0.0)), step=1000.0)
                pb_animal = st.number_input(_t("pb_animal"), value=float(fin.get("pb_animal", 0.0)), step=1000.0)
            with c2:
                pb_acs = st.number_input(_t("pb_acs"), value=float(fin.get("pb_acs", 0.0)), step=1000.0)
                pb_immo = st.number_input(_t("pb_immo"), value=float(fin.get("pb_immo", 0.0)), step=1000.0)
            with c3:
                subventions = st.number_input(_t("subventions"), value=float(fin.get("subventions", 0.0)), step=1000.0)
                indemnites = st.number_input(_t("indemnites"), value=float(fin.get("indemnites", 0.0)), step=1000.0)
            with c4:
                autres_produits = st.number_input(_t("autres_produits"), value=float(fin.get("autres_produits", 0.0)), step=1000.0)

            st.subheader(_t("charges_op_section"))
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                engrais = st.number_input(_t("engrais"), value=float(fin.get("engrais", 0.0)), step=1000.0)
                semences = st.number_input(_t("semences"), value=float(fin.get("semences", 0.0)), step=1000.0)
                phyto = st.number_input(_t("phyto"), value=float(fin.get("phyto", 0.0)), step=1000.0)
            with c2:
                aliments_betail = st.number_input(_t("aliments_betail"), value=float(fin.get("aliments_betail", 0.0)), step=1000.0)
                veto = st.number_input(_t("veto"), value=float(fin.get("veto", 0.0)), step=1000.0)
                energie = st.number_input(_t("energie"), value=float(fin.get("energie", 0.0)), step=1000.0)
            with c3:
                emballages = st.number_input(_t("emballages"), value=float(fin.get("emballages", 0.0)), step=1000.0)
                autres_matieres = st.number_input(_t("autres_matieres"), value=float(fin.get("autres_matieres", 0.0)), step=1000.0)
                travaux_tiers_veg = st.number_input(_t("travaux_tiers_veg"), value=float(fin.get("travaux_tiers_veg", 0.0)), step=1000.0)
            with c4:
                travaux_tiers_ani = st.number_input(_t("travaux_tiers_ani"), value=float(fin.get("travaux_tiers_ani", 0.0)), step=1000.0)
                location_animaux = st.number_input(_t("location_animaux"), value=float(fin.get("location_animaux", 0.0)), step=1000.0)
                cacao_operational_costs = st.number_input(
                    "↳ " + _t("charges_op_section") + " (cacao)",
                    value=float(fin.get("cacao_operational_costs", 0.0)), step=1000.0,
                    help="Part des charges opérationnelles imputable spécifiquement à l'activité cacao.",
                )

            st.subheader(_t("services_exterieurs"))
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                eau_gaz = st.number_input(_t("eau_gaz"), value=float(fin.get("eau_gaz", 0.0)), step=1000.0)
                petits_equip = st.number_input(_t("petits_equip"), value=float(fin.get("petits_equip", 0.0)), step=1000.0)
                autres_fournitures = st.number_input(_t("autres_fournitures"), value=float(fin.get("autres_fournitures", 0.0)), step=1000.0)
            with c2:
                credit_bail = st.number_input(_t("credit_bail"), value=float(fin.get("credit_bail", 0.0)), step=1000.0)
                locations = st.number_input(_t("locations"), value=float(fin.get("locations", 0.0)), step=1000.0)
                entretien = st.number_input(_t("entretien"), value=float(fin.get("entretien", 0.0)), step=1000.0)
            with c3:
                assurances = st.number_input(_t("assurances"), value=float(fin.get("assurances", 0.0)), step=1000.0)
                cotisations = st.number_input(_t("cotisations"), value=float(fin.get("cotisations", 0.0)), step=1000.0)
                transport = st.number_input(_t("transport"), value=float(fin.get("transport", 0.0)), step=1000.0)
            with c4:
                autres_services = st.number_input(_t("autres_services"), value=float(fin.get("autres_services", 0.0)), step=1000.0)
                impots = st.number_input(_t("impots"), value=float(fin.get("impots", 0.0)), step=1000.0)

            st.subheader(_t("charges_structure_section"))
            c1, c2, c3 = st.columns(3)
            with c1:
                remuneration = st.number_input(_t("remuneration"), value=float(fin.get("remuneration", 0.0)), step=1000.0)
                charges_sociales_pers = st.number_input(_t("charges_sociales_pers"), value=float(fin.get("charges_sociales_pers", 0.0)), step=1000.0)
            with c2:
                charges_sociales_exploit = st.number_input(_t("charges_sociales_exploit"), value=float(fin.get("charges_sociales_exploit", 0.0)), step=1000.0)
                amortissements = st.number_input(_t("amortissements"), value=float(fin.get("amortissements", 0.0)), step=1000.0)
            with c3:
                interets = st.number_input(_t("interets"), value=float(fin.get("interets", 0.0)), step=1000.0)
                autres_agios = st.number_input(_t("autres_agios"), value=float(fin.get("autres_agios", 0.0)), step=1000.0)

            st.subheader(_t("bilan_section"))
            c1, c2, c3 = st.columns(3)
            with c1:
                stocks = st.number_input(_t("stocks"), value=float(fin.get("stocks", 0.0)), step=1000.0)
                creances = st.number_input(_t("creances"), value=float(fin.get("creances", 0.0)), step=1000.0)
            with c2:
                tresorerie_actif = st.number_input(_t("tresorerie_actif"), value=float(fin.get("tresorerie_actif", 0.0)), step=1000.0)
                capitaux_propres = st.number_input(_t("capitaux_propres"), value=float(fin.get("capitaux_propres", 0.0)), step=1000.0)
            with c3:
                dettes_lmt = st.number_input(_t("dettes_lmt"), value=float(fin.get("dettes_lmt", 0.0)), step=1000.0)
                dettes_ct = st.number_input(_t("dettes_ct"), value=float(fin.get("dettes_ct", 0.0)), step=1000.0)
                actif_immobilise = st.number_input(_t("actif_immobilise"), value=float(fin.get("actif_immobilise", 0.0)), step=1000.0)

            calc_submitted = st.form_submit_button(f"📊 {_t('calc_button')}")

        if calc_submitted:
            fin_inputs = dict(
                pb_vegetal=pb_vegetal, pb_animal=pb_animal, pb_acs=pb_acs, pb_immo=pb_immo,
                subventions=subventions, indemnites=indemnites, autres_produits=autres_produits,
                engrais=engrais, semences=semences, phyto=phyto, aliments_betail=aliments_betail,
                veto=veto, energie=energie, emballages=emballages, autres_matieres=autres_matieres,
                travaux_tiers_veg=travaux_tiers_veg, travaux_tiers_ani=travaux_tiers_ani,
                location_animaux=location_animaux, cacao_operational_costs=cacao_operational_costs,
                eau_gaz=eau_gaz, petits_equip=petits_equip, autres_fournitures=autres_fournitures,
                credit_bail=credit_bail, locations=locations, entretien=entretien,
                assurances=assurances, cotisations=cotisations, transport=transport,
                autres_services=autres_services, impots=impots,
                remuneration=remuneration, charges_sociales_pers=charges_sociales_pers,
                charges_sociales_exploit=charges_sociales_exploit, amortissements=amortissements,
                interets=interets, autres_agios=autres_agios,
                stocks=stocks, creances=creances, tresorerie_actif=tresorerie_actif,
                capitaux_propres=capitaux_propres, dettes_lmt=dettes_lmt, dettes_ct=dettes_ct,
                actif_immobilise=actif_immobilise,
            )
            data["fin_inputs"] = fin_inputs
            st.session_state.efa_data = data
            storage.save_efa(data["code_efa"], data)

        fin = data.get("fin_inputs")
        if fin:
            ff = FarmFinancials(
                surface_ha=data.get("surface_ha", 0.0),
                cacao_surface_ha=data.get("cacao_surface_ha", 0.0),
                uth_exploitant=data.get("uth_exploitant", 0.0),
                uth_salarie=data.get("uth_salarie", 0.0),
                cacao_qty_kg=data.get("cacao_qty_kg", 0.0),
                cacao_price_op=data.get("cacao_price_op", 0.0),
                cacao_price_third=data.get("cacao_price_third", 0.0),
                cacao_qty_sold_op=data.get("cacao_qty_sold_op", 0.0),
                cacao_qty_sold_third=data.get("cacao_qty_sold_third", 0.0),
                **fin,
            )
            results = ff.as_results_dict()

            st.divider()
            st.subheader(_t("results_section"))

            r1, r2, r3 = st.columns(3)
            with r1:
                st.metric(_t("res_produit_brut_total"), f"{results['res_produit_brut_total']:,.0f} FCFA")
                st.metric(_t("res_charges_op_total"), f"{results['res_charges_op_total']:,.0f} FCFA")
                st.metric(_t("res_marge_brute"), f"{results['res_marge_brute']:,.0f} FCFA")
                st.metric(_t("res_valeur_ajoutee"), f"{results['res_valeur_ajoutee']:,.0f} FCFA")
                st.metric(_t("res_va_ha"), f"{results['res_va_ha']:,.0f} FCFA/ha")
                st.metric(_t("res_va_uth"), f"{results['res_va_uth']:,.0f} FCFA/UTH")
                st.metric(_t("res_charges_structure"), f"{results['res_charges_structure']:,.0f} FCFA")
            with r2:
                st.metric(_t("res_ebe"), f"{results['res_ebe']:,.0f} FCFA")
                st.metric(_t("res_ebe_ha"), f"{results['res_ebe_ha']:,.0f} FCFA/ha")
                st.metric(_t("res_ebe_uth"), f"{results['res_ebe_uth']:,.0f} FCFA/UTH")
                st.metric(_t("res_resultat_courant"), f"{results['res_resultat_courant']:,.0f} FCFA")
                st.metric(_t("res_resultat_ha"), f"{results['res_resultat_ha']:,.0f} FCFA/ha")
                st.metric(_t("res_resultat_uth"), f"{results['res_resultat_uth']:,.0f} FCFA/UTH")
                st.metric(_t("res_charges_financieres"), f"{results['res_charges_financieres']:,.0f} FCFA")
            with r3:
                st.metric(_t("res_cout_kg"), f"{results['res_cout_kg']:,.0f} FCFA/kg")
                st.metric(_t("res_prix_revient_kg"), f"{results['res_prix_revient_kg']:,.0f} FCFA/kg")
                st.metric(_t("res_seuil_rentabilite"), f"{results['res_seuil_rentabilite']:,.0f} FCFA/kg")
                st.metric(_t("res_services_ext_total"), f"{results['res_services_ext_total']:,.0f} FCFA")
                st.metric(_t("res_services_ext_ha"), f"{results['res_services_ext_ha']:,.0f} FCFA/ha")
                st.metric(_t("res_approvisionnements_total"), f"{results['res_approvisionnements_total']:,.0f} FCFA")
                st.metric(_t("res_approvisionnements_ha"), f"{results['res_approvisionnements_ha']:,.0f} FCFA/ha")

            st.divider()
            st.subheader(_t("bilan_section"))
            b1, b2 = st.columns(2)
            with b1:
                st.metric(_t("res_fdr"), f"{results['res_fdr']:,.0f} FCFA")
                st.metric(_t("res_bfr"), f"{results['res_bfr']:,.0f} FCFA")
                st.metric(_t("res_tresorerie"), f"{results['res_tresorerie']:,.0f} FCFA")
            with b2:
                st.metric(_t("res_actif_circulant"), f"{results['res_actif_circulant']:,.0f} FCFA")
                st.metric(_t("res_ratio_liquidite"), f"{results['res_ratio_liquidite']:.2f}")

            # ---------------------- Interpretation ----------------------
            st.divider()
            st.subheader(_t("interpretation_title"))

            prix_vente = ff.prix_vente_moyen_cacao
            seuil = results["res_seuil_rentabilite"]

            if results["res_resultat_courant"] > 0:
                st.success(_t("interpretation_good"))
            else:
                st.warning(_t("interpretation_warning"))

            if seuil > 0:
                if prix_vente < seuil:
                    st.error(_t("interpretation_below_threshold") +
                             f" ({prix_vente:,.0f} < {seuil:,.0f} FCFA/kg)")
                else:
                    st.success(_t("interpretation_above_threshold") +
                               f" ({prix_vente:,.0f} ≥ {seuil:,.0f} FCFA/kg)")

            if results["res_ratio_liquidite"] >= 1:
                st.success(_t("interpretation_liquidity_good"))
            else:
                st.warning(_t("interpretation_liquidity_bad"))

            # ---------------------- Chart: revenue vs cost waterfall ----
            chart_data = pd.DataFrame({
                "Indicateur": [
                    _t("res_produit_brut_total"), _t("res_charges_op_total"),
                    _t("res_marge_brute"), _t("res_valeur_ajoutee"),
                    _t("res_ebe"), _t("res_resultat_courant"),
                ],
                "Valeur (FCFA)": [
                    results["res_produit_brut_total"], -results["res_charges_op_total"],
                    results["res_marge_brute"], results["res_valeur_ajoutee"],
                    results["res_ebe"], results["res_resultat_courant"],
                ],
            })
            fig = px.bar(chart_data, x="Indicateur", y="Valeur (FCFA)",
                          color="Valeur (FCFA)", color_continuous_scale="RdYlGn")
            st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------
# PAGE: ANALYSE STRATEGIQUE
# ----------------------------------------------------------------------
elif page == "strategique":
    st.title(_t("strategique_title"))

    tool = st.selectbox(
        _t("tool_select"),
        options=["etoile_conseil", "swot", "pestel", "porter", "bcg", "ansoff"],
        format_func=lambda x: _t(x),
    )

    # ----- Étoile du conseil -----
    if tool == "etoile_conseil":
        st.info(_t("etoile_intro"))
        branches = ["etoile_moyens", "etoile_perf", "etoile_finances",
                    "etoile_milieu", "etoile_politiques", "etoile_marches"]
        cols = st.columns(3)
        values = {}
        for i, b in enumerate(branches):
            with cols[i % 3]:
                values[b] = st.slider(_t(b), 1, 5, 3)

        if st.button(_t("generate_radar")):
            labels = [_t(b) for b in branches]
            vals = [values[b] for b in branches]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=labels + [labels[0]],
                fill='toself',
                name=_t("etoile_conseil"),
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

    # ----- SWOT -----
    elif tool == "swot":
        st.info(_t("swot_intro"))
        c1, c2 = st.columns(2)
        with c1:
            forces = st.text_area(_t("swot_forces"), height=150)
            opportunites = st.text_area(_t("swot_opportunites"), height=150)
        with c2:
            faiblesses = st.text_area(_t("swot_faiblesses"), height=150)
            menaces = st.text_area(_t("swot_menaces"), height=150)

        if forces or faiblesses or opportunites or menaces:
            fig = go.Figure()
            quadrants = [
                (_t("swot_forces"), forces, "#2ecc71", 0, 1),
                (_t("swot_faiblesses"), faiblesses, "#e74c3c", 1, 1),
                (_t("swot_opportunites"), opportunites, "#3498db", 0, 0),
                (_t("swot_menaces"), menaces, "#f39c12", 1, 0),
            ]
            fig = go.Figure()
            for title, text, color, col, row in quadrants:
                x0, x1 = col, col + 1
                y0, y1 = row, row + 1
                fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                               line=dict(color="white"), fillcolor=color, opacity=0.25)
                content = "<br>".join(f"• {line}" for line in text.splitlines() if line.strip())
                fig.add_annotation(x=(x0+x1)/2, y=y1-0.05, text=f"<b>{title}</b>",
                                    showarrow=False, font=dict(size=14), yanchor="top")
                fig.add_annotation(x=(x0+x1)/2, y=(y0+y1)/2 - 0.1, text=content,
                                    showarrow=False, font=dict(size=11), align="center")
            fig.update_xaxes(visible=False, range=[0, 2])
            fig.update_yaxes(visible=False, range=[0, 2])
            fig.update_layout(height=500, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)

    # ----- PESTEL -----
    elif tool == "pestel":
        st.info(_t("pestel_intro"))
        factors = ["pestel_politique", "pestel_economique", "pestel_social",
                   "pestel_techno", "pestel_environnement", "pestel_legal"]
        cols = st.columns(2)
        pestel_values = {}
        for i, f in enumerate(factors):
            with cols[i % 2]:
                pestel_values[f] = st.text_area(_t(f), height=100, key=f"pestel_{f}")

        if any(pestel_values.values()):
            rows = []
            for f in factors:
                lines = [l for l in pestel_values[f].splitlines() if l.strip()]
                for l in lines:
                    rows.append({"Facteur": _t(f), "Élément": l})
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ----- Porter -----
    elif tool == "porter":
        st.info(_t("porter_intro"))
        forces_keys = ["porter_nouveaux", "porter_fournisseurs", "porter_clients",
                       "porter_substituts", "porter_rivalite"]
        vals = {}
        comments = {}
        for k in forces_keys:
            c1, c2 = st.columns([1, 3])
            with c1:
                vals[k] = st.slider(_t(k), 1, 5, 3, key=f"porter_slider_{k}")
            with c2:
                comments[k] = st.text_input("", key=f"porter_comment_{k}", placeholder=_t(k))

        fig = px.bar(
            x=[_t(k) for k in forces_keys],
            y=[vals[k] for k in forces_keys],
            labels={"x": "", "y": "Intensité (1-5)"},
            color=[vals[k] for k in forces_keys],
            color_continuous_scale="OrRd",
            range_y=[0, 5],
        )
        st.plotly_chart(fig, use_container_width=True)

    # ----- BCG -----
    elif tool == "bcg":
        st.info(_t("bcg_intro"))

        if "bcg_rows" not in st.session_state:
            st.session_state.bcg_rows = [
                {"activity": "Cacao", "share": 0.6, "growth": 5.0},
            ]

        for idx, row in enumerate(st.session_state.bcg_rows):
            c1, c2, c3 = st.columns(3)
            with c1:
                row["activity"] = st.text_input(_t("bcg_activity"), value=row["activity"], key=f"bcg_act_{idx}")
            with c2:
                row["share"] = st.number_input(_t("bcg_part_marche"), 0.0, 2.0, value=row["share"], step=0.05, key=f"bcg_share_{idx}")
            with c3:
                row["growth"] = st.number_input(_t("bcg_croissance"), -50.0, 100.0, value=row["growth"], step=1.0, key=f"bcg_growth_{idx}")

        if st.button(_t("bcg_add_row")):
            st.session_state.bcg_rows.append({"activity": "", "share": 0.5, "growth": 0.0})
            st.rerun()

        if st.button(_t("bcg_generate")):
            df = pd.DataFrame(st.session_state.bcg_rows)
            fig = px.scatter(
                df, x="share", y="growth", text="activity", size=[20]*len(df),
                labels={"share": _t("bcg_part_marche"), "growth": _t("bcg_croissance")},
            )
            fig.add_vline(x=1.0, line_dash="dash", line_color="gray")
            fig.add_hline(y=10.0, line_dash="dash", line_color="gray")
            fig.update_traces(textposition="top center")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Étoiles / Stars (haut-droite) · Vedettes / Question marks (haut-gauche) · "
                       "Vaches à lait / Cash cows (bas-droite) · Poids morts / Dogs (bas-gauche)")

    # ----- Ansoff -----
    elif tool == "ansoff":
        st.info(_t("ansoff_intro"))
        c1, c2 = st.columns(2)
        with c1:
            penetration = st.text_area(_t("ansoff_penetration"), height=120)
            developpement_marche = st.text_area(_t("ansoff_developpement_marche"), height=120)
        with c2:
            developpement_produit = st.text_area(_t("ansoff_developpement_produit"), height=120)
            diversification = st.text_area(_t("ansoff_diversification"), height=120)


# ----------------------------------------------------------------------
# PAGE: REFERENCES TECHNICO-ECONOMIQUES
# ----------------------------------------------------------------------
elif page == "references":
    st.title(_t("references_title"))
    st.markdown(_t("ref_intro"))

    filter_typ = st.selectbox(_t("ref_filter_system"), options=["Toutes / All"] + ref.COCOA_PLOT_TYPES)

    sheets = ref.REFERENCE_SHEETS
    if filter_typ != "Toutes / All":
        sheets = [s for s in sheets if s["typology"] == filter_typ]

    df = pd.DataFrame(sheets)
    notes_col = "notes_fr" if st.session_state.lang == "fr" else "notes_en"
    display_df = df[["typology", "yield_kg_ha", "price_fcfa_kg", "operational_costs_fcfa_ha", "labor_hj_ha", notes_col]].copy()
    display_df.columns = [
        "Typologie" if st.session_state.lang == "fr" else "Typology",
        "Rendement (kg/ha)" if st.session_state.lang == "fr" else "Yield (kg/ha)",
        "Prix (FCFA/kg)" if st.session_state.lang == "fr" else "Price (FCFA/kg)",
        "Charges op. (FCFA/ha)" if st.session_state.lang == "fr" else "Operational costs (FCFA/ha)",
        "Main d'œuvre (HJ/ha)" if st.session_state.lang == "fr" else "Labor (man-day/ha)",
        "Notes",
    ]
    st.subheader(_t("ref_table_title"))
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Margin chart
    df["marge_brute_ha"] = df["yield_kg_ha"] * df["price_fcfa_kg"] - df["operational_costs_fcfa_ha"]
    fig = px.bar(df, x="typology", y="marge_brute_ha",
                  labels={"typology": "", "marge_brute_ha": "Marge brute (FCFA/ha)" if st.session_state.lang == "fr" else "Gross margin (FCFA/ha)"},
                  color="marge_brute_ha", color_continuous_scale="RdYlGn")
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(_t("ref_itinerary_title"))
    months = ["Jan", "Fév", "Mars", "Avril", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"] \
        if st.session_state.lang == "fr" else \
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ops = ref.REFERENCE_ITINERARY["operations"] if st.session_state.lang == "fr" else ref.REFERENCE_ITINERARY["operations_en"]
    itinerary_df = pd.DataFrame(ref.REFERENCE_ITINERARY["monthly_hj"], columns=months, index=ops)
    itinerary_df["Total HJ/ha"] = itinerary_df.sum(axis=1)
    st.dataframe(itinerary_df, use_container_width=True)

    # Heatmap
    heat_df = pd.DataFrame(ref.REFERENCE_ITINERARY["monthly_hj"], columns=months, index=ops)
    fig2 = px.imshow(heat_df, labels=dict(color="HJ/ha"), aspect="auto", color_continuous_scale="YlOrBr")
    st.plotly_chart(fig2, use_container_width=True)


# ----------------------------------------------------------------------
# PAGE: PLAN STRATEGIQUE & OPERATIONNEL
# ----------------------------------------------------------------------
elif page == "plan":
    st.title(_t("plan_title"))
    st.markdown(_t("plan_intro"))

    data = st.session_state.efa_data
    if not data or not data.get("code_efa"):
        st.warning(_t("no_data_warning"))
    else:
        fin = data.get("fin_inputs")

        if st.button(f"🤖 {_t('plan_generate')}"):
            objectives = []
            actions = []

            if fin:
                ff = FarmFinancials(
                    surface_ha=data.get("surface_ha", 0.0),
                    cacao_surface_ha=data.get("cacao_surface_ha", 0.0),
                    uth_exploitant=data.get("uth_exploitant", 0.0),
                    uth_salarie=data.get("uth_salarie", 0.0),
                    cacao_qty_kg=data.get("cacao_qty_kg", 0.0),
                    cacao_price_op=data.get("cacao_price_op", 0.0),
                    cacao_price_third=data.get("cacao_price_third", 0.0),
                    cacao_qty_sold_op=data.get("cacao_qty_sold_op", 0.0),
                    cacao_qty_sold_third=data.get("cacao_qty_sold_third", 0.0),
                    **fin,
                )
                results = ff.as_results_dict()
                prix_vente = ff.prix_vente_moyen_cacao
                seuil = results["res_seuil_rentabilite"]

                if st.session_state.lang == "fr":
                    if seuil > 0 and prix_vente < seuil:
                        objectives.append("Réduire le coût de production du kg de cacao pour repasser sous le seuil de rentabilité.")
                        actions.append("Optimiser l'usage des intrants (engrais, phytosanitaires) selon les références technico-économiques.")
                        actions.append("Améliorer le rendement par hectare via la taille d'entretien et la fertilisation raisonnée.")
                    else:
                        objectives.append("Consolider la rentabilité actuelle de la parcelle de cacao.")
                        actions.append("Maintenir l'itinéraire technique de référence et surveiller l'évolution des charges.")

                    if results["res_ratio_liquidite"] < 1:
                        objectives.append("Améliorer la trésorerie et réduire le besoin en fonds de roulement (BFR).")
                        actions.append("Étaler les charges opérationnelles et explorer des solutions de financement court terme via l'OP.")
                    if data.get("yield_ha", 0) < 600:
                        objectives.append("Augmenter le rendement cacao par hectare vers les références régionales.")
                        actions.append("Mettre en place un calendrier de fertilisation et de protection phytosanitaire adapté à la typologie de la parcelle.")
                    objectives.append("Diversifier les sources de revenu de l'EFA (activités associées, ACS).")
                    actions.append("Évaluer les opportunités de cultures associées ou d'activités ACS (transformation, prestation de service).")
                else:
                    if seuil > 0 and prix_vente < seuil:
                        objectives.append("Reduce the production cost per kg of cocoa to return below the profitability threshold.")
                        actions.append("Optimize input use (fertilizers, crop protection) based on technical-economic references.")
                        actions.append("Improve yield per hectare via maintenance pruning and tailored fertilization.")
                    else:
                        objectives.append("Consolidate the current profitability of the cocoa plot.")
                        actions.append("Maintain the reference technical itinerary and monitor cost trends.")

                    if results["res_ratio_liquidite"] < 1:
                        objectives.append("Improve cash position and reduce the working capital requirement (BFR).")
                        actions.append("Spread operational costs over time and explore short-term financing through the producer organization.")
                    if data.get("yield_ha", 0) < 600:
                        objectives.append("Increase cocoa yield per hectare towards regional references.")
                        actions.append("Establish a fertilization and crop protection calendar suited to the plot typology.")
                    objectives.append("Diversify the farm's income sources (associated crops, trade/service activities).")
                    actions.append("Assess opportunities for intercropping or trade/service activities (processing, service provision).")
            else:
                if st.session_state.lang == "fr":
                    objectives.append("Compléter le diagnostic financier pour affiner le plan stratégique.")
                    actions.append("Renseigner les données financières dans 'Diagnostic financier'.")
                else:
                    objectives.append("Complete the financial diagnosis to refine the strategic plan.")
                    actions.append("Enter financial data in 'Financial Diagnosis'.")

            st.session_state.generated_plan = {"objectives": objectives, "actions": actions}
            st.session_state.plan_validated = False

        plan = st.session_state.generated_plan
        if plan:
            st.subheader(_t("plan_objectifs"))
            for o in plan["objectives"]:
                st.markdown(f"- {o}")

            st.subheader(_t("plan_actions"))
            for a in plan["actions"]:
                st.markdown(f"- {a}")

            st.divider()
            validate = st.checkbox(_t("plan_validate"), value=st.session_state.plan_validated)
            st.session_state.plan_validated = validate

            if validate:
                st.success(_t("plan_validated"))
            else:
                st.info(_t("plan_not_validated"))

            export_text = "## " + _t("plan_objectifs") + "\n" + "\n".join(f"- {o}" for o in plan["objectives"])
            export_text += "\n\n## " + _t("plan_actions") + "\n" + "\n".join(f"- {a}" for a in plan["actions"])
            export_text += f"\n\nStatus: {'VALIDATED' if validate else 'DRAFT - NOT VALIDATED'}"
            st.download_button(_t("plan_export"), data=export_text,
                                file_name=f"plan_{data.get('code_efa')}.md", mime="text/markdown")


# ----------------------------------------------------------------------
# PAGE: ABOUT
# ----------------------------------------------------------------------
elif page == "about":
    st.title(_t("about_title"))
    st.markdown(_t("about_text"))
    st.warning(_t("about_disclaimer"))
    st.caption(_t("data_local_note"))
