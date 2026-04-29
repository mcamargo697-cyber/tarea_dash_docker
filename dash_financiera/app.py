import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go


# ============================================================
# ESTILO EXTERNO BOOTSTRAP
# ============================================================

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


# ============================================================
# CARGA DE DATOS
# ============================================================

df = pd.read_csv(
    "https://raw.githubusercontent.com/lihkir/Uninorte/main/AppliedStatisticMS/DataVisualizationRPython/Lectures/Python/PythonDataSets/dash-stock-ticker-demo.csv"
)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(["Stock", "Date"])

stocks = sorted(df["Stock"].dropna().unique())


# ============================================================
# FUNCIONES DE INDICADORES TECNICOS
# ============================================================

def bollinger_bands(price, window=20, num_std=2):
    rolling_mean = price.rolling(window=window).mean()
    rolling_std = price.rolling(window=window).std()

    upper_band = rolling_mean + num_std * rolling_std
    lower_band = rolling_mean - num_std * rolling_std

    return rolling_mean, upper_band, lower_band


def sma(price, window=20):
    return price.rolling(window=window).mean()


def ema(price, span=20):
    return price.ewm(span=span, adjust=False).mean()


def macd(price, fast=12, slow=26, signal=9):
    ema_fast = price.ewm(span=fast, adjust=False).mean()
    ema_slow = price.ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram


def rsi(price, window=14):
    delta = price.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi_value = 100 - (100 / (1 + rs))

    return rsi_value


def obv(close, volume):
    direction = close.diff()

    obv_values = []
    current_obv = 0

    for i in range(len(close)):
        if i == 0:
            obv_values.append(0)
        elif direction.iloc[i] > 0:
            current_obv += volume.iloc[i]
            obv_values.append(current_obv)
        elif direction.iloc[i] < 0:
            current_obv -= volume.iloc[i]
            obv_values.append(current_obv)
        else:
            obv_values.append(current_obv)

    return pd.Series(obv_values, index=close.index)


# ============================================================
# ESTILOS
# ============================================================

PAGE_STYLE = {
    "backgroundColor": "#f3f4f6",
    "minHeight": "100vh",
    "padding": "25px",
}

CARD_STYLE = {
    "backgroundColor": "white",
    "padding": "18px",
    "borderRadius": "14px",
    "boxShadow": "0 4px 14px rgba(0,0,0,0.12)",
    "marginBottom": "18px",
}

TITLE_STYLE = {
    "fontWeight": "bold",
    "color": "#111827",
    "marginBottom": "5px",
}

TEXT_STYLE = {
    "fontSize": "16px",
    "color": "#4b5563",
}


# ============================================================
# LAYOUT
# ============================================================

