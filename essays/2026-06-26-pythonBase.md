# Python GUIファイラーの雛形を作った

2026.06.26 ・ Python / PySide6

---

## 動機

PySide6でGUIアプリを書くとき、ファイルシステムの操作とUI描画がいつの間にか混ざり合っていく。どこで読んでどこで表示するのか、境界が曖昧になると、ちょっとした機能追加のたびにあちこちを直す羽目になる。

何度か同じ失敗を繰り返したので、きちんと整理したベースクラスを作ることにした。

---

## 構成

役割を3層に分けた。GUIとロジックが疎結合になれば、テストも拡張もしやすくなる。

**Model — `BaseNodeObject.py`**
ファイル・ディレクトリをオブジェクトとして表現。アイコン、タイプ名、サイズ表示などUI向けの情報をここに閉じ込めた。

**Repository — `FilerRepository.py`**
ファイルシステムへの読み書きをすべてここに集約。GUI層から標準モジュールを直接触らせない。

**UI — `main.py`**
PySide6製のデスクトップGUI。サイドバー、ソート可能なテーブル、コンテキストメニュー、詳細パネルを実装済み。テーマはTokyo Night。

---

## 使い道

このベースクラスがあれば、画像ビューア、音楽ライブラリ管理、クラウド同期ファイラーなど、ファイルを扱うアプリを一から書き直さずに済む。サンプルとして動くGUIアプリも同梱したので、動作確認しながら好きなように拡張できる。

---

## プロジェクト構成

```
PythonBaseClasses/
├── BaseNodeObject.py    # データモデル
├── FilerRepository.py   # リポジトリ
├── main.py              # GUIアプリ
└── README.md
```

---

## 動かすまで

1. 仮想環境を作る
   ```bash
   python3 -m venv venv
   ```

2. 依存関係を入れる
   ```bash
   ./venv/bin/pip install PySide6
   ```

3. 起動
   ```bash
   ./venv/bin/python main.py
   ```

---

ソース: [github.com/amekusa03/PythonBaseClasses](https://github.com/amekusa03/PythonBaseClasses)