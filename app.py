"""
BLAST DESIGN & COST ESTIMATION TOOL
Open-Pit Mining | Streamlit App
Author: abrazie
"""

import math
import streamlit as st
from datetime import datetime

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG  – must be first Streamlit call
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blast Design Tool",
    page_icon="💥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS  – blue + green palette, no yellow / gold
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

/* ── Root tokens ── */
:root {
    --bg-deep:      #04101C;
    --bg-panel:     #071A2B;
    --bg-card:      #0A2236;
    --border:       #0D3D5C;
    --accent-blue:  #12A3D8;
    --accent-green: #0FBF6A;
    --mid-blue:     #0A7FAD;
    --mid-green:    #0C9A56;
    --text-main:    #D6EEF8;
    --text-muted:   #4D7A99;
    --text-label:   #88BDD6;
    --mono:         'Share Tech Mono', monospace;
    --body:         'Exo 2', sans-serif;
}

/* ── App shell ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-deep) !important;
    color: var(--text-main) !important;
    font-family: var(--body);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-panel) !important;
    border-right: 1px solid var(--border);
}

/* ── Sidebar header ── */
.sidebar-brand {
    text-align: center;
    padding: 18px 0 10px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.sidebar-brand h1 {
    font-family: var(--mono);
    font-size: 15px;
    color: var(--accent-blue);
    letter-spacing: 3px;
    margin: 0;
    text-transform: uppercase;
}
.sidebar-brand p {
    font-size: 11px;
    color: var(--text-muted);
    margin: 4px 0 0;
    letter-spacing: 1px;
}

/* ── Section labels in sidebar ── */
.section-tag {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--accent-green);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 22px 0 8px;
    border-left: 3px solid var(--accent-green);
    padding-left: 8px;
}

/* ── Streamlit input overrides ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background-color: #040E19 !important;
    color: var(--accent-blue) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px rgba(18,163,216,0.15) !important;
}

label, .stLabel p {
    color: var(--text-label) !important;
    font-family: var(--body) !important;
    font-size: 13px !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--mid-blue), var(--mid-green)) !important;
    color: #fff !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 12px 0 !important;
    margin-top: 10px !important;
    transition: opacity 0.2s ease;
}
.stButton > button:hover { opacity: 0.85; }

/* ── Page title ── */
.app-title {
    font-family: var(--mono);
    font-size: 26px;
    color: var(--accent-blue);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin: 0;
    line-height: 1.2;
}
.app-subtitle {
    font-family: var(--body);
    font-size: 13px;
    color: var(--text-muted);
    letter-spacing: 2px;
    margin-top: 4px;
}
.title-bar {
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 28px;
}

/* ── Result card ── */
.result-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 22px 26px;
    margin-bottom: 16px;
}
.result-card-title {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent-green);
    margin-bottom: 18px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
}

/* ── Individual result row ── */
.r-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 7px 0;
    border-bottom: 1px solid #0A2030;
}
.r-row:last-child { border-bottom: none; }
.r-label {
    font-family: var(--body);
    font-size: 13px;
    color: var(--text-label);
}
.r-value {
    font-family: var(--mono);
    font-size: 15px;
    color: var(--text-main);
}
.r-unit {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
    margin-left: 6px;
}

