#!/usr/bin/env python3
"""
generate_essay_pages.py
エッセイのMarkdownファイルから個別HTMLページを生成し、
sitemap.xmlにエッセイURLを追加するスクリプト

Usage: python3 generate_essay_pages.py
"""

import re
import os
import json
from datetime import datetime, date

BASE_URL = "https://amekusa.vercel.app"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ESSAYS_DIR = os.path.join(BASE_DIR, "essays")
INDEX_HTML = os.path.join(BASE_DIR, "index.html")
SITEMAP_XML = os.path.join(BASE_DIR, "sitemap.xml")

# index.htmlからESSAYS配列を解析
def parse_essays_from_index():
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    # ESSAYS配列の各エントリを抽出
    pattern = r'\{\s*slug:\s*"([^"]+)",\s*date:\s*"([^"]+)",\s*title:\s*"([^"]+)",\s*categories:\s*\[([^\]]*)\]\s*\}'
    matches = re.findall(pattern, content)

    essays = []
    for slug, date_str, title, cats_str in matches:
        cats = re.findall(r'"([^"]+)"', cats_str)
        essays.append({
            'slug': slug,
            'date': date_str,
            'title': title,
            'categories': cats
        })
    return essays

# 個別HTMLページのテンプレートを生成
def generate_essay_html(essay):
    slug = essay['slug']
    title = essay['title']
    date_str = essay['date']
    categories = essay['categories']

    # 日付をISO形式に変換 (2026.08.12 -> 2026-08-12)
    iso_date = date_str.replace('.', '-')

    # OGP画像の候補（記事専用pngがあれば使用）
    essay_png = os.path.join(ESSAYS_DIR, f"{slug}.png")
    if os.path.exists(essay_png):
        ogp_image = f"{BASE_URL}/essays/{slug}.png"
    else:
        ogp_image = f"{BASE_URL}/ogp.png"

    cats_label = "・".join(categories) if categories else "その他"
    description = f"{title} — {cats_label}。雨草の庭 技術随筆。"

    html = f'''<!DOCTYPE html>
<html lang="ja">

<head>
  <script>
    window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
  </script>
  <script defer src="/_vercel/insights/script.js"></script>

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-SRGF2MMYGD"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {{ dataLayer.push(arguments); }}
    gtag('js', new Date());
    gtag('config', 'G-SRGF2MMYGD');
  </script>

  <link rel="icon" href="../Favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="../amenoniwa.png">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="canonical" href="{BASE_URL}/essays/{slug}">
  <meta name="author" content="雨草 (Amekusa)">
  <meta name="description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{BASE_URL}/essays/{slug}">
  <meta property="og:title" content="{title} | 雨草の庭">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{ogp_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="雨草の庭">
  <meta property="article:published_time" content="{iso_date}">
  <meta property="article:author" content="雨草 (Amekusa)">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | 雨草の庭">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{ogp_image}">
  <title>{title} | 雨草の庭</title>

  <!-- JSON-LD 構造化データ -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "@id": "{BASE_URL}/essays/{slug}",
    "url": "{BASE_URL}/essays/{slug}",
    "headline": "{title}",
    "description": "{description}",
    "datePublished": "{iso_date}",
    "dateModified": "{iso_date}",
    "inLanguage": "ja",
    "author": {{
      "@type": "Person",
      "@id": "{BASE_URL}/#person",
      "name": "雨草 (Amekusa)",
      "url": "{BASE_URL}/"
    }},
    "publisher": {{
      "@type": "Person",
      "@id": "{BASE_URL}/#person",
      "name": "雨草 (Amekusa)"
    }},
    "isPartOf": {{
      "@type": "Blog",
      "@id": "{BASE_URL}/#blog",
      "name": "Notes — 雨草の庭"
    }},
    "image": {{
      "@type": "ImageObject",
      "url": "{ogp_image}"
    }}
  }}
  </script>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500&family=Noto+Serif+JP:wght@300;400;600&display=swap" rel="stylesheet">

  <!-- Markdown Parser -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

  <link rel="stylesheet" href="../style.css">
</head>

<body>
  <canvas id="rain-canvas"></canvas>

  <div class="container">
    <div class="sidebar">
      <header>
        <a href="../"><img src="../amenoniwa.png" alt="Character animation" class="hero-gif"></a>
        <h1>雨草の庭</h1>
        <p class="subtitle">Engineering &amp; Nature Notes</p>
      </header>

      <nav class="global-nav">
        <a href="../#notes" class="nav-item active">Notes</a>
        <a href="../#photography" class="nav-item">Photography</a>
        <a href="../#profile" class="nav-item">Profile</a>
        <a href="../#links" class="nav-item">Links</a>
        <a href="../en/" class="nav-item">🌐 English</a>
      </nav>
    </div>

    <div class="main-content">
      <main id="essay-content">
        <div class="loading">読み込み中...</div>
      </main>
    </div>
  </div>

  <script src="../rain.js"></script>
  <script>
    // Markdownを読み込んで表示
    async function loadEssay() {{
      const contentArea = document.getElementById('essay-content');
      try {{
        const response = await fetch('{slug}.md');
        if (!response.ok) throw new Error('File not found');
        const markdownText = await response.text();
        const parsedHtml = marked.parse(markdownText);

        contentArea.innerHTML = `
          <section class="essay-detail-section">
            <a href="../essays/" class="back-btn">← 一覧に戻る</a>
            <div class="essay-content">
              ${{parsedHtml}}
            </div>
          </section>
        `;
        // 画像パスを修正（essays/相対パスがある場合）
        contentArea.querySelectorAll('img').forEach(img => {{
          const src = img.getAttribute('src');
          if (src && src.startsWith('essays/')) {{
            img.setAttribute('src', '../' + src);
          }}
        }});
      }} catch (error) {{
        contentArea.innerHTML = `
          <div style="text-align: center; padding: 3rem 0;">
            <p style="font-size: 1.2rem; margin-bottom: 1.5rem;">記事が見つかりませんでした。</p>
            <a href="../essays/" class="back-btn" style="margin-bottom: 0;">← 一覧に戻る</a>
          </div>
        `;
      }}
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      loadEssay();
      if (typeof initRain === 'function') initRain();
    }});
  </script>
</body>

</html>'''
    return html

