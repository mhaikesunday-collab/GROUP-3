import streamlit as st
import pandas as pd
import math

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="BLAST DESIGN TOOL",
    page_icon="💥",
    layout="wide"
)

# =====================================================
# SAFE STATE
# =====================================================
st.session_state.setdefault("theme", "DARK")

# =====================================================
# THEME
# =====================================================
def theme_css(mode):
    if mode == "DARK":
        st.markdown("""
        <style>
        .stApp {background:#0b1320; color:white;}
        section[data-testid="stSidebar"] {background:#0f172a;}
        h1,h2,h3 {color:#FFD700;}
        label {color:white !important; font-weight:600;}
        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>
        .stApp {background:#f1f5f9; color:black;}
        section[data-testid="stSidebar"] {background:#e2e8f0;}
        h1,h2,h3 {color:#1e3a8a;}
        label {color:black !important; font-weight:600;}
        </style>
        """, unsafe_allow_html=True)

# =====================================================
# SETTINGS PANEL
# =====================================================
with st.sidebar.expander("⚙️ SETTINGS", expanded=False):

    st.session_state.theme = st.selectbox(
        "THEME",
        ["DARK", "LIGHT"],
        index=["DARK","LIGHT"].index(st.session_state.theme)
    )

    st.write("VERSION 1.0")
    st.write("BLAST DESIGN ENGINEERING TOOL")

theme_css(st.session_state.theme)

# =====================================================
# TITLE
# =====================================================
st.title("💥 BLAST DESIGN TOOL")

# =====================================================
# CONVERSIONS
# =====================================================
def length(v,u):
    if v < 0: return None
    return {"MM":v/1000,"CM":v/100,"M":v,"FT":v*0.3048}[u]

def diameter(v,u):
    if v < 0: return None
    return {"MM":v/1000,"CM":v/100,"M":v,"IN":v*0.0254}[u]

def density(v,u):
    if v < 0: return None
    return {"T/M³":v,"KG/M³":v/1000}[u]

# =====================================================
# FORMULAS
# =====================================================
def burden(d,r): return 25*d/r if r>0 else 0
def spacing(b): return 1.25*b
def holes(a,b,s): return max(1,int(a/(b*s))) if b>0 and s>0 else 1

def charge(d,h,r):
    if d<=0 or h<=0 or r<=0:
        return 0
    return math.pi*(d/2)**2*h*r

# =====================================================
# INPUT SECTION (INLINE UNITS)
# =====================================================
st.subheader("🧱 INPUTS")

def input_with_unit(label, value, units, key):
    col1, col2 = st.columns([4,1])
    with col1:
        val = st.number_input(label, min_value=0.0, value=value, key=key+"_val")
    with col2:
        unit = st.selectbox(" ", units, key=key+"_unit")
    return val, unit

bench, bu = input_with_unit("BENCH HEIGHT", 10.0, ["MM","CM","M","FT"], "bench")
dia, du = input_with_unit("HOLE DIAMETER", 115.0, ["MM","CM","M","IN"], "dia")
stemming, su = input_with_unit("STEMMING", 2.0, ["MM","CM","M","FT"], "stem")
sub, subu = input_with_unit("SUBDRILL", 1.0, ["MM","CM","M","FT"], "sub")

area = st.number_input("BENCH AREA (M²)", min_value=0.0, value=5000.0)

rock, ru = input_with_unit("ROCK DENSITY", 2.7, ["T/M³","KG/M³"], "rock")
exp, eu = input_with_unit("EXPLOSIVE DENSITY", 0.85, ["T/M³","KG/M³"], "exp")

expl_cost = st.number_input("EXPLOSIVE COST ($/T)", min_value=0.0, value=450.0)
drill_cost = st.number_input("DRILLING COST ($/M)", min_value=0.0, value=50.0)
det_cost = st.number_input("DETONATOR COST ($/HOLE)", min_value=0.0, value=10.0)

run = st.button("💥 CALCULATE")

# =====================================================
# CALCULATION
# =====================================================
if run:

    bench_m = length(bench,bu)
    dia_m = diameter(dia,du)
    stem_m = length(stemming,su)
    sub_m = length(sub,subu)

    rock_d = density(rock,ru)
    exp_d = density(exp,eu)

    if None in [bench_m,dia_m,stem_m,sub_m,rock_d,exp_d]:
        st.error("INVALID INPUT: NO NEGATIVE VALUES ALLOWED")
        st.stop()

    b = burden(dia_m,rock_d)
    s = spacing(b)
    h = holes(area,b,s)

    eff_h = max(0,bench_m+sub_m-stem_m)
    ch = charge(dia_m,eff_h,exp_d)

    total_exp = ch*h
    rock_vol = area*bench_m
    pf = total_exp/rock_vol if rock_vol>0 else 0

    exp_cost = total_exp*expl_cost
    drill_total = h*(bench_m+sub_m)*drill_cost
    det_total = h*det_cost

    total_cost = exp_cost + drill_total + det_total

    # =================================================
    # RESULTS TABLE
    # =================================================
    df = pd.DataFrame([
        ["BURDEN", f"{b:.2f} M"],
        ["SPACING", f"{s:.2f} M"],
        ["HOLES", h],
        ["CHARGE PER HOLE", f"{ch:.3f} T"],
        ["TOTAL EXPLOSIVE", f"{total_exp:.2f} T"],
        ["ROCK VOLUME", f"{rock_vol:.2f} M³"],
        ["POWDER FACTOR", f"{pf:.4f} T/M³"],
        ["EXPLOSIVE COST", f"${exp_cost:,.2f}"],
        ["DRILLING COST", f"${drill_total:,.2f}"],
        ["DETONATOR COST", f"${det_total:,.2f}"],
        ["TOTAL COST", f"${total_cost:,.2f}"]
    ], columns=["PARAMETER","VALUE"])

    st.subheader("📊 RESULTS")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ DOWNLOAD REPORT",
        csv,
        "BLAST_REPORT.csv",
        "text/csv"
    )

# =====================================================
# FOOTER
# =====================================================
st.caption("VERSION 1.0 | BLAST DESIGN ENGINEERING TOOL")
