"""
BLAST DESIGN & COST ESTIMATION TOOL
Open-Pit Mining | Streamlit App
Author: mhaike
"""

import math
import streamlit as st
from datetime import datetime
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Blast Design Tool",
    page_icon="💥",
    layout="wide"
)

# ─────────────────────────────────────────────
# LOGO + MOTTO
# ─────────────────────────────────────────────
col1, col2 = st.columns([1, 3])

with col1:
    st.image("logo.png", width=120)  # <-- put your logo file here

with col2:
    st.markdown("## 💥 Blast Design & Cost Tool")
    st.markdown("### 🔥 BLAST LIKE A PRO, SAVE LIKE A BOSS")

st.markdown("---")

# ─────────────────────────────────────────────
# UNIT CONVERSION SYSTEM
# ─────────────────────────────────────────────
unit_factors = {
    "m": 1.0,
    "cm": 0.01,
    "mm": 0.001,
}

density_factors = {
    "t/m³": 1.0,
    "kg/m³": 0.001,
}

cost_factors = {
    "$/t": 1.0,
    "$/kg": 0.001,
}

# ─────────────────────────────────────────────
# SIDEBAR INPUTS
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ INPUTS")

    rock_density_val = st.number_input("Rock Density", 0.1, value=2.7)
    rock_density_unit = st.selectbox("Unit (Rock Density)", list(density_factors.keys()))

    bench_height_val = st.number_input("Bench Height", 0.1, value=10.0)
    bench_height_unit = st.selectbox("Unit (Height)", list(unit_factors.keys()))

    hole_diameter_val = st.number_input("Hole Diameter", 0.01, value=0.115)
    hole_diameter_unit = st.selectbox("Unit (Diameter)", list(unit_factors.keys()))

    explosive_density_val = st.number_input("Explosive Density", 0.1, value=0.85)
    explosive_density_unit = st.selectbox("Unit (Explosive Density)", list(density_factors.keys()))

    unit_cost_val = st.number_input("Unit Cost", 0.0, value=450.0)
    unit_cost_unit = st.selectbox("Unit (Cost)", list(cost_factors.keys()))

    area_val = st.number_input("Bench Area", 1.0, value=5000.0)
    area_unit = st.selectbox("Unit (Area)", list(unit_factors.keys()))

    run_btn = st.button("CALCULATE")

# ─────────────────────────────────────────────
# UNIT CONVERSION FUNCTION
# ─────────────────────────────────────────────
def convert(value, unit, factors):
    return value * factors[unit]

# ─────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────
def calc_all(inputs):
    burden = 25 * inputs["diameter"] * (1 / inputs["rock_density"])
    spacing = 1.25 * burden

    holes = max(1, int(inputs["area"] / (burden * spacing)))

    radius = inputs["diameter"] / 2
    volume = math.pi * (radius ** 2) * inputs["height"]

    charge_per_hole = volume * inputs["explosive_density"]
    total_exp = charge_per_hole * holes

    rock_volume = inputs["area"] * inputs["height"]
    powder_factor = total_exp / rock_volume

    cost = total_exp * inputs["unit_cost"]

    return {
        "burden": burden,
        "spacing": spacing,
        "holes": holes,
        "charge": charge_per_hole,
        "total_exp": total_exp,
        "rock_volume": rock_volume,
        "pf": powder_factor,
        "cost": cost,
    }

# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if run_btn or "results" not in st.session_state:

    inputs = {
        "rock_density": convert(rock_density_val, rock_density_unit, density_factors),
        "height": convert(bench_height_val, bench_height_unit, unit_factors),
        "diameter": convert(hole_diameter_val, hole_diameter_unit, unit_factors),
        "explosive_density": convert(explosive_density_val, explosive_density_unit, density_factors),
        "unit_cost": convert(unit_cost_val, unit_cost_unit, cost_factors),
        "area": convert(area_val, area_unit, unit_factors),
    }

    results = calc_all(inputs)

    st.session_state["inputs"] = inputs
    st.session_state["results"] = results

inputs = st.session_state["inputs"]
results = st.session_state["results"]

# ─────────────────────────────────────────────
# TABLES (INPUT + RESULTS SIDE BY SIDE)
# ─────────────────────────────────────────────
colA, colB = st.columns(2)

with colA:
    st.subheader("📥 Inputs")
    df_inputs = pd.DataFrame({
        "Parameter": [
            "Rock Density",
            "Bench Height",
            "Hole Diameter",
            "Explosive Density",
            "Unit Cost",
            "Bench Area",
        ],
        "Value": [
            inputs["rock_density"],
            inputs["height"],
            inputs["diameter"],
            inputs["explosive_density"],
            inputs["unit_cost"],
            inputs["area"],
        ]
    })
    st.table(df_inputs)

with colB:
    st.subheader("📊 Results")
    df_results = pd.DataFrame({
        "Parameter": [
            "Burden",
            "Spacing",
            "Holes",
            "Charge per Hole",
            "Total Explosive",
            "Rock Volume",
            "Powder Factor",
            "Cost",
        ],
        "Value": [
            results["burden"],
            results["spacing"],
            results["holes"],
            results["charge"],
            results["total_exp"],
            results["rock_volume"],
            results["pf"],
            results["cost"],
        ]
    })
    st.table(df_results)

# ─────────────────────────────────────────────
# COST DISPLAY
# ─────────────────────────────────────────────
st.markdown("---")

st.markdown(f"""
### 💰 Total Cost

**${results['cost']:,.2f}**

""")

# ─────────────────────────────────────────────
# TXT REPORT ONLY (NO EXCEL)
# ─────────────────────────────────────────────
def generate_report(inputs, results):
    return f"""
BLAST DESIGN REPORT
{datetime.now()}

Burden: {results['burden']:.3f}
Spacing: {results['spacing']:.3f}
Holes: {results['holes']}
Charge: {results['charge']:.4f}
Total Explosive: {results['total_exp']:.3f}
Cost: ${results['cost']:,.2f}
"""

st.download_button(
    "📄 Download TXT Report",
    generate_report(inputs, results),
    file_name=f"Blast_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
)
