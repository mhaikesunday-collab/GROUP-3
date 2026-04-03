"""
BLAST DESIGN & COST ESTIMATION TOOL
Open-Pit Mining | Streamlit App
Author: mhaike
"""

import math
import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO

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
#  GLOBAL CSS  – full dark theme + background image + motto
# ─────────────────────────────────────────────────────────────
# NOTE: Replace the background image URL with a publicly accessible one.
# For Google Drive, you need a direct link (e.g., via raw.githubusercontent.com or other hosting).
# Example: url('https://your-image-host.com/mining-background.jpg')
# If no image, the dark theme remains.
background_image_url = ""  # <-- PUT YOUR DIRECT IMAGE URL HERE

bg_style = ""
if background_image_url:
    bg_style = f"""
    [data-testid="stAppViewContainer"] {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(4, 16, 28, 0.85);  /* dark overlay for readability */
        z-index: -1;
    }}
    """
else:
    bg_style = """
    [data-testid="stAppViewContainer"] {
        background-color: #04101C !important;
    }
    """

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

:root {{
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
}}

{bg_style}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: var(--bg-panel) !important;
    border-right: 1px solid var(--border);
}}

/* Hide Streamlit default elements */
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}

/* Headers */
h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
    color: var(--accent-blue) !important;
    font-family: var(--mono) !important;
    letter-spacing: 1px;
}}

/* Subheader */
.stSubheader {{
    color: var(--accent-green) !important;
    font-family: var(--mono) !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
    margin-top: 20px;
}}

/* Tables */
table {{
    width: 100%;
    background-color: var(--bg-card) !important;
    border-collapse: collapse;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}}

th {{
    background-color: #0D2A3E !important;
    color: var(--accent-green) !important;
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 600;
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}}

td {{
    padding: 8px 12px;
    color: var(--text-main) !important;
    font-family: var(--body);
    font-size: 14px;
    border-bottom: 1px solid var(--border);
}}

tr:last-child td {{
    border-bottom: none;
}}

/* Cost highlight block */
.cost-block {{
    background: linear-gradient(120deg, #062A3D, #063320);
    border: 1px solid var(--accent-green);
    border-radius: 8px;
    padding: 18px 24px;
    margin: 20px 0;
}}
.cost-label {{
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: 2px;
    color: var(--accent-green);
    text-transform: uppercase;
    margin-bottom: 8px;
}}
.cost-value {{
    font-family: var(--mono);
    font-size: 38px;
    color: var(--accent-green);
    font-weight: bold;
}}
.cost-sub {{
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 6px;
}}

/* Motto styling */
.motto {{
    text-align: center;
    font-family: var(--mono);
    font-size: 28px;
    font-weight: bold;
    letter-spacing: 4px;
    color: var(--accent-green);
    text-shadow: 0 0 8px rgba(15,191,106,0.5);
    margin: 20px 0 30px 0;
    padding: 15px;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    background: rgba(4,16,28,0.6);
    backdrop-filter: blur(2px);
}}

/* Download buttons */
.stDownloadButton button {{
    background: linear-gradient(135deg, var(--mid-blue), var(--mid-green)) !important;
    color: white !important;
    font-family: var(--mono);
    font-size: 13px;
    letter-spacing: 2px;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    transition: 0.2s;
}}

/* Sidebar inputs */
[data-testid="stSidebar"] .stNumberInput input {{
    background-color: #040E19 !important;
    color: var(--accent-blue) !important;
    border: 1px solid var(--border);
    border-radius: 4px;
}}
[data-testid="stSidebar"] label {{
    color: var(--text-label) !important;
}}
[data-testid="stSidebar"] .stButton button {{
    background: linear-gradient(135deg, var(--mid-blue), var(--mid-green));
    color: white;
    font-family: var(--mono);
    width: 100%;
}}

/* Unit converter styling */
.converter-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    margin: 10px 0;
}}
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

