import math
import streamlit as st
from datetime import datetime
import pandas as pd

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
#  GLOBAL CSS (shortened for clarity, keep your full CSS here)
# ─────────────────────────────────────────────────────────────
st.markdown("""<style>/* your CSS here */</style>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  BACKEND FUNCTIONS
# ─────────────────────────────────────────────────────────────
def calc_burden(diameter: float, rock_density: float) -> float:
    return 25 * diameter * (1 / rock_density)

def calc_spacing(burden: float) -> float:
    return 1.25 * burden

def calc_holes(area: float, burden: float, spacing: float) -> int:
    return max(1, int(area / (burden * spacing)))

def calc_charge_per_hole(diameter: float, bench_height: float, explosive_density: float) -> float:
    radius = diameter / 2
    volume = math.pi * (radius ** 2) * bench_height
    return volume * explosive_density

def calc_powder_factor(total_explosive: float, rock_volume: float) -> float:
    return total_explosive / rock_volume

def calc_total_cost(total_explosive: float, unit_cost: float) -> float:
    return total_explosive * unit_cost

# NEW FUNCTIONS
def calc_effective_height(bench_height: float, stemming: float, subdrill: float) -> float:
    return max(0.0, bench_height + subdrill - stemming)

def calc_charge_per_hole_extended(diameter: float, effective_height: float, explosive_density: float) -> float:
    radius = diameter / 2
    volume = math.pi * (radius ** 2) * effective_height
    return volume * explosive_density

def calc_drilling_cost(holes: int, hole_depth: float, cost_per_m: float) -> float:
    return holes * hole_depth * cost_per_m

def calc_initiation_cost(holes: int, detonator_cost: float) -> float:
    return holes * detonator_cost

def calc_explosive_energy(charge_tonnes: float, energy_mj_per_kg: float) -> float:
    return charge_tonnes * 1000 * energy_mj_per_kg

def calc_vibration_ppv(charge_kg: float, distance_m: float, k: float = 1000, alpha: float = 1.6) -> float:
    return k * (charge_kg ** 0.5) / (distance_m ** alpha)

def run_design(bench_height, hole_diameter, rock_density,
               explosive_density, unit_cost, area,
               stemming_length, subdrill_depth,
               drilling_cost_m, detonator_cost,
               explosive_energy, distance_to_struct):

    burden      = calc_burden(hole_diameter, rock_density)
    spacing     = calc_spacing(burden)
    holes       = calc_holes(area, burden, spacing)

    effective_h = calc_effective_height(bench_height, stemming_length, subdrill_depth)
    charge      = calc_charge_per_hole_extended(hole_diameter, effective_h, explosive_density)

    total_exp   = charge * holes
    rock_vol    = area * bench_height
    pf          = calc_powder_factor(total_exp, rock_vol)
    explosive_cost = calc_total_cost(total_exp, unit_cost)

    drilling_cost   = calc_drilling_cost(holes, bench_height + subdrill_depth, drilling_cost_m)
    initiation_cost = calc_initiation_cost(holes, detonator_cost)
    total_cost      = explosive_cost + drilling_cost + initiation_cost

    energy_per_hole = calc_explosive_energy(charge, explosive_energy)
    ppv             = calc_vibration_ppv(charge * 1000, distance_to_struct)

    return dict(burden=burden, spacing=spacing, holes=holes,
                charge=charge, total_exp=total_exp, rock_vol=rock_vol,
                pf=pf, explosive_cost=explosive_cost,
                drilling_cost=drilling_cost, initiation_cost=initiation_cost,
                cost=total_cost, energy_per_hole=energy_per_hole, ppv=ppv)

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

    # NEW INPUTS
    stemming_length   = st.number_input("Stemming Length (m)", min_value=0.0, value=0.0, step=0.5)
    subdrill_depth    = st.number_input("Subdrill Depth (m)", min_value=0.0, value=0.0, step=0.5)
    drilling_cost_m   = st.number_input("Drilling Cost ($/m)", min_value=0.0, value=50.0, step=1.0)
    detonator_cost    = st.number_input("Detonator Cost ($/hole)", min_value=0.0, value=10.0, step=1.0)
    explosive_energy  = st.number_input("Explosive Energy (MJ/kg)", min_value=1.0, value=3.8, step=0.1)
    distance_to_struct= st.number_input("Distance to Structure (m)", min_value=1.0, value=100.0, step=1.0)

    run_btn = st.button("CALCULATE")

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────
st.title("💥 Blast Design & Cost Estimation")
st.caption("Open-Pit Mining | Drill & Blast Engineering Tool")

if run_btn or "results" not in st.session_state:
    inputs = dict(
        bench_height=bench_height,
        hole_diameter=hole_diameter,
        rock_density=rock_density,
        explosive_density=explosive_density,
        unit_cost=unit_cost,
        area=area,
        stemming_length=stemming_length,
        subdrill_depth=subdrill_depth,
        drilling_cost_m=drilling_cost_m,
        detonator_cost=detonator_cost,
        explosive_energy=explosive_energy,
        distance_to_struct=distance_to_struct,
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
st.table(pd.DataFrame([
    ("Burden", f"{results['burden']:.3f} m"),
    ("Spacing", f"{results['spacing']:.3f} m"),
    ("Number of Holes", results['holes']),
    ("Charge per Hole", f"{results['charge']:.4f} t"),
], columns=["Parameter", "Value"]))

st.subheader("📦 Explosive & Rock Volume")
st.table(pd.DataFrame([
    ("Total Explosive", f"{results['total_exp']:.3f} t"),
    ("Rock Volume", f"{results['rock_vol']:.2f} m³"),
    ("Powder Factor", f"{results['pf']:.4f} t/m³"),
], columns=["Parameter", "Value"]))

st.subheader("💰 Cost Estimation")
st.table(pd.DataFrame([
    ("Explosive Cost", f"${results['explosive_cost']:,.2f}"),
    ("Drilling Cost", f"${results['drilling_cost']:,.2f}"),
    ("Initiation Cost", f"${results['initiation_cost']:,.2f}"),
    ("Total Cost", f"${results['cost']:,.2f}"),
], columns=["Component", "Value"]
