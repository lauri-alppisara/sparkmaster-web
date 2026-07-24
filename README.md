# Sparkmaster website

Static GitHub Pages website for [sparkmaster.app](https://sparkmaster.app).

## Files

- `index.html` — landing page (8 languages: en, fi, de, es, fr, sv, ja, ko)
- `winterize.html` — seasonal winterization checklist landing (en/fi/sv)
- `privacy.html` — privacy language chooser (auto-redirects by browser/saved language; `?chooser=1` keeps the grid)
- `privacy-*.html` — localized privacy policies from app legal markdown v2
- `support.html` — support page (same 8 languages)
- `CNAME` — custom domain for GitHub Pages
- `assets/` — logo and app icon
- `scripts/generate_privacy_html.py` — regenerates privacy HTML from app sources

## Regenerate privacy pages

From this repo (with `outboard-companion` as a sibling directory):

```bash
python scripts/generate_privacy_html.py
```

Sources: `../outboard-companion/outboard_companion/assets/legal/privacy_policy_*_v2.md`

## Publish

Repo is deployed via GitHub Pages from branch `main` (root), domain `sparkmaster.app`.
