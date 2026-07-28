#!/usr/bin/env python3
"""Build a local static preview of the GitHub Pages site."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import markdown
import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_preview"
PAGES = ["index.md", "research.md", "teaching.md", "cv.md", "contact.md"]


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    _, raw_meta, body = text.split("---\n", 2)
    return yaml.safe_load(raw_meta) or {}, body


def relative_url(url: str, page_depth: int) -> str:
    if ":" in url or url.startswith("#"):
        return url
    if url == "/":
        target = "index.html"
    elif url.endswith("/"):
        target = f"{url.strip('/')}/index.html"
    else:
        target = url.lstrip("/")
    prefix = "../" * page_depth
    return f"{prefix}{target}"


def render_liquid_urls(text: str, page_depth: int) -> str:
    pattern = re.compile(r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}")
    return pattern.sub(lambda match: relative_url(match.group(1), page_depth), text)


def page_output_path(meta: dict, source: str) -> tuple[Path, int, str]:
    if source == "index.md":
        return OUT / "index.html", 0, "/"
    permalink = meta.get("permalink")
    if permalink:
        clean = permalink.strip("/")
        return OUT / clean / "index.html", 1 if clean else 0, f"/{clean}/"
    stem = Path(source).stem
    return OUT / stem / "index.html", 1, f"/{stem}/"


def nav_html(config: dict, current_url: str, page_depth: int) -> str:
    links = []
    for item in config["navigation"]:
        href = relative_url(item["url"], page_depth)
        current = ' aria-current="page"' if item["url"] == current_url else ""
        links.append(f'<a href="{href}"{current}>{item["title"]}</a>')
    return "\n          ".join(links)


def render_page(config: dict, meta: dict, body: str, page_depth: int, current_url: str) -> str:
    body = render_liquid_urls(body, page_depth)
    content = markdown.markdown(body, extensions=["extra"])
    title = f"{meta.get('title')} | {config['title']}" if meta.get("title") else config["title"]
    css_url = relative_url("/assets/css/style.css", page_depth)

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{config['description']}">
    <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>

    <div class="site-shell">
      <aside class="sidebar" aria-label="Site introduction">
        <div class="identity">
          <a class="site-name" href="{relative_url('/', page_depth)}">{config['author']['name']}</a>
          <p class="site-role">{config['author']['role']}</p>
          <p class="site-affiliation">{config['author']['affiliation']}</p>
          <p class="site-location">{config['author']['location']}</p>
          <p class="site-email"><a href="mailto:{config['email']}">{config['email']}</a></p>
        </div>

        <nav class="site-nav" aria-label="Main navigation">
          {nav_html(config, current_url, page_depth)}
        </nav>
      </aside>

      <main id="main" class="content">
        {content}
      </main>
    </div>
  </body>
</html>
"""


def build() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    config = yaml.safe_load((ROOT / "_config.yml").read_text()) or {}

    css_source = (ROOT / "assets/css/style.scss").read_text()
    css = re.sub(r"^---\s*\n---\s*\n", "", css_source)
    css_dir = OUT / "assets/css"
    css_dir.mkdir(parents=True)
    (css_dir / "style.css").write_text(css)

    files_src = ROOT / "assets/files"
    files_dest = OUT / "assets/files"
    if files_src.exists():
        shutil.copytree(files_src, files_dest)

    published_src = ROOT / "Published Papers"
    published_dest = OUT / "Published Papers"
    if published_src.exists():
        shutil.copytree(published_src, published_dest, ignore=shutil.ignore_patterns(".DS_Store"))

    for source in PAGES:
        meta, body = split_front_matter((ROOT / source).read_text())
        output_path, depth, current_url = page_output_path(meta, source)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_page(config, meta, body, depth, current_url))

    print(f"Built preview at {OUT}")


if __name__ == "__main__":
    build()
