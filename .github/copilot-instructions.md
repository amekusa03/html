---
description: "Workspace instructions for the static Vercel homepage project. Use this guidance when editing HTML/CSS/JS, maintaining project pages, or updating deployment metadata."
applyTo: ["**/*"]
---

# Project overview

- This repository is a static personal/portfolio website built with plain HTML, CSS, and client-side JavaScript.
- Root files include `index.html`, `index_en.html`, `style.css`, `rain.js`, `robots.txt`, `sitemap.xml`, and `versel.json`.
- The `app/` directory contains independent project detail pages.
- The `doc/` directory contains source notes and link references, not the rendered site.
- Deployment is intended for Vercel.

# What to do

- Edit page content directly in HTML and CSS.
- Preserve the existing static structure; do not introduce a build system unless the repository explicitly adds one.
- Keep `sitemap.xml` and `robots.txt` consistent with added or removed pages.
- When adding pages under `app/`, ensure they match the existing language, navigation, and Vercel-friendly static structure.
- Update `versel.json` only when adding site-level headers or Vercel-specific configuration.

# Key files

- `index.html`, `index_en.html`: main Japanese and English landing pages.
- `style.css`: global styles used by the site.
- `rain.js`: client-side script for visual effects.
- `app/**/*.html`: project pages and subsite content.
- `doc/concept.md`, `doc/linklist.md`: project design notes, not part of rendered site.
- `sitemap.xml`: hard-coded site map entries for search engines.
- `versel.json`: Vercel configuration for static headers.

# Important conventions

- Keep markup simple and accessible for static hosting.
- Preserve the existing Vercel-specific asset references like `/_vercel/insights/script.js`.
- Favor direct edits over adding a JS framework or extra deployment tooling.
- If local preview is needed, use a static file server or open pages directly; do not assume `npm start` works without a `package.json`.

# Helpful prompt examples

- "Review `index.html` and suggest improvements for Japanese/English consistency and SEO metadata."
- "Add a new project page under `app/` and update `sitemap.xml` with the new URL."
- "Explain how to keep `versel.json` and `robots.txt` aligned with the site’s current structure."