app.layout = html.Div(
    style=PAGE_STYLE,
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
                                    "Financial Technical Analysis Explorer",
                                    style=TITLE_STYLE,
                                ),
                                html.P(
                                    "Dashboard interactivo para visualizar candlesticks e indicadores técnicos en un mismo gráfico.",
                                    style=TEXT_STYLE,
                                ),
                            ]
                        ),
                        html.Img(
                            src="https://upload.wikimedia.org/wikipedia/commons/3/37/Plotly-logo-01-square.png",
                            style={
                                "height": "90px",
                                "width": "90px",
                                "objectFit": "contain",
                                "borderRadius": "18px",
                                "boxShadow": "0 4px 12px rgba(0,0,0,0.18)",
                            },
                        ),
                    ],
                ),

                # FILTROS
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="col-lg-3 col-md-6",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.Label(
                                            "Seleccione uno o varios stocks",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="stock-dropdown",
                                            options=[
                                                {"label": stock, "value": stock}
                                                for stock in stocks
                                            ],
                                            value=["AAPL"],
                                            multi=True,
                                            clearable=False,
                                        ),
                                    ],
                                )
                            ],
                        ),

                        html.Div(
                            className="col-lg-3 col-md-6",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.Label(
                                            "Seleccione indicadores técnicos",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="indicator-dropdown",
                                            options=[
                                                {
                                                    "label": "Bollinger Bands",
                                                    "value": "BBANDS",
                                                },
                                                {
                                                    "label": "Media móvil simple - SMA",
                                                    "value": "SMA",
                                                },
                                                {
                                                    "label": "Media móvil exponencial - EMA",
                                                    "value": "EMA",
                                                },
                                                {
                                                    "label": "MACD",
                                                    "value": "MACD",
                                                },
                                                {
                                                    "label": "RSI",
                                                    "value": "RSI",
                                                },
                                                {
                                                    "label": "On-Balance Volume - OBV",
                                                    "value": "OBV",
                                                },
                                            ],
                                            value=[
                                                "BBANDS",
                                                "SMA",
                                                "EMA",
                                                "MACD",
                                                "RSI",
                                            ],
                                            multi=True,
                                            clearable=False,
                                        ),
                                    ],
                                )
                            ],
                        ),

                        html.Div(
                            className="col-lg-2 col-md-4",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.Label(
                                            "Periodo media móvil",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="window-dropdown",
                                            options=[
                                                {"label": str(w), "value": w}
                                                for w in [5, 10, 20, 30, 50]
                                            ],
                                            value=20,
                                            clearable=False,
                                        ),
                                    ],
                                )
                            ],
                        ),

                        html.Div(
                            className="col-lg-2 col-md-4",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.Label(
                                            "Desviaciones Bollinger",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="std-dropdown",
                                            options=[
                                                {"label": str(s), "value": s}
                                                for s in [1, 2, 3, 4, 5]
                                            ],
                                            value=2,
                                            clearable=False,
                                        ),
                                    ],
                                )
                            ],
                        ),

                        html.Div(
                            className="col-lg-2 col-md-4",
                            children=[
                                html.Div(
                                    style=CARD_STYLE,
                                    children=[
                                        html.Label(
                                            "Periodo RSI",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="rsi-window-dropdown",
                                            options=[
                                                {"label": str(w), "value": w}
                                                for w in [7, 14, 21, 28]
                                            ],
                                            value=14,
                                            clearable=False,
                                        ),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),

                # DESCRIPCION
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H4(
                            "Lectura del dashboard",
                            style={"fontWeight": "bold"},
                        ),
                        html.P(
                            "El gráfico principal muestra el candlestick del stock seleccionado. "
                            "Sobre el mismo chart se agregan indicadores técnicos como Bollinger Bands, SMA, EMA, MACD, RSI y OBV. "
                            "El objetivo es facilitar la comparación visual de varias señales antes de tomar una decisión de compra o venta.",
                            style=TEXT_STYLE,
                        ),
                    ],
                ),

                # CONTENEDOR DE GRAFICOS
                html.Div(id="graphs-container"),
            ],
        )
    ],
)


# ============================================================
# CALLBACK PRINCIPAL
# ============================================================