# sitemap.xmlを更新してエッセイURLを追加
def update_sitemap(essays):
    with open(SITEMAP_XML, 'r', encoding='utf-8') as f:
        sitemap_content = f.read()

    # 既存のエッセイURLエントリを削除（再生成するため）
    # essays/で始まるURLエントリを除去
    essay_url_pattern = r'\s*<url>\s*<loc>https://amekusa\.vercel\.app/essays/[^<]+</loc>.*?</url>'
    sitemap_content = re.sub(essay_url_pattern, '', sitemap_content, flags=re.DOTALL)

    # 新しいエッセイURLエントリを生成
    today = date.today().isoformat()
    essay_entries = []
    for essay in essays:
        slug = essay['slug']
        iso_date = essay['date'].replace('.', '-')
        # .mdファイルの実際の更新日を取得
        md_path = os.path.join(ESSAYS_DIR, f"{slug}.md")
        if os.path.exists(md_path):
            mtime = os.path.getmtime(md_path)
            lastmod = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        else:
            lastmod = iso_date

        entry = f'''  <url>
    <loc>{BASE_URL}/essays/{slug}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>'''
        essay_entries.append(entry)

    # </urlset>の直前に挿入
    insert_block = "\n" + "\n".join(essay_entries) + "\n"
    sitemap_content = sitemap_content.replace('</urlset>', insert_block + '</urlset>')

    with open(SITEMAP_XML, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)

    return len(essay_entries)

def main():
    print("=== Essay SEO Page Generator ===")

    # ESSAYSデータを読み込み
    essays = parse_essays_from_index()
    print(f"Found {len(essays)} essays in index.html")

    # 個別HTMLファイルを生成
    generated = 0
    skipped_no_md = 0
    for essay in essays:
        slug = essay['slug']
        md_path = os.path.join(ESSAYS_DIR, f"{slug}.md")
        html_path = os.path.join(ESSAYS_DIR, f"{slug}.html")

        # .mdが存在する場合のみHTML生成
        if not os.path.exists(md_path):
            skipped_no_md += 1
            continue

        html_content = generate_essay_html(essay)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        generated += 1

    print(f"Generated: {generated} HTML files")
    print(f"Skipped (no .md): {skipped_no_md}")

    # sitemapを更新（.mdがある記事のみ）
    md_essays = [e for e in essays if os.path.exists(os.path.join(ESSAYS_DIR, f"{e['slug']}.md"))]
    n = update_sitemap(md_essays)
    print(f"Updated sitemap.xml with {n} essay URLs")

    print("\nDone!")

if __name__ == "__main__":
    main()
