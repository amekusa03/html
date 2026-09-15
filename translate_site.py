#!/usr/bin/env python3
import os
import re
import urllib.request
import urllib.error
import urllib.parse
import json
import time
from bs4 import BeautifulSoup, Comment

# Root directory of the repository
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = BASE_DIR
DEST_DIR = os.path.join(SRC_DIR, "en")

# DeepL API Key (Check env var first, then optional key file)
DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "").strip()
if not DEEPL_API_KEY:
    key_file = os.path.join(BASE_DIR, "deepl_api_key.txt")
    if os.path.exists(key_file):
        try:
            with open(key_file, "r", encoding="utf-8") as f:
                DEEPL_API_KEY = f.read().strip()
        except Exception:
            pass

if DEEPL_API_KEY:
    print(f"DeepL API configured ({'Free' if DEEPL_API_KEY.endswith(':fx') else 'Pro'} plan)")
else:
    print("No DeepL API key found. Using Google Translate (Free endpoint).")


# Pre-populated cache for critical UI terms to ensure top quality
translation_cache = {
    "雨草の庭": "Amekusa's Garden",
    "雨草の庭 技術エッセイ": "Amekusa's Garden Technical Essay",
    "雨草の庭 技術エッセイ・開発ログ": "Amekusa's Garden Technical Essays & Dev Logs",
    "随想 — 雨草の庭": "Notes — Amekusa's Garden",
    "開発 — 雨草の庭 技術エッセイ": "Development — Amekusa's Garden Technical Essay",
    "雨宿の庭": "Ameyado no Niwa - Engineering Portfolio",
    "雨草": "Amekusa",
    "訪問者数": "Visitor Count",
    "読み込み中...": "Loading...",
    "← 一覧に戻る": "← Back to List",
    "エッセイが見つかりませんでした。": "Essay not found.",
    "開発": "Development",
    "日常": "Daily Life",
    "車": "Car",
    "音楽": "Music",
    "その他": "Others",
    "← 庭に戻る": "← Back to Garden",
    "お気に入りリンク集へ →": "To Favorite Links →",
    "My Hobbiesへ →": "To My Hobbies →",
    "全ての写真を見る →": "View all photos →",
    "趣味": "Hobbies",
    "自動車": "Automobiles",
    "山登り": "Mountain Climbing",
    "書物": "Books",
    "しふとべる": "ShiftVet",
    "雨月": "Ugetsu",
    "過去の記事をもっと見る →": "See more past articles →",
    "該当する記事がありません。": "No matching articles found.",
    "記事一覧を見る →": "View Article List →"
}

