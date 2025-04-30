
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import datetime
from textblob import TextBlob
import random

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Mental Health & Well-Being Dashboard"
app.config.suppress_callback_exceptions = True

LA_TROBE_RED = "#CD2F2B"
logo_path = "/assets/logo.png"
ai_avatar_path = "/assets/ai-avatar.png"
mood_icons = {
    "Positive": "/assets/happy.png",
    "Neutral": "/assets/neutral.png",
    "Negative": "/assets/sad.png"
}

# 模拟历史数据
def generate_history():
    history = []
    start = datetime.date(2025, 3, 1)
    end = datetime.date.today() - datetime.timedelta(days=1)
    for i in range((end - start).days):
        d = start + datetime.timedelta(days=i)
        history.append({
            "date": d.strftime("%b %d"),
            "mood": random.choice(["Positive", "Neutral", "Negative"]),
            "stress": random.randint(3, 9),
            "anxiety": random.randint(3, 9)
        })
    return history
    start = datetime.date(2025, 3, 1)
    end = datetime.date.today() - datetime.timedelta(days=1)
    for i in range((end - start).days):
        d = start + datetime.timedelta(days=i)
        history.append({
            "date": d.strftime("%b %d"),
            "mood": random.choice(["Positive", "Neutral", "Negative"]),
            "stress": random.randint(3, 9),
            "anxiety": random.randint(3, 9)
        })
    return history, ""

# Layout 页面
initial_chat = [{"role": "ai", "message": "🙂 Hello! I'm here to support you. How are you feeling today?"}]
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="chat-store", data=initial_chat),
    dcc.Store(id="mood-history", data=generate_history()),
    html.Div([
        html.Img(src=logo_path, style={"width": "100%", "marginBottom": "1rem"}),
        html.Hr(),
        dbc.Nav([
            dbc.NavLink("Overview", href="/", active="exact", className="text-white"),
            dbc.NavLink("Reports", href="/reports", active="exact", className="text-white"),
            dbc.NavLink("Surveys", href="/surveys", active="exact", className="text-white"),
            dbc.NavLink("AI Support", href="/ai", active="exact", className="text-white"),
        ], vertical=True, pills=True)
    ], className="sidebar", style={
        "position": "fixed", "top": 0, "left": 0, "bottom": 0,
        "width": "17rem", "padding": "2rem 1rem",
        "backgroundColor": LA_TROBE_RED,
    }),
    html.Div(id="page-content", style={"marginLeft": "18rem", "padding": "2rem 1rem"})
])

def chat_bubble(message, is_user=False):
    return html.Div(message, className="chat-bubble-right" if is_user else "chat-bubble-left")

overview_layout = html.Div([
    html.H2("EMOTION TRENDS", style={"color": LA_TROBE_RED}),
    dbc.Row([
        dbc.Col(dcc.Graph(id="trend-chart", style={"height": "300px"}), width=8),
        dbc.Col([
            html.Img(src=ai_avatar_path, style={"width": "60%"}),
            html.Div(id="emotion-tip", className="mt-2")
        ])
    ]),
    dbc.Row([
        dbc.Col(html.Div(id="mood-icons", className="d-flex justify-content-around"))
    ], className="my-4"),
    dbc.Card([
        dbc.CardHeader("Daily Input"),
        dbc.CardBody([
            dcc.Textarea(id="input-text", placeholder="Describe how you feel today...", style={"width": "100%", "height": 100}),
            dbc.Button("Submit", id="submit-button", className="custom-btn mt-2"),
            html.Div(id="overview-feedback", className="mt-3")
        ])
    ]),
    html.Div(id="mood-history-display", className="mt-4")
])

reports_layout = html.Div([
    html.H2("Reports", style={"color": LA_TROBE_RED}),
    dbc.Row([
        dbc.Col(dcc.Graph(id="mood-pie")),
        dbc.Col(dcc.Graph(id="mood-bar"))
    ])
])

surveys_layout = html.Div([
    html.H2("MENTAL HEALTH & WELL-BEING SURVEYS", style={"color": LA_TROBE_RED}),
    dbc.Card([
        dbc.CardBody([
            html.P("Over the past week, how often have you been bothered by anxiety?"),
            dbc.RadioItems(
                id="survey-radio",
                options=[
                    {"label": "Not at all", "value": "0"},
                    {"label": "Several days", "value": "1"},
                    {"label": "More than half the days", "value": "2"},
                    {"label": "Nearly every day", "value": "3"}
                ],
                value="1"
            ),
            html.Br(),
            html.P("I’ve been able to cope with stress"),
            dcc.Slider(id="survey-slider", min=0, max=10, step=1, value=5),
            dbc.Button("Submit", id="survey-submit", className="custom-btn mt-3"),
            html.Div(id="survey-feedback", className="mt-3")
        ])
    ])
])

ai_layout = html.Div([
    html.H2("AI Support", style={"color": LA_TROBE_RED}),
    dbc.Card([
        dbc.CardBody([
            html.Div(id="chat-window", style={"maxHeight": "400px", "overflowY": "auto", "marginBottom": "1rem"}),
            dbc.InputGroup([
                dbc.Input(id="user-message", placeholder="How are you feeling today?"),
                dbc.Button("Send", id="send-button", className="custom-btn")
            ])
        ])
    ]),
    html.Div([
        html.Hr(),
        html.H5("Suggestions"),
        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody(["🧘 Try a breathing exercise"])])),
            dbc.Col(dbc.Card([dbc.CardBody(["🎧 Listen to calming music"])])),
            dbc.Col(dbc.Card([dbc.CardBody(["📍 View campus resources"])]))
        ])
    ])
])

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def route(path):
    if path == "/":
        return overview_layout
    elif path == "/reports":
        return reports_layout
    elif path == "/surveys":
        return surveys_layout
    elif path == "/ai":
        return ai_layout
    return html.Div("404 Page Not Found")

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"

