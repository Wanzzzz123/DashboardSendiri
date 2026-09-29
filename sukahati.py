# ============================================================

# CSAM WIP LOTS MONITORING DASHBOARD

# GitHub -> Streamlit Community Cloud

# ============================================================
 
from pathlib import Path

from datetime import datetime
 
import pandas as pd

import plotly.express as px

import plotly.graph_objects as go

import streamlit as st
 
 
# ============================================================

# PAGE CONFIG

# ============================================================
 
st.set_page_config(

    page_title="CSAM WIP Lots Monitoring",

    page_icon="📊",

    layout="wide",

    initial_sidebar_state="collapsed",

)
 
 
# ============================================================

# PATH

# ============================================================
 
BASE = Path(__file__).resolve().parent
 
 
# ============================================================

# THEME

# ============================================================
 
BG = "#071018"

PANEL = "#0D1822"

PANEL2 = "#101F2C"

TEXT = "#E8F1F7"

MUTED = "#8EA4B4"

CYAN = "#19C7F3"

GREEN = "#35D07F"

AMBER = "#FFC857"

RED = "#FF5A5F"

GRID = "#203342"
 
 
# ============================================================

# CSS

# ============================================================
 
st.markdown(

    f"""
<style>
 
    /* Main page */

    .stApp {{

        background-color: {BG};

    }}
 
    .block-container {{

        max-width: 100%;

        padding-top: 1rem;

        padding-bottom: 2rem;

        padding-left: 1.5rem;

        padding-right: 1.5rem;

    }}
 
    /* Header */

    .dashboard-header {{

        display: grid;

        grid-template-columns: 1fr 2fr 1fr;

        align-items: center;

        background: #050B10;

        border: 1px solid {GRID};

        border-radius: 10px;

        padding: 12px 20px;

        margin-bottom: 10px;

    }}
 
    .company-name {{

        color: #FFFFFF;

        font-size: 17px;

        font-weight: 800;

    }}
 
    .company-subtitle {{

        color: {MUTED};

        font-size: 9px;

        letter-spacing: 1.2px;

    }}
 
    .dashboard-title {{

        color: {CYAN};

        font-size: 25px;

        font-weight: 800;

        text-align: center;

    }}
 
    .update-time {{

        color: {MUTED};

        font-size: 11px;

        text-align: right;

    }}
 
    /* KPI cards */

    .kpi-card {{

        background: {PANEL};

        border: 1px solid {GRID};

        border-radius: 10px;

        padding: 13px 16px;

        min-height: 105px;

        box-shadow: 0 5px 18px rgba(0,0,0,.22);

    }}
 
    .kpi-title {{

        color: {MUTED};

        font-size: 12px;

        font-weight: 600;

    }}
 
    .kpi-value {{

        color: {TEXT};

        font-size: 27px;

        font-weight: 700;

        margin-top: 4px;

    }}
 
    .kpi-subtitle {{

        font-size: 11px;

        margin-top: 4px;

    }}
 
    /* Section heading */

    .section-title {{

        color: {TEXT};

        font-size: 15px;

        font-weight: 700;

        margin-top: 8px;

        margin-bottom: 3px;

    }}
 
    /* Action panel */

    .action-panel {{

        background: {PANEL};

        border: 1px solid {GRID};

        border-radius: 10px;

        padding: 14px;

        color: {TEXT};

        font-size: 12px;

        min-height: 240px;

    }}
 
    .action-row {{

        padding: 10px 0;

        border-bottom: 1px solid {GRID};

    }}
 
    /* Dataframe */

    [data-testid="stDataFrame"] {{

        border: 1px solid {GRID};

        border-radius: 8px;

    }}
 
    /* Streamlit labels */

    label {{

        color: {TEXT} !important;

    }}
 
    </style>

    """,

    unsafe_allow_html=True,

)
 
 
# ============================================================

# DATA

# ============================================================
 
@st.cache_data(ttl=60)

def load_data():
 
    wip_file = BASE / "csam_wip_demo.csv"

    machine_file = BASE / "csam_machine_demo.csv"
 
    if not wip_file.exists():

        st.error("Missing file: csam_wip_demo.csv")

        st.stop()
 
    if not machine_file.exists():

        st.error("Missing file: csam_machine_demo.csv")

        st.stop()
 
    wip = pd.read_csv(wip_file)

    machines = pd.read_csv(machine_file)
 
    wip["age_hr"] = pd.to_numeric(

        wip["age_hr"],

        errors="coerce"

    ).fillna(0)
 
    return wip, machines
 
 
wip, machines = load_data()
 
 
# ============================================================

