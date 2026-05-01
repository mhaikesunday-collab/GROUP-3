import streamlit as st
import pandas as pd
import math
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Blast Design Tool",
    page_icon="💥",
    layout="wide"
)

# =====================================================
# THEME SETTINGS (SESSION STATE)
# =====================================================
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

def apply_theme(theme):
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp {background: #0f172a; color: white;}
        section[data-testid="stSidebar"] {background: #111827;}
        h1,h2,h3 {color: #facc15;}
        label {color: white !important;}
        </style>
        """, unsafe_allow_html=True)

    elif theme == "Light":
        st.markdown("""
        <style>
        .stApp {background: #f8fafc; color: black;}
        section[data-testid="stSidebar"] {background: #e2e8f0;}
        h1,h2,h3 {color: #1e3a8a;}
        label {color: black !important;}
        </style>
        """, unsafe_allow_html=True)

apply_theme(st.session_state.theme)

# =====================================================
# HEADER
# =====================================================
st.title("Blast Design & Cost Tool")
st.caption("Version 1.0 | Open Pit Drill & Blast Engineering")

# =====================================================
# INFO SECTION
# =====================================================
with st.expander("How to use this app"):
    st.write("""
    1. Enter all required design parameters in the left panel.  
    2. Select units for each input where applicable.  
    3. Click CALCULATE to generate blast design.  
    4. View results in a single consolidated table.  
    5. Download results for reporting.
    """)

# =====================================================
# SETTINGS
# =====================================================
with st.sidebar:
    st.header("Settings")

    st.session_state.theme = st.selectbox(
        "Theme",
        ["Dark", "Light"],
        index=["Dark","Light"].index(st.session_state.theme)
    )

    st.markdown("---")
    st.write("App Version: 1.0")

# =====================================================
# UNIT CONVERSIONS
# =====================================================
def length(v,u):
    if v < 0: return None
    if u=="mm": return v/1000
    if u=="cm": return v/100
    if u=="m": return v
    if u=="ft": return v*0.3048

def diameter(v,u):
    if v < 0: return None
    if u=="mm": return v/1000
    if u=="cm": return v/100
    if u=="m": return v
    if u=="in": return v*0.0254

def density(v,u):
    if v < 0: return None
    if u=="t/m³": return v
    if u=="kg/m³": return v/1000

# =====================================================
# CALCULATIONS
# =====================================================
def burden(d,r): return 25*d/r if r>0 else 0
def spacing(b): return 1.25*b
def holes(a,b,s): return max(1,int(a/(b*s))) if b>0 and s>0 else 1

def charge(d,h,r):
    if d<=0 or h<=0 or r<=0:
        return 0
    return math.pi*(d/2)**2*h*r

# =====================================================
# INPUTS
# =====================================================
with st.sidebar:

    st.header("Inputs")

    bench = st.number_input("Bench Height", min_value=0.0, value=10.0)
    bu = st.selectbox("Bench Unit", ["mm","cm","m","ft"])

    dia = st.number_input("Hole Diameter", min_value=0.0, value=115.0)
    du = st.selectbox("Diameter Unit", ["mm","cm","m","in"])

    area = st.number_input("Bench Area (m²)", min_value=0.0, value=5000.0)

    rock = st.number_input("Rock Density", min_value=0.0, value=2.7)
    ru = st.selectbox("Rock Unit", ["t/m³","kg/m³"])

    exp = st.number_input("Explosive Density", min_value=0.0, value=0.85)
    eu = st.selectbox("Explosive Unit", ["t/m³","kg/m³"])

    stemming = st.number_input("Stemming", min_value=0.0, value=2.0)
    su = st.selectbox("Stemming Unit", ["mm","cm","m","ft"])

    sub = st.number_input("Subdrill", min_value=0.0, value=1.0)
    subu = st.selectbox("Subdrill Unit", ["mm","cm","m","ft"])

    expl_cost = st.number_input("Explosive Cost ($/t)", min_value=0.0, value=450.0)
    drill_cost = st.number_input("Drilling Cost ($/m)", min_value=0.0, value=50.0)
    det_cost = st.number_input("Detonator Cost ($/hole)", min_value=0.0, value=10.0)

    run = st.button("Calculate")

# =====================================================
# MAIN
# =====================================================
if run:

    bench_m = length(bench,bu)
    dia_m = diameter(dia,du)
    stem_m = length(stemming,su)
    sub_m = length(sub,subu)

    rock_d = density(rock,ru)
    exp_d = density(exp,eu)

    if None in [bench_m,dia_m,stem_m,sub_m,rock_d,exp_d]:
        st.error("Invalid negative input detected")
        st.stop()

    b = burden(dia_m,rock_d)
    s = spacing(b)
    h = holes(area,b,s)

    eff_h = max(0,bench_m + sub_m - stem_m)
    ch = charge(dia_m,eff_h,exp_d)

    total_exp = ch*h
    rock_vol = area*bench_m
    pf = total_exp/rock_vol if rock_vol>0 else 0

    exp_cost = total_exp*expl_cost
    drill_total = h*(bench_m+sub_m)*drill_cost
    det_total = h*det_cost

    total_cost = exp_cost + drill_total + det_total

    # SINGLE TABLE OUTPUT
    df = pd.DataFrame([
        ["Burden", f"{b:.2f} m"],
        ["Spacing", f"{s:.2f} m"],
        ["Holes", h],
        ["Charge per Hole", f"{ch:.3f} t"],
        ["Total Explosive", f"{total_exp:.2f} t"],
        ["Rock Volume", f"{rock_vol:.2f} m³"],
        ["Powder Factor", f"{pf:.4f} t/m³"],
        ["Explosive Cost", f"${exp_cost:,.2f}"],
        ["Drilling Cost", f"${drill_total:,.2f}"],
        ["Detonator Cost", f"${det_total:,.2f}"],
        ["TOTAL COST", f"${total_cost:,.2f}"]
    ], columns=["Parameter","Value"])

    st.subheader("Results")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Report",
        csv,
        "blast_report.csv",
        "text/csv"
    )

# =====================================================
# FOOTER
# =====================================================
st.caption("Version 1.0 | Blast Design Engineering Tool")
