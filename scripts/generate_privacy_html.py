#!/usr/bin/env python3
"""Generate privacy HTML pages from v2 markdown sources."""

from __future__ import annotations

import html
import re
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent.parent
MD_DIR = WEB_DIR.parent / "outboard-companion" / "outboard_companion" / "assets" / "legal"

CSS = """\
:root{color-scheme:dark;--bg:#07090d;--text:#f4f4f5;--muted:#b7bcc7;--line:rgba(255,255,255,.12);--accent:#e53e3e}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;min-height:100vh;background:radial-gradient(ellipse 70% 40% at 50% 0%,rgba(229,62,62,.12),transparent 65%),var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.6}
a{color:inherit;text-decoration-color:rgba(229,62,62,.75);text-underline-offset:.18em}a:hover{color:#fff;text-decoration-color:var(--accent)}
.wrap{width:min(940px,calc(100% - 40px));margin:0 auto;padding:32px 0 72px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:18px 0 34px}
.brand{display:inline-flex;align-items:center;gap:12px;color:var(--text);text-decoration:none;font-weight:800;letter-spacing:-.02em}
.brand img{width:40px;height:40px;border-radius:10px}.nav{display:flex;align-items:center;gap:14px;color:var(--muted);font-size:14px;flex-wrap:wrap}
.card{background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.02));border:1px solid var(--line);border-radius:24px;padding:clamp(24px,4vw,56px);box-shadow:0 24px 80px rgba(0,0,0,.35)}
h1{margin:0 0 10px;font-size:clamp(2rem,5vw,3.4rem);line-height:1.05;letter-spacing:-.055em}
h2{margin:42px 0 12px;padding-top:18px;border-top:1px solid var(--line);font-size:clamp(1.25rem,2.4vw,1.65rem);line-height:1.2;letter-spacing:-.025em}
h3{margin:26px 0 8px;font-size:1.08rem;color:#fff}p,li{color:var(--muted);font-size:16px}p{margin:10px 0}ul{margin:12px 0 0;padding-left:22px}li{margin:7px 0}strong{color:#fff;font-weight:700}
.footer{margin-top:28px;color:rgba(255,255,255,.55);font-size:13px;text-align:center}@media(max-width:640px){.topbar{align-items:flex-start;flex-direction:column}}"""

LANGS = [
    {
        "code": "en",
        "html": "privacy-en.html",
        "md": "privacy_policy_en_v2.md",
        "title": "Privacy Policy — Sparkmaster",
        "description": "Privacy Policy — Sparkmaster",
        "nav_home": "Home",
        "nav_languages": "Languages",
        "nav_support": "Support",
    },
    {
        "code": "fi",
        "html": "privacy-fi.html",
        "md": "privacy_policy_fi_v2.md",
        "title": "Tietosuojaseloste — Sparkmaster",
        "description": "Tietosuojaseloste — Sparkmaster",
        "nav_home": "Home",
        "nav_languages": "Kielet",
        "nav_support": "Support",
    },
    {
        "code": "de",
        "html": "privacy-de.html",
        "md": "privacy_policy_de_v2.md",
        "title": "Datenschutzerklärung — Sparkmaster",
        "description": "Datenschutzerklärung — Sparkmaster",
        "nav_home": "Start",
        "nav_languages": "Sprachen",
        "nav_support": "Support",
    },
    {
        "code": "es",
        "html": "privacy-es.html",
        "md": "privacy_policy_es_v2.md",
        "title": "Política de privacidad — Sparkmaster",
        "description": "Política de privacidad — Sparkmaster",
        "nav_home": "Inicio",
        "nav_languages": "Idiomas",
        "nav_support": "Soporte",
    },
    {
        "code": "fr",
        "html": "privacy-fr.html",
        "md": "privacy_policy_fr_v2.md",
        "title": "Politique de confidentialité — Sparkmaster",
        "description": "Politique de confidentialité — Sparkmaster",
        "nav_home": "Accueil",
        "nav_languages": "Langues",
        "nav_support": "Assistance",
    },
    {
        "code": "sv",
        "html": "privacy-sv.html",
        "md": "privacy_policy_sv_v2.md",
        "title": "Integritetspolicy — Sparkmaster",
        "description": "Integritetspolicy — Sparkmaster",
        "nav_home": "Hem",
        "nav_languages": "Språk",
        "nav_support": "Support",
    },
    {
        "code": "ja",
        "html": "privacy-ja.html",
        "md": "privacy_policy_ja_v2.md",
        "title": "プライバシーポリシー — Sparkmaster",
        "description": "プライバシーポリシー — Sparkmaster",
        "nav_home": "ホーム",
        "nav_languages": "言語",
        "nav_support": "サポート",
    },
    {
        "code": "ko",
        "html": "privacy-ko.html",
        "md": "privacy_policy_ko_v2.md",
        "title": "개인정보 처리방침 — Sparkmaster",
        "description": "개인정보 처리방침 — Sparkmaster",
        "nav_home": "홈",
        "nav_languages": "언어",
        "nav_support": "지원",
    },
]

