import math
import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Blast Cost Estimator", layout="wide", page_icon="💣")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400;1,600;1,700&family=Lora:ital,wght@0,400;0,600;1,400;1,600&family=DM+Mono:ital,wght@0,300;0,400;1,300;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,600;1,300;1,400;1,600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #EEE9E0 !important;
    color: #1A1A18 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer { visibility: hidden; }

[data-testid="stAppViewContainer"] > .main > .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ═══════════════════════════
   MASTHEAD
═══════════════════════════ */
.masthead {
    background: #1A2E1A;
    padding: 52px 72px 44px;
    position: relative;
    overflow: hidden;
}
.masthead::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        90deg,
        transparent, transparent 80px,
        rgba(255,255,255,0.012) 80px,
        rgba(255,255,255,0.012) 81px
    );
    pointer-events: none;
}
.masthead::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #C0392B 0%, #E05A3A 40%, transparent 100%);
}
.mh-eyebrow {
    font-family: 'DM Mono', monospace;
    font-style: italic;
    font-size: 10px;
    letter-spacing: 6px;
    color: #6B9E6B;
    text-transform: uppercase;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.mh-eyebrow::before {
    content: '';
    display: inline-block;
    width: 28px; height: 1px;
    background: #6B9E6B;
}
.mh-title {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 700;
    font-size: 58px;
    color: #EEE9E0;
    line-height: 1.0;
    letter-spacing: -1.5px;
    margin-bottom: 12px;
}
.mh-title em { color: #C0392B; font-style: italic; }
.mh-desc {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 300;
    font-size: 16px;
    color: #5A7A5A;
    letter-spacing: 2px;
    margin-top: 6px;
}

/* ═══════════════════════════
   SECTION RULE
═══════════════════════════ */
.sec-rule {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 0 0 28px 0;
}
.sec-rule-icon { font-size: 16px; line-height: 1; }
.sec-rule-txt {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 6px;
    color: #1A2E1A;
    text-transform: uppercase;
}
.sec-rule-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, #1A2E1A 0%, transparent 100%);
    opacity: 0.18;
}

/* ═══════════════════════════
   INPUT CARDS
═══════════════════════════ */
.inp-card {
    background: #F8F4EE;
    border-radius: 3px;
    padding: 16px 20px 8px;
    margin-bottom: 14px;
    border-top: 3px solid #1A2E1A;
    transition: box-shadow 0.2s, transform 0.2s;
}
.inp-card:hover {
    box-shadow: 4px 4px 0 #D4CECC;
    transform: translateY(-1px);
}
.inp-card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}
.inp-card-icon { font-size: 13px; opacity: 0.85; }
.inp-card-label {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 11px;
    font-weight: 600;
    color: #1A2E1A;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ═══════════════════════════
   STREAMLIT INPUT OVERRIDES
═══════════════════════════ */
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid #B8B0A8 !important;
    border-radius: 0 !important;
    color: #1A1A18 !important;
    font-family: 'DM Mono', monospace !important;
    font-style: italic !important;
    font-size: 22px !important;
    font-weight: 300 !important;
    padding: 4px 2px 8px !important;
    letter-spacing: 0.5px !important;
    box-shadow: none !important;
    outline: none !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-bottom-color: #C0392B !important;
    box-shadow: 0 2px 0 0 rgba(192,57,43,0.12) !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #C0B8B0 !important;
    font-size: 13px !important;
    font-style: italic !important;
}
[data-testid="stTextInput"] label { display: none !important; }
[data-testid="stTextInput"] > div,
[data-testid="stTextInput"] > div > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* ═══════════════════════════
   CALCULATE BUTTON — pill
═══════════════════════════ */
.stButton > button {
    background: #C0392B !important;
    color: #F8F4EE !important;
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    font-weight: 700 !important;
    font-size: 17px !important;
    letter-spacing: 1.5px !important;
    border: none !important;
    border-radius: 9999px !important;
    padding: 18px 56px !important;
    width: 100% !important;
    margin-top: 24px !important;
    cursor: pointer !important;
    box-shadow: 0 6px 20px rgba(192,57,43,0.28) !important;
    transition: background 0.2s, box-shadow 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    background: #A93226 !important;
    box-shadow: 0 10px 28px rgba(192,57,43,0.38) !important;
    transform: translateY(-2px) !important;
}

/* ═══════════════════════════
   RESULTS HEADER BAND
═══════════════════════════ */
.res-band {
    background: #1A2E1A;
    padding: 16px 24px;
    border-radius: 4px 4px 0 0;
    display: flex;
    align-items: center;
    gap: 12px;
}
.res-band-txt {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 300;
    font-size: 11px;
    letter-spacing: 6px;
    color: #6B9E6B;
    text-transform: uppercase;
}

/* ═══════════════════════════
   DATAFRAME CONTAINER WRAP
═══════════════════════════ */
.df-wrap {
    border: 1px solid #D4CECC;
    border-top: none;
    border-radius: 0;
    overflow: hidden;
    background: #F8F4EE;
}

