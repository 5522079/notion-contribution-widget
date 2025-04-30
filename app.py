import os
import re
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
limiter = Limiter(get_remote_address, app=app)

TOKEN = os.getenv('TOKEN')
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

VALID_BACKGROUND_COLORS = ['#191919', '#ffffff']
VALID_COLOR_SCHEMES = ['green', 'yellow', 'orange', 'blue', 'purple', 'pink', 'red']
VALID_SIZES = ['s', 'm', 'l']

def load_contributions(username):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    # GraphQLクエリ
    query = """
    query($username: String!) {
        user(login: $username) {
            contributionsCollection {
                contributionCalendar {
                    weeks {
                        contributionDays {
                            date
                            contributionCount
                        }
                    }
                }
            }
        }
    }
    """
    
    # リクエスト
    payload = {
        "query": query,
        "variables": {"username": username}
    }
    
    response = requests.post(GITHUB_GRAPHQL_URL, json=payload, headers=headers)
    
    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL API returned errors: {data['errors']}")
    
    # コントリビューションデータを整形
    contributions = {}
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    for week in weeks:
        for day in week["contributionDays"]:
            date = day["date"]
            count = day["contributionCount"]
            contributions[date] = count
    
    max_count = max(contributions.values(), default=0)
    
    return contributions, max_count

def get_color(count, max_count, color_scheme="green", background_color="#191919"):
    color_schemes = {
        "green": {
            "#191919": ["#2b2b2b", "#0e4429", "#006d32", "#26a641", "#39d353"],
            "#ffffff": ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
        },
        "yellow": {
            "#191919": ["#2b2b2b", "#f9e79f", "#f7dc6f", "#f4d03f", "#f1c40f"],
            "#ffffff": ["#ebedf0", "#fff5b1", "#ffea7f", "#ffd33d", "#f9c513"]
        },
        "orange": {
            "#191919": ["#2b2b2b", "#f5cba7", "#f0b27a", "#eb984e", "#e67e22"],
            "#ffffff": ["#ebedf0", "#ffd6b5", "#ffab70", "#fb8532", "#e36209"]
        },
        "blue": {
            "#191919": ["#2b2b2b", "#aed6f1", "#5dade2", "#2e86c1", "#1b4f72"],
            "#ffffff": ["#ebedf0", "#c6dbf7", "#96c8f3", "#6ca8f0", "#2188ff"]
        },
        "purple": {
            "#191919": ["#2b2b2b", "#d2b4de", "#af7ac5", "#884ea0", "#512e5f"],
            "#ffffff": ["#ebedf0", "#e6ccf2", "#d1a9f0", "#b084f5", "#8a63d2"]
        },
        "pink": {
            "#191919": ["#2b2b2b", "#f5b7b1", "#f1948a", "#ec7063", "#c0392b"],
            "#ffffff": ["#ebedf0", "#ffc2c0", "#ff8a8a", "#ff5a5f", "#d73a49"]
        },
        "red": {
            "#191919": ["#2b2b2b", "#f1948a", "#e74c3c", "#c0392b", "#922b21"],
            "#ffffff": ["#ebedf0", "#fdaeb7", "#f97583", "#ea4a3c", "#d73a49"]
        }
    }

    colors = color_schemes[color_scheme][background_color]

    if count == 0:
        return colors[0]
    elif 0 < count <= max_count / 5:
        return colors[1]
    elif max_count / 5 < count <= max_count * 2 / 5:
        return colors[2]
    elif max_count * 2 / 5 < count <= max_count * 3 / 5:
        return colors[3]
    elif max_count * 3 / 5 < count <= max_count * 4 / 5:
        return colors[4]
    elif max_count * 4 / 5 < count <= max_count:
        return colors[4]

@app.route('/')
@limiter.limit("10 per minute") 
def index():
    username = request.args.get('username', 'default-username')
    if not re.fullmatch(r'^[a-zA-Z0-9-]{1,39}$', username):
        return render_template('error.html', error_message="Invalid user name."), 400
    
    background_color = request.args.get('background_color', '#191919')  # default : #191919
    if background_color not in VALID_BACKGROUND_COLORS:
        return render_template('error.html', error_message="Invalid background color."), 400
    
    color_scheme = request.args.get('color_scheme', 'green')  # default : green    
    if color_scheme not in VALID_COLOR_SCHEMES:
        return render_template('error.html', error_message="Invalid color scheme."), 400
    
    size = request.args.get('size', 's')  # default : s
    if size not in VALID_SIZES:
        return render_template('error.html', error_message="Invalid size."), 400

    try:
        contributions, max_count = load_contributions(username)
    except Exception as e:
        return render_template('error.html', error_message="An error occurred while retrieving contribution data."), 500

    today = datetime.now()
    dow = (6 if today.weekday() == 6 else 5 - today.weekday())  # 曜日
    size = {'s': 49, 'm': 147, 'l': 343}[size]  # サイズ

    # カレンダー
    calendar_data = []
    for i in range(size - dow):
        day = today - timedelta(days=size - dow - i - 1)
        date_str = day.strftime("%Y-%m-%d")
        count = contributions.get(date_str, 0)
        calendar_data.append({
            "day": day.day,
            "color": get_color(count, max_count)
        })

    show_data = [[] for _ in range(len(calendar_data) // 7 + 1)]
    for i in range(len(calendar_data)):
        show_data[i // 7].append(calendar_data[i])

    return render_template('index.html', calendar=show_data, username=username, background_color=background_color)

# if __name__ == '__main__':
#     app.run(debug=False)