"""
BLAST DESIGN & COST ESTIMATION TOOL
Open-Pit Mining | Streamlit App
Author: mhaike
"""

import math
import streamlit as st
from datetime import datetime
import pandas as pd
import os
import base64

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blast Design Tool",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  FUNCTION TO GET BASE64 OF LOCAL IMAGE
# ─────────────────────────────────────────────────────────────
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# ─────────────────────────────────────────────────────────────
#  FULL-WIDTH LOGO WITH COMPACT MOTTO
# ─────────────────────────────────────────────────────────────
logo_b64 = get_base64_image("logo.png")
if logo_b64:
    st.markdown(f"""
    <style>
    .hero-logo {{
        background-image: url("data:image/png;base64,{logo_b64}");
        background-size: cover;
        background-position: center;
        height: 150px;
        width: 100%;
        border-radius: 12px;
        margin-bottom: 20px;
        position: relative;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    .hero-logo .motto-overlay {{
        font-family: 'Share Tech Mono', monospace;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 1px;
        color: #0FBF6A;
        text-shadow: 0 0 4px black;
        background: rgba(4, 16, 28, 0.8);
        padding: 4px 12px;
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(2px);
        margin-bottom: 8px;
        white-space: nowrap;
        max-width: 95%;
        overflow-x: auto;
    }}
    </style>
    <div class="hero-logo">
        <div class="motto-overlay"> BLAST LIKE A PRO, SAVE LIKE A BOSS </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="motto" style="margin-top:0;">  BLAST LIKE A PRO, SAVE LIKE A BOSS </div>', unsafe_allow_html=True)

st.title("Blast Design & Cost Estimation Tool")
st.caption("Open‑Pit Mining | Drill & Blast Engineering")

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS – dark theme + table styling
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

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-deep) !important;
    color: var(--text-main) !important;
    font-family: var(--body);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-panel) !important;
    border-right: 1px solid var(--border);
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Headers */
h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--accent-blue) !important;
    font-family: var(--mono) !important;
}

.stSubheader {
    color: var(--accent-green) !important;
    font-family: var(--mono) !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
}

/* Tables */
table {
    width: 100%;
    background-color: var(--bg-card) !important;
    border-collapse: collapse;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 20px;
}
th {
    background-color: #0D2A3E !important;
    color: var(--accent-green) !important;
    font-family: var(--mono);
    padding: 10px 12px;
}
td {
    padding: 8px 12px;
    color: var(--text-main) !important;
    border-bottom: 1px solid var(--border);
}

/* Cost block */
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
    color: var(--accent-green);
    text-transform: uppercase;
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
}

/* Download button */
.stDownloadButton button {
    background: linear-gradient(135deg, var(--mid-blue), var(--mid-green)) !important;
    color: white !important;
    font-family: var(--mono);
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    width: 100%;
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
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  UNIT CONVERSION FUNCTIONS
# ─────────────────────────────────────────────────────────────
def length_to_m(value, unit):
    to_m = {
        "m": 1.0, "cm": 0.01, "mm": 0.001, "ft": 0.3048, "inch": 0.0254
    }
    return value * to_m.get(unit, 1.0)

def area_to_m2(value, unit):
    to_m2 = {
        "m²": 1.0, "cm²": 0.0001, "ha": 10000.0, "ft²": 0.092903, "ac": 4046.86
    }
    return value * to_m2.get(unit, 1.0)

def density_to_tpm3(value, unit):
    to_tpm3 = {
        "t/m³": 1.0, "kg/m³": 0.001, "g/cm³": 1.0, "lb/ft³": 0.0160185
    }
    return value * to_tpm3.get(unit, 1.0)

def cost_to_dollar_per_tonne(value, unit):
    to_dpt = {
        "$/t": 1.0, "$/kg": 1000.0
    }
    return value * to_dpt.get(unit, 1.0)

# ─────────────────────────────────────────────────────────────
#  CALCULATION ENGINE (SI: m, m², t/m³, $/t)
#  Returns None if any required input is zero or negative
# ─────────────────────────────────────────────────────────────
def run_design(bench_height_m, hole_diameter_m, rock_density_tpm3,
               explosive_density_tpm3, unit_cost_dpt, area_m2):
    # Prevent division by zero or invalid dimensions
    if rock_density_tpm3 <= 0:
        return None
    if bench_height_m <= 0 or hole_diameter_m <= 0 or area_m2 <= 0:
        return None
    if explosive_density_tpm3 <= 0:
        return None
    
    burden = 25 * hole_diameter_m 
    spacing = 1.25 * burden
    holes = (area_m2 / (burden * spacing))
    radius = hole_diameter_m / 2
    volume_m3 = math.pi * (radius ** 2) * bench_height_m
    charge_per_hole_t = volume_m3 * explosive_density_tpm3
    total_exp_t = charge_per_hole_t * holes
    rock_vol_m3 = area_m2 * bench_height_m
    pf = total_exp_kg / rock_vol_m3
    cost = total_exp_t * unit_cost_dpt
    return {
        "burden_m": burden,
        "spacing_m": spacing,
        "holes": holes,
        "charge_t": charge_per_hole_t,
        "total_exp_t": total_exp_t,
        "rock_vol_m3": rock_vol_m3,
        "pf_tpm3": pf,
        "cost_usd": cost,
    }

# ─────────────────────────────────────────────────────────────
#  SIDEBAR – INPUTS WITH INLINE UNITS (all start at 0)
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⬇️ INPUT PARAMETERS")
    
    # Rock Density
    col1, col2 = st.columns([2, 1])
    with col1:
        rd_val = st.number_input("Rock Density", min_value=0.0, value=0.0, step=0.1, format="%.2f", key="rd")
    with col2:
        rd_unit = st.selectbox("Unit", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"], index=0, key="rd_u")
    
    # Bench Height
    col1, col2 = st.columns([2, 1])
    with col1:
        bh_val = st.number_input("Bench Height", min_value=0.0, value=0.0, step=0.5, format="%.2f", key="bh")
    with col2:
        bh_unit = st.selectbox("Unit", ["m", "cm", "mm", "ft", "inch"], index=0, key="bh_u")
    
    # Hole Diameter
    col1, col2 = st.columns([2, 1])
    with col1:
        hd_val = st.number_input("Hole Diameter", min_value=0.0, value=0.0, step=0.005, format="%.4f", key="hd")
    with col2:
        hd_unit = st.selectbox("Unit", ["m", "cm", "mm", "ft", "inch"], index=0, key="hd_u")
    
    # Explosive Density
    col1, col2 = st.columns([2, 1])
    with col1:
        ed_val = st.number_input("Explosive Density", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="ed")
    with col2:
        ed_unit = st.selectbox("Unit", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"], index=0, key="ed_u")
    
    # Bench Area
    col1, col2 = st.columns([2, 1])
    with col1:
        area_val = st.number_input("Bench Area", min_value=0.0, value=0.0, step=100.0, format="%.1f", key="area")
    with col2:
        area_unit = st.selectbox("Unit", ["m²", "cm²", "ha", "ft²", "ac"], index=0, key="area_u")
    
    # Unit Cost
    col1, col2 = st.columns([2, 1])
    with col1:
        cost_val = st.number_input("Unit Cost", min_value=0.0, value=0.0, step=10.0, format="%.2f", key="cost")
    with col2:
        cost_unit = st.selectbox("Unit", ["$/t", "$/kg"], index=0, key="cost_u")
    
    run_btn = st.button("CALCULATE", use_container_width=True)

# ─────────────────────────────────────────────────────────────
#  PROCESS CALCULATION
# ─────────────────────────────────────────────────────────────
if run_btn:
    # Convert all inputs to SI units
    rock_density_tpm3 = density_to_tpm3(rd_val, rd_unit)
    bench_height_m = length_to_m(bh_val, bh_unit)
    hole_diameter_m = length_to_m(hd_val, hd_unit)
    explosive_density_tpm3 = density_to_tpm3(ed_val, ed_unit)
    area_m2 = area_to_m2(area_val, area_unit)
    unit_cost_dpt = cost_to_dollar_per_tonne(cost_val, cost_unit)
    
    results = run_design(bench_height_m, hole_diameter_m, rock_density_tpm3,
                         explosive_density_tpm3, unit_cost_dpt, area_m2)
    
    if results is None:
        st.error("❌ Please enter positive values for all inputs (Rock Density, Bench Height, Hole Diameter, Explosive Density, Bench Area).")
        st.session_state.pop("results", None)
        st.session_state.pop("inputs_si", None)
    else:
        st.session_state["results"] = results
        st.session_state["inputs_si"] = {
            "Rock Density (t/m³)": rock_density_tpm3,
            "Bench Height (m)": bench_height_m,
            "Hole Diameter (m)": hole_diameter_m,
            "Explosive Density (t/m³)": explosive_density_tpm3,
            "Bench Area (m²)": area_m2,
            "Unit Cost ($/t)": unit_cost_dpt,
        }

# Display results if available
if "results" in st.session_state:
    res = st.session_state["results"]
    ins = st.session_state["inputs_si"]
    
    # Vertical stack: INPUTS → RESULTS → Cost → Download
    st.subheader("INPUTS")
    input_df = pd.DataFrame({
        "Parameter": list(ins.keys()),
        "Value": [f"{v:.4f}" if isinstance(v, float) else v for v in ins.values()]
    })
    st.table(input_df)
    
    st.subheader("📃RESULTS")
    result_items = [
        ("Burden (m)", res["burden_m"]),
        ("Spacing (m)", res["spacing_m"]),
        ("Number of Holes", res["holes"]),
        ("Charge per Hole (t)", res["charge_t"]),
        ("Total Explosive (t)", res["total_exp_t"]),
        ("Rock Volume (m³)", res["rock_vol_m3"]),
        ("Powder Factor (t/m³)", res["pf_tpm3"]),
    ]
    result_df = pd.DataFrame({
        "Parameter": [item[0] for item in result_items],
        "Value": [f"{item[1]:.4f}" if isinstance(item[1], float) else item[1] for item in result_items]
    })
    st.table(result_df)
    
    # Cost block
    st.markdown(f"""
    <div class="cost-block">
        <div class="cost-label">Total Blasting Cost</div>
        <div class="cost-value">${res['cost_usd']:,.2f}</div>
        <div class="cost-sub">
            Based on {res['total_exp_t']:.3f} t explosive × ${ins['Unit Cost ($/t)']:.2f}/t
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Download TXT report
    def txt_report():
        return f"""
BLAST DESIGN REPORT
{datetime.now().strftime("%d %B %Y %H:%M:%S")}

=== INPUTS ===
{chr(10).join([f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}" for k, v in ins.items()])}

=== RESULTS ===
Burden               : {res['burden_m']:.3f} m
Spacing              : {res['spacing_m']:.3f} m
Number of Holes      : {res['holes']}
Charge per Hole      : {res['charge_t']:.4f} t
Total Explosive      : {res['total_exp_t']:.3f} t
Rock Volume          : {res['rock_vol_m3']:.2f} m³
Powder Factor        : {res['pf_tpm3']:.4f} t/m³
Total Cost           : ${res['cost_usd']:,.2f}
"""
    
    st.markdown("---")
    st.download_button(
        "📥 Download Report (TXT)",
        txt_report(),
        file_name=f"BlastDesign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
else:
    # Show a message only if no calculation has been performed yet (not after an error)
    if not run_btn:
        st.info("👈 Enter your parameters in the sidebar and click **CALCULATE** to see results.")

# ─────────────────────────────────────────────────────────────
#  OPTIONAL UNIT CONVERTER (expandable)
# ─────────────────────────────────────────────────────────────
with st.expander("🔄 Quick Unit Converter (optional)"):
    conv_type = st.selectbox("Conversion type", ["Length", "Area", "Density", "Cost"])
    val = st.number_input("Value", value=1.0, key="conv_val")
    if conv_type == "Length":
        from_u = st.selectbox("From", ["m", "cm", "mm", "ft", "inch"])
        to_u = st.selectbox("To", ["m", "cm", "mm", "ft", "inch"], index=1)
        result = length_to_m(val, from_u)
        result = result * {"m":1, "cm":100, "mm":1000, "ft":3.28084, "inch":39.3701}[to_u]
    elif conv_type == "Area":
        from_u = st.selectbox("From", ["m²", "cm²", "ha", "ft²", "ac"])
        to_u = st.selectbox("To", ["m²", "cm²", "ha", "ft²", "ac"])
        result = area_to_m2(val, from_u)
        result = result / {"m²":1, "cm²":0.0001, "ha":10000, "ft²":0.092903, "ac":4046.86}[to_u]
    elif conv_type == "Density":
        from_u = st.selectbox("From", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"])
        to_u = st.selectbox("To", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"])
        result = density_to_tpm3(val, from_u)
        result = result / {"t/m³":1, "kg/m³":0.001, "g/cm³":1, "lb/ft³":0.0160185}[to_u]
    else:  # Cost
        from_u = st.selectbox("From", ["$/t", "$/kg"])
        to_u = st.selectbox("To", ["$/t", "$/kg"])
        result = cost_to_dollar_per_tonne(val, from_u)
        result = result / {"$/t":1, "$/kg":1000}[to_u]
    st.success(f"Result: {result:.6f} {to_u}")
