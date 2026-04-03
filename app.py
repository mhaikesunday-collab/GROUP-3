"""
BLAST DESIGN & COST ESTIMATION TOOL
Open-Pit Mining | Streamlit App
"""

import math
import streamlit as st
from datetime import datetime
import pandas as pd

# ─────────────────────────────
# PAGE CONFIG
# ─────────────────────────────
st.set_page_config(
    page_title="Blast Design Tool",
    page_icon="💥",
    layout="wide"
)

# ─────────────────────────────
# LOGO + MOTTO
# ─────────────────────────────
col1, col2 = st.columns([1, 3])

with col1:
    st.image("logo.png", width=120)  # Put your logo file in folder

with col2:
    st.markdown("## 💥 Blast Design & Cost Tool")
    st.markdown("### 🔥 BLAST LIKE A PRO, SAVE LIKE A BOSS")

st.markdown("---")

# ─────────────────────────────
# UNIT CONVERSION (CORRECTED)
# ─────────────────────────────
def convert_length(value, unit):
    return {
        "m": value,
        "cm": value / 100,
        "mm": value / 1000
    }[unit]

def convert_area(value, unit):
    return {
        "m²": value,
        "cm²": value / 10000,
        "ha": value * 10000
    }[unit]

def convert_density(value, unit):
    return {
        "t/m³": value,
        "kg/m³": value / 1000
    }[unit]

def convert_cost(value, unit):
    return {
        "$/t": value,
        "$/kg": value * 1000
    }[unit]

# ─────────────────────────────
# SIDEBAR INPUTS
# ─────────────────────────────
with st.sidebar:
    st.header("⚙️ INPUTS")

    rock_density_val = st.number_input("Rock Density", 0.1, value=2.7)
    rock_density_unit = st.selectbox("Unit (Density)", ["t/m³", "kg/m³"])

    bench_height_val = st.number_input("Bench Height", 0.1, value=10.0)
    bench_height_unit = st.selectbox("Unit (Height)", ["m", "cm", "mm"])

    hole_diameter_val = st.number_input("Hole Diameter", 0.01, value=0.115)
    hole_diameter_unit = st.selectbox("Unit (Diameter)", ["m", "cm", "mm"])

    explosive_density_val = st.number_input("Explosive Density", 0.1, value=0.85)
    explosive_density_unit = st.selectbox("Unit (Explosive Density)", ["t/m³", "kg/m³"])

    unit_cost_val = st.number_input("Unit Cost", 0.0, value=450.0)
    unit_cost_unit = st.selectbox("Unit (Cost)", ["$/t", "$/kg"])

    area_val = st.number_input("Bench Area", 1.0, value=5000.0)
    area_unit = st.selectbox("Unit (Area)", ["m²", "cm²", "ha"])

    run_btn = st.button("CALCULATE")

# ─────────────────────────────
# CALCULATIONS
# ─────────────────────────────
def run_calc():

    # Convert everything to SI units FIRST
    inputs = {
        "rock_density": convert_density(rock_density_val, rock_density_unit),
        "height": convert_length(bench_height_val, bench_height_unit),
        "diameter": convert_length(hole_diameter_val, hole_diameter_unit),
        "explosive_density": convert_density(explosive_density_val, explosive_density_unit),
        "unit_cost": convert_cost(unit_cost_val, unit_cost_unit),
        "area": convert_area(area_val, area_unit),
    }

    # Core formulas
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

    results = {
        "burden": burden,
        "spacing": spacing,
        "holes": holes,
        "charge": charge_per_hole,
        "total_exp": total_exp,
        "rock_volume": rock_volume,
        "pf": powder_factor,
        "cost": cost,
    }

    return inputs, results

# ─────────────────────────────
# RUN LOGIC
# ─────────────────────────────
if run_btn:
    inputs, results = run_calc()
    st.session_state["inputs"] = inputs
    st.session_state["results"] = results

if "results" in st.session_state:
    inputs = st.session_state["inputs"]
    results = st.session_state["results"]

    # ───────── TABLES ─────────
    colA, colB = st.columns(2)

    with colA:
        st.subheader("📥 Inputs")
        st.table(pd.DataFrame({
            "Parameter": list(inputs.keys()),
            "Value": list(inputs.values())
        }))

    with colB:
        st.subheader("📊 Results")
        st.table(pd.DataFrame({
            "Parameter": [
                "Burden", "Spacing", "Holes",
                "Charge per Hole", "Total Explosive",
                "Rock Volume", "Powder Factor", "Cost"
            ],
            "Value": [
                results["burden"],
                results["spacing"],
                results["holes"],
                results["charge"],
                results["total_exp"],
                results["rock_volume"],
                results["pf"],
                results["cost"]
            ]
        }))

    # COST DISPLAY
    st.markdown("---")
    st.markdown(f"""
    ### 💰 Total Cost

    **${results['cost']:,.2f}**
    """)

    # TXT DOWNLOAD ONLY
    def report():
        return f"""
BLAST REPORT
{datetime.now()}

Burden: {results['burden']:.3f}
Spacing: {results['spacing']:.3f}
Holes: {results['holes']}
Charge: {results['charge']:.4f}
Total Explosive: {results['total_exp']:.3f}
Cost: ${results['cost']:,.2f}
"""

    st.download_button(
        "📄 Download Report",
        report(),
        file_name="blast_report.txt"
    )
