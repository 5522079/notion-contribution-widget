from flask import Flask, render_template
from datetime import datetime, timedelta


app = Flask(__name__)

file_path = "./data/contributions.csv"

def load_csv(file_path):
    contributions = {}
    with open(file_path) as csv:
        for line in csv:
            date, count = line.strip().split(',')
            contributions[date] = int(count)
    max_count = max(contributions.values())
    return contributions, max_count

def get_color(count):
    _, max_count = load_csv(file_path)
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
    today = datetime.now()
    dow = (6 if today.weekday() == 6 else 5 - today.weekday()) # 曜日
    size = 49 # サイズ設定（7の倍数）
    contributions, _ = load_csv(file_path)
    
    # カレンダー
    calendar_data = []
    for i in range(size - dow):
        day = today - timedelta(days=size - dow - i - 1)
        date_str = day.strftime("%Y-%m-%d")
        count = contributions.get(date_str, 0)
        calendar_data.append({"day": day.day, "color": get_color(count)})

    show_data = [[] for _ in range(len(calendar_data) // 7 + 1)]
    for i in range(len(calendar_data)):
        show_data[i // 7].append(calendar_data[i])

    return render_template('index.html',calendar=show_data)

if __name__ == '__main__':
    app.run(debug=True)