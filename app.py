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
# LOGO + MOTTO (fixed, no external file)
# ─────────────────────────────
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("## 💥")   # emoji as placeholder logo

with col2:
    st.markdown("## 💥 Blast Design & Cost Tool")
    st.markdown("### 🔥 BLAST LIKE A PRO, SAVE LIKE A BOSS")

st.markdown("---")

# ─────────────────────────────
# UNIT CONVERSION (corrected & safe)
# ─────────────────────────────
def convert_length(value, unit):
    unit = unit.lower()
    if unit == "m":
        return value
    elif unit == "cm":
        return value / 100
    elif unit == "mm":
        return value / 1000
    else:
        return value  # fallback

def convert_area(value, unit):
    unit = unit.lower()
    if unit == "m²" or unit == "m2":
        return value
    elif unit == "cm²" or unit == "cm2":
        return value / 10000
    elif unit == "ha":
        return value * 10000
    else:
        return value

def convert_density(value, unit):
    unit = unit.lower()
    if unit == "t/m³" or unit == "t/m3":
        return value
    elif unit == "kg/m³" or unit == "kg/m3":
        return value / 1000
    else:
        return value

def convert_cost(value, unit):
    unit = unit.lower()
    if unit == "$/t" or unit == "$/tonne":
        return value
    elif unit == "$/kg":
        return value * 1000
    else:
        return value

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
    # Convert everything to SI units
    inputs = {
        "Rock Density (t/m³)": convert_density(rock_density_val, rock_density_unit),
        "Bench Height (m)": convert_length(bench_height_val, bench_height_unit),
        "Hole Diameter (m)": convert_length(hole_diameter_val, hole_diameter_unit),
        "Explosive Density (t/m³)": convert_density(explosive_density_val, explosive_density_unit),
        "Unit Cost ($/t)": convert_cost(unit_cost_val, unit_cost_unit),
        "Bench Area (m²)": convert_area(area_val, area_unit),
    }

    # Core formulas
    burden = 25 * inputs["Hole Diameter (m)"] * (1 / inputs["Rock Density (t/m³)"])
    spacing = 1.25 * burden

    holes = max(1, int(inputs["Bench Area (m²)"] / (burden * spacing)))

    radius = inputs["Hole Diameter (m)"] / 2
    volume = math.pi * (radius ** 2) * inputs["Bench Height (m)"]

    charge_per_hole = volume * inputs["Explosive Density (t/m³)"]
    total_exp = charge_per_hole * holes

    rock_volume = inputs["Bench Area (m²)"] * inputs["Bench Height (m)"]
    powder_factor = total_exp / rock_volume

    cost = total_exp * inputs["Unit Cost ($/t)"]

    results = {
        "Burden (m)": burden,
        "Spacing (m)": spacing,
        "Number of Holes": holes,
        "Charge per Hole (t)": charge_per_hole,
        "Total Explosive (t)": total_exp,
        "Rock Volume (m³)": rock_volume,
        "Powder Factor (t/m³)": powder_factor,
        "Total Cost ($)": cost,
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
        st.subheader("📥 Inputs (converted to SI)")
        # Convert inputs dict to DataFrame for clean display
        input_df = pd.DataFrame({
            "Parameter": list(inputs.keys()),
            "Value": [f"{v:.4f}" if isinstance(v, float) else v for v in inputs.values()]
        })
        st.table(input_df)

    with colB:
        st.subheader("📊 Results")
        result_df = pd.DataFrame({
            "Parameter": list(results.keys()),
            "Value": [f"{v:.4f}" if isinstance(v, float) else v for v in results.values()]
        })
        st.table(result_df)

    # COST DISPLAY
    st.markdown("---")
    st.markdown(f"""
    ### 💰 Total Cost

    **${results['Total Cost ($)']:,.2f}**
    """)

    # TXT DOWNLOAD
    def report():
        return f"""
BLAST REPORT
{datetime.now()}

Burden: {results['Burden (m)']:.3f} m
Spacing: {results['Spacing (m)']:.3f} m
Holes: {results['Number of Holes']}
Charge per Hole: {results['Charge per Hole (t)']:.4f} t
Total Explosive: {results['Total Explosive (t)']:.3f} t
Rock Volume: {results['Rock Volume (m³)']:.2f} m³
Powder Factor: {results['Powder Factor (t/m³)']:.4f}
Total Cost: ${results['Total Cost ($)']:,.2f}
"""

    st.download_button(
        "📄 Download Report",
        report(),
        file_name="blast_report.txt"
    )

else:
    # Show a friendly message before first calculation
    st.info("👈 Enter your parameters in the sidebar and click **CALCULATE** to see results.")
