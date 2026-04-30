import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os

# ============================================================
# ESTILO EXTERNO BOOTSTRAP
# ============================================================

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


# ============================================================
# CARGA Y PREPROCESAMIENTO DE DATOS
# ============================================================

df = pd.read_csv(
    "https://raw.githubusercontent.com/lihkir/Uninorte/main/AppliedStatisticMS/DataVisualizationRPython/Lectures/Python/PythonDataSets/intro_bees.csv"
)

df = (
    df.groupby(
        ["State", "ANSI", "Affected by", "Year", "state_code"],
        as_index=False
    )[["Pct of Colonies Impacted"]]
    .mean()
)

years = sorted(df["Year"].unique())
affected_options = sorted(df["Affected by"].unique())


# ============================================================
# ESTILOS
# ============================================================

CARD_STYLE = {
    "backgroundColor": "#1f2c3a",
    "padding": "18px",
    "borderRadius": "14px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.25)",
    "marginBottom": "18px",
}

TITLE_STYLE = {
    "color": "#f9fafb",
    "fontWeight": "bold",
    "marginBottom": "5px",
}

TEXT_STYLE = {
    "color": "#d1d5db",
    "fontSize": "16px",
}


# ============================================================
# LAYOUT
# ============================================================

app.layout = html.Div(
    style={
        "backgroundColor": "#111827",
        "minHeight": "100vh",
        "padding": "25px",
    },
    children=[
        html.Div(
            className="container-fluid",
            children=[
                # ENCABEZADO
                html.Div(
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "marginBottom": "25px",
                    },
                    children=[
                        html.Div(
                            children=[
                                html.H1(
                                    "Bee Health Explorer",
                                    style=TITLE_STYLE,
                                ),
                                html.P(
                                    "Dashboard interactivo para analizar el porcentaje promedio de colonias de abejas afectadas en Estados Unidos.",
                                    style=TEXT_STYLE,
                                ),
                            ]
                        ),
                        html.Img(
                            src="https://upload.wikimedia.org/wikipedia/commons/4/4c/Bee_Collecting_Pollen_2004-08-14.jpg",
                            style={
                                "height": "95px",
                                "width": "95px",
                                "objectFit": "cover",
                                "borderRadius": "50%",
                                "border": "3px solid #f59e0b",
                            },
                        ),
                    ],
                ),

                # FILTROS
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.Label(
                                            "Seleccione el año",
                                            style={
                                                "color": "#f9fafb",
                                                "fontWeight": "bold",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="year-dropdown",
                                            options=[
                                                {
                                                    "label": str(year),
                                                    "value": int(year),
                                                }
                                                for year in years
                                            ],
                                            value=int(years[0]),
                                            clearable=False,
                                            style={"color": "#111827"},
                                        ),
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.Label(
                                            "Seleccione la causa de afectación",
                                            style={
                                                "color": "#f9fafb",
                                                "fontWeight": "bold",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="affected-dropdown",
                                            options=[
                                                {
                                                    "label": affected,
                                                    "value": affected,
                                                }
                                                for affected in affected_options
                                            ],
                                            value="Varroa_mites"
                                            if "Varroa_mites" in affected_options
                                            else affected_options[0],
                                            clearable=False,
                                            style={"color": "#111827"},
                                        ),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),

                # TARJETAS RESUMEN
                html.Div(
                    id="summary-cards",
                    className="row",
                ),

                # MAPA
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H3(
                            "Mapa coroplético por estado",
                            style={"color": "#f9fafb"},
                        ),
                        dcc.Graph(id="bee-map"),
                    ],
                ),

                # GRAFICOS DESCRIPTIVOS 1
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.H4(
                                            "Top 10 estados más afectados",
                                            style={"color": "#f9fafb"},
                                        ),
                                        dcc.Graph(id="top-states-bar"),
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.H4(
                                            "Evolución temporal de la causa seleccionada",
                                            style={"color": "#f9fafb"},
                                        ),
                                        dcc.Graph(id="temporal-line"),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),

                # GRAFICOS DESCRIPTIVOS 2
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.H4(
                                            "Distribución por causa de afectación",
                                            style={"color": "#f9fafb"},
                                        ),
                                        dcc.Graph(id="affected-box"),
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.H4(
                                            "Promedio por causa y año",
                                            style={"color": "#f9fafb"},
                                        ),
                                        dcc.Graph(id="heatmap"),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )
    ],
)


# ============================================================
# CALLBACK PRINCIPAL
# ============================================================

