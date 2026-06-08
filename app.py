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

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fond général */
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #21262d;
}
section[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}

/* Masquer le bouton deploy, menu et footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
/* NE PAS masquer header — contient le bouton d'ouverture de la sidebar */

/* Titre principal */
.main-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: #e6edf3;
    letter-spacing: -0.5px;
    margin-bottom: 0;
    line-height: 1.1;
}
.main-subtitle {
    font-size: 0.95rem;
    color: #7d8590;
    font-weight: 300;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-top: 4px;
    margin-bottom: 0;
}
.badge-source {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 10px;
}
.badge-naiades { background: #1f4e79; color: #58a6ff; border: 1px solid #1f6feb; }
.badge-ades { background: #1e3a2e; color: #3fb950; border: 1px solid #2ea043; }
.badge-unknown { background: #2d2d2d; color: #8b949e; border: 1px solid #30363d; }

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(155px, 1fr));
    gap: 14px;
    margin: 24px 0 28px 0;
}
.kpi-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 18px 20px 16px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #388bfd; }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
}
.kpi-icon {
    font-size: 1.3rem;
    margin-bottom: 8px;
    opacity: 0.85;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.1rem;
    color: #e6edf3;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-label {
    font-size: 0.72rem;
    color: #7d8590;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-weight: 500;
}

/* Sections */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #e6edf3;
    margin: 36px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #21262d;
}