HREFLANGS = [(item["code"], item["html"]) for item in LANGS]

URL_RE = re.compile(r"https?://[^\s<]+")
EMAIL_RE = re.compile(r"(?<![\w.-])support@sparkmaster\.app(?![\w@])")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
CODE_RE = re.compile(r"`([^`]+)`")


def inline(text: str) -> str:
    text = html.escape(text)
    text = BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = CODE_RE.sub(r"<code>\1</code>", text)

    def link_url(match: re.Match[str]) -> str:
        url = match.group(0)
        return f'<a href="{url}">{url}</a>'

    text = URL_RE.sub(link_url, text)
    text = EMAIL_RE.sub(
        r'<a href="mailto:support@sparkmaster.app">support@sparkmaster.app</a>',
        text,
    )
    return text


def md_to_html_body(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if not line.strip():
            i += 1
            continue

        if line.startswith("# "):
            out.append(f"<h1>{inline(line[2:])}</h1>")
            i += 1
            continue

        if line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
            i += 1
            continue

        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
            i += 1
            continue

        if line.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{inline(lines[i][2:].rstrip())}</li>")
                i += 1
            out.append("</ul>")
            continue

        out.append(f"<p>{inline(line)}</p>")
        i += 1

    return "\n".join(out)


def hreflang_links(current: str) -> str:
    parts = []
    for code, filename in HREFLANGS:
        parts.append(
            f'  <link rel="alternate" hreflang="{code}" href="https://sparkmaster.app/{filename}">'
        )
    parts.append(
        '  <link rel="alternate" hreflang="x-default" href="https://sparkmaster.app/privacy-en.html">'
    )
    return "\n".join(parts)


def render_page(meta: dict, body: str) -> str:
    hreflangs = hreflang_links(meta["html"])
    return f"""<!doctype html>
<html lang="{meta["code"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(meta["title"])}</title>
  <meta name="description" content="{html.escape(meta["description"])}">
  <link rel="canonical" href="https://sparkmaster.app/{meta["html"]}">
{hreflangs}
  <link rel="icon" href="assets/app-icon.png">
  <style>
{CSS}
  </style>
</head>
<body>
  <main class="wrap">
    <header class="topbar">
      <a class="brand" href="/">
        <img src="assets/app-icon.png" alt="" width="40" height="40">
        <span>Sparkmaster</span>
      </a>
      <nav class="nav" aria-label="Navigation">
        <a href="/">{meta["nav_home"]}</a>
        <a href="privacy.html">{meta["nav_languages"]}</a>
        <a href="support.html">{meta["nav_support"]}</a>
      </nav>
    </header>
    <article class="card">
{body}
    </article>
    <footer class="footer">© 2026 Sparkmaster · Sublime Web Oy · <a href="mailto:support@sparkmaster.app">support@sparkmaster.app</a></footer>
  </main>
</body>
</html>
"""


def main() -> None:
    written: list[str] = []
    for meta in LANGS:
        md_path = MD_DIR / meta["md"]
        md_text = md_path.read_text(encoding="utf-8")
        body = md_to_html_body(md_text)
        html_text = render_page(meta, body)
        out_path = WEB_DIR / meta["html"]
        out_path.write_text(html_text, encoding="utf-8", newline="\n")
        written.append(meta["html"])
        print(f"Wrote {out_path.name} ({len(md_text)} chars MD -> {len(body)} chars body)")


if __name__ == "__main__":
    main()
