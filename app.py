import streamlit as st
import pandas as pd
import math
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="💥 Professional Blast Design Tool",
    page_icon="💥",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS (Dark + Colored UI)
# ---------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #141e30, #243b55);
    color: white;
}

h1, h2, h3, h4, h5 {
    color: #FFD700;
}

div[data-testid="metric-container"] {
    background: #1e3c72;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #00FFFF;
}

.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    font-weight: bold;
}

.stDownloadButton>button {
    background-color: #00c853;
    color: white;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("💥 Professional Blast Design Tool")
st.caption("Open Pit Mining | Drill & Blast Engineering Software")

# ---------------------------------------------------
# UNIT CONVERSION
# ---------------------------------------------------
def convert_length(value, unit):
    conversions = {
        "mm": value / 1000,
        "cm": value / 100,
        "m": value,
        "ft": value * 0.3048
    }
    return conversions[unit]

def convert_diameter(value, unit):
    conversions = {
        "mm": value / 1000,
        "cm": value / 100,
        "m": value,
        "in": value * 0.0254
    }
    return conversions[unit]

def convert_density(value, unit):
    conversions = {
        "t/m³": value,
        "kg/m³": value / 1000
    }
    return conversions[unit]

# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------
def calc_burden(diameter, rock_density):
    return 25 * diameter / rock_density

def calc_spacing(burden):
    return 1.25 * burden

def calc_holes(area, burden, spacing):
    return max(1, int(area / (burden * spacing)))

def calc_charge(diameter, height, density):
    radius = diameter / 2
    volume = math.pi * radius**2 * height
    return volume * density

# ---------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------
with st.sidebar:
    st.header("⚙️ Input Parameters")

    # Bench Height
    bench_height = st.number_input("⛰️ Bench Height", value=10.0)
    bench_unit = st.selectbox("Bench Height Unit", ["mm", "cm", "m", "ft"])

    # Hole Diameter
    hole_diameter = st.number_input("🕳️ Hole Diameter", value=115.0)
    hole_unit = st.selectbox("Hole Diameter Unit", ["mm", "cm", "m", "in"])

    # Stemming
    stemming = st.number_input("🧱 Stemming Length", value=2.0)
    stemming_unit = st.selectbox("Stemming Unit", ["mm", "cm", "m", "ft"])

    # Subdrill
    subdrill = st.number_input("🔩 Subdrill Depth", value=1.0)
    subdrill_unit = st.selectbox("Subdrill Unit", ["mm", "cm", "m", "ft"])

    # Area
    area = st.number_input("📐 Bench Area (m²)", value=5000.0)

    # Densities
    rock_density = st.number_input("🪨 Rock Density", value=2.7)
    rock_unit = st.selectbox("Rock Density Unit", ["t/m³", "kg/m³"])

    explosive_density = st.number_input("💣 Explosive Density", value=0.85)
    explosive_unit = st.selectbox("Explosive Density Unit", ["t/m³", "kg/m³"])

    # Costs
    explosive_cost = st.number_input("💵 Explosive Cost ($/t)", value=450.0)
    drilling_cost = st.number_input("⛏️ Drilling Cost ($/m)", value=50.0)
    detonator_cost = st.number_input("⚡ Detonator Cost ($/hole)", value=10.0)

    run = st.button("💥 Calculate")

# ---------------------------------------------------
# MAIN CALCULATIONS
# ---------------------------------------------------
if run:

    # Convert to SI Units
    bench_m = convert_length(bench_height, bench_unit)
    hole_m = convert_diameter(hole_diameter, hole_unit)
    stem_m = convert_length(stemming, stemming_unit)
    sub_m = convert_length(subdrill, subdrill_unit)

    rock_den = convert_density(rock_density, rock_unit)
    exp_den = convert_density(explosive_density, explosive_unit)

    # Blast Design
    burden = calc_burden(hole_m, rock_den)
    spacing = calc_spacing(burden)
    holes = calc_holes(area, burden, spacing)

    effective_height = max(0, bench_m + sub_m - stem_m)

    charge = calc_charge(hole_m, effective_height, exp_den)

    total_exp = charge * holes
    rock_volume = area * bench_m
    powder_factor = total_exp / rock_volume

    explosive_total = total_exp * explosive_cost
    drilling_total = holes * (bench_m + sub_m) * drilling_cost
    initiation_total = holes * detonator_cost

    total_cost = explosive_total + drilling_total + initiation_total

    # ---------------------------------------------------
    # METRICS
    # ---------------------------------------------------
    st.subheader("📊 Key Parameters")

    c1, c2, c3 = st.columns(3)

    c1.metric("📏 Burden", f"{burden:.2f} m")
    c2.metric("↔️ Spacing", f"{spacing:.2f} m")
    c3.metric("🕳️ Holes", holes)

    # ---------------------------------------------------
    # RESULTS TABLE
    # ---------------------------------------------------
    st.subheader("📋 Full Results")

    results = pd.DataFrame([
        ["Charge per Hole", f"{charge:.3f} t"],
        ["Total Explosive", f"{total_exp:.2f} t"],
        ["Rock Volume", f"{rock_volume:.2f} m³"],
        ["Powder Factor", f"{powder_factor:.4f} t/m³"],
        ["Explosive Cost", f"${explosive_total:,.2f}"],
        ["Drilling Cost", f"${drilling_total:,.2f}"],
        ["Initiation Cost", f"${initiation_total:,.2f}"],
        ["Total Cost", f"${total_cost:,.2f}"]
    ], columns=["Item", "Value"])

    st.dataframe(results, use_container_width=True)

    # Download CSV
    csv = results.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Results CSV",
        csv,
        "blast_results.csv",
        "text/csv"
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.caption(
    f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)