/* Qualité pill */
.qual-correct { color: #3fb950; font-weight: 600; }
.qual-incorrect { color: #f85149; font-weight: 600; }
.qual-uncertain { color: #d29922; font-weight: 600; }

/* Info banner */
.info-banner {
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 3px solid #388bfd;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.85rem;
    color: #8b949e;
    margin: 16px 0;
}

/* Plotly overrides */
.js-plotly-plot .plotly .modebar { background: transparent !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-bottom: 1px solid #21262d;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7d8590;
    border: none;
    padding: 10px 20px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 0.03em;
}
.stTabs [aria-selected="true"] {
    color: #58a6ff !important;
    background: transparent !important;
    border-bottom: 2px solid #388bfd !important;
}

/* Upload zone */
.uploadedFile {
    background: #161b22 !important;
    border: 1px dashed #30363d !important;
}

/* Selectbox / widgets */
.stSelectbox > div > div {
    background: #21262d !important;
    border-color: #30363d !important;
    color: #e6edf3 !important;
}

div[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 14px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#c9d1d9', size=12),
    xaxis=dict(gridcolor='#21262d', linecolor='#30363d', tickcolor='#30363d'),
    yaxis=dict(gridcolor='#21262d', linecolor='#30363d', tickcolor='#30363d'),
    margin=dict(l=20, r=20, t=40, b=20),
)
# Version sans xaxis/yaxis pour make_subplots et cas particuliers
PLOTLY_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#c9d1d9', size=12),
    margin=dict(l=20, r=20, t=40, b=20),
)
AXIS_STYLE = dict(gridcolor='#21262d', linecolor='#30363d', tickcolor='#30363d')

COLORS_NAIADES = ['#58a6ff', '#1f6feb', '#388bfd', '#79c0ff', '#a5d6ff', '#cae8ff']
COLORS_ADES    = ['#3fb950', '#238636', '#2ea043', '#56d364', '#7ee787', '#acf2bd']
COLORS_MIX     = ['#58a6ff', '#3fb950', '#d29922', '#f85149', '#bc8cff', '#79c0ff']

# ─────────────────────────────────────────────
# DÉTECTION FORMAT
# ─────────────────────────────────────────────
def detect_format(df):
    cols = [c.lower() for c in df.columns]
    if 'cdstationmesure' in ' '.join(cols) or 'lbsupport' in ' '.join(cols) or 'cdparametere' in ' '.join(cols):
        return 'NAIADES'
    if 'identifiant national bss' in ' '.join(cols) or 'bss' in ' '.join(cols):
        return 'ADES'
    return 'INCONNU'

# ─────────────────────────────────────────────
# PARSING NAIADES
# ─────────────────────────────────────────────
def parse_naiades(df):
    df = df.copy()
    # Dates (serial Excel)
    for col in ['DatePrel', 'DateAna']:
        if col in df.columns:
            df[col] = pd.to_datetime('1899-12-30') + pd.to_timedelta(pd.to_numeric(df[col], errors='coerce'), unit='D')
    df['année'] = df['DatePrel'].dt.year if 'DatePrel' in df.columns else np.nan
    df['mois']  = df['DatePrel'].dt.month if 'DatePrel' in df.columns else np.nan
    return df

def stats_naiades(df):
    s = {}
    s['source'] = 'NAIADES'
    s['n_mesures']   = len(df)
    s['n_stations']  = df['LbStationMesureEauxSurface'].nunique() if 'LbStationMesureEauxSurface' in df.columns else 0
    s['n_parametres']= df['LbLongParamètre'].nunique() if 'LbLongParamètre' in df.columns else 0
    s['n_campagnes'] = df['CdPrelevement'].nunique() if 'CdPrelevement' in df.columns else 0
    s['annee_min']   = int(df['année'].min()) if 'année' in df.columns else '?'
    s['annee_max']   = int(df['année'].max()) if 'année' in df.columns else '?'
    s['n_annees']    = df['année'].nunique() if 'année' in df.columns else 0
    s['n_supports']  = df['LbSupport'].nunique() if 'LbSupport' in df.columns else 0
    s['supports']    = df['LbSupport'].unique().tolist() if 'LbSupport' in df.columns else []
    s['n_fractions'] = df['LbFractionAnalysee'].nunique() if 'LbFractionAnalysee' in df.columns else 0
    s['fractions']   = df['LbFractionAnalysee'].unique().tolist() if 'LbFractionAnalysee' in df.columns else []
    s['qualif']      = df['LbQualAna'].value_counts().to_dict() if 'LbQualAna' in df.columns else {}
    s['statut']      = df['MnemoStatutAna'].value_counts().to_dict() if 'MnemoStatutAna' in df.columns else {}
    s['n_producteurs']= df['NomProducteur'].nunique() if 'NomProducteur' in df.columns else 0
    s['producteurs'] = df['NomProducteur'].value_counts().to_dict() if 'NomProducteur' in df.columns else {}
    s['params_par_support'] = df.groupby('LbSupport')['LbLongParamètre'].nunique().to_dict() if 'LbSupport' in df.columns else {}
    s['mesures_par_station'] = df.groupby('LbStationMesureEauxSurface').size().sort_values(ascending=False).to_dict() if 'LbStationMesureEauxSurface' in df.columns else {}
    s['params_par_station']  = df.groupby('LbStationMesureEauxSurface')['LbLongParamètre'].nunique().sort_values(ascending=False).to_dict() if 'LbStationMesureEauxSurface' in df.columns else {}
    s['annees_par_station']  = df.groupby('LbStationMesureEauxSurface')['année'].nunique().sort_values(ascending=False).to_dict() if 'LbStationMesureEauxSurface' in df.columns else {}
    s['campagnes_par_annee'] = df.groupby('année')['CdPrelevement'].nunique().to_dict() if 'CdPrelevement' in df.columns else {}
    s['mesures_par_annee']   = df.groupby('année').size().to_dict() if 'année' in df.columns else {}
    return s

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

def stats_ades(df):
    s = {}
    s['source'] = 'ADES'
    s['n_mesures']    = len(df)
    s['n_stations']   = df['Identifiant national BSS'].nunique() if 'Identifiant national BSS' in df.columns else 0
    s['n_parametres'] = df['Paramètre'].nunique() if 'Paramètre' in df.columns else 0
    s['n_campagnes']  = df["Numéro de prélèvement"].nunique() if "Numéro de prélèvement" in df.columns else 0
    s['annee_min']    = int(df['année'].min()) if 'année' in df.columns else '?'
    s['annee_max']    = int(df['année'].max()) if 'année' in df.columns else '?'
    s['n_annees']     = df['année'].nunique() if 'année' in df.columns else 0
    s['n_supports']   = df['Support'].nunique() if 'Support' in df.columns else 0
    s['supports']     = df['Support'].unique().tolist() if 'Support' in df.columns else []
    s['n_fractions']  = df['Fraction analysée'].nunique() if 'Fraction analysée' in df.columns else 0
    s['fractions']    = df['Fraction analysée'].unique().tolist() if 'Fraction analysée' in df.columns else []
    s['qualif']       = df['Qualification'].value_counts().to_dict() if 'Qualification' in df.columns else {}
    s['statut']       = df['Statut mesure'].value_counts().to_dict() if 'Statut mesure' in df.columns else {}
    s['n_producteurs']= df['Producteur données'].nunique() if 'Producteur données' in df.columns else 0
    s['producteurs']  = df['Producteur données'].value_counts().to_dict() if 'Producteur données' in df.columns else {}
    s['types_point']  = df['Type qualitomètre'].value_counts().to_dict() if 'Type qualitomètre' in df.columns else {}
    s['mesures_par_station'] = df.groupby('Identifiant national BSS').size().sort_values(ascending=False).to_dict() if 'Identifiant national BSS' in df.columns else {}
    s['params_par_station']  = df.groupby('Identifiant national BSS')['Paramètre'].nunique().sort_values(ascending=False).to_dict() if 'Identifiant national BSS' in df.columns else {}
    s['annees_par_station']  = df.groupby('Identifiant national BSS')['année'].nunique().sort_values(ascending=False).to_dict() if 'Identifiant national BSS' in df.columns else {}
    s['campagnes_par_annee'] = df.groupby('année')["Numéro de prélèvement"].nunique().to_dict() if 'Numéro de prélèvement' in df.columns else {}
    s['mesures_par_annee']   = df.groupby('année').size().to_dict() if 'année' in df.columns else {}
    return s

# ─────────────────────────────────────────────
# COMPOSANTS GRAPHIQUES
# ─────────────────────────────────────────────
def render_kpis(s, colors):
    accent = colors[0]
    items = [
        ("📍", s.get('n_stations', 0), "Stations"),
        ("🔬", s.get('n_parametres', 0), "Paramètres"),
        ("📋", s.get('n_campagnes', 0), "Campagnes"),
        ("📅", s.get('n_annees', 0), "Années"),
        ("📊", f"{s.get('n_mesures', 0):,}".replace(',', '\u202f'), "Mesures"),
        ("🧪", s.get('n_supports', 0), "Supports"),
    ]
    cols = st.columns(len(items))
    for col, (icon, val, label) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent: {accent}">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{label}</div>
            </div>""", unsafe_allow_html=True)

def fig_timeline(s, colors):
    if not s.get('mesures_par_annee'):
        return None
    ann = sorted(s['mesures_par_annee'].keys())
    mes = [s['mesures_par_annee'][a] for a in ann]
    camp = [s.get('campagnes_par_annee', {}).get(a, 0) for a in ann]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=ann, y=mes, name="Mesures", marker_color=colors[0],
        opacity=0.8, marker_line_width=0,
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=ann, y=camp, name="Campagnes", line=dict(color=colors[2], width=2.5),
        mode='lines+markers', marker=dict(size=5),
    ), secondary_y=True)
    # make_subplots: ne pas passer xaxis/yaxis via **PLOTLY_LAYOUT, les gérer via update_xaxes/update_yaxes
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#c9d1d9', size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(text="Évolution temporelle", font=dict(size=14, color='#e6edf3'), x=0),
        legend=dict(orientation='h', y=1.08, bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
        height=280,
        barmode='overlay',
    )
    fig.update_xaxes(gridcolor='#21262d', linecolor='#30363d', tickcolor='#30363d', dtick=5)
    fig.update_yaxes(title_text="Nb mesures", secondary_y=False,
                     gridcolor='#21262d', linecolor='#30363d', color='#7d8590', title_font_size=11)
    fig.update_yaxes(title_text="Nb campagnes", secondary_y=True,
                     gridcolor='rgba(0,0,0,0)', linecolor='#30363d', color='#7d8590', title_font_size=11)
    return fig

def fig_stations_heterogeneite(s, colors, source):
    if source == 'NAIADES':
        col_station = 'LbStationMesureEauxSurface'
        stations = list(s.get('mesures_par_station', {}).keys())[:20]
    else:
        col_station = 'Identifiant national BSS'
        stations = list(s.get('mesures_par_station', {}).keys())[:20]

    mesures  = [s.get('mesures_par_station', {}).get(st, 0) for st in stations]
    params   = [s.get('params_par_station', {}).get(st, 0) for st in stations]
    annees   = [s.get('annees_par_station', {}).get(st, 0) for st in stations]

    # Bubble chart
    fig = go.Figure(go.Scatter(
        x=annees, y=params,
        mode='markers+text',
        marker=dict(
            size=[m/max(mesures)*60+8 for m in mesures],
            color=mesures, colorscale=[[0, '#21262d'], [1, colors[0]]],
            showscale=True,
            colorbar=dict(title="Mesures", thickness=12, len=0.7,
                          tickfont=dict(color='#7d8590', size=10),
                          title_font=dict(color='#7d8590', size=10)),
            line=dict(color=colors[0], width=1),
        ),
        text=[st.split(' ')[-1] if len(st) > 20 else st for st in stations],
        textposition='top center',
        textfont=dict(size=9, color='#8b949e'),
        hovertemplate='<b>%{customdata}</b><br>Années: %{x}<br>Paramètres: %{y}<extra></extra>',
        customdata=stations,
    ))
    fig.update_layout(
        **PLOTLY_BASE,
        title=dict(text="Hétérogénéité inter-stations (taille = nb mesures)", font=dict(size=14, color='#e6edf3'), x=0),
        height=380,
    )
    fig.update_xaxes(**AXIS_STYLE, title='Années actives')
    fig.update_yaxes(**AXIS_STYLE, title='Paramètres uniques')
    return fig

def fig_supports_params(s, colors):
    data = s.get('params_par_support', {})
    if not data:
        return None
    labels = list(data.keys())
    values = list(data.values())
    fig = go.Figure(go.Bar(
        y=labels, x=values,
        orientation='h',
        marker=dict(
            color=values,
            colorscale=[[0, colors[1]], [1, colors[0]]],
            line=dict(width=0),
        ),
        text=[f" {v}" for v in values],
        textfont=dict(color='#c9d1d9', size=11),
        textposition='outside',
    ))
    fig.update_layout(
        **PLOTLY_BASE,
        title=dict(text="Paramètres par support", font=dict(size=14, color='#e6edf3'), x=0),
        height=max(200, len(labels)*55),
    )
    fig.update_xaxes(**AXIS_STYLE, title='Nb paramètres uniques')
    fig.update_yaxes(**AXIS_STYLE, categoryorder='total ascending')
    return fig

def fig_qualite(s, colors):
    qualif = s.get('qualif', {})
    if not qualif:
        return None
    labels = list(qualif.keys())
    values = list(qualif.values())
    color_map = {
        'Correcte': '#3fb950', 'Correct': '#3fb950',
        'Incorrecte': '#f85149', 'non définissable': '#7d8590',
        'Incertaine': '#d29922',
    }
    colors_q = [color_map.get(l, colors[2]) for l in labels]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=colors_q, line=dict(color='#0d1117', width=2)),
        hole=0.55,
        textinfo='label+percent',
        textfont=dict(size=11, color='#c9d1d9'),
        insidetextorientation='auto',
    ))
    total = sum(values)
    fig.add_annotation(text=f"<b>{total:,}</b>".replace(',', '\u202f'),
                       font=dict(size=18, color='#e6edf3', family='DM Serif Display'),
                       showarrow=False, x=0.5, y=0.5)
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Qualification des données", font=dict(size=14, color='#e6edf3'), x=0),
        showlegend=True,
        legend=dict(font=dict(size=10, color='#8b949e'), bgcolor='rgba(0,0,0,0)', x=1.02),
        height=260,
    )
    return fig

def fig_producteurs(s, colors):
    prod = s.get('producteurs', {})
    if not prod:
        return None
    labels = list(prod.keys())
    short_labels = [k[:42]+'…' if len(k) > 42 else k for k in labels]
    values = list(prod.values())
    fig = go.Figure(go.Bar(
        x=short_labels, y=values,
        marker=dict(color=colors[:len(labels)], line=dict(width=0)),
        text=values, textfont=dict(color='#c9d1d9', size=11), textposition='outside',
    ))
    fig.update_layout(
        **PLOTLY_BASE,
        title=dict(text="Répartition par producteur", font=dict(size=14, color='#e6edf3'), x=0),
        height=260,
    )
    fig.update_xaxes(**AXIS_STYLE, tickangle=-25)
    fig.update_yaxes(**AXIS_STYLE, title='Mesures')
    return fig

def fig_heatmap_stations(df, s, source):
    """Heatmap stations × années (nb mesures)."""
    try:
        if source == 'NAIADES':
            col_st = 'LbStationMesureEauxSurface'
        else:
            col_st = 'Identifiant national BSS'
        pivot = df.groupby([col_st, 'année']).size().unstack(fill_value=0)
        # Top 20 stations
        top = pivot.sum(axis=1).nlargest(20).index
        pivot = pivot.loc[top]
        fig = px.imshow(
            pivot,
            color_continuous_scale=[[0,'#161b22'],[0.01,'#1f2937'],[0.3, '#1f6feb'],[1,'#58a6ff']],
            aspect='auto',
            labels=dict(x='Année', y='Station', color='Mesures'),
        )
        fig.update_layout(
            **PLOTLY_BASE,
            title=dict(text="Couverture temporelle par station (Top 20)", font=dict(size=14, color='#e6edf3'), x=0),
            height=480,
            coloraxis_colorbar=dict(
                title="Mesures", thickness=12, len=0.7,
                tickfont=dict(color='#7d8590', size=10),
                title_font=dict(color='#7d8590', size=10),
            ),
        )
        fig.update_xaxes(**AXIS_STYLE, title='', dtick=5)
        fig.update_yaxes(**AXIS_STYLE, title='', tickfont=dict(size=9))
        return fig
    except Exception as e:
        return None

def fig_top_params(df, source, colors, n=20):
    if source == 'NAIADES':
        col = 'LbLongParamètre'
        col_sup = 'LbSupport'
    else:
        col = 'Paramètre'
        col_sup = 'Support'
    top = df[col].value_counts().head(n)
    sups = df.groupby(col)[col_sup].first() if col_sup in df.columns else None
    fig = go.Figure(go.Bar(
        y=top.index.tolist(), x=top.values.tolist(),
        orientation='h',
        marker=dict(color=top.values.tolist(),
                    colorscale=[[0, colors[1]], [1, colors[0]]],
                    line=dict(width=0)),
        text=[f" {v:,}".replace(',', '\u202f') for v in top.values],
        textfont=dict(color='#c9d1d9', size=10), textposition='outside',
    ))
    fig.update_layout(
        **PLOTLY_BASE,
        title=dict(text=f"Top {n} paramètres les plus mesurés", font=dict(size=14, color='#e6edf3'), x=0),
        height=max(300, n*24),
    )
    fig.update_xaxes(**AXIS_STYLE, title='Nb mesures')
    fig.update_yaxes(**AXIS_STYLE, tickfont=dict(size=9), categoryorder='total ascending')
    return fig

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 10px 0 20px 0;'>
        <div style='font-family:"DM Serif Display",serif; font-size:1.4rem; color:#e6edf3;'>DataScope</div>
        <div style='font-size:0.7rem; color:#7d8590; letter-spacing:0.1em; text-transform:uppercase;'>Exploration de données</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Charger un fichier**")
    uploaded = st.file_uploader(
        "CSV — Naïades ou ADES",
        type=['csv'],
        help="Fichiers issus des bases Naïades (eaux de surface) ou ADES (eaux souterraines). Encodage latin-1 supporté."
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#484f58; line-height:1.6;'>
    Formats supportés<br>
    <span style='color:#58a6ff;'>● Naïades</span> physico-chimie<br>
    <span style='color:#3fb950;'>● ADES</span> eaux souterraines<br><br>
    Le format est détecté automatiquement.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LANDING / ACCUEIL
# ─────────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div style='padding: 20px 0 8px 0;'>
        <div class='main-title'>Exploration<br>de la donnée</div>
        <div class='main-subtitle'>Naïades · ADES · Qualité des eaux</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-banner'>
    👈 <b>Ouvrez le panneau latéral gauche</b> (flèche <code>&gt;</code> en haut à gauche si fermé)
    pour charger votre fichier CSV Naïades ou ADES.<br><br>
    Le tableau de bord s'affiche automatiquement : stations, paramètres, supports, campagnes,
    couverture temporelle et qualité de la donnée.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='kpi-card' style='--accent:#58a6ff; margin-bottom:14px;'>
            <div class='kpi-icon'>🏞️</div>
            <div style='font-family:"DM Serif Display",serif; font-size:1.1rem; color:#e6edf3; margin-bottom:6px;'>Naïades</div>
            <div style='font-size:0.8rem; color:#7d8590; line-height:1.5;'>
            Eaux de surface · Physico-chimie<br>
            Supports : eau, sédiments, biotes<br>
            Colonnes : CdStation, LbSupport, DatePrel…
            </div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='kpi-card' style='--accent:#3fb950; margin-bottom:14px;'>
            <div class='kpi-icon'>💧</div>
            <div style='font-family:"DM Serif Display",serif; font-size:1.1rem; color:#e6edf3; margin-bottom:6px;'>ADES</div>
            <div style='font-size:0.8rem; color:#7d8590; line-height:1.5;'>
            Eaux souterraines · BSS<br>
            Supports : eau, air brut<br>
            Colonnes : Identifiant BSS, Paramètre…
            </div>
        </div>""", unsafe_allow_html=True)

    st.stop()

# ─────────────────────────────────────────────
# CHARGEMENT
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(file_bytes, filename):
    encodings = ['latin1', 'utf-8', 'cp1252']
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
            head_str = head.decode(enc, errors='replace')
            first_line = head_str.split('\n')[0]
            sep_counts = {s: first_line.count(s) for s in separators}
            best_sep = max(sep_counts, key=sep_counts.get)
        except Exception:
            best_sep = ','
        for sep in ([best_sep] + [s for s in separators if s != best_sep]):
            try:
                df = pd.read_csv(
                    io.BytesIO(file_bytes),
                    sep=sep,
                    encoding=enc,
                    low_memory=False,
                    on_bad_lines='skip',
                )
                if df.shape[1] >= 3:
                    return df, enc, sep
            except Exception:
                continue
    return None, None, None

with st.spinner("Chargement du fichier… (patientez pour les fichiers volumineux)"):
    file_bytes = uploaded.read()
    df_raw, detected_enc, detected_sep = load_data(file_bytes, uploaded.name)

if df_raw is None:
    st.error("❌ Impossible de lire le fichier.")
    st.markdown("""
**Causes possibles :**
- Fichier corrompu ou incomplet
- Format non CSV (Excel .xlsx → enregistrer en CSV depuis Excel d'abord)
- Encodage inhabituel

**Solution rapide :** ouvre le fichier dans Excel → *Enregistrer sous* → CSV UTF-8, puis recharge.
    """)
    st.stop()
else:
    st.sidebar.markdown(f"""
    <div style='font-size:0.7rem; color:#484f58; margin-top:8px;'>
    ✓ Encodage : <code style='color:#58a6ff'>{detected_enc}</code><br>
    ✓ Séparateur : <code style='color:#58a6ff'>{repr(detected_sep)}</code><br>
    ✓ {len(df_raw):,} lignes · {df_raw.shape[1]} colonnes
    </div>""".replace(',', '\u202f'), unsafe_allow_html=True)

fmt = detect_format(df_raw)

if fmt == 'NAIADES':
    df = parse_naiades(df_raw)
    s  = stats_naiades(df)
    colors = COLORS_NAIADES
    badge_class = 'badge-naiades'
    badge_label = 'Naïades — Eaux de surface'
elif fmt == 'ADES':
    df = parse_ades(df_raw)
    s  = stats_ades(df)
    colors = COLORS_ADES
    badge_class = 'badge-ades'
    badge_label = 'ADES — Eaux souterraines'
else:
    st.warning("Format non reconnu automatiquement. Vérifiez la structure du fichier.")
    st.dataframe(df_raw.head(3))
    st.stop()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style='padding: 10px 0 0 0;'>
    <div class='main-title'>{uploaded.name.replace('.csv','').replace('_',' ')}</div>
    <div class='main-subtitle'>Exploration · Synthèse de la base de données</div>
    <span class='badge-source {badge_class}'>{badge_label}</span>
    <span style='font-size:0.75rem; color:#484f58; margin-left:14px;'>
        {s['annee_min']} – {s['annee_max']} · {s['n_mesures']:,} mesures
    </span>
</div>
""".replace(',', '\u202f'), unsafe_allow_html=True)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# KPIs
render_kpis(s, colors)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Temporalité",
    "📍  Stations & Hétérogénéité",
    "🔬  Paramètres & Supports",
    "✅  Qualité & Producteurs",
])

# ── TAB 1 : Temporalité ──
with tab1:
    st.markdown("<div class='section-header'>Évolution temporelle</div>", unsafe_allow_html=True)
    fig_t = fig_timeline(s, colors)
    if fig_t:
        st.plotly_chart(fig_t, use_container_width=True)

    st.markdown("<div class='section-header'>Couverture par station</div>", unsafe_allow_html=True)
    fig_hm = fig_heatmap_stations(df, s, fmt)
    if fig_hm:
        st.plotly_chart(fig_hm, use_container_width=True)
    else:
        st.info("Données insuffisantes pour la heatmap.")

# ── TAB 2 : Stations ──
with tab2:
    st.markdown("<div class='section-header'>Hétérogénéité inter-stations</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-banner'>
    Chaque bulle représente une station. La <b>taille</b> est proportionnelle au nombre de mesures,
    la position reflète le nombre d'<b>années actives</b> (X) et de <b>paramètres uniques</b> (Y).
    </div>""", unsafe_allow_html=True)
    fig_het = fig_stations_heterogeneite(s, colors, fmt)
    if fig_het:
        st.plotly_chart(fig_het, use_container_width=True)

    # Tableau récap stations
    st.markdown("<div class='section-header'>Inventaire des stations</div>", unsafe_allow_html=True)
    if fmt == 'NAIADES':
        df_st = pd.DataFrame({
            'Station': list(s['mesures_par_station'].keys()),
            'Mesures': list(s['mesures_par_station'].values()),
            'Paramètres': [s['params_par_station'].get(k, 0) for k in s['mesures_par_station'].keys()],
            'Années actives': [s['annees_par_station'].get(k, 0) for k in s['mesures_par_station'].keys()],
        })
    else:
        df_st = pd.DataFrame({
            'Station (BSS)': list(s['mesures_par_station'].keys()),
            'Mesures': list(s['mesures_par_station'].values()),
            'Paramètres': [s['params_par_station'].get(k, 0) for k in s['mesures_par_station'].keys()],
            'Années actives': [s['annees_par_station'].get(k, 0) for k in s['mesures_par_station'].keys()],
        })
    st.dataframe(df_st.reset_index(drop=True), use_container_width=True, height=380)

