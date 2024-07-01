# Reservation System

## Setup

1. Clone the repository.
2. Install the required packages using `pip install flask`.
3. Run the application using `python app.py`.

## Directory Structure

- `app.py`: The main Flask application.
- `templates/`: Contains HTML templates.
- `static/`: Contains static files such as CSS and JavaScript.
- `README.md`: This file.


以下に、日本語で詳細に記述されたREADMEファイルを示します。

```markdown
# 予約システム

## 概要

このプロジェクトは、ユーザーが空き時間を確認して予約を行うためのシステムです。カレンダー形式で空き時間を表示し、ユーザーが希望の時間帯を選択して予約を確定できます。

## セットアップ手順

### 1. リポジトリをクローンする

まず、リポジトリをクローンします。

```bash
git clone <リポジトリのURL>
cd reservation-system
```

### 2. 必要なパッケージをインストールする

必要なPythonパッケージをインストールします。このプロジェクトではFlaskを使用しています。

```bash
pip install flask
```

### 3. アプリケーションを実行する

アプリケーションを実行します。

```bash
python app.py
```

ブラウザで `http://127.0.0.1:5000` にアクセスすると、予約システムが表示されます。

## ディレクトリ構成

```
reservation-system/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── confirm_reservation.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── calendar.js
|   |   └── confirm_reservation.js
└── README.md
```

- `app.py`: Flaskアプリケーションのメインファイル。
- `templates/`: HTMLテンプレートが含まれています。
  - `base.html`: 基本テンプレート。
  - `index.html`: 予約システムのカレンダー表示ページ。
  - `confirm_reservation.html`: 予約確認ページ。
- `static/`: 静的ファイルが含まれています。
  - `css/`: CSSファイル。
    - `styles.css`: スタイルシート。
  - `js/`: JavaScriptファイル。
    - `calendar.js`: カレンダーの表示と操作を行うスクリプト。
- `README.md`: このファイル。

## 機能の説明

### カレンダー表示

- 現在の週の日付と曜日を表示します。
- 各時間帯の空き状況を表示します。
  - 空き: 緑色
  - 予約済み: 赤色
- 時間帯をクリックすると、その時間帯が選択されます（緑色から青色に変わります）。

### 予約確認

- 選択された時間帯を確認します。
- 「予約確認をする」ボタンをクリックすると、予約確認ページに遷移します。
- 予約確認ページで詳細を確認し、「予約を確定する」ボタンをクリックすると、予約が確定され、確認メールが送信されます。

## メール送信機能

- `send_reservation`エンドポイントが予約情報を受け取り、メールで送信します。
- SMTPサーバーの設定が必要です。
  - `your_email@example.com`: 送信元のメールアドレス。
  - `recipient@example.com`: 送信先のメールアドレス。
  - `smtp.example.com`: SMTPサーバー。
  - `your_password`: 送信元メールアドレスのパスワード。

SMTPサーバーの設定を適宜変更してください。

## 注意点

- 本プロジェクトはローカル環境での動作を想定しています。デプロイ時には、適切なセキュリティ対策を講じてください。
- メール送信機能を利用するためには、正しいSMTPサーバーの設定が必要です。

以上が予約システムのセットアップ手順と機能の詳細です。質問や問題がある場合は、適宜サポートを求めてください。
```

このREADMEファイルに従うことで、プロジェクトのセットアップと使用方法を理解しやすくなります。また、各ファイルの役割や機能についても詳細に記載しているため、プロジェクトのメンテナンスや拡張も容易になるでしょう。