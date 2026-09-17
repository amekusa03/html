# 気象庁の裏側JSONで、常駐型気象・地震モニターを作る

2026-09-18 / Python / PySide6 / Qt

## 経緯

作業中、ふと天気の変化や雨雲の接近が気になるときがある。しかし、そのためだけにブラウザを開いて気象庁のサイトを見に行くのは地味に煩わしい。

知っている人も多いかもしれないが、気象庁の公式Webサイト（jma.go.jp）は、フロントエンドが裏側で軽量なJSONエンドポイントを直接叩いてデータを取得している。余計なHTMLスクレイピングをしなくても、公式の一次データがそのままJSONで手に入る。

それなら、システムトレイに静かに常駐し、普段は邪魔にならず、警報や地震が発生したときだけサッと通知してくれる自分専用のモニターを作ろうと思い立った。

## 気象庁の内部JSONエンドポイント

気象庁のシステムは合理的で、以下のエンドポイントから即座にデータを取得できる。

- **エリア定義マスター**: `https://www.jma.go.jp/bosai/common/const/area.json`
- **天気予報（3日/7日）**: `https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json`
- **警報・注意報・特別警報**: `https://www.jma.go.jp/bosai/warning/data/warning/{area_code}.json`
- **リアルタイム地震速報**: `https://www.jma.go.jp/bosai/quake/data/list.json`

APIキー不要、レスポンスも非常に速い。

## 実装

UIフレームワークには **PySide6 (Qt for Python)** を採用した。

ウィンドウを閉じてもバックグラウンドで監視を継続し、大雨・暴風などの警報発表時や新規地震発生時にOSのデスクトップ通知を自動発信するようにした。

国内外を問わず使えるよう、日本語と英語をワンクリックで切り替え可能にした。UIだけでなく、「大雨警報 ↔ Heavy Rain Warning」や震度表記も辞書定義で自動変換する。気象庁から届いたJSONペイロードをリアルタイムに確認・コピーできるデバッグビューも搭載し、長時間の作業でも目に優しいダークスタイル（QSS）を適用した。

## GitHubへの公開

せっかく形になったので、英語ドキュメントをメインに整えてGitHubに公開した。GitHub CLI (`gh`) を使えば、リポジトリの初期化から公開、トピックタグの設定まで一瞬で完了する。

```bash
gh repo create JapanMonitor --public --source=. --remote=origin \
  --description "Real-time Japan Meteorological Agency (JMA) weather forecast, emergency warning & earthquake monitor desktop app built with PySide6 (Qt)" \
  --push
```

PCログイン時に自動常駐させておくと、作業の邪魔を一切せず、必要なときだけ確実な情報を教えてくれる頼もしい相棒になった。

## ソース

- [JapanMonitor (GitHub)](https://github.com/amekusa03/JapanMonitor)
