import os
import re
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request


app = Flask(__name__)

load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def load_contributions(username):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
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

def get_color(count, max_count):
    if count == 0:
        return "#2b2b2b"
    elif 0 < count <= max_count / 4:
        return "#0e4429"
    elif max_count / 4 < count <= max_count / 2:
        return "#006d32"
    elif max_count / 2 < count <= max_count * 3 / 4:
        return "#26a641"
    elif max_count * 3 / 4 < count <= max_count:
        return "#39d353"

@app.route('/')
def index():
    username = request.args.get('username', 'default-username')
    if not re.match(r'^[a-zA-Z0-9-]{1,39}$', username): # ユーザ名のバリデーション
        return render_template('error.html', error_message="Invalid user name."), 400

    try:
        contributions, max_count = load_contributions(username)
    except Exception as e:
        return render_template('error.html', error_message="An error occurred while retrieving contribution data."), 500
    
    today = datetime.now()
    dow = (6 if today.weekday() == 6 else 5 - today.weekday()) # 曜日
    size = 49 # サイズ設定（7の倍数）

    # カレンダー
    calendar_data = []
    for i in range(size - dow):
        day = today - timedelta(days=size - dow - i - 1)
        date_str = day.strftime("%Y-%m-%d")
        count = contributions.get(date_str, 0)
        calendar_data.append({"day": day.day, "color": get_color(count, max_count)})

    show_data = [[] for _ in range(len(calendar_data) // 7 + 1)]
    for i in range(len(calendar_data)):
        show_data[i // 7].append(calendar_data[i])

    return render_template('index.html', calendar=show_data, username=username)

if __name__ == '__main__':
    app.run(debug=True)