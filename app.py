"""
BLAST DESIGN & COST ESTIMATION TOOL
Open-Pit Mining | Streamlit App
Author: mhaike
"""

import math
import streamlit as st
from datetime import datetime
import pandas as pd

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
#  GLOBAL CSS  – full dark theme + table styling
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

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

/* App background */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-deep) !important;
    color: var(--text-main) !important;
    font-family: var(--body);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--bg-panel) !important;
    border-right: 1px solid var(--border);
}

/* Hide Streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Headers */
h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--accent-blue) !important;
    font-family: var(--mono) !important;
    letter-spacing: 1px;
}

/* Subheader */
.stSubheader {
    color: var(--accent-green) !important;
    font-family: var(--mono) !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
    margin-top: 20px;
}

/* Tables */
table {
    width: 100%;
    background-color: var(--bg-card) !important;
    border-collapse: collapse;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}

th {
    background-color: #0D2A3E !important;
    color: var(--accent-green) !important;
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 600;
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

td {
    padding: 8px 12px;
    color: var(--text-main) !important;
    font-family: var(--body);
    font-size: 14px;
    border-bottom: 1px solid var(--border);
}

tr:last-child td {
    border-bottom: none;
}

/* Cost highlight block */
.cost-block {
    background: linear-gradient(120deg, #062A3D, #063320);
    border: 1px solid var(--accent-green);
    border-radius: 8px;
    padding: 18px 24px;
    margin: 20px 0;
}
.cost-label {
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: 2px;
    color: var(--accent-green);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.cost-value {
    font-family: var(--mono);
    font-size: 38px;
    color: var(--accent-green);
    font-weight: bold;
}
.cost-sub {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 6px;
}

/* Download button */
.stDownloadButton button {
    background: linear-gradient(135deg, var(--mid-blue), var(--mid-green)) !important;
    color: white !important;
    font-family: var(--mono);
    font-size: 13px;
    letter-spacing: 2px;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    transition: 0.2s;
}

/* Sidebar inputs */
[data-testid="stSidebar"] .stNumberInput input {
    background-color: #040E19 !important;
    color: var(--accent-blue) !important;
    border: 1px solid var(--border);
    border-radius: 4px;
}
[data-testid="stSidebar"] label {
    color: var(--text-label) !important;
}
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, var(--mid-blue), var(--mid-green));
    color: white;
    font-family: var(--mono);
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  BACKEND FUNCTIONS (UNCHANGED)
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
    return f"""
BLAST DESIGN REPORT
{ts}

=== DRILL DESIGN ===
Burden               : {results['burden']:.3f} m
Spacing              : {results['spacing']:.3f} m
Number of Holes      : {results['holes']}
Charge per Hole      : {results['charge']:.4f} t

=== EXPLOSIVE & ROCK ===
Total Explosive      : {results['total_exp']:.3f} t
Rock Volume          : {results['rock_vol']:.2f} m³
Powder Factor        : {results['pf']:.4f} t/m³

=== COST ===
Total Blasting Cost  : ${results['cost']:,.2f}

=== INPUT SUMMARY ===
Bench Height         : {inputs['bench_height']:.1f} m
Hole Diameter        : {inputs['hole_diameter']:.4f} m
Rock Density         : {inputs['rock_density']:.2f} t/m³
Explosive Density    : {inputs['explosive_density']:.2f} t/m³
Bench Area           : {inputs['area']:.1f} m²
Unit Cost            : ${inputs['unit_cost']:.2f} /t
"""

# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ INPUT PARAMETERS")
    rock_density      = st.number_input("Rock Density (t/m³)", min_value=0.1, value=2.7, step=0.1, format="%.2f")
    bench_height      = st.number_input("Bench Height (m)", min_value=0.1, value=10.0, step=0.5, format="%.1f")
    area              = st.number_input("Bench Area (m²)", min_value=1.0, value=5000.0, step=100.0, format="%.1f")
    hole_diameter     = st.number_input("Hole Diameter (m)", min_value=0.01, value=0.115, step=0.005, format="%.4f")
    explosive_density = st.number_input("Explosive Density (t/m³)", min_value=0.1, value=0.85, step=0.05, format="%.2f")
    unit_cost         = st.number_input("Unit Cost ($/t)", min_value=0.0, value=450.0, step=10.0, format="%.2f")

    run_btn = st.button("CALCULATE")

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────
st.title("💥 Blast Design & Cost Estimation")
st.caption("Open-Pit Mining | Drill & Blast Engineering Tool")

if run_btn or "results" not in st.session_state:
    inputs = dict(
        bench_height=bench_height,
        hole_diameter=hole_diameter,
        rock_density=rock_density,
        explosive_density=explosive_density,
        unit_cost=unit_cost,
        area=area,
    )
    results = run_design(**inputs)
    st.session_state["results"] = results
    st.session_state["inputs"] = inputs

results = st.session_state["results"]
inputs  = st.session_state["inputs"]

# ─────────────────────────────────────────────────────────────
#  OUTPUT TABLES
# ─────────────────────────────────────────────────────────────

st.subheader("📊 Drill Design Parameters")

# Table 1: Drill Design
drill_data = pd.DataFrame([
    ("Burden", f"{results['burden']:.3f} m"),
    ("Spacing", f"{results['spacing']:.3f} m"),
    ("Number of Holes", results['holes']),
    ("Charge per Hole", f"{results['charge']:.4f} t"),
], columns=["Parameter", "Value"])
st.table(drill_data)

st.subheader("📦 Explosive & Rock Volume")

# Table 2: Explosive & Rock
rock_data = pd.DataFrame([
    ("Total Explosive", f"{results['total_exp']:.3f} t"),
    ("Rock Volume", f"{results['rock_vol']:.2f} m³"),
    ("Powder Factor", f"{results['pf']:.4f} t/m³"),
], columns=["Parameter", "Value"])
st.table(rock_data)

st.subheader("💰 Cost Estimation")

# Cost highlight block
st.markdown(f"""
<div class="cost-block">
    <div class="cost-label">Total Blasting Cost — Bench Estimate</div>
    <div class="cost-value">${results['cost']:,.2f}</div>
    <div class="cost-sub">
        Based on {results['total_exp']:.3f} t explosive × ${inputs['unit_cost']:.2f}/t
    </div>
</div>
""", unsafe_allow_html=True)

st.subheader("📋 Input Summary")

# Table 3: Input parameters
input_data = pd.DataFrame([
    ("Bench Height", f"{inputs['bench_height']:.1f} m"),
    ("Hole Diameter", f"{inputs['hole_diameter']:.4f} m"),
    ("Rock Density", f"{inputs['rock_density']:.2f} t/m³"),
    ("Explosive Density", f"{inputs['explosive_density']:.2f} t/m³"),
    ("Bench Area", f"{inputs['area']:.1f} m²"),
    ("Unit Cost", f"${inputs['unit_cost']:.2f} /t"),
], columns=["Parameter", "Value"])
st.table(input_data)

# ─────────────────────────────────────────────────────────────
#  DOWNLOAD REPORT
# ─────────────────────────────────────────────────────────────
report_text = generate_report_text(inputs, results)

st.download_button(
    "📄 Download Report (TXT)",
    report_text,
    file_name=f"BlastDesign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
)