@app.callback(
    Output("overview-feedback", "children"),
    Output("mood-icons", "children"),
    Output("mood-history", "data"),
    Input("submit-button", "n_clicks"),
    State("input-text", "value"),
    State("mood-history", "data"),
    prevent_initial_call=True
)
def handle_overview(n, val, history):
    if not val:
        return "Please write something.", [], history
    mood = analyze_sentiment(val)
    icon = html.Div([
        html.Img(src=mood_icons[mood], style={"height": "60px"}),
        html.Div(mood, className="text-center")
    ])
    today = datetime.date.today().strftime("%b %d")
    history.append({
        "date": today,
        "mood": mood,
        "stress": random.randint(4, 8),
        "anxiety": random.randint(4, 8),
        "stress": random.randint(4, 8),
        "anxiety": random.randint(4, 8)
    })
    return f"You seem to be feeling {mood}.", [icon], history

@app.callback(Output("trend-chart", "figure"), Input("mood-history", "data"))
def update_trend_chart(data):
    data = data[-7:] if data else []
    if not data:
        return {"data": [], "layout": {"title": "Emotion Trends"}}
    data = data[-7:]  # 只显示最近 7 条数据
    dates = [d["date"] for d in data]
    mood_score = {"Positive": 7, "Neutral": 5, "Negative": 3}
    mood = [mood_score.get(d.get("mood", "Neutral"), 5) for d in data if isinstance(d, dict)]
    stress = [d.get("stress", 5) for d in data if isinstance(d, dict)]
    anxiety = [d.get("anxiety", 5) for d in data if isinstance(d, dict)]
    return {
        "data": [
            {"x": dates, "y": anxiety, "type": "line", "name": "Anxiety", "line": {"color": "orange"}},
            {"x": dates, "y": stress, "type": "line", "name": "Stress", "line": {"color": "red"}},
            {"x": dates, "y": mood, "type": "line", "name": "Mood", "line": {"color": "gray"}}
        ],
        "layout": {"title": "Emotion Trends", "yaxis": {"range": [1, 10]}}
    }

@app.callback(Output("mood-history-display", "children"), Input("mood-history", "data"))
def update_history(data):
    if not data:
        return html.Div("No history data.")
    return html.Div([
        html.H5("History"),
        html.Ul([html.Li(f"{d.get('date', '-')} — {d.get('mood', '-')}") for d in reversed(data[-7:]) if isinstance(d, dict)])
    ])

@app.callback(
    Output("mood-pie", "figure"),
    Output("mood-bar", "figure"),
    Input("mood-history", "data")
)
def update_reports(data):
    if not data:
        empty_fig = {"data": [], "layout": {"title": "No data"}}
        return empty_fig, empty_fig
    mood_count = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for d in data:
        mood_count[d.get("mood", "Neutral")] += 1
    pie_fig = {
        "data": [{"labels": list(mood_count.keys()), "values": list(mood_count.values()), "type": "pie", "marker": {"colors": ["#CD2F2B", "#FFA500", "#A9A9A9"]}}],
        "layout": {"title": "Mood Distribution"}
    }
    bar_fig = {
        "data": [{"x": list(mood_count.keys()), "y": list(mood_count.values()), "type": "bar", "marker": {"color": ["#CD2F2B", "#FFA500", "#A9A9A9"]}}],
        "layout": {"title": "Mood Count"}
    }
    return pie_fig, bar_fig

@app.callback(Output("survey-feedback", "children"), Input("survey-submit", "n_clicks"),
              State("survey-radio", "value"), State("survey-slider", "value"), prevent_initial_call=True)
def survey_result(n, freq, cope):
    suggestions = [
        "Try journaling your emotions.",
        "Spending time with friends can help boost your mood.",
        "Consider taking a walk or doing light exercise.",
        "Try a breathing technique or guided meditation."
    ]
    return html.Div([
        html.Div("💡 Thank you for your response", className="fw-bold"),
        html.Div(random.choice(suggestions))
    ])

@app.callback([Output("chat-store", "data"), Output("user-message", "value")], Input("send-button", "n_clicks"),
              State("user-message", "value"), State("chat-store", "data"), prevent_initial_call=True)
def handle_chat(n, msg, history):
    if not msg:
        return history, ""
    mood = analyze_sentiment(msg)
    if mood == "Positive":
        reply = "😊 That's great to hear!"
    elif mood == "Negative":
        reply = "😟 I'm here for you. Try taking a deep breath."
    else:
        reply = "😐 Thanks for sharing. Would you like some calming resources?"
    history.append({"role": "user", "message": msg})
    history.append({"role": "ai", "message": reply})
    return history, ""

@app.callback(Output("chat-window", "children"), Input("chat-store", "data"))
def update_chat(chat_data):
    return [chat_bubble(m["message"], is_user=(m["role"] == "user")) for m in chat_data]

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)

