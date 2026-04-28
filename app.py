# ============================================
# 📦 IMPORTS
# ============================================
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# ============================================
# 📂 DADOS
# ============================================
df_resultados = pd.read_csv("alunos_resultado.csv")
df_erros = pd.read_csv("alunos_erros_detalhados.csv")
df_intervencoes = pd.read_csv("alunos_intervencao.csv")

# ============================================
# 🎨 APP
# ============================================
app = Dash(__name__)

# ============================================
# 🎯 FUNÇÃO CARD
# ============================================
def card(titulo, valor):
    return html.Div([
        html.H4(titulo),
        html.H2(valor)
    ], style={
        "background": "white",
        "padding": "20px",
        "borderRadius": "12px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
        "flex": "1",
        "textAlign": "center"
    })

# ============================================
# 🧱 LAYOUT
# ============================================
app.layout = html.Div(style={
    "fontFamily": "Arial",
    "background": "#f4f6f9",
    "padding": "20px"
}, children=[

    html.H1("📊 Dashboard Inteligente de Alfabetização", style={"textAlign": "center"}),

    # =========================
    # 🎯 FILTRO
    # =========================
    dcc.Dropdown(
        id="aluno-dropdown",
        options=[{"label": f"Aluno {i}", "value": i} for i in df_resultados["aluno_id"]],
        value=1
    ),

    # =========================
    # 🚨 ALERTA
    # =========================
    html.Div(id="alerta"),

    # =========================
    # 📊 CARDS KPI
    # =========================
    html.Div(id="kpis", style={"display": "flex", "gap": "10px", "marginTop": "20px"}),

    # =========================
    # 📈 GRÁFICO ERROS
    # =========================
    dcc.Graph(id="grafico-erros"),

    # =========================
    # ❌ RESUMO + 🧠 INTERVENÇÃO
    # =========================
    html.Div(id="resumo-erros", style={"marginTop": "20px"}),

    # =========================
    # 📋 TABELA DETALHADA
    # =========================
    html.Div(id="tabela-erros", style={"marginTop": "20px"}),

    # =========================
    # 🏆 RANKING
    # =========================
    html.Div([
        html.H3("🏆 Ranking de Alunos"),

        html.Div([
            html.Div([
                html.H4("🔴 Piores (maior score)"),
                html.Ul([
                    html.Li(f"Aluno {row.aluno_id} - Score {row.score}")
                    for _, row in df_resultados.sort_values(by="score", ascending=False).head(5).iterrows()
                ])
            ], style={"flex": 1}),

            html.Div([
                html.H4("🟢 Melhores (menor score)"),
                html.Ul([
                    html.Li(f"Aluno {row.aluno_id} - Score {row.score}")
                    for _, row in df_resultados.sort_values(by="score", ascending=True).head(5).iterrows()
                ])
            ], style={"flex": 1}),

        ], style={"display": "flex", "gap": "20px"})
    ], style={"marginTop": "40px"}),

    # =========================
    # 📊 ROSCA FINAL
    # =========================
    html.Div([
        html.H3("📊 Distribuição de Níveis (Todos os Alunos)", style={"textAlign": "center"}),

        dcc.Graph(
            figure=px.pie(
                df_resultados,
                names="nivel",
                color="nivel",
                hole=0.5
            )
        )
    ], style={"marginTop": "40px"})
])

# ============================================
# 🔄 CALLBACK
# ============================================
@app.callback(
    [
        Output("kpis", "children"),
        Output("grafico-erros", "figure"),
        Output("alerta", "children"),
        Output("resumo-erros", "children"),
        Output("tabela-erros", "children"),
    ],
    [Input("aluno-dropdown", "value")]
)
def atualizar(aluno_id):

    df_a = df_resultados[df_resultados["aluno_id"] == aluno_id]
    df_e = df_erros[df_erros["aluno_id"] == aluno_id]
    df_i = df_intervencoes[df_intervencoes["aluno_id"] == aluno_id]

    nivel = df_a["nivel"].values[0]
    score = df_a["score"].values[0]
    nivel_erro = df_a["nivel_erro"].values[0]

    # =========================
    # 🚨 ALERTA
    # =========================
    if score > 3:
        alerta = html.Div("🚨 Aluno em nível crítico! Intervenção urgente necessária.", style={
            "background": "#ffcccc",
            "padding": "10px",
            "borderRadius": "8px",
            "marginTop": "10px"
        })
    else:
        alerta = html.Div("✅ Situação sob controle", style={
            "background": "#ccffcc",
            "padding": "10px",
            "borderRadius": "8px",
            "marginTop": "10px"
        })

    # =========================
    # 📊 CARDS
    # =========================
    kpis = [
        card("Nível", nivel),
        card("Score", score),
        card("Nível de Erro", nivel_erro)
    ]

    # =========================
    # 📈 GRÁFICO
    # =========================
    resumo_df = df_e["tipo"].value_counts().reset_index()
    resumo_df.columns = ["tipo", "quantidade"]

    fig = px.bar(resumo_df, x="tipo", y="quantidade", title="Erros do Aluno")

    # =========================
    # ❌ RESUMO DE ERROS
    # =========================
    contagem = df_e["tipo"].value_counts()

    resumo = html.Div([
        html.H3("❌ Resumo de tipos"),
        html.Ul([
            html.Li(f"Omissão: {contagem.get('omissao', 0)}"),
            html.Li(f"Adição: {contagem.get('adicao', 0)}"),
            html.Li(f"Substituição: {contagem.get('substituicao', 0)}"),
            html.Li(f"Fonológico: {contagem.get('fonologico', 0)}"),
        ])
    ])

    # =========================
    # 🧠 INTERVENÇÃO
    # =========================
    intervencao = html.Div([
        html.H3("🧠 Intervenções"),
        html.Div(df_i["recomendacoes"].values[0], style={
            "background": "#f8f9fa",
            "padding": "10px",
            "borderRadius": "8px"
        })
    ])

    bloco_resumo = html.Div([resumo, intervencao])

    # =========================
    # 📋 TABELA
    # =========================
    tabela = html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df_e.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df_e.iloc[i][col]) for col in df_e.columns
            ]) for i in range(len(df_e))
        ])
    ], style={
        "width": "100%",
        "border": "1px solid #ccc",
        "marginTop": "10px"
    })

    return kpis, fig, alerta, bloco_resumo, tabela



server = app.server

if __name__ == "__main__":
    app.run(debug=True)
