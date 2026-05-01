import streamlit as st
import pandas as pd
import math
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="💥 Blast Design Tool",
    page_icon="💥",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:white;
}

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#141e30,#243b55);
}

h1,h2,h3,h4{
    color:#FFD700;
}

label{
    color:white !important;
    font-weight:600;
}

div[data-testid="metric-container"]{
    background:#13293d;
    border:1px solid #00e5ff;
    padding:15px;
    border-radius:15px;
}

.stButton>button{
    background:#ff1744;
    color:white;
    font-weight:bold;
    border-radius:10px;
    height:3em;
    width:100%;
}

.stDownloadButton>button{
    background:#00c853;
    color:white;
    font-weight:bold;
    border-radius:10px;
    width:100%;
}

[data-testid="stDataFrame"]{
    background:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.title("💥 Professional Blast Design Tool")
st.caption("Open Pit Mining | Drill & Blast Engineering")

# =====================================================
# CONVERSION FUNCTIONS
# =====================================================
def length_to_m(v,u):
    if u=="mm":
        return v/1000
    elif u=="cm":
        return v/100
    elif u=="m":
        return v
    elif u=="ft":
        return v*0.3048

def dia_to_m(v,u):
    if u=="mm":
        return v/1000
    elif u=="cm":
        return v/100
    elif u=="m":
        return v
    elif u=="in":
        return v*0.0254

def density_to_t(v,u):
    if u=="t/m³":
        return v
    elif u=="kg/m³":
        return v/1000

# =====================================================
# CALCULATIONS
# =====================================================
def burden_fn(d,rho):
    return 25*d/rho

def spacing_fn(b):
    return 1.25*b

def holes_fn(area,b,s):
    return max(1,int(area/(b*s)))

def charge_fn(d,h,rho):
    r=d/2
    vol=math.pi*r*r*h
    return vol*rho

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.header("⚙️ Inputs")

    # Bench Height
    c1,c2 = st.columns([3,1])
    with c1:
        bench_height = st.number_input("⛰️ Bench Height", value=10.0)
    with c2:
        bh_unit = st.selectbox("",["mm","cm","m","ft"],key="bh")

    # Hole Diameter
    c1,c2 = st.columns([3,1])
    with c1:
        hole_diameter = st.number_input("🕳️ Hole Diameter", value=115.0)
    with c2:
        hd_unit = st.selectbox("",["mm","cm","m","in"],key="hd")

    # Stemming
    c1,c2 = st.columns([3,1])
    with c1:
        stemming = st.number_input("🧱 Stemming Length", value=2.0)
    with c2:
        st_unit = st.selectbox("",["mm","cm","m","ft"],key="st")

    # Subdrill
    c1,c2 = st.columns([3,1])
    with c1:
        subdrill = st.number_input("🔩 Subdrill Depth", value=1.0)
    with c2:
        sd_unit = st.selectbox("",["mm","cm","m","ft"],key="sd")

    # Area
    area = st.number_input("📐 Bench Area (m²)", value=5000.0)

    # Rock Density
    c1,c2 = st.columns([3,1])
    with c1:
        rock_density = st.number_input("🪨 Rock Density", value=2.7)
    with c2:
        rd_unit = st.selectbox("",["t/m³","kg/m³"],key="rd")

    # Explosive Density
    c1,c2 = st.columns([3,1])
    with c1:
        explosive_density = st.number_input("💣 Explosive Density", value=0.85)
    with c2:
        ed_unit = st.selectbox("",["t/m³","kg/m³"],key="ed")

    explosive_cost = st.number_input("💵 Explosive Cost ($/t)", value=450.0)
    drilling_cost = st.number_input("⛏️ Drilling Cost ($/m)", value=50.0)
    detonator_cost = st.number_input("⚡ Detonator Cost ($/hole)", value=10.0)

    run = st.button("💥 CALCULATE")

# =====================================================
# MAIN CALCULATIONS
# =====================================================
if run:

    bench_m = length_to_m(bench_height,bh_unit)
    dia_m = dia_to_m(hole_diameter,hd_unit)
    stem_m = length_to_m(stemming,st_unit)
    sub_m = length_to_m(subdrill,sd_unit)

    rock_den = density_to_t(rock_density,rd_unit)
    exp_den = density_to_t(explosive_density,ed_unit)

    burden = burden_fn(dia_m,rock_den)
    spacing = spacing_fn(burden)
    holes = holes_fn(area,burden,spacing)

    effective_height = max(0,bench_m+sub_m-stem_m)

    charge = charge_fn(dia_m,effective_height,exp_den)

    total_exp = charge*holes
    rock_vol = area*bench_m
    powder_factor = total_exp/rock_vol

    explosive_total = total_exp*explosive_cost
    drilling_total = holes*(bench_m+sub_m)*drilling_cost
    initiation_total = holes*detonator_cost

    total_cost = explosive_total + drilling_total + initiation_total

    # =================================================
    # METRICS
    # =================================================
    st.subheader("📊 Blast Design Summary")

    a,b,c = st.columns(3)

    a.metric("📏 Burden", f"{burden:.2f} m")
    b.metric("↔️ Spacing", f"{spacing:.2f} m")
    c.metric("🕳️ Holes", holes)

    # =================================================
    # RESULTS TABLE
    # =================================================
    st.subheader("📋 Results")

    df = pd.DataFrame([
        ["Charge per Hole",f"{charge:.3f} t"],
        ["Total Explosive",f"{total_exp:.2f} t"],
        ["Rock Volume",f"{rock_vol:.2f} m³"],
        ["Powder Factor",f"{powder_factor:.4f} t/m³"],
        ["Explosive Cost",f"${explosive_total:,.2f}"],
        ["Drilling Cost",f"${drilling_total:,.2f}"],
        ["Initiation Cost",f"${initiation_total:,.2f}"],
        ["Total Cost",f"${total_cost:,.2f}"]
    ],columns=["Item","Value"])

    st.dataframe(df,use_container_width=True)

    # DOWNLOAD
    csv=df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Results",
        csv,
        "blast_results.csv",
        "text/csv"
    )

# =====================================================
# FOOTER
# =====================================================
st.caption(
    f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)