/* ═══════════════════════════
   COST STRIP
═══════════════════════════ */
.cost-strip {
    background: #C0392B;
    padding: 26px 30px;
    border-radius: 0 0 4px 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
}
.cost-lhs-label {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 300;
    font-size: 11px;
    letter-spacing: 5px;
    color: rgba(238,233,224,0.65);
    text-transform: uppercase;
    margin-bottom: 5px;
}
.cost-lhs-note {
    font-family: 'DM Mono', monospace;
    font-style: italic;
    font-size: 11px;
    color: rgba(238,233,224,0.45);
    letter-spacing: 1px;
}
.cost-figure {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 700;
    font-size: 50px;
    color: #EEE9E0;
    line-height: 1;
    letter-spacing: -2px;
    text-shadow: 0 2px 16px rgba(0,0,0,0.2);
}

/* ═══════════════════════════
   COPY HINT + TIMESTAMP
═══════════════════════════ */
.copy-hint {
    font-family: 'DM Mono', monospace;
    font-style: italic;
    font-size: 9px;
    letter-spacing: 3px;
    color: #A09888;
    text-transform: uppercase;
    text-align: right;
    margin-bottom: 6px;
}
.ts-line {
    font-family: 'DM Mono', monospace;
    font-style: italic;
    font-size: 9px;
    letter-spacing: 3px;
    color: #8A8078;
    text-align: right;
    margin-top: 10px;
    text-transform: uppercase;
}

/* ═══════════════════════════
   ERROR
═══════════════════════════ */
.err-shell {
    background: #FDF0EE;
    border: 1px solid #E8C0BC;
    border-left: 5px solid #C0392B;
    border-radius: 3px;
    padding: 18px 24px;
    margin-top: 18px;
}
.err-item {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 13px;
    color: #C0392B;
    line-height: 2.4;
}
</style>
""", unsafe_allow_html=True)


# ── BACKEND ──────────────────────────────────────────────────

def run_design(bench_height, hole_diameter, rock_density,
               explosive_density, unit_cost, area):
    burden    = 25 * hole_diameter * (1 / rock_density)
    spacing   = 1.25 * burden
    holes     = max(1, int(area / (burden * spacing)))
    radius    = hole_diameter / 2
    charge    = math.pi * (radius ** 2) * bench_height * explosive_density
    total_exp = charge * holes
    rock_vol  = area * bench_height
    pf        = total_exp / rock_vol
    cost      = total_exp * unit_cost
    return dict(burden=burden, spacing=spacing, holes=holes, charge=charge,
                total_exp=total_exp, rock_vol=rock_vol, pf=pf, cost=cost)


# ── MASTHEAD ─────────────────────────────────────────────────

st.markdown("""
<div class="masthead">
    <div class="mh-eyebrow">💣 &nbsp; Open-Pit Mining</div>
    <div class="mh-title">Blast Design &amp;<br><em>Cost Estimation</em></div>
    <div class="mh-desc">Drill &amp; Blast Engineering &nbsp;·&nbsp; Bench Analysis Tool</div>
</div>
""", unsafe_allow_html=True)


# ── INPUTS ───────────────────────────────────────────────────

st.markdown("""
<div style="padding: 44px 72px 0;">
    <div class="sec-rule">
        <span class="sec-rule-icon">⚙️</span>
        <span class="sec-rule-txt">Input Parameters</span>
        <span class="sec-rule-line"></span>
    </div>
