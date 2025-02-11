# notion-contribution-widget

![img_1](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3828517%2Fa61704d4-8dce-dafe-5296-4504242bfaab.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=67a95e2de5e99ea43087a95f6f590bed)

## 概要
このプログラムはGitHubのコントリビューション状況をNotion上で確認できるツールです。

## 機能
### 1.  GitHubのコントリビューション数を取得
`robot.py`を実行し`user_name`で指定したGitHubユーザのコントリビューションデータをスクレイピングし、`./data/contributions.csv`に保存します。
### 2.  Webアプリケーションの構築
`app.py`を実行し`size`に7の倍数を指定することでコントリビューショングラブのサイズを変更することができます。
### 3.  Azure Web Appsでデプロイ
アプリケーションをAzureにデプロイするには`requirements.txt`と`app.py`をリポジトリのルートに配置します。Azureポータルから新しいWebアプリを作成し、GitHubリポジトリをデプロイ設定に指定します。
### 4.  GitHub Actionsによる自動更新
GitHub Actionsを使用して定期的にコントリビューションデータを更新します。
`.github/workflows/deploy.yaml`で、スケジュールを指定します。デフォルトで毎日0:00, 6:00, 12:00, 18:00 (JST)に更新するように設定されています。
### 5.  Notionへの埋め込み
デプロイしたアプリのURLをコピーし、NotionでURLを埋め込みます。

