"""
BLAST DESIGN & COST ESTIMATION TOOL
Open-Pit Mining | Streamlit App
Author: mhaike
Flexible unit inputs & outputs
"""

import math
import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO

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
# UNIT CONVERSION FUNCTIONS
# ─────────────────────────────────────────────────────────────
def length_to_m(value, unit):
    to_m = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0, "inch": 0.0254, "ft": 0.3048, "yd": 0.9144}
    return value * to_m[unit]

def m_to_length(value, unit):
    from_m = {"mm": 1000, "cm": 100, "m": 1, "km": 0.001, "inch": 39.3701, "ft": 3.28084, "yd": 1.09361}
    return value * from_m[unit]

def area_to_m2(value, unit):
    to_m2 = {"m²": 1.0, "km²": 1e6, "ha": 10000.0, "ft²": 0.092903, "ac": 4046.86}
    return value * to_m2[unit]

def m2_to_area(value, unit):
    from_m2 = {"m²": 1, "km²": 1e-6, "ha": 0.0001, "ft²": 10.7639, "ac": 0.000247105}
    return value * from_m2[unit]

def density_to_kgpm3(value, unit):
    to_kgm3 = {"kg/m³": 1.0, "g/cm³": 1000.0, "t/m³": 1000.0, "lb/ft³": 16.0185}
    return value * to_kgm3[unit]

def kgpm3_to_density(value, unit):
    from_kgm3 = {"kg/m³": 1, "g/cm³": 0.001, "t/m³": 0.001, "lb/ft³": 0.062428}
    return value * from_kgm3[unit]

# ─────────────────────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────────────────────
def run_design(bench_height_m, hole_diameter_m, rock_density_kgpm3,
               explosive_density_kgpm3, unit_cost_per_tonne, area_m2):

    burden_m = 25 * hole_diameter_m * (1000.0 / rock_density_kgpm3)
    spacing_m = 1.25 * burden_m
    holes = max(1, int(area_m2 / (burden_m * spacing_m)))

    radius = hole_diameter_m / 2.0
    volume = math.pi * radius**2 * bench_height_m
    charge_tonnes = (volume * explosive_density_kgpm3) / 1000.0

    total_exp = charge_tonnes * holes
    rock_vol = area_m2 * bench_height_m
    pf = total_exp / rock_vol
    cost = total_exp * unit_cost_per_tonne

    return dict(
        burden_m=burden_m,
        spacing_m=spacing_m,
        holes=holes,
        charge_tonnes=charge_tonnes,
        total_exp_tonnes=total_exp,
        rock_vol_m3=rock_vol,
        pf=pf,
        cost=cost
    )

# ─────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────
if "results_si" not in st.session_state:
    st.session_state["results_si"] = None
    st.session_state["inputs_si"] = None

# ─────────────────────────────────────────────────────────────
# SIDEBAR INPUTS
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Inputs")

    bh = length_to_m(st.number_input("Bench Height", 10.0), "m")
    hd = length_to_m(st.number_input("Hole Diameter", 0.115), "m")
    rd = density_to_kgpm3(st.number_input("Rock Density", 2.7), "t/m³")
    ed = density_to_kgpm3(st.number_input("Explosive Density", 0.85), "t/m³")
    area = area_to_m2(st.number_input("Bench Area", 5000.0), "m²")
    cost = st.number_input("Unit Cost ($/t)", 450.0)

    run_btn = st.button("CALCULATE")

# ─────────────────────────────────────────────────────────────
# RUN CALCULATION
# ─────────────────────────────────────────────────────────────
if run_btn:
    inputs = dict(
        bench_height_m=bh,
        hole_diameter_m=hd,
        rock_density_kgpm3=rd,
        explosive_density_kgpm3=ed,
        unit_cost_per_tonne=cost,
        area_m2=area,
    )

    st.session_state["inputs_si"] = inputs
    st.session_state["results_si"] = run_design(**inputs)

# ─────────────────────────────────────────────────────────────
# SAFETY CHECK
# ─────────────────────────────────────────────────────────────
if st.session_state["results_si"] is None:
    st.warning("Click CALCULATE before downloading or viewing results.")
    st.stop()

results_si = st.session_state["results_si"]
inputs_si = st.session_state["inputs_si"]

# ─────────────────────────────────────────────────────────────
# EXCEL EXPORT (FIXED + SAFE)
# ─────────────────────────────────────────────────────────────
def generate_excel_report():
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:

        df_inputs = pd.DataFrame([
            ("Bench Height (m)", inputs_si['bench_height_m']),
            ("Hole Diameter (m)", inputs_si['hole_diameter_m']),
            ("Rock Density", inputs_si['rock_density_kgpm3']),
            ("Explosive Density", inputs_si['explosive_density_kgpm3']),
            ("Area (m²)", inputs_si['area_m2']),
            ("Unit Cost", inputs_si['unit_cost_per_tonne']),
        ], columns=["Parameter", "Value"])

        df_results = pd.DataFrame([
            ("Burden (m)", results_si['burden_m']),
            ("Spacing (m)", results_si['spacing_m']),
            ("Holes", results_si['holes']),
            ("Charge (t)", results_si['charge_tonnes']),
            ("Total Explosive (t)", results_si['total_exp_tonnes']),
            ("Rock Volume (m³)", results_si['rock_vol_m3']),
            ("Powder Factor", results_si['pf']),
            ("Cost ($)", results_si['cost']),
        ], columns=["Parameter", "Value"])

        df_inputs.to_excel(writer, sheet_name="Inputs", index=False)
        df_results.to_excel(writer, sheet_name="Results", index=False)

    output.seek(0)
    return output

# ─────────────────────────────────────────────────────────────
# DISPLAY
# ─────────────────────────────────────────────────────────────
st.title("💥 Blast Design Tool")

st.metric("Total Cost ($)", f"{results_si['cost']:,.2f}")
st.metric("Powder Factor", f"{results_si['pf']:.4f}")

# ─────────────────────────────────────────────────────────────
# DOWNLOAD BUTTON (SAFE)
# ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "Download TXT",
        str(results_si),
        file_name="report.txt"
    )

with col2:
    st.download_button(
        "Download Excel",
        generate_excel_report(),
        file_name=f"Blast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
