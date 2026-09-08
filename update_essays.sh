#!/bin/bash
# update_essays.sh
# エッセイ追加後に実行するスクリプト
# - 個別HTMLページを生成
# - sitemap.xml を更新
# - 英語翻訳サイトを更新

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [1/2] Essay ページ生成 & sitemap.xml 更新 ==="
python3 generate_essay_pages.py

echo ""
echo "=== [2/2] 英語翻訳サイト更新 ==="
python3 translate_site.py

echo ""
echo "完了！"