# ── TAB 3 : Paramètres & Supports ──
with tab3:
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("<div class='section-header'>Supports & fractions</div>", unsafe_allow_html=True)
        if fmt == 'NAIADES':
            fig_sp = fig_supports_params(s, colors)
            if fig_sp:
                st.plotly_chart(fig_sp, use_container_width=True)
        else:
            st.markdown(f"""
            <div class='kpi-card' style='--accent:{colors[0]};'>
            <div class='kpi-label'>Supports</div>
            <div style='margin-top:10px; font-size:0.9rem; color:#c9d1d9;'>
            {'<br>'.join(['· ' + s for s in s.get('supports', [])])}
            </div>
            <br>
            <div class='kpi-label'>Fractions analysées</div>
            <div style='margin-top:10px; font-size:0.85rem; color:#8b949e;'>
            {'<br>'.join(['· ' + f for f in s.get('fractions', [])])}
            </div>
            </div>""", unsafe_allow_html=True)
        # Fractions (Naïades)
        if fmt == 'NAIADES' and s.get('fractions'):
            st.markdown("<div class='section-header' style='margin-top:20px;'>Fractions analysées</div>", unsafe_allow_html=True)
            for f in s['fractions']:
                st.markdown(f"<div style='font-size:0.85rem; color:#8b949e; padding:3px 0;'>· {f}</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='section-header'>Top paramètres</div>", unsafe_allow_html=True)
        n_top = st.slider("Nombre de paramètres", 10, 40, 20, key='top_params')
        fig_tp = fig_top_params(df, fmt, colors, n=n_top)
        st.plotly_chart(fig_tp, use_container_width=True)