@app.callback(
    Output("graphs-container", "children"),
    [
        Input("stock-dropdown", "value"),
        Input("indicator-dropdown", "value"),
        Input("window-dropdown", "value"),
        Input("std-dropdown", "value"),
        Input("rsi-window-dropdown", "value"),
    ],
)
def update_finance_dashboard(
    selected_stocks,
    selected_indicators,
    selected_window,
    selected_std,
    selected_rsi_window,
):

    if not selected_stocks:
        return [
            html.Div(
                style=CARD_STYLE,
                children=[
                    html.H4("Seleccione al menos un stock.")
                ],
            )
        ]

    if not selected_indicators:
        selected_indicators = []

    graphs = []

    for ticker in selected_stocks:
        dff = df[df["Stock"] == ticker].copy()
        dff = dff.sort_values("Date")

        fig = go.Figure()

        # ====================================================
        # CANDLESTICK BASE
        # ====================================================

        fig.add_trace(
            go.Candlestick(
                x=dff["Date"],
                open=dff["Open"],
                high=dff["High"],
                low=dff["Low"],
                close=dff["Close"],
                name=f"{ticker} Candlestick",
                increasing_line_color="#16a34a",
                decreasing_line_color="#dc2626",
            )
        )

        # ====================================================
        # BOLLINGER BANDS
        # ====================================================

        if "BBANDS" in selected_indicators:
            rolling_mean, upper_band, lower_band = bollinger_bands(
                dff["Close"],
                window=selected_window,
                num_std=selected_std,
            )

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=upper_band,
                    mode="lines",
                    name=f"Bollinger superior ({selected_window}, {selected_std}σ)",
                    line=dict(width=1),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=rolling_mean,
                    mode="lines",
                    name=f"Media Bollinger ({selected_window})",
                    line=dict(width=1, dash="dot"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=lower_band,
                    mode="lines",
                    name=f"Bollinger inferior ({selected_window}, {selected_std}σ)",
                    line=dict(width=1),
                )
            )

        # ====================================================
        # SMA
        # ====================================================

        if "SMA" in selected_indicators:
            sma_values = sma(dff["Close"], window=selected_window)

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=sma_values,
                    mode="lines",
                    name=f"SMA {selected_window}",
                    line=dict(width=2),
                )
            )

        # ====================================================
        # EMA
        # ====================================================

        if "EMA" in selected_indicators:
            ema_values = ema(dff["Close"], span=selected_window)

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=ema_values,
                    mode="lines",
                    name=f"EMA {selected_window}",
                    line=dict(width=2),
                )
            )

        # ====================================================
        # MACD
        # ====================================================

        if "MACD" in selected_indicators:
            macd_line, signal_line, histogram = macd(dff["Close"])

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=macd_line,
                    mode="lines",
                    name="MACD",
                    yaxis="y2",
                    line=dict(width=1),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=signal_line,
                    mode="lines",
                    name="Señal MACD",
                    yaxis="y2",
                    line=dict(width=1, dash="dash"),
                )
            )

        # ====================================================
        # RSI
        # ====================================================

        if "RSI" in selected_indicators:
            rsi_values = rsi(
                dff["Close"],
                window=selected_rsi_window,
            )

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=rsi_values,
                    mode="lines",
                    name=f"RSI {selected_rsi_window}",
                    yaxis="y2",
                    line=dict(width=1),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=[70] * len(dff),
                    mode="lines",
                    name="RSI sobrecompra 70",
                    yaxis="y2",
                    line=dict(width=1, dash="dot"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=[30] * len(dff),
                    mode="lines",
                    name="RSI sobreventa 30",
                    yaxis="y2",
                    line=dict(width=1, dash="dot"),
                )
            )

        # ====================================================
        # OBV
        # ====================================================

        if "OBV" in selected_indicators:
            obv_values = obv(dff["Close"], dff["Volume"])

            fig.add_trace(
                go.Scatter(
                    x=dff["Date"],
                    y=obv_values,
                    mode="lines",
                    name="OBV",
                    yaxis="y3",
                    line=dict(width=1),
                )
            )

        # ====================================================
        # LAYOUT DEL GRAFICO
        # ====================================================

        fig.update_layout(
            title=f"Análisis técnico integrado - {ticker}",
            template="plotly_white",
            height=750,
            xaxis=dict(
                title="Fecha",
                rangeslider=dict(visible=False),
            ),
            yaxis=dict(
                title="Precio",
                side="left",
            ),
            yaxis2=dict(
                title="MACD / RSI",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
            yaxis3=dict(
                title="OBV",
                overlaying="y",
                side="right",
                anchor="free",
                position=0.95,
                showgrid=False,
                visible=True,
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0,
            ),
            margin=dict(l=40, r=80, t=100, b=40),
        )

        latest = dff.iloc[-1]

        card = html.Div(
            style=CARD_STYLE,
            children=[
                html.H3(
                    f"{ticker}",
                    style={"fontWeight": "bold"},
                ),
                html.P(
                    f"Último cierre disponible: {latest['Close']:.2f}. "
                    f"Volumen: {latest['Volume']:.0f}. "
                    "Los indicadores seleccionados se muestran en el mismo gráfico para facilitar la confirmación visual.",
                    style=TEXT_STYLE,
                ),
                dcc.Graph(figure=fig),
            ],
        )

        graphs.append(card)

    return graphs


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9010)