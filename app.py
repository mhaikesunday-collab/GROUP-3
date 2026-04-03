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
    st.image("logo.png", width=120)

with col2:
    st.markdown("## 💥 Blast Design & Cost Tool")
    st.markdown("### 🔥 BLAST LIKE A PRO, SAVE LIKE A BOSS")

st.markdown("---")

# ─────────────────────────────────────────────
# UNIT CONVERSIONS (FIXED)
# ─────────────────────────────────────────────
def length_to_m(v, u):
    return {
        "m": v,
        "cm": v / 100,
        "mm": v / 1000,
        "ft": v * 0.3048,
        "inch": v * 0.0254
    }[u]

def area_to_m2(v, u):
    return {
        "m²": v,
        "cm²": v / 10000,
        "ha": v * 10000,
        "ft²": v * 0.092903,
        "ac": v * 4046.86
    }[u]

def density_to_tpm3(v, u):
    return {
        "t/m³": v,
        "kg/m³": v / 1000,
        "g/cm³": v,
        "lb/ft³": v * 0.0160185
    }[u]

def cost_to_dpt(v, u):
    return {
        "$/t": v,
        "$/kg": v * 1000
    }[u]

# ─────────────────────────────────────────────
# SIDEBAR INPUTS
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ INPUTS")

    rd = st.number_input("Rock Density", value=2.7)
    rd_u = st.selectbox("Unit", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"])

    bh = st.number_input("Bench Height", value=10.0)
    bh_u = st.selectbox("Unit ", ["m", "cm", "mm", "ft", "inch"])

    hd = st.number_input("Hole Diameter", value=0.115)
    hd_u = st.selectbox("Unit  ", ["m", "cm", "mm", "ft", "inch"])

    ed = st.number_input("Explosive Density", value=0.85)
    ed_u = st.selectbox("Unit   ", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"])

    area = st.number_input("Bench Area", value=5000.0)
    area_u = st.selectbox("Unit    ", ["m²", "cm²", "ha", "ft²", "ac"])

    cost = st.number_input("Unit Cost", value=450.0)
    cost_u = st.selectbox("Unit     ", ["$/t", "$/kg"])

    run_btn = st.button("CALCULATE")

# ─────────────────────────────────────────────
# CALCULATION
# ─────────────────────────────────────────────
def calculate():

    inputs = {
        "rock_density": density_to_tpm3(rd, rd_u),
        "bench_height": length_to_m(bh, bh_u),
        "hole_diameter": length_to_m(hd, hd_u),
        "explosive_density": density_to_tpm3(ed, ed_u),
        "area": area_to_m2(area, area_u),
        "unit_cost": cost_to_dpt(cost, cost_u),
    }

    burden = 25 * inputs["hole_diameter"] * (1 / inputs["rock_density"])
    spacing = 1.25 * burden

    holes = max(1, int(inputs["area"] / (burden * spacing)))

    radius = inputs["hole_diameter"] / 2
    volume = math.pi * radius**2 * inputs["bench_height"]

    charge = volume * inputs["explosive_density"]
    total_exp = charge * holes

    rock_vol = inputs["area"] * inputs["bench_height"]
    pf = total_exp / rock_vol

    cost_total = total_exp * inputs["unit_cost"]

    results = {
        "Burden": burden,
        "Spacing": spacing,
        "Holes": holes,
        "Charge per Hole": charge,
        "Total Explosive": total_exp,
        "Rock Volume": rock_vol,
        "Powder Factor": pf,
        "Cost": cost_total
    }

    return inputs, results

# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if run_btn:
    inputs, results = calculate()
    st.session_state["inputs"] = inputs
    st.session_state["results"] = results

# ─────────────────────────────────────────────
# DISPLAY
# ─────────────────────────────────────────────
if "results" in st.session_state:

    inputs = st.session_state["inputs"]
    results = st.session_state["results"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📥 INPUTS")
        st.table(pd.DataFrame({
            "Parameter": list(inputs.keys()),
            "Value": list(inputs.values())
        }))

    with col2:
        st.subheader("📊 RESULTS")
        st.table(pd.DataFrame({
            "Parameter": list(results.keys()),
            "Value": list(results.values())
        }))

    st.markdown("---")

    st.markdown(f"""
    ### 💰 TOTAL COST

    **${results['Cost']:,.2f}**
    """)

    # TXT ONLY (NO EXCEL)
    def report():
        return f"""
BLAST REPORT
{datetime.now()}

{chr(10).join([f"{k}: {v}" for k, v in inputs.items()])}

--- RESULTS ---
{chr(10).join([f"{k}: {v}" for k, v in results.items()])}
"""

    st.download_button(
        "📄 Download TXT Report",
        report(),
        file_name="blast_report.txt"
    )

else:
    st.info("Enter inputs and click CALCULATE")
