"""
CSAM WIP Lots Monitoring Dashboard
-----------------------------------
Run:
    pip install dash plotly pandas
    python csam_dashboard.py

The app loads:
    csam_wip_demo.csv
    csam_machine_demo.csv

Replace the demo CSV files with your actual data using the same column names,
or modify load_data() for your database / Datalyzer / QMS source.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, dash_table, Input, Output

BASE = Path(__file__).resolve().parent

# -------------------------
# Theme
# -------------------------
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

app = Dash(__name__)
app.title = "CSAM WIP Lots Monitoring"

# -------------------------
# Data
# -------------------------
def load_data():
    wip = pd.read_csv(BASE / "csam_wip_demo.csv")
    machines = pd.read_csv(BASE / "csam_machine_demo.csv")
    wip["age_hr"] = pd.to_numeric(wip["age_hr"], errors="coerce").fillna(0)
    return wip, machines

def card(title, value, subtitle="", accent=CYAN):
    return html.Div([
        html.Div(title, style={"color": MUTED, "fontSize": "12px", "fontWeight": "600"}),
        html.Div(value, style={"color": TEXT, "fontSize": "27px", "fontWeight": "700", "marginTop": "4px"}),
        html.Div(subtitle, style={"color": accent, "fontSize": "11px", "marginTop": "4px"})
    ], style={
        "background": PANEL,
        "border": f"1px solid {GRID}",
        "borderLeft": f"4px solid {accent}",
        "borderRadius": "10px",
        "padding": "13px 16px",
        "minHeight": "78px",
        "boxShadow": "0 5px 18px rgba(0,0,0,.22)"
    })

def section(title, children):
    return html.Div([
        html.Div(title, style={"fontSize": "15px", "fontWeight": "700", "color": TEXT, "marginBottom": "10px"}),
        children
    ], style={
        "background": PANEL,
        "border": f"1px solid {GRID}",
        "borderRadius": "10px",
        "padding": "14px",
        "boxShadow": "0 5px 18px rgba(0,0,0,.18)"
    })

# -------------------------
# Layout
# -------------------------
app.layout = html.Div([
    dcc.Interval(id="refresh", interval=60*1000, n_intervals=0),

    html.Div([
        html.Div([
            html.Div("TF AMD", style={"fontWeight": "800", "fontSize": "17px", "color": "#FFFFFF"}),
            html.Div("QUALITY / PROCESS ENGINEERING", style={"fontSize": "9px", "color": MUTED, "letterSpacing": "1.2px"})
        ]),
        html.Div("CSAM WIP LOTS MONITORING", style={"fontSize": "25px", "fontWeight": "800", "color": CYAN, "textAlign": "center"}),
        html.Div(id="last-update", style={"fontSize": "11px", "color": MUTED, "textAlign": "right"})
    ], style={
        "display": "grid",
        "gridTemplateColumns": "1fr 2fr 1fr",
        "alignItems": "center",
        "padding": "12px 20px",
        "background": "#050B10",
        "borderBottom": f"1px solid {GRID}"
    }),

    html.Div([
        html.Div("Process:", style={"color": MUTED, "fontSize": "12px", "paddingTop": "8px"}),
        dcc.Dropdown(
            id="process-filter",
            options=[{"label": "All CSAM", "value": "ALL"},
                     {"label": "UP CSAM", "value": "UP CSAM"},
                     {"label": "Lid CSAM", "value": "Lid CSAM"},
                     {"label": "DM CSAM", "value": "DM CSAM"}],
            value="ALL",
            clearable=False,
            style={"width": "180px", "color": "#111"}
        ),
        html.Div("WIP age alert:", style={"color": MUTED, "fontSize": "12px", "paddingTop": "8px", "marginLeft": "20px"}),
        dcc.Input(id="age-limit", type="number", value=8, min=1, max=48,
                  style={"width": "65px", "padding": "7px", "borderRadius": "5px", "border": "1px solid #344B5B"}),
        html.Div("hours", style={"color": MUTED, "fontSize": "12px", "paddingTop": "8px"})
    ], style={
        "display": "flex", "gap": "9px", "alignItems": "center",
        "padding": "10px 20px", "background": "#09131C"
    }),

    html.Div(id="kpi-row", style={
        "display": "grid",
        "gridTemplateColumns": "repeat(5, 1fr)",
        "gap": "10px",
        "padding": "14px 20px 10px"
    }),

    html.Div([
        html.Div([
            section("WIP BY CSAM PROCESS",
                    dcc.Graph(id="wip-by-process", config={"displayModeBar": False}, style={"height": "260px"}))
        ]),
        html.Div([
            section("MACHINE AVAILABILITY",
                    dcc.Graph(id="machine-availability", config={"displayModeBar": False}, style={"height": "260px"}))
        ])
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "10px", "padding": "0 20px 10px"}),

    html.Div([
        html.Div([
            section("WIP LOTS BEFORE UP CSAM",
                    dash_table.DataTable(
                        id="up-table",
                        columns=[{"name": x, "id": x} for x in ["timestamp","lot","device","package","priority","age_hr"]],
                        style_table={"overflowX": "auto", "maxHeight": "245px", "overflowY": "auto"},
                        style_header={"backgroundColor": "#152A39", "color": CYAN, "fontWeight": "700", "fontSize": "11px"},
                        style_cell={"backgroundColor": PANEL2, "color": TEXT, "border": f"1px solid {GRID}", "fontSize": "10px", "padding": "6px"},
                        style_data_conditional=[{"if": {"filter_query": "{age_hr} > 8"}, "color": RED, "fontWeight": "700"}]
                    ))
        ]),
        html.Div([
            section("WIP LOTS BEFORE LID CSAM",
                    dash_table.DataTable(
                        id="lid-table",
                        columns=[{"name": x, "id": x} for x in ["timestamp","lot","device","package","priority","age_hr"]],
                        style_table={"overflowX": "auto", "maxHeight": "245px", "overflowY": "auto"},
                        style_header={"backgroundColor": "#152A39", "color": CYAN, "fontWeight": "700", "fontSize": "11px"},
                        style_cell={"backgroundColor": PANEL2, "color": TEXT, "border": f"1px solid {GRID}", "fontSize": "10px", "padding": "6px"},
                        style_data_conditional=[{"if": {"filter_query": "{age_hr} > 8"}, "color": RED, "fontWeight": "700"}]
                    ))
        ]),
        html.Div([
            section("WIP LOTS BEFORE DM CSAM",
                    dash_table.DataTable(
                        id="dm-table",
                        columns=[{"name": x, "id": x} for x in ["timestamp","lot","device","package","priority","age_hr"]],
                        style_table={"overflowX": "auto", "maxHeight": "245px", "overflowY": "auto"},
                        style_header={"backgroundColor": "#152A39", "color": CYAN, "fontWeight": "700", "fontSize": "11px"},
                        style_cell={"backgroundColor": PANEL2, "color": TEXT, "border": f"1px solid {GRID}", "fontSize": "10px", "padding": "6px"},
                        style_data_conditional=[{"if": {"filter_query": "{age_hr} > 8"}, "color": RED, "fontWeight": "700"}]
                    ))
        ])
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "10px", "padding": "0 20px 10px"}),

    html.Div([
        html.Div([
            section("UNAVAILABLE CSAM MACHINES",
                dash_table.DataTable(
                    id="machine-table",
                    columns=[
                        {"name":"PROCESS","id":"process"},
                        {"name":"MACHINE","id":"machine"},
                        {"name":"STATUS","id":"status"},
                        {"name":"REASON","id":"reason"},
                        {"name":"LAST UPDATE","id":"last_update"}
                    ],
                    style_table={"overflowX":"auto", "maxHeight":"255px", "overflowY":"auto"},
                    style_header={"backgroundColor":"#152A39","color":CYAN,"fontWeight":"700","fontSize":"10px"},
                    style_cell={"backgroundColor":PANEL2,"color":TEXT,"border":f"1px solid {GRID}","fontSize":"10px","padding":"6px"},
                    style_data_conditional=[
                        {"if":{"filter_query":'{status} = "Unavailable"'},"color":RED,"fontWeight":"700"},
                        {"if":{"filter_query":'{status} = "Available"'},"color":GREEN}
                    ]
                ))
        ]),
        html.Div([
            section("QUALITY CONTROL / ACTION VIEW",
                html.Div([
                    html.Div("1. Escalate WIP > age limit to CSAM owner", style={"padding":"9px 0","borderBottom":f"1px solid {GRID}", "color":TEXT}),
                    html.Div("2. Review unavailable machine reason every shift", style={"padding":"9px 0","borderBottom":f"1px solid {GRID}", "color":TEXT}),
                    html.Div("3. Prioritize Hot Lot / customer-critical WIP", style={"padding":"9px 0","borderBottom":f"1px solid {GRID}", "color":TEXT}),
                    html.Div("4. Track machine recovery ETA and containment", style={"padding":"9px 0","color":TEXT}),
                ], style={"fontSize":"11px"})
            )
        ])
    ], style={"display":"grid","gridTemplateColumns":"2fr 1fr","gap":"10px","padding":"0 20px 20px"}),

], style={"background": BG, "minHeight": "100vh", "fontFamily": "Arial, sans-serif"})

# -------------------------
# Callback
# -------------------------
@app.callback(
    Output("kpi-row", "children"),
    Output("wip-by-process", "figure"),
    Output("machine-availability", "figure"),
    Output("up-table", "data"),
    Output("lid-table", "data"),
    Output("dm-table", "data"),
    Output("machine-table", "data"),
    Output("last-update", "children"),
    Input("refresh", "n_intervals"),
    Input("process-filter", "value"),
    Input("age-limit", "value")
)
def update_dashboard(_, selected_process, age_limit):
    wip, machines = load_data()

    if selected_process != "ALL":
        wip_view = wip[wip["process"] == selected_process].copy()
        machine_view = machines[machines["process"] == selected_process].copy()
    else:
        wip_view = wip.copy()
        machine_view = machines.copy()

    total_wip = len(wip_view)
    aged_wip = int((wip_view["age_hr"] > float(age_limit or 8)).sum())
    unavailable = int((machine_view["status"] == "Unavailable").sum())
    total_machines = len(machine_view)
    availability = 100 * (total_machines - unavailable) / total_machines if total_machines else 0

    # KPIs
    kpis = [
        card("TOTAL WIP LOTS", total_wip, "lots in CSAM queue", CYAN),
        card("AGED WIP", aged_wip, f"> {age_limit} hr threshold", RED if aged_wip else GREEN),
        card("MACHINE AVAILABILITY", f"{availability:.1f}%", f"{total_machines-unavailable}/{total_machines} machines available", GREEN if availability >= 90 else AMBER),
        card("UNAVAILABLE MACHINES", unavailable, "requires owner action", RED if unavailable else GREEN),
        card("HOT LOTS", int((wip_view["priority"] == "Hot Lot").sum()), "priority queue", AMBER),
    ]

    # WIP by process
    counts = wip_view.groupby("process").size().reset_index(name="WIP")
    fig1 = px.bar(counts, x="WIP", y="process", orientation="h", text="WIP")
    fig1.update_traces(marker_color=CYAN, textposition="outside")
    fig1.update_layout(
        template="plotly_dark", paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        font={"color": TEXT}, margin={"l":80,"r":35,"t":15,"b":35},
        xaxis={"gridcolor":GRID, "title":None}, yaxis={"gridcolor":PANEL, "title":None}
    )

    # Machine availability
    m = machine_view.groupby(["process","status"]).size().reset_index(name="count")
    fig2 = px.bar(m, x="process", y="count", color="status", barmode="stack",
                  color_discrete_map={"Available": GREEN, "Unavailable": RED},
                  text="count")
    fig2.update_layout(
        template="plotly_dark", paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        font={"color": TEXT}, margin={"l":40,"r":20,"t":15,"b":35},
        xaxis={"gridcolor":PANEL}, yaxis={"gridcolor":GRID, "title":None},
        legend={"orientation":"h","y":1.12}
    )

    # Tables
    def table_data(process):
        cols = ["timestamp","lot","device","package","priority","age_hr"]
        df = wip_view[wip_view["process"] == process].sort_values("age_hr", ascending=False).head(15).copy()
        if df.empty:
            return []
        df["age_hr"] = df["age_hr"].round(1)
        return df[cols].to_dict("records")

    unavailable_rows = machine_view.sort_values(["status","process"], ascending=[True, True])
    return (
        kpis, fig1, fig2,
        table_data("UP CSAM"), table_data("Lid CSAM"), table_data("DM CSAM"),
        unavailable_rows.to_dict("records"),
        "LIVE DEMO • Updated " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
