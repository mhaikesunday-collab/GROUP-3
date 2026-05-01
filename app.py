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
# TITLE
# ---------------------------------------------------
st.title("💥 Professional Blast Design Tool")
st.caption("Open Pit Mining | Drill & Blast Engineering Software")

# ---------------------------------------------------
# UNIT CONVERSION FUNCTIONS
# ---------------------------------------------------
def length_to_m(value, unit):
    if unit == "m":
        return value
    elif unit == "ft":
        return value * 0.3048

def diameter_to_m(value, unit):
    if unit == "mm":
        return value / 1000
    elif unit == "in":
        return value * 0.0254

def density_to_t(value, unit):
    if unit == "t/m³":
        return value
    elif unit == "kg/m³":
        return value / 1000

# ---------------------------------------------------
# CALCULATION FUNCTIONS
# ---------------------------------------------------
def calc_burden(diameter, rock_density):
    return 25 * diameter / rock_density

def calc_spacing(burden):
    return 1.25 * burden

def calc_holes(area, burden, spacing):
    return max(1, int(area / (burden * spacing)))

def calc_charge_per_hole(diameter, height, explosive_density):
    radius = diameter / 2
    volume = math.pi * radius**2 * height
    return volume * explosive_density

# ---------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------
with st.sidebar:
    st.header("⚙️ Input Parameters")

    # Units
    st.subheader("🔁 Units")
    length_unit = st.selectbox("📏 Length Unit", ["m", "ft"])
    diameter_unit = st.selectbox("🕳️ Hole Diameter Unit", ["mm", "in"])
    density_unit = st.selectbox("🪨 Density Unit", ["t/m³", "kg/m³"])

    # Inputs
    st.subheader("📥 Design Inputs")

    rock_density = st.number_input(
        "🪨 Rock Density",
        min_value=0.1,
        value=2.7
    )

    bench_height = st.number_input(
        "⛰️ Bench Height",
        min_value=0.1,
        value=10.0
    )

    area = st.number_input(
        "📐 Bench Area (m²)",
        min_value=1.0,
        value=5000.0
    )

    hole_diameter = st.number_input(
        "🕳️ Hole Diameter",
        min_value=1.0,
        value=115.0
    )

    explosive_density = st.number_input(
        "💣 Explosive Density",
        min_value=0.1,
        value=0.85
    )

    stemming = st.number_input(
        "🧱 Stemming Length",
        min_value=0.0,
        value=2.0
    )

    subdrill = st.number_input(
        "🔩 Subdrill Depth",
        min_value=0.0,
        value=1.0
    )

    explosive_cost = st.number_input(
        "💵 Explosive Cost ($/t)",
        min_value=0.0,
        value=450.0
    )

    drilling_cost = st.number_input(
        "⛏️ Drilling Cost ($/m)",
        min_value=0.0,
        value=50.0
    )

    detonator_cost = st.number_input(
        "⚡ Detonator Cost ($/hole)",
        min_value=0.0,
        value=10.0
    )

    run = st.button("💥 Calculate")

# ---------------------------------------------------
# MAIN CALCULATIONS
# ---------------------------------------------------
if run:

    # Convert Units
    bench_height_m = length_to_m(bench_height, length_unit)
    stemming_m = length_to_m(stemming, length_unit)
    subdrill_m = length_to_m(subdrill, length_unit)

    hole_diameter_m = diameter_to_m(
        hole_diameter,
        diameter_unit
    )

    rock_density_t = density_to_t(
        rock_density,
        density_unit
    )

    explosive_density_t = density_to_t(
        explosive_density,
        density_unit
    )

    # Design Calculations
    burden = calc_burden(
        hole_diameter_m,
        rock_density_t
    )

    spacing = calc_spacing(burden)

    holes = calc_holes(
        area,
        burden,
        spacing
    )

    effective_height = max(
        0,
        bench_height_m +
        subdrill_m -
        stemming_m
    )

    charge = calc_charge_per_hole(
        hole_diameter_m,
        effective_height,
        explosive_density_t
    )

    total_explosive = charge * holes

    rock_volume = area * bench_height_m

    powder_factor = total_explosive / rock_volume

    explosive_total_cost = (
        total_explosive * explosive_cost
    )

    drilling_total_cost = (
        holes *
        (bench_height_m + subdrill_m) *
        drilling_cost
    )

    initiation_cost = holes * detonator_cost

    total_cost = (
        explosive_total_cost +
        drilling_total_cost +
        initiation_cost
    )

    # ---------------------------------------------------
    # DISPLAY METRICS
    # ---------------------------------------------------
    st.subheader("📊 Key Design Parameters")

    col1, col2, col3 = st.columns(3)

    col1.metric("📏 Burden", f"{burden:.2f} m")
    col2.metric("↔️ Spacing", f"{spacing:.2f} m")
    col3.metric("🕳️ Holes", holes)

    # ---------------------------------------------------
    # RESULTS TABLE
    # ---------------------------------------------------
    st.subheader("📋 Full Results")

    results = pd.DataFrame([
        ["Charge per Hole", f"{charge:.3f} t"],
        ["Total Explosive", f"{total_explosive:.2f} t"],
        ["Rock Volume", f"{rock_volume:.2f} m³"],
        ["Powder Factor", f"{powder_factor:.4f} t/m³"],
        ["Explosive Cost", f"${explosive_total_cost:,.2f}"],
        ["Drilling Cost", f"${drilling_total_cost:,.2f}"],
        ["Initiation Cost", f"${initiation_cost:,.2f}"],
        ["Total Cost", f"${total_cost:,.2f}"]
    ], columns=["Item", "Value"])

    st.table(results)

    # ---------------------------------------------------
    # DOWNLOAD BUTTON
    # ---------------------------------------------------
    csv = results.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Results CSV",
        data=csv,
        file_name="blast_results.csv",
        mime="text/csv"
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.caption(
    f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)
