#!/usr/bin/env python3
"""Dependency-free static checks for the public FactuSerein website."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_EXCLUDED_PARTS = {".git", ".github", ".agents", "docs", "kit-commercial"}
CANONICAL_ORIGIN = "https://factuserein.fr"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.h1_count = 0
        self.meta: list[dict[str, str]] = []
        self.canonicals: list[str] = []
        self.links: list[str] = []
        self.assets: list[tuple[str, str]] = []
        self.scripts: list[str] = []
        self.jsonld: list[str] = []
        self._capture: str | None = None
        self._capture_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()

        if tag == "title":
            self._begin_capture("title")
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonicals.append(values.get("href", ""))
        elif tag == "a":
            self.links.append(values.get("href", ""))
        elif tag == "img":
            self.assets.append((values.get("src", ""), values.get("alt", "")))
        elif tag == "script":
            source = values.get("src", "")
            if source:
                self.scripts.append(source)
            elif values.get("type", "").lower() == "application/ld+json":
                self._begin_capture("jsonld")
            else:
                self._begin_capture("javascript")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title" and self._capture == "title":
            self.title = "".join(self._capture_buffer).strip()
            self._finish_capture()
        elif tag == "script" and self._capture in {"jsonld", "javascript"}:
            content = "".join(self._capture_buffer).strip()
            if self._capture == "jsonld":
                self.jsonld.append(content)
            elif content:
                self.scripts.append(f"inline:{content}")
            self._finish_capture()

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._capture_buffer.append(data)

    def _begin_capture(self, kind: str) -> None:
        self._capture = kind
        self._capture_buffer = []

    def _finish_capture(self) -> None:
        self._capture = None
        self._capture_buffer = []


def public_html_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if not any(part in PUBLIC_EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)
    )


def relative_url(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    return "/" if relative == "index.html" else f"/{relative}"


def is_noindex(parser: PageParser) -> bool:
    return any(
        meta.get("name", "").lower() == "robots"
        and "noindex" in meta.get("content", "").lower()
        for meta in parser.meta
    )


def check_local_reference(page: Path, reference: str, errors: list[str], kind: str) -> None:
    if not reference or reference.startswith("#"):
        return
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        return
    raw_path = unquote(parsed.path)
    if not raw_path:
        return
    if raw_path.startswith("/"):
        target = (ROOT / raw_path.lstrip("/")).resolve()
    else:
        target = (page.parent / raw_path).resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f"{page.relative_to(ROOT)}: {kind} sort du site: {reference}")
        return
    if raw_path.endswith("/"):
        target /= "index.html"
    if not target.is_file():
        errors.append(f"{page.relative_to(ROOT)}: {kind} introuvable: {reference}")


def check_canonical(page: Path, canonical: str, errors: list[str]) -> None:
    parsed = urlsplit(canonical)
    if parsed.scheme != "https" or parsed.netloc != "factuserein.fr":
        errors.append(f"{page.relative_to(ROOT)}: canonical hors domaine: {canonical}")
        return
    if parsed.query or parsed.fragment:
        errors.append(f"{page.relative_to(ROOT)}: canonical avec query/fragment: {canonical}")


def check_pages(errors: list[str]) -> dict[Path, PageParser]:
    parsed_pages: dict[Path, PageParser] = {}
    for page in public_html_files():
        parser = PageParser()
        try:
            parser.feed(page.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"{page.relative_to(ROOT)}: lecture impossible: {exc}")
            continue
        parsed_pages[page] = parser

        for href in parser.links:
            check_local_reference(page, href, errors, "lien")
        for source, alt in parser.assets:
            check_local_reference(page, source, errors, "image")
            if source and not alt.strip():
                errors.append(f"{page.relative_to(ROOT)}: image sans alt: {source}")
        for source in parser.scripts:
            if not source.startswith("inline:"):
                check_local_reference(page, source, errors, "script")

        if len(parser.canonicals) != 1:
            errors.append(f"{page.relative_to(ROOT)}: {len(parser.canonicals)} canonical au lieu de 1")
        elif not is_noindex(parser):
            check_canonical(page, parser.canonicals[0], errors)

        if is_noindex(parser):
            continue

        if not 30 <= len(parser.title) <= 70:
            errors.append(f"{page.relative_to(ROOT)}: title hors longueur SEO (30-70): {len(parser.title)}")
        descriptions = [
            meta.get("content", "").strip()
            for meta in parser.meta
            if meta.get("name", "").lower() == "description"
        ]
        if len(descriptions) != 1:
            errors.append(f"{page.relative_to(ROOT)}: {len(descriptions)} meta description au lieu de 1")
        elif not 110 <= len(descriptions[0]) <= 170:
            errors.append(
                f"{page.relative_to(ROOT)}: description hors longueur SEO (110-170): {len(descriptions[0])}"
            )
        if parser.h1_count != 1:
            errors.append(f"{page.relative_to(ROOT)}: {parser.h1_count} balise h1 au lieu de 1")

        og_title = [meta for meta in parser.meta if meta.get("property", "").lower() == "og:title"]
        og_description = [meta for meta in parser.meta if meta.get("property", "").lower() == "og:description"]
        if len(og_title) != 1 or not og_title[0].get("content", "").strip():
            errors.append(f"{page.relative_to(ROOT)}: og:title absent ou dupliqué")
        if len(og_description) != 1 or not og_description[0].get("content", "").strip():
            errors.append(f"{page.relative_to(ROOT)}: og:description absent ou dupliqué")

        for payload in parser.jsonld:
            try:
                json.loads(payload)
            except json.JSONDecodeError as exc:
                errors.append(f"{page.relative_to(ROOT)}: JSON-LD invalide: {exc.msg}")

    return parsed_pages


def check_sitemap(errors: list[str], parsed_pages: dict[Path, PageParser]) -> None:
    sitemap_path = ROOT / "sitemap.xml"
    try:
        root = ElementTree.parse(sitemap_path).getroot()
    except (OSError, ElementTree.ParseError) as exc:
        errors.append(f"sitemap.xml invalide: {exc}")
        return

    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locations = [node.text.strip() for node in root.findall(f"{namespace}url/{namespace}loc") if node.text]
    if len(locations) != len(set(locations)):
        errors.append("sitemap.xml contient des URLs dupliquées")

    expected: set[str] = set()
    for page, parser in parsed_pages.items():
        if not is_noindex(parser):
            expected.add(f"{CANONICAL_ORIGIN}{relative_url(page)}")
    missing = sorted(expected - set(locations))
    if missing:
        errors.append(f"sitemap.xml oublie: {', '.join(missing)}")
    forbidden = [url for url in locations if "validateur.html" in url or "cloudfront.net" in url]
    if forbidden:
        errors.append(f"sitemap.xml contient une URL legacy/temporaire: {', '.join(forbidden)}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: https://factuserein.fr/sitemap.xml" not in robots:
        errors.append("robots.txt ne référence pas le sitemap canonique")
    for private_path in ("/kit-commercial/", "/docs/", "/README.md"):
        if f"Disallow: {private_path}" not in robots:
            errors.append(f"robots.txt ne bloque pas {private_path}")


def check_javascript(errors: list[str], parsed_pages: dict[Path, PageParser]) -> None:
    sources: list[tuple[str, str]] = []
    for path in sorted((ROOT / "assets" / "js").glob("*.js")):
        sources.append((path.relative_to(ROOT).as_posix(), path.read_text(encoding="utf-8")))
    for page, parser in parsed_pages.items():
        for source in parser.scripts:
            if source.startswith("inline:"):
                sources.append((f"{page.relative_to(ROOT).as_posix()} (inline)", source[7:]))

    for label, source in sources:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".js", delete=False) as handle:
            handle.write(source)
            temporary_path = Path(handle.name)
        try:
            result = subprocess.run(
                ["node", "--check", str(temporary_path)],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            errors.append("Node.js est requis pour vérifier le JavaScript")
            return
        finally:
            temporary_path.unlink(missing_ok=True)
        if result.returncode:
            detail = (result.stderr or result.stdout).strip().splitlines()[-1:]
            errors.append(f"{label}: JavaScript invalide: {' '.join(detail)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors: list[str] = []
    parsed_pages = check_pages(errors)
    check_sitemap(errors, parsed_pages)
    check_javascript(errors, parsed_pages)

    if errors:
        print("Site validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Site validation passed: {len(parsed_pages)} public HTML pages checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