# ── TAB 4 : Qualité ──
with tab4:
    col_q, col_p = st.columns([1, 1])
    with col_q:
        st.markdown("<div class='section-header'>Qualification des données</div>", unsafe_allow_html=True)
        fig_qua = fig_qualite(s, colors)
        if fig_qua:
            st.plotly_chart(fig_qua, use_container_width=True)
        # Statuts
        if s.get('statut'):
            st.markdown("<div class='section-header'>Statut des analyses</div>", unsafe_allow_html=True)
            for k, v in s['statut'].items():
                pct = v / s['n_mesures'] * 100
                label = k[:50] + '…' if len(k) > 50 else k
                st.markdown(f"""
                <div style='margin-bottom:8px;'>
                    <div style='font-size:0.8rem; color:#8b949e; margin-bottom:3px;'>{label}</div>
                    <div style='background:#21262d; border-radius:4px; height:6px;'>
                        <div style='background:{colors[0]}; width:{pct:.1f}%; height:6px; border-radius:4px;'></div>
                    </div>
                    <div style='font-size:0.75rem; color:#484f58; margin-top:2px;'>{v:,} mesures ({pct:.1f}%)</div>
                </div>""".replace(',', '\u202f'), unsafe_allow_html=True)

    with col_p:
        st.markdown("<div class='section-header'>Producteurs de données</div>", unsafe_allow_html=True)
        fig_pr = fig_producteurs(s, colors)
        if fig_pr:
            st.plotly_chart(fig_pr, use_container_width=True)
        if fmt == 'ADES' and s.get('types_point'):
            st.markdown("<div class='section-header'>Types de points de mesure</div>", unsafe_allow_html=True)
            for k, v in s['types_point'].items():
                pct = v / s['n_mesures'] * 100
                st.markdown(f"""
                <div style='margin-bottom:8px;'>
                    <div style='font-size:0.8rem; color:#8b949e; margin-bottom:3px;'>{k}</div>
                    <div style='background:#21262d; border-radius:4px; height:6px;'>
                        <div style='background:{colors[0]}; width:{pct:.1f}%; height:6px; border-radius:4px;'></div>
                    </div>
                    <div style='font-size:0.75rem; color:#484f58; margin-top:2px;'>{v:,} ({pct:.1f}%)</div>
                </div>""".replace(',', '\u202f'), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='margin-top:48px; padding:20px 0; border-top:1px solid #21262d; text-align:center;
     font-size:0.72rem; color:#484f58; letter-spacing:0.04em;'>
DataScope · Exploration de données qualité des eaux · Naïades & ADES
</div>""", unsafe_allow_html=True)
