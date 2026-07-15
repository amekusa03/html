# メールでGemini

2026/04/16 Google Apps Script

メールで環境はあるけど、ブラウザーやスマホが使えない時に、
自分宛てにメールをすると、Geminiの応答をメールで返してくれるアプリ。

## How to Use

1. Google Cloud Platformでプロジェクトを作成し、Gemini APIを有効化する。 
2. APIキーを取得し、Google Apps Scriptのプロジェクトに設定する。 
3. Google Apps Scriptでメール受信トリガーを設定し、特定の件名や内容のメールを受信した際にGemini APIを呼び出すスクリプトを作成する。 
4. スクリプトがGemini APIからの応答を処理し、適切な返信メールを送信するように実装する。 
5. テストメールを送信して、システムが正しく動作することを確認する。

## Resource

設定を誤ると**Google Cloud Platformから料金 **が発生する場合があり。 

[View on GitHub](https://github.com/amekusa03/AskGeminibyemail)
