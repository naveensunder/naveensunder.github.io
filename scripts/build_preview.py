#!/usr/bin/env python3
"""Build a local static preview of the GitHub Pages site into _preview/.

Renders the real _layouts/default.html and _includes/*.html with python-liquid
(pip install --user python-liquid), so the preview matches what Jekyll builds.
Serve it with:  python3 -m http.server 8001 --directory _preview
"""

from __future__ import annotations

import re
import shutil
import urllib.parse
from pathlib import Path

import yaml

try:
    from liquid import Environment, FileSystemLoader
except ImportError:  # pragma: no cover
    raise SystemExit("python-liquid is missing. Run: python3 -m pip install --user python-liquid")


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_preview"
PAGES = ["index.html", "publications.html", "working-papers.html", "teaching.html",
         "cv.html", "contact.html", "404.html"]
STATIC_DIRS = ["assets/files", "assets/images", "assets/js", "Published Papers", "Working Papers"]
SKIP_SUFFIXES = {".docx", ".DS_Store"}


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    _, raw_meta, body = text.split("---\n", 2)
    return yaml.safe_load(raw_meta) or {}, body


def jekyll_includes_to_liquid(src: str) -> str:
    """Jekyll writes {% include name.html %}; python-liquid wants the name quoted."""
    return re.sub(r"{%-?\s*include\s+([^\s\"'%]+)\s*-?%}", lambda m: '{% include "' + m.group(1) + '" %}', src)


def make_env(config: dict) -> Environment:
    env = Environment(loader=FileSystemLoader(str(ROOT / "_includes")))
    baseurl = config.get("baseurl", "") or ""
    site_url = (config.get("url", "") or "").rstrip("/")
    env.filters["relative_url"] = lambda s: baseurl + str(s)
    env.filters["absolute_url"] = lambda s: site_url + baseurl + str(s)
    env.filters["uri_escape"] = lambda s: urllib.parse.quote(str(s), safe="/:&?=#(),'")
    return env


def page_output_path(meta: dict, source: str) -> tuple[Path, str]:
    if source == "index.html":
        return OUT / "index.html", "/"
    permalink = meta.get("permalink")
    if permalink and permalink.endswith(".html"):
        return OUT / permalink.lstrip("/"), permalink
    if permalink:
        clean = permalink.strip("/")
        return OUT / clean / "index.html", f"/{clean}/"
    stem = Path(source).stem
    return OUT / stem / "index.html", f"/{stem}/"


def copy_tree(src: Path, dest: Path) -> None:
    if not src.exists():
        return
    for path in src.rglob("*"):
        if path.is_dir() or path.suffix in SKIP_SUFFIXES or path.name == ".DS_Store":
            continue
        target = dest / path.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def build() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    config = yaml.safe_load((ROOT / "_config.yml").read_text()) or {}
    data = {}
    for yml in sorted((ROOT / "_data").glob("*.yml")):
        data[yml.stem] = yaml.safe_load(yml.read_text())
    site = dict(config)
    site["data"] = data

    env = make_env(config)
    # Includes are loaded by python-liquid itself; rewrite their Jekyll-style nested includes too.
    env.loader = FileSystemLoader(str(ROOT / "_includes"))
    layout_src = jekyll_includes_to_liquid((ROOT / "_layouts/default.html").read_text())
    layout = env.from_string(layout_src)

    css_source = (ROOT / "assets/css/style.scss").read_text()
    css = re.sub(r"^---\s*\n---\s*\n", "", css_source)
    (OUT / "assets/css").mkdir(parents=True)
    (OUT / "assets/css/style.css").write_text(css)

    for sub in STATIC_DIRS:
        copy_tree(ROOT / sub, OUT / sub)

    for source in PAGES:
        meta, body = split_front_matter((ROOT / source).read_text())
        output_path, url = page_output_path(meta, source)
        page = dict(meta)
        page["url"] = url
        content = env.from_string(jekyll_includes_to_liquid(body)).render(site=site, page=page)
        html = layout.render(site=site, page=page, content=content)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)

    print(f"Built preview at {OUT}")


if __name__ == "__main__":
    build()