/* ── Cost highlight ── */
.cost-block {
    background: linear-gradient(120deg, #062A3D, #063320);
    border: 1px solid var(--accent-green);
    border-radius: 8px;
    padding: 22px 26px;
    margin-bottom: 16px;
}
.cost-label {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--accent-green);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.cost-value {
    font-family: var(--mono);
    font-size: 36px;
    color: var(--accent-green);
    line-height: 1.1;
}
.cost-sub {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ── Info / warning strip ── */
.info-strip {
    background: #041728;
    border-left: 3px solid var(--accent-blue);
    padding: 10px 16px;
    border-radius: 0 4px 4px 0;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
    margin-bottom: 20px;
    letter-spacing: 1px;
}

/* ── Timestamp ── */
.timestamp {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-muted);
    text-align: right;
    margin-top: 10px;
    letter-spacing: 1px;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  BACKEND – pure calculation functions
# ─────────────────────────────────────────────────────────────

def calc_burden(diameter: float, rock_density: float) -> float:
    return 25 * diameter * (1 / rock_density)

def calc_spacing(burden: float) -> float:
    return 1.25 * burden

def calc_holes(area: float, burden: float, spacing: float) -> int:
    return max(1, int(area / (burden * spacing)))

def calc_charge_per_hole(diameter: float, bench_height: float,
                          explosive_density: float) -> float:
    radius = diameter / 2
    volume = math.pi * (radius ** 2) * bench_height
    return volume * explosive_density

def calc_powder_factor(total_explosive: float, rock_volume: float) -> float:
    return total_explosive / rock_volume

def calc_total_cost(total_explosive: float, unit_cost: float) -> float:
    return total_explosive * unit_cost

def run_design(bench_height, hole_diameter, rock_density,
               explosive_density, unit_cost, area):
    burden      = calc_burden(hole_diameter, rock_density)
    spacing     = calc_spacing(burden)
    holes       = calc_holes(area, burden, spacing)
    charge      = calc_charge_per_hole(hole_diameter, bench_height, explosive_density)
    total_exp   = charge * holes
    rock_vol    = area * bench_height
    pf          = calc_powder_factor(total_exp, rock_vol)
    cost        = calc_total_cost(total_exp, unit_cost)
    return dict(burden=burden, spacing=spacing, holes=holes, charge=charge,
                total_exp=total_exp, rock_vol=rock_vol, pf=pf, cost=cost)

def generate_report_text(inputs: dict, results: dict) -> str:
    ts = datetime.now().strftime("%d %B %Y   %H:%M:%S")
    lines = [
        "=" * 54,
        "   BLAST DESIGN & COST ESTIMATION REPORT",
        f"   {ts}",
        "=" * 54,
        "",
        "  ── INPUT PARAMETERS ──────────────────────────",
        f"  Bench Height          :  {inputs['bench_height']:.2f} m",
        f"  Hole Diameter         :  {inputs['hole_diameter']:.4f} m",
        f"  Rock Density          :  {inputs['rock_density']:.2f} t/m³",
        f"  Explosive Density     :  {inputs['explosive_density']:.2f} t/m³",
        f"  Bench Area            :  {inputs['area']:.2f} m²",
        f"  Explosive Unit Cost   :  ${inputs['unit_cost']:.2f} /t",
        "",
        "  ── DRILL & BLAST DESIGN ──────────────────────",
        f"  Burden                :  {results['burden']:.3f} m",
        f"  Spacing               :  {results['spacing']:.3f} m",
        f"  Number of Holes       :  {results['holes']}",
        f"  Charge per Hole       :  {results['charge']:.4f} t",
        "",
        "  ── EXPLOSIVE & ROCK ──────────────────────────",
        f"  Total Explosive       :  {results['total_exp']:.3f} t",
        f"  Rock Volume           :  {results['rock_vol']:.2f} m³",
        f"  Powder Factor         :  {results['pf']:.4f} t/m³",
        "",
        "  ── COST ESTIMATION ───────────────────────────",
        f"  Total Blasting Cost   :  ${results['cost']:,.2f}",
        "",
        "=" * 54,
        "  Open-Pit Blast Design Tool",
        "=" * 54,
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
#  SIDEBAR – inputs
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h1>BLAST DESIGN</h1>
        <p>Open-Pit Mining Tool</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-tag">Rock Parameters</div>', unsafe_allow_html=True)
    rock_density      = st.number_input("Rock Density (t/m³)", min_value=0.1, value=2.7, step=0.1, format="%.2f")

    st.markdown('<div class="section-tag">Bench Geometry</div>', unsafe_allow_html=True)
    bench_height      = st.number_input("Bench Height (m)", min_value=0.1, value=10.0, step=0.5, format="%.1f")
    area              = st.number_input("Bench Area (m²)", min_value=1.0, value=5000.0, step=100.0, format="%.1f")

    st.markdown('<div class="section-tag">Drill & Explosive</div>', unsafe_allow_html=True)
    hole_diameter     = st.number_input("Hole Diameter (m)", min_value=0.01, value=0.115, step=0.005, format="%.4f")
    explosive_density = st.number_input("Explosive Density (t/m³)", min_value=0.1, value=0.85, step=0.05, format="%.2f")

    st.markdown('<div class="section-tag">Cost</div>', unsafe_allow_html=True)
    unit_cost         = st.number_input("Explosive Unit Cost ($/t)", min_value=0.0, value=450.0, step=10.0, format="%.2f")

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("RUN BLAST DESIGN")


# ─────────────────────────────────────────────────────────────
#  MAIN PAGE
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="title-bar">
    <p class="app-title">Blast Design & Cost Estimation</p>
    <p class="app-subtitle">OPEN-PIT MINING  ·  DRILL & BLAST ENGINEERING</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-strip">
  Enter parameters in the left panel and press  RUN BLAST DESIGN  to compute results.
  Adjust inputs anytime to compare scenarios.
</div>
""", unsafe_allow_html=True)

# ── Run on button press or on first load with defaults ────────
if run_btn or "results" not in st.session_state:
    inputs = dict(
        bench_height=bench_height,
        hole_diameter=hole_diameter,
        rock_density=rock_density,
        explosive_density=explosive_density,
        unit_cost=unit_cost,
        area=area,
    )
    try:
        results = run_design(**inputs)
        st.session_state["results"] = results
        st.session_state["inputs"]  = inputs
        st.session_state["ts"]      = datetime.now().strftime("%d %b %Y  %H:%M:%S")
    except ZeroDivisionError:
        st.error("Division by zero – check density or area values.")
        st.stop()

results = st.session_state.get("results")
inputs  = st.session_state.get("inputs")
ts      = st.session_state.get("ts", "")

if results is None:
    st.stop()

# ─────────────────────────────────────────────────────────────
#  OUTPUT LAYOUT  – two columns
# ─────────────────────────────────────────────────────────────

col_left, col_right = st.columns([1, 1], gap="large")

# ── LEFT column ───────────────────────────────────────────────
with col_left:

    # DRILL DESIGN card
    st.markdown(f"""
    <div class="result-card">
        <div class="result-card-title">Drill Design Parameters</div>

        <div class="r-row">
            <span class="r-label">Burden</span>
            <span class="r-value">{results['burden']:.3f}<span class="r-unit">m</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Spacing</span>
            <span class="r-value">{results['spacing']:.3f}<span class="r-unit">m</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Number of Drill Holes</span>
            <span class="r-value">{results['holes']}<span class="r-unit">holes</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Charge per Hole</span>
            <span class="r-value">{results['charge']:.4f}<span class="r-unit">t</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # EXPLOSIVE & ROCK card
    st.markdown(f"""
    <div class="result-card">
        <div class="result-card-title">Explosive &amp; Rock Volume</div>

        <div class="r-row">
            <span class="r-label">Total Explosive Quantity</span>
            <span class="r-value">{results['total_exp']:.3f}<span class="r-unit">t</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Rock Volume</span>
            <span class="r-value">{results['rock_vol']:.2f}<span class="r-unit">m³</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Powder Factor</span>
            <span class="r-value">{results['pf']:.4f}<span class="r-unit">t/m³</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── RIGHT column ──────────────────────────────────────────────
with col_right:

    # COST highlight block
    st.markdown(f"""
    <div class="cost-block">
        <div class="cost-label">Total Blasting Cost — Bench Estimate</div>
        <div class="cost-value">${results['cost']:,.2f}</div>
        <div class="cost-sub">
            Based on {results['total_exp']:.3f} t explosive
            &nbsp;×&nbsp; ${inputs['unit_cost']:.2f} /t
        </div>
    </div>
    """, unsafe_allow_html=True)

    # INPUT SUMMARY card (read-only confirmation)
    st.markdown(f"""
    <div class="result-card">
        <div class="result-card-title">Input Summary</div>

        <div class="r-row">
            <span class="r-label">Bench Height</span>
            <span class="r-value">{inputs['bench_height']:.1f}<span class="r-unit">m</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Hole Diameter</span>
            <span class="r-value">{inputs['hole_diameter']:.4f}<span class="r-unit">m</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Rock Density</span>
            <span class="r-value">{inputs['rock_density']:.2f}<span class="r-unit">t/m³</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Explosive Density</span>
            <span class="r-value">{inputs['explosive_density']:.2f}<span class="r-unit">t/m³</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Bench Area</span>
            <span class="r-value">{inputs['area']:.1f}<span class="r-unit">m²</span></span>
        </div>
        <div class="r-row">
            <span class="r-label">Unit Cost</span>
            <span class="r-value">${inputs['unit_cost']:.2f}<span class="r-unit">/t</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="timestamp">Calculated: {ts}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  SAVE REPORT  (plain-text download via Streamlit)
# ─────────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
report_text = generate_report_text(inputs, results)
st.download_button(
    label="SAVE REPORT  (.txt)",
    data=report_text,
    file_name=f"BlastDesign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
    mime="text/plain",
)

# ─────────────────────────────────────────────────────────────
#  FORMULA REFERENCE  (collapsible)
# ─────────────────────────────────────────────────────────────

with st.expander("FORMULA REFERENCE"):
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; font-size:13px;
                color:#88BDD6; line-height:2;">

    <span style="color:#0FBF6A;">Burden (m)</span>
        = 25 × Hole Diameter × (1 / Rock Density)<br>

    <span style="color:#0FBF6A;">Spacing (m)</span>
        = 1.25 × Burden<br>

    <span style="color:#0FBF6A;">Number of Holes</span>
        = Bench Area / (Burden × Spacing)<br>

    <span style="color:#0FBF6A;">Charge per Hole (t)</span>
        = π × (d/2)² × Bench Height × Explosive Density<br>

    <span style="color:#0FBF6A;">Total Explosive (t)</span>
        = Charge per Hole × Number of Holes<br>

    <span style="color:#0FBF6A;">Rock Volume (m³)</span>
        = Bench Area × Bench Height<br>

    <span style="color:#0FBF6A;">Powder Factor (t/m³)</span>
        = Total Explosive / Rock Volume<br>

    <span style="color:#0FBF6A;">Total Blasting Cost ($)</span>
        = Total Explosive × Explosive Unit Cost<br>

    </div>
    """, unsafe_allow_html=True)