</div>
""", unsafe_allow_html=True)

col_l, col_r = st.columns([1, 20])   # left spacer
with col_r:
    pad_l, c1, c2, c3, pad_r = st.columns([1, 6, 6, 6, 1])

    with c1:
        st.markdown('<div class="inp-card"><div class="inp-card-header"><span class="inp-card-icon">📏</span><span class="inp-card-label">Bench Height (m)</span></div></div>', unsafe_allow_html=True)
        t_bench = st.text_input("bh", value="10.0", placeholder="e.g. 10.0", label_visibility="hidden", key="bench")

        st.markdown('<div class="inp-card"><div class="inp-card-header"><span class="inp-card-icon">🕳️</span><span class="inp-card-label">Hole Diameter (m)</span></div></div>', unsafe_allow_html=True)
        t_hole = st.text_input("hd", value="0.115", placeholder="e.g. 0.115", label_visibility="hidden", key="hole")

    with c2:
        st.markdown('<div class="inp-card"><div class="inp-card-header"><span class="inp-card-icon">🪨</span><span class="inp-card-label">Rock Density (t/m³)</span></div></div>', unsafe_allow_html=True)
        t_rock = st.text_input("rd", value="2.7", placeholder="e.g. 2.7", label_visibility="hidden", key="rock")

        st.markdown('<div class="inp-card"><div class="inp-card-header"><span class="inp-card-icon">💥</span><span class="inp-card-label">Explosive Density (t/m³)</span></div></div>', unsafe_allow_html=True)
        t_expden = st.text_input("ed", value="0.85", placeholder="e.g. 0.85", label_visibility="hidden", key="expden")

    with c3:
        st.markdown('<div class="inp-card"><div class="inp-card-header"><span class="inp-card-icon">📐</span><span class="inp-card-label">Bench Area (m²)</span></div></div>', unsafe_allow_html=True)
        t_area = st.text_input("ba", value="5000", placeholder="e.g. 5000", label_visibility="hidden", key="area")

        st.markdown('<div class="inp-card"><div class="inp-card-header"><span class="inp-card-icon">💰</span><span class="inp-card-label">Unit Cost ($/t)</span></div></div>', unsafe_allow_html=True)
        t_cost = st.text_input("uc", value="450", placeholder="e.g. 450", label_visibility="hidden", key="cost")


# ── BUTTON ───────────────────────────────────────────────────

_, btn_mid, _ = st.columns([3, 4, 3])
with btn_mid:
    st.markdown('<div style="padding: 0 20px;">', unsafe_allow_html=True)
    run = st.button("Estimate Cost")
    st.markdown('</div>', unsafe_allow_html=True)


# ── CALCULATE ────────────────────────────────────────────────

if run:
    errors = []

    def parse(val, name):
        try:
            v = float(val)
            if v <= 0:
                errors.append(f"{name} — must be greater than zero")
            return v
        except ValueError:
            errors.append(f"{name} — please enter a valid number")
            return None

    bench_height      = parse(t_bench,  "Bench Height")
    hole_diameter     = parse(t_hole,   "Hole Diameter")
    rock_density      = parse(t_rock,   "Rock Density")
    explosive_density = parse(t_expden, "Explosive Density")
    area              = parse(t_area,   "Bench Area")
    unit_cost         = parse(t_cost,   "Unit Cost")

    if errors:
        items = "".join(f'<div class="err-item">▶ &nbsp;{e}</div>' for e in errors)
        st.markdown(
            f'<div style="padding:0 72px;"><div class="err-shell">{items}</div></div>',
            unsafe_allow_html=True
        )
    else:
        res = run_design(bench_height, hole_diameter, rock_density,
                         explosive_density, unit_cost, area)
        st.session_state["res"] = res
        st.session_state["inp"] = dict(
            bench_height=bench_height, hole_diameter=hole_diameter,
            rock_density=rock_density, explosive_density=explosive_density,
            unit_cost=unit_cost, area=area
        )
        st.session_state["ts"] = datetime.now().strftime("%d %b %Y  —  %H:%M:%S")


# ── OUTPUTS ──────────────────────────────────────────────────

if "res" in st.session_state:
    res = st.session_state["res"]
    inp = st.session_state["inp"]
    ts  = st.session_state["ts"]

    st.markdown("""
    <div style="padding: 44px 72px 0;">
        <div class="sec-rule">
            <span class="sec-rule-icon">📊</span>
            <span class="sec-rule-txt">Results</span>
            <span class="sec-rule-line"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Header band above table
    st.markdown("""
    <div style="padding: 0 72px 0;">
        <div class="res-band">
            <span style="font-size:14px;">🔩</span>
            <span class="res-band-txt">Computed output — drill &amp; blast parameters</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Build DataFrame
    df = pd.DataFrame({
        "Parameter": [
            "Burden",
            "Hole Spacing",
            "Number of Drill Holes",
            "Charge per Hole",
            "Total Explosive",
            "Rock Volume",
            "Powder Factor",
        ],
        "Value": [
            f"{res['burden']:.3f}",
            f"{res['spacing']:.3f}",
            f"{res['holes']}",
            f"{res['charge']:.4f}",
            f"{res['total_exp']:.3f}",
            f"{res['rock_vol']:.2f}",
            f"{res['pf']:.4f}",
        ],
        "Unit": ["m", "m", "holes", "t", "t", "m³", "t/m³"]
    })

    # Copy hint
    st.markdown('<div style="padding: 0 72px;"><div class="copy-hint">click any cell · select all · ctrl+c to copy</div></div>',
                unsafe_allow_html=True)

    # Render the table inside padded container using columns
    _, tbl, _ = st.columns([1, 18, 1])
    with tbl:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=280,
            column_config={
                "Parameter": st.column_config.TextColumn("Parameter", width="large"),
                "Value":     st.column_config.TextColumn("Value",     width="medium"),
                "Unit":      st.column_config.TextColumn("Unit",      width="small"),
            }
        )

    # Cost strip
    st.markdown(f"""
    <div style="padding: 0 72px;">
        <div class="cost-strip">
            <div>
                <div class="cost-lhs-label">Total Blasting Cost — Bench Estimate</div>
                <div class="cost-lhs-note">
                    {res['total_exp']:.3f} t &nbsp;×&nbsp; ${inp['unit_cost']:.2f} per tonne
                </div>
            </div>
            <div class="cost-figure">${res['cost']:,.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="padding: 4px 72px;"><div class="ts-line">Calculated: {ts}</div></div>',
                unsafe_allow_html=True)

    st.markdown('<div style="height:64px;"></div>', unsafe_allow_html=True)