# HEADER

# ============================================================
 
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
st.markdown(

    f"""
<div class="dashboard-header">
 
        <div>
<div class="company-name">TF AMD</div>
<div class="company-subtitle">

                QUALITY / PROCESS ENGINEERING
</div>
</div>
 
        <div class="dashboard-title">

            CSAM WIP LOTS MONITORING
</div>
 
        <div class="update-time">

            LIVE DEMO<br>

            Updated {current_time}
</div>
 
    </div>

    """,

    unsafe_allow_html=True,

)
 
 
# ============================================================

# FILTER

# ============================================================
 
filter_col1, filter_col2, filter_col3 = st.columns(

    [2, 1, 6],

    vertical_alignment="bottom"

)
 
with filter_col1:
 
    selected_process = st.selectbox(

        "Process",

        [

            "All CSAM",

            "UP CSAM",

            "Lid CSAM",

            "DM CSAM",

        ],

    )
 
with filter_col2:
 
    age_limit = st.number_input(

        "WIP age alert (hr)",

        min_value=1,

        max_value=48,

        value=8,

        step=1,

    )
 
 
# ============================================================

# FILTER DATA

# ============================================================
 
if selected_process != "All CSAM":
 
    wip_view = wip[

        wip["process"] == selected_process

    ].copy()
 
    machine_view = machines[

        machines["process"] == selected_process

    ].copy()
 
else:
 
    wip_view = wip.copy()

    machine_view = machines.copy()
 
 
# ============================================================

# KPI CALCULATION

# ============================================================
 
total_wip = len(wip_view)
 
aged_wip = int(

    (wip_view["age_hr"] > float(age_limit)).sum()

)
 
unavailable = int(

    (machine_view["status"] == "Unavailable").sum()

)
 
total_machines = len(machine_view)
 
if total_machines:
 
    availability = (

        100

        * (total_machines - unavailable)

        / total_machines

    )
 
else:
 
    availability = 0
 
 
hot_lots = int(

    (wip_view["priority"] == "Hot Lot").sum()

)
 
 
# ============================================================

# KPI CARD FUNCTION

# ============================================================
 
def kpi_card(title, value, subtitle, accent):
 
    st.markdown(

        f"""
<div

            class="kpi-card"

            style="border-left:4px solid {accent};"
>
 
            <div class="kpi-title">

                {title}
</div>
 
            <div class="kpi-value">

                {value}
</div>
 
            <div

                class="kpi-subtitle"

                style="color:{accent};"
>

                {subtitle}
</div>
 
        </div>

        """,

        unsafe_allow_html=True,

    )
 
 
# ============================================================

# KPI ROW

# ============================================================
 
k1, k2, k3, k4, k5 = st.columns(5)
 
with k1:
 
    kpi_card(

        "TOTAL WIP LOTS",

        total_wip,

        "lots in CSAM queue",

        CYAN,

    )
 
with k2:
 
    kpi_card(

        "AGED WIP",

        aged_wip,

        f"> {age_limit} hr threshold",

        RED if aged_wip else GREEN,

    )
 
with k3:
 
    kpi_card(

        "MACHINE AVAILABILITY",

        f"{availability:.1f}%",

        f"{total_machines - unavailable}/{total_machines} machines available",

        GREEN if availability >= 90 else AMBER,

    )
 
with k4:
 
    kpi_card(

        "UNAVAILABLE MACHINES",

        unavailable,

        "requires owner action",

        RED if unavailable else GREEN,

    )
 
with k5:
 
    kpi_card(

        "HOT LOTS",

        hot_lots,

        "priority queue",

        AMBER,

    )
 
 
# ============================================================

# CHART ROW

# ============================================================
 
chart1_col, chart2_col = st.columns(2)
 
 
# ============================================================

# WIP BY PROCESS

# ============================================================
 
with chart1_col:
 
    st.markdown(

        '<div class="section-title">WIP BY CSAM PROCESS</div>',

        unsafe_allow_html=True,

    )
 
    counts = (

        wip_view

        .groupby("process")

        .size()

        .reset_index(name="WIP")

    )
 
    fig1 = px.bar(

        counts,

        x="WIP",

        y="process",

        orientation="h",

        text="WIP",

    )
 
    fig1.update_traces(

        marker_color=CYAN,

        textposition="outside",

    )
 
    fig1.update_layout(

        template="plotly_dark",

        paper_bgcolor=PANEL,

        plot_bgcolor=PANEL,

        font={"color": TEXT},

        margin={

            "l": 80,

            "r": 35,

            "t": 15,

            "b": 35,

        },

        height=270,

        xaxis={

            "gridcolor": GRID,

            "title": None,

        },

        yaxis={

            "gridcolor": PANEL,

            "title": None,

        },

    )
 
    st.plotly_chart(

        fig1,

        use_container_width=True,

        config={

            "displayModeBar": False

        },

    )
 
 