def save_cache():
    cache_file = os.path.join(BASE_DIR, "translation_cache.json")
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(translation_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save translation cache: {e}")

def has_japanese(text):
    if not text:
        return False
    return bool(re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]', text))

def translate_with_deepl(text_stripped):
    if not DEEPL_API_KEY:
        return None
    try:
        endpoint = "https://api-free.deepl.com/v2/translate" if DEEPL_API_KEY.endswith(":fx") else "https://api.deepl.com/v2/translate"
        params = {
            "text": [text_stripped],
            "target_lang": "EN",
            "source_lang": "JA"
        }
        data = json.dumps(params).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers={
                "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            translations = res_data.get("translations", [])
            if translations and "text" in translations[0]:
                return translations[0]["text"]
    except Exception as e:
        print(f"DeepL API call failed: {e}")
    return None

def translate_text(text):
    if not text or not has_japanese(text):
        return text
    
    text_stripped = text.strip()
    if text_stripped in translation_cache:
        lead_ws = text[:len(text) - len(text.lstrip())]
        trail_ws = text[len(text.rstrip()):] if len(text.rstrip()) < len(text) else ""
        return lead_ws + translation_cache[text_stripped] + trail_ws

    # Try DeepL if key exists
    if DEEPL_API_KEY:
        print(f"Translating (DeepL): {text_stripped[:50]}")
        translated = translate_with_deepl(text_stripped)
        if translated:
            translation_cache[text_stripped] = translated
            save_cache()
            lead_ws = text[:len(text) - len(text.lstrip())]
            trail_ws = text[len(text.rstrip()):] if len(text.rstrip()) < len(text) else ""
            return lead_ws + translated + trail_ws

    max_retries = 5
    base_backoff = 2.0

    for attempt in range(max_retries):
        if attempt == 0:
            print(f"Translating: {text_stripped[:50]}")
        else:
            print(f"Retrying translation (attempt {attempt+1}/{max_retries}): {text_stripped[:50]}")

        # Method 1: GTX endpoint
        try:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q=" + urllib.parse.quote(text_stripped)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                translated = "".join([segment[0] for segment in data[0] if segment[0]])
                if translated:
                    translation_cache[text_stripped] = translated
                    save_cache()
                    time.sleep(0.2)
                    lead_ws = text[:len(text) - len(text.lstrip())]
                    trail_ws = text[len(text.rstrip()):] if len(text.rstrip()) < len(text) else ""
                    return lead_ws + translated + trail_ws
        except Exception:
            pass

        # Method 2: google.com/m web endpoint
        try:
            url = "https://translate.google.com/m?sl=ja&tl=en&q=" + urllib.parse.quote(text_stripped)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')
                container = soup.find('div', class_='result-container')
                if container and container.text.strip():
                    translated = container.text.strip()
                    translation_cache[text_stripped] = translated
                    save_cache()
                    time.sleep(0.2)
                    lead_ws = text[:len(text) - len(text.lstrip())]
                    trail_ws = text[len(text.rstrip()):] if len(text.rstrip()) < len(text) else ""
                    return lead_ws + translated + trail_ws
        except Exception:
            pass

        sleep_time = base_backoff * (2 ** attempt)
        print(f"Rate-limited on both methods. Waiting {sleep_time:.1f}s before retry (attempt {attempt+1}/{max_retries})...")
        time.sleep(sleep_time)

    print(f"Failed to translate '{text_stripped[:30]}' after {max_retries} attempts.")
    return text

def fix_url_for_en(url, current_rel_path=""):
    if not url:
        return url

    if url.startswith(('mailto:', 'tel:', 'javascript:', '#')):
        return url

    domain = "https://amekusa.vercel.app"
    if url.startswith(domain):
        path = url[len(domain):]
        if not any(path.startswith(ext) for ext in ['/ogp.png', '/Favicon.png', '/amenoniwa.png', '/_vercel']):
            if not path.startswith('/en/') and path != '/en':
                if path == '' or path == '/':
                    return f"{domain}/en/"
                else:
                    return f"{domain}/en{path}"
        return url

    if url.startswith(('http://', 'https://')):
        return url

    # Ignore asset files (images, stylesheets, js, etc.)
    url_without_query = url.split('?')[0].split('#')[0]
    if any(url_without_query.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.css', '.js']) or url.startswith('/_vercel'):
        return url

    # Separate hash fragment
    hash_fragment = ''
    if '#' in url:
        url_part, hash_fragment = url.split('#', 1)
        hash_fragment = '#' + hash_fragment
    else:
        url_part = url

    if not url_part and hash_fragment:
        return hash_fragment

    # Root-relative path
    if url_part.startswith('/'):
        if any(url_part.startswith(p) for p in ['/_vercel', '/Favicon.png', '/amenoniwa.png', '/ogp.png', '/css/', '/js/', '/en/']):
            return url
        if url_part == '/' or url_part == '/index.html':
            return '/en/' + hash_fragment
        return f"/en{url_part}" + hash_fragment

    # Relative path resolution against current_rel_path
    dir_name = os.path.dirname(current_rel_path) if current_rel_path else ""
    joined = os.path.normpath(os.path.join(dir_name, url_part))

    if joined in ['.', '', 'index.html']:
        target_root = '/en/'
    else:
        target_root = '/en/' + joined.lstrip('/')
        if url_part.endswith('/') and not target_root.endswith('/'):
            target_root += '/'

    return target_root + hash_fragment

JS_TOKEN_REGEX = re.compile(
    r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|'
    r'(?P<double>"(?:\\.|[^"\\\n])*")|'
    r"(?P<single>'(?:\\.|[^'\\\n])*')|"
    r'(?P<backtick>`(?:\\.|[^`\\])*`)',
    re.MULTILINE
)

def translate_js_strings(js_code, current_rel_path=""):
    def repl_token(match):
        kind = match.lastgroup
        raw_val = match.group(0)

        if kind == 'comment':
            return raw_val

        elif kind == 'double':
            content = raw_val[1:-1]
            if has_japanese(content):
                unescaped = content.replace('\\"', '"')
                translated = translate_text(unescaped)
                escaped = json.dumps(translated)[1:-1]
                return f'"{escaped}"'
            return raw_val

        elif kind == 'single':
            content = raw_val[1:-1]
            if has_japanese(content):
                unescaped = content.replace("\\'", "'")
                translated = translate_text(unescaped)
                escaped = json.dumps(translated)[1:-1].replace("'", "\\'")
                return f"'{escaped}'"
            return raw_val

        elif kind == 'backtick':
            content = raw_val[1:-1]
            if has_japanese(content):
                placeholders = {}
                idx = 0
                def repl_placeholder(m):
                    nonlocal idx
                    ph = f"__JS_PH_{idx}__"
                    placeholders[ph] = m.group(0)
                    idx += 1
                    return ph
                temp_content = re.sub(r'\$\{[^}]+\}', repl_placeholder, content)
                translated = translate_text(temp_content)
                for ph, original in placeholders.items():
                    translated = translated.replace(ph, original)
                escaped = json.dumps(translated)[1:-1].replace('`', '\\`')
                return f"`{escaped}`"
            return raw_val

        return raw_val

    return JS_TOKEN_REGEX.sub(repl_token, js_code)

def translate_json_ld(obj, current_rel_path=""):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if k == 'inLanguage':
                new_obj[k] = 'en'
            elif k in ['url', '@id', 'image', 'logo'] and isinstance(v, str):
                new_obj[k] = fix_url_for_en(v, current_rel_path)
            elif isinstance(v, str):
                if has_japanese(v):
                    new_obj[k] = translate_text(v)
                else:
                    new_obj[k] = v
            else:
                new_obj[k] = translate_json_ld(v, current_rel_path)
        return new_obj
    elif isinstance(obj, list):
        return [translate_json_ld(item, current_rel_path) for item in obj]
    return obj

def translate_html_content(html_content, current_rel_path=""):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    html_tag = soup.find('html')
    if html_tag and html_tag.has_attr('lang'):
        html_tag['lang'] = 'en'
    
    # Fix canonical & alternate link URLs
    for link in soup.find_all('link'):
        if link.has_attr('href'):
            href = link['href']
            rel = link.get('rel', [])
            if isinstance(rel, str):
                rel = [rel]
            if 'canonical' in rel:
                link['href'] = fix_url_for_en(href, current_rel_path)

    # Fix meta tags (og:url, twitter:url, etc.)
    for meta in soup.find_all('meta'):
        if meta.has_attr('property') and meta['property'] in ['og:url', 'twitter:url']:
            if meta.has_attr('content'):
                meta['content'] = fix_url_for_en(meta['content'], current_rel_path)
        if meta.has_attr('property') and meta['property'] == 'og:locale':
            meta['content'] = 'en_US'

    # Language switcher button fix
    for a in soup.find_all('a'):
        href = a.get('href', '')
        text = a.get_text().strip()
        is_switcher = (
            href in ['en', 'en/', 'en/index.html', '/en', '/en/', '/en/index.html'] or
            href.startswith(('en/', '../en/', '/en/')) or
            text in ['🌐 English', 'English'] or
            ('English' in text and 'nav-item' in a.get('class', []))
        )
        if is_switcher:
            if current_rel_path in ['', 'index.html']:
                ja_url = '/'
            elif current_rel_path.endswith('/index.html'):
                ja_url = '/' + current_rel_path[:-len('index.html')]
            else:
                ja_url = '/' + current_rel_path
            a['href'] = ja_url
            a.string = '🌐 日本語'
            a['data-lang-switched'] = 'true'

    # Process and translate JSON-LD scripts
    for script in soup.find_all('script', type='application/ld+json'):
        if script.string:
            try:
                data = json.loads(script.string)
                translated_data = translate_json_ld(data, current_rel_path)
                script.string = "\n" + json.dumps(translated_data, ensure_ascii=False, indent=2) + "\n"
                script['data-jsonld-processed'] = 'true'
            except Exception as e:
                print(f"JSON-LD parse error in {current_rel_path}: {e}")

    # General a[href] link fix
    for a in soup.find_all('a'):
        if a.has_attr('data-lang-switched'):
            del a['data-lang-switched']
            continue
        if a.has_attr('href'):
            a['href'] = fix_url_for_en(a['href'], current_rel_path)

    # Translate text nodes and script blocks
    for text_node in soup.find_all(string=True):
        if isinstance(text_node, Comment):
            continue
        parent = text_node.parent
        if parent and parent.name == 'style':
            continue
        # Skip translation inside pre, code, kbd, samp tags
        if any(p.name in ['pre', 'code', 'kbd', 'samp'] for p in text_node.parents):
            continue
        if parent and parent.name == 'script':
            if parent.has_attr('data-jsonld-processed'):
                continue
            new_js = translate_js_strings(text_node, current_rel_path)
            text_node.replace_with(new_js)
            continue
        
        if has_japanese(text_node):
            translated = translate_text(text_node)
            text_node.replace_with(translated)
            
    # Translate attributes
    for tag in soup.find_all(True):
        if tag.has_attr('data-jsonld-processed'):
            del tag['data-jsonld-processed']
        for attr in ['alt', 'placeholder', 'title', 'content']:
            if tag.has_attr(attr) and has_japanese(tag[attr]):
                tag[attr] = translate_text(tag[attr])
                
    return str(soup)

def translate_markdown_text(text, current_rel_path=""):
    placeholders = {}
    idx = 0

    # 1. Protect HTML tags
    def repl_html(match):
        nonlocal idx
        ph = f"__HTML_PH_{idx}__"
        placeholders[ph] = match.group(0)
        idx += 1
        return ph
    text = re.sub(r'<[^>]+>', repl_html, text)

    # 2. Protect Inline code blocks
    def repl_code(match):
        nonlocal idx
        ph = f"__CODE_PH_{idx}__"
        placeholders[ph] = match.group(0)
        idx += 1
        return ph
    text = re.sub(r'`[^`]+`', repl_code, text)

    # 3. Protect Image links, translating alt text & fixing URL
    def repl_img(match):
        nonlocal idx
        ph = f"__IMG_PH_{idx}__"
        alt_text = match.group(1)
        url = match.group(2)
        translated_alt = translate_text(alt_text)
        fixed_url = fix_url_for_en(url, current_rel_path)
        placeholders[ph] = f"![{translated_alt}]({fixed_url})"
        idx += 1
        return ph
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', repl_img, text)

    # 4. Protect Regular Markdown links, translating link text & fixing URL
    def repl_link(match):
        nonlocal idx
        ph = f"__LINK_PH_{idx}__"
        link_text = match.group(1)
        url = match.group(2)
        translated_link_text = translate_text(link_text)
        fixed_url = fix_url_for_en(url, current_rel_path)
        placeholders[ph] = f"[{translated_link_text}]({fixed_url})"
        idx += 1
        return ph
    text = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', repl_link, text)

    # Translate text after protecting Markdown entities
    translated_text = translate_text(text)

    # Restore placeholders
    for ph, original in placeholders.items():
        parts = ph.strip('_').split('_')
        regex_pattern = r'_\s*_\s*' + r'\s*_\s*'.join(re.escape(p) for p in parts) + r'\s*_\s*_'
        pattern = re.compile(regex_pattern, re.IGNORECASE)
        translated_text = pattern.sub(original, translated_text)

    return translated_text

def translate_markdown_content(md_content, current_rel_path=""):
    lines = md_content.split('\n')
    blocks = []
    current_block = []
    current_type = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.strip().startswith('```'):
            if current_block:
                blocks.append((current_type, '\n'.join(current_block)))
                current_block = []
            
            code_block = [line]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_block.append(lines[i])
                i += 1
            if i < len(lines):
                code_block.append(lines[i])
            blocks.append(('code', '\n'.join(code_block)))
            current_type = None
            i += 1
            continue
        
        if line.strip().startswith('#'):
            if current_block:
                blocks.append((current_type, '\n'.join(current_block)))
                current_block = []
            blocks.append(('header', line))
            current_type = None
            i += 1
            continue
            
        if not line.strip():
            if current_block:
                blocks.append((current_type, '\n'.join(current_block)))
                current_block = []
            blocks.append(('blank', line))
            current_type = None
            i += 1
            continue
            
        list_match = re.match(r'^(\s*[-*+]\s+|\s*\d+\.\s+)(.*)', line)
        if list_match:
            if current_block:
                blocks.append((current_type, '\n'.join(current_block)))
                current_block = []
            prefix = list_match.group(1)
            content = list_match.group(2)
            blocks.append(('list', (prefix, content)))
            current_type = None
            i += 1
            continue
            
        if current_type != 'paragraph':
            if current_block:
                blocks.append((current_type, '\n'.join(current_block)))
            current_block = [line]
            current_type = 'paragraph'
        else:
            current_block.append(line)
        i += 1
        
    if current_block:
        blocks.append((current_type, '\n'.join(current_block)))
        
    translated_parts = []
    for btype, bval in blocks:
        if btype == 'code' or btype == 'blank':
            translated_parts.append(bval)
        elif btype == 'header':
            header_match = re.match(r'^(#+\s+)(.*)', bval)
            if header_match:
                prefix, text = header_match.groups()
                translated_parts.append(prefix + translate_markdown_text(text, current_rel_path))
            else:
                translated_parts.append(translate_markdown_text(bval, current_rel_path))
        elif btype == 'list':
            prefix, text = bval
            translated_parts.append(prefix + translate_markdown_text(text, current_rel_path))
        elif btype == 'paragraph':
            translated_parts.append(translate_markdown_text(bval, current_rel_path))
            
    return '\n'.join(translated_parts)

def process_file(src_file_path):
    rel_path = os.path.relpath(src_file_path, SRC_DIR)
    dest_file_path = os.path.join(DEST_DIR, rel_path)
    
    dest_dir = os.path.dirname(dest_file_path)
    os.makedirs(dest_dir, exist_ok=True)
    
    ext = os.path.splitext(src_file_path)[1].lower()
    
    if ext in ['.html', '.htm']:
        print(f"Translating HTML: {rel_path}")
        with open(src_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        translated = translate_html_content(content, rel_path)
        with open(dest_file_path, 'w', encoding='utf-8') as f:
            f.write(translated)
            
    elif ext in ['.md', '.markdown']:
        print(f"Translating Markdown: {rel_path}")
        with open(src_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        translated = translate_markdown_content(content, rel_path)
        with open(dest_file_path, 'w', encoding='utf-8') as f:
            f.write(translated)
            
    else:
        if os.path.lexists(dest_file_path):
            os.remove(dest_file_path)
        
        rel_target = os.path.relpath(src_file_path, dest_dir)
        print(f"Symlinking: {rel_path} -> {rel_target}")
        os.symlink(rel_target, dest_file_path)

def main():
    print("Starting translation process...")
    
    cache_file = os.path.join(BASE_DIR, "translation_cache.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                loaded_cache = json.load(f)
                translation_cache.update(loaded_cache)
                print(f"Loaded {len(loaded_cache)} cached translations.")
        except Exception as e:
            print(f"Failed to load translation cache: {e}")
            
    os.makedirs(DEST_DIR, exist_ok=True)
    
    exclude_dirs = {
        'en', 
        'node_modules', 
        '.git', 
        '.github', 
        '.claude', 
        'venv', 
        '__pycache__'
    }
    
    for root, dirs, files in os.walk(SRC_DIR):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            if file.startswith('.'):
                continue
            process_file(file_path)
            
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(translation_cache, f, ensure_ascii=False, indent=2)
            print("Saved translation cache.")
    except Exception as e:
        print(f"Failed to save translation cache: {e}")
        
    print("Translation completed successfully!")

if __name__ == "__main__":
    main()
