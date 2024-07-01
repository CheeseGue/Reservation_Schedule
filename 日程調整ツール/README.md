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
日程調整ツール
├── README.md
├── app.py
├── app_2.py
├── app_py.md
├── credentials.json
├── install.sh
├── send_email.py
├── static
│   ├── css
│   │   └── styles.css
│   └── js
│       ├── calendar.js
│       └── confirm_reservation.js
├── templates
│   ├── base.html
│   ├── confirm_reservation.html
│   └── index.html
└── utils
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-311.pyc
    │   ├── calendar_service.cpython-311.pyc
    │   ├── gmail_service.cpython-311.pyc
    │   └── helpers.cpython-311.pyc
    ├── calendar_service.py
    ├── gmail_service.py
    └── helpers.py
```

このファイル構成を見て、各ファイルの役割は次の通りです：

README.md: プロジェクトの概要や設定方法などを記載するファイル。
app.py: メインのFlaskアプリケーションのエントリーポイント。
app_2.py: 追加のFlaskアプリケーションや機能。
app_py.md: app.pyに関するドキュメントファイル。
credentials.json: Google APIの認証情報が格納されたファイル。
install.sh: プロジェクトのインストールやセットアップに関するシェルスクリプト。
send_email.py: メール送信に関するスクリプト。
static ディレクトリは静的ファイルを格納する場所です：

static/css/styles.css: CSSスタイルシート。
static/js/calendar.js: カレンダー機能に関するJavaScriptファイル。
static/js/confirm_reservation.js: 予約確認機能に関するJavaScriptファイル。
templates ディレクトリはHTMLテンプレートを格納する場所です：

templates/base.html: 他のHTMLテンプレートで使用するベーステンプレート。
templates/confirm_reservation.html: 予約確認ページのHTMLテンプレート。
templates/index.html: ホームページのHTMLテンプレート。
utils ディレクトリはユーティリティ関数を格納する場所です：

utils/__init__.py: パッケージとして認識させるための空ファイル。
utils/calendar_service.py: Googleカレンダー関連のサービスを提供するモジュール。
utils/gmail_service.py: Gmail関連のサービスを提供するモジュール。
utils/helpers.py: その他の補助的な関数を提供するモジュール。
__pycache__ フォルダはPythonによって自動生成されたキャッシュファイルを格納します。

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