# ============================================================

# MACHINE AVAILABILITY

# ============================================================
 
with chart2_col:
 
    st.markdown(

        '<div class="section-title">MACHINE AVAILABILITY</div>',

        unsafe_allow_html=True,

    )
 
    m = (

        machine_view

        .groupby(

            [

                "process",

                "status",

            ]

        )

        .size()

        .reset_index(name="count")

    )
 
    fig2 = px.bar(

        m,

        x="process",

        y="count",

        color="status",

        barmode="stack",

        color_discrete_map={

            "Available": GREEN,

            "Unavailable": RED,

        },

        text="count",

    )
 
    fig2.update_layout(

        template="plotly_dark",

        paper_bgcolor=PANEL,

        plot_bgcolor=PANEL,

        font={"color": TEXT},

        margin={

            "l": 40,

            "r": 20,

            "t": 15,

            "b": 35,

        },

        height=270,

        xaxis={

            "gridcolor": PANEL

        },

        yaxis={

            "gridcolor": GRID,

            "title": None,

        },

        legend={

            "orientation": "h",

            "y": 1.12,

        },

    )
 
    st.plotly_chart(

        fig2,

        use_container_width=True,

        config={

            "displayModeBar": False

        },

    )
 
 
# ============================================================

# TABLE FUNCTION

# ============================================================
 
def get_process_table(process):
 
    cols = [

        "timestamp",

        "lot",

        "device",

        "package",

        "priority",

        "age_hr",

    ]
 
    df = (

        wip_view[

            wip_view["process"] == process

        ]

        .sort_values(

            "age_hr",

            ascending=False

        )

        .head(15)

        .copy()

    )
 
    if df.empty:

        return pd.DataFrame(columns=cols)
 
    df["age_hr"] = df["age_hr"].round(1)
 
    return df[cols]
 
 
# ============================================================

# WIP TABLES

# ============================================================
 
t1, t2, t3 = st.columns(3)
 
with t1:
 
    st.markdown(

        '<div class="section-title">WIP LOTS BEFORE UP CSAM</div>',

        unsafe_allow_html=True,

    )
 
    st.dataframe(

        get_process_table("UP CSAM"),

        use_container_width=True,

        hide_index=True,

        height=270,

    )
 
with t2:
 
    st.markdown(

        '<div class="section-title">WIP LOTS BEFORE LID CSAM</div>',

        unsafe_allow_html=True,

    )
 
    st.dataframe(

        get_process_table("Lid CSAM"),

        use_container_width=True,

        hide_index=True,

        height=270,

    )
 
with t3:
 
    st.markdown(

        '<div class="section-title">WIP LOTS BEFORE DM CSAM</div>',

        unsafe_allow_html=True,

    )
 
    st.dataframe(

        get_process_table("DM CSAM"),

        use_container_width=True,

        hide_index=True,

        height=270,

    )
 
 
# ============================================================

# BOTTOM ROW

# ============================================================
 
machine_col, action_col = st.columns([2, 1])
 
 
# ============================================================

# MACHINE TABLE

# ============================================================
 
with machine_col:
 
    st.markdown(

        '<div class="section-title">UNAVAILABLE CSAM MACHINES</div>',

        unsafe_allow_html=True,

    )
 
    machine_display = (

        machine_view

        .sort_values(

            ["status", "process"],

            ascending=[

                True,

                True,

            ],

        )

        .copy()

    )
 
    st.dataframe(

        machine_display,

        use_container_width=True,

        hide_index=True,

        height=250,

    )
 
 
# ============================================================

# ACTION VIEW

# ============================================================
 
with action_col:
 
    st.markdown(

        '<div class="section-title">QUALITY CONTROL / ACTION VIEW</div>',

        unsafe_allow_html=True,

    )
 
    st.markdown(

        f"""
<div class="action-panel">
 
            <div class="action-row">

                1. Escalate WIP &gt; {age_limit} hr to CSAM owner
</div>
 
            <div class="action-row">

                2. Review unavailable machine reason every shift
</div>
 
            <div class="action-row">

                3. Prioritize Hot Lot / customer-critical WIP
</div>
 
            <div style="padding:10px 0;">

                4. Track machine recovery ETA and containment
</div>
 
        </div>

        """,

        unsafe_allow_html=True,

    )
 
