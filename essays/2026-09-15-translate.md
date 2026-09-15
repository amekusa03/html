# 英語サイトの自動変換を、本気で仕上げる

2026-09-15 / Python / DeepL / 開発

## 「とりあえず作った」から1ヶ月

先月、思いつき半分で始めた個人サイトの英語化。当時は「とりあえず動けばいい」と簡易なスクリプトを書いて公開したものの、記事を新しく書くたびに細かな課題が積み重なっていた。

特にストレスだったのが、無料翻訳エンドポイントの**レートリミット（IP制限）**だ。記事が長くなるとアクセス制限に引っかかり、段落ごとに指数関数的なリトライ待機（2秒、4秒、8秒……）が発生して、ビルドに数分以上待たされるようになっていた。

おまけに、JSON-LD（構造化データ）の `inLanguage` が `ja` のまま残っていたり、サイト名の「雨草の庭」が「Rainweed Garden（雨の雑草の庭？）」と直訳されてキャッシュに居座り続けたりと、見過ごせないアラが目立ってきた。

そこで今回、翻訳パイプラインを本格的に改修することにした。

## DeepL API の導入と圧倒的な速度

一番の改善は、翻訳エンジンを **DeepL API**（無料プランで月50万文字）に切り替えたことだ。

APIキーを読み込む仕組みを作り、キャッシュ（`translation_cache.json`）と組み合わせたところ、更新処理が劇的に変化した。これまで数分かかっていた新規記事の英語化が、わずか十数秒で一気に駆け抜けるようになった。

何より訳文の質が段違いに自然だ。主語の補完や技術用語の文脈理解がスムーズで、機械翻訳特有のぎこちなさが大幅に減った。

## HTML構造とメタデータを守る工夫

単にテキストを翻訳するだけなら簡単だが、実際のWebページには壊してはいけない要素が無数にある。

- **コードブロックの保護**: `<pre><code>` やインラインコード内のプログラムコード、シェルコマンドが翻訳で崩れないよう、プレースホルダーで退避してから復元する。
- **JSON-LD と OGP の最適化**: `og:locale` を `en_US` に書き換え、構造化データ内の `inLanguage` を `en` に、記事URLや著者URLを `/en/` 配下に自動変換する。
- **辞書とキャッシュのクレンジング**: 過去のGoogle翻訳で「Rainweed Garden」や「Amegusa no Niwa」としてキャッシュされていた約380件のデータを一括で置換し、サイト全体のブランド表記を「Amekusa's Garden」に統一した。

```python
# JSON-LD構造化データを再帰的に英語化・URL変換
def translate_json_ld(obj, current_rel_path=""):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if k == 'inLanguage':
                new_obj[k] = 'en'
            elif k in ['url', '@id', 'image', 'logo'] and isinstance(v, str):
                new_obj[k] = fix_url_for_en(v, current_rel_path)
            elif isinstance(v, str) and has_japanese(v):
                new_obj[k] = translate_text(v)
            else:
                new_obj[k] = translate_json_ld(v, current_rel_path)
        return new_obj
    ...
```

## ワンコマンドで世界へ

これで、運用フローは極めてシンプルになった。

日本語で新しい Markdown 記事を書いて `./update_essays.sh` を一度叩くだけ。

1. 日本語版 HTML の生成
2. DeepL による英語版 HTML / Markdown の自動生成
3. サイトマップ（`sitemap.xml`）の自動更新

これらすべてが十数秒で完了し、Git にコミットしてプッシュすれば世界中に配信される（もちろん API キーは `.gitignore` で安全に守られている）。

最初は「誰が見るわけでもない」と思って始めた英語対応だったが、パイプラインが綺麗に整ってワンクリックで2言語が同時に同期される様子を眺めていると、それだけでエンジニアとして心地よい満足感がある。
