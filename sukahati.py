import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Quality Feedback Dashboard - SUZ TMP (WW35'26)",
    page_icon="🛡️",
    layout="wide",
)

# ============================================================
# STYLING
# ============================================================
st.markdown("""
<style>
    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }

    [data-testid="stHeader"] {
        background: rgba(15, 23, 42, 0);
    }

    .block-container {
        max-width: 1280px;
        padding-top: 1.3rem;
        padding-bottom: 2rem;
    }

    .top-header {
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 15px 18px;
        margin-bottom: 18px;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #dc2626, #ED1C24);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }

    .brand-tag {
        display: inline-block;
        color: #ef4444;
        background: rgba(127, 29, 29, 0.35);
        border: 1px solid rgba(153, 27, 27, 0.65);
        border-radius: 6px;
        padding: 2px 7px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .07em;
    }

    .ww-tag {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 600;
        margin-left: 8px;
    }

    .dashboard-title {
        margin: 5px 0 0 0;
        color: white;
        font-size: 21px;
        font-weight: 800;
    }

    .glass-card {
        min-height: 145px;
        background: rgba(30, 41, 59, 0.72);
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 13px;
        padding: 16px;
        margin-bottom: 4px;
    }

    .kpi-sky { border-left: 4px solid #0ea5e9; }
    .kpi-green { border-left: 4px solid #10b981; }
    .kpi-amber { border-left: 4px solid #f59e0b; }
    .kpi-red { border-left: 4px solid #ef4444; }
    .kpi-indigo { border-left: 4px solid #6366f1; }

    .kpi-label {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .06em;
    }

    .kpi-value {
        color: white;
        font-size: 30px;
        line-height: 1.15;
        font-weight: 800;
        margin-top: 16px;
    }

    .kpi-value.green { color: #34d399; }
    .kpi-value.amber { color: #fbbf24; }

    .kpi-sub {
        color: #94a3b8;
        font-size: 11px;
        margin-top: 8px;
    }

    .mini-pill {
        display: inline-block;
        padding: 3px 7px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
    }

    .pill-green {
        background: rgba(6,78,59,.65);
        color: #6ee7b7;
        border: 1px solid #065f46;
    }

    .briefing {
        background: linear-gradient(90deg,#0f172a,#1e293b,#0f172a);
        border: 1px solid #334155;
        border-radius: 13px;
        padding: 18px;
        margin: 20px 0;
    }

    .briefing-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #334155;
        padding-bottom: 10px;
        margin-bottom: 13px;
    }

    .briefing-title {
        font-size: 15px;
        font-weight: 800;
        color: white;
    }

    .brief-card {
        height: 100%;
        background: rgba(15,23,42,.6);
        border: 1px solid #1e293b;
        border-radius: 9px;
        padding: 14px;
        font-size: 12px;
        line-height: 1.6;
        color: #cbd5e1;
    }

    .brief-sky { color:#38bdf8; font-weight:700; margin-bottom:5px; }
    .brief-red { color:#f87171; font-weight:700; margin-bottom:5px; }
    .brief-green { color:#34d399; font-weight:700; margin-bottom:5px; }

    .section-card {
        background: rgba(30,41,59,.72);
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 13px;
        padding: 17px;
        margin-top: 8px;
        margin-bottom: 18px;
    }

    .section-title {
        color: white;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 2px;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 11px;
        margin-bottom: 8px;
    }

    .status-box {
        background: rgba(15,23,42,.5);
        border: 1px solid #1e293b;
        border-radius: 9px;
        padding: 10px;
        text-align: center;
    }

    .status-label {
        color:#94a3b8;
        font-size:11px;
    }

    .status-value {
        color:#34d399;
        font-size:16px;
        font-weight:800;
    }

    .footer {
        border-top: 1px solid #1e293b;
        margin-top: 22px;
        padding: 18px 2px 4px;
        color: #64748b;
        font-size: 11px;
        display:flex;
        justify-content:space-between;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #1e293b;
        border-radius: 8px;
    }

    .stDownloadButton > button {
        background: #059669;
        color: white;
        border: none;
        font-weight: 700;
    }

    .stDownloadButton > button:hover {
        background: #10b981;
        color: white;
        border: none;
    }

    div[data-testid="stTextInput"] input {
        background: #0f172a;
        color: #e2e8f0;
        border-color: #334155;
    }

    div[data-testid="stRadio"] label {
        color: #cbd5e1;
    }

    hr {
        border-color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SOURCE DATA
# ============================================================
trend_full = pd.DataFrame({
    "Timeline": [
        "Q2 '25", "Q3 '25", "Q4 '25", "Q1 '26", "Q2 '26",
        "Jan '26", "Feb '26", "Mar '26", "Apr '26", "May '26",
        "Jun '26", "Jul '26", "WW30", "WW31", "WW32", "WW33",
        "WW34", "WW35"
    ],
    "Feedback": [7, 2, 23, 16, 7, 19, 2, 3, 2, 0, 4, 8, 1, 0, 2, 2, 1, 0]
})

trend_quarterly = pd.DataFrame({
    "Timeline": ["Q2 '25", "Q3 '25", "Q4 '25", "Q1 '26", "Q2 '26"],
    "Feedback": [7, 2, 23, 16, 7]
})

trend_monthly = pd.DataFrame({
    "Timeline": ["Jan '26", "Feb '26", "Mar '26", "Apr '26", "May '26", "Jun '26", "Jul '26"],
    "Feedback": [19, 2, 3, 2, 0, 4, 8]
})

trend_weekly = pd.DataFrame({
    "Timeline": ["WW30", "WW31", "WW32", "WW33", "WW34", "WW35"],
    "Feedback": [1, 0, 2, 2, 1, 0]
})

pareto_df = pd.DataFrame({
    "Defect Category": [
        "Non de-taping",
        "Package Chip",
        "LID exposed copper",
        "Package Foreign Material",
        "Stiffener Shifted",
        "Others",
    ],
    "Quantity": [19, 8, 5, 5, 5, 3],
    "Cumulative %": [42.2, 60.0, 71.1, 82.2, 93.3, 100.0],
})

incident_df = pd.DataFrame([
    {
        "WW": 35,
        "Lot ID": "N/A",
        "Device": "N/A",
        "Plant": "SUZ",
        "Reject Qty": "0",
        "Defect Mode": "No SUZ Feedback",
        "Root Cause (RC)": "No quality anomalies reported in WW35.",
        "Corrective Action (CA)": "Continuous line monitoring maintained.",
        "Status": "Clear",
    },
    {
        "WW": 34,
        "Lot ID": "WBL5720",
        "Device": "STONES10",
        "Plant": "BKF",
        "Reject Qty": "2 Trays",
        "Defect Mode": "Tray Reversed",
        "Root Cause (RC)": (
            "Gap in Packing Inspection: Emphasize to all Manufacturing Specialists "
            "(MS) at packing process to ensure 100% check of tray gap and orientation "
            "during unit checking & strapping per standard spec M07-60800 (7.6.1)."
        ),
        "Corrective Action (CA)": (
            "Training Re-certification: Requested Training Department to retrain all "
            "MS at BLF and BKF lines for packing process compliance against standard "
            "operating procedure M07-60800 (7.6.1)."
        ),
        "Status": "Done",
    },
])

excel_matrix_df = pd.DataFrame({
    "Cat/Timeline": ["SUZ FEEDBACK"],
    "Q2'25": [7],
    "Q3'25": [2],
    "Q4'25": [23],
    "Q1'26": [16],
    "Q2'26": [7],
    "Jan'26": [19],
    "Feb'26": [2],
    "Mar'26": [3],
    "Apr'26": [2],
    "May'26": [0],
    "Jun'26": [4],
    "Jul'26": [8],
    "WW30": [1],
    "WW31": [0],
    "WW32": [2],
    "WW33": [2],
    "WW34": [1],
    "WW35": [0],
})

# ============================================================
# CSV EXPORT
# ============================================================
def build_csv():
    output = io.StringIO()
    output.write("QUALITY FEEDBACK FROM SUZ TMP (WW35'26) - OVERVIEW\n\n")

    output.write("TIMELINE TREND ANALYSIS\n")
    excel_matrix_df.to_csv(output, index=False)
    output.write("\n")

    output.write("DEFECT PARETO BREAKDOWN (2026)\n")
    pareto_export = pareto_df.copy()
    pareto_export["Pareto %"] = (
        pareto_export["Quantity"] / pareto_export["Quantity"].sum() * 100
    ).round(1).astype(str) + "%"
    pareto_export["Cumulative %"] = pareto_export["Cumulative %"].astype(str) + "%"
    pareto_export.to_csv(output, index=False)
    output.write("\n")

    output.write("FEEDBACK STATUS 2026\n")
    pd.DataFrame({
        "Status": ["Closed", "Open"],
        "Quantity": [40, 5],
        "Percentage": ["88.9%", "11.1%"],
    }).to_csv(output, index=False)
    output.write("\n")

    output.write("WEEKLY INCIDENT LOG\n")
    incident_df.to_csv(output, index=False)

    return output.getvalue().encode("utf-8")

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="top-header">
    <div class="brand-row">
        <div class="brand-icon">✓</div>
        <div>
            <div>
                <span class="brand-tag">TF • AMD QUALITY ENGINEERING</span>
                <span class="ww-tag">Work Week 35, 2026</span>
            </div>
            <div class="dashboard-title">SUZ TMP Quality Feedback Overview</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

button_col, spacer = st.columns([1.25, 4.75])
with button_col:
    st.download_button(
        "⬇ Export Excel CSV",
        data=build_csv(),
        file_name="SUZ_TMP_Quality_Feedback_WW35_2026.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ============================================================
# KPI CARDS
# ============================================================
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown("""
    <div class="glass-card kpi-sky">
        <div class="kpi-label">Total Feedbacks YTD</div>
        <div class="kpi-value">45</div>
        <div class="kpi-sub">2026 Total</div>
        <div class="kpi-sub">Peak: Jan '26 (19 cases)</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="glass-card kpi-green">
        <div class="kpi-label">Closure Rate</div>
        <div class="kpi-value green">89%</div>
        <div class="kpi-sub"><span class="mini-pill pill-green">40 Closed</span></div>
        <div class="kpi-sub">5 Open Pending Items</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="glass-card kpi-amber">
        <div class="kpi-label">Open Feedback</div>
        <div class="kpi-value amber">5</div>
        <div class="kpi-sub">11% Total</div>
        <div class="kpi-sub">Target closure: &lt; 14 days</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="glass-card kpi-red">
        <div class="kpi-label">Top Pareto Issue</div>
        <div style="font-size:18px;font-weight:800;color:white;margin-top:16px;">Non de-taping</div>
        <div style="color:#f87171;font-size:14px;font-weight:700;margin-top:7px;">19 Cases</div>
        <div class="kpi-sub">(42.2% Pareto)</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown("""
    <div class="glass-card kpi-indigo">
        <div class="kpi-label">WW35 Status</div>
        <div class="kpi-value green" style="font-size:23px;">0 Feedback</div>
        <div class="kpi-sub"><span class="mini-pill pill-green">Clean</span></div>
        <div class="kpi-sub">WW34: 1 Tray Reversed (Closed)</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# EXECUTIVE BRIEFING
# ============================================================
st.markdown("""
<div class="briefing">
    <div class="briefing-header">
        <div class="briefing-title">📄 Sr. Quality Engineer - Top Management Executive Briefing</div>
        <span class="mini-pill" style="background:#1e293b;color:#94a3b8;border:1px solid #334155;">WW35'26 Update</span>
    </div>
</div>
""", unsafe_allow_html=True)

b1, b2, b3 = st.columns(3)

with b1:
    st.markdown("""
    <div class="brief-card">
        <div class="brief-sky">↘ 1. Significant Quality Stabilization</div>
        Quality feedback saw a dramatic drop post-Jan '26 spike (19 cases).
        Average monthly volume stabilized to <strong>2.8 cases/month</strong>
        (Feb–Jul '26), representing a <strong>78% reduction</strong> in defect rates.
    </div>
    """, unsafe_allow_html=True)

with b2:
    st.markdown("""
    <div class="brief-card">
        <div class="brief-red">◉ 2. Pareto Defect Concentration</div>
        <strong>"Non de-taping"</strong> constitutes <strong>42.2% (19 cases)</strong>
        of all feedback, followed by <strong>Package Chip (8 cases, 17.8%)</strong>.
        Targeted auto-sensor validation at de-taping stations is prioritized for Q3/Q4.
    </div>
    """, unsafe_allow_html=True)

with b3:
    st.markdown("""
    <div class="brief-card">
        <div class="brief-green">☑ 3. CAPA Execution & WW35 Status</div>
        <strong>WW35 logged 0 feedbacks</strong>. WW34 defect
        (Lot WBL5720 Tray Reversed) was contained. 100% retraining of MS personnel
        completed across BLF/BKF plants per spec <strong>M07-60800 (7.6.1)</strong>.
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ============================================================
# TREND + STATUS
# ============================================================
trend_col, status_col = st.columns([2, 1])

with trend_col:
    st.markdown(
        '<div class="section-title">📈 SUZ Feedback Trend Analysis (2025 - 2026)</div>'
        '<div class="section-subtitle">Quarterly, Monthly, & Weekly Breakdown</div>',
        unsafe_allow_html=True
    )

    view = st.radio(
        "Trend View",
        ["All", "Quarterly", "Monthly", "WW30-35"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if view == "Quarterly":
        trend_df = trend_quarterly
    elif view == "Monthly":
        trend_df = trend_monthly
    elif view == "WW30-35":
        trend_df = trend_weekly
    else:
        trend_df = trend_full

    bar_colors = []
    for label in trend_df["Timeline"]:
        if label == "Jan '26":
            bar_colors.append("#ef4444")
        elif label.startswith("WW"):
            bar_colors.append("#10b981")
        elif "'" in label and label.startswith(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul")):
            bar_colors.append("#38bdf8")
        else:
            bar_colors.append("#6366f1")

    fig_trend = go.Figure(
        go.Bar(
            x=trend_df["Timeline"],
            y=trend_df["Feedback"],
            marker_color=bar_colors,
            hovertemplate="<b>%{x}</b><br>SUZ Feedback: %{y}<extra></extra>",
        )
    )

    fig_trend.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title="Feedback",
            rangemode="tozero",
            gridcolor="rgba(255,255,255,.05)",
            zeroline=False,
        ),
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

with status_col:
    st.markdown(
        '<div class="section-title">◉ Feedback Status 2026</div>'
        '<div class="section-subtitle">Closure Rate vs Open Work Orders</div>',
        unsafe_allow_html=True
    )

    fig_status = go.Figure(
        go.Pie(
            labels=["Closed", "Open"],
            values=[40, 5],
            hole=0.72,
            marker=dict(colors=["#10b981", "#38bdf8"]),
            textinfo="none",
            hovertemplate="%{label}: %{value} cases (%{percent})<extra></extra>",
        )
    )
    fig_status.update_layout(
        height=285,
        margin=dict(l=10, r=10, t=5, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1"),
        showlegend=False,
        annotations=[
            dict(
                text="<b>Total 45</b>",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16, color="#f8fafc"),
            )
        ],
    )
    st.plotly_chart(fig_status, use_container_width=True, config={"displayModeBar": False})

    s1, s2 = st.columns(2)
    with s1:
        st.markdown("""
        <div class="status-box">
            <div class="status-label">Closed</div>
            <div class="status-value">40 (88.9%)</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="status-box">
            <div class="status-label">Open</div>
            <div class="status-value" style="color:#38bdf8;">5 (11.1%)</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PARETO
# ============================================================
st.markdown(
    '<div class="section-title">⚙ Defect Categorization & Pareto Analysis (80/20 Distribution)</div>'
    '<div class="section-subtitle">Top Defect Modes Driving Quality Rejections</div>',
    unsafe_allow_html=True
)

fig_pareto = go.Figure()

fig_pareto.add_trace(
    go.Bar(
        x=pareto_df["Defect Category"],
        y=pareto_df["Quantity"],
        name="Defect Quantity",
        marker_color=["#dc2626", "#ea580c", "#d97706", "#2563eb", "#7c3aed", "#475569"],
        yaxis="y",
        hovertemplate="%{x}<br>Quantity: %{y}<extra></extra>",
    )
)

fig_pareto.add_trace(
    go.Scatter(
        x=pareto_df["Defect Category"],
        y=pareto_df["Cumulative %"],
        name="Cumulative %",
        mode="lines+markers",
        line=dict(color="#fbbf24", width=2),
        marker=dict(color="#fbbf24", size=7),
        yaxis="y2",
        hovertemplate="%{x}<br>Cumulative: %{y:.1f}%<extra></extra>",
    )
)

fig_pareto.update_layout(
    height=350,
    margin=dict(l=10, r=10, t=30, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cbd5e1"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
    xaxis=dict(showgrid=False),
    yaxis=dict(
        title="Defect Quantity",
        range=[0, 22],
        gridcolor="rgba(255,255,255,.05)",
        zeroline=False,
    ),
    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right",
        range=[0, 100],
        ticksuffix="%",
        showgrid=False,
        color="#fbbf24",
    ),
)

st.plotly_chart(fig_pareto, use_container_width=True, config={"displayModeBar": False})

# ============================================================
# INCIDENT TRACKER
# ============================================================
st.markdown(
    '<div class="section-title">☑ Quality Feedback Incident Tracking Log (WW34 - WW35)</div>'
    '<div class="section-subtitle">Detailed Root Cause (RC) & Corrective Actions (CA)</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search Incident",
    placeholder="Search Lot, Plant, Defect...",
    label_visibility="collapsed",
)

display_incidents = incident_df.copy()

if search:
    mask = display_incidents.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1,
    )
    display_incidents = display_incidents[mask]

st.dataframe(
    display_incidents,
    use_container_width=True,
    hide_index=True,
    column_config={
        "WW": st.column_config.NumberColumn("WW", width="small", format="%d"),
        "Lot ID": st.column_config.TextColumn("Lot ID", width="small"),
        "Device": st.column_config.TextColumn("Device", width="small"),
        "Plant": st.column_config.TextColumn("Plant", width="small"),
        "Reject Qty": st.column_config.TextColumn("Reject Qty", width="small"),
        "Defect Mode": st.column_config.TextColumn("Defect Mode", width="medium"),
        "Root Cause (RC)": st.column_config.TextColumn("Root Cause (RC)", width="large"),
        "Corrective Action (CA)": st.column_config.TextColumn("Corrective Action (CA)", width="large"),
        "Status": st.column_config.TextColumn("Status", width="small"),
    },
)

# ============================================================
# RAW DATA MATRIX
# ============================================================
st.markdown(
    '<div class="section-title">▦ Structured Excel Raw Data Overview</div>'
    '<div class="section-subtitle">Standardized matrix ready for direct copy into Excel graph tools</div>',
    unsafe_allow_html=True
)

st.dataframe(excel_matrix_df, use_container_width=True, hide_index=True)

pareto_display = pareto_df.copy()
pareto_display["Pareto %"] = (
    pareto_display["Quantity"] / pareto_display["Quantity"].sum() * 100
).round(1)
pareto_display["Cumulative %"] = pareto_display["Cumulative %"].round(1)

st.dataframe(
    pareto_display[["Defect Category", "Quantity", "Pareto %", "Cumulative %"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Pareto %": st.column_config.NumberColumn("Pareto %", format="%.1f%%"),
        "Cumulative %": st.column_config.NumberColumn("Cum %", format="%.1f%%"),
    },
)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    <span>TF • AMD Quality Engineering Department © 2026. Confidential - Top Management Review.</span>
    <span>Prepared for WW35'26 Executive Meeting</span>
</div>
""", unsafe_allow_html=True)
