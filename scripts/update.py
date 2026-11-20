#!/usr/bin/env python3
"""Fetch public trend sources and render the awesome-trending hub.

Stdlib only (urllib, json, xml, concurrent.futures). No API keys, tokens or
secrets. Every source is optional: a source that times out, errors or returns
nothing is listed as skipped in the sources table and the run carries on.
No numbers are ever invented; a dash means the source did not give a value.

Usage (from the repository root):

    python3 scripts/update.py              # fetch and write files
    python3 scripts/update.py --dry-run    # fetch and print a report only

Optional flags:

    --root DIR     Repository root (default: parent of this script's directory)
    --only KEYS    Comma-separated source keys to fetch (for debugging)
"""

from __future__ import annotations

import argparse
import gzip
import html as htmlmod
import json
import re
import sys
import threading
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

BERLIN = ZoneInfo("Europe/Berlin")
USER_AGENT = "awesome-trending/1.0 (+https://github.com/mjmirza/awesome-trending)"

REQUEST_TIMEOUT = 15        # seconds per HTTP request
RETRIES = 1                 # one retry on network errors and 5xx
TOTAL_BUDGET = 150          # seconds for all fetching; later requests are refused
MAX_WORKERS = 8

REPO_OWNER = "mjmirza"
REPO_NAME = "awesome-trending"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
SUBMIT_URL = f"{REPO_URL}/issues/new?template=submit-repo.yml"

GENERATED_START = "<!-- awesome-trending:generated:start -->"
GENERATED_END = "<!-- awesome-trending:generated:end -->"

MAINTAINER_REPOS = [
    "mjmirza/app-store-compliance",
    "mjmirza/hetzner-mcp",
    "mjmirza/patterns",
]

GITHUB_LANGUAGES = [
    ("python", "Python"),
    ("typescript", "TypeScript"),
    ("rust", "Rust"),
    ("go", "Go"),
]

ARXIV_CATEGORIES = [
    ("cs.AI", "Artificial intelligence"),
    ("cs.CL", "Computation and language"),
    ("cs.LG", "Machine learning"),
    ("cs.CV", "Computer vision"),
    ("cs.CR", "Cryptography and security"),
    ("cs.SE", "Software engineering"),
]

# Projects whose GitHub release feeds are checked (public Atom feeds, no API).
RELEASE_WATCH = [
    "ollama/ollama", "ggml-org/llama.cpp", "vllm-project/vllm",
    "huggingface/transformers", "pytorch/pytorch", "langchain-ai/langchain",
    "openai/openai-python", "anthropics/anthropic-sdk-python",
    "modelcontextprotocol/typescript-sdk", "modelcontextprotocol/python-sdk",
    "open-webui/open-webui", "n8n-io/n8n", "microsoft/vscode", "nodejs/node",
    "denoland/deno", "oven-sh/bun", "vercel/next.js", "facebook/react",
    "astral-sh/uv", "astral-sh/ruff", "kubernetes/kubernetes", "docker/compose",
    "hashicorp/terraform", "grafana/grafana", "supabase/supabase",
    "tailwindlabs/tailwindcss", "rust-lang/rust", "home-assistant/core",
]

PYPI_WATCH = [
    "openai", "anthropic", "mcp", "langchain", "transformers", "torch", "vllm",
    "litellm", "llama-index", "crewai", "fastapi", "pydantic", "uv", "polars",
]

NEWS_FEEDS = [
    ("techmeme", "Techmeme", "https://www.techmeme.com/feed.xml", "pulse"),
    ("verge", "The Verge", "https://www.theverge.com/rss/index.xml", "pulse"),
    ("techcrunch", "TechCrunch", "https://techcrunch.com/feed/", "pulse"),
    ("ars", "Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab", "pulse"),
    ("lwn", "LWN.net", "https://lwn.net/headlines/rss", "devops-cloud"),
    ("thn", "The Hacker News", "https://feeds.feedburner.com/TheHackersNews", "security"),
    ("bleeping", "BleepingComputer", "https://www.bleepingcomputer.com/feed/", "security"),
    ("ghchangelog", "GitHub Changelog", "https://github.blog/changelog/feed/", "devtools"),
    ("simonw", "Simon Willison", "https://simonwillison.net/atom/everything/", "ai-llms"),
]

LAB_FEEDS = [
    ("openai_news", "OpenAI News", "https://openai.com/news/rss.xml"),
    ("google_ai", "Google AI blog", "https://blog.google/technology/ai/rss/"),
    ("deepmind", "Google DeepMind blog", "https://deepmind.google/blog/rss.xml"),
    ("hf_blog", "Hugging Face blog", "https://huggingface.co/blog/feed.xml"),
]

STATUS_PAGES = [
    ("githubstatus", "GitHub", "https://www.githubstatus.com/api/v2/incidents.json"),
    ("cloudflarestatus", "Cloudflare", "https://www.cloudflarestatus.com/api/v2/incidents.json"),
]

NICHES = [
    {"slug": "ai-llms", "emoji": "🤖", "title": "AI & LLMs",
     "intro": "Models, labs, inference tools and the work around large language models."},
    {"slug": "agents-mcp", "emoji": "🧠", "title": "Agents & MCP",
     "intro": "Agent frameworks, skills, sandboxes and Model Context Protocol servers."},
    {"slug": "research", "emoji": "📄", "title": "Research & papers",
     "intro": "New papers from arXiv and the Hugging Face daily papers page."},
    {"slug": "devtools", "emoji": "🧰", "title": "Dev tools",
     "intro": "Editors, CLIs, package ecosystems, languages and other tools for building software."},
    {"slug": "web", "emoji": "🌐", "title": "Web",
     "intro": "Web platforms, front-end frameworks, browsers and writing about the web."},
    {"slug": "mobile", "emoji": "📱", "title": "Mobile",
     "intro": "iOS, Android, cross-platform apps and app-store work."},
    {"slug": "devops-cloud", "emoji": "☁️", "title": "DevOps & Cloud",
     "intro": "Infrastructure, containers, CI/CD, self-hosting, outages and cloud operations."},
    {"slug": "security", "emoji": "🔒", "title": "Security",
     "intro": "Exploited and newly published vulnerabilities, advisories and security tools."},
    {"slug": "data", "emoji": "📊", "title": "Data",
     "intro": "Databases, datasets, pipelines and data tooling."},
    {"slug": "pulse", "emoji": "🌍", "title": "Tech news & public pulse",
     "intro": "Tech headlines plus what the wider public is searching, reading and posting."},
]
NICHE_BY_SLUG = {n["slug"]: n for n in NICHES}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def now_berlin() -> datetime:
    return datetime.now(BERLIN)


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%-d %B %Y")


