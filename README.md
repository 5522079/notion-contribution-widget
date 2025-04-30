# Contribution Graph Widget for Notion

![img_top](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3828517%2Fa61704d4-8dce-dafe-5296-4504242bfaab.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=67a95e2de5e99ea43087a95f6f590bed)

## 概要

このプログラムはGitHubのコントリビューショングラフをNotion上で確認できるウィジェットを提供します。

## 使用技術
<p style="display: inline">
    <img src="https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat">
    <img src="https://img.shields.io/badge/-CSS3-1572B6.svg?logo=css3&style=flat">
    <img src="https://img.shields.io/badge/-HTML5-333.svg?logo=html5&style=flat">
    <img src="https://img.shields.io/badge/-Github-181717.svg?logo=github&style=popout">
    <img src="https://img.shields.io/badge/GraphQL-ff379b?style=flat&logo=graphql">
    <img src="https://img.shields.io/badge/-Azure-2560E0.svg?logo=azure-pipelines&style=popout">
    <img src="https://img.shields.io/badge/Azure%20Web%20App-blue?style=flat">
</p>

## 動作環境
| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.12       |
| flask                 | 3.1.0      |
| requests              | 2.24.0     |

その他のパッケージのバージョンは [requirements.txt](./requirements.txtrequirements.txt) を参照してください。

## 使い方
1. アプリケーションのURLにアクセス
    
    以下のURLにアクセスします。<br>
    https://notion-contribution-widget.azurewebsites.net/

2. GitHubユーザー名を指定
    
    URLのクエリパラメータにusernameを指定して、自分のGitHubアカウント名を入力します。<br>
    例：https://notion-contribution-widget.azurewebsites.net/?username=your_github_username

3. Notionに埋め込む

    Notionのページに移動し、「埋め込み」ブロックを追加します。アプリケーションのURLを入力して埋め込みます。
    
    ![img_embed](https://github.com/user-attachments/assets/c0d1757f-f20c-42b3-ab1e-af8a72b66255)

4. カスタマイズする
   
   `background_color`や`color_shceme`などを指定することで自分好みにカスタマイズすることができます。詳しくはNotionの[デモページ](https://www.notion.so/DemoPage-1814e6035cdd8060b088d3d8c19ffc95?pvs=4)をご覧ください。
   ![img_custom](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3828517%2F81c6ab70-c74b-4194-81b1-f07904391843.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=8bf070bbec7d4f5a01d0e46757f94e5e)