import math
import streamlit as st
from datetime import datetime
import pandas as pd

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
# SIMPLE CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
body {
    font-family: Arial, sans-serif;
}
div[data-testid="stMetric"] {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────────────────────
def calc_burden(diameter, rock_density):
    return 25 * diameter / rock_density

def calc_spacing(burden):
    return 1.25 * burden

def calc_holes(area, burden, spacing):
    return max(1, int(area / (burden * spacing)))

def calc_effective_height(bench_height, stemming, subdrill):
    return max(0, bench_height + subdrill - stemming)

def calc_charge_per_hole(diameter, effective_height, explosive_density):
    radius = diameter / 2
    volume = math.pi * radius**2 * effective_height
    return volume * explosive_density

def calc_powder_factor(total_explosive, rock_volume):
    return total_explosive / rock_volume if rock_volume > 0 else 0

def calc_total_cost(total_explosive, unit_cost):
    return total_explosive * unit_cost

def calc_drilling_cost(holes, depth, cost_per_m):
    return holes * depth * cost_per_m

def calc_initiation_cost(holes, detonator_cost):
    return holes * detonator_cost

def calc_explosive_energy(charge_tonnes, energy_mj_per_kg):
    return charge_tonnes * 1000 * energy_mj_per_kg

def calc_vibration_ppv(charge_kg, distance_m, k=1000, alpha=1.6):
    return k * (charge_kg**0.5) / (distance_m**alpha)

def run_design(
    bench_height, hole_diameter, rock_density,
    explosive_density, unit_cost, area,
    stemming_length, subdrill_depth,
    drilling_cost_m, detonator_cost,
    explosive_energy, distance_to_struct
):
    burden = calc_burden(hole_diameter, rock_density)
    spacing = calc_spacing(burden)
    holes = calc_holes(area, burden, spacing)

    effective_h = calc_effective_height(
        bench_height, stemming_length, subdrill_depth
    )

    charge = calc_charge_per_hole(
        hole_diameter, effective_h, explosive_density
    )

    total_exp = charge * holes
    rock_vol = area * bench_height
    pf = calc_powder_factor(total_exp, rock_vol)

    explosive_cost = calc_total_cost(total_exp, unit_cost)
    drilling_cost = calc_drilling_cost(
        holes, bench_height + subdrill_depth, drilling_cost_m
    )

    initiation_cost = calc_initiation_cost(
        holes, detonator_cost
    )

    total_cost = explosive_cost + drilling_cost + initiation_cost

    energy_per_hole = calc_explosive_energy(
        charge, explosive_energy
    )

    ppv = calc_vibration_ppv(
        charge * 1000, distance_to_struct
    )

    return {
        "burden": burden,
        "spacing": spacing,
        "holes": holes,
        "charge": charge,
        "total_exp": total_exp,
        "rock_vol": rock_vol,
        "pf": pf,
        "explosive_cost": explosive_cost,
        "drilling_cost": drilling_cost,
        "initiation_cost": initiation_cost,
        "cost": total_cost,
        "energy_per_hole": energy_per_hole,
        "ppv": ppv
    }

# ─────────────────────────────────────────────────────────────
# SIDEBAR INPUTS
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Input Parameters")

    rock_density = st.number_input(
        "Rock Density (t/m³)", 0.1, value=2.7
    )

    bench_height = st.number_input(
        "Bench Height (m)", 0.1, value=10.0
    )

    area = st.number_input(
        "Bench Area (m²)", 1.0, value=5000.0
    )

    hole_diameter = st.number_input(
        "Hole Diameter (m)", 0.01, value=0.115
    )

    explosive_density = st.number_input(
        "Explosive Density (t/m³)", 0.1, value=0.85
    )

    unit_cost = st.number_input(
        "Explosive Cost ($/t)", 0.0, value=450.0
    )

    stemming_length = st.number_input(
        "Stemming Length (m)", 0.0, value=2.0
    )

    subdrill_depth = st.number_input(
        "Subdrill Depth (m)", 0.0, value=1.0
    )

    drilling_cost_m = st.number_input(
        "Drilling Cost ($/m)", 0.0, value=50.0
    )

    detonator_cost = st.number_input(
        "Detonator Cost ($/hole)", 0.0, value=10.0
    )

    explosive_energy = st.number_input(
        "Explosive Energy (MJ/kg)", 1.0, value=3.8
    )

    distance_to_struct = st.number_input(
        "Distance to Structure (m)", 1.0, value=100.0
    )

    run_btn = st.button("💥 Calculate")

# ─────────────────────────────────────────────────────────────
# MAIN TITLE
# ─────────────────────────────────────────────────────────────
st.title("💥 Blast Design & Cost Estimation Tool")
st.caption("Open Pit Mining | Drill & Blast Engineering")

# ─────────────────────────────────────────────────────────────
# RUN CALCULATION
# ─────────────────────────────────────────────────────────────
if run_btn or "results" not in st.session_state:

    results = run_design(
        bench_height,
        hole_diameter,
        rock_density,
        explosive_density,
        unit_cost,
        area,
        stemming_length,
        subdrill_depth,
        drilling_cost_m,
        detonator_cost,
        explosive_energy,
        distance_to_struct
    )

    st.session_state["results"] = results

results = st.session_state["results"]

# ─────────────────────────────────────────────────────────────
# OUTPUT TABLES
# ─────────────────────────────────────────────────────────────
st.subheader("📊 Drill Design Parameters")

df1 = pd.DataFrame([
    ["Burden", f"{results['burden']:.2f} m"],
    ["Spacing", f"{results['spacing']:.2f} m"],
    ["Number of Holes", results["holes"]],
    ["Charge per Hole", f"{results['charge']:.3f} t"]
], columns=["Parameter", "Value"])

st.table(df1)

# ------------------------------------------------------------

st.subheader("📦 Explosive & Rock Volume")

df2 = pd.DataFrame([
    ["Total Explosive", f"{results['total_exp']:.2f} t"],
    ["Rock Volume", f"{results['rock_vol']:.2f} m³"],
    ["Powder Factor", f"{results['pf']:.4f} t/m³"]
], columns=["Parameter", "Value"])

st.table(df2)

# ------------------------------------------------------------

st.subheader("💰 Cost Estimation")

df3 = pd.DataFrame([
    ["Explosive Cost", f"${results['explosive_cost']:,.2f}"],
    ["Drilling Cost", f"${results['drilling_cost']:,.2f}"],
    ["Initiation Cost", f"${results['initiation_cost']:,.2f}"],
    ["Total Cost", f"${results['cost']:,.2f}"]
], columns=["Parameter", "Value"])

st.table(df3)

# ------------------------------------------------------------

st.subheader("⚡ Blast Performance")

df4 = pd.DataFrame([
    ["Energy per Hole", f"{results['energy_per_hole']:.2f} MJ"],
    ["Predicted PPV", f"{results['ppv']:.2f} mm/s"]
], columns=["Parameter", "Value"])

st.table(df4)

# ------------------------------------------------------------

st.caption(
    f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)
