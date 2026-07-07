# 音楽管理機能付きのGUIファイラーを作った

2026.06.28 ・ Python / PySide6

---

## 動機

前回の「Python GUIファイラーの雛形」をベースにして、音楽ライブラリの自動整理・管理機能を兼ね備えたハイブリッドなファイルマネージャーアプリケーション「PythonpicMusic」を作成した。

通常のファイルシステムによる階層ブラウズだけでなく、大量のメディアファイルを再帰スキャンしてメタデータ基準でフラットに一覧表示し、さらにタグ編集に連動してフォルダ構造を自動整理する仕組みを目指した。

---

## 構成

役割を明確に分け、GUIとロジックを疎結合に保つ設計を踏襲している。

**Model — `BaseNodeObject.py`**
ファイル・画像・MP3オブジェクトのデータモデル定義。PySide6の `QObject` に依存しないピュアPython実装にすることで、別スレッドからのスキャン・読込処理時のメモリ・スレッド衝突（コアダンプ）を完全に防止した。Qtシグナル・スロットと同等の書き方を維持する `PythonSignal` を内製して補っている。

**Repository — `FilerRepository.py` & `MusicFilerRepository.py`**
ファイル操作やスキャン処理をカプセル化。ベースとなる `FilerRepository` で基本CRUD操作（非再帰読み込み等）を担い、それを継承した `MusicFilerRepository` でメディア再帰スキャン、ID3タグ解析、自動クリーンアップといった本アプリ特有の音楽ドメインロジックを実装している。

**UI — `main.py`**
階層表示の通常モードと、再帰的にメディアを一覧表示するフラット表示（ライブラリビュー）を切り替え可能なデスクトップGUI。Tokyo Nightテーマを採用し、非同期スレッド処理により数千〜数万の音楽ファイルがあってもUIをフリーズさせずに読み込める。

---

## 主な機能

### 1. 階層表示モード（標準ファイラー）

- フォルダ階層のブラウズ。`os.scandir` による非再帰読み込みを採用しているため、巨大なフォルダも遅延なく瞬時に開く。

### 2. フラット表示モード（ライブラリビュー）

- 指定フォルダ配下のメディアファイルを再帰的に走査し、ID3メタデータ（アーティスト、アルバム、タイトル等）をグリッドに一覧表示。

### 3. ID3タグ編集とライブラリ自動整理

- MP3のタグ編集ダイアログ。

- タグの保存に連動し、`[ライブラリパス]/[アーティスト名]/[アルバム名]/[ファイル名]` へファイルを自動移動。空になった旧フォルダは自動で再帰クリーンアップ。

### 4. プレビュー機能

- 画像のサムネイルプレビュー、およびMP3に埋め込まれたカバーアートの自動パース・描画。

---

## プロジェクト構成

```bash
PythonpicMusic/
├── BaseNodeObject.py         # ピュアPythonによるデータモデル
├── FilerRepository.py        # 汎用リポジトリ
├── MusicFilerRepository.py   # 音楽専用リポジトリ
├── main.py                   # GUIアプリケーション
├── test_filer.py             # 自動テスト
└── README.md                 # 説明書
```

---

## 動かすまで

1. 仮想環境を作る

   ```bash
   python3 -m venv venv
   ```

2. 依存関係を入れる

   ```bash
   ./venv/bin/pip install PySide6 mutagen
   ```

3. 起動

   ```bash
   ./venv/bin/python main.py
   ```

4. テストの実行

   ```bash
   xvfb-run ./venv/bin/python test_filer.py
   ```

---

ソース: [github.com/amekusa03/PythonpicMusic](https://github.com/amekusa03/PythonpicMusic)
