import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ─────────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DataScope · Exploration BDD",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0d1117; color: #e6edf3; }
section[data-testid="stSidebar"] { background: #161b22 !important; border-right: 1px solid #21262d; }
section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
.main-title { font-family: 'DM Serif Display', serif; font-size: 2.4rem; font-weight: 400;
    color: #e6edf3; letter-spacing: -0.5px; margin-bottom: 0; line-height: 1.1; }
.main-subtitle { font-size: 0.9rem; color: #7d8590; font-weight: 300;
    letter-spacing: 0.04em; text-transform: uppercase; margin-top: 4px; }
.badge-source { display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; margin-top: 10px; }
.badge-naiades { background: #1f4e79; color: #58a6ff; border: 1px solid #1f6feb; }
.badge-ades    { background: #1e3a2e; color: #3fb950; border: 1px solid #2ea043; }
.kpi-card { background: #161b22; border: 1px solid #21262d; border-radius: 12px;
    padding: 16px 18px 14px 18px; position: relative; overflow: hidden; transition: border-color 0.2s; }
.kpi-card:hover { border-color: #388bfd; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 2px; background: var(--accent); }
.kpi-icon { font-size: 1.2rem; margin-bottom: 6px; opacity: 0.85; }
.kpi-value { font-family: 'DM Serif Display', serif; font-size: 1.9rem;
    color: #e6edf3; line-height: 1; margin-bottom: 4px; }
.kpi-label { font-size: 0.7rem; color: #7d8590; text-transform: uppercase;
    letter-spacing: 0.07em; font-weight: 500; }
.section-header { font-family: 'DM Serif Display', serif; font-size: 1.25rem;
    color: #e6edf3; margin: 28px 0 14px 0; padding-bottom: 8px; border-bottom: 1px solid #21262d; }
.info-banner { background: #161b22; border: 1px solid #21262d; border-left: 3px solid #388bfd;
    border-radius: 8px; padding: 12px 16px; font-size: 0.83rem; color: #8b949e; margin: 12px 0; }
.filter-box { background: #161b22; border: 1px solid #21262d; border-radius: 10px;
    padding: 12px 16px; margin-bottom: 16px; }
.js-plotly-plot .plotly .modebar { background: transparent !important; }
.stTabs [data-baseweb="tab-list"] { background: #161b22; border-bottom: 1px solid #21262d; gap: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #7d8590; border: none;
    padding: 10px 20px; font-family: 'DM Sans', sans-serif; font-size: 0.85rem;
    font-weight: 500; letter-spacing: 0.03em; }
.stTabs [aria-selected="true"] { color: #58a6ff !important; background: transparent !important;
    border-bottom: 2px solid #388bfd !important; }
.stSelectbox > div > div { background: #21262d !important; border-color: #30363d !important; color: #e6edf3 !important; }
div[data-testid="stMetric"] { background: #161b22; border: 1px solid #21262d; border-radius: 10px; padding: 14px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PALETTES & THÈMES EXPORT
# ─────────────────────────────────────────────
PALETTES = {
    "Bleu (Naïades)":   ['#1565C0','#1976D2','#2196F3','#42A5F5','#90CAF9','#BBDEFB'],
    "Vert (ADES)":      ['#1B5E20','#2E7D32','#388E3C','#4CAF50','#81C784','#C8E6C9'],
    "Teal professionnel": ['#004D40','#00695C','#00796B','#009688','#4DB6AC','#B2DFDB'],
    "Gris ardoise":     ['#263238','#37474F','#455A64','#546E7A','#78909C','#B0BEC5'],
    "Bordeaux/Or":      ['#4A148C','#6A1B9A','#880E4F','#B71C1C','#E65100','#F57F17'],
    "Multi catégoriel": ['#1565C0','#2E7D32','#E65100','#6A1B9A','#00695C','#B71C1C'],
}

THEMES_EXPORT = {
    "Fond blanc (publication)": dict(
        paper_bgcolor='white', plot_bgcolor='white',
        font_color='#1a1a1a', grid_color='#e0e0e0',
        line_color='#bdbdbd', title_color='#1a1a1a', text_color='#333333',
    ),
    "Fond blanc cassé (rapport)": dict(
        paper_bgcolor='#FAFAFA', plot_bgcolor='#FAFAFA',
        font_color='#212121', grid_color='#eeeeee',
        line_color='#cccccc', title_color='#212121', text_color='#444444',
    ),
    "Fond sombre (écran)": dict(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#c9d1d9', grid_color='#21262d',
        line_color='#30363d', title_color='#e6edf3', text_color='#8b949e',
    ),
}

FORMATS_PAGE = {
    # h_base       : hauteur de base des graphiques (px dans Streamlit)
    # h_kpi        : hauteur cartouche chiffres clés (px)
    # kpi_val_mult : multiplicateur fsize pour la valeur numérique
    # kpi_lbl_mult : multiplicateur fsize pour le libellé
    # margin       : marges fixes l/r/t/b (px) — indépendantes de fsize
    # export_w/h   : dimensions du PNG exporté (px × scale)
    "PowerPoint paysage (33 × 19 cm)": dict(
        h_base=400, h_kpi=165,
        kpi_val_mult=2.6, kpi_lbl_mult=0.92,
        margin=dict(l=70, r=40, t=55, b=65),
        export_w_cm=24, export_scale=2,
    ),
    "Word / A4 portrait (16 × 10 cm)": dict(
        h_base=680, h_kpi=155,
        kpi_val_mult=2.3, kpi_lbl_mult=0.88,
        margin=dict(l=65, r=35, t=50, b=60),
        export_w_cm=16, export_scale=2,
    ),
    "Demi-page A4 portrait (16 × 7 cm)": dict(
        h_base=500, h_kpi=145,
        kpi_val_mult=2.1, kpi_lbl_mult=0.85,
        margin=dict(l=60, r=30, t=48, b=55),
        export_w_cm=16, export_scale=2,
    ),
    "Carré (présentation web)": dict(
        h_base=560, h_kpi=160,
        kpi_val_mult=2.5, kpi_lbl_mult=0.90,
        margin=dict(l=65, r=35, t=52, b=60),
        export_w_cm=18, export_scale=2,
    ),
}

# ─────────────────────────────────────────────
# HELPERS THÈME
# ─────────────────────────────────────────────
def build_layout(theme, fsize, fig_h, title_text="", fmt_params=None, margin_top=None):
    t = THEMES_EXPORT[theme]
    if fmt_params and 'margin' in fmt_params:
        m = fmt_params['margin']
        mt = margin_top if margin_top is not None else m['t']
        mg = dict(l=m['l'], r=m['r'], t=mt, b=m['b'])
    else:
        mt = margin_top if margin_top is not None else 52
        mg = dict(l=68, r=36, t=mt, b=62)
    return dict(
        paper_bgcolor=t['paper_bgcolor'],
        plot_bgcolor=t['plot_bgcolor'],
        font=dict(family='DM Sans', color=t['font_color'], size=fsize),
        title=dict(text=title_text, font=dict(size=max(fsize+2, 13), color=t['title_color']),
                   x=0, xanchor='left'),
        height=fig_h,
        margin=mg,
    )

def axis_style(theme, fsize=11, extra=None):
    t = THEMES_EXPORT[theme]
    d = dict(
        gridcolor=t['grid_color'],
        linecolor=t['line_color'],
        tickcolor=t['line_color'],
        color=t['text_color'],
        tickfont=dict(size=max(7, fsize-2), color=t['text_color'], family='DM Sans'),
        title_font=dict(size=fsize, color=t['text_color'], family='DM Sans'),
    )
    if extra:
        d.update(extra)
    return d

def bar_textcolor(theme):
    return THEMES_EXPORT[theme]['font_color']

# ─────────────────────────────────────────────
# DÉTECTION FORMAT
# ─────────────────────────────────────────────
def detect_format(df):
    cols = ' '.join([c.lower() for c in df.columns])
    if 'lbsupport' in cols or 'cdstationmesure' in cols or 'lblong' in cols:
        return 'NAIADES'
    if 'identifiant national bss' in cols or 'code_bss' in cols or ('bss' in cols and 'qualification' in cols and 'lbsupport' not in cols):
        return 'ADES'
    return 'INCONNU'

# ─────────────────────────────────────────────
# PARSING NAÏADES
# ─────────────────────────────────────────────
def parse_naiades(df):
    df = df.copy()
    for col in ['DatePrel', 'DateAna']:
        if col in df.columns:
            df[col] = pd.to_datetime('1899-12-30') + pd.to_timedelta(
                pd.to_numeric(df[col], errors='coerce'), unit='D')
    df['année'] = df['DatePrel'].dt.year if 'DatePrel' in df.columns else np.nan
    df['mois']  = df['DatePrel'].dt.month if 'DatePrel' in df.columns else np.nan
    return df

def stats_naiades(df, support_filter=None):
    d = df.copy()
    if support_filter and 'LbSupport' in d.columns:
        d = d[d['LbSupport'].isin(support_filter)]
    s = {}
    s['source']          = 'NAIADES'
    s['col_station']     = 'LbStationMesureEauxSurface'
    s['col_param']       = 'LbLongParamètre'
    s['col_support']     = 'LbSupport'
    s['col_fraction']    = 'LbFractionAnalysee'
    s['col_campagne']    = 'CdPrelevement'
    s['col_qualif']      = 'LbQualAna'
    s['col_statut']      = 'MnemoStatutAna'
    s['col_producteur']  = 'NomProducteur'
    s['n_mesures']       = len(d)
    s['n_stations']      = d['LbStationMesureEauxSurface'].nunique() if 'LbStationMesureEauxSurface' in d.columns else 0
    s['n_parametres']    = d['LbLongParamètre'].nunique() if 'LbLongParamètre' in d.columns else 0
    s['n_campagnes']     = d['CdPrelevement'].nunique() if 'CdPrelevement' in d.columns else 0
    try:
        s['annee_min'] = int(d['année'].min()) if 'année' in d.columns and d['année'].notna().any() else '?'
        s['annee_max'] = int(d['année'].max()) if 'année' in d.columns and d['année'].notna().any() else '?'
    except (ValueError, TypeError):
        s['annee_min'] = '?'
        s['annee_max'] = '?'
    s['n_annees']        = d['année'].nunique() if 'année' in d.columns else 0
    s['supports']        = sorted(df['LbSupport'].dropna().unique().tolist()) if 'LbSupport' in df.columns else []
    s['n_supports']      = len(s['supports'])
    s['fractions']       = d['LbFractionAnalysee'].dropna().unique().tolist() if 'LbFractionAnalysee' in d.columns else []
    s['n_fractions']     = len(s['fractions'])
    s['qualif']          = {str(k): v for k,v in d['LbQualAna'].value_counts().to_dict().items() if str(k) != 'nan'} if 'LbQualAna' in d.columns else {}
    s['statut']          = {str(k): v for k,v in d['MnemoStatutAna'].value_counts().to_dict().items() if str(k) != 'nan'} if 'MnemoStatutAna' in d.columns else {}
    s['n_producteurs']   = d['NomProducteur'].nunique() if 'NomProducteur' in d.columns else 0
    s['producteurs']     = {str(k): v for k,v in d['NomProducteur'].value_counts().to_dict().items() if str(k) != 'nan'} if 'NomProducteur' in d.columns else {}
    s['params_par_support']  = d.dropna(subset=['LbSupport']).groupby('LbSupport')['LbLongParamètre'].nunique().to_dict() if 'LbSupport' in d.columns else {}
    s['mesures_par_station'] = d.dropna(subset=['LbStationMesureEauxSurface']).groupby('LbStationMesureEauxSurface').size().sort_values(ascending=False).to_dict() if 'LbStationMesureEauxSurface' in d.columns else {}
    s['params_par_station']  = d.dropna(subset=['LbStationMesureEauxSurface']).groupby('LbStationMesureEauxSurface')['LbLongParamètre'].nunique().sort_values(ascending=False).to_dict() if 'LbStationMesureEauxSurface' in d.columns else {}
    s['annees_par_station']  = d.dropna(subset=['LbStationMesureEauxSurface']).groupby('LbStationMesureEauxSurface')['année'].nunique().sort_values(ascending=False).to_dict() if 'LbStationMesureEauxSurface' in d.columns else {}
    s['campagnes_par_annee'] = d.dropna(subset=['année']).groupby('année')['CdPrelevement'].nunique().to_dict() if 'CdPrelevement' in d.columns else {}
    s['mesures_par_annee']   = d.dropna(subset=['année']).groupby('année').size().to_dict() if 'année' in d.columns else {}
    return s, d

# ─────────────────────────────────────────────
# PARSING ADES
# ─────────────────────────────────────────────
def parse_ades(df):
    df = df.copy()
    if 'Date prélèvement' in df.columns:
        df['DatePrel'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(
            df['Date prélèvement'].astype(str).str.replace(',', '.').pipe(pd.to_numeric, errors='coerce'), unit='D')
        df['année'] = df['DatePrel'].dt.year
        df['mois']  = df['DatePrel'].dt.month
    return df

def stats_ades(df, support_filter=None):
    d = df.copy()
    if support_filter and 'Support' in d.columns:
        d = d[d['Support'].isin(support_filter)]
    s = {}
    s['source']          = 'ADES'
    s['col_station']     = 'Identifiant national BSS'
    s['col_param']       = 'Paramètre'
    s['col_support']     = 'Support'
    s['col_fraction']    = 'Fraction analysée'
    s['col_campagne']    = 'Numéro de prélèvement'
    s['col_qualif']      = 'Qualification'
    s['col_statut']      = 'Statut mesure'
    s['col_producteur']  = 'Producteur données'
    s['n_mesures']       = len(d)
    s['n_stations']      = d['Identifiant national BSS'].nunique() if 'Identifiant national BSS' in d.columns else 0
    s['n_parametres']    = d['Paramètre'].nunique() if 'Paramètre' in d.columns else 0
    s['n_campagnes']     = d['Numéro de prélèvement'].nunique() if 'Numéro de prélèvement' in d.columns else 0
    try:
        s['annee_min'] = int(d['année'].min()) if 'année' in d.columns and d['année'].notna().any() else '?'
        s['annee_max'] = int(d['année'].max()) if 'année' in d.columns and d['année'].notna().any() else '?'
    except (ValueError, TypeError):
        s['annee_min'] = '?'
        s['annee_max'] = '?'
    s['n_annees']        = d['année'].nunique() if 'année' in d.columns else 0
    s['supports']        = sorted(df['Support'].dropna().unique().tolist()) if 'Support' in df.columns else []
    s['n_supports']      = len(s['supports'])
    s['fractions']       = d['Fraction analysée'].dropna().unique().tolist() if 'Fraction analysée' in d.columns else []
    s['n_fractions']     = len(s['fractions'])
    s['qualif']          = {str(k): v for k,v in d['Qualification'].value_counts().to_dict().items() if str(k) != 'nan'} if 'Qualification' in d.columns else {}
    s['statut']          = {str(k): v for k,v in d['Statut mesure'].value_counts().to_dict().items() if str(k) != 'nan'} if 'Statut mesure' in d.columns else {}
    s['n_producteurs']   = d['Producteur données'].nunique() if 'Producteur données' in d.columns else 0
    s['producteurs']     = {str(k): v for k,v in d['Producteur données'].value_counts().to_dict().items() if str(k) != 'nan'} if 'Producteur données' in d.columns else {}
    s['types_point']     = {str(k): v for k,v in d['Type qualitomètre'].value_counts().to_dict().items() if str(k) != 'nan'} if 'Type qualitomètre' in d.columns else {}
    s['params_par_support']  = d.dropna(subset=['Support']).groupby('Support')['Paramètre'].nunique().to_dict() if 'Support' in d.columns else {}
    s['mesures_par_station'] = d.dropna(subset=['Identifiant national BSS']).groupby('Identifiant national BSS').size().sort_values(ascending=False).to_dict() if 'Identifiant national BSS' in d.columns else {}
    s['params_par_station']  = d.dropna(subset=['Identifiant national BSS']).groupby('Identifiant national BSS')['Paramètre'].nunique().sort_values(ascending=False).to_dict() if 'Identifiant national BSS' in d.columns else {}
    s['annees_par_station']  = d.dropna(subset=['Identifiant national BSS']).groupby('Identifiant national BSS')['année'].nunique().sort_values(ascending=False).to_dict() if 'Identifiant national BSS' in d.columns else {}
    s['campagnes_par_annee'] = d.dropna(subset=['année']).groupby('année')['Numéro de prélèvement'].nunique().to_dict() if 'Numéro de prélèvement' in d.columns else {}
    s['mesures_par_annee']   = d.dropna(subset=['année']).groupby('année').size().to_dict() if 'année' in d.columns else {}
    return s, d

# ─────────────────────────────────────────────
# GRAPHIQUES
# ─────────────────────────────────────────────
def fig_timeline(s, palette, theme, fsize, fig_h, fmt_params=None):
    mpa = {k:v for k,v in s.get('mesures_par_annee',{}).items() if k == k}  # filtre NaN
    if not mpa:
        return None
    ann  = sorted(mpa.keys())
    mes  = [mpa[a] for a in ann]
    camp = [s.get('campagnes_par_annee', {}).get(a, 0) for a in ann]
    c1, c2 = palette[0], palette[2] if len(palette) > 2 else palette[-1]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=ann, y=mes, name="Mesures", marker_color=c1,
        opacity=0.85, marker_line_width=0,
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=ann, y=camp, name="Campagnes",
        line=dict(color=c2, width=2.5),
        mode='lines+markers', marker=dict(size=5),
    ), secondary_y=True)

    t = THEMES_EXPORT[theme]
    fig.update_layout(
        paper_bgcolor=t['paper_bgcolor'], plot_bgcolor=t['plot_bgcolor'],
        font=dict(family='DM Sans', color=t['font_color'], size=fsize),
        title=dict(text="Évolution temporelle", font=dict(size=fsize+2, color=t['title_color']), x=0),
        legend=dict(orientation='h', y=1.06, x=0, bgcolor='rgba(0,0,0,0)',
                    font=dict(size=fsize-1, color=t['font_color'])),
        height=fig_h, barmode='overlay',
        margin=dict(
            l=fmt_params['margin']['l'] if fmt_params else 68,
            r=fmt_params['margin']['r']+20 if fmt_params else 56,
            t=fmt_params['margin']['t']+8 if fmt_params else 60,
            b=fmt_params['margin']['b'] if fmt_params else 62,
        ),
    )
    ax = axis_style(theme, fsize)
    fig.update_xaxes(**ax, dtick=5, title_text="Année")
    fig.update_yaxes(title_text="Nb mesures", secondary_y=False,
                     gridcolor=ax['gridcolor'], linecolor=ax['linecolor'],
                     tickfont=ax['tickfont'], title_font=ax['title_font'],
                     color=t['text_color'])
    fig.update_yaxes(title_text="Nb campagnes", secondary_y=True,
                     gridcolor='rgba(0,0,0,0)', linecolor=ax['linecolor'],
                     tickfont=ax['tickfont'], title_font=ax['title_font'],
                     color=t['text_color'], showgrid=False)
    return fig


def fig_heatmap_stations(df, s, fmt, palette, theme, fsize, fig_h, fmt_params=None):
    try:
        col_st = s['col_station']
        df_hm = df.dropna(subset=[col_st, 'année']).copy()
        df_hm['année'] = df_hm['année'].astype(int)
        if df_hm.empty:
            return None
        pivot = df_hm.groupby([col_st, 'année']).size().unstack(fill_value=0)
        top = pivot.sum(axis=1).nlargest(20).index
        pivot = pivot.loc[top]
        t = THEMES_EXPORT[theme]
        # Transformation log pour faire ressortir les faibles densités
        pivot_log = np.log1p(pivot.values)  # log(1+x) : 0 reste 0, faibles valeurs ressortent

        # Colorscale : contraste fort même sur fond blanc
        if 'sombre' in theme.lower():
            cscale = [
                [0.00, '#0d1117'],
                [0.05, '#1f2937'],
                [0.25, palette[1]],
                [0.65, palette[0]],
                [1.00, '#ffffff'],
            ]
        else:
            # Fond blanc : partir d'un gris très clair vers la couleur pleine
            # — évite le piège du bleu pâle quasi-blanc
            cscale = [
                [0.00, '#f0f0f0'],   # vide / zéro : gris très clair
                [0.08, '#d0e8ff'] if palette[0].startswith('#1') else [0.08, '#d5f0d5'],
                [0.30, palette[3] if len(palette)>3 else palette[-1]],
                [0.70, palette[1]],
                [1.00, palette[0]],
            ]

        fig = px.imshow(
            pivot_log,
            x=[str(c) for c in pivot.columns],   # années (int → str pour affichage)
            y=pivot.index.tolist(),               # noms de stations conservés
            color_continuous_scale=cscale,
            aspect='auto',
            labels=dict(x='Année', y='Station', color='Mesures (log)'),
        )
        fig.update_layout(
            paper_bgcolor=t['paper_bgcolor'], plot_bgcolor=t['plot_bgcolor'],
            font=dict(family='DM Sans', color=t['font_color'], size=fsize),
            title=dict(text="Couverture temporelle par station (Top 20)",
                       font=dict(size=fsize+2, color=t['title_color']), x=0),
            height=fig_h + 120,
            margin=dict(
                l=fmt_params['margin']['l'] if fmt_params else 20,
                r=fmt_params['margin']['r']+60 if fmt_params else 80,
                t=fmt_params['margin']['t'] if fmt_params else 50,
                b=fmt_params['margin']['b'] if fmt_params else 40,
            ),
            coloraxis_colorbar=dict(
                title="Mesures",
                thickness=12, len=0.7,
                # Reconvertir log → vraies valeurs sur l'échelle colorbar
                tickvals=[np.log1p(v) for v in [0,1,5,10,50,100,500,1000,5000]
                          if np.log1p(v) <= pivot_log.max()],
                ticktext=[str(v) for v in [0,1,5,10,50,100,500,1000,5000]
                          if np.log1p(v) <= pivot_log.max()],
                tickfont=dict(color=t['text_color'], size=max(7,fsize-2)),
                title_font=dict(color=t['text_color'], size=fsize-1),
            ),
        )
        ax = axis_style(theme, fsize)
        fig.update_xaxes(**ax, title='', dtick=5)
        fig.update_yaxes(**ax, title='')
        return fig
    except Exception:
        return None


def fig_stations_heterogeneite(s, palette, theme, fsize, fig_h, fmt_params=None):
    stations = list(s.get('mesures_par_station', {}).keys())[:25]
    if not stations:
        return None
    mesures = [s['mesures_par_station'].get(st, 0) for st in stations]
    params  = [s.get('params_par_station', {}).get(st, 0) for st in stations]
    annees  = [s.get('annees_par_station', {}).get(st, 0) for st in stations]
    max_m   = max(mesures) if mesures else 1
    t = THEMES_EXPORT[theme]

    if 'sombre' in theme.lower():
        cscale = [[0,'#21262d'],[1, palette[0]]]
    else:
        cscale = [[0, palette[4] if len(palette) > 4 else '#90CAF9'],[1, palette[0]]]

    # Filtre anti-superposition des labels :
    # on n'affiche le label que si aucun autre point n'est trop proche
    sizes_px = [m/max_m*55+10 for m in mesures]
    x_range = max(annees) - min(annees) if len(annees) > 1 else 1
    y_range = max(params) - min(params) if len(params) > 1 else 1
    show_label = []
    for i in range(len(stations)):
        too_close = False
        for j in range(len(stations)):
            if i == j:
                continue
            dx = abs(annees[i] - annees[j]) / (x_range + 1e-9)
            dy = abs(params[i] - params[j]) / (y_range + 1e-9)
            dist = (dx**2 + dy**2) ** 0.5
            min_dist = 0.08 + (sizes_px[i] + sizes_px[j]) / 2 / 600
            if dist < min_dist:
                too_close = True
                break
        show_label.append(not too_close)

    labels_display = [
        (st[:18]+'…' if len(st)>18 else st) if show_label[i] else ''
        for i, st in enumerate(stations)
    ]

    fig = go.Figure(go.Scatter(
        x=annees, y=params,
        mode='markers+text',
        marker=dict(
            size=sizes_px,
            color=mesures, colorscale=cscale, showscale=True,
            colorbar=dict(title="Mesures", thickness=12, len=0.65,
                          tickfont=dict(color=t['text_color'], size=fsize-2),
                          title_font=dict(color=t['text_color'], size=fsize-1)),
            line=dict(color=palette[0], width=1),
            opacity=0.85,
        ),
        text=labels_display,
        textposition='top center',
        textfont=dict(size=max(7, fsize-3), color=t['text_color']),
        hovertemplate='<b>%{customdata}</b><br>Années actives: %{x}<br>Paramètres: %{y}<extra></extra>',
        customdata=stations,
    ))
    fig.update_layout(
        paper_bgcolor=t['paper_bgcolor'], plot_bgcolor=t['plot_bgcolor'],
        font=dict(family='DM Sans', color=t['font_color'], size=fsize),
        title=dict(text="Hétérogénéité inter-stations  (taille ∝ nb mesures)",
                   font=dict(size=fsize+2, color=t['title_color']), x=0),
        height=fig_h + 60, margin=dict(
            l=fmt_params['margin']['l'] if fmt_params else 68,
            r=fmt_params['margin']['r']+60 if fmt_params else 80,
            t=fmt_params['margin']['t']+5 if fmt_params else 58,
            b=fmt_params['margin']['b'] if fmt_params else 62,
        ),
    )
    ax = axis_style(theme, fsize)
    fig.update_xaxes(**ax, title='Années actives')
    fig.update_yaxes(**ax, title='Paramètres uniques')
    return fig


def fig_supports_params(s, palette, theme, fsize, fig_h, fmt_params=None):
    data = s.get('params_par_support', {})
    if not data:
        return None
    labels = list(data.keys())
    values = list(data.values())
    t = THEMES_EXPORT[theme]
    fig = go.Figure(go.Bar(
        y=labels, x=values, orientation='h',
        marker=dict(
            color=values,
            colorscale=[[0, palette[3] if len(palette) > 3 else palette[-1]],[1, palette[0]]],
            line=dict(width=0),
        ),
        text=[f" {v}" for v in values],
        textfont=dict(color=bar_textcolor(theme), size=fsize-1),
        textposition='outside',
    ))
    fig.update_layout(**build_layout(theme, fsize, max(fig_h, len(labels)*max(40,fsize*3)), "Paramètres par support", fmt_params))
    fig.update_xaxes(**axis_style(theme, fsize), title='Nb paramètres uniques')
    fig.update_yaxes(**axis_style(theme, fsize), categoryorder='total ascending')
    return fig


def fig_qualite(s, palette, theme, fsize, fig_h):
    qualif = s.get('qualif', {})
    if not qualif:
        return None
    labels = list(qualif.keys())
    values = list(qualif.values())
    t = THEMES_EXPORT[theme]
    # Couleurs sémantiques fixes (indépendantes de la palette)
    cmap = {'Correcte':'#2E7D32','Correct':'#2E7D32',
            'Incorrecte':'#C62828','Incorrect':'#C62828',
            'Incertaine':'#E65100','non définissable':'#78909C'}
    colors_q = [cmap.get(l, palette[i % len(palette)]) for i, l in enumerate(labels)]
    total = sum(values)

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=colors_q, line=dict(color=t['paper_bgcolor'], width=3)),
        hole=0.52,
        textinfo='label+percent',
        textfont=dict(size=fsize-1, color=t['font_color']),
        insidetextorientation='auto',
    ))
    fig.add_annotation(
        text=f"<b>{total:,}</b>".replace(',', '\u202f'),
        font=dict(size=fsize+4, color=t['title_color'], family='DM Serif Display'),
        showarrow=False, x=0.5, y=0.5
    )
    fig.update_layout(
        paper_bgcolor=t['paper_bgcolor'],
        font=dict(family='DM Sans', color=t['font_color'], size=fsize),
        title=dict(text="Qualification des données", font=dict(size=fsize+2, color=t['title_color']), x=0),
        showlegend=True,
        legend=dict(font=dict(size=fsize-1, color=t['font_color']),
                    bgcolor='rgba(0,0,0,0)', x=1.02, y=0.5),
        height=fig_h, margin=dict(l=20, r=120, t=50, b=20),
    )
    return fig


def fig_producteurs(s, palette, theme, fsize, fig_h, fmt_params=None):
    prod = s.get('producteurs', {})
    if not prod:
        return None
    labels = list(prod.keys())
    short_labels = [k[:40]+'…' if len(k) > 40 else k for k in labels]
    values = list(prod.values())
    n = len(labels)
    colors_p = [palette[i % len(palette)] for i in range(n)]
    t = THEMES_EXPORT[theme]

    fig = go.Figure(go.Bar(
        x=short_labels, y=values,
        marker=dict(color=colors_p, line=dict(width=0)),
        text=values,
        textfont=dict(color=bar_textcolor(theme), size=fsize-1),
        textposition='outside',
    ))
    fig.update_layout(**build_layout(theme, fsize, fig_h, "Répartition par producteur", fmt_params))
    fig.update_xaxes(**axis_style(theme, fsize), tickangle=-30)
    fig.update_yaxes(**axis_style(theme, fsize), title='Mesures')
    return fig


def fig_top_params(df, s, palette, theme, fsize, fig_h, fmt_params=None, n=20):
    col = s['col_param']
    top = df[col].value_counts().head(n)
    t = THEMES_EXPORT[theme]
    fig = go.Figure(go.Bar(
        y=top.index.tolist(), x=top.values.tolist(),
        orientation='h',
        marker=dict(
            color=top.values.tolist(),
            colorscale=[[0, palette[3] if len(palette) > 3 else palette[-1]],[1, palette[0]]],
            line=dict(width=0)
        ),
        text=[f" {v:,}".replace(',', '\u202f') for v in top.values],
        textfont=dict(color=bar_textcolor(theme), size=max(8, fsize-2)),
        textposition='outside',
    ))
    fig.update_layout(**build_layout(theme, fsize, max(fig_h, n*max(24,fsize*2)), f"Top {n} paramètres les plus mesurés", fmt_params))
    fig.update_xaxes(**axis_style(theme, fsize), title='Nb mesures')
    fig.update_yaxes(**axis_style(theme, fsize), categoryorder='total ascending')
    return fig


def make_kpi_figure(s, palette, theme, fsize, fmt_params, source_label, annee_min, annee_max, filename=""):
    """
    Cartouche KPI en coordonnées data (range 0-N × 0-1).
    Shapes et annotations sur le même référentiel → pas de décalage.
    """
    t = THEMES_EXPORT[theme]
    accent   = palette[0]
    bg_paper = t['paper_bgcolor'] if t['paper_bgcolor'] not in ('rgba(0,0,0,0)', 'transparent') else '#161b22'
    border_c = '#484f58' if 'sombre' in theme.lower() else '#d0d0d0'

    items = [
        ("Stations",   s.get('n_stations', 0)),
        ("Paramètres", s.get('n_parametres', 0)),
        ("Campagnes",  s.get('n_campagnes', 0)),
        ("Années",     s.get('n_annees', 0)),
        ("Mesures",    s.get('n_mesures', 0)),
        ("Supports",   s.get('n_supports', 0)),
    ]
    N = len(items)

    # Tailles de police calées sur fsize
    val_size = max(14, int(fsize * fmt_params.get('kpi_val_mult', 2.4)))
    lbl_size = max(7,  int(fsize * fmt_params.get('kpi_lbl_mult', 0.88)))
    foot_size = max(7, fsize - 2)

    fig = go.Figure()

    # Coordonnées data : x ∈ [0, N], y ∈ [0, 1]
    # → shapes et annotations parfaitement alignés quelle que soit la hauteur
    pad = 0.04  # espace entre cartes

    for i in range(N):
        x0, x1 = i + pad, i + 1 - pad
        # Barre colorée en haut
        fig.add_shape(
            type="rect", x0=x0, x1=x1, y0=0.84, y1=0.98,
            fillcolor=accent, line_width=0,
        )
        # Corps de la carte
        fig.add_shape(
            type="rect", x0=x0, x1=x1, y0=0.02, y1=0.84,
            fillcolor=bg_paper,
            line=dict(color=border_c, width=1),
        )
        # Valeur numérique
        val = items[i][1]
        val_str = f"{val:,}".replace(',', '\u202f') if isinstance(val, int) else str(val)
        fig.add_annotation(
            x=i + 0.5, y=0.57,
            text=f"<b>{val_str}</b>",
            font=dict(size=val_size, color=t['title_color'], family='DM Serif Display'),
            showarrow=False, align="center", xanchor="center", yanchor="middle",
        )
        # Libellé
        fig.add_annotation(
            x=i + 0.5, y=0.20,
            text=items[i][0].upper(),
            font=dict(size=lbl_size, color=t['text_color'], family='DM Sans'),
            showarrow=False, align="center", xanchor="center", yanchor="middle",
        )

    # Pied de cartouche (hors de la zone data, en paper coords)
    period = f"{annee_min} – {annee_max}"
    fname_clean = filename.replace('.csv','').replace('_',' ')
    fig.add_annotation(
        x=0.5, y=-0.10, xref="paper", yref="paper",
        text=f"<b>{fname_clean}</b>  ·  {source_label}  ·  {period}",
        font=dict(size=foot_size, color=t['text_color'], family='DM Sans'),
        showarrow=False, align="center",
    )

    fig.update_layout(
        paper_bgcolor=bg_paper,
        plot_bgcolor='rgba(0,0,0,0)',
        height=fmt_params['h_kpi'],
        margin=dict(l=8, r=8, t=8, b=28),
        xaxis=dict(visible=False, range=[0, N], fixedrange=True),
        yaxis=dict(visible=False, range=[0, 1],  fixedrange=True),
        showlegend=False,
    )
    return fig


def render_kpis(s, palette, theme, fsize, fmt_params, fig_w_px, source_label, annee_min, annee_max, filename=""):
    """Affiche la cartouche KPI Plotly avec bouton de téléchargement PNG intégré."""
    fig = make_kpi_figure(s, palette, theme, fsize, fmt_params, source_label, annee_min, annee_max, filename)
    # Hauteur export : proportionnelle à la largeur (ratio ≈ 1:4 pour une cartouche)
    h_export = max(160, int(fig_w_px * 0.22))
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "toImageButtonOptions": {
                "format": "png",
                "filename": f"kpi_{filename.replace('.csv','').replace(' ','_')}",
                "height": h_export,
                "width":  fig_w_px,
                "scale":  fmt_params.get('export_scale', 2),
            },
            "modeBarButtonsToRemove": [
                "zoom2d","pan2d","select2d","lasso2d",
                "zoomIn2d","zoomOut2d","autoScale2d","resetScale2d"
            ],
        }
    )

# ─────────────────────────────────────────────
# CHARGEMENT
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(file_bytes, filename):
    encodings  = ['latin1', 'utf-8', 'cp1252']
    separators = [',', ';', '\t']
    for enc in encodings:
        try:
            sample = io.BytesIO(file_bytes)
            head = b""
            for _ in range(20):
                line = sample.readline()
                if not line:
                    break
                head += line
            first_line = head.decode(enc, errors='replace').split('\n')[0]
            sep_counts = {s: first_line.count(s) for s in separators}
            best_sep = max(sep_counts, key=sep_counts.get)
        except Exception:
            best_sep = ','
        for sep in ([best_sep] + [s for s in separators if s != best_sep]):
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), sep=sep, encoding=enc,
                                 low_memory=False, on_bad_lines='skip')
                if df.shape[1] >= 3:
                    return df, enc, sep
            except Exception:
                continue
    return None, None, None

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 16px 0;'>
        <div style='font-family:"DM Serif Display",serif; font-size:1.35rem; color:#e6edf3;'>DataScope</div>
        <div style='font-size:0.68rem; color:#7d8590; letter-spacing:0.1em; text-transform:uppercase;'>Exploration de données</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**📂 Charger un fichier**")
    uploaded = st.file_uploader("CSV — Naïades ou ADES", type=['csv'],
        help="Fichiers issus des bases Naïades ou ADES. Encodage latin-1 supporté. Séparateur auto-détecté.")

    st.markdown("---")
    st.markdown("**🎨 Mise en page**")

    sel_theme = st.selectbox("Fond / contexte d'export",
        list(THEMES_EXPORT.keys()), index=2,
        help="Choisir 'Fond blanc' pour copier dans Word/PPT")

    sel_palette_name = st.selectbox("Palette de couleurs", list(PALETTES.keys()), index=0)
    sel_palette = PALETTES[sel_palette_name]

    sel_format = st.selectbox("Format cible", list(FORMATS_PAGE.keys()), index=0,
        help="Détermine les proportions et hauteurs des figures")
    fmt_params = FORMATS_PAGE[sel_format]

    # Tout en cm — conversion px ↔ cm à 150 dpi (qualité impression)
    DPI   = 150
    CM_PX = DPI / 2.54  # ≈ 59 px/cm

    col_hw1, col_hw2 = st.columns(2)
    with col_hw1:
        fig_h_cm = st.slider(
            "Hauteur (cm)", min_value=4, max_value=25,
            value=round(fmt_params['h_base'] / CM_PX),
            step=1,
            help="Hauteur des graphiques (4–25 cm)"
        )
    with col_hw2:
        fig_w_cm = st.slider(
            "Largeur (cm)", min_value=8, max_value=30,
            value=fmt_params.get('export_w_cm', 16),
            step=1,
            help="Largeur des graphiques (8–30 cm · 16 cm = A4 pleine largeur)"
        )
    # Conversion cm → px pour Plotly (hauteur affichage) et export PNG
    fig_h_base     = int(fig_h_cm * CM_PX)
    fig_w_px_export = int(fig_w_cm * CM_PX)

    fsize = st.slider("Taille de police (pt)", 9, 18, 11)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.7rem; color:#484f58; line-height:1.7;'>
    Formats supportés<br>
    <span style='color:#58a6ff;'>● Naïades</span> physico-chimie<br>
    <span style='color:#3fb950;'>● ADES</span> eaux souterraines
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LANDING
# ─────────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div style='padding: 20px 0 8px 0;'>
        <div class='main-title'>Exploration<br>de la donnée</div>
        <div class='main-subtitle'>Naïades · ADES · Qualité des eaux</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-banner'>
    👈 <b>Ouvrez le panneau latéral gauche</b> pour charger votre fichier CSV et paramétrer la mise en page.<br>
    Si la barre est fermée, cliquez sur la flèche <code>&gt;</code> en haut à gauche.
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='kpi-card' style='--accent:#58a6ff;'>
            <div class='kpi-icon'>🏞️</div>
            <div style='font-family:"DM Serif Display",serif;font-size:1.05rem;color:#e6edf3;margin-bottom:5px;'>Naïades</div>
            <div style='font-size:0.78rem;color:#7d8590;line-height:1.5;'>Eaux de surface · Physico-chimie<br>Supports : eau, sédiments, biotes</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='kpi-card' style='--accent:#3fb950;'>
            <div class='kpi-icon'>💧</div>
            <div style='font-family:"DM Serif Display",serif;font-size:1.05rem;color:#e6edf3;margin-bottom:5px;'>ADES</div>
            <div style='font-size:0.78rem;color:#7d8590;line-height:1.5;'>Eaux souterraines · BSS<br>Supports : eau, air brut</div>
        </div>""", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# CHARGEMENT & PARSING — tout en session_state
# ─────────────────────────────────────────────
# Clé unique par fichier (nom + taille)
file_key = uploaded.name + "_" + str(uploaded.size)

# Si nouveau fichier : lire, parser, mettre en cache
if st.session_state.get('file_key') != file_key:
    raw_bytes = uploaded.read()
    if not raw_bytes:
        st.error("❌ Fichier vide.")
        st.stop()

    with st.spinner("Chargement… (patientez pour les fichiers volumineux)"):
        df_raw, detected_enc, detected_sep = load_data(raw_bytes, uploaded.name)

    if df_raw is None:
        st.error("❌ Impossible de lire le fichier.")
        st.markdown("**Solution :** ouvre le fichier dans Excel → *Enregistrer sous* → **CSV UTF-8**, puis recharge.")
        st.stop()

    fmt_detected = detect_format(df_raw)
    if fmt_detected not in ('NAIADES', 'ADES'):
        st.warning("Format non reconnu. Vérifiez la structure du fichier.")
        st.dataframe(df_raw.head(3))
        st.stop()

    with st.spinner("Analyse de la structure…"):
        if fmt_detected == 'NAIADES':
            df_parsed = parse_naiades(df_raw)
            s_full, _ = stats_naiades(df_parsed)
            badge_class  = 'badge-naiades'
            badge_label  = 'Naïades — Eaux de surface'
        else:
            df_parsed = parse_ades(df_raw)
            s_full, _ = stats_ades(df_parsed)
            badge_class  = 'badge-ades'
            badge_label  = 'ADES — Eaux souterraines'

    # Tout stocker en session_state
    st.session_state['file_key']      = file_key
    st.session_state['df_parsed']     = df_parsed
    st.session_state['s_full']        = s_full
    st.session_state['fmt']           = fmt_detected
    st.session_state['badge_class']   = badge_class
    st.session_state['badge_label']   = badge_label
    st.session_state['detected_enc']  = detected_enc
    st.session_state['detected_sep']  = detected_sep
    st.session_state['n_raw_rows']    = len(df_raw)
    st.session_state['n_raw_cols']    = df_raw.shape[1]

# Récupérer depuis session_state (reruns sans re-parsing)
df_parsed     = st.session_state['df_parsed']
s_full        = st.session_state['s_full']
fmt           = st.session_state['fmt']
badge_class   = st.session_state['badge_class']
badge_label   = st.session_state['badge_label']
detected_enc  = st.session_state['detected_enc']
detected_sep  = st.session_state['detected_sep']
n_raw_rows    = st.session_state['n_raw_rows']
n_raw_cols    = st.session_state['n_raw_cols']

all_supports = s_full.get('supports', [])

# ─────────────────────────────────────────────
# FILTRES SUPPORT (sidebar, après détection)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    if all_supports:
        st.markdown("**🔽 Filtre par support**")
        st.markdown(
            "<div style='font-size:0.72rem;color:#7d8590;margin-bottom:6px;'>"
            "Actif sur les onglets 1 et 2. Tout décocher = données vides.</div>",
            unsafe_allow_html=True
        )
        sel_supports = st.multiselect(
            "Supports à inclure",
            options=all_supports,
            default=all_supports,
            help="Filtre actif sur les onglets Temporalité et Stations. Sélectionner un ou plusieurs supports."
        )
        if not sel_supports:
            st.warning("⚠️ Aucun support sélectionné — sélectionnez au moins un support.")
    else:
        sel_supports = []

    if st.session_state.get('file_key'):
        st.markdown(f"""
        <div style='font-size:0.68rem; color:#484f58; margin-top:10px;'>
        ✓ Encodage : <code style='color:#58a6ff'>{st.session_state.get('detected_enc','?')}</code><br>
        ✓ Séparateur : <code style='color:#58a6ff'>{repr(st.session_state.get('detected_sep','?'))}</code><br>
        ✓ {st.session_state.get('n_raw_rows',0):,} lignes · {st.session_state.get('n_raw_cols',0)} colonnes
        </div>""".replace(',', '\u202f'), unsafe_allow_html=True)

# Stats filtrées (pour onglets 1 et 2) et complètes (pour 3 et 4)
support_filter = sel_supports if sel_supports and set(sel_supports) != set(all_supports) else None

# Cache les stats filtrées (recalcul seulement si le filtre change)
filt_key = str(sorted(support_filter)) if support_filter else "all"
if st.session_state.get('filt_key') != filt_key or st.session_state.get('file_key') != file_key:
    if fmt == 'NAIADES':
        s_filt, df_filt = stats_naiades(df_parsed, support_filter)
        s_full_new, df_full = stats_naiades(df_parsed)
    else:
        s_filt, df_filt = stats_ades(df_parsed, support_filter)
        s_full_new, df_full = stats_ades(df_parsed)
    st.session_state['filt_key'] = filt_key
    st.session_state['s_filt']   = s_filt
    st.session_state['df_filt']  = df_filt
    st.session_state['df_full']  = df_full
    # s_full already stored but recompute if new file
    if st.session_state.get('s_full_computed') != file_key:
        st.session_state['s_full'] = s_full_new
        st.session_state['s_full_computed'] = file_key

s_filt  = st.session_state['s_filt']
df_filt = st.session_state['df_filt']
df_full = st.session_state['df_full']
s_full  = st.session_state['s_full']

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
filter_note = ""
if support_filter:
    filter_note = f" · Filtre : {', '.join(support_filter)}"

st.markdown(f"""
<div style='padding: 8px 0 0 0;'>
    <div class='main-title'>{uploaded.name.replace('.csv','').replace('_',' ')}</div>
    <div class='main-subtitle'>Exploration · Synthèse de la base de données</div>
    <span class='badge-source {badge_class}'>{badge_label}</span>
    <span style='font-size:0.73rem; color:#484f58; margin-left:12px;'>
        {s_filt['annee_min']} – {s_filt['annee_max']} · {s_filt['n_mesures']:,} mesures{filter_note}
    </span>
</div>
""".replace(',', '\u202f'), unsafe_allow_html=True)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
render_kpis(s_filt, sel_palette, sel_theme, fsize, fmt_params, fig_w_px_export, badge_label, s_filt['annee_min'], s_filt['annee_max'], uploaded.name)

if support_filter:
    st.markdown(f"""
    <div class='info-banner' style='margin-top:8px; border-left-color:#d29922;'>
    🔽 Filtre actif — Support(s) : <b>{', '.join(support_filter)}</b>
    · Onglets 1 et 2 filtrés · Onglets 3 et 4 sur la totalité des données
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Temporalité",
    "📍  Stations & Hétérogénéité",
    "🔬  Paramètres & Supports",
    "✅  Qualité & Producteurs",
])

# ── TAB 1 : Temporalité ──────────────────────
with tab1:
    if support_filter:
        st.markdown(f"<div class='filter-box'>🔽 Support(s) filtrés : <b>{', '.join(support_filter)}</b></div>",
                    unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Évolution temporelle</div>", unsafe_allow_html=True)
    fig_t = fig_timeline(s_filt, sel_palette, sel_theme, fsize, fig_h_base, fmt_params)
    if fig_t:
        try:
            st.plotly_chart(fig_t, use_container_width=True)
        except Exception as e:
            st.warning(f'⚠️ Impossible d\'afficher ce graphique : {e}')

    st.markdown("<div class='section-header'>Couverture par station</div>", unsafe_allow_html=True)
    fig_hm = fig_heatmap_stations(df_filt, s_filt, fmt, sel_palette, sel_theme, fsize, fig_h_base, fmt_params)
    if fig_hm:
        try:
            st.plotly_chart(fig_hm, use_container_width=True)
        except Exception as e:
            st.warning(f'⚠️ Impossible d\'afficher la heatmap : {e}')
    else:
        st.info("Données insuffisantes pour la heatmap.")

# ── TAB 2 : Stations ─────────────────────────
with tab2:
    if support_filter:
        st.markdown(f"<div class='filter-box'>🔽 Support(s) filtrés : <b>{', '.join(support_filter)}</b></div>",
                    unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Hétérogénéité inter-stations</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-banner'>
    Chaque bulle = une station. <b>Taille</b> ∝ nb de mesures.
    Position : nb d'<b>années actives</b> (X) × nb de <b>paramètres uniques</b> (Y).
    </div>""", unsafe_allow_html=True)

    fig_het = fig_stations_heterogeneite(s_filt, sel_palette, sel_theme, fsize, fig_h_base, fmt_params)
    if fig_het:
        try:
            st.plotly_chart(fig_het, use_container_width=True)
        except Exception as e:
            st.warning(f'⚠️ Impossible d\'afficher ce graphique : {e}')

    st.markdown("<div class='section-header'>Inventaire des stations</div>", unsafe_allow_html=True)
    col_st_name = 'Station' if fmt == 'NAIADES' else 'Station (BSS)'
    df_st = pd.DataFrame({
        col_st_name: list(s_filt['mesures_par_station'].keys()),
        'Mesures':        list(s_filt['mesures_par_station'].values()),
        'Paramètres':     [s_filt['params_par_station'].get(k, 0) for k in s_filt['mesures_par_station']],
        'Années actives': [s_filt['annees_par_station'].get(k, 0) for k in s_filt['mesures_par_station']],
    })
    st.dataframe(df_st.reset_index(drop=True), use_container_width=True, height=340)

# ── TAB 3 : Paramètres & Supports ────────────
with tab3:
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("<div class='section-header'>Paramètres par support</div>", unsafe_allow_html=True)
        # Paramètres par support : filtré si filtre actif
        s_for_sup = s_filt if support_filter else s_full
        fig_sp = fig_supports_params(s_for_sup, sel_palette, sel_theme, fsize, fig_h_base, fmt_params)
        if fig_sp:
            try:
                st.plotly_chart(fig_sp, use_container_width=True)
            except Exception as e:
                st.warning(f'⚠️ {e}')
        # Fractions
        if s_full.get('fractions'):
            st.markdown("<div class='section-header' style='margin-top:14px;'>Fractions analysées</div>",
                        unsafe_allow_html=True)
            for f in s_full['fractions']:
                st.markdown(f"<div style='font-size:0.83rem;color:#8b949e;padding:2px 0;'>· {f}</div>",
                            unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='section-header'>Top paramètres</div>", unsafe_allow_html=True)
        if support_filter:
            st.markdown(
                f"<div class='filter-box'>🔽 Filtré — Support(s) : <b>{', '.join(support_filter)}</b></div>",
                unsafe_allow_html=True)
        n_top = st.slider("Nombre de paramètres", 10, 50, 20, key='top_params')
        # Utilise les données filtrées si un filtre support est actif
        df_for_params = df_filt if support_filter else df_full
        s_for_params  = s_filt  if support_filter else s_full
        fig_tp = fig_top_params(df_for_params, s_for_params, sel_palette, sel_theme, fsize, fig_h_base, fmt_params, n=n_top)
        try:
            st.plotly_chart(fig_tp, use_container_width=True)
        except Exception as e:
            st.warning(f'⚠️ {e}')

# ── TAB 4 : Qualité & Producteurs ────────────
with tab4:
    col_q, col_p = st.columns([1, 1])
    with col_q:
        st.markdown("<div class='section-header'>Qualification des données</div>", unsafe_allow_html=True)
        fig_qua = fig_qualite(s_full, sel_palette, sel_theme, fsize, fig_h_base)
        if fig_qua:
            try:
                st.plotly_chart(fig_qua, use_container_width=True)
            except Exception as e:
                st.warning(f'⚠️ {e}')

        if s_full.get('statut'):
            st.markdown("<div class='section-header'>Statut des analyses</div>", unsafe_allow_html=True)
            t = THEMES_EXPORT[sel_theme]
            for k, v in s_full['statut'].items():
                pct = (v / s_full['n_mesures'] * 100) if s_full.get('n_mesures', 0) > 0 else 0
                label = k[:55] + '…' if len(k) > 55 else k
                st.markdown(f"""
                <div style='margin-bottom:10px;'>
                    <div style='font-size:0.8rem;color:#8b949e;margin-bottom:3px;'>{label}</div>
                    <div style='background:#21262d;border-radius:4px;height:6px;'>
                        <div style='background:{sel_palette[0]};width:{pct:.1f}%;height:6px;border-radius:4px;'></div>
                    </div>
                    <div style='font-size:0.73rem;color:#484f58;margin-top:2px;'>{v:,} mesures ({pct:.1f}%)</div>
                </div>""".replace(',', '\u202f'), unsafe_allow_html=True)

    with col_p:
        st.markdown("<div class='section-header'>Producteurs de données</div>", unsafe_allow_html=True)
        fig_pr = fig_producteurs(s_full, sel_palette, sel_theme, fsize, fig_h_base, fmt_params)
        if fig_pr:
            try:
                st.plotly_chart(fig_pr, use_container_width=True)
            except Exception as e:
                st.warning(f'⚠️ {e}')

        if fmt == 'ADES' and s_full.get('types_point'):
            st.markdown("<div class='section-header'>Types de points de mesure</div>", unsafe_allow_html=True)
            for k, v in s_full['types_point'].items():
                pct = (v / s_full['n_mesures'] * 100) if s_full.get('n_mesures', 0) > 0 else 0
                st.markdown(f"""
                <div style='margin-bottom:10px;'>
                    <div style='font-size:0.8rem;color:#8b949e;margin-bottom:3px;'>{k}</div>
                    <div style='background:#21262d;border-radius:4px;height:6px;'>
                        <div style='background:{sel_palette[0]};width:{pct:.1f}%;height:6px;border-radius:4px;'></div>
                    </div>
                    <div style='font-size:0.73rem;color:#484f58;margin-top:2px;'>{v:,} ({pct:.1f}%)</div>
                </div>""".replace(',', '\u202f'), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='margin-top:40px;padding:16px 0;border-top:1px solid #21262d;
     text-align:center;font-size:0.7rem;color:#484f58;letter-spacing:0.04em;'>
DataScope · Exploration de données qualité des eaux · Naïades & ADES
</div>""", unsafe_allow_html=True)