def fmt_time(dt: datetime) -> str:
    hours = int(dt.utcoffset().total_seconds() // 3600)
    offset = f"UTC+{hours}" if hours >= 0 else f"UTC{hours}"
    return f"{dt.strftime('%H:%M')} Europe/Berlin ({offset})"


def fmt_hm(dt: datetime | None) -> str:
    return dt.astimezone(BERLIN).strftime("%H:%M") if dt else "—"


def fmt_day(dt: datetime | None) -> str:
    """Short Berlin date, e.g. '19 Nov 14:05'."""
    if not dt:
        return "—"
    return dt.astimezone(BERLIN).strftime("%-d %b %H:%M")


def fmt_int(n: Any) -> str:
    if n is None or n == "":
        return "—"
    if isinstance(n, str):
        raw = n.replace(",", "").strip()
        if not re.fullmatch(r"-?\d+", raw):
            return n
        n = int(raw)
    if isinstance(n, float) and not n.is_integer():
        return f"{n:,.1f}"
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return str(n)


def fmt_compact(n: Any) -> str:
    """1234567 -> 1.2M. Only for display of real numbers."""
    if n is None or n == "":
        return "—"
    try:
        v = float(n)
    except (TypeError, ValueError):
        return str(n)
    for div, suf in ((1e9, "B"), (1e6, "M"), (1e3, "k")):
        if abs(v) >= div:
            s = f"{v / div:.1f}".rstrip("0").rstrip(".")
            return f"{s}{suf}"
    return f"{int(v):,}"


def parse_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    s = str(value).replace(",", "").replace("\xa0", "").strip()
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return None


def parse_dt(value: Any) -> datetime | None:
    """Parse ISO 8601, RFC 822 or epoch seconds into an aware datetime."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    s = str(value).strip()
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    try:
        dt = parsedate_to_datetime(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError, IndexError):
        pass
    for fmt in ("%b %d, %Y, %I:%M:%S %p",):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", htmlmod.unescape(text)).strip()


def clip(text: str, n: int = 110) -> str:
    text = re.sub(r"\s+", " ", (text or "")).strip()
    if len(text) <= n:
        return text
    cut = text[: n - 1].rsplit(" ", 1)[0].rstrip(" ,.;:-–—(")
    return cut + "…"


def md_escape(text: Any) -> str:
    s = "" if text is None else str(text)
    s = s.replace("\r", " ").replace("\n", " ")
    s = s.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
    return s.strip()


def md_link(label: str, url: str) -> str:
    label = md_escape(label).replace("[", "\\[").replace("]", "\\]")
    if not url:
        return label
    url = url.replace(" ", "%20").replace(")", "%29").replace("(", "%28")
    return f"[{label}]({url})"


def domain_of(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def canonical_url(url: str) -> str:
    """Key used to spot the same item across sources."""
    if not url:
        return ""
    u = url.strip()
    u = re.sub(r"^http://", "https://", u)
    u = re.sub(r"^https://(www\.|m\.)", "https://", u)
    u = u.split("#", 1)[0]
    m = re.match(r"https://github\.com/([^/]+)/([^/?#]+)", u)
    if m:
        return f"https://github.com/{m.group(1).lower()}/{m.group(2).lower()}"
    m = re.match(r"https://(?:arxiv\.org/(?:abs|pdf)|huggingface\.co/papers)/(\d{4}\.\d{4,5})", u)
    if m:
        return f"arxiv:{m.group(1)}"
    u = re.sub(r"[?&](utm_[a-z]+|ref|source)=[^&]*", "", u)
    return u.rstrip("/?").lower()


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def within(dt: datetime | None, hours: float, ref: datetime) -> bool:
    return bool(dt) and (ref - dt) <= timedelta(hours=hours)


# ---------------------------------------------------------------------------
# HTTP: timeouts, one retry, per-host spacing, global time budget
# ---------------------------------------------------------------------------

_HOST_GAP = {
    "export.arxiv.org": 3.1,     # arXiv asks for 3 seconds between calls
    "api.github.com": 1.0,
    "github.com": 0.5,
    "pypistats.org": 0.6,
    "services.nvd.nist.gov": 6.5,  # NVD: 5 requests per 30 seconds without a key
}
_host_lock = threading.Lock()
_host_next: dict[str, float] = {}
_host_locks: dict[str, threading.Lock] = {}
DEADLINE = [time.monotonic() + TOTAL_BUDGET]


class FetchError(Exception):
    pass


def _host_slot(host: str) -> None:
    gap = _HOST_GAP.get(host, 0.25)
    with _host_lock:
        lock = _host_locks.setdefault(host, threading.Lock())
    with lock:
        wait_s = _host_next.get(host, 0) - time.monotonic()
        if wait_s > 0:
            time.sleep(wait_s)
        _host_next[host] = time.monotonic() + gap


def fetch(url: str, accept: str | None = None, data: bytes | None = None,
          headers: dict | None = None) -> str:
    """GET (or POST when data is given). Raises FetchError with a short reason."""
    host = urlparse(url).netloc
    hdrs = {"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"}
    if accept:
        hdrs["Accept"] = accept
    if headers:
        hdrs.update(headers)
    last = "unknown error"
    for attempt in range(RETRIES + 1):
        remaining = DEADLINE[0] - time.monotonic()
        if remaining <= 1:
            raise FetchError("run time budget used up")
        _host_slot(host)
        req = Request(url, data=data, headers=hdrs)
        try:
            with urlopen(req, timeout=min(REQUEST_TIMEOUT, remaining)) as resp:
                raw = resp.read()
                if raw[:2] == b"\x1f\x8b":
                    raw = gzip.decompress(raw)
                charset = resp.headers.get_content_charset() or "utf-8"
                return raw.decode(charset, errors="replace")
        except HTTPError as exc:
            last = f"HTTP {exc.code}"
            if exc.code == 429 and attempt < RETRIES:
                wait_s = parse_int(exc.headers.get("Retry-After")) or 0
                if 0 < wait_s <= 45 and DEADLINE[0] - time.monotonic() > wait_s + 5:
                    time.sleep(wait_s + 1)
                    continue
            if exc.code in (403, 429):
                body = ""
                try:
                    body = exc.read()[:300].decode("utf-8", "replace").lower()
                except Exception:
                    pass
                if "rate limit" in body or exc.code == 429:
                    last = f"HTTP {exc.code} (rate limited)"
                raise FetchError(last)
            if exc.code < 500:
                raise FetchError(last)
        except URLError as exc:
            last = f"network error ({exc.reason})"
        except TimeoutError:
            last = "timed out"
        except Exception as exc:  # fail soft on anything odd
            last = f"{type(exc).__name__}: {exc}"
        if attempt < RETRIES:
            time.sleep(2)
    raise FetchError(last)


def fetch_json(url: str, **kw) -> Any:
    body = fetch(url, accept="application/json", **kw)
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise FetchError(f"invalid JSON ({exc.msg})")


def fetch_xml(url: str) -> ET.Element:
    body = fetch(url, accept="application/rss+xml, application/atom+xml, application/xml, text/xml")
    body = body.lstrip("\ufeff").strip()
    try:
        return ET.fromstring(body)
    except ET.ParseError as exc:
        raise FetchError(f"invalid XML ({exc})")


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_feed(root: ET.Element) -> list[dict]:
    """RSS 2.0, RSS 1.0 (RDF) or Atom into [{title, url, published, summary, author}]."""
    out = []
    for el in root.iter():
        name = _local(el.tag)
        if name not in ("item", "entry"):
            continue
        rec = {"title": "", "url": "", "published": None, "summary": "", "author": ""}
        for ch in el:
            cn = _local(ch.tag)
            text = (ch.text or "").strip()
            if cn == "title":
                rec["title"] = strip_html(text)
            elif cn == "link":
                href = ch.attrib.get("href")
                rel = ch.attrib.get("rel", "alternate")
                if href and rel == "alternate" and not rec["url"]:
                    rec["url"] = href
                elif text and not rec["url"]:
                    rec["url"] = text
            elif cn in ("pubDate", "published", "date") and not rec["published"]:
                rec["published"] = parse_dt(text)
            elif cn == "updated" and not rec.get("updated"):
                rec["updated"] = parse_dt(text)
            elif cn in ("description", "summary", "content") and not rec["summary"]:
                rec["summary"] = strip_html(text)
            elif cn in ("creator", "author"):
                nm = text or "".join((c.text or "") for c in ch if _local(c.tag) == "name")
                rec["author"] = nm.strip()
        if not rec["published"]:
            rec["published"] = rec.get("updated")
        if rec["title"] and rec["url"]:
            out.append(rec)
    return out


# ---------------------------------------------------------------------------
# Source registry
# ---------------------------------------------------------------------------

class SourceResult:
    def __init__(self, key: str, name: str, url: str):
        self.key = key
        self.name = name
        self.url = url
        self.ok = False
        self.items: list[dict] = []
        self.note = ""
        self.fetched_at: datetime | None = None
        self.elapsed = 0.0


SOURCES: list[tuple[str, str, str, Callable[[], tuple[list[dict], str]]]] = []


def source(key: str, name: str, url: str):
    def deco(fn):
        SOURCES.append((key, name, url, fn))
        return fn
    return deco


def item(kind: str, title: str, url: str, **fields) -> dict:
    d = {"kind": kind, "title": title, "url": url}
    d.update(fields)
    return d


# ---- GitHub -----------------------------------------------------------------

def parse_github_trending_html(text: str, period_word: str) -> list[dict]:
    repos = []
    for art in re.split(r'<article class="Box-row"', text)[1:]:
        h2 = re.search(r"<h2[\s\S]*?</h2>", art)
        if not h2:
            continue
        m = re.search(r'href="/(?P<owner>[^"/]+)/(?P<name>[^"/]+)"', h2.group(0))
        if not m:
            continue
        owner, name = m.group("owner"), m.group("name")
        dm = re.search(r'<p class="col-9 color-fg-muted[^"]*">\s*([\s\S]*?)\s*</p>', art)
        desc = strip_html(dm.group(1)) if dm else ""
        lm = re.search(r'itemprop="programmingLanguage">([^<]+)', art)
        stars = forks = None
        sm = re.search(rf'href="/{re.escape(owner)}/{re.escape(name)}/stargazers"[^>]*>([\s\S]*?)</a>', art)
        if sm:
            stars = parse_int(strip_html(sm.group(1)))
        fm = re.search(rf'href="/{re.escape(owner)}/{re.escape(name)}/forks"[^>]*>([\s\S]*?)</a>', art)
        if fm:
            forks = parse_int(strip_html(fm.group(1)))
        tm = re.search(rf"([0-9,]+)\s+stars?\s+{period_word}", art, re.I)
        slug = f"{owner}/{name}"
        repos.append(item(
            "repo", slug, f"https://github.com/{slug}", desc=desc,
            language=lm.group(1).strip() if lm else "", stars=stars, forks=forks,
            gained=parse_int(tm.group(1)) if tm else None,
        ))
    return repos


def _trending(path: str, period: str, word: str, limit: int) -> tuple[list[dict], str]:
    url = f"https://github.com/trending{path}?since={period}"
    repos = parse_github_trending_html(fetch(url), word)[:limit]
    if not repos:
        raise FetchError("trending page had no repository rows")
    return repos, f"{len(repos)} repos in the order GitHub shows them"


@source("gh_daily", "GitHub trending · today", "https://github.com/trending?since=daily")
def src_gh_daily():
    return _trending("", "daily", "today", 25)


@source("gh_weekly", "GitHub trending · this week", "https://github.com/trending?since=weekly")
def src_gh_weekly():
    return _trending("", "weekly", "this week", 15)


def _make_lang_source(slug: str, label: str):
    @source(f"gh_{slug}", f"GitHub trending · {label}", f"https://github.com/trending/{slug}?since=daily")
    def _src():
        return _trending(f"/{slug}", "daily", "today", 10)
    return _src


for _slug, _label in GITHUB_LANGUAGES:
    _make_lang_source(_slug, _label)


def github_search(q: str, per_page: int = 30, sort: str = "", order: str = "desc") -> list[dict]:
    params = {"q": q, "per_page": per_page}
    if sort:
        params.update({"sort": sort, "order": order})
    data = fetch_json("https://api.github.com/search/repositories?" + urlencode(params),
                      headers={"Accept": "application/vnd.github+json"})
    if not isinstance(data, dict) or "items" not in data:
        raise FetchError(str((data or {}).get("message", "unexpected response"))[:80])
    return data["items"]


def repo_from_api(r: dict) -> dict:
    lic = (r.get("license") or {}).get("spdx_id")
    if lic in (None, "NOASSERTION"):
        lic = (r.get("license") or {}).get("name") and "Other"
    return item(
        "repo", r["full_name"], r["html_url"], desc=r.get("description") or "",
        language=r.get("language") or "", stars=r.get("stargazers_count"),
        forks=r.get("forks_count"), license=lic or "", topics=r.get("topics") or [],
        created=parse_dt(r.get("created_at")), pushed=parse_dt(r.get("pushed_at")),
    )


@source("gh_new", "GitHub · new repos gaining stars (created in the last 7 days)",
        "https://docs.github.com/en/rest/search/search#search-repositories")
def src_gh_new():
    since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    rows = github_search(f"created:>{since} fork:false archived:false", 40, sort="stars")
    out = []
    for r in rows:
        rec = repo_from_api(r)
        # Freshly created repos with no licence or description are often star-farmed
        # bait; keep only repos that state both.
        if not rec["license"] or not rec["desc"]:
            continue
        out.append(rec)
    out = out[:15]
    return out, f"GitHub search API, sorted by stars; {len(out)} repos that state a licence and a description"


@source("maintainer", "Maintainer repos (not a ranking)", f"https://github.com/{REPO_OWNER}")
def src_maintainer():
    rows = github_search(" ".join(f"repo:{r}" for r in MAINTAINER_REPOS), 10)
    order = {r.lower(): i for i, r in enumerate(MAINTAINER_REPOS)}
    out = sorted((repo_from_api(r) for r in rows), key=lambda x: order.get(x["title"].lower(), 99))
    return out, "GitHub search API, repo: qualifiers"


def enrich_repos(results: dict[str, SourceResult]) -> str:
    """Add licence and topics to trending repos with batched search calls."""
    slugs: list[str] = []
    for key, res in results.items():
        if key.startswith("gh_") and key != "gh_new" and res.ok:
            for it in res.items:
                if it["title"] not in slugs:
                    slugs.append(it["title"])
    if not slugs:
        return "nothing to enrich"
    found: dict[str, dict] = {}
    errors = []
    for i in range(0, len(slugs), 25):
        batch = slugs[i:i + 25]
        try:
            for r in github_search(" ".join(f"repo:{s}" for s in batch), 100):
                found[r["full_name"].lower()] = r
        except FetchError as exc:
            errors.append(str(exc))
            break
    for key, res in results.items():
        if key.startswith("gh_") and key != "gh_new":
            for it in res.items:
                r = found.get(it["title"].lower())
                if r:
                    api = repo_from_api(r)
                    it["license"] = api["license"]
                    it["topics"] = api["topics"]
                    if not it.get("desc"):
                        it["desc"] = api["desc"]
    note = f"licence and topics added for {len(found)} of {len(slugs)} repos via the GitHub search API"
    if errors:
        note += f" (stopped: {errors[0]})"
    return note


# ---- Hacker News (Algolia search API; official HN data) --------------------

def _hn(params: dict, limit: int) -> list[dict]:
    data = fetch_json("https://hn.algolia.com/api/v1/search?" + urlencode(params))
    out = []
    for h in data.get("hits", [])[:limit]:
        oid = h.get("objectID")
        disc = f"https://news.ycombinator.com/item?id={oid}"
        url = h.get("url") or disc
        out.append(item(
            "hn", h.get("title") or "", url, points=h.get("points"),
            comments=h.get("num_comments"), domain=domain_of(h.get("url") or "") or "news.ycombinator.com",
            discuss=disc, author=h.get("author"), created=parse_dt(h.get("created_at_i")),
        ))
    return out


@source("hn_front", "Hacker News · front page", "https://news.ycombinator.com/")
def src_hn_front():
    out = _hn({"tags": "front_page", "hitsPerPage": 30}, 30)
    out.sort(key=lambda x: x.get("points") or 0, reverse=True)
    return out[:20], "Algolia HN API, front_page tag, sorted by points"


def _since(hours: int) -> int:
    return int(time.time()) - hours * 3600


@source("hn_show", "Hacker News · Show HN (last 24 h)", "https://news.ycombinator.com/show")
def src_hn_show():
    out = _hn({"tags": "show_hn", "numericFilters": f"created_at_i>{_since(24)},points>5", "hitsPerPage": 50}, 50)
    out.sort(key=lambda x: x.get("points") or 0, reverse=True)
    return out[:10], "Algolia HN API, show_hn posts from the last 24 h, sorted by points"


@source("hn_ask", "Hacker News · Ask HN (last 24 h)", "https://news.ycombinator.com/ask")
def src_hn_ask():
    out = _hn({"tags": "ask_hn", "numericFilters": f"created_at_i>{_since(24)}", "hitsPerPage": 50}, 50)
    out.sort(key=lambda x: (x.get("comments") or 0), reverse=True)
    return out[:8], "Algolia HN API, ask_hn posts from the last 24 h, sorted by comments"


@source("hn_best", "Hacker News · best of the week", "https://news.ycombinator.com/best")
def src_hn_best():
    out = _hn({"tags": "story", "numericFilters": f"created_at_i>{_since(168)},points>300", "hitsPerPage": 100}, 100)
    out.sort(key=lambda x: x.get("points") or 0, reverse=True)
    return out[:10], "Algolia HN API, stories from the last 7 days with 300+ points"


# ---- Hugging Face -------------------------------------------------------------

def _hf_license(tags: list[str]) -> str:
    for t in tags or []:
        if t.startswith("license:"):
            return t.split(":", 1)[1]
    return ""


@source("hf_models", "Hugging Face · trending models", "https://huggingface.co/models?sort=trending")
def src_hf_models():
    rows = fetch_json("https://huggingface.co/api/models?sort=trendingScore&limit=15")
    out = [item(
        "model", r["id"], f"https://huggingface.co/{r['id']}", task=r.get("pipeline_tag") or "",
        library=r.get("library_name") or "", downloads=r.get("downloads"), likes=r.get("likes"),
        license=_hf_license(r.get("tags")), created=parse_dt(r.get("createdAt")),
    ) for r in rows]
    return out, "Hub API sort=trendingScore; downloads are the Hub's last-30-days count"


@source("hf_spaces", "Hugging Face · trending Spaces", "https://huggingface.co/spaces?sort=trending")
def src_hf_spaces():
    rows = fetch_json("https://huggingface.co/api/spaces?sort=trendingScore&limit=12"
                      "&expand%5B%5D=cardData&expand%5B%5D=likes&expand%5B%5D=sdk")
    out = [item(
        "space", r["id"], f"https://huggingface.co/spaces/{r['id']}",
        desc=((r.get("cardData") or {}).get("short_description") or (r.get("cardData") or {}).get("title") or ""),
        sdk=r.get("sdk") or "", likes=r.get("likes"),
        license=(r.get("cardData") or {}).get("license") or "",
    ) for r in rows]
    return out, "Hub API sort=trendingScore"


@source("hf_datasets", "Hugging Face · trending datasets", "https://huggingface.co/datasets?sort=trending")
def src_hf_datasets():
    rows = fetch_json("https://huggingface.co/api/datasets?sort=trendingScore&limit=12")
    out = []
    for r in rows:
        tags = r.get("tags") or []
        tasks = [t.split(":", 1)[1] for t in tags if t.startswith("task_categories:")]
        out.append(item(
            "dataset", r["id"], f"https://huggingface.co/datasets/{r['id']}",
            desc=clip(strip_html(r.get("description") or ""), 90), downloads=r.get("downloads"),
            likes=r.get("likes"), license=_hf_license(tags), task=", ".join(tasks[:2]),
        ))
    return out, "Hub API sort=trendingScore; downloads are the Hub's last-30-days count"


@source("hf_papers", "Hugging Face · daily papers", "https://huggingface.co/papers")
def src_hf_papers():
    rows = fetch_json("https://huggingface.co/api/daily_papers?limit=50")
    out = []
    for r in rows:
        p = r.get("paper") or {}
        pid = p.get("id") or ""
        authors = [a.get("name") for a in p.get("authors", []) if a.get("name")]
        out.append(item(
            "paper", p.get("title") or r.get("title") or "", f"https://huggingface.co/papers/{pid}",
            arxiv=pid, authors=authors, upvotes=p.get("upvotes"), comments=r.get("numComments"),
            github=p.get("githubRepo") or "", github_stars=p.get("githubStars"),
            org=(r.get("organization") or {}).get("fullname") or "",
            published=parse_dt(p.get("publishedAt")), category="HF daily papers",
        ))
    out.sort(key=lambda x: x.get("upvotes") or 0, reverse=True)
    return out[:15], "daily_papers API, sorted by community upvotes"


# ---- arXiv ----------------------------------------------------------------------

ATOM = "{http://www.w3.org/2005/Atom}"


def _arxiv(cat: str, label: str, limit: int = 6) -> list[dict]:
    params = {"search_query": f"cat:{cat}", "sortBy": "submittedDate", "sortOrder": "descending",
              "max_results": limit}
    root = fetch_xml("https://export.arxiv.org/api/query?" + urlencode(params))
    out = []
    for e in root.findall(f"{ATOM}entry"):
        title = re.sub(r"\s+", " ", e.findtext(f"{ATOM}title") or "").strip()
        aid = (e.findtext(f"{ATOM}id") or "").rsplit("/abs/", 1)[-1]
        aid_base = re.sub(r"v\d+$", "", aid)
        authors = [a.findtext(f"{ATOM}name") for a in e.findall(f"{ATOM}author")]
        prim = e.find("{http://arxiv.org/schemas/atom}primary_category")
        out.append(item(
            "paper", title, f"https://arxiv.org/abs/{aid_base}", arxiv=aid_base,
            authors=[a for a in authors if a], category=(prim.attrib.get("term") if prim is not None else cat),
            published=parse_dt(e.findtext(f"{ATOM}published")),
            desc=clip(re.sub(r"\s+", " ", e.findtext(f"{ATOM}summary") or ""), 160),
        ))
    return out


@source("arxiv", "arXiv · newest by category", "https://arxiv.org/")
def src_arxiv():
    out, failed = [], []
    for cat, label in ARXIV_CATEGORIES:
        try:
            out.extend(_arxiv(cat, label))
        except FetchError as exc:
            failed.append(f"{cat}: {exc}")
    if not out:
        raise FetchError("; ".join(failed) or "no entries")
    note = "export API, newest submissions in " + ", ".join(c for c, _ in ARXIV_CATEGORIES)
    if failed:
        note += " (skipped " + "; ".join(failed) + ")"
    return out, note


# ---- Agents & MCP -----------------------------------------------------------------

@source("mcp_registry", "MCP Registry · new and updated servers (24 h)", "https://registry.modelcontextprotocol.io/")
def src_mcp_registry():
    since = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    seen: dict[str, dict] = {}
    page_token = None
    total = 0
    for _ in range(5):
        params = {"limit": 100, "updated_since": since}
        if page_token:
            params["cursor"] = page_token
        data = fetch_json("https://registry.modelcontextprotocol.io/v0/servers?" + urlencode(params))
        for row in data.get("servers", []):
            total += 1
            s = row.get("server") or {}
            meta = (row.get("_meta") or {}).get("io.modelcontextprotocol.registry/official") or {}
            name = s.get("name") or ""
            repo = (s.get("repository") or {}).get("url") or ""
            rec = item(
                "mcp", s.get("title") or name, repo or s.get("websiteUrl") or
                f"https://registry.modelcontextprotocol.io/v0/servers?search={quote(name)}",
                name=name, desc=s.get("description") or "", version=s.get("version") or "",
                published=parse_dt(meta.get("publishedAt") or meta.get("updatedAt")),
                remote=bool(s.get("remotes")), packages=[p.get("registryType") for p in s.get("packages") or []],
            )
            prev = seen.get(name)
            if not prev or (rec["published"] or datetime.min.replace(tzinfo=timezone.utc)) > (
                    prev["published"] or datetime.min.replace(tzinfo=timezone.utc)):
                seen[name] = rec
        page_token = (data.get("metadata") or {}).get("nextCursor")
        if not page_token:
            break
    out = sorted(seen.values(), key=lambda x: x["published"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    # Prefer servers that link a source repository.
    out = [o for o in out if "github.com" in o["url"]][:12] or out[:12]
    return out, f"official registry API, {len(seen)} distinct servers published or updated in the last 24 h"


@source("smithery", "Smithery · most-used MCP servers", "https://smithery.ai/")
def src_smithery():
    data = fetch_json("https://registry.smithery.ai/servers?pageSize=50")
    rows = data.get("servers", [])
    out = [item(
        "mcp", r.get("displayName") or r.get("qualifiedName"), f"https://smithery.ai/server/{r.get('qualifiedName')}",
        name=r.get("qualifiedName"), desc=strip_html(r.get("description") or ""), uses=r.get("useCount"),
        verified=r.get("verified"), remote=r.get("remote"),
    ) for r in rows if r.get("qualifiedName")]
    out.sort(key=lambda x: x.get("uses") or 0, reverse=True)
    total = (data.get("pagination") or {}).get("totalCount")
    return out[:10], f"public registry API, first 50 listed servers sorted by use count ({fmt_int(total)} servers listed)"


# ---- AI models and labs ------------------------------------------------------------

@source("openrouter", "OpenRouter · newest models", "https://openrouter.ai/models")
def src_openrouter():
    data = fetch_json("https://openrouter.ai/api/v1/models")
    rows = sorted(data.get("data", []), key=lambda r: r.get("created") or 0, reverse=True)
    out, seen = [], set()
    for r in rows:
        base = (r.get("id") or "").split(":", 1)[0]
        if base in seen:
            continue
        seen.add(base)
        pr = r.get("pricing") or {}

        def per_m(v):
            try:
                return round(float(v) * 1_000_000, 3)
            except (TypeError, ValueError):
                return None
        out.append(item(
            "llm", r.get("name") or base, f"https://openrouter.ai/{base}", model_id=base,
            context=r.get("context_length"), price_in=per_m(pr.get("prompt")), price_out=per_m(pr.get("completion")),
            created=parse_dt(r.get("created")),
            modality=((r.get("architecture") or {}).get("modality") or ""),
        ))
        if len(out) >= 10:
            break
    return out, f"public models API ({len(data.get('data', []))} models listed), newest first; prices in USD per 1M tokens"


def _feed_source(key, name, url, kind, hours, limit, niche=None):
    @source(key, name, url)
    def _src():
        entries = parse_feed(fetch_xml(url))
        ref = datetime.now(timezone.utc)
        recent = [e for e in entries if e["published"] and within(e["published"], hours, ref)]
        recent.sort(key=lambda e: e["published"], reverse=True)
        out = [item(kind, e["title"], e["url"], outlet=name.split(" · ")[0], published=e["published"],
                    desc=clip(e["summary"], 140), author=e["author"], niche=niche) for e in recent[:limit]]
        return out, f"feed, items from the last {hours} h ({len(recent)} found)"
    return _src


for _k, _n, _u in LAB_FEEDS:
    _feed_source(_k, _n, _u, "lab", 24 * 7, 4, "ai-llms")


# ---- Packages -------------------------------------------------------------------------

def _npm(keyword: str, size: int = 10) -> list[dict]:
    data = fetch_json("https://registry.npmjs.org/-/v1/search?" + urlencode({"text": f"keywords:{keyword}", "size": size}))
    out = []
    for o in data.get("objects", []):
        p = o.get("package") or {}
        out.append(item(
            "package", p.get("name"), (p.get("links") or {}).get("npm") or f"https://www.npmjs.com/package/{p.get('name')}",
            ecosystem="npm", version=p.get("version"), weekly=(o.get("downloads") or {}).get("weekly"),
            published=parse_dt(p.get("date")), license=p.get("license") or "", desc=p.get("description") or "",
            keyword=keyword,
        ))
    return out


@source("npm", "npm · top packages for MCP, AI agents and LLMs", "https://www.npmjs.com/")
def src_npm():
    out, seen = [], set()
    for kw in ("mcp", "ai-agent", "llm"):
        for p in _npm(kw):
            if p["title"] not in seen:
                seen.add(p["title"])
                out.append(p)
    out.sort(key=lambda x: x.get("weekly") or 0, reverse=True)
    return out[:20], "registry search API, keywords mcp, ai-agent and llm; weekly downloads as npm reports them"


@source("pypi", "PyPI · latest releases of key AI and Python packages", "https://pypi.org/")
def src_pypi():
    out, failed = [], []
    for name in PYPI_WATCH:
        try:
            d = fetch_json(f"https://pypi.org/pypi/{name}/json")
        except FetchError as exc:
            failed.append(name)
            continue
        info = d.get("info") or {}
        ver = info.get("version")
        files = (d.get("releases") or {}).get(ver) or d.get("urls") or []
        up = min((parse_dt(f.get("upload_time_iso_8601")) for f in files if f.get("upload_time_iso_8601")), default=None)
        weekly = None
        try:
            st = fetch_json(f"https://pypistats.org/api/packages/{name.lower()}/recent")
            weekly = (st.get("data") or {}).get("last_week")
        except FetchError:
            pass
        out.append(item(
            "package", info.get("name") or name, f"https://pypi.org/project/{name}/", ecosystem="PyPI",
            version=ver, published=up, weekly=weekly, desc=info.get("summary") or "",
            license=(info.get("license_expression") or (info.get("license") or "")[:30]),
        ))
    if not out:
        raise FetchError("no package responded")
    out.sort(key=lambda x: x["published"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    note = "PyPI JSON API for versions; weekly downloads from pypistats.org"
    if failed:
        note += f" (no data for {', '.join(failed)})"
    return out, note


@source("crates", "crates.io · most downloaded recently", "https://crates.io/")
def src_crates():
    d = fetch_json("https://crates.io/api/v1/summary")
    out = []
    for group, label in (("most_recently_downloaded", "recent"), ("new_crates", "new"), ("just_updated", "updated")):
        for c in d.get(group, [])[:8]:
            out.append(item(
                "package", c.get("name"), f"https://crates.io/crates/{c.get('name')}", ecosystem="crates.io",
                version=c.get("newest_version") or c.get("max_version"), recent=c.get("recent_downloads"),
                downloads=c.get("downloads"), desc=c.get("description") or "", group=label,
                published=parse_dt(c.get("updated_at")),
            ))
    return out, "summary API; 'recent downloads' is crates.io's 90-day count"


@source("jsdelivr", "jsDelivr · top npm packages by CDN hits this week", "https://www.jsdelivr.com/statistics")
def src_jsdelivr():
    rows = fetch_json("https://data.jsdelivr.com/v1/stats/packages?" + urlencode({"period": "week", "type": "npm", "limit": 15}))
    out = []
    for r in rows:
        hits, prev = r.get("hits"), (r.get("prev") or {}).get("hits")
        change = round((hits - prev) / prev * 100, 1) if hits and prev else None
        out.append(item("cdn", r.get("name"), f"https://www.jsdelivr.com/package/npm/{r.get('name')}",
                        hits=hits, change=change))
    return out, "public data API, period=week; change is against the previous week"


@source("dockerhub", "Docker Hub · official images updated in the last 48 h", "https://hub.docker.com/search?badges=official")
def src_dockerhub():
    d = fetch_json("https://hub.docker.com/v2/repositories/library/?" + urlencode({"page_size": 50, "ordering": "last_updated"}))
    ref = datetime.now(timezone.utc)
    out = []
    for r in d.get("results", []):
        upd = parse_dt(r.get("last_updated"))
        if not within(upd, 48, ref):
            continue
        out.append(item("image", r.get("name"), f"https://hub.docker.com/_/{r.get('name')}",
                        pulls=r.get("pull_count"), stars=r.get("star_count"), published=upd,
                        desc=r.get("description") or ""))
    out.sort(key=lambda x: x.get("pulls") or 0, reverse=True)
    return out[:12], "Hub API, library namespace ordered by last update, sorted by total pulls"


@source("releases", "GitHub releases · major projects (last 72 h)", "https://github.com/")
def src_releases():
    ref = datetime.now(timezone.utc)
    out, failed = [], 0
    for slug in RELEASE_WATCH:
        try:
            entries = parse_feed(fetch_xml(f"https://github.com/{slug}/releases.atom"))
        except FetchError:
            failed += 1
            continue
        kept = 0
        for e in entries[:5]:
            if kept >= 2:
                break
            if re.search(r"/tag/(viable|ciflow|nightly|trunk)", e["url"]):
                continue
            if within(e["published"], 72, ref):
                kept += 1
                tag = e["url"].rsplit("/tag/", 1)[-1] if "/tag/" in e["url"] else e["title"]
                out.append(item("release", f"{slug} {e['title']}", e["url"], project=slug, tag=tag,
                                release_title=e["title"], published=e["published"],
                                prerelease=bool(re.search(r"(rc|alpha|beta|preview|nightly|canary|dev)", tag, re.I))))
    if failed == len(RELEASE_WATCH):
        raise FetchError("no release feed responded")
    out.sort(key=lambda x: x["published"], reverse=True)
    note = f"public releases.atom feeds of {len(RELEASE_WATCH)} projects"
    if failed:
        note += f" ({failed} feeds did not respond)"
    return out, note


# ---- Security ---------------------------------------------------------------------------

@source("kev", "CISA KEV · known exploited vulnerabilities (last 14 days)",
        "https://www.cisa.gov/known-exploited-vulnerabilities-catalog")
def src_kev():
    d = fetch_json("https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json")
    ref = now_berlin().date()
    out = []
    for v in d.get("vulnerabilities", []):
        try:
            added = datetime.strptime(v["dateAdded"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            continue
        if (ref - added).days > 14:
            continue
        cve = v.get("cveID")
        out.append(item(
            "kev", cve, f"https://nvd.nist.gov/vuln/detail/{cve}", vendor=v.get("vendorProject"),
            product=v.get("product"), name=v.get("vulnerabilityName"), added=v.get("dateAdded"),
            due=v.get("dueDate"), ransomware=v.get("knownRansomwareCampaignUse"),
            desc=v.get("shortDescription") or "",
        ))
    out.sort(key=lambda x: x["added"], reverse=True)
    return out[:20], f"catalog version {d.get('catalogVersion')}, {fmt_int(d.get('count'))} entries in total"


def _nvd_score(metrics: dict) -> tuple[float | None, str, str]:
    for key, ver in (("cvssMetricV40", "4.0"), ("cvssMetricV31", "3.1"), ("cvssMetricV30", "3.0")):
        for m in metrics.get(key) or []:
            data = m.get("cvssData") or {}
            if data.get("baseScore") is not None:
                return data.get("baseScore"), data.get("baseSeverity") or "", ver
    return None, "", ""


@source("nvd", "NVD · critical CVEs published in the last 48 h", "https://nvd.nist.gov/vuln/search")
def src_nvd():
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=48)
    fmt = "%Y-%m-%dT%H:%M:%S.000"
    out, total = [], 0
    for sev in ("CRITICAL",):
        params = {"pubStartDate": start.strftime(fmt), "pubEndDate": end.strftime(fmt),
                  "cvssV3Severity": sev, "resultsPerPage": 40}
        d = fetch_json("https://services.nvd.nist.gov/rest/json/cves/2.0?" + urlencode(params))
        total += d.get("totalResults") or 0
        for v in d.get("vulnerabilities", []):
            c = v.get("cve") or {}
            score, severity, ver = _nvd_score(c.get("metrics") or {})
            vendors = []
            for conf in c.get("configurations") or []:
                for node in conf.get("nodes") or []:
                    for cm in node.get("cpeMatch") or []:
                        parts = (cm.get("criteria") or "").split(":")
                        if len(parts) > 4 and parts[3] not in vendors:
                            vendors.append(parts[3])
            desc = next((x.get("value") for x in c.get("descriptions", []) if x.get("lang") == "en"), "")
            out.append(item(
                "cve", c.get("id"), f"https://nvd.nist.gov/vuln/detail/{c.get('id')}", score=score,
                severity=severity, cvss=ver, vendor=", ".join(vendors[:2]), assigner=c.get("sourceIdentifier") or "",
                published=parse_dt(c.get("published")), desc=clip(desc, 150),
            ))
    out.sort(key=lambda x: (x.get("score") or 0, x["published"] or end), reverse=True)
    return out[:15], f"CVE API 2.0, {total} CVEs with a CVSS v3 severity of CRITICAL published in the window"


@source("euvd", "ENISA EUVD · latest vulnerabilities", "https://euvd.enisa.europa.eu/")
def src_euvd():
    rows = fetch_json("https://euvdservices.enisa.europa.eu/api/lastvulnerabilities")
    out = []
    for r in rows:
        aliases = [a.strip() for a in (r.get("aliases") or "").split("\n") if a.strip()]
        cve = next((a for a in aliases if a.startswith("CVE-")), "")
        vendors = [((v.get("vendor") or {}).get("name") or "") for v in r.get("enisaIdVendor") or []]
        products = [((p.get("product") or {}).get("name") or "") for p in r.get("enisaIdProduct") or []]
        eid = r.get("id")
        out.append(item(
            "euvd", eid, f"https://euvd.enisa.europa.eu/vulnerability/{eid}", cve=cve,
            score=r.get("baseScore"), cvss=r.get("baseScoreVersion"), vendor=", ".join(v for v in vendors if v)[:40],
            product=", ".join(p for p in products if p)[:40], epss=r.get("epss"),
            published=parse_dt(r.get("datePublished")), desc=clip(r.get("description") or "", 150),
        ))
    out.sort(key=lambda x: (x.get("score") or 0), reverse=True)
    return out[:12], "EU Vulnerability Database public API, sorted by base score"


# ---- Status pages -----------------------------------------------------------------------

def _status_source(key, name, url):
    @source(key, f"{name} status · incidents (last 72 h)", url.replace("/api/v2/incidents.json", ""))
    def _src():
        d = fetch_json(url)
        ref = datetime.now(timezone.utc)
        out = []
        for inc in d.get("incidents", []):
            started = parse_dt(inc.get("started_at") or inc.get("created_at"))
            if not within(started, 72, ref):
                continue
            out.append(item(
                "incident", inc.get("name"), inc.get("shortlink") or url.replace("/api/v2/incidents.json", ""),
                service=name, impact=inc.get("impact"), status=inc.get("status"), published=started,
                resolved=parse_dt(inc.get("resolved_at")),
                components=[c.get("name") for c in inc.get("components") or []][:3],
            ))
        return out[:10], "Statuspage public API"
    return _src


for _k, _n, _u in STATUS_PAGES:
    _status_source(_k, _n, _u)


# ---- Community ---------------------------------------------------------------------------

def _devto(params: dict) -> list[dict]:
    rows = fetch_json("https://dev.to/api/articles?" + urlencode(params))
    return [item(
        "post", r.get("title"), r.get("url"), outlet="Dev.to", reactions=r.get("public_reactions_count"),
        comments=r.get("comments_count"), tags=r.get("tag_list") or [], author=(r.get("user") or {}).get("name"),
        minutes=r.get("reading_time_minutes"), published=parse_dt(r.get("published_timestamp")),
    ) for r in rows]


@source("devto_day", "Dev.to · top today", "https://dev.to/top/day")
def src_devto_day():
    return _devto({"top": 1, "per_page": 10}), "Forem API top=1"


@source("devto_week", "Dev.to · top this week", "https://dev.to/top/week")
def src_devto_week():
    return _devto({"top": 7, "per_page": 10}), "Forem API top=7"


@source("lobsters", "Lobsters · hottest", "https://lobste.rs/")
def src_lobsters():
    rows = fetch_json("https://lobste.rs/hottest.json")
    return [item(
        "post", r.get("title"), r.get("url") or r.get("comments_url"), outlet="Lobsters", score=r.get("score"),
        comments=r.get("comment_count"), tags=r.get("tags") or [], discuss=r.get("comments_url"),
        domain=domain_of(r.get("url") or ""), published=parse_dt(r.get("created_at")),
    ) for r in rows[:15]], "official hottest.json"


@source("stackoverflow", "Stack Overflow · hot questions", "https://stackoverflow.com/questions?tab=Hot")
def src_stackoverflow():
    d = fetch_json("https://api.stackexchange.com/2.3/questions?" + urlencode(
        {"order": "desc", "sort": "hot", "site": "stackoverflow", "pagesize": 12}))
    out = [item(
        "question", strip_html(q.get("title") or ""), q.get("link"), score=q.get("score"),
        answers=q.get("answer_count"), views=q.get("view_count"), tags=q.get("tags") or [],
        answered=q.get("is_answered"), published=parse_dt(q.get("creation_date")),
    ) for q in d.get("items", [])]
    return out, f"Stack Exchange API 2.3, sort=hot (quota left today: {d.get('quota_remaining')})"


@source("producthunt", "Product Hunt · newest featured", "https://www.producthunt.com/")
def src_producthunt():
    entries = parse_feed(fetch_xml("https://www.producthunt.com/feed"))
    out = []
    for e in entries[:15]:
        tagline = re.sub(r"\s*Discussion\s*\|\s*Link\s*$", "", e["summary"]).strip()
        out.append(item("product", e["title"], e["url"].split("?", 1)[0], desc=tagline, author=e["author"],
                        published=e["published"]))
    return out, "public Atom feed (the feed carries no vote counts)"


# ---- News feeds ---------------------------------------------------------------------------

for _k, _n, _u, _niche in NEWS_FEEDS:
    _feed_source(_k, _n, _u, "news", 36, 6, _niche)


# ---- Public pulse ---------------------------------------------------------------------------

def _gtrends(geo: str) -> list[dict]:
    root = fetch_xml(f"https://trends.google.com/trending/rss?geo={geo}")
    ns = "{https://trends.google.com/trending/rss}"
    out = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        traffic = (it.findtext(f"{ns}approx_traffic") or "").strip()
        news = it.find(f"{ns}news_item")
        out.append(item(
            "search", title, "https://trends.google.com/trending?" + urlencode({"geo": geo}) + "&q=" + quote(title),
            geo=geo, traffic=traffic, published=parse_dt(it.findtext("pubDate")),
            news_title=(news.findtext(f"{ns}news_item_title") if news is not None else "") or "",
            news_url=(news.findtext(f"{ns}news_item_url") if news is not None else "") or "",
            news_source=(news.findtext(f"{ns}news_item_source") if news is not None else "") or "",
        ))
    return out


def _traffic_num(t: str) -> int:
    m = re.match(r"([\d,.]+)\s*([KkMm]?)", t or "")
    if not m:
        return 0
    n = float(m.group(1).replace(",", ""))
    return int(n * {"k": 1e3, "m": 1e6}.get(m.group(2).lower(), 1))


@source("gtrends", "Google Trends · daily searches (US and DE)", "https://trends.google.com/trending")
def src_gtrends():
    out = []
    for geo in ("US", "DE"):
        rows = _gtrends(geo)
        rows.sort(key=lambda x: _traffic_num(x["traffic"]), reverse=True)
        out.extend(rows[:10])
    return out, "Trending now RSS; search volume is Google's approximate bucket"


@source("wikipedia", "Wikipedia · most read yesterday (English)", "https://en.wikipedia.org/wiki/Special:TopViews")
def src_wikipedia():
    day = now_berlin() - timedelta(days=1)
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{day:%Y/%m/%d}"
    try:
        d = fetch_json(url)
    except FetchError:
        day = day - timedelta(days=1)
        d = fetch_json(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{day:%Y/%m/%d}")
    arts = (d.get("items") or [{}])[0].get("articles", [])
    out = []
    for a in arts:
        name = a.get("article") or ""
        if name == "Main_Page" or ":" in name:
            continue
        out.append(item("wiki", name.replace("_", " "), f"https://en.wikipedia.org/wiki/{quote(name)}",
                        views=a.get("views"), rank=a.get("rank")))
        if len(out) >= 15:
            break
    return out, f"Wikimedia pageviews API, {day:%-d %B %Y} (UTC day), main page and special pages left out"


@source("mastodon_tags", "Mastodon · trending hashtags (mastodon.social)", "https://mastodon.social/explore/tags")
def src_mastodon_tags():
    rows = fetch_json("https://mastodon.social/api/v1/trends/tags?limit=15")
    out = []
    for r in rows:
        hist = r.get("history") or []
        uses = sum(parse_int(h.get("uses")) or 0 for h in hist[:2])
        accounts = sum(parse_int(h.get("accounts")) or 0 for h in hist[:2])
        out.append(item("tag", f"#{r.get('name')}", r.get("url"), uses=uses, accounts=accounts))
    return out, "instance trends API; uses and accounts summed over the last two days"


@source("mastodon_links", "Mastodon · most shared links (mastodon.social)", "https://mastodon.social/explore/links")
def src_mastodon_links():
    rows = fetch_json("https://mastodon.social/api/v1/trends/links?limit=12")
    out = []
    for r in rows:
        hist = r.get("history") or []
        out.append(item("news", r.get("title"), r.get("url"), outlet=r.get("provider_name") or domain_of(r.get("url") or ""),
                        shares=sum(parse_int(h.get("uses")) or 0 for h in hist[:2]),
                        published=parse_dt(r.get("published_at")), niche="pulse"))
    return out, "instance trends API; shares summed over the last two days"


@source("bluesky", "Bluesky · trending topics", "https://bsky.app/")
def src_bluesky():
    d = fetch_json("https://public.api.bsky.app/xrpc/app.bsky.unspecced.getTrendingTopics?limit=15")
    out = []
    for t in d.get("topics", []):
        link = t.get("link") or ""
        out.append(item("topic", t.get("displayName") or t.get("topic"),
                        ("https://bsky.app" + link) if link.startswith("/") else link,
                        desc=t.get("description") or ""))
    return out, "public AppView API getTrendingTopics"


# ---------------------------------------------------------------------------
# X trends (reused from tables already stored in today's archive; no X call)
# ---------------------------------------------------------------------------

TECH_X_RE = re.compile(
    r"(?i)(\$[A-Z]{2,5}\b|\b(AI|A\.I\.|AGI|LLM|GPT|ChatGPT|OpenAI|Anthropic|Claude|Gemini|DeepMind|"
    r"Copilot|Nvidia|NVDA|AMD|Intel|Apple|iPhone|iPad|iOS|macOS|Android|Google|Alphabet|Microsoft|"
    r"Windows|Meta|Tesla|SpaceX|Starlink|Neuralink|xAI|Samsung|Pixel|Qualcomm|TSMC|chip|chips|"
    r"semiconductor|robot|robotics|crypto|Bitcoin|BTC|Ethereum|ETH|Solana|blockchain|hack|hacked|"
    r"breach|cyber|outage|AWS|Azure|Cloudflare|GitHub|Linux|startup|IPO|Nasdaq|app|apps|"
    r"PlayStation|PS5|Xbox|Nintendo|Switch 2|Steam|GTA ?(6|VI)|Grand Theft Auto|Rockstar|"
    r"YouTube|TikTok|Instagram|WhatsApp|Netflix|Spotify|Amazon|Huawei|Xiaomi|OnePlus|Vision Pro|"
    r"quantum|data center|datacenter)\b)"
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
            rows.append({
                "name": m.group(1) if m else parts[0], "url": m.group(2) if m else "",
                "posts": parts[1], "context": parts[2], "region": current,
            })
    if current:
        sections[current] = rows
    return {k: v for k, v in sections.items() if k in {"Worldwide", "Germany", "United States"}}


def load_x_trends(root: Path, today: datetime) -> tuple[dict[str, list[dict]], str]:
    """Reuse X trend tables already stored in today's archive (no new X fetch)."""
    day = today.strftime("%Y-%m-%d")
    candidates = [
        root / "archive" / today.strftime("%Y/%m") / f"{day}.md",
        root / "archive" / today.strftime("%Y/%m") / f"{day}.original.md",
    ]
    for path in candidates:
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            prefix = text.split(GENERATED_START)[0]
            sections = parse_x_tables(prefix)
            if sections:
                return sections, "reused the X trend tables stored in today's archive (no new X call)"
    return {}, "no X trend tables in today's archive yet"


def select_tech_on_x(x_sections: dict[str, list[dict]]) -> list[dict]:
    chosen: dict[str, dict] = {}
    region_pref = {"Worldwide": 3, "United States": 2, "Germany": 1}
    for region, rows in x_sections.items():
        for row in rows:
            ctx = row.get("context") or ""
            ctx_ok = "No independently confirmed context" not in ctx
            if not (TECH_X_RE.search(row["name"]) or (ctx_ok and TECH_X_RE.search(ctx))):
                continue
            key = row["name"].lower()
            score = (parse_int(row["posts"]) or -1, region_pref.get(region, 0))
            if key not in chosen or score > chosen[key]["_score"]:
                chosen[key] = dict(row, _score=score)
    items = sorted(chosen.values(), key=lambda r: r["_score"], reverse=True)
    for it in items:
        it.pop("_score", None)
    return items


# ---------------------------------------------------------------------------
# Niche routing (keyword rules, conservative)
# ---------------------------------------------------------------------------

NICHE_RULES = {
    "ai-llms": r"\b(ai|llms?|gpt|openai|anthropic|claude|gemini|llama|qwen|mistral|deepseek|transformers?|"
               r"diffusion|inference|fine-?tun\w*|machine learning|deep learning|neural|embedding\w*|rag|"
               r"vllm|ollama|pytorch|torch|tensorflow|text-generation|text-to-\w+|multimodal|vision-language|"
               r"chatbot|prompt\w*|tokens?|reasoning model|language model|hugging ?face|openvino|minimind)\b",
    "agents-mcp": r"\b(agents?|agentic|mcp|model context protocol|skills?|sandbox\w*|harness|claude code|codex|"
                  r"coding agent|autonomous|crewai|langgraph|tool[- ]calling|a2a|computer[- ]use)\b",
    "devtools": r"\b(cli|ide|editor|vs ?code|vim|neovim|emacs|plugin|sdk|compiler|debugg\w*|lint\w*|"
                r"terminal|git|github|package manager|npm|pypi|crates?|cargo|rust|golang|python|typescript|"
                r"javascript|zig|ruff|deno|node\.?js|refactor\w*|developers?|devtools?|programming|coding)\b",
    "web": r"\b(web|frontend|front-end|browser|css|html|react|next\.js|vue|svelte|angular|tailwind|"
           r"webassembly|wasm|http/?[23]?|chrome|firefox|safari|javascript|dom|web ?gpu|jsdelivr)\b",
    "mobile": r"\b(ios|ipados|android|iphone|ipad|app store|google play|mobile|react native|flutter|"
              r"swiftui|swift|kotlin|jetpack|xcode|testflight)\b",
    "devops-cloud": r"\b(devops|kubernetes|k8s|docker|containers?|helm|terraform|ansible|ci/?cd|aws|azure|gcp|"
                    r"cloud|serverless|nginx|linux|kernel|self-host\w*|homelab|observability|grafana|"
                    r"prometheus|sre|outage|incident|hetzner|cloudflare|infrastructure)\b",
    "security": r"\b(security|vulnerab\w*|cve-\d+|exploit\w*|malware|ransomware|phishing|breach\w*|"
                r"pentest\w*|red[- ]team|bug[- ]?bount\w*|bug hunt\w*|zero-day|0-day|backdoor|encryption|cryptography|"
                r"authentication bypass|xss|sqli|rce|privilege escalation|supply[- ]chain attack|cyber\w*|infosec|hacker\w*)\b",
    "data": r"\b(database|postgres\w*|sqlite|mysql|duckdb|clickhouse|polars|pandas|spark|kafka|airflow|"
            r"parquet|iceberg|etl|data pipeline|dataset|data engineering|vector (db|database)|analytics|olake)\b",
    "research": r"\b(paper|arxiv|benchmark|survey|we propose|state-of-the-art)\b",
}
NICHE_RE = {k: re.compile(v, re.I) for k, v in NICHE_RULES.items()}

SOURCE_NICHES = {
    "hf_models": ["ai-llms"], "hf_spaces": ["ai-llms"], "hf_datasets": ["data", "ai-llms"],
    "hf_papers": ["research", "ai-llms"], "arxiv": ["research"],
    "mcp_registry": ["agents-mcp"], "smithery": ["agents-mcp"], "openrouter": ["ai-llms"],
    "openai_news": ["ai-llms"], "google_ai": ["ai-llms"], "deepmind": ["ai-llms", "research"],
    "hf_blog": ["ai-llms"], "npm": ["devtools"], "pypi": ["devtools"], "crates": ["devtools"],
    "jsdelivr": ["web"], "dockerhub": ["devops-cloud"], "releases": [],
    "kev": ["security"], "nvd": ["security"], "euvd": ["security"],
    "githubstatus": ["devops-cloud"], "cloudflarestatus": ["devops-cloud"],
    "gtrends": ["pulse"], "wikipedia": ["pulse"], "mastodon_tags": ["pulse"],
    "mastodon_links": ["pulse"], "bluesky": ["pulse"],
}
# Text rules are not applied to these sources (their text is general news or search terms).
NO_TEXT_RULES = {"gtrends", "wikipedia", "mastodon_tags", "mastodon_links", "bluesky", "kev", "nvd", "euvd"}


def route(key: str, it: dict) -> list[str]:
    hits = set(SOURCE_NICHES.get(key, []))
    if it.get("niche"):
        hits.add(it["niche"])
    if key == "arxiv":
        cat = it.get("category", "")
        if cat in ("cs.AI", "cs.CL", "cs.LG", "cs.CV"):
            hits.add("ai-llms")
        elif cat == "cs.CR":
            hits.add("security")
        elif cat == "cs.SE":
            hits.add("devtools")
        return sorted(hits)
    if key in NO_TEXT_RULES:
        return sorted(hits)
    text = " ".join(str(x) for x in (
        it.get("title"), it.get("desc"), it.get("task"), it.get("language"),
        " ".join(it.get("topics") or []), " ".join(it.get("tags") or []), it.get("keyword"),
    ) if x)
    for slug, rx in NICHE_RE.items():
        if slug == "research" and key not in ("hn_front", "hn_best", "lobsters"):
            continue
        if rx.search(text):
            hits.add(slug)
    if key == "releases" and not hits:
        hits.add("devtools")
    return sorted(hits)


# ---------------------------------------------------------------------------
# Table renderers: one per item kind, used by README, archive and niche pages
# ---------------------------------------------------------------------------

def _topics(t: list[str], n: int = 3) -> str:
    return ", ".join(f"`{x}`" for x in (t or [])[:n]) or "—"


def _authors(a: list[str]) -> str:
    if not a:
        return "—"
    return md_escape(", ".join(a[:3]) + (f" +{len(a) - 3}" if len(a) > 3 else ""))


def _also(it: dict) -> str:
    also = it.get("_also") or []
    return f" <sub>also: {md_escape(', '.join(also))}</sub>" if also else ""


def _gained_label(key: str) -> str:
    return "Stars this week" if key == "gh_weekly" else ("Stars" if key in ("gh_new", "maintainer") else "Stars today")


def columns(kind: str, key: str):
    """Return (headers, row_fn). row_fn(item) -> list of cells (without the # column)."""
    if kind == "repo":
        if key in ("gh_new", "maintainer"):
            return (["Repository", "What it is", "Lang", "Licence", "Stars", "Created", "Topics"],
                    lambda i: [md_link(i["title"], i["url"]) + _also(i), md_escape(clip(i.get("desc"), 100)) or "—",
                               md_escape(i.get("language")) or "—", md_escape(i.get("license")) or "—",
                               fmt_int(i.get("stars")), fmt_day(i.get("created")).rsplit(" ", 1)[0], _topics(i.get("topics"))])
        return (["Repository", "What it is", "Lang", "Licence", "Stars", _gained_label(key), "Topics"],
                lambda i: [md_link(i["title"], i["url"]) + _also(i), md_escape(clip(i.get("desc"), 100)) or "—",
                           md_escape(i.get("language")) or "—", md_escape(i.get("license")) or "—",
                           fmt_int(i.get("stars")), fmt_int(i.get("gained")), _topics(i.get("topics"))])
    if kind == "hn":
        return (["Story", "Points", "Comments", "Site", "Discuss"],
                lambda i: [md_link(i["title"], i["url"]) + _also(i), fmt_int(i.get("points")), fmt_int(i.get("comments")),
                           md_escape(i.get("domain")) or "—", md_link("thread", i.get("discuss"))])
    if kind == "model":
        return (["Model", "Task", "Library", "Downloads (30 d)", "Likes", "Licence"],
                lambda i: [md_link(i["title"], i["url"]), md_escape(i.get("task")) or "—", md_escape(i.get("library")) or "—",
                           fmt_int(i.get("downloads")), fmt_int(i.get("likes")), md_escape(i.get("license")) or "—"])
    if kind == "space":
        return (["Space", "What it does", "SDK", "Likes", "Licence"],
                lambda i: [md_link(i["title"], i["url"]), md_escape(clip(i.get("desc"), 90)) or "—", md_escape(i.get("sdk")) or "—",
                           fmt_int(i.get("likes")), md_escape(i.get("license")) or "—"])
    if kind == "dataset":
        return (["Dataset", "Task", "Downloads (30 d)", "Likes", "Licence"],
                lambda i: [md_link(i["title"], i["url"]), md_escape(i.get("task")) or "—", fmt_int(i.get("downloads")),
                           fmt_int(i.get("likes")), md_escape(i.get("license")) or "—"])
    if kind == "paper" and key == "hf_papers":
        return (["Paper", "Authors", "Org", "Upvotes", "Code"],
                lambda i: [md_link(clip(i["title"], 110), i["url"]) + _also(i), _authors(i.get("authors")),
                           md_escape(i.get("org")) or "—", fmt_int(i.get("upvotes")),
                           (md_link("repo", i["github"]) + (f" ⭐ {fmt_int(i['github_stars'])}" if i.get("github_stars") else ""))
                           if i.get("github") else "—"])
    if kind == "paper":
        return (["Paper", "Authors", "Category", "Submitted"],
                lambda i: [md_link(clip(i["title"], 110), i["url"]) + _also(i), _authors(i.get("authors")),
                           f"`{md_escape(i.get('category'))}`", fmt_day(i.get("published"))])
    if kind == "mcp":
        if key == "smithery":
            return (["Server", "What it does", "Uses", "Verified", "Hosted"],
                    lambda i: [md_link(i["title"], i["url"]), md_escape(clip(i.get("desc"), 100)) or "—", fmt_int(i.get("uses")),
                               "yes" if i.get("verified") else "no", "remote" if i.get("remote") else "local"])
        return (["Server", "What it does", "Version", "Transport", "Published"],
                lambda i: [md_link(i["title"], i["url"]) + (f" <sub>`{md_escape(i['name'])}`</sub>" if i.get("name") and i["name"] != i["title"] else ""),
                           md_escape(clip(i.get("desc"), 100)) or "—", md_escape(i.get("version")) or "—",
                           ", ".join((["remote"] if i.get("remote") else []) + [p for p in i.get("packages") or [] if p]) or "—",
                           fmt_day(i.get("published"))])
    if kind == "llm":
        return (["Model", "Provider id", "Context", "Input $/1M", "Output $/1M", "Added"],
                lambda i: [md_link(i["title"], i["url"]), f"`{md_escape(i.get('model_id'))}`", fmt_compact(i.get("context")),
                           "—" if i.get("price_in") is None else f"{i['price_in']:g}",
                           "—" if i.get("price_out") is None else f"{i['price_out']:g}", fmt_day(i.get("created")).rsplit(" ", 1)[0]])
    if kind == "lab" or kind == "news":
        return (["Headline", "Outlet", "Published"],
                lambda i: [md_link(clip(i["title"], 120), i["url"]) + _also(i), md_escape(i.get("outlet")) or "—",
                           fmt_day(i.get("published"))])
    if kind == "package":
        if key == "crates":
            return (["Crate", "What it is", "Version", "Downloads (90 d)", "All-time", "List"],
                    lambda i: [md_link(i["title"], i["url"]), md_escape(clip(i.get("desc"), 80)) or "—", f"`{md_escape(i.get('version'))}`",
                               fmt_int(i.get("recent")), fmt_int(i.get("downloads")), i.get("group", "")])
        return (["Package", "What it is", "Version", "Weekly downloads", "Released", "Licence"],
                lambda i: [md_link(i["title"], i["url"]), md_escape(clip(i.get("desc"), 80)) or "—", f"`{md_escape(i.get('version'))}`",
                           fmt_int(i.get("weekly")), fmt_day(i.get("published")).rsplit(" ", 1)[0], md_escape(i.get("license")) or "—"])
    if kind == "cdn":
        return (["Package", "CDN hits this week", "Change vs last week"],
                lambda i: [md_link(i["title"], i["url"]), fmt_compact(i.get("hits")),
                           "—" if i.get("change") is None else f"{i['change']:+.1f}%"])
    if kind == "image":
        return (["Image", "What it is", "Pulls (all-time)", "Stars", "Updated"],
                lambda i: [md_link(i["title"], i["url"]), md_escape(clip(i.get("desc"), 80)) or "—", fmt_compact(i.get("pulls")),
                           fmt_int(i.get("stars")), fmt_day(i.get("published"))])
    if kind == "release":
        return (["Project", "Release", "Type", "Published"],
                lambda i: [md_link(i["project"], f"https://github.com/{i['project']}"), md_link(i.get("release_title") or i.get("tag"), i["url"]),
                           "pre-release" if i.get("prerelease") else "release", fmt_day(i.get("published"))])
    if kind == "kev":
        return (["CVE", "Vendor", "Product", "Vulnerability", "Added", "Ransomware use", "Fix due"],
                lambda i: [md_link(i["title"], i["url"]), md_escape(i.get("vendor")), md_escape(i.get("product")),
                           md_escape(clip(i.get("name"), 80)), i.get("added") or "—", md_escape(i.get("ransomware")) or "—", i.get("due") or "—"])
    if kind == "cve":
        return (["CVE", "Score", "Vendor", "Reported by", "Summary", "Published"],
                lambda i: [md_link(i["title"], i["url"]),
                           f"{i['score']} {md_escape(i.get('severity', '').title())} <sub>v{i.get('cvss')}</sub>" if i.get("score") is not None else "—",
                           md_escape(i.get("vendor")) or "—", md_escape(clip((i.get("assigner") or "").split("@")[-1], 30)) or "—",
                           md_escape(clip(i.get("desc"), 110)), fmt_day(i.get("published"))])
    if kind == "euvd":
        return (["EUVD id", "CVE", "Score", "Vendor", "Product", "Summary"],
                lambda i: [md_link(i["title"], i["url"]), md_escape(i.get("cve")) or "—",
                           f"{i['score']} <sub>v{i.get('cvss')}</sub>" if i.get("score") is not None else "—",
                           md_escape(i.get("vendor")) or "—", md_escape(i.get("product")) or "—", md_escape(clip(i.get("desc"), 100))])
    if kind == "incident":
        return (["Service", "Incident", "Impact", "Status", "Started"],
                lambda i: [md_escape(i.get("service")), md_link(clip(i["title"], 90), i["url"]), md_escape(i.get("impact")) or "—",
                           md_escape(i.get("status")) or "—", fmt_day(i.get("published"))])
    if kind == "post":
        if i_is_lobsters(key):
            return (["Story", "Score", "Comments", "Tags", "Discuss"],
                    lambda i: [md_link(clip(i["title"], 110), i["url"]) + _also(i), fmt_int(i.get("score")), fmt_int(i.get("comments")),
                               _topics(i.get("tags")), md_link("thread", i.get("discuss"))])
        return (["Article", "Author", "Reactions", "Comments", "Read", "Tags"],
                lambda i: [md_link(clip(i["title"], 110), i["url"]) + _also(i), md_escape(i.get("author")) or "—",
                           fmt_int(i.get("reactions")), fmt_int(i.get("comments")),
                           f"{i['minutes']} min" if i.get("minutes") else "—", _topics(i.get("tags"))])
    if kind == "question":
        return (["Question", "Score", "Answers", "Views", "Tags"],
                lambda i: [md_link(clip(i["title"], 110), i["url"]), fmt_int(i.get("score")),
                           fmt_int(i.get("answers")) + (" ✓" if i.get("answered") else ""), fmt_int(i.get("views")), _topics(i.get("tags"))])
    if kind == "product":
        return (["Product", "Tagline", "Posted by"],
                lambda i: [md_link(i["title"], i["url"]), md_escape(clip(i.get("desc"), 100)) or "—", md_escape(i.get("author")) or "—"])
    if kind == "search":
        return (["Search", "Country", "Searches", "Top story"],
                lambda i: [md_link(i["title"], i["url"]), i.get("geo"), md_escape(i.get("traffic")) or "—",
                           (md_link(clip(i["news_title"], 80), i["news_url"]) + (f" <sub>{md_escape(i['news_source'])}</sub>" if i.get("news_source") else ""))
                           if i.get("news_title") else "—"])
    if kind == "wiki":
        return (["Article", "Views", "Rank"],
                lambda i: [md_link(i["title"], i["url"]), fmt_int(i.get("views")), fmt_int(i.get("rank"))])
    if kind == "tag":
        return (["Hashtag", "Posts (2 days)", "Accounts (2 days)"],
                lambda i: [md_link(i["title"], i["url"]), fmt_int(i.get("uses")), fmt_int(i.get("accounts"))])
    if kind == "topic":
        return (["Topic", "Context"],
                lambda i: [md_link(i["title"], i["url"]), md_escape(clip(i.get("desc"), 120)) or "—"])
    return (["Item"], lambda i: [md_link(i["title"], i["url"])])


def i_is_lobsters(key: str) -> bool:
    return key == "lobsters"


def table(headers: list[str], rows: list[list[str]], numbered: bool = True) -> str:
    if numbered:
        headers = ["#"] + headers
        rows = [[str(n)] + r for n, r in enumerate(rows, 1)]
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out += ["| " + " | ".join(c if c else "—" for c in r) + " |" for r in rows]
    return "\n".join(out)


def render_block(res: SourceResult, items: list[dict], visible: int, title: str | None = None,
                 hidden_dupes: int = 0, cap: int | None = None, more_link: str = "") -> str:
    """One source: heading line, source line, table with overflow in <details>."""
    parts = []
    if title:
        parts += [f"### {title}", ""]
    src = f"Source: {md_link(domain_of(res.url) or res.url, res.url)} · fetched {fmt_hm(res.fetched_at)} Europe/Berlin"
    if not res.ok:
        parts += [f"_Skipped today: {md_escape(res.note)}._ {src}", ""]
        return "\n".join(parts)
    if not items:
        msg = "Nothing new in this window today."
        if hidden_dupes:
            msg = f"All {hidden_dupes} items were already listed higher up on this page."
        parts += [f"_{msg}_ <sub>{src}</sub>", ""]
        return "\n".join(parts)
    kind = items[0]["kind"]
    headers, fn = columns(kind, res.key)
    rows = [fn(i) for i in items]
    cut = 0
    if cap is not None and len(rows) > cap:
        cut = len(rows) - cap
        rows = rows[:cap]
    parts += [f"<sub>{src}. {md_escape(res.note)}.</sub>", ""]
    parts.append(table(headers, rows[:visible]))
    if len(rows) > visible:
        more = [[str(n)] + r for n, r in enumerate(rows[visible:], visible + 1)]
        parts += ["", "<details>", f"<summary>Show {len(rows) - visible} more</summary>", "",
                  _table_with_numbers(headers, more), "", "</details>"]
    notes = []
    if cut and more_link:
        notes.append(f"{cut} more in [today's full list]({more_link})")
    if hidden_dupes:
        notes.append(f"{hidden_dupes} already listed higher up and not repeated")
    if notes:
        parts += ["", "<sub>" + " · ".join(notes) + ".</sub>"]
    parts.append("")
    return "\n".join(parts)


def _table_with_numbers(headers: list[str], rows: list[list[str]]) -> str:
    return table(["#"] + headers, rows, numbered=False)


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------

# (anchor, heading, one-line blurb, [(source key, sub-heading, README rows, archive rows)])
SECTIONS = [
    ("github", "🐙 GitHub", "Repos people are starring right now. Stars and stars gained come straight from GitHub.", [
        ("gh_daily", "Trending today · all languages", 10, 25),
        ("gh_new", "New this week · fastest-starred repos created in the last 7 days", 5, 15),
        ("gh_weekly", "Trending this week", 0, 15),
        ("gh_python", "Trending today · Python", 0, 10),
        ("gh_typescript", "Trending today · TypeScript", 0, 10),
        ("gh_rust", "Trending today · Rust", 0, 10),
        ("gh_go", "Trending today · Go", 0, 10),
    ]),
    ("hn", "🔥 Hacker News", "What engineers are reading and arguing about.", [
        ("hn_front", "Front page", 10, 20),
        ("hn_show", "Show HN · last 24 hours", 5, 10),
        ("hn_best", "Best of the week", 0, 10),
        ("hn_ask", "Ask HN · last 24 hours", 0, 8),
    ]),
    ("ai", "🤖 AI models & labs", "New models, what is rising on Hugging Face, and what the big labs published.", [
        ("hf_models", "Hugging Face · trending models", 5, 15),
        ("openrouter", "OpenRouter · newest models with prices", 5, 10),
        ("hf_spaces", "Hugging Face · trending Spaces (demos)", 0, 12),
        ("hf_datasets", "Hugging Face · trending datasets", 0, 12),
        ("openai_news", "OpenAI news · last 7 days", 0, 4),
        ("google_ai", "Google AI blog · last 7 days", 0, 4),
        ("deepmind", "Google DeepMind blog · last 7 days", 0, 4),
        ("hf_blog", "Hugging Face blog · last 7 days", 0, 4),
    ]),
    ("research", "📄 Research", "Papers the community upvoted today, then the newest arXiv submissions by field.", [
        ("hf_papers", "Hugging Face daily papers · by upvotes", 5, 15),
        ("arxiv", "arXiv · newest submissions", 0, 36),
    ]),
    ("agents", "🧠 Agents & MCP", "Model Context Protocol servers: what was just published and what people use most.", [
        ("mcp_registry", "Official MCP Registry · published or updated in the last 24 hours", 5, 12),
        ("smithery", "Smithery · most-used servers", 0, 10),
    ]),
    ("packages", "📦 Packages & releases", "Versions, downloads and releases across npm, PyPI, crates.io, Docker Hub and GitHub.", [
        ("releases", "GitHub releases of major projects · last 72 hours", 8, 40),
        ("npm", "npm · top MCP, agent and LLM packages", 0, 20),
        ("pypi", "PyPI · latest versions of key packages", 0, 14),
        ("crates", "crates.io · recent, new and just-updated crates", 0, 24),
        ("jsdelivr", "jsDelivr · most-served npm packages this week", 0, 15),
        ("dockerhub", "Docker Hub · official images updated in the last 48 hours", 0, 12),
    ]),
    ("security", "🔒 Security", "Exploited-in-the-wild bugs first, then fresh critical CVEs.", [
        ("kev", "CISA KEV · added in the last 14 days", 5, 20),
        ("nvd", "NVD · critical CVEs published in the last 48 hours", 0, 15),
        ("euvd", "ENISA EU Vulnerability Database · latest", 0, 12),
    ]),
    ("status", "☁️ Platform status", "Incidents on the platforms most teams depend on.", [
        ("githubstatus", "GitHub · last 72 hours", 3, 10),
        ("cloudflarestatus", "Cloudflare · last 72 hours", 3, 10),
    ]),
    ("community", "✍️ Community", "Developer writing, questions and launches.", [
        ("lobsters", "Lobsters · hottest", 5, 15),
        ("devto_day", "Dev.to · top today", 0, 10),
        ("devto_week", "Dev.to · top this week", 0, 10),
        ("stackoverflow", "Stack Overflow · hot questions", 0, 12),
        ("producthunt", "Product Hunt · newest featured", 0, 15),
    ]),
    ("news", "🗞️ Tech news", "Headlines and links only, newest first, from the last 36 hours.", [
        (k, f"{n}", 5 if k == "techmeme" else 0, 6) for k, n, _u, _ni in NEWS_FEEDS
    ]),
    ("pulse", "🌍 Public pulse", "What the wider public is searching, reading and sharing. Not tech-only.", [
        ("gtrends", "Google Trends · today's searches (US, DE)", 5, 20),
        ("wikipedia", "Wikipedia · most read yesterday", 0, 15),
        ("mastodon_links", "Mastodon · most shared links", 0, 12),
        ("mastodon_tags", "Mastodon · trending hashtags", 0, 15),
        ("bluesky", "Bluesky · trending topics", 0, 15),
    ]),
]


def build_also(results: dict[str, SourceResult]) -> None:
    """Mark items that appear in more than one source (by URL, or by title for news)."""
    names = {k: r.name.split(" · ")[0] for k, r in results.items()}
    where: dict[str, list[str]] = {}
    for key, res in results.items():
        if key == "maintainer" or not res.ok:
            continue
        for it in res.items:
            for k in {canonical_url(it["url"]), "t:" + title_key(it["title"]) if it["kind"] in ("news", "hn", "post", "lab") else ""}:
                if k and names[key] not in where.setdefault(k, []):
                    where[k].append(names[key])
    for key, res in results.items():
        for it in res.items:
            seen = where.get(canonical_url(it["url"]), [])
            it["_also"] = [n for n in seen if n != names[key]][:3]


def dedupe_keys(it: dict) -> set[str]:
    keys = {canonical_url(it["url"])}
    if it["kind"] in ("news", "hn", "post", "lab"):
        keys.add("t:" + title_key(it["title"]))
    return {k for k in keys if k and k != "t:"}


def section_blocks(results, mode: str) -> list[tuple]:
    """Resolve SECTIONS against results with cross-source dedupe, in page order."""
    shown: set[str] = set()
    out = []
    for anchor, heading, blurb, blocks in SECTIONS:
        resolved = []
        for key, sub, readme_n, archive_n in blocks:
            res = results.get(key)
            if not res:
                continue
            limit = archive_n
            keep, dupes = [], 0
            for it in res.items:
                ks = dedupe_keys(it)
                if ks & shown:
                    dupes += 1
                    continue
                keep.append(it)
            keep = keep[:limit]
            for it in keep:
                shown |= dedupe_keys(it)
            resolved.append((key, sub, readme_n, archive_n, res, keep, dupes))
        out.append((anchor, heading, blurb, resolved))
    return out


def count_ok(results) -> tuple[int, int]:
    keys = [k for k in results if k != "maintainer"]
    return sum(1 for k in keys if results[k].ok), len(keys)


def render_today(results, tech_x: list[dict]) -> list[str]:
    b = []

    def ok(k):
        r = results.get(k)
        return r.items if r and r.ok else []

    gh = [i for i in ok("gh_daily") if i.get("gained") is not None]
    if gh:
        top = max(gh, key=lambda i: i["gained"])
        b.append(f"🐙 **Most stars today:** {md_link(top['title'], top['url'])} — {md_escape(clip(top.get('desc'), 80))} "
                 f"(+{fmt_int(top['gained'])} today, {fmt_int(top.get('stars'))} total, {md_escape(top.get('language')) or 'no language listed'}).")
    new = ok("gh_new")
    if new:
        n = new[0]
        b.append(f"🆕 **Fastest new repo this week:** {md_link(n['title'], n['url'])} — {md_escape(clip(n.get('desc'), 70))} "
                 f"({fmt_int(n.get('stars'))} stars since {fmt_day(n.get('created')).rsplit(' ', 1)[0]}).")
    hn = ok("hn_front")
    if hn:
        h = hn[0]
        b.append(f"🔥 **Top on Hacker News:** {md_link(h['title'], h['url'])} — {fmt_int(h.get('points'))} points, "
                 f"{fmt_int(h.get('comments'))} comments.")
    pp = ok("hf_papers")
    if pp:
        p = pp[0]
        b.append(f"📄 **Most upvoted paper:** {md_link(clip(p['title'], 90), p['url'])} — {fmt_int(p.get('upvotes'))} upvotes on Hugging Face.")
    hm = ok("hf_models")
    if hm:
        m = hm[0]
        b.append(f"🤗 **#1 trending model:** {md_link(m['title'], m['url'])} — {md_escape(m.get('task')) or 'task not listed'}, "
                 f"{fmt_int(m.get('likes'))} likes.")
    kev = ok("kev")
    if kev:
        recent = [k for k in kev if k["added"] == kev[0]["added"]]
        names = ", ".join(md_escape(re.sub(r"\s*\([^)]*\)", "", k["product"])) for k in recent[:4])
        b.append(f"🔒 **Exploited in the wild:** CISA added {len(recent)} on {kev[0]['added']} ({names}); "
                 f"{len(kev)} in the last 14 days.")
    mcp = results.get("mcp_registry")
    if mcp and mcp.ok:
        m = re.search(r"(\d+) distinct servers", mcp.note)
        if m:
            b.append(f"🧠 **MCP:** {m.group(1)} servers were published or updated in the official registry in the last 24 hours.")
    rel, projects = [], set()
    for r in ok("releases"):
        if not r.get("prerelease") and r["project"] not in projects:
            projects.add(r["project"])
            rel.append(r)
    if rel:
        b.append("🚀 **Shipped:** " + ", ".join(f"{md_link(r['project'].split('/')[1] + ' ' + (r.get('release_title') or r['tag']), r['url'])}"
                                                for r in rel[:3]) + ".")
    if tech_x:
        t = tech_x[0]
        posts = f"{t['posts']} posts" if t.get("posts") and t["posts"] != "—" else "volume not shown"
        b.append(f"🐦 **Tech on X:** {md_link(t['name'], t['url'])} ({posts}, {md_escape(t['region'])} list).")
    return [f"- {x}" for x in b[:9]]


def render_jump(blocks) -> list[str]:
    rows = [["[⚡ Today in 30 seconds](#today)", "The headlines, one line each", "—"]]
    for anchor, heading, blurb, resolved in blocks:
        n = sum(len(r[5]) for r in resolved)
        live = sum(1 for r in resolved if r[4].ok)
        rows.append([f"[{heading}](#{anchor})", md_escape(blurb.split('.')[0]), f"{n} items · {live}/{len(resolved)} sources"])
    rows += [["[🐦 Tech on X](#x)", "Tech topics from today's X trend lists", "—"],
             ["[🗂️ Niches](#niches)", "The same items, sorted by topic", "—"],
             ["[👤 From the maintainer](#maintainer)", "Labelled, not a ranking", "—"],
             ["[📚 Archive](#archive) · [✅ Sources](#sources)", "Past days and where every number comes from", "—"]]
    return [table(["Section", "What's inside", "Today"], rows, numbered=False)]


def render_sources_table(results, x_note: str, enrich_note: str) -> list[str]:
    rows = []
    for n, (key, name, url, _fn) in enumerate(SOURCES, 1):
        r = results.get(key)
        if not r:
            continue
        status = "✅ OK" if r.ok else "⏭️ Skipped"
        note = r.note if r.ok else f"{r.note}"
        rows.append([str(n), md_link(name, url), status, str(len(r.items)) if r.ok else "0",
                     fmt_hm(r.fetched_at), md_escape(clip(note, 140))])
    rows.append(["—", "X trends", "✅ OK" if "reused" in x_note else "⏭️ Skipped", "—", "—", md_escape(x_note)])
    rows.append(["—", "Licence and topics for trending repos", "✅ OK" if "added for" in enrich_note else "⏭️ Skipped",
                 "—", "—", md_escape(enrich_note)])
    return [table(["#", "Source", "Status", "Items", "Fetched", "How it is read"], rows, numbered=False)]


def render_niche_index(niche_counts: dict[str, int], prefix: str) -> list[str]:
    rows = [[f"{n['emoji']} [{n['title']}]({prefix}niches/{n['slug']}.md)", md_escape(n["intro"]), str(niche_counts.get(n["slug"], 0))]
            for n in NICHES]
    return [table(["Niche", "What's in it", "Items today"], rows, numbered=False)]


def render_x(tech_x, x_sections, full: bool) -> list[str]:
    p = []
    if not tech_x:
        p.append("_No tech topics in today's X trend lists, or the lists were not captured yet._")
        return p + [""]
    p.append("Post volume is the `tweet_count` X showed when the lists were captured. A dash means X showed no number.")
    p.append("")
    rows = [[md_link(t["name"], t["url"]), md_escape(t["posts"]), md_escape(t["region"]),
             md_escape(clip(t["context"], 100)) if "No independently confirmed" not in t["context"] else "—"] for t in tech_x[:12]]
    p.append(table(["Trend", "Posts", "List", "Context"], rows))
    if full and x_sections:
        p += ["", "<details>", "<summary>Full X trend lists (all topics, not just tech)</summary>", ""]
        for region, rows_ in x_sections.items():
            p += [f"#### {region}", "", table(["Trend", "Posts"], [[md_link(r["name"], r["url"]), md_escape(r["posts"])] for r in rows_]), ""]
        p.append("</details>")
    return p + [""]


def render_maintainer(results) -> list[str]:
    r = results.get("maintainer")
    p = ["These are the maintainer's own projects. **This is not a ranking.** They show up in the tables above only when a source listed them on its own.", ""]
    if not r or not r.ok or not r.items:
        return p + ["- [mjmirza on GitHub](https://github.com/mjmirza)", ""]
    for it in r.items:
        p.append(f"- {md_link(it['title'], it['url'])} — {md_escape(it.get('desc'))} ({fmt_int(it.get('stars'))} stars)")
    return p + [""]


LICENSE_LINE = (
    "- License: [OpenRoots Agent License 2.3](LICENSE) (SPDX `LicenseRef-OpenRoots-ORA-2.3`). Free and unconditional at or below "
    "USD 20,000,000 annual revenue, and for any individual, nonprofit, school, or government body at any size. Above that "
    "threshold, a small self-reported royalty applies, capped per year. AI training on this work is not granted by either "
    "tier and needs a separate Compute license; human reading and search indexing are unaffected. Canonical text: "
    "[openroots.org/licenses/ora/2.3](https://openroots.org/licenses/ora/2.3)."
)


def render_page(results, blocks, fetched_at, tech_x, x_sections, x_note, enrich_note,
                niche_counts, archive_links, mode: str, archive_rel: str = "") -> str:
    """mode='readme' (compact, top rows visible) or 'archive' (every row)."""
    readme = mode == "readme"
    okn, total = count_ok(results)
    p = []
    if readme:
        p += ["# awesome-trending", "",
              "One page for everything rising in tech today: GitHub, Hacker News, AI models and papers, MCP servers, "
              "packages, releases, security advisories, platform status, tech news and the public pulse.", "",
              f"[![Last commit](https://img.shields.io/github/last-commit/{REPO_OWNER}/{REPO_NAME})]({REPO_URL}/commits/main) "
              f"[![License](https://img.shields.io/badge/License-OpenRoots_ORA_2.3-2ea44f)](LICENSE) "
              f"[![Sources](https://img.shields.io/badge/sources_live_today-{okn}%2F{total}-informational)](#sources)", ""]
    else:
        p += [f"# awesome-trending — {fmt_date(fetched_at)}", ""]
    p += [f"**Today:** {fmt_date(fetched_at)} · snapshot at {fmt_time(fetched_at)} · {okn} of {total} sources answered", "",
          "**How to read this page:** the 30-second summary first, then one section per area. "
          + ("Each table shows the top rows; click **Show more** for the rest. The [daily archive](#archive) has every row." if readme
             else "Every row fetched today is here. Long lists are folded; click **Show more**."), "",
          '<a id="today"></a>', "", "## ⚡ Today in 30 seconds", ""]
    p += render_today(results, tech_x) + [""]
    p += ["## 🧭 Jump to", ""] + render_jump(blocks) + [""]

    for anchor, heading, blurb, resolved in blocks:
        p += [f'<a id="{anchor}"></a>', "", f"## {heading}", "", blurb, ""]
        folded = []
        full = f"{archive_rel}#{anchor}" if archive_rel else ""
        for key, sub, readme_n, archive_n, res, keep, dupes in resolved:
            if readme:
                if readme_n > 0:
                    p.append(render_block(res, keep, readme_n, sub, dupes, cap=10, more_link=full))
                else:
                    folded.append((sub, res, keep, dupes))
            else:
                p.append(render_block(res, keep, 10, sub, dupes))
        if folded:
            label = ", ".join(f"{s.split(' · ')[0]}" if " · " in s else s for s, *_ in folded)
            total_items = sum(len(k) for _s, _r, k, _d in folded)
            p += ["<details>", f"<summary><b>More in this section</b> ({total_items} items): {md_escape(clip(', '.join(dict.fromkeys(label.split(', '))), 150))}</summary>", ""]
            for sub, res, keep, dupes in folded:
                p.append(render_block(res, keep, 5, sub, dupes, cap=5, more_link=full))
            p += ["</details>", ""]
        p += [f"<sub>[↑ Back to top](#today)</sub>", ""]

    p += ['<a id="x"></a>', "", "## 🐦 Tech on X", ""] + render_x(tech_x, x_sections, full=not readme)
    prefix = "" if readme else "../../../"
    p += ['<a id="niches"></a>', "", "## 🗂️ Niches", "", "Every item above, routed by topic. One file per niche.", ""]
    p += render_niche_index(niche_counts, prefix) + [""]
    p += ['<a id="maintainer"></a>', "", "## 👤 From the maintainer", ""] + render_maintainer(results)
    if readme:
        p += ['<a id="archive"></a>', "", "## 📚 Archive", "", "<details>", "<summary>Every past day</summary>", ""]
        p += [f"- [{label}]({rel})" for label, rel in archive_links] + ["", "</details>", ""]
        p += ["## 🤝 Contribute", "",
              f"- Submit a repo with the [issue form]({SUBMIT_URL}). Tables are rebuilt from the sources every morning.",
              "- [Featured in awesome-trending badge](docs/badge.md) for repos that appeared here.",
              "- How it works and the full source list: [CONTRIBUTING.md](CONTRIBUTING.md).", LICENSE_LINE, ""]
    p += ['<a id="sources"></a>', "", "## ✅ Sources", "",
          f"Fetched {fmt_date(fetched_at)} at {fmt_time(fetched_at)}. Every figure comes from the source named in its row. "
          "A dash means the source did not give a number. Nothing here is invented. Items listed by more than one source appear "
          "once, with an <sub>also:</sub> note.", ""]
    p += render_sources_table(results, x_note, enrich_note) + [""]
    return "\n".join(p).rstrip() + "\n"


NICHE_LABELS = {
    "repo": "Repositories", "hn": "Hacker News", "model": "Models", "space": "Spaces", "dataset": "Datasets",
    "paper": "Papers", "mcp": "MCP servers", "llm": "New hosted models", "lab": "Lab posts", "news": "Headlines",
    "package": "Packages", "cdn": "CDN traffic", "image": "Container images", "release": "Releases",
    "kev": "Exploited vulnerabilities (CISA KEV)", "cve": "Critical CVEs (NVD)", "euvd": "EU vulnerability database",
    "incident": "Incidents", "post": "Posts", "question": "Questions", "product": "Launches",
    "search": "Searches", "wiki": "Most-read articles", "tag": "Hashtags", "topic": "Topics",
}


def _momentum(key: str, i: dict) -> str:
    if key == "gh_new":
        return f"new, created {fmt_day(i.get('created')).rsplit(' ', 1)[0]}"
    if i.get("gained") is None:
        return "—"
    return f"+{fmt_int(i['gained'])} {'this week' if key == 'gh_weekly' else 'today'}"


def niche_columns(kind: str):
    """Unified columns per kind so one niche table can mix several sources. fn(key, item)."""
    if kind == "repo":
        return (["Repository", "What it is", "Lang", "Licence", "Stars", "Momentum", "Topics"],
                lambda k, i: [md_link(i["title"], i["url"]), md_escape(clip(i.get("desc"), 100)) or "—",
                              md_escape(i.get("language")) or "—", md_escape(i.get("license")) or "—",
                              fmt_int(i.get("stars")), _momentum(k, i), _topics(i.get("topics"))])
    if kind == "paper":
        return (["Paper", "Authors", "Signal"],
                lambda k, i: [md_link(clip(i["title"], 110), i["url"]), _authors(i.get("authors")),
                              f"{fmt_int(i.get('upvotes'))} upvotes" if k == "hf_papers" else f"`{md_escape(i.get('category'))}`, new"])
    if kind == "mcp":
        return (["Server", "What it does", "Signal"],
                lambda k, i: [md_link(i["title"], i["url"]), md_escape(clip(i.get("desc"), 100)) or "—",
                              f"{fmt_int(i.get('uses'))} uses" if k == "smithery" else f"v{md_escape(i.get('version'))}, {fmt_day(i.get('published'))}"])
    if kind == "package":
        def cells(k, i):
            if k == "crates":
                dl = f"{fmt_int(i.get('recent'))} in 90 d"
            else:
                dl = f"{fmt_int(i.get('weekly'))} a week" if i.get("weekly") is not None else "—"
            return [md_link(i["title"], i["url"]), md_escape(i.get("ecosystem")), f"`{md_escape(i.get('version'))}`",
                    dl, md_escape(clip(i.get("desc"), 80)) or "—"]
        return (["Package", "Ecosystem", "Version", "Downloads", "What it is"], cells)
    if kind == "post":
        def pcells(k, i):
            if k == "lobsters":
                eng = f"{fmt_int(i.get('score'))} score, {fmt_int(i.get('comments'))} comments"
            else:
                eng = f"{fmt_int(i.get('reactions'))} reactions, {fmt_int(i.get('comments'))} comments"
            return [md_link(clip(i["title"], 110), i["url"]), eng, _topics(i.get("tags"))]
        return (["Post", "Engagement", "Tags"], pcells)
    headers, fn = columns(kind, "")
    return headers, (lambda k, i, _fn=fn: columns(kind, k)[1](i))


def render_niche_page(niche: dict, rows: list[tuple[str, dict]], results, fetched_at: datetime) -> str:
    slug = niche["slug"]
    p = [f"# {niche['emoji']} {niche['title']}", "", niche["intro"], "",
         f"**Updated:** {fmt_date(fetched_at)} at {fmt_time(fetched_at)} · {len(rows)} items from today's sources. "
         "This is a daily snapshot, not a complete catalogue.", "",
         f"[⬅ All of today on the main page](../README.md) · [Other niches](../README.md#niches) · [Submit a repo]({SUBMIT_URL})", ""]
    if not rows:
        p += ["Nothing from today's sources landed in this niche. It fills as matching items appear.", ""]
        return "\n".join(p)
    groups: dict[str, list[tuple[str, dict]]] = {}
    first_core: dict[str, int] = {}
    for n, (key, it) in enumerate(rows):
        kind = it["kind"]
        groups.setdefault(kind, []).append((key, it))
        core = slug in SOURCE_NICHES.get(key, []) or it.get("niche") == slug
        first_core.setdefault(kind, n if core else 10_000 + n)
        if core:
            first_core[kind] = min(first_core[kind], n)
    order = sorted(groups, key=lambda k: first_core[k])
    p += ["**In this file:** " + " · ".join(f"[{NICHE_LABELS.get(k, k)}](#{_anchor(NICHE_LABELS.get(k, k))}) ({len(groups[k])})"
                                           for k in order), ""]
    for kind in order:
        group = groups[kind][:30]
        label = NICHE_LABELS.get(kind, kind)
        p += [f"## {label}", ""]
        headers, fn = niche_columns(kind)
        body = [fn(k, it) + [md_link(results[k].name.split(" · ")[0], results[k].url)] for k, it in group]
        p.append(table(headers + ["Source"], body[:10]))
        if len(body) > 10:
            more = [[str(n)] + r for n, r in enumerate(body[10:], 11)]
            p += ["", "<details>", f"<summary>Show {len(body) - 10} more</summary>", "",
                  _table_with_numbers(headers + ["Source"], more), "", "</details>"]
        p.append("")
    p += [f"<sub>Every figure comes from the linked source, fetched {fmt_time(fetched_at)}. "
          "See the [sources table](../README.md#sources).</sub>", ""]
    return "\n".join(p)


def _anchor(heading: str) -> str:
    a = heading.lower()
    a = re.sub(r"[^\w\- ]", "", a)
    return a.replace(" ", "-")


def collect_niches(results) -> dict[str, list[tuple[str, dict]]]:
    out: dict[str, list[tuple[str, dict]]] = {n["slug"]: [] for n in NICHES}
    seen: dict[str, set] = {n["slug"]: set() for n in NICHES}
    for _a, _h, _b, blocks in SECTIONS:
        for key, *_rest in blocks:
            res = results.get(key)
            if not res or not res.ok:
                continue
            for it in res.items:
                for slug in route(key, it):
                    ks = dedupe_keys(it)
                    if ks & seen[slug]:
                        continue
                    seen[slug] |= ks
                    out[slug].append((key, it))
    return out


# ---------------------------------------------------------------------------
# Archive handling
# ---------------------------------------------------------------------------

def merge_archive(path: Path, generated: str, fetched_at: datetime) -> str:
    """Keep anything written earlier in the day (the X trend snapshot) above the generated block."""
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    original_path = path.with_name(path.stem + ".original.md")
    if not existing and original_path.is_file():
        existing = original_path.read_text(encoding="utf-8")
    prefix = existing.split(GENERATED_START)[0] if GENERATED_START in existing else existing
    prefix = re.sub(r"(\n+---\s*\n+\s*## Additional sources[\s\S]*)$", "", prefix.rstrip()).rstrip()
    if prefix:
        header = (f"\n\n---\n\n## Additional sources — {fmt_date(fetched_at)}\n\n"
                  "The snapshot above is unchanged. The full daily directory follows.\n\n")
        return prefix + header + GENERATED_START + "\n" + generated + GENERATED_END + "\n"
    return GENERATED_START + "\n" + generated + GENERATED_END + "\n"


def list_archive_links(root: Path, today_rel: str) -> list[tuple[str, str]]:
    archive_root = root / "archive"
    files = [p for p in archive_root.rglob("*.md")] if archive_root.is_dir() else []
    rels = {p.relative_to(root).as_posix() for p in files if not p.name.endswith(".original.md")}
    rels.add(today_rel)
    links = []
    for rel in sorted(rels, reverse=True):
        stem = Path(rel).stem
        try:
            label = datetime.strptime(stem, "%Y-%m-%d").strftime("%-d %B %Y")
        except ValueError:
            label = stem
        links.append((label, rel))
    return links


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run_sources(only: set[str] | None) -> dict[str, SourceResult]:
    results: dict[str, SourceResult] = {}
    todo = [s for s in SOURCES if not only or s[0] in only]

    def one(spec):
        key, name, url, fn = spec
        res = SourceResult(key, name, url)
        t0 = time.monotonic()
        try:
            items, note = fn()
            res.items = [i for i in items if i.get("title") and i.get("url")]
            res.ok, res.note = True, note
        except FetchError as exc:
            res.note = str(exc)
        except Exception as exc:  # a broken parser must not stop the run
            res.note = f"parser error: {type(exc).__name__}: {exc}"
        res.fetched_at = now_berlin()
        res.elapsed = time.monotonic() - t0
        return res

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(one, s): s for s in todo}
        done, pending = wait(futures, timeout=TOTAL_BUDGET + REQUEST_TIMEOUT + 10)
        for f in done:
            r = f.result()
            results[r.key] = r
        for f in pending:
            key, name, url, _fn = futures[f]
            r = SourceResult(key, name, url)
            r.note, r.fetched_at = "timed out", now_berlin()
            results[key] = r
    # Keep registry order.
    return {k: results[k] for k, *_ in SOURCES if k in results}


