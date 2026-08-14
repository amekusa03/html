# I made an English site for the time being.

2026-08-14

## Not that I particularly wanted to do it

Without really coming up with any good ideas, I decided to create an English website. We don't expect visitors who need the English version to come to us, nor are we expecting any SEO benefits. However, I started it as an exploration of what I would do if I were to do it.

## Leave the translation to the script

I decided to write a Python script to translate each page at once. The mechanism is to use the Google Translate API, sequentially input existing Markdown files, and generate the English version under the `en/` folder.

[Python Script](essays/2026-08-14-translate.text)

The batch conversion itself worked easily, but when I reviewed it, I found some issues.

## What I learned after trying it

**Link misalignment. ** The script does not have a process to insert `en/` at the beginning of the URL. If I tried to rewrite the links on all pages mechanically, it would probably become chaotic, so I decided to do it manually.

**Japanese in the image. ** A surprising blind spot was the case where the image file contained Japanese text. Scripts can only translate text, so of course they can't access the contents of images. If you want to seriously support multiple languages, I feel that this is an important point to consider from the beginning.

**Missing the conversion in "". ** In several cases, the part enclosed in square brackets was left intact. Apparently this is a specification of Google Translate. It would be a good idea to be aware of how to use parentheses when writing the material.

**Unnatural literal translation. ** If you translate subject omission, which is unique to Japanese, into English, you will end up with a sentence in which it is difficult to tell who is speaking. "think..." is sometimes written as `We think...`, but depending on the context, `I think...` is more natural. If you want to properly convey the nuances, you need to correct this with a human eye.

**sitemap.xml. ** To tell search engines that your site is multilingual, you need to write the Japanese and English versions as a pair in `xhtml:link`.

```html
<xhtml:link rel="alternate" hreflang="ja" href="https://amekusa.vercel.app/hobbies"/>
<xhtml:link rel="alternate" hreflang="en" href="https://amekusa.vercel.app/en/hobbies/"/>
```

## Release for now

Although it is rough cut, it will be released in this condition. There is no point in waiting for perfection.
