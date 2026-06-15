"""
Module de calculs financiers pour le diagnostic des exploitations cacaoyères.
Financial calculation module for cocoa farm diagnosis.

Toutes les formules suivent les définitions du référentiel filière cacao :
- Produit brut, charges opérationnelles, marge brute
- Valeur ajoutée (VA), EBE, résultat courant
- FDR, BFR, trésorerie, ratio de liquidité
- Coût de production / prix de revient du kg de cacao et seuil de rentabilité
"""

from dataclasses import dataclass, field


@dataclass
class FarmFinancials:
    # --- Surfaces & main d'oeuvre ---
    surface_ha: float = 0.0
    cacao_surface_ha: float = 0.0
    uth_exploitant: float = 0.0
    uth_salarie: float = 0.0

    # --- Produits bruts (FCFA) ---
    pb_vegetal: float = 0.0
    pb_animal: float = 0.0
    pb_acs: float = 0.0
    pb_immo: float = 0.0
    subventions: float = 0.0
    indemnites: float = 0.0
    autres_produits: float = 0.0

    # --- Charges opérationnelles (FCFA) ---
    engrais: float = 0.0
    semences: float = 0.0
    phyto: float = 0.0
    aliments_betail: float = 0.0
    veto: float = 0.0
    energie: float = 0.0
    emballages: float = 0.0
    autres_matieres: float = 0.0
    travaux_tiers_veg: float = 0.0
    travaux_tiers_ani: float = 0.0
    location_animaux: float = 0.0

    # --- Services extérieurs (FCFA) ---
    eau_gaz: float = 0.0
    petits_equip: float = 0.0
    autres_fournitures: float = 0.0
    credit_bail: float = 0.0
    locations: float = 0.0
    entretien: float = 0.0
    assurances: float = 0.0
    cotisations: float = 0.0
    transport: float = 0.0
    autres_services: float = 0.0
    impots: float = 0.0

    # --- Charges de structure / personnel / financier (FCFA) ---
    remuneration: float = 0.0
    charges_sociales_pers: float = 0.0
    charges_sociales_exploit: float = 0.0
    amortissements: float = 0.0
    interets: float = 0.0
    autres_agios: float = 0.0

    # --- Bilan (FCFA) ---
    stocks: float = 0.0
    creances: float = 0.0
    tresorerie_actif: float = 0.0
    capitaux_propres: float = 0.0
    dettes_lmt: float = 0.0
    dettes_ct: float = 0.0
    actif_immobilise: float = 0.0

    # --- Données cacao spécifiques ---
    cacao_qty_kg: float = 0.0
    cacao_price_op: float = 0.0
    cacao_price_third: float = 0.0
    cacao_qty_sold_op: float = 0.0
    cacao_qty_sold_third: float = 0.0
    cacao_operational_costs: float = 0.0  # somme des charges opérationnelles imputables au cacao

    # ---------------------------------------------------------------
    # PRODUIT BRUT
    # ---------------------------------------------------------------
    @property
    def produit_brut_total(self) -> float:
        return (
            self.pb_vegetal
            + self.pb_animal
            + self.pb_acs
            + self.pb_immo
            + self.subventions
            + self.indemnites
            + self.autres_produits
        )

    # ---------------------------------------------------------------
    # CHARGES OPERATIONNELLES (au sens strict : intrants directement
    # proportionnels à la production, y compris travaux par tiers et
    # location/achat d'animaux)
    # ---------------------------------------------------------------
    @property
    def charges_operationnelles_total(self) -> float:
        return (
            self.engrais
            + self.semences
            + self.phyto
            + self.aliments_betail
            + self.veto
            + self.energie
            + self.emballages
            + self.autres_matieres
            + self.travaux_tiers_veg
            + self.travaux_tiers_ani
            + self.location_animaux
        )

    # ---------------------------------------------------------------
    # MARGE BRUTE GLOBALE (avant main d'oeuvre)
    # Marge brute = produit brut - charges opérationnelles
    # ---------------------------------------------------------------
    @property
    def marge_brute_globale(self) -> float:
        return self.produit_brut_total - self.charges_operationnelles_total

    # ---------------------------------------------------------------
    # SERVICES EXTERIEURS
    # ---------------------------------------------------------------
    @property
    def services_exterieurs_total(self) -> float:
        return (
            self.credit_bail
            + self.locations
            + self.entretien
            + self.assurances
            + self.cotisations
            + self.transport
            + self.autres_services
            + self.impots
            + self.eau_gaz
        )

    @property
    def services_exterieurs_par_ha(self) -> float:
        return self._safe_div(self.services_exterieurs_total, self.surface_ha)

    # ---------------------------------------------------------------
    # APPROVISIONNEMENTS (petits équipements et fournitures hors charges
    # opérationnelles directes)
    # ---------------------------------------------------------------
    @property
    def approvisionnements_total(self) -> float:
        return self.petits_equip + self.autres_fournitures

    @property
    def approvisionnements_par_ha(self) -> float:
        return self._safe_div(self.approvisionnements_total, self.surface_ha)

    # ---------------------------------------------------------------
    # CHARGES DE STRUCTURE (hors charges opérationnelles)
    # = services extérieurs + approvisionnements + personnel +
    #   amortissements + charges financières
    # ---------------------------------------------------------------
    @property
    def charges_personnel_total(self) -> float:
        return self.remuneration + self.charges_sociales_pers + self.charges_sociales_exploit

    @property
    def charges_financieres_total(self) -> float:
        return self.interets + self.autres_agios

    @property
    def charges_structure_total(self) -> float:
        return (
            self.services_exterieurs_total
            + self.approvisionnements_total
            + self.charges_personnel_total
            + self.amortissements
            + self.charges_financieres_total
        )

    # ---------------------------------------------------------------
    # VALEUR AJOUTEE (VA)
    # VA = Produit brut - charges opérationnelles - services extérieurs
    #      - approvisionnements
    # ---------------------------------------------------------------
    @property
    def valeur_ajoutee(self) -> float:
        return (
            self.produit_brut_total
            - self.charges_operationnelles_total
            - self.services_exterieurs_total
            - self.approvisionnements_total
        )

    @property
    def valeur_ajoutee_par_ha(self) -> float:
        return self._safe_div(self.valeur_ajoutee, self.surface_ha)

    @property
    def valeur_ajoutee_par_uth(self) -> float:
        return self._safe_div(self.valeur_ajoutee, self.uth_exploitant)

    # ---------------------------------------------------------------
    # EBE (Excédent Brut d'Exploitation)
    # EBE = VA - charges de personnel (main d'oeuvre salariée + charges sociales)
    # ---------------------------------------------------------------
    @property
    def ebe(self) -> float:
        return self.valeur_ajoutee - self.charges_personnel_total

    @property
    def ebe_par_ha(self) -> float:
        return self._safe_div(self.ebe, self.surface_ha)

    @property
    def ebe_par_uth(self) -> float:
        return self._safe_div(self.ebe, self.uth_exploitant)

    # ---------------------------------------------------------------
    # RESULTAT COURANT
    # Résultat courant = EBE - amortissements - charges financières
    # ---------------------------------------------------------------
    @property
    def resultat_courant(self) -> float:
        return self.ebe - self.amortissements - self.charges_financieres_total

    @property
    def resultat_courant_par_ha(self) -> float:
        return self._safe_div(self.resultat_courant, self.surface_ha)

    @property
    def resultat_courant_par_uth(self) -> float:
        return self._safe_div(self.resultat_courant, self.uth_exploitant)

    # ---------------------------------------------------------------
    # BILAN : FDR, BFR, TRESORERIE, RATIO DE LIQUIDITE
    # ---------------------------------------------------------------
    @property
    def actif_circulant(self) -> float:
        return self.stocks + self.creances + self.tresorerie_actif

    @property
    def fdr(self) -> float:
        """FDR = (Capitaux propres + Dettes LMT) - Actif immobilisé"""
        return (self.capitaux_propres + self.dettes_lmt) - self.actif_immobilise

    @property
    def bfr(self) -> float:
        """BFR = (Stocks + Créances) - Dettes CT (hors trésorerie)"""
        return (self.stocks + self.creances) - self.dettes_ct

    @property
    def tresorerie(self) -> float:
        """Trésorerie = FDR - BFR (doit être cohérente avec Banque + Caisse)"""
        return self.fdr - self.bfr

    @property
    def ratio_liquidite(self) -> float:
        return self._safe_div(self.actif_circulant, self.dettes_ct)

    # ---------------------------------------------------------------
    # COUT DE PRODUCTION / PRIX DE REVIENT DU KG DE CACAO ET SEUIL
    # DE RENTABILITE (LIGNE ROUGE)
    # ---------------------------------------------------------------
    @property
    def cout_production_kg(self) -> float:
        """
        Coût de production du kg = charges opérationnelles cacao / quantité produite.
        """
        return self._safe_div(self.cacao_operational_costs, self.cacao_qty_kg)

    @property
    def prix_revient_kg(self) -> float:
        """
        Prix de revient du kg = (charges opérationnelles cacao + quote-part des
        charges de structure imputable au cacao) / quantité produite.
        La quote-part est estimée proportionnellement à la surface cacao / surface totale.
        """
        if self.surface_ha > 0:
            prorata = self.cacao_surface_ha / self.surface_ha
        else:
            prorata = 1.0
        charges_structure_cacao = self.charges_structure_total * prorata
        total_charges = self.cacao_operational_costs + charges_structure_cacao
        return self._safe_div(total_charges, self.cacao_qty_kg)

    @property
    def seuil_rentabilite_kg(self) -> float:
        """
        Seuil de rentabilité (ligne rouge) = prix de revient du kg.
        Si le prix de vente moyen < ce seuil, la parcelle n'est pas rentable.
        """
        return self.prix_revient_kg

    @property
    def prix_vente_moyen_cacao(self) -> float:
        total_qty = self.cacao_qty_sold_op + self.cacao_qty_sold_third
        total_value = (
            self.cacao_qty_sold_op * self.cacao_price_op
            + self.cacao_qty_sold_third * self.cacao_price_third
        )
        return self._safe_div(total_value, total_qty)

    # ---------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------
    @staticmethod
    def _safe_div(numerator: float, denominator: float) -> float:
        try:
            if denominator in (0, None):
                return 0.0
            return numerator / denominator
        except (TypeError, ZeroDivisionError):
            return 0.0

    def as_results_dict(self) -> dict:
        """Return all computed indicators as a flat dict for display/export."""
        return {
            "res_produit_brut_total": self.produit_brut_total,
            "res_charges_op_total": self.charges_operationnelles_total,
            "res_marge_brute": self.marge_brute_globale,
            "res_cout_kg": self.cout_production_kg,
            "res_prix_revient_kg": self.prix_revient_kg,
            "res_seuil_rentabilite": self.seuil_rentabilite_kg,
            "res_charges_structure": self.charges_structure_total,
            "res_amortissements": self.amortissements,
            "res_valeur_ajoutee": self.valeur_ajoutee,
            "res_va_ha": self.valeur_ajoutee_par_ha,
            "res_va_uth": self.valeur_ajoutee_par_uth,
            "res_ebe": self.ebe,
            "res_ebe_ha": self.ebe_par_ha,
            "res_ebe_uth": self.ebe_par_uth,
            "res_charges_mo": self.charges_personnel_total,
            "res_charges_mo_ha": self._safe_div(self.charges_personnel_total, self.surface_ha),
            "res_amort_ha": self._safe_div(self.amortissements, self.surface_ha),
            "res_charges_financieres": self.charges_financieres_total,
            "res_resultat_courant": self.resultat_courant,
            "res_resultat_ha": self.resultat_courant_par_ha,
            "res_resultat_uth": self.resultat_courant_par_uth,
            "res_services_ext_total": self.services_exterieurs_total,
            "res_services_ext_ha": self.services_exterieurs_par_ha,
            "res_approvisionnements_total": self.approvisionnements_total,
            "res_approvisionnements_ha": self.approvisionnements_par_ha,
            "res_fdr": self.fdr,
            "res_bfr": self.bfr,
            "res_tresorerie": self.tresorerie,
            "res_actif_circulant": self.actif_circulant,
            "res_ratio_liquidite": self.ratio_liquidite,
        }