def run(root: Path, dry_run: bool = False, only: set[str] | None = None) -> int:
    t0 = time.monotonic()
    DEADLINE[0] = t0 + TOTAL_BUDGET
    fetched_at = now_berlin()
    results = run_sources(only)
    DEADLINE[0] = max(DEADLINE[0], time.monotonic() + 25)  # small reserve for the enrichment calls
    enrich_note = enrich_repos(results)
    build_also(results)

    x_sections, x_note = load_x_trends(root, fetched_at)
    tech_x = select_tech_on_x(x_sections) if x_sections else []

    for r in results.values():
        flag = "ok  " if r.ok else "SKIP"
        print(f"  [{flag}] {r.key:18} {len(r.items):3} items {r.elapsed:5.1f}s  {r.note[:90]}")
    print(f"  [x   ] {x_note}; {len(tech_x)} tech rows")
    print(f"  [enr ] {enrich_note}")

    niche_rows = collect_niches(results)
    niche_counts = {k: len(v) for k, v in niche_rows.items()}
    blocks = section_blocks(results, "readme")

    day_dir = root / "archive" / fetched_at.strftime("%Y/%m")
    rel_archive = f"archive/{fetched_at:%Y/%m}/{fetched_at:%Y-%m-%d}.md"
    archive_links = list_archive_links(root, rel_archive)

    readme = render_page(results, blocks, fetched_at, tech_x, x_sections, x_note, enrich_note,
                         niche_counts, archive_links, "readme", rel_archive)
    archive_body = render_page(results, blocks, fetched_at, tech_x, x_sections, x_note, enrich_note,
                               niche_counts, archive_links, "archive")
    archive_path = root / rel_archive
    archive_md = merge_archive(archive_path, archive_body, fetched_at)
    niche_pages = {f"niches/{n['slug']}.md": render_niche_page(n, niche_rows[n["slug"]], results, fetched_at) for n in NICHES}

    okn, total = count_ok(results)
    print(f"Sources answered: {okn}/{total}; fetch time {time.monotonic() - t0:.1f}s")
    if dry_run:
        print(f"Dry run: README {len(readme):,} bytes, archive {len(archive_md):,} bytes")
        for path, text in niche_pages.items():
            print(f"  {path}: {niche_counts[Path(path).stem]} items, {len(text):,} bytes")
        return 0
    if okn == 0:
        print("No source answered; leaving files untouched.")
        return 1
    (root / "README.md").write_text(readme, encoding="utf-8")
    day_dir.mkdir(parents=True, exist_ok=True)
    archive_path.write_text(archive_md, encoding="utf-8")
    for rel, text in niche_pages.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    print(f"Wrote README.md, {rel_archive} and {len(niche_pages)} niche files")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update the awesome-trending hub")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", default="", help="Comma-separated source keys")
    args = parser.parse_args(argv)
    root = args.root or Path(__file__).resolve().parent.parent
    only = {k.strip() for k in args.only.split(",") if k.strip()} or None
    return run(root.resolve(), dry_run=args.dry_run, only=only)


if __name__ == "__main__":
    sys.exit(main())
