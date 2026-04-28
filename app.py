# ============================================
# 📦 IMPORTS
# ============================================
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# ============================================
# 📂 CARREGAR DADOS (com segurança)
# ============================================
try:
    df_erros = pd.read_csv("analise_erros.csv")
    df_resumo = pd.read_csv("resumo_erros.csv")
    df_features = pd.read_csv("features.csv")
    df_intervencao = pd.read_csv("intervencao.csv")
except Exception as e:
    print("❌ Erro ao carregar CSV:", e)
    exit()

# ============================================
# 🎯 DADOS PRINCIPAIS
# ============================================
score = int(df_intervencao["score"][0])
nivel_erro = df_intervencao["nivel_erro"][0]
recomendacoes = df_intervencao["recomendacoes"][0]

# ============================================
# 📊 GRÁFICOS
# ============================================

# Gráfico de erros
df_plot = df_resumo.melt(var_name="tipo", value_name="quantidade")

fig_erros = px.bar(
    df_plot,
    x="tipo",
    y="quantidade",
    title="Distribuição de Erros"
)

# ============================================
# 🎨 APP DASH
# ============================================
app = Dash(__name__)

app.layout = html.Div(style={"fontFamily": "Arial", "padding": "20px"}, children=[

    html.H1("📊 Dashboard de Alfabetização", style={"textAlign": "center"}),

    # =========================
    # KPI PRINCIPAL
    # =========================
    html.Div([
        html.Div([
            html.H2("Score"),
            html.H1(score)
        ], style={"flex": "1", "textAlign": "center"}),

        html.Div([
            html.H2("Nível de Erro"),
            html.H3(nivel_erro)
        ], style={"flex": "1", "textAlign": "center"}),

    ], style={"display": "flex", "margin": "20px"}),

    # =========================
    # FEATURES
    # =========================
    html.Div([
        html.H3("📈 Features"),
        html.Ul([
            html.Li(f"Total de palavras: {df_features['total_palavras'][0]}"),
            html.Li(f"Tamanho médio: {df_features['tamanho_medio'][0]:.2f}"),
            html.Li(f"Diversidade lexical: {df_features['diversidade_lexica'][0]:.2f}"),
            html.Li(f"Erro médio: {df_features['erro_medio'][0]:.2f}")
        ])
    ], style={"marginTop": "20px"}),

    # =========================
    # GRÁFICO
    # =========================
    html.Div([
        dcc.Graph(figure=fig_erros)
    ]),

    # =========================
    # RESUMO ERROS
    # =========================
    html.Div([
        html.H3("❌ Resumo de Erros"),
        html.Ul([
            html.Li(f"Omissão: {df_resumo['omissao'][0]}"),
            html.Li(f"Adição: {df_resumo['adicao'][0]}"),
            html.Li(f"Substituição: {df_resumo['substituicao'][0]}"),
            html.Li(f"Fonológico: {df_resumo['fonologico'][0]}")
        ])
    ], style={"marginTop": "20px"}),

    # =========================
    # INTERVENÇÃO
    # =========================
    html.Div([
        html.H3("🧠 Intervenções"),
        html.Div(recomendacoes, style={
            "background": "#f8f9fa",
            "padding": "10px",
            "borderRadius": "8px"
        })
    ], style={"marginTop": "20px"}),

    # =========================
    # TABELA DE ERROS
    # =========================
    html.Div([
        html.H3("📋 Detalhamento dos Erros"),
        html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in df_erros.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(df_erros.iloc[i][col]) for col in df_erros.columns
                ]) for i in range(len(df_erros))
            ])
        ], style={"width": "100%", "border": "1px solid black"})
    ], style={"marginTop": "20px"})

])

# ============================================
# ▶️ RODAR APP
# ============================================
if __name__ == "__main__":
    app.run(debug=True, port=8050)