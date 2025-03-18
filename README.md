# Contribution Graph Widget for Notion

![img_1](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3828517%2Fa61704d4-8dce-dafe-5296-4504242bfaab.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=67a95e2de5e99ea43087a95f6f590bed)

## 概要

このプログラムはGitHubのコントリビューショングラフをNotion上で確認できるウィジェットを提供します。

## 使用技術
<p style="display: inline">
    <img src="https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat">
    <img src="https://img.shields.io/badge/-CSS3-1572B6.svg?logo=css3&style=flat">
    <img src="https://img.shields.io/badge/-HTML5-333.svg?logo=html5&style=flat">
    <img src="https://img.shields.io/badge/-Github%20Actions-181717.svg?logo=github&style=popout">
    <img src="https://img.shields.io/badge/-Azure%20Web%20Apps-0078D7.svg?logo=azure&style=popout">
</p>

## 動作環境
| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.12       |
| flask                 | 3.1.0      |
| beautifulsoup4        | 4.12.3     |
| requests              | 2.24.0     |

その他のパッケージのバージョンは requirements.txt を参照してください。

## ディレクトリ構成
```txt
./
├─ .github/
│   ├─ main_notion-contribution-widget.yml
│   └─ scrape.yml
├─ data/
│   └─ contributions.csv
├─ static/
│   └─ style.css
├─ templates/
│   └─ index.html
├─ .env
├─ .gitignore
├─ app.py
├─ robot.py
├─ requirements.txt
└─ README.md
```

## インストール
```bash
# リポジトリをクローン
git clone https://github.com/5522079/notion-contribution-widget.git

# ディレクトリに移動
cd notion-contribution-widget

# 仮想環境の作成
python -m venv .venv
.venv\Scripts\activate # Windows

# ライブラリのインストール
pip install -r requirements.txt
```

## 使い方
`.env`ファイルを作成し、GitHubユーザーネームを設定します。
```env
GITHUB_USER_NAME=your_github_user_name
```

以下のコマンドを実行します。
```bash
python app.py
```
http://127.0.0.1:8000 にアクセスできたら成功です。