@app.callback(
    [
        Output("summary-cards", "children"),
        Output("bee-map", "figure"),
        Output("top-states-bar", "figure"),
        Output("temporal-line", "figure"),
        Output("affected-box", "figure"),
        Output("heatmap", "figure"),
    ],
    [
        Input("year-dropdown", "value"),
        Input("affected-dropdown", "value"),
    ],
)
def update_dashboard(selected_year, selected_affected):
    dff = df[
        (df["Year"] == selected_year)
        & (df["Affected by"] == selected_affected)
    ].copy()

    national_mean = dff["Pct of Colonies Impacted"].mean()
    n_states = dff["State"].nunique()

    if not dff.empty:
        max_row = dff.loc[dff["Pct of Colonies Impacted"].idxmax()]
        max_state = max_row["State"]
        max_value = max_row["Pct of Colonies Impacted"]
    else:
        max_state = "N/A"
        max_value = 0

    summary_cards = [
        html.Div(
            className="col-md-4",
            children=[
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H5(
                            "Promedio nacional",
                            style={"color": "#d1d5db"},
                        ),
                        html.H2(
                            f"{national_mean:.2f} %",
                            style={
                                "color": "#f59e0b",
                                "fontWeight": "bold",
                            },
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            className="col-md-4",
            children=[
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H5(
                            "Estado más afectado",
                            style={"color": "#d1d5db"},
                        ),
                        html.H2(
                            max_state,
                            style={
                                "color": "#f59e0b",
                                "fontWeight": "bold",
                            },
                        ),
                        html.P(
                            f"{max_value:.2f} %",
                            style={"color": "#d1d5db"},
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            className="col-md-4",
            children=[
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H5(
                            "Estados analizados",
                            style={"color": "#d1d5db"},
                        ),
                        html.H2(
                            str(n_states),
                            style={
                                "color": "#f59e0b",
                                "fontWeight": "bold",
                            },
                        ),
                    ],
                )
            ],
        ),
    ]

    # ========================================================
    # MAPA COROPLETICO
    # ========================================================

    fig_map = px.choropleth(
        dff,
        locationmode="USA-states",
        locations="state_code",
        scope="usa",
        color="Pct of Colonies Impacted",
        hover_data=[
            "State",
            "Affected by",
            "Pct of Colonies Impacted",
        ],
        color_continuous_scale="YlOrRd",
        labels={
            "Pct of Colonies Impacted": "% colonias afectadas"
        },
        template="plotly_dark",
    )

    fig_map.update_layout(
        paper_bgcolor="#1f2c3a",
        plot_bgcolor="#1f2c3a",
        margin=dict(l=0, r=0, t=20, b=0),
    )

    # ========================================================
    # TOP 10 ESTADOS MAS AFECTADOS
    # ========================================================

    top_states = (
        dff.sort_values(
            "Pct of Colonies Impacted",
            ascending=False,
        )
        .head(10)
    )

    fig_bar = px.bar(
        top_states,
        x="Pct of Colonies Impacted",
        y="State",
        orientation="h",
        color="Pct of Colonies Impacted",
        color_continuous_scale="YlOrRd",
        template="plotly_dark",
        labels={
            "Pct of Colonies Impacted": "% colonias afectadas",
            "State": "Estado",
        },
    )

    fig_bar.update_layout(
        yaxis={"categoryorder": "total ascending"},
        paper_bgcolor="#1f2c3a",
        plot_bgcolor="#1f2c3a",
    )

    # ========================================================
    # SERIE TEMPORAL
    # ========================================================

    temporal = (
        df[df["Affected by"] == selected_affected]
        .groupby("Year", as_index=False)["Pct of Colonies Impacted"]
        .mean()
    )

    fig_line = px.line(
        temporal,
        x="Year",
        y="Pct of Colonies Impacted",
        markers=True,
        template="plotly_dark",
        labels={
            "Pct of Colonies Impacted": "% promedio",
            "Year": "Año",
        },
    )

    fig_line.update_layout(
        paper_bgcolor="#1f2c3a",
        plot_bgcolor="#1f2c3a",
    )

    # ========================================================
    # BOXPLOT POR CAUSA
    # ========================================================

    fig_box = px.box(
        df[df["Year"] == selected_year],
        x="Affected by",
        y="Pct of Colonies Impacted",
        template="plotly_dark",
        labels={
            "Affected by": "Causa",
            "Pct of Colonies Impacted": "% colonias afectadas",
        },
    )

    fig_box.update_layout(
        paper_bgcolor="#1f2c3a",
        plot_bgcolor="#1f2c3a",
        xaxis_tickangle=-35,
    )

    # ========================================================
    # HEATMAP CAUSA VS AÑO
    # ========================================================

    heat = (
        df.groupby(["Affected by", "Year"], as_index=False)[
            "Pct of Colonies Impacted"
        ]
        .mean()
    )

    fig_heat = px.density_heatmap(
        heat,
        x="Year",
        y="Affected by",
        z="Pct of Colonies Impacted",
        color_continuous_scale="YlOrRd",
        template="plotly_dark",
        labels={
            "Pct of Colonies Impacted": "% promedio",
            "Year": "Año",
            "Affected by": "Causa",
        },
    )

    fig_heat.update_layout(
        paper_bgcolor="#1f2c3a",
        plot_bgcolor="#1f2c3a",
    )

    return (
        summary_cards,
        fig_map,
        fig_bar,
        fig_line,
        fig_box,
        fig_heat,
    )


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    app.run(debug=False, host="0.0.0.0", port=port)