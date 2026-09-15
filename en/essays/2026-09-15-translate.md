# Seriously Perfecting the Automatic Translation of English Websites

September 15, 2026 / Python / DeepL / Development

## One Month Since I "Just Put It Together"

Last month, I started translating my personal website into English, mostly on a whim. At the time, I figured, “As long as it works for now,” so I wrote a simple script and published it, but every time I wrote a new post, minor issues kept piling up.

What was particularly stressful was the **rate limit (IP restriction)** on the free translation endpoint. When articles got too long, they would hit the access limit, causing exponential wait times for retries with each paragraph (2 seconds, 4 seconds, 8 seconds…), which meant I had to wait several minutes or more for the build to complete.

On top of that, issues that couldn’t be overlooked began to stand out, such as the `inLanguage` in the JSON-LD (structured data) remaining as `ja`, and the site name “Rainweed Garden” "Rainweed Garden" (a garden of rain weeds?) and has remained in the cache—these and other glaring flaws that cannot be overlooked have become increasingly noticeable.

So, this time, we decided to undertake a full-scale overhaul of the translation pipeline.

## Implementing the DeepL API and Its Unmatched Speed

The biggest improvement was switching to the **DeepL API** (500,000 characters per month on the free plan) as our translation engine.

After creating a mechanism to load API keys and combining it with the cache (`translation_cache.json`), the update process changed dramatically. Translating new articles into English, which used to take several minutes, now completes in just over ten seconds.

Above all, the quality of the translation is significantly more natural. The translation smoothly handles subject complementation and contextual understanding of technical terms, greatly reducing the awkwardness typically associated with machine translation.

## Strategies for Preserving HTML Structure and Metadata

It's easy if you're just translating text, but actual web pages contain countless elements that must not be broken.

- **Code Block Protection**: To prevent program code, such as `__HTML_PH_0____HTML_PH_1__` or code within inline code, and shell commands from being corrupted during translation, they are temporarily stored in placeholders and then restored.
- **Optimizing JSON-LD and OGP**: Replace `og:locale` with `en_US`, replace `inLanguage` with `en` in the structured data, and automatically convert the article URL and author URL to be under `/en/`.
- **Dictionary and Cache Cleanup**: We batch-replaced approximately 380 entries that had been cached by Google Translate in the past as "Rainweed Garden" or "Amegusa no Niwa," thereby standardizing the brand name across the entire site to "Amekusa's Garden."

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

## To the World with a Single Command

As a result, the operational workflow has become extremely simple.

Just write a new Markdown post in Japanese and run `./update_essays.sh` once.

1. Generating the Japanese Version of the HTML
2. Automatic Generation of English HTML/Markdown Using DeepL
3. Automatic Updates to the Sitemap (`sitemap.xml`)

All of this is completed in just over ten seconds, and once you commit and push it to Git, it’s distributed worldwide (of course, the API key is securely protected by `.gitignore`).

At first, I started working on English localization thinking, “No one’s going to see it anyway,” but watching the pipeline run smoothly and seeing two languages synchronize simultaneously with a single click gives me a sense of satisfaction as an engineer—just that alone.
