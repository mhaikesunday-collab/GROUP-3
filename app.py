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
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blast Design Tool",
    page_icon="💥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────────────────────
def calc_burden(diameter: float, rock_density: float) -> float:
    return 25 * diameter * (1 / rock_density)

def calc_spacing(burden: float) -> float:
    return 1.25 * burden

def calc_holes(area: float, burden: float, spacing: float) -> int:
    return max(1, int(area / (burden * spacing)))

def calc_charge_per_hole(diameter: float, bench_height: float, explosive_density: float) -> float:
    radius = diameter / 2
    volume = math.pi * (radius ** 2) * bench_height
    return volume * explosive_density

def run_design(bench_height, hole_diameter, rock_density,
               explosive_density, unit_cost, area):

    burden    = calc_burden(hole_diameter, rock_density)
    spacing   = calc_spacing(burden)
    holes     = calc_holes(area, burden, spacing)
    charge    = calc_charge_per_hole(hole_diameter, bench_height, explosive_density)

    total_exp = charge * holes
    rock_vol  = area * bench_height
    pf        = total_exp / rock_vol
    cost      = total_exp * unit_cost

    return dict(
        burden=burden,
        spacing=spacing,
        holes=holes,
        charge=charge,
        total_exp=total_exp,
        rock_vol=rock_vol,
        pf=pf,
        cost=cost
    )

# ─────────────────────────────────────────────────────────────
# SIDEBAR INPUTS
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Inputs")

    rock_density      = st.number_input("Rock Density (t/m³)", 2.7)
    bench_height      = st.number_input("Bench Height (m)", 10.0)
    area              = st.number_input("Bench Area (m²)", 5000.0)
    hole_diameter     = st.number_input("Hole Diameter (m)", 0.115)
    explosive_density = st.number_input("Explosive Density (t/m³)", 0.85)
    unit_cost         = st.number_input("Unit Cost ($/t)", 450.0)

    run_btn = st.button("CALCULATE")

# ─────────────────────────────────────────────────────────────
# RUN CALCULATION
# ─────────────────────────────────────────────────────────────
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

    st.session_state["inputs"] = inputs
    st.session_state["results"] = results

inputs = st.session_state["inputs"]
results = st.session_state["results"]

# ─────────────────────────────────────────────────────────────
# DISPLAY
# ─────────────────────────────────────────────────────────────
st.title("💥 Blast Design & Cost Estimation")

# ─────────────────────────────────────────────────────────────
# RESULTS TABLE (Drill Design)
# ─────────────────────────────────────────────────────────────
st.subheader("📊 Drill Design Parameters")

drill_df = pd.DataFrame([
    ("Burden", f"{results['burden']:.3f} m"),
    ("Spacing", f"{results['spacing']:.3f} m"),
    ("Number of Holes", results['holes']),
    ("Charge per Hole", f"{results['charge']:.4f} t"),
], columns=["Parameter", "Value"])

st.table(drill_df)

# ─────────────────────────────────────────────────────────────
# RESULTS TABLE (Explosive & Rock)
# ─────────────────────────────────────────────────────────────
st.subheader("📦 Explosive & Rock Volume")

rock_df = pd.DataFrame([
    ("Total Explosive", f"{results['total_exp']:.3f} t"),
    ("Rock Volume", f"{results['rock_vol']:.2f} m³"),
    ("Powder Factor", f"{results['pf']:.4f} t/m³"),
], columns=["Parameter", "Value"])

st.table(rock_df)

# ─────────────────────────────────────────────────────────────
# COST BLOCK
# ─────────────────────────────────────────────────────────────
st.subheader("💰 Cost Estimation")

st.markdown(f"""
<div style="
    background: linear-gradient(120deg, #062A3D, #063320);
    border: 1px solid #0FBF6A;
    border-radius: 8px;
    padding: 18px 24px;
    margin: 20px 0;
">
    <div style="color:#0FBF6A; font-family:monospace; font-size:12px;">
        TOTAL BLASTING COST
    </div>
    <div style="color:#0FBF6A; font-family:monospace; font-size:38px; font-weight:bold;">
        ${results['cost']:,.2f}
    </div>
    <div style="color:#4D7A99; font-size:12px;">
        Based on {results['total_exp']:.3f} t × ${inputs['unit_cost']:.2f}/t
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# INPUT SUMMARY TABLE
# ─────────────────────────────────────────────────────────────
st.subheader("📋 Input Summary")

input_df = pd.DataFrame([
    ("Bench Height", f"{inputs['bench_height']:.1f} m"),
    ("Hole Diameter", f"{inputs['hole_diameter']:.4f} m"),
    ("Rock Density", f"{inputs['rock_density']:.2f} t/m³"),
    ("Explosive Density", f"{inputs['explosive_density']:.2f} t/m³"),
    ("Bench Area", f"{inputs['area']:.1f} m²"),
    ("Unit Cost", f"${inputs['unit_cost']:.2f}/t"),
], columns=["Parameter", "Value"])

st.table(input_df)

# ─────────────────────────────────────────────────────────────
# DOWNLOAD REPORT (TXT ONLY)
# ─────────────────────────────────────────────────────────────
def generate_report_text(inputs, results):
    ts = datetime.now().strftime("%d %B %Y %H:%M:%S")
    return f"""
BLAST DESIGN REPORT
{ts}

Burden: {results['burden']:.3f} m
Spacing: {results['spacing']:.3f} m
Holes: {results['holes']}
Charge per Hole: {results['charge']:.4f} t

Total Explosive: {results['total_exp']:.3f} t
Rock Volume: {results['rock_vol']:.2f} m³
Powder Factor: {results['pf']:.4f} t/m³

Total Cost: ${results['cost']:,.2f}
"""

st.download_button(
    "📄 Download Report (TXT)",
    generate_report_text(inputs, results),
    file_name=f"BlastDesign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
)
