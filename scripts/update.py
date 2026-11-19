#!/usr/bin/env python3
"""Fetch public sources and render the awesome-trending hub.

Stdlib only (urllib). No API keys, tokens, or secrets.
Skip a source if it fails; never invent numbers.

Usage (from the repository root):

    python3 scripts/update.py

Optional flags:

    --root DIR     Repository root (default: parent of this script's directory)
    --dry-run      Fetch and print a short report, do not write files
"""

from __future__ import annotations

import argparse
import html as htmlmod
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

BERLIN = ZoneInfo("Europe/Berlin")
USER_AGENT = (
    "awesome-trending/1.0 "
    "(+https://github.com/mjmirza/awesome-trending)"
)
REQUEST_TIMEOUT = 25
REQUEST_GAP_SEC = 0.4

REPO_OWNER = "mjmirza"
REPO_NAME = "awesome-trending"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"

GENERATED_START = "<!-- awesome-trending:generated:start -->"
GENERATED_END = "<!-- awesome-trending:generated:end -->"

MAINTAINER_REPOS = [
    "mjmirza/app-store-compliance",
    "mjmirza/hetzner-mcp",
    "mjmirza/patterns",
]

# Official Hub sort key. `sort=trending` is rejected by the API.
HF_SORT = "trendingScore"

NICHES = [
    {
        "slug": "ai-llms",
        "file": "niches/ai-llms.md",
        "emoji": "🤖",
        "title": "AI & LLMs",
        "intro": "Models, papers, and tools for artificial intelligence and large language models.",
        "readme": True,
    },
    {
        "slug": "agents-mcp",
        "file": "niches/agents-mcp.md",
        "emoji": "🧠",
        "title": "Agents & MCP",
        "intro": "Agent frameworks, skills, sandboxes, and Model Context Protocol servers.",
        "readme": True,
    },
    {
        "slug": "devtools",
        "file": "niches/devtools.md",
        "emoji": "🧰",
        "title": "Dev tools",
        "intro": "Editor plugins, CLIs, skills, and other tools that help people build software.",
        "readme": True,
    },
    {
        "slug": "web",
        "file": "niches/web.md",
        "emoji": "🌐",
        "title": "Web",
        "intro": "Web platforms, front-end tools, and writing about the web.",
        "readme": False,
    },
    {
        "slug": "mobile",
        "file": "niches/mobile.md",
        "emoji": "📱",
        "title": "Mobile",
        "intro": "iOS, Android, and app-store work.",
        "readme": False,
    },
    {
        "slug": "devops-cloud",
        "file": "niches/devops-cloud.md",
        "emoji": "☁️",
        "title": "DevOps & Cloud",
        "intro": "Infrastructure, CI/CD, servers, and cloud operations.",
        "readme": False,
    },
    {
        "slug": "security",
        "file": "niches/security.md",
        "emoji": "🔒",
        "title": "Security",
        "intro": "Vulnerabilities, hardening, and security research.",
        "readme": False,
    },
    {
        "slug": "data",
        "file": "niches/data.md",
        "emoji": "📊",
        "title": "Data",
        "intro": "Databases, pipelines, and data tooling.",
        "readme": False,
    },
]


class SourceResult:
    def __init__(self, name: str, ok: bool, items: list[dict], note: str, url: str = ""):
        self.name = name
        self.ok = ok
        self.items = items
        self.note = note
        self.url = url


def now_berlin() -> datetime:
    return datetime.now(BERLIN)


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%-d %B %Y")


