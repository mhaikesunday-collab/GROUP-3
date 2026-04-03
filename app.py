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
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blast Design Tool",
    page_icon="💥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS – dark theme with logo & motto styling
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

/* Logo container */
.logo-container {
    text-align: center;
    margin: 20px 0 10px 0;
}
.logo-img {
    max-width: 200px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* Motto */
.motto {
    text-align: center;
    font-family: var(--mono);
    font-size: 24px;
    font-weight: bold;
    letter-spacing: 3px;
    color: var(--accent-green);
    text-shadow: 0 0 6px rgba(15,191,106,0.4);
    margin: 10px 0 25px 0;
    padding: 12px;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    background: rgba(4,16,28,0.5);
}

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

.stDownloadButton button {
    background: linear-gradient(135deg, var(--mid-blue), var(--mid-green)) !important;
    color: white !important;
    font-family: var(--mono);
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  UNIT CONVERSION FUNCTIONS (SI base: m, kg, m², kg/m³)
# ─────────────────────────────────────────────────────────────
def length_to_m(value, unit):
    to_m = {
        "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
        "inch": 0.0254, "ft": 0.3048, "yd": 0.9144
    }
    return value * to_m[unit]

def m_to_length(value, unit):
    from_m = {
        "mm": 1000, "cm": 100, "m": 1, "km": 0.001,
        "inch": 39.3701, "ft": 3.28084, "yd": 1.09361
    }
    return value * from_m[unit]

def area_to_m2(value, unit):
    to_m2 = {
        "m²": 1.0, "km²": 1e6, "ha": 10000.0, "ft²": 0.092903, "ac": 4046.86
    }
    return value * to_m2[unit]

def m2_to_area(value, unit):
    from_m2 = {
        "m²": 1, "km²": 1e-6, "ha": 0.0001, "ft²": 10.7639, "ac": 0.000247105
    }
    return value * from_m2[unit]

def density_to_kgpm3(value, unit):
    to_kgm3 = {
        "kg/m³": 1.0, "g/cm³": 1000.0, "t/m³": 1000.0, "lb/ft³": 16.0185
    }
    return value * to_kgm3[unit]

def kgpm3_to_density(value, unit):
    from_kgm3 = {
        "kg/m³": 1, "g/cm³": 0.001, "t/m³": 0.001, "lb/ft³": 0.062428
    }
    return value * from_kgm3[unit]

# ─────────────────────────────────────────────────────────────
#  BACKEND CALCULATIONS (all SI: m, m², kg/m³, t = 1000 kg)
# ─────────────────────────────────────────────────────────────
def calc_burden(diameter_m: float, rock_density_kgpm3: float) -> float:
    rock_density_tpm3 = rock_density_kgpm3 / 1000.0
    return 25 * diameter_m * (1.0 / rock_density_tpm3)

def calc_spacing(burden_m: float) -> float:
    return 1.25 * burden_m

def calc_holes(area_m2: float, burden_m: float, spacing_m: float) -> int:
    return max(1, int(area_m2 / (burden_m * spacing_m)))

def calc_charge_per_hole(diameter_m: float, bench_height_m: float,
                          explosive_density_kgpm3: float) -> float:
    radius = diameter_m / 2.0
    volume_m3 = math.pi * (radius ** 2) * bench_height_m
    mass_kg = volume_m3 * explosive_density_kgpm3
    return mass_kg / 1000.0  # tonnes

def run_design(bench_height_m, hole_diameter_m, rock_density_kgpm3,
               explosive_density_kgpm3, unit_cost_per_tonne, area_m2):
    burden_m = calc_burden(hole_diameter_m, rock_density_kgpm3)
    spacing_m = calc_spacing(burden_m)
    holes = calc_holes(area_m2, burden_m, spacing_m)
    charge_tonnes = calc_charge_per_hole(hole_diameter_m, bench_height_m, explosive_density_kgpm3)
    total_exp_tonnes = charge_tonnes * holes
    rock_vol_m3 = area_m2 * bench_height_m
    pf = total_exp_tonnes / rock_vol_m3
    cost = total_exp_tonnes * unit_cost_per_tonne
    return dict(burden_m=burden_m, spacing_m=spacing_m, holes=holes,
                charge_tonnes=charge_tonnes, total_exp_tonnes=total_exp_tonnes,
                rock_vol_m3=rock_vol_m3, pf=pf, cost=cost)

# ─────────────────────────────────────────────────────────────
#  INITIALIZE SESSION STATE (to avoid KeyError)
# ─────────────────────────────────────────────────────────────
if "results_si" not in st.session_state:
    # Default values in SI
    default_inputs = dict(
        bench_height_m=10.0,
        hole_diameter_m=0.115,
        rock_density_kgpm3=2700.0,   # 2.7 t/m³
        explosive_density_kgpm3=850.0,  # 0.85 t/m³
        unit_cost_per_tonne=450.0,
        area_m2=5000.0,
    )
    default_results = run_design(**default_inputs)
    st.session_state["results_si"] = default_results
    st.session_state["inputs_si"] = default_inputs
    st.session_state["display_units"] = {"length": "m", "area": "m²", "density": "t/m³"}

# ─────────────────────────────────────────────────────────────
#  SIDEBAR – flexible inputs with unit selection
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ INPUT PARAMETERS")
    
    # Bench Height
    col1, col2 = st.columns([2, 1])
    with col1:
        bh_val = st.number_input("Bench Height", value=10.0, step=0.5, format="%.2f", key="bh_val")
    with col2:
        bh_unit = st.selectbox("Unit", ["m", "ft", "cm", "inch"], index=0, key="bh_unit")
    bench_height_m = length_to_m(bh_val, bh_unit)
    
    # Hole Diameter
    col1, col2 = st.columns([2, 1])
    with col1:
        hd_val = st.number_input("Hole Diameter", value=0.115, step=0.005, format="%.4f", key="hd_val")
    with col2:
        hd_unit = st.selectbox("Unit", ["m", "mm", "inch", "ft"], index=0, key="hd_unit")
    hole_diameter_m = length_to_m(hd_val, hd_unit)
    
    # Rock Density
    col1, col2 = st.columns([2, 1])
    with col1:
        rd_val = st.number_input("Rock Density", value=2.7, step=0.1, format="%.2f", key="rd_val")
    with col2:
        rd_unit = st.selectbox("Unit", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"], index=0, key="rd_unit")
    rock_density_kgpm3 = density_to_kgpm3(rd_val, rd_unit)
    
    # Explosive Density
    col1, col2 = st.columns([2, 1])
    with col1:
        ed_val = st.number_input("Explosive Density", value=0.85, step=0.05, format="%.2f", key="ed_val")
    with col2:
        ed_unit = st.selectbox("Unit", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"], index=0, key="ed_unit")
    explosive_density_kgpm3 = density_to_kgpm3(ed_val, ed_unit)
    
    # Bench Area
    col1, col2 = st.columns([2, 1])
    with col1:
        area_val = st.number_input("Bench Area", value=5000.0, step=100.0, format="%.1f", key="area_val")
    with col2:
        area_unit = st.selectbox("Unit", ["m²", "ft²", "ac", "ha"], index=0, key="area_unit")
    area_m2 = area_to_m2(area_val, area_unit)
    
    # Unit Cost (always $/tonne)
    unit_cost = st.number_input("Explosive Unit Cost ($/t)", min_value=0.0, value=450.0, step=10.0, format="%.2f", key="unit_cost")
    
    # Output unit preferences
    st.markdown("---")
    st.markdown("### 📐 DISPLAY UNITS")
    length_display_unit = st.selectbox("Show lengths in", ["m", "ft", "inch"], index=0, key="len_disp")
    area_display_unit = st.selectbox("Show areas in", ["m²", "ft²", "ac"], index=0, key="area_disp")
    density_display_unit = st.selectbox("Show density in", ["t/m³", "kg/m³", "lb/ft³"], index=0, key="dens_disp")
    
    run_btn = st.button("CALCULATE", use_container_width=True)

# ─────────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────────

# Logo (replace URL with your actual image link)
logo_url = "https://via.placeholder.com/200x80?text=MINING+LOGO"  # CHANGE THIS
st.markdown(f"""
<div class="logo-container">
    <img src="{logo_url}" class="logo-img" alt="Company Logo">
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="motto">BLAST LIKE A PRO, SAVE LIKE A BOSS</div>', unsafe_allow_html=True)

st.title("💥 Blast Design & Cost Estimation")
st.caption("Open-Pit Mining | Drill & Blast Engineering Tool | Flexible Units")

# Optional unit converter expander (can be removed if not wanted)
with st.expander("🔄 UNIT CONVERTER (Quick conversion tool)"):
    conv_type = st.selectbox("Conversion type", ["Length", "Area", "Density"])
    val = st.number_input("Value", value=1.0, key="conv_val")
    if conv_type == "Length":
        from_u = st.selectbox("From", ["m", "ft", "inch", "cm", "mm"], key="len_from")
        to_u = st.selectbox("To", ["m", "ft", "inch", "cm", "mm"], index=1, key="len_to")
        result = length_to_m(val, from_u)
        result = m_to_length(result, to_u)
    elif conv_type == "Area":
        from_u = st.selectbox("From", ["m²", "ft²", "ac", "ha"], key="area_from")
        to_u = st.selectbox("To", ["m²", "ft²", "ac", "ha"], key="area_to")
        result = area_to_m2(val, from_u)
        result = m2_to_area(result, to_u)
    else:  # Density
        from_u = st.selectbox("From", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"], key="dens_from")
        to_u = st.selectbox("To", ["t/m³", "kg/m³", "g/cm³", "lb/ft³"], key="dens_to")
        kgm3 = density_to_kgpm3(val, from_u)
        result = kgpm3_to_density(kgm3, to_u)
    st.success(f"Result: {result:.6f} {to_u}")

# Run calculation when button is pressed
if run_btn:
    inputs_si = dict(
        bench_height_m=bench_height_m,
        hole_diameter_m=hole_diameter_m,
        rock_density_kgpm3=rock_density_kgpm3,
        explosive_density_kgpm3=explosive_density_kgpm3,
        unit_cost_per_tonne=unit_cost,
        area_m2=area_m2,
    )
    results_si = run_design(**inputs_si)
    st.session_state["results_si"] = results_si
    st.session_state["inputs_si"] = inputs_si
    st.session_state["display_units"] = {
        "length": length_display_unit,
        "area": area_display_unit,
        "density": density_display_unit,
    }

# Retrieve from session state
results_si = st.session_state["results_si"]
inputs_si = st.session_state["inputs_si"]
disp = st.session_state["display_units"]

# Helper functions for display
def disp_length(m):
    return m_to_length(m, disp["length"])
def disp_area(m2):
    return m2_to_area(m2, disp["area"])
def disp_density(kgpm3):
    return kgpm3_to_density(kgpm3, disp["density"])

# ─────────────────────────────────────────────────────────────
#  OUTPUT TABLES WITH CONVERTED UNITS
# ─────────────────────────────────────────────────────────────
st.subheader("📊 Drill Design Parameters")
drill_data = pd.DataFrame([
    ("Burden", f"{disp_length(results_si['burden_m']):.3f} {disp['length']}"),
    ("Spacing", f"{disp_length(results_si['spacing_m']):.3f} {disp['length']}"),
    ("Number of Holes", results_si['holes']),
    ("Charge per Hole", f"{results_si['charge_tonnes']:.4f} t"),
], columns=["Parameter", "Value"])
st.table(drill_data)

st.subheader("📦 Explosive & Rock Volume")
rock_data = pd.DataFrame([
    ("Total Explosive", f"{results_si['total_exp_tonnes']:.3f} t"),
    ("Rock Volume", f"{disp_area(results_si['rock_vol_m3']):.2f} {disp['area']}"),
    ("Powder Factor", f"{results_si['pf']:.4f} t/m³"),
], columns=["Parameter", "Value"])
st.table(rock_data)

st.subheader("💰 Cost Estimation")
st.markdown(f"""
<div class="cost-block">
    <div class="cost-label">Total Blasting Cost — Bench Estimate</div>
    <div class="cost-value">${results_si['cost']:,.2f}</div>
    <div class="cost-sub">
        Based on {results_si['total_exp_tonnes']:.3f} t explosive × ${inputs_si['unit_cost_per_tonne']:.2f}/t
    </div>
</div>
""", unsafe_allow_html=True)

st.subheader("📋 Input Summary")
input_data = pd.DataFrame([
    ("Bench Height", f"{disp_length(inputs_si['bench_height_m']):.1f} {disp['length']}"),
    ("Hole Diameter", f"{disp_length(inputs_si['hole_diameter_m']):.4f} {disp['length']}"),
    ("Rock Density", f"{disp_density(inputs_si['rock_density_kgpm3']):.2f} {disp['density']}"),
    ("Explosive Density", f"{disp_density(inputs_si['explosive_density_kgpm3']):.2f} {disp['density']}"),
    ("Bench Area", f"{disp_area(inputs_si['area_m2']):.1f} {disp['area']}"),
    ("Unit Cost", f"${inputs_si['unit_cost_per_tonne']:.2f} /t"),
], columns=["Parameter", "Value"])
st.table(input_data)

# ─────────────────────────────────────────────────────────────
#  DOWNLOAD REPORTS (TXT & EXCEL)
# ─────────────────────────────────────────────────────────────
def generate_report_text():
    ts = datetime.now().strftime("%d %B %Y   %H:%M:%S")
    return f"""
BLAST DESIGN REPORT
{ts}

=== DRILL DESIGN ===
Burden               : {disp_length(results_si['burden_m']):.3f} {disp['length']}
Spacing              : {disp_length(results_si['spacing_m']):.3f} {disp['length']}
Number of Holes      : {results_si['holes']}
Charge per Hole      : {results_si['charge_tonnes']:.4f} t

=== EXPLOSIVE & ROCK ===
Total Explosive      : {results_si['total_exp_tonnes']:.3f} t
Rock Volume          : {disp_area(results_si['rock_vol_m3']):.2f} {disp['area']}
Powder Factor        : {results_si['pf']:.4f} t/m³

=== COST ===
Total Blasting Cost  : ${results_si['cost']:,.2f}

=== INPUT SUMMARY ===
Bench Height         : {disp_length(inputs_si['bench_height_m']):.1f} {disp['length']}
Hole Diameter        : {disp_length(inputs_si['hole_diameter_m']):.4f} {disp['length']}
Rock Density         : {disp_density(inputs_si['rock_density_kgpm3']):.2f} {disp['density']}
Explosive Density    : {disp_density(inputs_si['explosive_density_kgpm3']):.2f} {disp['density']}
Bench Area           : {disp_area(inputs_si['area_m2']):.1f} {disp['area']}
Unit Cost            : ${inputs_si['unit_cost_per_tonne']:.2f} /t
"""

def generate_excel_report():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Input sheet (SI values)
        pd.DataFrame([
            ("Bench Height (m)", inputs_si['bench_height_m']),
            ("Hole Diameter (m)", inputs_si['hole_diameter_m']),
            ("Rock Density (kg/m³)", inputs_si['rock_density_kgpm3']),
            ("Explosive Density (kg/m³)", inputs_si['explosive_density_kgpm3']),
            ("Bench Area (m²)", inputs_si['area_m2']),
            ("Unit Cost ($/t)", inputs_si['unit_cost_per_tonne']),
        ], columns=["Parameter", "Value (SI)"]).to_excel(writer, sheet_name="Input SI", index=False)
        
        # Results sheet (SI)
        pd.DataFrame([
            ("Burden (m)", results_si['burden_m']),
            ("Spacing (m)", results_si['spacing_m']),
            ("Number of Holes", results_si['holes']),
            ("Charge per Hole (t)", results_si['charge_tonnes']),
            ("Total Explosive (t)", results_si['total_exp_tonnes']),
            ("Rock Volume (m³)", results_si['rock_vol_m3']),
            ("Powder Factor (t/m³)", results_si['pf']),
            ("Total Cost ($)", results_si['cost']),
        ], columns=["Parameter", "Value (SI)"]).to_excel(writer, sheet_name="Results SI", index=False)
        
        # Display units sheet (for reference)
        pd.DataFrame([
            ("Length unit", disp['length']),
            ("Area unit", disp['area']),
            ("Density unit", disp['density']),
        ], columns=["Display Setting", "Unit"]).to_excel(writer, sheet_name="Display Units", index=False)
        
    output.seek(0)
    return output

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    st.download_button("📄 Download Report (TXT)", generate_report_text(),
                       file_name=f"BlastDesign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
with col_btn2:
    st.download_button("📊 Download Report (Excel)", generate_excel_report(),
                       file_name=f"BlastDesign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