def generate_excel_report(inputs: dict, results: dict) -> BytesIO:
    """Create an Excel file with multiple sheets using xlsxwriter engine."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        input_df = pd.DataFrame([
            ("Bench Height (m)", inputs['bench_height']),
            ("Hole Diameter (m)", inputs['hole_diameter']),
            ("Rock Density (t/m³)", inputs['rock_density']),
            ("Explosive Density (t/m³)", inputs['explosive_density']),
            ("Bench Area (m²)", inputs['area']),
            ("Unit Cost ($/t)", inputs['unit_cost']),
        ], columns=["Parameter", "Value"])
        input_df.to_excel(writer, sheet_name="Input Summary", index=False)
        
        drill_df = pd.DataFrame([
            ("Burden (m)", results['burden']),
            ("Spacing (m)", results['spacing']),
            ("Number of Holes", results['holes']),
            ("Charge per Hole (t)", results['charge']),
        ], columns=["Parameter", "Value"])
        drill_df.to_excel(writer, sheet_name="Drill Design", index=False)
        
        rock_df = pd.DataFrame([
            ("Total Explosive (t)", results['total_exp']),
            ("Rock Volume (m³)", results['rock_vol']),
            ("Powder Factor (t/m³)", results['pf']),
        ], columns=["Parameter", "Value"])
        rock_df.to_excel(writer, sheet_name="Explosive & Rock", index=False)
        
        cost_df = pd.DataFrame([
            ("Total Blasting Cost ($)", results['cost']),
            ("Explosive Unit Cost ($/t)", inputs['unit_cost']),
            ("Total Explosive Used (t)", results['total_exp']),
        ], columns=["Parameter", "Value"])
        cost_df.to_excel(writer, sheet_name="Cost Summary", index=False)
        
    output.seek(0)
    return output

# ─────────────────────────────────────────────────────────────
#  UNIT CONVERSION FUNCTIONS
# ─────────────────────────────────────────────────────────────
def convert_length(value, from_unit, to_unit):
    # meters base
    to_m = {
        "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
        "inch": 0.0254, "ft": 0.3048, "yd": 0.9144
    }
    return value * to_m[from_unit] / to_m[to_unit]

def convert_mass(value, from_unit, to_unit):
    # kilograms base
    to_kg = {
        "g": 0.001, "kg": 1.0, "t": 1000.0, "lb": 0.453592, "oz": 0.0283495
    }
    return value * to_kg[from_unit] / to_kg[to_unit]

def convert_volume(value, from_unit, to_unit):
    # cubic meters base
    to_m3 = {
        "m³": 1.0, "L": 0.001, "gal_us": 0.00378541, "gal_uk": 0.00454609,
        "ft³": 0.0283168, "in³": 1.6387e-5
    }
    return value * to_m3[from_unit] / to_m3[to_unit]

def convert_area(value, from_unit, to_unit):
    # square meters base
    to_m2 = {
        "m²": 1.0, "km²": 1e6, "ha": 10000.0, "ft²": 0.092903, "ac": 4046.86
    }
    return value * to_m2[from_unit] / to_m2[to_unit]

def convert_density(value, from_unit, to_unit):
    # kg/m³ base
    to_kgm3 = {
        "kg/m³": 1.0, "g/cm³": 1000.0, "t/m³": 1000.0, "lb/ft³": 16.0185
    }
    return value * to_kgm3[from_unit] / to_kgm3[to_unit]

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

# Motto in capitals
st.markdown('<div class="motto">BLAST LIKE A PRO, SAVE LIKE A BOSS</div>', unsafe_allow_html=True)

# Unit Converter Expander
with st.expander("🔄 UNIT CONVERTER - Convert between common mining units"):
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    conv_type = st.selectbox("Select conversion type", ["Length", "Mass", "Volume", "Area", "Density"])
    
    col_conv1, col_conv2, col_conv3 = st.columns(3)
    with col_conv1:
        value_in = st.number_input("Value to convert", value=1.0, step=0.1, key="conv_val")
    with col_conv2:
        if conv_type == "Length":
            from_unit = st.selectbox("From", ["mm", "cm", "m", "km", "inch", "ft", "yd"])
            to_unit = st.selectbox("To", ["mm", "cm", "m", "km", "inch", "ft", "yd"], index=2)
            result = convert_length(value_in, from_unit, to_unit)
        elif conv_type == "Mass":
            from_unit = st.selectbox("From", ["g", "kg", "t", "lb", "oz"])
            to_unit = st.selectbox("To", ["g", "kg", "t", "lb", "oz"], index=1)
            result = convert_mass(value_in, from_unit, to_unit)
        elif conv_type == "Volume":
            from_unit = st.selectbox("From", ["m³", "L", "gal_us", "gal_uk", "ft³", "in³"])
            to_unit = st.selectbox("To", ["m³", "L", "gal_us", "gal_uk", "ft³", "in³"])
            result = convert_volume(value_in, from_unit, to_unit)
        elif conv_type == "Area":
            from_unit = st.selectbox("From", ["m²", "km²", "ha", "ft²", "ac"])
            to_unit = st.selectbox("To", ["m²", "km²", "ha", "ft²", "ac"])
            result = convert_area(value_in, from_unit, to_unit)
        elif conv_type == "Density":
            from_unit = st.selectbox("From", ["kg/m³", "g/cm³", "t/m³", "lb/ft³"])
            to_unit = st.selectbox("To", ["kg/m³", "g/cm³", "t/m³", "lb/ft³"])
            result = convert_density(value_in, from_unit, to_unit)
    with col_conv3:
        st.metric("Converted value", f"{result:.6f}")
    st.markdown('</div>', unsafe_allow_html=True)

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
drill_data = pd.DataFrame([
    ("Burden", f"{results['burden']:.3f} m"),
    ("Spacing", f"{results['spacing']:.3f} m"),
    ("Number of Holes", results['holes']),
    ("Charge per Hole", f"{results['charge']:.4f} t"),
], columns=["Parameter", "Value"])
st.table(drill_data)

st.subheader("📦 Explosive & Rock Volume")
rock_data = pd.DataFrame([
    ("Total Explosive", f"{results['total_exp']:.3f} t"),
    ("Rock Volume", f"{results['rock_vol']:.2f} m³"),
    ("Powder Factor", f"{results['pf']:.4f} t/m³"),
], columns=["Parameter", "Value"])
st.table(rock_data)

st.subheader("💰 Cost Estimation")
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
#  DOWNLOAD BUTTONS
# ─────────────────────────────────────────────────────────────
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    report_text = generate_report_text(inputs, results)
    st.download_button(
        "📄 Download Report (TXT)",
        report_text,
        file_name=f"BlastDesign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
    )

with col_btn2:
    excel_data = generate_excel_report(inputs, results)
    st.download_button(
        "📊 Download Report (Excel)",
        excel_data,
        file_name=f"BlastDesign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