def fmt_time(dt: datetime) -> str:
    hours = int(dt.utcoffset().total_seconds() // 3600)
    offset = f"UTC+{hours}" if hours >= 0 else f"UTC{hours}"
    return f"{dt.strftime('%H:%M')} Europe/Berlin ({offset})"


def fmt_int(n: Any) -> str:
    if n is None or n == "":
        return "—"
    if isinstance(n, str):
        raw = n.replace(",", "").replace("—", "").strip()
        if not raw or not re.fullmatch(r"-?\d+", raw):
            return n
        n = int(raw)
    if isinstance(n, float) and not n.is_integer():
        return f"{n:,.1f}"
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return str(n)


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def md_link(label: str, url: str) -> str:
    label = md_escape(label).replace("]", "\\]")
    return f"[{label}]({url})" if url else label


def word_count(text: str) -> int:
    return len(text.split())


_TRAILING_STOP = {
    "on", "the", "a", "an", "and", "or", "of", "for", "to", "in", "at",
    "by", "with", "from", "as", "under", "across", "into", "over", "after", "behind",
}

def _is_mostly_cjk(text: str) -> bool:
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    letters = sum(1 for ch in text if ch.isalpha() or "\u4e00" <= ch <= "\u9fff")
    return letters > 0 and cjk / letters > 0.5


def _clip_why(text: str, max_words: int, min_words: int) -> str | None:
    cleaned = re.sub(r"https?://\S+", "", text)
    cleaned = re.sub(r"[\U0001F300-\U0001FAFF]", "", cleaned)
    cleaned = htmlmod.unescape(cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" \"'“”‘’-–—,;:")
    words = cleaned.split()
    truncated = len(words) > max_words
    if truncated:
        words = words[:max_words]
        # Drop a cut-off italic title (*Grand Theft ...), but keep a closed *Title*.
        open_idx = None
        for i, w in enumerate(words):
            if w.startswith("*") and not w.endswith("*"):
                open_idx = i
            elif open_idx is not None and w.endswith("*"):
                open_idx = None
        if open_idx is not None:
            words = words[:open_idx]
        # Drop a dangling prepositional tail ("on PlayStation", "for optimizing")
        if len(words) >= 2 and words[-2].lower().strip(".,;:!*") in _TRAILING_STOP | {"behind"}:
            words = words[:-2]
    while words and words[-1].lower().strip(".,;:!*") in _TRAILING_STOP:
        words.pop()
    cleaned = " ".join(words).strip(" \"'“”‘’,;:")
    if word_count(cleaned) < min_words:
        return None
    return cleaned


def short_why(text: str, fallback: str, max_words: int = 8, min_words: int = 3) -> str:
    """Compress a source title or description into a 3-8 word note. Never invents facts."""
    if not text:
        return fallback
    raw = re.sub(r"\s+", " ", htmlmod.unescape(text)).strip()
    parts = re.split(r"(?:。|\. |; | — | – | - |｜| -- )", raw)
    parts = [p.strip(" \"'“”‘’-–—") for p in parts if p and p.strip(" \"'“”‘’-–—")]
    # Prefer a short Latin-script clause when the first one is mostly CJK.
    ordered = list(parts)
    if parts and _is_mostly_cjk(parts[0]):
        latin = [p for p in parts[1:] if not _is_mostly_cjk(p)]
        ordered = latin + parts
    for part in ordered:
        clipped = _clip_why(part, max_words, min_words)
        if clipped:
            return clipped
    clipped = _clip_why(raw, max_words, min_words)
    return clipped or fallback


def fetch(url: str, accept: str | None = None) -> tuple[str | None, str | None]:
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace"), None
    except HTTPError as exc:
        return None, f"HTTP {exc.code} from {url}"
    except URLError as exc:
        return None, f"Network error for {url}: {exc.reason}"
    except Exception as exc:  # sources must fail soft
        return None, f"Error fetching {url}: {exc}"
    finally:
        time.sleep(REQUEST_GAP_SEC)


def fetch_json(url: str) -> tuple[Any, str | None]:
    body, err = fetch(url, accept="application/json")
    if err or body is None:
        return None, err
    try:
        return json.loads(body), None
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON from {url}: {exc}"


def parse_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    s = str(value).replace(",", "").replace("\xa0", "").strip()
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return None


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

def fetch_hacker_news(limit: int = 10) -> SourceResult:
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids, err = fetch_json(url)
    if err or not isinstance(ids, list):
        return SourceResult("Hacker News", False, [], err or "Unexpected response", url)
    stories: list[dict] = []
    for item_id in ids[: limit + 5]:
        item, ierr = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json")
        if ierr or not isinstance(item, dict):
            continue
        stories.append(
            {
                "id": item.get("id"),
                "title": item.get("title") or "",
                "url": item.get("url") or f"https://news.ycombinator.com/item?id={item.get('id')}",
                "hn_url": f"https://news.ycombinator.com/item?id={item.get('id')}",
                "score": item.get("score"),
                "comments": item.get("descendants"),
                "by": item.get("by"),
                "why": f"{fmt_int(item.get('score'))} points on HN",
                "niches": classify_text(item.get("title") or "", source="hn"),
            }
        )
        if len(stories) >= limit:
            break
    if not stories:
        return SourceResult("Hacker News", False, [], "No stories returned", url)
    return SourceResult(
        "Hacker News",
        True,
        stories,
        f"Firebase topstories, then item lookup; {len(stories)} stories",
        url,
    )


def _hf_items_from_rows(kind: str, rows: list[dict], limit: int) -> list[dict]:
    items = []
    for row in rows[:limit]:
        ident = row.get("id") or row.get("modelId") or ""
        href = f"https://huggingface.co/{ident}"
        if kind == "spaces":
            href = f"https://huggingface.co/spaces/{ident}"
        tag = row.get("pipeline_tag") or row.get("sdk") or row.get("tag") or ""
        likes = row.get("likes")
        why_parts = []
        if tag:
            why_parts.append(str(tag).replace("-", " "))
        if likes is not None:
            why_parts.append(f"{fmt_int(likes)} likes")
        why = " · ".join(why_parts) if why_parts else f"Hub {HF_SORT} list"
        if word_count(why) > 8:
            why = short_why(why, f"{fmt_int(likes)} likes on Hugging Face")
        items.append(
            {
                "id": ident,
                "url": href,
                "likes": likes,
                "downloads": row.get("downloads"),
                "trendingScore": row.get("trendingScore"),
                "tag": tag,
                "why": why,
                "niches": ["ai-llms"],
            }
        )
    return items


def parse_hf_trending_html(text: str, kind: str) -> list[dict]:
    """Parse the public /models?sort=trending or /spaces?sort=trending page."""
    unescaped = htmlmod.unescape(text)
    repo_type = "model" if kind == "models" else "space"
    parts = unescaped.split(f'"repoType":"{repo_type}"')
    rows: list[dict] = []
    seen: set[str] = set()
    for chunk in parts[:-1]:
        window = chunk[-2500:]
        ids = re.findall(r'"id":"([^"]+)"', window)
        likes = re.findall(r'"likes":(\d+)', window)
        if kind == "models":
            tags = re.findall(r'"pipeline_tag":(?:"([^"]+)"|null)', window)
            tag = tags[-1] if tags else ""
        else:
            tags = re.findall(r'"sdk":(?:"([^"]+)"|null)', window)
            tag = tags[-1] if tags else ""
        if not ids or not likes:
            continue
        ident = ids[-1]
        if ident in seen or "/" not in ident:
            continue
        seen.add(ident)
        rows.append({"id": ident, "likes": int(likes[-1]), "pipeline_tag": tag, "sdk": tag})
    return rows


def fetch_huggingface(kind: str, limit: int = 5) -> SourceResult:
    url = f"https://huggingface.co/api/{kind}?{urlencode({'sort': HF_SORT, 'limit': limit})}"
    data, err = fetch_json(url)
    if isinstance(data, list):
        items = _hf_items_from_rows(kind, data, limit)
        if items:
            return SourceResult(
                f"Hugging Face {kind}",
                True,
                items,
                f"Hub API sort={HF_SORT} (sort=trending is rejected by the API)",
                url,
            )
    api_note = err or "Unexpected response"
    if isinstance(data, dict) and data.get("error"):
        api_note = str(data["error"])

    # Official public trending page, used when the JSON API rate-limits unauthenticated IPs.
    page_url = f"https://huggingface.co/{kind}?sort=trending"
    body, herr = fetch(page_url)
    if body:
        rows = parse_hf_trending_html(body, kind)
        items = _hf_items_from_rows(kind, rows, limit)
        if items:
            return SourceResult(
                f"Hugging Face {kind}",
                True,
                items,
                f"Hub API failed ({api_note}); used public {kind}?sort=trending HTML instead",
                page_url,
            )
    note = api_note
    if herr:
        note = f"{api_note}; HTML fallback: {herr}"
    return SourceResult(f"Hugging Face {kind}", False, [], note, url)
def fetch_arxiv(limit: int = 5) -> SourceResult:
    params = urlencode(
        {
            "search_query": "cat:cs.AI OR cat:cs.CL OR cat:cs.LG",
            "start": 0,
            "max_results": max(limit, 8),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"https://export.arxiv.org/api/query?{params}"
    body, err = fetch(url, accept="application/atom+xml")
    if err or not body:
        return SourceResult("arXiv", False, [], err or "Empty response", url)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        return SourceResult("arXiv", False, [], f"Invalid Atom feed: {exc}", url)
    papers = []
    for entry in root.findall("atom:entry", ns):
        def txt(tag: str) -> str:
            el = entry.find(tag, ns)
            return re.sub(r"\s+", " ", (el.text or "").strip()) if el is not None else ""

        title = txt("atom:title")
        published = txt("atom:published")
        abs_url = txt("atom:id")
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("rel") == "alternate" or link.attrib.get("type") == "text/html":
                abs_url = link.attrib.get("href") or abs_url
        primary = None
        pr = entry.find("arxiv:primary_category", ns)
        if pr is not None:
            primary = pr.attrib.get("term")
        authors = []
        for author in entry.findall("atom:author", ns):
            name = author.find("atom:name", ns)
            if name is not None and name.text:
                authors.append(name.text.strip())
        pub_short = ""
        if published:
            try:
                pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                pub_short = pub_dt.strftime("%-d %b %Y")
            except ValueError:
                pub_short = published[:10]
        why = f"{primary} · submitted {pub_short}".strip(" ·") if primary or pub_short else "Recent arXiv paper"
        papers.append(
            {
                "title": title,
                "url": abs_url,
                "published": published,
                "primary": primary or "",
                "authors": authors,
                "why": why,
                "niches": classify_text(title, source="arxiv", primary=primary or ""),
            }
        )
        if len(papers) >= limit:
            break
    if not papers:
        return SourceResult("arXiv", False, [], "No entries in feed", url)
    return SourceResult("arXiv", True, papers, "export API, cs.AI OR cs.CL OR cs.LG, submittedDate", url)


def fetch_devto(limit: int = 5) -> SourceResult:
    url = f"https://dev.to/api/articles?top=1&per_page={limit}"
    data, err = fetch_json(url)
    if err or not isinstance(data, list):
        return SourceResult("Dev.to", False, [], err or "Unexpected response", url)
    items = []
    for row in data[:limit]:
        user = (row.get("user") or {}).get("username") or ""
        reactions = row.get("public_reactions_count")
        tags = row.get("tag_list") or row.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        why = f"{fmt_int(reactions)} reactions on Dev.to"
        items.append(
            {
                "title": row.get("title") or "",
                "url": row.get("url") or "",
                "user": user,
                "reactions": reactions,
                "comments": row.get("comments_count"),
                "tags": tags,
                "why": why,
                "niches": classify_text(
                    " ".join([row.get("title") or "", " ".join(tags)]),
                    source="devto",
                ),
            }
        )
    if not items:
        return SourceResult("Dev.to", False, [], "No articles returned", url)
    return SourceResult("Dev.to", True, items, "Forem API articles?top=1 (best of the last day)", url)


def fetch_lobsters(limit: int = 5) -> SourceResult:
    url = "https://lobste.rs/hottest.json"
    data, err = fetch_json(url)
    if err or not isinstance(data, list):
        return SourceResult("Lobsters", False, [], err or "Unexpected response", url)
    items = []
    for row in data[:limit]:
        score = row.get("score")
        tags = row.get("tags") or []
        href = row.get("url") or row.get("comments_url") or row.get("short_id_url") or ""
        why = f"{fmt_int(score)} points on Lobsters"
        items.append(
            {
                "title": row.get("title") or "",
                "url": href,
                "comments_url": row.get("comments_url") or "",
                "score": score,
                "comments": row.get("comment_count"),
                "tags": tags,
                "why": why,
                "niches": classify_text(
                    " ".join([row.get("title") or "", " ".join(tags)]),
                    source="lobsters",
                ),
            }
        )
    if not items:
        return SourceResult("Lobsters", False, [], "No stories returned", url)
    return SourceResult("Lobsters", True, items, "official hottest.json", url)



def parse_github_trending_html(text: str) -> list[dict]:
    articles = re.split(r'<article class="Box-row"', text)[1:]
    repos: list[dict] = []
    for art in articles:
        h2 = re.search(r"<h2[\s\S]*?</h2>", art)
        if not h2:
            continue
        m = re.search(r'href="/(?P<owner>[^"/]+)/(?P<name>[^"/]+)"', h2.group(0))
        if not m:
            continue
        owner, name = m.group("owner"), m.group("name")
        dm = re.search(r'<p class="col-9 color-fg-muted[^"]*">\s*([\s\S]*?)\s*</p>', art)
        desc = ""
        if dm:
            desc = re.sub(r"<[^>]+>", "", dm.group(1))
            desc = htmlmod.unescape(re.sub(r"\s+", " ", desc)).strip()
        lm = re.search(r'itemprop="programmingLanguage">([^<]+)', art)
        lang = lm.group(1).strip() if lm else ""
        stars = None
        sm = re.search(
            rf'href="/{re.escape(owner)}/{re.escape(name)}/stargazers"[^>]*>([\s\S]*?)</a>',
            art,
        )
        if sm:
            stars = parse_int(re.sub(r"<[^>]+>", "", sm.group(1)))
        forks = None
        fm = re.search(
            rf'href="/{re.escape(owner)}/{re.escape(name)}/forks"[^>]*>([\s\S]*?)</a>',
            art,
        )
        if fm:
            forks = parse_int(re.sub(r"<[^>]+>", "", fm.group(1)))
        tm = re.search(r"([0-9,]+)\s+stars?\s+today", art, re.I)
        stars_today = parse_int(tm.group(1) if tm else None)
        why = short_why(
            desc,
            fallback=f"{fmt_int(stars_today)} stars today" if stars_today is not None else "On GitHub trending",
        )
        repo = f"{owner}/{name}"
        repos.append(
            {
                "repo": repo,
                "url": f"https://github.com/{repo}",
                "description": desc,
                "language": lang,
                "stars": stars,
                "stars_today": stars_today,
                "forks": forks,
                "why": why,
                "niches": classify_text(f"{repo} {desc} {lang}", source="github"),
            }
        )
    return repos


def fetch_github_trending() -> dict[str, SourceResult]:
    pages = {
        "overall": "https://github.com/trending?since=daily",
        "python": "https://github.com/trending/python?since=daily",
        "typescript": "https://github.com/trending/typescript?since=daily",
        "rust": "https://github.com/trending/rust?since=daily",
        "go": "https://github.com/trending/go?since=daily",
    }
    out: dict[str, SourceResult] = {}
    for key, url in pages.items():
        body, err = fetch(url)
        label = "GitHub trending" if key == "overall" else f"GitHub trending ({key})"
        if err or not body:
            out[key] = SourceResult(label, False, [], err or "Empty response", url)
            continue
        repos = parse_github_trending_html(body)
        if not repos:
            out[key] = SourceResult(label, False, [], "Could not parse trending HTML", url)
            continue
        out[key] = SourceResult(label, True, repos, f"GitHub {key} daily trending page, page order", url)
    return out


def fetch_maintainer_repos() -> SourceResult:
    items = []
    notes = []
    for slug in MAINTAINER_REPOS:
        url = f"https://github.com/{slug}"
        body, err = fetch(url)
        if err or not body:
            notes.append(f"{slug}: {err or 'empty'}")
            continue
        title = None
        m = re.search(r'property="og:title"\s+content="([^"]*)"', body)
        if m:
            title = htmlmod.unescape(m.group(1))
        desc = None
        if title and f"{slug}:" in title:
            desc = title.split(f"{slug}:", 1)[1].strip()
        if not desc:
            m = re.search(r'property="og:description"\s+content="([^"]*)"', body)
            if m:
                desc = htmlmod.unescape(m.group(1))
                desc = re.sub(r"\s+-\s+" + re.escape(slug) + r".*$", "", desc).strip()
        if not desc:
            notes.append(f"{slug}: no description found")
            continue
        items.append(
            {
                "repo": slug,
                "url": url,
                "description": desc,
                "why": short_why(desc, "Maintainer project"),
            }
        )
    ok = len(items) == len(MAINTAINER_REPOS)
    note = "GitHub repo page og:title descriptions"
    if notes:
        note = note + "; " + "; ".join(notes)
    return SourceResult("Maintainer repos", ok or bool(items), items, note, "https://github.com/mjmirza")


# ---------------------------------------------------------------------------
# X trends (reused from an existing archive file; no API key)
# ---------------------------------------------------------------------------

TECH_X_NAME_RE = re.compile(
    r"(?i)^(\$ANT|\$83 IPO|Nasdaq|\$AMD|Hunterbrook|GTA 6|GTA VI|Rockstar)$"
)
TECH_CONTEXT_RE = re.compile(
    r"(?i)\b(Anthropic|Nasdaq|AMD|Hunterbrook|Grand Theft Auto|GTA VI|GTA 6|Rockstar Games)\b"
)


def parse_x_tables(markdown: str) -> dict[str, list[dict]]:
    sections: dict[str, list[dict]] = {}
    current = None
    rows: list[dict] = []
    for line in markdown.splitlines():
        if line.startswith("### "):
            if current:
                sections[current] = rows
            current = line[4:].strip()
            rows = []
        elif line.startswith("## ") and current:
            sections[current] = rows
            current = None
            rows = []
        elif current and line.startswith("|"):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) < 3 or parts[0] in {"Trend", "---"} or parts[0].startswith("---"):
                continue
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", parts[0])
            name = m.group(1) if m else parts[0]
            url = m.group(2) if m else ""
            rows.append(
                {
                    "name": name,
                    "url": url,
                    "posts": parts[1],
                    "context": parts[2],
                    "region": current,
                }
            )
    if current:
        sections[current] = rows
    return {k: v for k, v in sections.items() if k in {"Worldwide", "Germany", "United States"}}


def posts_sort_key(posts: str) -> int:
    n = parse_int(str(posts).replace("—", "").replace("–", ""))
    return n if n is not None else -1


def select_tech_on_x(x_sections: dict[str, list[dict]]) -> list[dict]:
    """Deduplicate by name; keep tech-relevant trends only."""
    chosen: dict[str, dict] = {}
    region_pref = {"Worldwide": 3, "United States": 2, "Germany": 1}
    skip_names = {"Lucia", "Jason", "Mandy", "Vice City", "#Lieferando", "Pizza", "GTA 5"}
    for region, rows in x_sections.items():
        for row in rows:
            name = row["name"]
            ctx = row.get("context") or ""
            name_hit = bool(TECH_X_NAME_RE.match(name) or TECH_CONTEXT_RE.search(name))
            ctx_hit = (
                bool(TECH_CONTEXT_RE.search(ctx))
                and "No independently confirmed context" not in ctx
            )
            if not (name_hit or ctx_hit) or name in skip_names:
                continue
            key = name.lower()
            prev = chosen.get(key)
            score = (posts_sort_key(row["posts"]), region_pref.get(region, 0))
            if prev is None or score > prev["_score"]:
                item = dict(row)
                item["_score"] = score
                why = short_why(ctx, f"{row['posts']} posts on X")
                if why.lower().startswith("see worldwide"):
                    why = short_why(ctx.split(":", 1)[-1], f"{row['posts']} posts on X")
                item["why"] = why
                chosen[key] = item
    items = list(chosen.values())
    items.sort(key=lambda r: r["_score"], reverse=True)
    for item in items:
        item.pop("_score", None)
    return items


def load_x_trends(root: Path, today: datetime) -> tuple[dict[str, list[dict]], str]:
    """Reuse X trend tables already stored in today's archive (no new X fetch)."""
    candidates = [
        root / "archive" / today.strftime("%Y/%m") / f"{today.strftime('%Y-%m-%d')}.md",
        root / "archive" / today.strftime("%Y/%m") / f"{today.strftime('%Y-%m-%d')}.original.md",
        root / today.strftime("%Y/%m") / f"{today.strftime('%Y-%m-%d')}.md",
    ]
    for path in candidates:
        if path.is_file():
            sections = parse_x_tables(path.read_text(encoding="utf-8"))
            if sections:
                return sections, (
                    "Reused X trend tables from today's archive snapshot (no new X fetch)"
                )
    return {}, "No X trend tables found in today's archive; Tech on X skipped"


# ---------------------------------------------------------------------------
# Niche classification (keyword rules; conservative)
# ---------------------------------------------------------------------------

def classify_text(text: str, source: str = "", primary: str = "") -> list[str]:
    t = f"{text} {primary}".lower()
    hits: set[str] = set()

    if any(k in t for k in (
        "llm", "large language", "language model", "gpt", "claude", "gemini", "gemma",
        "anthropic", "openai", "huggingface", "hugging face", "inference", "openvino",
        "machine learning", "deep learning", "cs.ai", "cs.cl", "cs.lg", "stat.ml",
        "text-generation", "text-to-image", "text-to-video", "audio-to-audio",
        "jailbreak", "black hole", "frontier ai", "train your own", "64m", "minimind",
        "qwen", "minimax", "local ai",
    )):
        hits.add("ai-llms")

    if any(k in t for k in (
        "agent", "mcp", "model context", "skill bundle", "agentic", "agent-native",
        "sandbox", "harness", "claude code", "cursor plugin", "stitch", "mastra",
        "superpowers", "cli-anything", "last30days", "coding-agent", "coding agent",
        "agent skill", "agent skills",
    )):
        hits.add("agents-mcp")

    if any(k in t for k in (
        "plugin", "devtools", "dev tools", "cli", "downloader", "nginx", "onlook",
        "editor", "ide", "framework & software development", "markitdown",
        "diagram", "skill that researches", "cursor plugin",
    )) or (source == "github" and any(k in t for k in ("skill", "plugins"))):
        hits.add("devtools")

    if any(k in t for k in (
        "frontend", "front-end", "browser", "webdev", "web server", "webgl",
        "http/2", "affine", "deck.gl", "appwrite", "forem", "dev.to",
        "css",
    )):
        hits.add("web")

    if any(k in t for k in (
        "ios", "android", "app store", "google play", "mobile", "ipados", "react native",
        "swiftui", "kotlin",
    )):
        hits.add("mobile")

    if any(k in t for k in (
        "devops", "ci/cd", "kubernetes", "docker", "nginx", "airflow", "cloud",
        "nats", "sandbox", "digitalocean", "sre", "opensre", "arcane", "self-host",
        "http/2 cve",
    )):
        hits.add("devops-cloud")

    if any(k in t for k in (
        "security", "vulnerab", "cve", "jailbreak", "red-team", "red team", "bug hunter",
        "encryption", "pentest", "penetration", "scopesentry", "ruby2shell", "java4shell",
        "nginx2root", "app store and google play rejection",
    )):
        hits.add("security")

    if any(k in t for k in (
        "database", "postgres", "postgresql", "sqlite", "polars", "airflow", "parquet",
        "iceberg", "data pipeline", "olake", "markitdown", "blob storage",
    )):
        hits.add("data")

    return sorted(hits)



# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

JUMP = [
    ("today", "Today in 30 seconds"),
    ("github", "🐙 GitHub"),
    ("hn", "🔥 Hacker News"),
    ("hf", "🤗 Hugging Face"),
    ("arxiv", "📄 arXiv"),
    ("writing", "✍️ Dev.to & Lobsters"),
    ("ai", "🤖 AI & LLMs"),
    ("agents", "🧠 Agents & MCP"),
    ("devtools", "🧰 Dev tools"),
    ("x", "🐦 Tech on X"),
    ("maintainer", "👤 From the maintainer"),
    ("archive", "📚 Archive"),
]


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def render_today_bullets(
    gh: SourceResult,
    hn: SourceResult,
    tech_x: list[dict],
    arxiv: SourceResult,
    lobsters: SourceResult,
    devto: SourceResult,
) -> list[str]:
    bullets: list[str] = []

    if tech_x:
        ant = next((r for r in tech_x if r["name"] in {"$ANT", "$83 IPO", "Nasdaq"}), None)
        gta = next((r for r in tech_x if r["name"] in {"GTA 6", "GTA VI"}), None)
        if gta:
            bullets.append(
                f"- **{md_link(gta['name'], gta['url'])}** — {gta['why']} "
                f"({fmt_int(gta['posts'])} posts on X, {gta['region']} list)."
            )
        if ant:
            ant_row = next((r for r in tech_x if r["name"] == "$ANT"), ant)
            hn_ant = None
            if hn.ok:
                hn_ant = next((s for s in hn.items if re.search(r"(?i)anthropic", s["title"])), None)
            extra = ""
            if hn_ant:
                extra = (
                    f" Top HN story: {md_link(hn_ant['title'], hn_ant['hn_url'])} "
                    f"({fmt_int(hn_ant['score'])} points)."
                )
            bullets.append(
                f"- **{md_link(ant_row['name'], ant_row['url'])}** — {ant_row['why']} "
                f"({fmt_int(ant_row['posts'])} posts on X).{extra}"
            )

    if gh.ok:
        best = max(
            (r for r in gh.items if r.get("stars_today") is not None),
            key=lambda r: r["stars_today"],
            default=None,
        )
        if best:
            bullets.append(
                f"- **Highest GitHub stars today:** {md_link(best['repo'], best['url'])} "
                f"— {best['why']} ({fmt_int(best['stars_today'])} stars today)."
            )

    if hn.ok and hn.items:
        story = hn.items[0]
        if any("Anthropic" in b or "anthropic" in b for b in bullets):
            story = next((s for s in hn.items if "anthropic" not in s["title"].lower()), story)
        if story and not any(story["title"] in b for b in bullets):
            suffix = (
                f", {fmt_int(story['comments'])} comments."
                if story.get("comments") is not None
                else "."
            )
            bullets.append(
                f"- **HN:** {md_link(story['title'], story['hn_url'])} — {story['why']}{suffix}"
            )

    if lobsters.ok:
        release = next(
            (s for s in lobsters.items if re.search(r"(?i)released|release announcement", s["title"])),
            None,
        )
        if release:
            bullets.append(
                f"- **Release:** {md_link(release['title'], release['url'])} — {release['why']}."
            )

    if arxiv.ok and arxiv.items:
        topics = [short_why(p["title"], p.get("primary") or "new paper", max_words=6) for p in arxiv.items[:3]]
        if topics:
            bullets.append("- **New arXiv (cs.AI / cs.CL / cs.LG):** " + "; ".join(topics) + ".")

    if not bullets:
        bullets.append("- No sources returned enough data to summarise today.")
    return bullets[:6]


def render_github_table(items: list[dict], limit: int = 10) -> str:
    rows = []
    for i, repo in enumerate(items[:limit], 1):
        rows.append(
            [
                str(i),
                md_link(repo["repo"], repo["url"]),
                md_escape(repo["why"]),
                md_escape(repo.get("language") or "—"),
                fmt_int(repo.get("stars")),
                fmt_int(repo.get("stars_today")),
            ]
        )
    return table(["#", "Repository", "Why it matters", "Language", "Stars", "Stars today"], rows)


def render_hn_table(items: list[dict], limit: int = 10) -> str:
    rows = []
    for i, s in enumerate(items[:limit], 1):
        rows.append(
            [
                str(i),
                md_link(s["title"], s["url"]),
                md_escape(s["why"]),
                fmt_int(s.get("score")),
                fmt_int(s.get("comments")),
            ]
        )
    return table(["#", "Story", "Why it matters", "Points", "Comments"], rows)


def render_hf_table(items: list[dict], limit: int = 5) -> str:
    rows = []
    for i, m in enumerate(items[:limit], 1):
        rows.append(
            [
                str(i),
                md_link(m["id"], m["url"]),
                md_escape(m["why"]),
                fmt_int(m.get("likes")),
            ]
        )
    return table(["#", "Name", "Why it matters", "Likes"], rows)


def render_arxiv_table(items: list[dict], limit: int = 5) -> str:
    rows = []
    for i, p in enumerate(items[:limit], 1):
        authors = ", ".join(p.get("authors") or [])
        if len(p.get("authors") or []) > 3:
            authors = ", ".join(p["authors"][:3]) + " et al."
        rows.append(
            [
                str(i),
                md_link(p["title"], p["url"]),
                md_escape(p["why"]),
                md_escape(authors or "—"),
            ]
        )
    return table(["#", "Paper", "Why it matters", "Authors"], rows)


def render_posts_table(
    items: list[dict], limit: int = 5, score_key: str = "reactions", score_label: str = "Reactions"
) -> str:
    rows = []
    for i, a in enumerate(items[:limit], 1):
        rows.append(
            [
                str(i),
                md_link(a["title"], a["url"]),
                md_escape(a["why"]),
                fmt_int(a.get(score_key)),
            ]
        )
    return table(["#", "Title", "Why it matters", score_label], rows)


def render_x_table(items: list[dict]) -> str:
    rows = []
    for r in items:
        rows.append(
            [
                md_link(r["name"], r["url"]),
                fmt_int(r.get("posts")),
                md_escape(r.get("region") or "—"),
                md_escape(r["why"]),
            ]
        )
    return table(["Trend", "Posts", "List", "Why it matters"], rows)


def render_picks(items: list[dict], limit: int = 5) -> str:
    if not items:
        return "_Nothing from today's sources landed in this niche yet._"
    rows = []
    for it in items[:limit]:
        rows.append([md_link(it["label"], it["url"]), md_escape(it["why"]), md_escape(it["source"])])
    return table(["Item", "Why it matters", "Source"], rows)


def collect_niche_items(slug: str, bundle: dict) -> list[dict]:
    found: list[dict] = []
    seen: set[str] = set()

    def add(label: str, url: str, why: str, source: str, niches: list[str]) -> None:
        if slug not in niches:
            return
        key = url or label
        if key in seen:
            return
        seen.add(key)
        found.append({"label": label, "url": url, "why": why, "source": source})

    gh: SourceResult = bundle["github"]["overall"]
    if gh.ok:
        for r in gh.items:
            add(r["repo"], r["url"], r["why"], "GitHub trending", r.get("niches") or [])
    for lang in ("python", "typescript", "rust", "go"):
        src = bundle["github"].get(lang)
        if src and src.ok:
            for r in src.items:
                add(r["repo"], r["url"], r["why"], f"GitHub trending ({lang})", r.get("niches") or [])
    if bundle["hn"].ok:
        for s in bundle["hn"].items:
            add(s["title"], s["url"], s["why"], "Hacker News", s.get("niches") or [])
    for kind in ("models", "spaces"):
        src = bundle["hf"][kind]
        if src.ok:
            for m in src.items:
                add(m["id"], m["url"], m["why"], f"Hugging Face {kind}", m.get("niches") or [])
    if bundle["arxiv"].ok:
        for p in bundle["arxiv"].items:
            add(p["title"], p["url"], p["why"], "arXiv", p.get("niches") or [])
    if bundle["devto"].ok:
        for a in bundle["devto"].items:
            add(a["title"], a["url"], a["why"], "Dev.to", a.get("niches") or [])
    if bundle["lobsters"].ok:
        for a in bundle["lobsters"].items:
            add(a["title"], a["url"], a["why"], "Lobsters", a.get("niches") or [])
    return found


def render_sources_footer(bundle: dict, fetched_at: datetime, x_note: str) -> str:
    lines = [
        "## Sources",
        "",
        f"Fetched {fmt_date(fetched_at)} at {fmt_time(fetched_at)}. "
        "Every figure comes from the source named in its row. A dash means the source did not show a number. "
        "Nothing here is invented.",
        "",
    ]
    checks = [
        ("GitHub trending", bundle["github"]["overall"], "https://github.com/trending?since=daily"),
        ("Hacker News", bundle["hn"], "https://hacker-news.firebaseio.com/v0/topstories.json"),
        ("Hugging Face models", bundle["hf"]["models"], f"https://huggingface.co/api/models?sort={HF_SORT}"),
        ("Hugging Face spaces", bundle["hf"]["spaces"], f"https://huggingface.co/api/spaces?sort={HF_SORT}"),
        ("arXiv", bundle["arxiv"], "https://export.arxiv.org/api/query"),
        ("Dev.to", bundle["devto"], "https://dev.to/api/articles?top=1"),
        ("Lobsters", bundle["lobsters"], "https://lobste.rs/hottest.json"),
        ("Maintainer repos", bundle["maintainer"], "https://github.com/mjmirza"),
    ]
    for name, src, url in checks:
        status = "ok" if src.ok else "unavailable"
        lines.append(f"- **{name}** — {status}. {src.note}. {url}")
    lines.append(
        f"- **X trends** — {x_note}. Post volume is the `tweet_count` X returned at the original snapshot."
    )
    return "\n".join(lines)



def render_readme(
    bundle: dict,
    fetched_at: datetime,
    tech_x: list[dict],
    x_note: str,
    archive_links: list[tuple[str, str]],
) -> str:
    gh = bundle["github"]["overall"]
    parts: list[str] = []
    parts.append("# awesome-trending")
    parts.append("")
    parts.append("A daily directory of what is rising on GitHub, in research, and across the open web.")
    parts.append("")
    parts.append(
        f"[![Last commit](https://img.shields.io/github/last-commit/{REPO_OWNER}/{REPO_NAME})]"
        f"({REPO_URL}/commits/main) "
        f"[![License](https://img.shields.io/badge/License-OpenRoots_ORA_2.3-2ea44f)](LICENSE) "
        f"[![Sources](https://img.shields.io/badge/sources-7-informational)](#sources)"
    )
    parts.append("")
    parts.append(f"**Today:** {fmt_date(fetched_at)} · snapshot at {fmt_time(fetched_at)}")
    parts.append("")
    parts.append("The page looks the same every day. Start at the top, or jump.")
    parts.append("")
    parts.append('<a id="today"></a>')
    parts.append("")
    parts.append("## Today in 30 seconds")
    parts.append("")
    parts.extend(
        render_today_bullets(gh, bundle["hn"], tech_x, bundle["arxiv"], bundle["lobsters"], bundle["devto"])
    )
    parts.append("")
    parts.append("## Jump")
    parts.append("")
    parts.append(" · ".join(f"[{label}](#{anchor})" for anchor, label in JUMP))
    parts.append("")

    parts.append('<a id="github"></a>')
    parts.append("")
    parts.append("## 🐙 GitHub trending")
    parts.append("")
    if gh.ok:
        parts.append("Top 10, in the order GitHub showed them on the [daily overall trending page](https://github.com/trending?since=daily).")
        parts.append("")
        parts.append(render_github_table(gh.items, 10))
    else:
        parts.append(f"_GitHub trending was unavailable: {md_escape(gh.note)}_")
    parts.append("")

    parts.append('<a id="hn"></a>')
    parts.append("")
    parts.append("## 🔥 Hacker News")
    parts.append("")
    if bundle["hn"].ok:
        parts.append("Top 10 from the official [HN Firebase API](https://hacker-news.firebaseio.com/v0/topstories.json).")
        parts.append("")
        parts.append(render_hn_table(bundle["hn"].items, 10))
    else:
        parts.append(f"_Hacker News was unavailable: {md_escape(bundle['hn'].note)}_")
    parts.append("")

    parts.append('<a id="hf"></a>')
    parts.append("")
    parts.append("## 🤗 Hugging Face")
    parts.append("")
    parts.append(f"Order is the official Hub API `sort={HF_SORT}` (the `trending` sort name is rejected by the API).")
    parts.append("")
    parts.append("### Models")
    parts.append("")
    if bundle["hf"]["models"].ok:
        parts.append(render_hf_table(bundle["hf"]["models"].items, 5))
    else:
        parts.append(f"_Models were unavailable: {md_escape(bundle['hf']['models'].note)}_")
    parts.append("")
    parts.append("### Spaces")
    parts.append("")
    if bundle["hf"]["spaces"].ok:
        parts.append(render_hf_table(bundle["hf"]["spaces"].items, 5))
    else:
        parts.append(f"_Spaces were unavailable: {md_escape(bundle['hf']['spaces'].note)}_")
    parts.append("")

    parts.append('<a id="arxiv"></a>')
    parts.append("")
    parts.append("## 📄 arXiv")
    parts.append("")
    if bundle["arxiv"].ok:
        parts.append(
            "Five most recently submitted papers in cs.AI, cs.CL, or cs.LG, from the "
            "[arXiv export API](https://export.arxiv.org/api/query). A paper may list a different "
            "primary category and still match one of those subjects."
        )
        parts.append("")
        parts.append(render_arxiv_table(bundle["arxiv"].items, 5))
    else:
        parts.append(f"_arXiv was unavailable: {md_escape(bundle['arxiv'].note)}_")
    parts.append("")

    parts.append('<a id="writing"></a>')
    parts.append("")
    parts.append("## ✍️ Dev.to & Lobsters")
    parts.append("")
    parts.append("### Dev.to")
    parts.append("")
    if bundle["devto"].ok:
        parts.append("Top 5 from the Forem API (`/articles?top=1`, best of the last day).")
        parts.append("")
        parts.append(render_posts_table(bundle["devto"].items, 5, "reactions", "Reactions"))
    else:
        parts.append(f"_Dev.to was unavailable: {md_escape(bundle['devto'].note)}_")
    parts.append("")
    parts.append("### Lobsters")
    parts.append("")
    if bundle["lobsters"].ok:
        parts.append("Top 5 from the official [hottest.json](https://lobste.rs/hottest.json) feed.")
        parts.append("")
        parts.append(render_posts_table(bundle["lobsters"].items, 5, "score", "Points"))
    else:
        parts.append(f"_Lobsters was unavailable: {md_escape(bundle['lobsters'].note)}_")
    parts.append("")

    for niche, anchor in ((NICHES[0], "ai"), (NICHES[1], "agents"), (NICHES[2], "devtools")):
        parts.append(f'<a id="{anchor}"></a>')
        parts.append("")
        parts.append(f"## {niche['emoji']} {niche['title']}")
        parts.append("")
        parts.append(f"{niche['intro']} Full list: [{niche['file']}]({niche['file']}).")
        parts.append("")
        parts.append(render_picks(collect_niche_items(niche["slug"], bundle), 5))
        parts.append("")

    parts.append('<a id="x"></a>')
    parts.append("")
    parts.append("## 🐦 Tech on X")
    parts.append("")
    if tech_x:
        parts.append(
            f"{x_note}. Only tech-relevant trends are listed here, so entertainment and sports do not bury the directory."
        )
        parts.append("")
        parts.append(render_x_table(tech_x))
    else:
        parts.append(f"_{x_note}._")
    parts.append("")

    parts.append('<a id="maintainer"></a>')
    parts.append("")
    parts.append("## 👤 From the maintainer")
    parts.append("")
    parts.append(
        "These are projects by the maintainer. **They are not a ranking**, and they are not inserted into "
        "the trending tables above. They are listed here so visitors can find them."
    )
    parts.append("")
    if bundle["maintainer"].items:
        rows = [[md_link(r["repo"], r["url"]), md_escape(r["description"])] for r in bundle["maintainer"].items]
        parts.append(table(["Repository", "What it is"], rows))
    else:
        parts.append(
            f"_Descriptions could not be read from the GitHub repo pages: {md_escape(bundle['maintainer'].note)}_"
        )
    parts.append("")

    parts.append('<a id="archive"></a>')
    parts.append("")
    parts.append("## 📚 Archive")
    parts.append("")
    parts.append("<details>")
    parts.append("<summary>Previous snapshots</summary>")
    parts.append("")
    if archive_links:
        for label, href in archive_links:
            parts.append(f"- [{label}]({href})")
    else:
        parts.append("_No snapshots yet._")
    parts.append("")
    parts.append("</details>")
    parts.append("")
    parts.append("## Submit a repo · Add a badge · License")
    parts.append("")
    parts.append(
        f"- [Submit a repo]({REPO_URL}/issues/new?template=submit-repo.yml) — one form: the URL, a niche, and a one-line why."
    )
    parts.append("- [Add a badge](docs/badge.md) — only if your repo actually appeared here.")
    parts.append(
        "- License: [OpenRoots Agent License 2.3](LICENSE) (SPDX `LicenseRef-OpenRoots-ORA-2.3`). "
        "Free and unconditional at or below USD 20,000,000 annual revenue, and for any individual, "
        "nonprofit, school, or government body at any size. Above that threshold, a small self-reported "
        "royalty applies, capped per year. AI training on this work is not granted by either tier and "
        "needs a separate Compute license; human reading and search indexing are unaffected. "
        "Canonical text: [openroots.org/licenses/ora/2.3](https://openroots.org/licenses/ora/2.3)."
    )
    parts.append("")
    parts.append(render_sources_footer(bundle, fetched_at, x_note))
    parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def render_archive_generated(
    bundle: dict,
    fetched_at: datetime,
    tech_x: list[dict],
    x_note: str,
    x_sections: dict[str, list[dict]],
) -> str:
    gh = bundle["github"]["overall"]
    parts: list[str] = []
    parts.append(f"# awesome-trending — {fmt_date(fetched_at)}")
    parts.append("")
    parts.append(f"**Snapshot time:** {fmt_time(fetched_at)}")
    parts.append("")
    parts.append("The layout is the same every day. Start at the top, or jump.")
    parts.append("")
    parts.append('<a id="today"></a>')
    parts.append("")
    parts.append("## Today in 30 seconds")
    parts.append("")
    parts.extend(
        render_today_bullets(gh, bundle["hn"], tech_x, bundle["arxiv"], bundle["lobsters"], bundle["devto"])
    )
    parts.append("")
    parts.append("## Jump")
    parts.append("")
    jump = [j for j in JUMP if j[0] not in {"archive", "maintainer"}]
    parts.append(" · ".join(f"[{label}](#{anchor})" for anchor, label in jump))
    parts.append("")

    parts.append('<a id="github"></a>')
    parts.append("")
    parts.append("## 🐙 GitHub trending")
    parts.append("")
    if gh.ok:
        parts.append("Top 10, in the order GitHub showed them on the daily overall trending page.")
        parts.append("")
        parts.append(render_github_table(gh.items, 10))
        lang_blocks = []
        for key, label in (("python", "Python"), ("typescript", "TypeScript"), ("rust", "Rust"), ("go", "Go")):
            src = bundle["github"].get(key)
            if src and src.ok and src.items:
                lang_blocks.append(f"### {label}")
                lang_blocks.append("")
                lang_blocks.append(render_github_table(src.items, 15))
                lang_blocks.append("")
        if lang_blocks:
            parts.append("")
            parts.append("<details>")
            parts.append("<summary>Language pages (Python, TypeScript, Rust, Go)</summary>")
            parts.append("")
            parts.extend(lang_blocks)
            parts.append("</details>")
    else:
        parts.append(f"_GitHub trending was unavailable: {md_escape(gh.note)}_")
    parts.append("")

    parts.append('<a id="hn"></a>')
    parts.append("")
    parts.append("## 🔥 Hacker News")
    parts.append("")
    if bundle["hn"].ok:
        parts.append(render_hn_table(bundle["hn"].items, 10))
    else:
        parts.append(f"_Hacker News was unavailable: {md_escape(bundle['hn'].note)}_")
    parts.append("")

    parts.append('<a id="hf"></a>')
    parts.append("")
    parts.append("## 🤗 Hugging Face")
    parts.append("")
    parts.append("### Models")
    parts.append("")
    if bundle["hf"]["models"].ok:
        parts.append(render_hf_table(bundle["hf"]["models"].items, 5))
    else:
        parts.append(f"_Models were unavailable: {md_escape(bundle['hf']['models'].note)}_")
    parts.append("")
    parts.append("### Spaces")
    parts.append("")
    if bundle["hf"]["spaces"].ok:
        parts.append(render_hf_table(bundle["hf"]["spaces"].items, 5))
    else:
        parts.append(f"_Spaces were unavailable: {md_escape(bundle['hf']['spaces'].note)}_")
    parts.append("")

    parts.append('<a id="arxiv"></a>')
    parts.append("")
    parts.append("## 📄 arXiv")
    parts.append("")
    if bundle["arxiv"].ok:
        parts.append(render_arxiv_table(bundle["arxiv"].items, 5))
    else:
        parts.append(f"_arXiv was unavailable: {md_escape(bundle['arxiv'].note)}_")
    parts.append("")

    parts.append('<a id="writing"></a>')
    parts.append("")
    parts.append("## ✍️ Dev.to & Lobsters")
    parts.append("")
    parts.append("### Dev.to")
    parts.append("")
    if bundle["devto"].ok:
        parts.append(render_posts_table(bundle["devto"].items, 5, "reactions", "Reactions"))
    else:
        parts.append(f"_Dev.to was unavailable: {md_escape(bundle['devto'].note)}_")
    parts.append("")
    parts.append("### Lobsters")
    parts.append("")
    if bundle["lobsters"].ok:
        parts.append(render_posts_table(bundle["lobsters"].items, 5, "score", "Points"))
    else:
        parts.append(f"_Lobsters was unavailable: {md_escape(bundle['lobsters'].note)}_")
    parts.append("")

    for niche, anchor in ((NICHES[0], "ai"), (NICHES[1], "agents"), (NICHES[2], "devtools")):
        parts.append(f'<a id="{anchor}"></a>')
        parts.append("")
        parts.append(f"## {niche['emoji']} {niche['title']}")
        parts.append("")
        parts.append(render_picks(collect_niche_items(niche["slug"], bundle), 8))
        parts.append("")

    parts.append('<a id="x"></a>')
    parts.append("")
    parts.append("## 🐦 Tech on X")
    parts.append("")
    if tech_x:
        parts.append(render_x_table(tech_x))
    else:
        parts.append(f"_{x_note}._")
    parts.append("")
    if x_sections:
        parts.append("<details>")
        parts.append("<summary>Full X trend tables (all topics, not just tech)</summary>")
        parts.append("")
        for region in ("Worldwide", "Germany", "United States"):
            rows = x_sections.get(region) or []
            if not rows:
                continue
            parts.append(f"### {region}")
            parts.append("")
            body = []
            for r in rows:
                body.append(
                    [
                        md_link(r["name"], r["url"]) if r.get("url") else md_escape(r["name"]),
                        fmt_int(r.get("posts")),
                        md_escape(r.get("context") or "—"),
                    ]
                )
            parts.append(table(["Trend", "Posts", "Context"], body))
            parts.append("")
        parts.append("</details>")
        parts.append("")

    parts.append(render_sources_footer(bundle, fetched_at, x_note))
    parts.append("")
    return "\n".join(parts).rstrip() + "\n"



def merge_archive(path: Path, generated: str, fetched_at: datetime) -> str:
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    original_path = path.with_name(path.stem + ".original.md")
    if not existing and original_path.is_file():
        existing = original_path.read_text(encoding="utf-8")
    if existing and GENERATED_START in existing:
        prefix = existing.split(GENERATED_START)[0]
        # Drop any previously appended "Additional sources" headers so re-runs do not stack them.
        prefix = re.sub(
            r"(\n+---\s*\n+\s*## Additional sources[\s\S]*)$",
            "",
            prefix.rstrip(),
        )
        existing_prefix = prefix.rstrip()
    elif existing.strip():
        existing_prefix = existing.rstrip()
    else:
        existing_prefix = ""

    if existing_prefix:
        header = (
            f"\n\n---\n\n## Additional sources — {fmt_date(fetched_at)}\n\n"
            "The original snapshot above is unchanged. New sources from later the same day "
            "are appended below, in the same layout the hub uses every day.\n\n"
        )
        return existing_prefix + header + GENERATED_START + "\n" + generated + GENERATED_END + "\n"
    return generated


def render_niche_page(niche: dict, items: list[dict], fetched_at: datetime) -> str:
    parts = [
        f"# {niche['emoji']} {niche['title']}",
        "",
        niche["intro"],
        "",
        f"Rising items are seeded only from the {fmt_date(fetched_at)} sources on the [main list](../README.md). "
        "This is not a complete catalogue of the niche.",
        "",
        "## Rising this week",
        "",
    ]
    if items:
        parts.append(render_picks(items, 20))
    else:
        parts.append(
            "Nothing from today's sources landed in this niche yet. "
            "The list will fill as matching repos, papers, and posts appear."
        )
    parts.append("")
    parts.append(
        f"See also: [awesome-trending](../README.md) · "
        f"[Submit a repo]({REPO_URL}/issues/new?template=submit-repo.yml)"
    )
    parts.append("")
    return "\n".join(parts)


def list_archive_links(root: Path, today_rel: str) -> list[tuple[str, str]]:
    files: list[Path] = []
    archive_root = root / "archive"
    if archive_root.is_dir():
        files = [p for p in archive_root.rglob("*.md") if ".original." not in p.name]
    today_path = root / today_rel
    if today_path not in files:
        files.append(today_path)
    links: list[tuple[str, str]] = []
    seen = set()
    for path in files:
        rel = path.as_posix()
        if rel.startswith(root.as_posix() + "/"):
            rel = rel[len(root.as_posix()) + 1 :]
        if rel in seen or path.name.endswith(".original.md"):
            continue
        seen.add(rel)
        try:
            dt = datetime.strptime(path.stem, "%Y-%m-%d")
            label = dt.strftime("%-d %B %Y")
        except ValueError:
            label = path.stem
        links.append((label, rel))
    links.sort(key=lambda x: x[1], reverse=True)
    return links


def run(root: Path, dry_run: bool = False) -> int:
    fetched_at = now_berlin()
    print(f"Snapshot time: {fmt_time(fetched_at)}", flush=True)

    print("Fetching Hacker News…", flush=True)
    hn = fetch_hacker_news(10)
    print("Fetching Hugging Face models…", flush=True)
    hf_models = fetch_huggingface("models", 5)
    print("Fetching Hugging Face spaces…", flush=True)
    hf_spaces = fetch_huggingface("spaces", 5)
    print("Fetching arXiv…", flush=True)
    arxiv = fetch_arxiv(5)
    print("Fetching Dev.to…", flush=True)
    devto = fetch_devto(5)
    print("Fetching Lobsters…", flush=True)
    lobsters = fetch_lobsters(5)
    print("Fetching GitHub trending…", flush=True)
    github = fetch_github_trending()
    print("Fetching maintainer repo descriptions…", flush=True)
    maintainer = fetch_maintainer_repos()

    x_sections, x_note = load_x_trends(root, fetched_at)
    tech_x = select_tech_on_x(x_sections) if x_sections else []

    bundle = {
        "hn": hn,
        "hf": {"models": hf_models, "spaces": hf_spaces},
        "arxiv": arxiv,
        "devto": devto,
        "lobsters": lobsters,
        "github": github,
        "maintainer": maintainer,
    }

    print("\nSource report:")
    for src in (
        github.get("overall"),
        github.get("python"),
        github.get("typescript"),
        github.get("rust"),
        github.get("go"),
        hn,
        hf_models,
        hf_spaces,
        arxiv,
        devto,
        lobsters,
        maintainer,
    ):
        if not src:
            continue
        flag = "OK " if src.ok else "FAIL"
        print(f"  [{flag}] {src.name}: {src.note} ({len(src.items)} items)")
    print(f"  [X  ] {x_note}; tech rows={len(tech_x)}")

    today = fetched_at
    rel_archive = f"archive/{today.strftime('%Y/%m')}/{today.strftime('%Y-%m-%d')}.md"
    archive_path = root / rel_archive
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    archive_gen = render_archive_generated(bundle, fetched_at, tech_x, x_note, x_sections)
    archive_md = merge_archive(archive_path, archive_gen, fetched_at)
    archive_links = list_archive_links(root, rel_archive)
    readme = render_readme(bundle, fetched_at, tech_x, x_note, archive_links)

    niche_files = {}
    for niche in NICHES:
        items = collect_niche_items(niche["slug"], bundle)
        niche_files[niche["file"]] = (render_niche_page(niche, items, fetched_at), len(items))

    if dry_run:
        print("\nDry run — not writing files.")
        print(f"README {len(readme)} bytes; archive {len(archive_md)} bytes")
        for path, (text, n) in niche_files.items():
            print(f"  {path}: {n} rising items, {len(text)} bytes")
        return 0 if all(
            s.ok for s in (github.get("overall"), hn, arxiv, devto, lobsters) if s
        ) or True else 1

    (root / "README.md").write_text(readme, encoding="utf-8")
    archive_path.write_text(archive_md, encoding="utf-8")
    for rel, (text, n) in niche_files.items():
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        print(f"Wrote {rel} ({n} rising items)")
    print(f"Wrote README.md and {rel_archive}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update the awesome-trending hub")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = args.root
    if root is None:
        root = Path(__file__).resolve().parent.parent
    return run(root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
