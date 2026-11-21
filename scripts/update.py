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
    --docs         Rewrite docs/methodology.md and the niches/ pointer files
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
MAX_WORKERS = 16

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
    ("cs.RO", "Robotics"),
    ("q-bio.*", "Quantitative biology"),
    ("q-fin.*", "Quantitative finance"),
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
    ("techmeme", "Techmeme", "https://www.techmeme.com/feed.xml", None),
    ("verge", "The Verge", "https://www.theverge.com/rss/index.xml", None),
    ("techcrunch", "TechCrunch", "https://techcrunch.com/feed/", None),
    ("ars", "Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab", None),
    ("lwn", "LWN.net", "https://lwn.net/headlines/rss", "cloud-devops"),
    ("thn", "The Hacker News", "https://feeds.feedburner.com/TheHackersNews", "cybersecurity"),
    ("bleeping", "BleepingComputer", "https://www.bleepingcomputer.com/feed/", "cybersecurity"),
    ("ghchangelog", "GitHub Changelog", "https://github.blog/changelog/feed/", "devtools"),
    ("simonw", "Simon Willison", "https://simonwillison.net/atom/everything/", "ai-llms"),
]

LAB_FEEDS = [
    ("openai_news", "OpenAI News", "https://openai.com/news/rss.xml"),
    ("google_ai", "Google AI blog", "https://blog.google/technology/ai/rss/"),
    ("deepmind", "Google DeepMind blog", "https://deepmind.google/blog/rss.xml"),
    ("hf_blog", "Hugging Face blog", "https://huggingface.co/blog/feed.xml"),
]

# Industry outlets: public RSS, headlines and links only. (key, outlet, url, industry)
INDUSTRY_FEEDS = [
    ("finextra", "Finextra", "https://www.finextra.com/rss/headlines.aspx", "fintech"),
    ("pymnts", "PYMNTS", "https://www.pymnts.com/feed/", "fintech"),
    ("coindesk", "CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/", "crypto-web3"),
    ("decrypt", "Decrypt", "https://decrypt.co/feed", "crypto-web3"),
    ("statnews", "STAT News", "https://www.statnews.com/feed/", "health-biotech"),
    ("robotreport", "The Robot Report", "https://www.therobotreport.com/feed/", "robotics-hardware"),
    ("ieee_robotics", "IEEE Spectrum Robotics", "https://spectrum.ieee.org/feeds/topic/robotics.rss", "robotics-hardware"),
    ("ieee_semis", "IEEE Spectrum Semiconductors", "https://spectrum.ieee.org/feeds/topic/semiconductors.rss", "semiconductors"),
    ("eetimes", "EE Times", "https://www.eetimes.com/feed/", "semiconductors"),
    ("semiwiki", "SemiWiki", "https://semiwiki.com/feed/", "semiconductors"),
    ("canary", "Canary Media", "https://www.canarymedia.com/rss.rss", "climate-energy"),
    ("electrek", "Electrek", "https://electrek.co/feed/", "climate-energy"),
    ("cleantechnica", "CleanTechnica", "https://cleantechnica.com/feed/", "climate-energy"),
    ("eia", "EIA Today in Energy", "https://www.eia.gov/rss/todayinenergy.xml", "climate-energy"),
    ("modernretail", "Modern Retail", "https://www.modernretail.co/feed/", "ecommerce-retail"),
    ("retaildive", "Retail Dive", "https://www.retaildive.com/feeds/news/", "ecommerce-retail"),
    ("dc360", "Digital Commerce 360", "https://www.digitalcommerce360.com/feed/", "ecommerce-retail"),
    ("gamesindustry", "GamesIndustry.biz", "https://www.gamesindustry.biz/feed", "gaming-xr"),
    ("gamedeveloper", "Game Developer", "https://www.gamedeveloper.com/rss.xml", "gaming-xr"),
    ("uploadvr", "UploadVR", "https://www.uploadvr.com/rss/", "gaming-xr"),
    ("tc_enterprise", "TechCrunch Enterprise", "https://techcrunch.com/category/enterprise/feed/", "enterprise-saas"),
    ("edsurge", "EdSurge", "https://www.edsurge.com/articles_rss", "education"),
    ("classcentral", "Class Central", "https://www.classcentral.com/report/feed/", "education"),
    ("niemanlab", "Nieman Lab", "https://www.niemanlab.org/feed/", "media-creator"),
    ("tubefilter", "Tubefilter", "https://www.tubefilter.com/feed/", "media-creator"),
    ("spacenews", "SpaceNews", "https://spacenews.com/feed/", "space-mobility"),
    ("nasa", "NASA news releases", "https://www.nasa.gov/news-release/feed/", "space-mobility"),
    ("tc_transport", "TechCrunch Transportation", "https://techcrunch.com/category/transportation/feed/", "space-mobility"),
    ("eff", "EFF Deeplinks", "https://www.eff.org/rss/updates.xml", "policy-regulation"),
    ("ec_press", "European Commission press corner", "https://ec.europa.eu/commission/presscorner/api/rss?language=en", "policy-regulation"),
    ("ninetofivemac", "9to5Mac", "https://9to5mac.com/feed/", "mobile"),
    ("androidpolice", "Android Police", "https://www.androidpolice.com/feed/", "mobile"),
    ("techeu", "Tech.eu", "https://tech.eu/feed/", None),
    ("sifted", "Sifted", "https://sifted.eu/feed", None),
]

# GitHub topics searched for young repos in industries that trending pages rarely cover.
GITHUB_TOPICS = [
    ("robotics", "robotics-hardware"),
    ("bioinformatics", "health-biotech"),
    ("fintech", "fintech"),
]

STATUS_PAGES = [
    ("githubstatus", "GitHub", "https://www.githubstatus.com/api/v2/incidents.json"),
    ("cloudflarestatus", "Cloudflare", "https://www.cloudflarestatus.com/api/v2/incidents.json"),
]

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
    "api.github.com": 6.2,      # search API: 10 calls a minute without a token
    "news.google.com": 1.6,
    "fred.stlouisfed.org": 0.5,
    "huggingface.co": 0.4,
    "datasets-server.huggingface.co": 0.5,
    "github.com": 0.5,
    "pypistats.org": 0.6,
    "services.nvd.nist.gov": 6.5,  # NVD: 5 requests per 30 seconds without a key
    "api.coingecko.com": 2.5,
    "ll.thespacedevs.com": 2.0,
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
    rows = github_search(f"created:>{since} fork:false archived:false", 100, sort="stars")
    out = []
    for r in rows:
        rec = repo_from_api(r)
        # Freshly created repos with no licence or description are often star-farmed
        # bait; keep only repos that state both.
        if not rec["license"] or not rec["desc"]:
            continue
        out.append(rec)
    out = out[:40]
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
        if key.startswith("gh_") and not key.startswith(("gh_new", "gh_topic_")) and res.ok:
            for it in res.items:
                if it["title"] not in slugs:
                    slugs.append(it["title"])
    if not slugs:
        return "nothing to enrich"
    found: dict[str, dict] = {}
    errors = []
    slugs = slugs[:75]   # three search calls at most; the search API allows 10 a minute without a token
    for i in range(0, len(slugs), 25):
        batch = slugs[i:i + 25]
        try:
            for r in github_search(" ".join(f"repo:{s}" for s in batch), 100):
                found[r["full_name"].lower()] = r
        except FetchError as exc:
            errors.append(str(exc))
            break
    for key, res in results.items():
        if key.startswith("gh_") and not key.startswith(("gh_new", "gh_topic_")):
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
            desc=clip(re.sub(r"\s+", " ", p.get("summary") or ""), 200),
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
            out.extend(_arxiv(cat, label, 5))
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
            desc=clip(strip_html(r.get("description") or ""), 200),
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
                    desc=clip(e["summary"], 140), author=e["author"], industry=niche) for e in recent[:limit]]
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

KEV_ALL: set[str] = set()


@source("kev", "CISA KEV · known exploited vulnerabilities (last 14 days)",
        "https://www.cisa.gov/known-exploited-vulnerabilities-catalog")
def src_kev():
    d = fetch_json("https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json")
    KEV_ALL.update(v.get("cveID") for v in d.get("vulnerabilities", []) if v.get("cveID"))
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
                        published=parse_dt(r.get("published_at"))))
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


# ---- Industry outlets, markets, preprints, launches -------------------------------------

for _k, _n, _u, _ind in INDUSTRY_FEEDS:
    _feed_source(_k, _n, _u, "news", 24 * 7, 6, _ind)


def _make_topic_source(topic: str, industry: str):
    @source(f"gh_topic_{topic}", f"GitHub · young repos tagged {topic}",
            f"https://github.com/topics/{topic}")
    def _src():
        since = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%d")
        rows = github_search(f"topic:{topic} created:>{since} fork:false archived:false stars:>=50", 30, sort="stars")
        out = []
        for r in rows:
            rec = repo_from_api(r)
            if rec["license"] and rec["desc"]:
                rec["industry"] = industry
                out.append(rec)
        return out[:10], f"GitHub search API: topic:{topic}, created in the last 90 days, 50+ stars, licence and description stated"
    return _src


for _t, _ind in GITHUB_TOPICS:
    _make_topic_source(_t, _ind)


@source("coingecko_trending", "CoinGecko · trending coins (searches, 24 h)", "https://www.coingecko.com/en/highlights/trending-crypto")
def src_coingecko_trending():
    d = fetch_json("https://api.coingecko.com/api/v3/search/trending")
    out = []
    for c in d.get("coins", []):
        it = c.get("item") or {}
        data = it.get("data") or {}
        out.append(item(
            "coin", f"{it.get('name')} ({(it.get('symbol') or '').upper()})",
            f"https://www.coingecko.com/en/coins/{it.get('id')}", mcap_rank=it.get("market_cap_rank"),
            price=data.get("price"), change_24h=(data.get("price_change_percentage_24h") or {}).get("usd"),
            mcap=data.get("market_cap"), industry="crypto-web3",
        ))
    return out[:15], "public API search/trending (ranked by CoinGecko search activity)"


@source("coingecko_markets", "CoinGecko · top 15 by market cap", "https://www.coingecko.com/")
def src_coingecko_markets():
    rows = fetch_json("https://api.coingecko.com/api/v3/coins/markets?" + urlencode(
        {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 15, "price_change_percentage": "24h,7d"}))
    out = [item(
        "coin", f"{r.get('name')} ({(r.get('symbol') or '').upper()})", f"https://www.coingecko.com/en/coins/{r.get('id')}",
        mcap_rank=r.get("market_cap_rank"), price=r.get("current_price"), change_24h=r.get("price_change_percentage_24h"),
        change_7d=r.get("price_change_percentage_7d_in_currency"), mcap=r.get("market_cap"),
        volume=r.get("total_volume"), industry="crypto-web3",
    ) for r in rows]
    return out, "public API coins/markets, USD"


@source("biorxiv", "bioRxiv and medRxiv · newest preprints", "https://www.biorxiv.org/")
def src_biorxiv():
    end = now_berlin().date() - timedelta(days=1)
    start = end - timedelta(days=1)
    out, failed = [], []
    for server in ("biorxiv", "medrxiv"):
        try:
            d = fetch_json(f"https://api.biorxiv.org/details/{server}/{start}/{end}/0")
        except FetchError as exc:
            failed.append(f"{server}: {exc}")
            continue
        seen = set()
        for r in d.get("collection", []):
            doi = r.get("doi")
            if doi in seen:
                continue
            seen.add(doi)
            authors = [a.strip() for a in (r.get("authors") or "").split(";") if a.strip()]
            out.append(item(
                "paper", r.get("title"), f"https://doi.org/{doi}", authors=authors,
                category=f"{'bioRxiv' if server == 'biorxiv' else 'medRxiv'} · {r.get('category')}",
                published=parse_dt(r.get("date")), desc=clip(re.sub(r"\s+", " ", r.get("abstract") or ""), 200),
                license=r.get("license") or "", industry="health-biotech",
            ))
            if len(seen) >= 8:
                break
    if not out:
        raise FetchError("; ".join(failed) or "no preprints")
    return out, f"public details API, first preprints posted {start} to {end}"


@source("launches", "Launch Library 2 · next orbital launches", "https://thespacedevs.com/llapi")
def src_launches():
    d = fetch_json("https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=10&mode=list")
    out = []
    for r in d.get("results", []):
        st = r.get("status") or {}
        out.append(item(
            "launch", r.get("name"), r.get("url") or "https://thespacedevs.com/llapi",
            provider=r.get("lsp_name"), net=parse_dt(r.get("net")), status=st.get("abbrev") or st.get("name"),
            status_desc=st.get("description"), pad=r.get("pad"), location=r.get("location"),
            mission_type=r.get("mission_type"), orbit=r.get("orbit"), industry="space-mobility",
        ))
    return out, "Launch Library 2 public API (The Space Devs), next 10 launches"


# ===========================================================================
# AI labs, AI media, AI newsletters, markets and economy, longer time windows
# ===========================================================================

GNEWS_HOST = "https://news.google.com"


def gnews(query: str, days: int, limit: int) -> list[dict]:
    """Google News public RSS search: headline, link, outlet, time. No summaries."""
    url = f"{GNEWS_HOST}/rss/search?" + urlencode({"q": f"{query} when:{days}d", "hl": "en-US", "gl": "US",
                                                     "ceid": "US:en"})
    root = fetch_xml(url)
    out = []
    for el in root.iter("item"):
        title = strip_html((el.findtext("title") or "").strip())
        link = (el.findtext("link") or "").strip()
        src = el.find("source")
        outlet = (src.text or "").strip() if src is not None else ""
        publisher = domain_of(src.attrib.get("url", "")) if src is not None else ""
        if outlet and title.endswith(" - " + outlet):
            title = title[: -len(outlet) - 3].strip()
        if title and link:
            out.append({"title": title, "url": link, "outlet": outlet or "Google News", "publisher": publisher,
                        "published": parse_dt(el.findtext("pubDate") or "")})
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    out.sort(key=lambda r: r["published"] or epoch, reverse=True)
    return out[:limit]


def gnews_page(query: str) -> str:
    return f"{GNEWS_HOST}/search?" + urlencode({"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})


def _gnews_source(key: str, name: str, query: str, days: int, limit: int, industry: str | None = None,
                  title_re: str | None = None, **extra):
    rx = re.compile(title_re, re.I) if title_re else None

    @source(key, name, gnews_page(query))
    def _src():
        rows = gnews(query, days, 40 if rx else limit)
        found = len(rows)
        if rx:
            rows = [r for r in rows if rx.search(r["title"])]
        out = [item("news", r["title"], r["url"], outlet=r["outlet"], publisher=r["publisher"], published=r["published"], desc="",
                    industry=industry, via="Google News", **extra) for r in rows[:limit]]
        note = f"Google News RSS search, last {days * 24} h, newest first (headline and outlet only)"
        if rx:
            note += f"; {len(rows)} of {found} headlines name the subject"
        return out, note
    return _src


# ---- AI labs and big players ---------------------------------------------------------
# slug, name, Google News query, blog feed keys, SDK repos, status key, OpenRouter prefixes, HF orgs, LMArena orgs
LABS = [
    ("anthropic", "Anthropic", '"Anthropic" OR "Claude AI"', ["anthropic_news"],
     ["anthropics/anthropic-sdk-python", "anthropics/claude-code"], "st_anthropic", ["anthropic"], [], ["anthropic"]),
    ("openai", "OpenAI", '"OpenAI"', ["openai_news"], ["openai/openai-python", "openai/codex"], "st_openai",
     ["openai"], ["openai"], ["openai"]),
    ("google", "Google DeepMind & Gemini", '"Google DeepMind" OR "Gemini" Google AI', ["google_ai", "deepmind", "gemini_blog"],
     ["googleapis/python-genai", "google-gemini/gemini-cli"], None, ["google"], ["google"], ["google"]),
    ("meta", "Meta AI", '"Meta AI" OR "Meta Superintelligence" OR "Llama" Meta', [], [], None,
     ["meta-llama"], ["meta-llama", "facebook"], ["meta"]),
    ("microsoft", "Microsoft AI", '"Microsoft AI" OR "Microsoft Copilot"', ["ms_ai"], ["microsoft/semantic-kernel"], None,
     ["microsoft"], ["microsoft"], ["microsoft"]),
    ("xai", "xAI", '"xAI" Musk AI', [], ["xai-org/xai-sdk-python"], None, ["x-ai"], ["xai-org"], ["xai"]),
    ("mistral", "Mistral AI", '"Mistral AI"', [], ["mistralai/client-python"], "st_mistral", ["mistralai"],
     ["mistralai"], ["mistral"]),
    ("cohere", "Cohere", '"Cohere" AI', [], ["cohere-ai/cohere-python"], "st_cohere", ["cohere"], ["CohereLabs"],
     ["cohere"]),
    ("nvidia", "NVIDIA", 'Nvidia AI', ["nvidia_blog"], ["NVIDIA/TensorRT-LLM"], None, ["nvidia"], ["nvidia"], ["nvidia"]),
    ("amazon", "Amazon & AWS", '"Amazon" AI (Bedrock OR Nova OR AWS)', ["aws_ml"], [], None, ["amazon"], ["amazon"],
     ["amazon"]),
    ("apple", "Apple", '"Apple Intelligence" OR "Apple AI"', ["apple_ml"], ["ml-explore/mlx"], None, [], ["apple"],
     ["apple"]),
    ("deepseek", "DeepSeek", 'DeepSeek', [], [], None, ["deepseek"], ["deepseek-ai"], ["deepseek"]),
    ("qwen", "Qwen & Alibaba", 'Qwen OR "Alibaba" AI model', [], ["QwenLM/qwen-code"], None, ["qwen"],
     ["Qwen"], ["alibaba", "qwen"]),
    ("moonshot", "Moonshot AI (Kimi)", '"Moonshot AI" OR Kimi AI', [], ["MoonshotAI/kimi-cli"], None, ["moonshotai"],
     ["moonshotai"], ["moonshot"]),
    ("zhipu", "Zhipu (Z.ai, GLM)", 'Zhipu OR "Z.ai" GLM', [], [], None, ["z-ai"], ["zai-org"], ["zhipu", "z.ai", "zai"]),
    ("perplexity", "Perplexity", '"Perplexity AI" OR "Perplexity" Comet', [], [], "st_perplexity", ["perplexity"], [],
     ["perplexity"]),
    ("huggingface", "Hugging Face", '"Hugging Face"', ["hf_blog"], ["huggingface/transformers"], None, [], [], []),
    ("stability", "Stability AI", '"Stability AI"', [], ["Stability-AI/generative-models"], None, [], ["stabilityai"],
     ["stability"]),
]
LAB = {lab[0]: lab for lab in LABS}

LAB_FEEDS_EXTRA = [
    ("gemini_blog", "Google · Gemini blog", "https://blog.google/products/gemini/rss/"),
    ("ms_ai", "Microsoft Source · AI", "https://news.microsoft.com/source/topics/ai/feed/"),
    ("nvidia_blog", "NVIDIA blog", "https://blogs.nvidia.com/feed/"),
    ("aws_ml", "AWS Machine Learning blog", "https://aws.amazon.com/blogs/machine-learning/feed/"),
    ("apple_ml", "Apple Machine Learning Research", "https://machinelearning.apple.com/rss.xml"),
    ("elevenlabs_blog", "ElevenLabs blog", "https://elevenlabs.io/blog/rss.xml"),
]
for _k, _n, _u in LAB_FEEDS_EXTRA:
    _feed_source(_k, _n, _u, "lab", 24 * 14, 5, "ai-media" if _k == "elevenlabs_blog" else "ai-llms")


@source("anthropic_news", "Anthropic · newsroom (public sitemap)", "https://www.anthropic.com/news")
def src_anthropic_news():
    body = fetch("https://www.anthropic.com/sitemap.xml")
    ref = datetime.now(timezone.utc)
    rows = []
    for loc, lastmod in re.findall(r"<loc>\s*([^<]+?)\s*</loc>\s*(?:<lastmod>\s*([^<]+?)\s*</lastmod>)?", body):
        if not re.match(r"https://www\.anthropic\.com/news/[\w-]+$", loc):
            continue
        dt = parse_dt(lastmod)
        if within(dt, 24 * 14, ref):
            slug = loc.rsplit("/", 1)[-1]
            title = slug.replace("-", " ").strip().capitalize()
            rows.append(item("lab", title, loc, outlet="Anthropic", published=dt, desc="", industry="ai-llms",
                             title_from_url=True))
    rows.sort(key=lambda x: x["published"], reverse=True)
    rows = rows[:8]
    titled = 0
    for it in rows:   # the sitemap has no titles: read each page's own og:title and description (robots.txt allows it)
        try:
            page = fetch(it["url"])
        except FetchError:
            continue
        t = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', page)
        d = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', page)
        if t:
            it["title"] = htmlmod.unescape(t.group(1)).strip()
            it["title_from_url"] = False
            titled += 1
        if d:
            it["desc"] = clip(htmlmod.unescape(d.group(1)).strip(), 200)
    return rows, (f"public sitemap.xml, news pages changed in the last 14 days; titles and summaries from each page's "
                  f"own meta tags ({titled} of {len(rows)} read; the rest show the page address in words); the date is "
                  "the page's last change")


LAB_TITLE_RE = {
    "anthropic": r"anthropic|claude", "openai": r"openai|chatgpt|altman|\bgpt-?\d|\bsora\b|\bcodex\b",
    "google": r"gemini|deepmind|google", "meta": r"\bmeta\b|llama|zuckerberg", "microsoft": r"microsoft|copilot",
    "xai": r"\bxai\b|musk", "mistral": r"mistral", "cohere": r"cohere", "nvidia": r"nvidia|jensen huang",
    "amazon": r"amazon|\baws\b|bedrock", "apple": r"\bapple\b|siri", "deepseek": r"deepseek",
    "qwen": r"qwen|alibaba", "moonshot": r"moonshot|\bkimi\b", "zhipu": r"zhipu|z\.ai|\bglm",
    "perplexity": r"perplexity", "huggingface": r"hugging ?face", "stability": r"stability ai|stable diffusion",
}
for _slug, _name, _q, *_rest in LABS:
    _gnews_source(f"lab_news_{_slug}", f"Google News · {_name}", _q, 2, 8, "ai-llms", LAB_TITLE_RE[_slug], lab=_slug)


for _k, _n, _u in [
    ("st_anthropic", "Anthropic", "https://status.anthropic.com/api/v2/incidents.json"),
    ("st_openai", "OpenAI", "https://status.openai.com/api/v2/incidents.json"),
    ("st_mistral", "Mistral AI", "https://status.mistral.ai/api/v2/incidents.json"),
    ("st_cohere", "Cohere", "https://status.cohere.com/api/v2/incidents.json"),
    ("st_perplexity", "Perplexity", "https://status.perplexity.com/api/v2/incidents.json"),
    ("st_elevenlabs", "ElevenLabs", "https://status.elevenlabs.io/api/v2/incidents.json"),
]:
    _status_source(_k, _n, _u)

AI_STATUS_KEYS = ["st_anthropic", "st_openai", "st_mistral", "st_cohere", "st_perplexity", "st_elevenlabs"]


@source("lab_releases", "GitHub releases · AI lab SDKs and tools (last 14 days)", "https://github.com/")
def src_lab_releases():
    ref = datetime.now(timezone.utc)
    out, failed, repos = [], 0, []
    for lab in LABS:
        repos += [(lab[0], r) for r in lab[4]]
    for slug, repo in repos:
        try:
            entries = parse_feed(fetch_xml(f"https://github.com/{repo}/releases.atom"))
        except FetchError:
            failed += 1
            continue
        kept = 0
        for e in entries[:6]:
            if kept >= 2:
                break
            if within(e["published"], 24 * 14, ref):
                kept += 1
                tag = e["url"].rsplit("/tag/", 1)[-1] if "/tag/" in e["url"] else e["title"]
                out.append(item("release", f"{repo} {e['title']}", e["url"], project=repo, tag=tag,
                                release_title=e["title"], published=e["published"], lab=slug,
                                prerelease=bool(re.search(r"(rc|alpha|beta|preview|nightly|canary|dev)", tag, re.I))))
    if failed == len(repos):
        raise FetchError("no release feed responded")
    out.sort(key=lambda x: x["published"], reverse=True)
    note = f"public releases.atom feeds of {len(repos)} lab repositories, up to 2 releases each"
    return out, note + (f" ({failed} feeds did not respond)" if failed else "")


def _lab_of_model_id(model_id: str) -> str | None:
    pre = model_id.split("/", 1)[0].lower()
    for lab in LABS:
        if pre in [p.lower() for p in lab[6]] or pre in [o.lower() for o in lab[7]]:
            return lab[0]
    return None


@source("lab_models", "OpenRouter · models added by the big labs (last 60 days)", "https://openrouter.ai/models")
def src_lab_models():
    data = fetch_json("https://openrouter.ai/api/v1/models")
    ref = datetime.now(timezone.utc)
    out, seen = [], set()
    for r in sorted(data.get("data", []), key=lambda r: r.get("created") or 0, reverse=True):
        base = (r.get("id") or "").split(":", 1)[0]
        lab = _lab_of_model_id(base)
        created = parse_dt(r.get("created"))
        if not lab or base in seen or not within(created, 24 * 60, ref):
            continue
        seen.add(base)
        pr = r.get("pricing") or {}

        def per_m(v):
            try:
                return round(float(v) * 1_000_000, 3)
            except (TypeError, ValueError):
                return None
        out.append(item("llm", r.get("name") or base, f"https://openrouter.ai/{base}", model_id=base, lab=lab,
                        context=r.get("context_length"), price_in=per_m(pr.get("prompt")),
                        price_out=per_m(pr.get("completion")), created=created, published=created,
                        modality=((r.get("architecture") or {}).get("modality") or ""),
                        desc=clip(strip_html(r.get("description") or ""), 200)))
    return out[:40], "public models API, models whose id starts with a tracked lab, newest first"


@source("lab_hf", "Hugging Face · newest open-weight models from the big labs (last 30 days)",
        "https://huggingface.co/models?sort=created")
def src_lab_hf():
    ref = datetime.now(timezone.utc)
    out, failed, orgs = [], 0, []
    for lab in LABS:
        orgs += [(lab[0], o) for o in lab[7]]
    for slug, org in orgs:
        try:
            rows = fetch_json(f"https://huggingface.co/api/models?author={org}&sort=createdAt&limit=4")
        except FetchError:
            failed += 1
            continue
        for r in rows:
            created = parse_dt(r.get("createdAt"))
            if within(created, 24 * 30, ref):
                out.append(item("model", r["id"], f"https://huggingface.co/{r['id']}", task=r.get("pipeline_tag") or "",
                                library=r.get("library_name") or "", downloads=r.get("downloads"),
                                likes=r.get("likes"), license=_hf_license(r.get("tags")), created=created,
                                published=created, lab=slug))
    if failed == len(orgs):
        raise FetchError("Hub API did not respond")
    out.sort(key=lambda x: x["created"], reverse=True)
    return out[:40], f"Hub API, newest models of {len(orgs)} lab organisations" + (
        f" ({failed} did not respond)" if failed else "")


def _arena(config: str, n: int):
    url = ("https://datasets-server.huggingface.co/rows?" +
           urlencode({"dataset": "lmarena-ai/leaderboard-dataset", "config": config, "split": "latest",
                      "offset": 0, "length": 100}))
    d = fetch_json(url)
    rows = [r["row"] for r in d.get("rows", []) if (r.get("row") or {}).get("category") == "overall"]
    rows.sort(key=lambda r: r.get("rank") or 9999)
    out = []
    for r in rows[:n]:
        org = r.get("organization") or ""
        lab = next((lab[0] for lab in LABS if org.lower() in lab[8]), None)
        out.append(item("arena", r.get("model_name") or "", "https://lmarena.ai/leaderboard", org=org, lab=lab,
                        rank=parse_int(r.get("rank")), rating=r.get("rating"), votes=parse_int(r.get("vote_count")),
                        license=r.get("license") or "", board=config, asof=r.get("leaderboard_publish_date") or ""))
    date = out[0]["asof"] if out else "?"
    return out, f"LMArena leaderboard dataset on Hugging Face (CC BY 4.0), '{config}' overall, published {date}"


@source("arena_text", "LMArena · text leaderboard", "https://lmarena.ai/leaderboard/text")
def src_arena_text():
    return _arena("text", 15)


@source("arena_image", "LMArena · text-to-image leaderboard", "https://lmarena.ai/leaderboard/text-to-image")
def src_arena_image():
    return _arena("text_to_image", 10)


@source("arena_video", "LMArena · text-to-video leaderboard", "https://lmarena.ai/leaderboard/text-to-video")
def src_arena_video():
    return _arena("text_to_video", 10)


# ---- AI media: video, image, audio and voice -------------------------------------------
MEDIA_PROVIDERS = [
    ("OpenAI Sora", r"\bsora\b"), ("Google Veo", r"\bveo ?\d*\b"), ("Google Nano Banana", r"nano banana"),
    ("Runway", r"\brunway(ml)?\b"), ("Luma AI", r"\bluma (ai|labs)\b|dream machine"), ("Pika", r"\bpika\b"),
    ("Kling", r"\bkling\b"), ("MiniMax Hailuo", r"\bhailuo\b|\bminimax\b"), ("Higgsfield", r"\bhiggsfield\b"),
    ("Midjourney", r"\bmidjourney\b"), ("Black Forest Labs (FLUX)", r"black forest labs|\bflux\.?\d"),
    ("Stability AI", r"stability ai|stable (diffusion|audio|video)"), ("ElevenLabs", r"\belevenlabs?\b"),
    ("Suno", r"\bsuno\b"), ("Udio", r"\budio\b"), ("HeyGen", r"\bheygen\b"), ("Synthesia", r"\bsynthesia\b"),
    ("Adobe Firefly", r"\bfirefly\b"), ("Ideogram", r"\bideogram\b"), ("Krea", r"\bkrea\b"),
]
MEDIA_RE = [(n, re.compile(rx, re.I)) for n, rx in MEDIA_PROVIDERS]
MEDIA_QUERIES = [
    ("media_news_1", "Sora, Veo, Runway", 'Sora OpenAI video OR "Google Veo" OR "Runway" AI video'),
    ("media_news_2", "Luma, Pika, Kling", '"Luma AI" OR "Pika" AI video OR "Kling" AI'),
    ("media_news_3", "Hailuo, Higgsfield, Midjourney", 'Hailuo OR MiniMax video OR Higgsfield OR Midjourney'),
    ("media_news_4", "FLUX, ElevenLabs, Suno", '"Black Forest Labs" OR FLUX image model OR ElevenLabs OR Suno'),
    ("media_news_5", "Udio, HeyGen, Synthesia", 'Udio OR HeyGen OR Synthesia OR "Nano Banana"'),
]
for _k, _label, _q in MEDIA_QUERIES:
    _gnews_source(_k, f"Google News · AI media ({_label})", _q, 3, 10, "ai-media",
                  "|".join(rx for _n, rx in MEDIA_PROVIDERS) + r"|ai video|text-to-video|image generat|video generat")


def media_provider(text: str) -> str | None:
    for n, rx in MEDIA_RE:
        if rx.search(text or ""):
            return n
    return None


HF_MEDIA_TASKS = ["text-to-video", "image-to-video", "text-to-image", "text-to-speech", "text-to-audio"]


@source("hf_media", "Hugging Face · trending video, image and audio models", "https://huggingface.co/models?sort=trending")
def src_hf_media():
    out, failed = [], 0
    for task in HF_MEDIA_TASKS:
        try:
            rows = fetch_json(f"https://huggingface.co/api/models?pipeline_tag={task}&sort=trendingScore&limit=6")
        except FetchError:
            failed += 1
            continue
        for r in rows:
            out.append(item("model", r["id"], f"https://huggingface.co/{r['id']}", task=task,
                            library=r.get("library_name") or "", downloads=r.get("downloads"), likes=r.get("likes"),
                            license=_hf_license(r.get("tags")), created=parse_dt(r.get("createdAt")),
                            industry="ai-media"))
    if failed == len(HF_MEDIA_TASKS):
        raise FetchError("Hub API did not respond")
    return out, "Hub API sort=trendingScore, top 6 for each of " + ", ".join(HF_MEDIA_TASKS)


# ---- AI newsletters and news sites ------------------------------------------------------
AI_NEWS_FEEDS = [
    ("decoder", "The Decoder", "https://the-decoder.com/feed/"),
    ("tc_ai", "TechCrunch · AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("mittr_ai", "MIT Technology Review · AI", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
    ("importai", "Import AI", "https://importai.substack.com/feed"),
    ("latent", "Latent Space", "https://www.latent.space/feed"),
    ("bensbites", "Ben's Bites", "https://www.bensbites.com/feed"),
    ("lwiai", "Last Week in AI", "https://lastweekin.ai/feed"),
    ("tldr_ai", "TLDR AI", "https://tldr.tech/api/rss/ai"),
    ("rundown", "The Rundown AI", "https://www.therundown.ai/feed"),
    ("interconnects", "Interconnects", "https://www.interconnects.ai/feed"),
]
for _k, _n, _u in AI_NEWS_FEEDS:
    _feed_source(_k, _n, _u, "news", 24 * 7, 6, "ai-llms")


# ---- Markets and economy ------------------------------------------------------------------
MARKET_FEEDS = [
    # key, name, feed, hours, limit, industry (None = keyword rules only)
    ("cnbc_top", "CNBC · top news", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114", 36, 8, "markets-economy"),
    ("cnbc_markets", "CNBC · markets", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258", 36, 8, "markets-economy"),
    ("cnbc_tech", "CNBC · technology", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910", 36, 8, None),
    ("mw_top", "MarketWatch · top stories", "https://feeds.content.dowjones.io/public/rss/mw_topstories", 36, 8, "markets-economy"),
    ("bbg_markets", "Bloomberg · markets", "https://feeds.bloomberg.com/markets/news.rss", 36, 8, "markets-economy"),
    ("bbg_tech", "Bloomberg · technology", "https://feeds.bloomberg.com/technology/news.rss", 36, 8, None),
    ("bbg_econ", "Bloomberg · economics", "https://feeds.bloomberg.com/economics/news.rss", 36, 8, "markets-economy"),
    ("ft_home", "Financial Times · home", "https://www.ft.com/rss/home", 36, 8, "markets-economy"),
    ("ft_tech", "Financial Times · technology", "https://www.ft.com/technology?format=rss", 36, 8, None),
    ("nyt_biz", "New York Times · business", "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", 36, 8, "markets-economy"),
    ("nyt_tech", "New York Times · technology", "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", 36, 8, None),
    ("bbc_biz", "BBC · business", "https://feeds.bbci.co.uk/news/business/rss.xml", 36, 8, "markets-economy"),
    ("guardian_biz", "The Guardian · business", "https://www.theguardian.com/uk/business/rss", 36, 8, "markets-economy"),
    ("economist_fin", "The Economist · finance and economics", "https://www.economist.com/finance-and-economics/rss.xml", 24 * 7, 6, "markets-economy"),
    ("theinformation", "The Information", "https://www.theinformation.com/feed", 72, 8, None),
    ("crunchbase", "Crunchbase News", "https://news.crunchbase.com/feed/", 72, 8, "markets-economy"),
    ("tc_venture", "TechCrunch · venture", "https://techcrunch.com/category/venture/feed/", 72, 8, "markets-economy"),
    ("ecb_press", "European Central Bank · press", "https://www.ecb.europa.eu/rss/press.html", 24 * 7, 6, "markets-economy"),
    ("fed_press", "Federal Reserve · press releases", "https://www.federalreserve.gov/feeds/press_all.xml", 24 * 7, 6, "markets-economy"),
]
for _k, _n, _u, _h, _l, _i in MARKET_FEEDS:
    _feed_source(_k, _n, _u, "news", _h, _l, _i)

DEAL_QUERIES = [
    ("deals_funding", "funding rounds and acquisitions", 'startup raises funding round OR tech acquisition acquires'),
    ("deals_ipo", "IPOs and layoffs", 'tech IPO shares debut OR tech layoffs job cuts'),
]
for _k, _label, _q in DEAL_QUERIES:
    _gnews_source(_k, f"Google News · {_label}", _q, 2, 10, "markets-economy", deal=_label)


FRED_SERIES = [
    # series, label, unit, kind of change shown
    ("SP500", "S&P 500", "index", "pct"), ("NASDAQCOM", "Nasdaq Composite", "index", "pct"),
    ("DJIA", "Dow Jones Industrial Average", "index", "pct"), ("VIXCLS", "VIX volatility index", "index", "pct"),
    ("DGS10", "US 10-year Treasury yield", "%", "bp"), ("DCOILBRENTEU", "Brent crude oil", "USD/bbl", "pct"),
]


@source("fred", "FRED · US markets and rates (St. Louis Fed)", "https://fred.stlouisfed.org/")
def src_fred():
    start = (datetime.now(timezone.utc) - timedelta(days=21)).strftime("%Y-%m-%d")
    out, failed = [], 0
    for sid, label, unit, chg in FRED_SERIES:
        try:
            body = fetch(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={start}")
        except FetchError:
            failed += 1
            continue
        obs = []
        for line in body.splitlines()[1:]:
            parts = line.split(",")
            if len(parts) == 2:
                try:
                    obs.append((parts[0], float(parts[1])))
                except ValueError:
                    pass   # FRED writes "." for days without a value
        if len(obs) < 2:
            continue
        (d0, v0), (d1, v1) = obs[-2], obs[-1]
        change = (v1 - v0) * 100 if chg == "bp" else (v1 / v0 - 1) * 100
        out.append(item("quote", label, f"https://fred.stlouisfed.org/series/{sid}", value=v1, prev=v0, asof=d1,
                        prev_date=d0, unit=unit, change=change, change_kind=chg, series=sid, outlet="FRED"))
    if not out:
        raise FetchError("no FRED series answered")
    return out, "fredgraph.csv, last two published observations (FRED publishes with a delay of one or more days)" + (
        f"; {failed} series did not respond" if failed else "")


@source("ecb_fx", "ECB · euro reference rate (USD)", "https://data.ecb.europa.eu/data/datasets/EXR")
def src_ecb_fx():
    d = fetch_json("https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=2&format=jsondata")
    try:
        dates = [v["id"] for v in d["structure"]["dimensions"]["observation"][0]["values"]]
        series = next(iter(d["dataSets"][0]["series"].values()))["observations"]
        vals = [series[str(i)][0] for i in range(len(dates))]
    except (KeyError, IndexError, StopIteration, TypeError):
        raise FetchError("unexpected ECB response")
    if len(vals) < 2:
        raise FetchError("fewer than two observations")
    return [item("quote", "EUR/USD (ECB reference rate)", "https://data.ecb.europa.eu/data/datasets/EXR",
                 value=vals[-1], prev=vals[-2], asof=dates[-1], prev_date=dates[-2], unit="USD per EUR",
                 change=(vals[-1] / vals[-2] - 1) * 100, change_kind="pct", outlet="ECB")], \
        "ECB Data Portal API, daily euro foreign exchange reference rate"


# ---- Longer time windows (native period endpoints) -----------------------------------------
WINDOW_OF = {
    "gh_weekly": "week", "gh_new": "week", "hn_best": "week", "devto_week": "week", "hf_papers_week": "week",
    "gh_monthly": "month", "gh_new_month": "month", "hn_month": "month", "devto_month": "month",
    "hf_papers_month": "month",
    "gh_new_year": "year", "hn_year": "year", "devto_year": "year",
}


@source("gh_monthly", "GitHub trending · this month", "https://github.com/trending?since=monthly")
def src_gh_monthly():
    return _trending("", "monthly", "this month", 25)


def _gh_created(days: int, keep: int):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = github_search(f"created:>{since} fork:false archived:false", 100, sort="stars")
    out = [r for r in (repo_from_api(x) for x in rows) if r["license"] and r["desc"]][:keep]
    return out, (f"GitHub search API, created since {since}, sorted by stars; {len(out)} repos that state a "
                 "licence and a description")


@source("gh_new_month", "GitHub · most-starred repos created in the last 30 days",
        "https://docs.github.com/en/rest/search/search#search-repositories")
def src_gh_new_month():
    return _gh_created(30, 25)


@source("gh_new_year", "GitHub · most-starred repos created in the last 365 days",
        "https://docs.github.com/en/rest/search/search#search-repositories")
def src_gh_new_year():
    return _gh_created(365, 25)


@source("hn_month", "Hacker News · best of the last 30 days", "https://news.ycombinator.com/best")
def src_hn_month():
    out = _hn({"tags": "story", "numericFilters": f"created_at_i>{_since(24 * 30)},points>500", "hitsPerPage": 200}, 200)
    out.sort(key=lambda x: x.get("points") or 0, reverse=True)
    return out[:20], "Algolia HN API, stories from the last 30 days with 500+ points, sorted by points"


@source("hn_year", "Hacker News · best of the last 365 days", "https://news.ycombinator.com/best")
def src_hn_year():
    out = _hn({"tags": "story", "numericFilters": f"created_at_i>{_since(24 * 365)},points>1500", "hitsPerPage": 300}, 300)
    out.sort(key=lambda x: x.get("points") or 0, reverse=True)
    return out[:20], "Algolia HN API, stories from the last 365 days with 1,500+ points, sorted by points"


@source("devto_month", "Dev.to · top this month", "https://dev.to/top/month")
def src_devto_month():
    return _devto({"top": 30, "per_page": 15}), "Forem API top=30"


@source("devto_year", "Dev.to · top this year", "https://dev.to/top/year")
def src_devto_year():
    return _devto({"top": 365, "per_page": 15}), "Forem API top=365"


def _hf_period_papers(param: str, value: str):
    rows = fetch_json(f"https://huggingface.co/api/daily_papers?{param}={value}&limit=100")
    out = []
    for r in rows:
        p = r.get("paper") or {}
        pid = p.get("id") or ""
        out.append(item(
            "paper", p.get("title") or r.get("title") or "", f"https://huggingface.co/papers/{pid}", arxiv=pid,
            authors=[a.get("name") for a in p.get("authors", []) if a.get("name")], upvotes=p.get("upvotes"),
            comments=r.get("numComments"), github=p.get("githubRepo") or "", github_stars=p.get("githubStars"),
            published=parse_dt(p.get("publishedAt")), category=f"HF papers ({value})",
            desc=clip(re.sub(r"\s+", " ", p.get("summary") or ""), 200)))
    out.sort(key=lambda x: x.get("upvotes") or 0, reverse=True)
    return out[:20], f"daily_papers API {param}={value}, sorted by community upvotes"


@source("hf_papers_week", "Hugging Face · papers of the week", "https://huggingface.co/papers")
def src_hf_papers_week():
    y, w, _ = now_berlin().isocalendar()
    return _hf_period_papers("week", f"{y}-W{w:02d}")


@source("hf_papers_month", "Hugging Face · papers of the month", "https://huggingface.co/papers")
def src_hf_papers_month():
    return _hf_period_papers("month", now_berlin().strftime("%Y-%m"))


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


def table(headers: list[str], rows: list[list[str]], numbered: bool = True) -> str:
    if numbered:
        headers = ["#"] + headers
        rows = [[str(n)] + r for n, r in enumerate(rows, 1)]
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out += ["| " + " | ".join(c if c else "—" for c in r) + " |" for r in rows]
    return "\n".join(out)



def _table_with_numbers(headers: list[str], rows: list[list[str]]) -> str:
    return table(["#"] + headers, rows, numbered=False)


LICENSE_LINE = (
    "- License: [OpenRoots Agent License 2.3](LICENSE) (SPDX `LicenseRef-OpenRoots-ORA-2.3`). Free and unconditional at or below "
    "USD 20,000,000 annual revenue, and for any individual, nonprofit, school, or government body at any size. Above that "
    "threshold, a small self-reported royalty applies, capped per year. AI training on this work is not granted by either "
    "tier and needs a separate Compute license; human reading and search indexing are unaffected. Canonical text: "
    "[openroots.org/licenses/ora/2.3](https://openroots.org/licenses/ora/2.3)."
)



# ---------------------------------------------------------------------------
# Archive handling
# ---------------------------------------------------------------------------

_EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2B07\u2705\uFE0F\u200d]")


def _no_emoji(text: str) -> str:
    """Drop emoji characters that arrive inside third-party titles and descriptions."""
    return re.sub(r"  +", " ", _EMOJI_RE.sub("", text)) if False else _EMOJI_RE.sub("", text)


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




# ---------------------------------------------------------------------------
# Industry taxonomy (multi-label, transparent rules). See docs/methodology.md.
# ---------------------------------------------------------------------------

INDUSTRIES = [
    # slug, emoji, title, short label, one-line scope, keyword regex, GitHub topics
    ("ai-llms", "", "AI & LLMs", "AI",
     "Foundation models, inference, ML research and the labs behind them.",
     r"\b(ai|a\.i\.|artificial intelligence|llms?|gpt[-\w.]*|chatgpt|openai|anthropic|claude|gemini|llama|qwen|mistral|"
     r"deepseek|transformers?|diffusion|inference|fine-?tun\w*|machine learning|deep learning|neural|embeddings?|"
     r"rag|vllm|ollama|pytorch|tensorflow|multimodal|vision-language|language models?|reasoning model|"
     r"text-generation|text-to-\w+|image-text-to-text|hugging ?face|openvino|copilot)\b",
     {"machine-learning", "deep-learning", "llm", "llms", "artificial-intelligence", "ai", "nlp", "pytorch",
      "transformers", "large-language-models", "generative-ai", "computer-vision", "openai", "llama"}),
    ("ai-agents", "", "AI agents & MCP", "Agents",
     "Agent frameworks, skills, tool use and Model Context Protocol servers.",
     r"\b(agents?|agentic|mcp|model context protocol|agent skills?|skills? (bundle|library|framework)|"
     r"claude code|codex|coding agents?|autonomous agents?|crewai|langgraph|autogen|tool[- ]calling|a2a|"
     r"computer[- ]use|browser[- ]use|sandbox(es|ed)?)\b",
     {"ai-agents", "agents", "mcp", "mcp-server", "model-context-protocol", "agent-skills", "claude-code",
      "agentic-ai", "ai-agent", "llm-agents", "autonomous-agents"}),
    ("ai-media", "", "AI media: video, image, audio & voice", "AI media",
     "Generative video, image, music, speech and voice models and the companies that make them.",
     r"\b(text-to-(video|image|speech|audio|music)|image-to-video|video generat\w*|image generat\w*|ai video|ai images?|"
     r"generative video|sora|veo ?\d*|runway(ml)?|kling|hailuo|higgsfield|midjourney|black forest labs|flux\.\d|"
     r"stable diffusion|stability ai|elevenlabs?|suno|udio|heygen|synthesia|nano banana|firefly|ideogram|luma ai|"
     r"dream machine|tts|speech synthesis|voice clon\w*|voice ai|music generat\w*|lip-?sync|diffusion models?|comfyui)\b",
     {"text-to-video", "text-to-image", "stable-diffusion", "diffusion-models", "tts", "text-to-speech", "voice-cloning",
      "image-generation", "video-generation", "comfyui", "speech-synthesis", "music-generation"}),
    ("devtools", "", "Developer tools", "Dev tools",
     "Languages, editors, CLIs, package ecosystems and the software toolchain.",
     r"\b(cli|ide|editor|vs ?code|vim|neovim|emacs|plugins?|sdk|compiler|debugg\w*|linters?|terminal|git|"
     r"package manager|npm|pypi|crates?\.io|cargo|rustc?|golang|python|typescript|javascript|zig|ruff|deno|"
     r"bun|node\.?js|refactor\w*|developers?|devtools?|programming|open[- ]source)\b",
     {"cli", "developer-tools", "devtools", "rust", "golang", "python", "typescript", "compiler", "neovim",
      "vscode", "terminal", "git", "programming-language"}),
    ("cloud-devops", "", "Cloud & DevOps", "Cloud",
     "Infrastructure, containers, CI/CD, self-hosting, outages and operations.",
     r"\b(devops|kubernetes|k8s|docker|containers?|helm|terraform|ansible|ci/?cd|aws|azure|gcp|google cloud|"
     r"cloud|serverless|nginx|linux|kernel|self-host\w*|homelab|observability|grafana|prometheus|sre|outages?|"
     r"incident|hetzner|cloudflare|data ?cent(er|re)s?|infrastructure)\b",
     {"kubernetes", "docker", "devops", "terraform", "self-hosted", "cloud", "aws", "observability",
      "infrastructure", "homelab", "linux"}),
    ("cybersecurity", "", "Cybersecurity", "Security",
     "Exploited and new vulnerabilities, attacks, defence and security tooling.",
     r"\b(security|vulnerab\w*|cve-\d+|exploit\w*|malware|ransomware|phishing|breach\w*|pentest\w*|red[- ]team|"
     r"bug[- ]?bount\w*|bug hunt\w*|zero-day|0-day|backdoor|cryptography|authentication bypass|xss|rce|"
     r"privilege escalation|supply[- ]chain attack|cyber\w*|infosec|hackers?|spyware|botnet|ddos)\b",
     {"security", "cybersecurity", "pentesting", "penetration-testing", "red-team", "bug-bounty", "malware",
      "vulnerability", "infosec", "ai-security", "osint", "ctf"}),
    ("data-analytics", "", "Data & analytics", "Data",
     "Databases, datasets, pipelines, analytics and BI.",
     r"\b(databases?|postgres\w*|sqlite|mysql|duckdb|clickhouse|polars|pandas|spark|kafka|airflow|parquet|"
     r"iceberg|etl|data pipelines?|datasets?|data engineering|vector (db|database)|analytics|olap|warehouse)\b",
     {"database", "data-engineering", "analytics", "postgresql", "sql", "etl", "data-science", "dataset",
      "vector-database", "big-data"}),
    ("web-frontend", "", "Web & frontend", "Web",
     "Browsers, front-end frameworks, CSS, web platform and the CDN layer.",
     r"\b(frontend|front-end|web apps?|web development|web framework|web platform|web standards?|browsers?|css|"
     r"html|react|next\.js|nextjs|vue|svelte|angular|tailwind|webassembly|wasm|chrome|firefox|safari|webgpu)\b",
     {"react", "nextjs", "vue", "svelte", "css", "frontend", "web", "tailwindcss", "webassembly", "javascript"}),
    ("mobile", "", "Mobile", "Mobile",
     "iOS, Android, phones, wearables and app stores.",
     r"\b(ios|ipados|android|iphone|ipad|app store|google play|mobile|react native|flutter|swiftui|swift|kotlin|"
     r"jetpack|xcode|testflight|smartphones?|samsung galaxy|pixel \d+|whatsapp|apple watch|wearables?)\b",
     {"ios", "android", "flutter", "react-native", "swift", "kotlin", "mobile", "swiftui"}),
    ("markets-economy", "", "Markets & economy", "Markets",
     "Stocks, rates, inflation, central banks, earnings, funding rounds, M&A, IPOs and layoffs.",
     r"\b(stocks?|shares (fell|rose|jumped|slid|surged|sank|climbed|dropped)|wall street|nasdaq|s&p 500|s&p|dow jones|"
     r"dax|ftse|nikkei|bonds?|treasur(y|ies)|yields?|interest rates?|rate (cut|hike)s?|inflation|cpi|gdp|recession|"
     r"central banks?|federal reserve|the fed|ecb|earnings|quarterly results|revenue|profits?|valuations?|ipos?|"
     r"acquisitions?|acquires?|acquired|mergers?|m&a|takeover|funding rounds?|raises \$[\d.]+|series [a-f]|venture capital|"
     r"investors?|layoffs?|job cuts|tariffs?|econom(y|ic|ies)|oil prices?|gold prices?|dollar|bitcoin etf|market cap)\b",
     {"finance", "stock-market", "trading", "economics", "quantitative-finance"}),
    ("fintech", "", "Fintech & payments", "Fintech",
     "Banking, payments, lending, trading, insurance and finance infrastructure.",
     r"\b(fintech|payments?|banks?|banking|neobank|stripe|paypal|visa|mastercard|klarna|adyen|lending|loans?|"
     r"credit cards?|trading|brokerage|insurtech|insurance|remittances?|open banking|financial)\b",
     {"fintech", "payments", "banking", "trading", "finance", "quantitative-finance", "algorithmic-trading"}),
    ("crypto-web3", "", "Crypto & web3", "Crypto",
     "Cryptocurrencies, blockchains, DeFi, stablecoins and tokenisation.",
     r"\b(crypto\w*|bitcoin|btc|ethereum|eth|solana|blockchains?|web3|defi|stablecoins?|tokens? (sale|launch)|"
     r"nfts?|coinbase|binance|monero|xrp|tokeni[sz]\w*)\b",
     {"blockchain", "cryptocurrency", "ethereum", "bitcoin", "solana", "web3", "defi", "smart-contracts", "crypto"}),
    ("health-biotech", "", "Health & biotech", "Health",
     "Medicine, biology, pharma, health systems and medtech.",
     r"\b(health\w*|medic\w*|clinical|patients?|hospitals?|biotech\w*|pharma\w*|drugs?|fda|genom\w*|proteins?|"
     r"bioinformatics|biology|cancer|vaccines?|medicare|medicaid|disease|neuro\w*|medrxiv|biorxiv)\b",
     {"bioinformatics", "healthcare", "medical", "biology", "genomics", "health", "medical-imaging"}),
    ("robotics-hardware", "", "Robotics & hardware", "Robotics",
     "Robots, drones, embedded devices and consumer hardware.",
     r"\b(robot\w*|humanoids?|drones?|embedded|firmware|arduino|raspberry pi|esp32|microcontrollers?|"
     r"hardware|3d print\w*|lidar|actuators?|exoskeleton\w*)\b",
     {"robotics", "ros", "ros2", "embedded", "hardware", "arduino", "esp32", "drones", "3d-printing", "iot"}),
    ("semiconductors", "", "Semiconductors & chips", "Chips",
     "Chip design, fabs, GPUs, accelerators and the supply chain.",
     r"\b(semiconductors?|chips?|chipmakers?|gpus?|tpus?|npus?|asics?|fpgas?|nvidia|nvda|amd|intel|tsmc|"
     r"qualcomm|risc-v|wafers?|fabs?|foundry|lithography|asml|hbm|cuda|silicon)\b",
     {"fpga", "risc-v", "verilog", "cuda", "gpu", "semiconductor", "vlsi", "chip-design"}),
    ("climate-energy", "", "Climate & energy", "Energy",
     "Clean energy, grids, EVs, batteries, oil and gas, and climate.",
     r"\b(climate|energy|solar|wind (power|farms?|turbines?)|battery storage|energy storage|power grids?|evs?|electric vehicles?|"
     r"ev charging|hydrogen|nuclear|carbon|emissions|oil|natural gas|lng|renewables?|heat pumps?|power plants?|utilities)\b",
     {"climate", "energy", "solar", "climate-change", "electric-vehicles", "renewable-energy", "sustainability"}),
    ("ecommerce-retail", "", "E-commerce & retail", "Retail",
     "Online and physical retail, marketplaces, logistics and shopping.",
     r"\b(e-?commerce|retail\w*|shopping|shoppers?|black friday|cyber monday|amazon|shopify|walmart|"
     r"marketplaces?|checkout|merchants?|logistics|grocer\w*|consumer brands?)\b",
     {"ecommerce", "e-commerce", "shopify", "retail", "marketplace"}),
    ("gaming-xr", "", "Gaming & XR", "Gaming",
     "Games, studios, engines, consoles and VR/AR.",
     r"\b(video ?games?|gaming|gamers?|game (studio|engine|developers?)|playstation|ps5|xbox|nintendo|switch 2|steam|"
     r"epic games|unreal engine|unity|godot|esports|gta ?(6|vi)|grand theft auto|rockstar|ubisoft|"
     r"vr|xr|virtual reality|mixed reality|vr headsets?|vision pro|meta quest)\b",
     {"game", "gamedev", "game-development", "godot", "unity", "unreal-engine", "vr", "xr", "game-engine"}),
    ("enterprise-saas", "", "Enterprise SaaS & productivity", "SaaS",
     "Business software, productivity, collaboration and the enterprise market.",
     r"\b(saas|enterprise software|enterprise ai|crm|erp|salesforce|workday|servicenow|sap|productivity apps?|"
     r"notion|slack|microsoft 365|no-?code|low-?code|b2b|knowledge base|workflow automation)\b",
     {"saas", "productivity", "crm", "erp", "workflow", "automation", "no-code", "low-code", "notion"}),
    ("education", "", "Education", "Education",
     "Schools, universities, edtech, courses and learning resources.",
     r"\b(education\w*|edtech|schools?|students?|teachers?|universit(y|ies)|courses?|learning resources|"
     r"tutorials?|mooc|curriculum|classrooms?|lessons?)\b",
     {"education", "learning", "tutorial", "course", "edtech", "roadmap", "interview"}),
    ("media-creator", "", "Media & creator economy", "Media",
     "News media, video, streaming, music, social platforms and creators.",
     r"\b(media|newsrooms?|newspapers?|journalis\w*|youtube|tiktok|instagram|creators?|influencers?|podcasts?|"
     r"streaming|netflix|spotify|music|films?|movies?|tv|publishers?|social media|bluesky)\b",
     {"video", "youtube", "streaming", "music", "media", "social-media", "podcast"}),
    ("space-mobility", "", "Space & mobility", "Space",
     "Launches, satellites, aviation, autonomous vehicles and transport.",
     r"\b(space ?x|spacex|spaceflight|starship|starlink|rockets?|satellites?|orbit(al)?|nasa|esa|moon|lunar|mars|"
     r"astronauts?|aviation|aircraft|airlines?|faa|autonomous (vehicles?|driving)|robotaxis?|waymo|"
     r"self-driving|uber|lyft|transportation|mobility)\b",
     {"space", "aerospace", "satellite", "autonomous-driving", "self-driving-car", "astronomy"}),
    ("policy-regulation", "", "Policy & regulation", "Policy",
     "Laws, regulators, courts, antitrust, privacy and digital policy.",
     r"\b(regulat\w*|laws?|legislat\w*|courts?|lawsuits?|sues?|judges?|antitrust|competition authority|"
     r"ftc|fcc|doj|european commission|commissioner|eu ai act|dma|dsa|gdpr|privacy|public policy|tech policy|government|"
     r"ministers?|congress|senate|parliament|tariffs?|sanctions|export controls?)\b",
     {"privacy", "gdpr", "regulation", "policy", "legal", "compliance"}),
]
OTHER = ("other", "", "Other", "Other", "Items that no rule matched. They still count; nothing is dropped.", r"$^", set())
ALL_INDUSTRIES = INDUSTRIES + [OTHER]
IND = {i[0]: i for i in ALL_INDUSTRIES}
IND_ORDER = [i[0] for i in ALL_INDUSTRIES]
IND_RE = {i[0]: re.compile(i[5], re.I) for i in INDUSTRIES}

# Sources whose items always belong to an industry, before any keyword rule.
SOURCE_INDUSTRIES = {
    "hf_models": ["ai-llms"], "hf_spaces": ["ai-llms"], "hf_datasets": ["ai-llms", "data-analytics"],
    "hf_papers": ["ai-llms"], "openrouter": ["ai-llms"], "openai_news": ["ai-llms"], "google_ai": ["ai-llms"],
    "deepmind": ["ai-llms"], "hf_blog": ["ai-llms"],
    "mcp_registry": ["ai-agents"], "smithery": ["ai-agents"],
    "npm": ["devtools"], "pypi": ["devtools"], "crates": ["devtools"], "stackoverflow": ["devtools"],
    "ghchangelog": ["devtools"], "jsdelivr": ["web-frontend"], "dockerhub": ["cloud-devops"],
    "githubstatus": ["cloud-devops"], "cloudflarestatus": ["cloud-devops"], "lwn": ["cloud-devops"],
    "kev": ["cybersecurity"], "nvd": ["cybersecurity"], "euvd": ["cybersecurity"],
    "hf_media": ["ai-media"], "arena_image": ["ai-media"], "arena_video": ["ai-media"], "arena_text": ["ai-llms"],
    "lab_models": ["ai-llms"], "lab_hf": ["ai-llms"], "lab_releases": ["ai-llms"], "anthropic_news": ["ai-llms"],
    "st_anthropic": ["ai-llms"], "st_openai": ["ai-llms"], "st_mistral": ["ai-llms"], "st_cohere": ["ai-llms"],
    "st_perplexity": ["ai-llms"], "st_elevenlabs": ["ai-media"], "fred": ["markets-economy"], "ecb_fx": ["markets-economy"],
    "thn": ["cybersecurity"], "bleeping": ["cybersecurity"],
}
# Sources where only the source rule applies (keyword rules would misfire on vendor names or prices).
SOURCE_ONLY = {"kev", "nvd", "euvd", "coingecko_trending", "coingecko_markets", "launches",
               "githubstatus", "cloudflarestatus", "jsdelivr", "fred", "ecb_fx", "arena_text", "arena_image",
               "arena_video", "st_anthropic", "st_openai", "st_mistral", "st_cohere", "st_perplexity", "st_elevenlabs"}
ARXIV_INDUSTRY = {"cs.AI": "ai-llms", "cs.CL": "ai-llms", "cs.LG": "ai-llms", "cs.CV": "ai-llms",
                  "cs.CR": "cybersecurity", "cs.SE": "devtools", "cs.RO": "robotics-hardware",
                  "q-bio": "health-biotech", "q-fin": "fintech"}


def classify(key: str, it: dict) -> list[str]:
    hits = set(SOURCE_INDUSTRIES.get(key, []))
    if it.get("industry"):
        hits.add(it["industry"])
    if key == "arxiv":
        cat = it.get("category", "")
        ind = ARXIV_INDUSTRY.get(cat) or ARXIV_INDUSTRY.get(cat.split(".")[0])
        if ind:
            hits.add(ind)
    if key not in SOURCE_ONLY:
        topics = {t.lower() for t in (it.get("topics") or []) + (it.get("tags") or [])}
        for slug, _e, _t, _s, _i, _rx, tset in INDUSTRIES:
            if topics & tset:
                hits.add(slug)
        title = it.get("title") or ""
        if it["kind"] in ("repo", "model", "dataset", "space") and "/" in title:
            title = title.split("/", 1)[1]   # match the project name, not the owner (avoids "nvidia/..." -> chips)
        text = " ".join(str(x) for x in (title, it.get("desc"), it.get("task"),
                                          " ".join(it.get("topics") or []), " ".join(it.get("tags") or []),
                                          it.get("keyword")) if x)
        for slug, rx in IND_RE.items():
            if rx.search(text):
                hits.add(slug)
    return sorted(hits, key=IND_ORDER.index) or ["other"]


# ---------------------------------------------------------------------------
# Entities: one row per real-world item, merged across sources, with a score
# ---------------------------------------------------------------------------

RANKED = {"gh_daily", "gh_weekly", "gh_new", "hn_front", "hn_show", "hn_best", "hn_ask", "hf_models", "hf_spaces",
          "hf_datasets", "hf_papers", "smithery", "npm", "jsdelivr", "lobsters", "devto_day", "devto_week",
          "stackoverflow", "coingecko_trending", "gtrends", "wikipedia", "mastodon_tags", "mastodon_links",
          "bluesky", "gh_monthly", "gh_new_month", "gh_new_year", "hn_month", "hn_year", "devto_month", "devto_year",
          "hf_papers_week", "hf_papers_month"} | {f"gh_{s}" for s, _ in GITHUB_LANGUAGES} | {f"gh_topic_{t}" for t, _ in GITHUB_TOPICS}
PULSE_FAMILIES = {"Google Trends", "Wikipedia", "Mastodon", "Bluesky"}
UNRANKED_BASE = 0.25
W_RANK, W_SPREAD, SPREAD_CAP = 0.6, 0.4, 3


def family(key: str, results) -> str:
    for prefix, name in (("gh_", "GitHub"), ("hn_", "Hacker News"), ("hf_", "Hugging Face"), ("devto", "Dev.to"),
                         ("mastodon", "Mastodon"), ("coingecko", "CoinGecko"), ("lab_news_", "Google News"),
                         ("media_news_", "Google News"), ("deals_", "Google News"), ("arena_", "LMArena")):
        if key.startswith(prefix):
            return name
    return results[key].name.split(" · ")[0]


def dedupe_keys(it: dict) -> set[str]:
    keys = {canonical_url(it["url"])}
    if it["kind"] in ("news", "hn", "post", "lab"):
        keys.add("t:" + title_key(it["title"]))
    if it.get("github"):
        keys.add(canonical_url(it["github"]))
    return {k for k in keys if k and k != "t:"}


class Entity:
    def __init__(self):
        self.hits: list[tuple[str, dict, float | None, int]] = []   # key, item, percentile, position
        self.families: list[str] = []
        self.industries: list[str] = []
        self.score = 0
        self.best_pct = 0.0

    @property
    def key(self):
        return self.hits[0][0]

    @property
    def item(self):
        return self.hits[0][1]


def build_entities(results, keys=None) -> list["Entity"]:
    allowed = set(keys) if keys is not None else None
    order = [k for k, *_ in SOURCES if k in results and results[k].ok and k != "maintainer"
             and (allowed is None or k in allowed)]
    by_key: dict[str, Entity] = {}
    ents: list[Entity] = []
    for key in order:
        items = results[key].items
        n = len(items)
        for pos, it in enumerate(items):
            ks = dedupe_keys(it)
            ent = next((by_key[k] for k in ks if k in by_key), None)
            if ent is None:
                ent = Entity()
                ents.append(ent)
            pct = (1 - pos / n) if key in RANKED and n else None
            ent.hits.append((key, it, pct, pos + 1))
            fam = family(key, results)
            if fam not in ent.families:
                ent.families.append(fam)
            for ind in classify(key, it):
                if ind not in ent.industries:
                    ent.industries.append(ind)
            for k in ks:
                by_key.setdefault(k, ent)
    for e in ents:
        if len(e.industries) > 1 and "other" in e.industries:
            e.industries.remove("other")
        e.industries.sort(key=IND_ORDER.index)
        pcts = [p for _k, _i, p, _pos in e.hits if p is not None]
        e.best_pct = max(pcts) if pcts else UNRANKED_BASE
        spread = min(len(e.families) - 1, SPREAD_CAP) / SPREAD_CAP
        e.score = round(100 * (W_RANK * e.best_pct + W_SPREAD * spread))
        for _k, it, _p, _pos in e.hits:
            it["_seen"] = e.families
            it["_ind"] = e.industries
            it["_score"] = e.score
    return ents


def mark_exploited(results) -> None:
    kev = results.get("kev")
    ids = set(KEV_ALL)
    if kev and kev.ok:
        ids |= {i["title"] for i in kev.items}
    for key in ("kev", "nvd", "euvd"):
        r = results.get(key)
        if r and r.ok:
            for it in r.items:
                cve = it.get("cve") if it["kind"] == "euvd" else it["title"]
                it["_exploited"] = it["kind"] == "kev" or (cve in ids)


# ---------------------------------------------------------------------------
# Cell helpers: why it matters, key metric, momentum, maturity
# ---------------------------------------------------------------------------

def first_sentence(text: str, n: int = 110) -> str:
    t = re.sub(r"\s+", " ", text or "").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    return clip(m.group(1) if m and len(m.group(1)) > 25 else t, n)


def why(key: str, it: dict) -> str:
    k = it["kind"]
    if k == "arena":
        return f"#{it.get('rank')} on the LMArena {it.get('board', '').replace('_', '-')} board ({it.get('org')})"
    if k == "quote":
        return "Latest published value"
    if k in ("news", "lab") and it.get("via") == "Google News" and not it.get("desc"):
        return f"Headline via Google News ({it.get('outlet')})"
    if k == "hn":
        d = it.get("domain")
        return f"Link to {d}" if d and d != "news.ycombinator.com" else "Discussion thread on HN"
    if k == "model":
        return " · ".join(b for b in (it.get("task"), it.get("library")) if b) or "—"
    if k == "kev":
        return clip(it.get("name") or it.get("desc"), 100)
    if k == "coin":
        return f"Market-cap rank #{it['mcap_rank']}" if it.get("mcap_rank") else "—"
    if k == "launch":
        orbit = it.get("orbit") if isinstance(it.get("orbit"), str) else None
        return " · ".join(b for b in (it.get("provider"), it.get("mission_type"), orbit) if b) or "—"
    if k == "release":
        return f"New {'pre-release' if it.get('prerelease') else 'release'} of {it['project']}"
    if k == "search":
        return clip(it.get("news_title"), 100) or "—"
    if k == "incident":
        return ", ".join(it.get("components") or []) or "—"
    if k in ("wiki", "tag"):
        return "—"
    if k == "cdn":
        return "Served from the jsDelivr CDN"
    if k in ("question", "post"):
        return ", ".join(f"#{t}" for t in (it.get("tags") or [])[:3]) or "—"
    return first_sentence(it.get("desc") or "", 110) or "—"


def momentum(key: str, it: dict) -> str:
    k = it["kind"]
    if k == "repo" and it.get("gained") is not None and it.get("stars"):
        base = max(it["stars"] - it["gained"], 1)
        return f"{it['gained'] / base * 100:+.1f}%"
    if k == "hn" and it.get("points") is not None and it.get("created"):
        hours = max((datetime.now(timezone.utc) - it["created"]).total_seconds() / 3600, 1)
        return f"{it['points'] / hours:.0f} pts/h"
    if k == "cdn" and it.get("change") is not None:
        return f"{it['change']:+.1f}% w/w"
    if k == "coin" and it.get("change_24h") is not None:
        return f"{it['change_24h']:+.1f}% 24h"
    return "—"


def _price(v) -> str:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return "—"
    return f"{f:,.2f}" if f >= 1 else f"{f:.6f}".rstrip("0")


def key_metric(key: str, it: dict) -> str:
    k = it["kind"]
    if k == "arena":
        return f"rating {it['rating']:.0f} · {fmt_int(it.get('votes'))} votes" if it.get("rating") else "—"
    if k == "quote":
        return f"{it.get('value')} ({it.get('asof')})"
    if k == "repo":
        s = f"{fmt_compact(it.get('stars'))} stars"
        if it.get("gained") is not None:
            s += f" · +{fmt_int(it['gained'])} {({'gh_weekly': 'this week', 'gh_monthly': 'this month'}).get(key, 'today')}"
        elif it.get("created"):
            s += f" · created {fmt_day(it['created']).rsplit(' ', 1)[0]}"
        return s
    if k == "hn":
        return f"{fmt_int(it.get('points'))} pts · {fmt_int(it.get('comments'))} comments"
    if k == "post":
        if key == "lobsters":
            return f"{fmt_int(it.get('score'))} score · {fmt_int(it.get('comments'))} comments"
        return f"{fmt_int(it.get('reactions'))} reactions · {fmt_int(it.get('comments'))} comments"
    if k == "question":
        return f"{fmt_int(it.get('score'))} score · {fmt_int(it.get('answers'))} answers · {fmt_compact(it.get('views'))} views"
    if k in ("model", "dataset"):
        return f"{fmt_int(it.get('likes'))} likes · {fmt_compact(it.get('downloads'))} dl/30d"
    if k == "space":
        return f"{fmt_int(it.get('likes'))} likes"
    if k == "llm":
        pin = "—" if it.get("price_in") is None else f"${it['price_in']:g}"
        pout = "—" if it.get("price_out") is None else f"${it['price_out']:g}"
        return f"{pin} in / {pout} out per 1M · {fmt_compact(it.get('context'))} ctx"
    if k == "paper":
        if it.get("upvotes") is not None:
            return f"{fmt_int(it['upvotes'])} upvotes"
        return f"{md_escape(it.get('category'))} · new"
    if k == "mcp":
        return f"{fmt_int(it.get('uses'))} uses" if key == "smithery" else f"v{md_escape(it.get('version'))} · {fmt_day(it.get('published'))}"
    if k == "package":
        if key == "crates":
            return f"{fmt_compact(it.get('recent'))} dl/90d"
        return f"{fmt_compact(it.get('weekly'))} dl/week" if it.get("weekly") is not None else f"v{md_escape(it.get('version'))}"
    if k == "cdn":
        return f"{fmt_compact(it.get('hits'))} hits/week"
    if k == "image":
        return f"{fmt_compact(it.get('pulls'))} pulls"
    if k == "release":
        return f"{md_escape(clip(it.get('release_title') or it.get('tag'), 40))} · {fmt_day(it.get('published'))}"
    if k in ("kev", "cve", "euvd"):
        s = f"CVSS {it['score']}" if it.get("score") is not None else "CVSS not scored"
        return s + (" · exploited" if it.get("_exploited") else "")
    if k in ("news", "lab"):
        return f"{md_escape(it.get('outlet'))} · {fmt_day(it.get('published'))}"
    if k == "incident":
        return f"{md_escape(it.get('impact'))} · {md_escape(it.get('status'))}"
    if k == "coin":
        return f"${_price(it.get('price'))} · {momentum(key, it)}"
    if k == "launch":
        return f"NET {fmt_day(it.get('net'))} · {md_escape(it.get('status'))}"
    if k == "search":
        return f"{md_escape(it.get('traffic'))} searches ({it.get('geo')})"
    if k == "wiki":
        return f"{fmt_compact(it.get('views'))} views"
    if k == "tag":
        return f"{fmt_int(it.get('uses'))} posts / 2 days"
    if k == "product":
        return "Featured launch"
    return "—"


def maturity(key: str, it: dict) -> str:
    k = it["kind"]
    if k == "repo":
        lic = it.get("license") or "no licence"
        created = it.get("created")
        if created:
            days = (datetime.now(timezone.utc) - created).days
            age = f"{days} d old" if days < 60 else (f"{days // 30} mo old" if days < 730 else f"{days // 365} y old")
            return f"{md_escape(lic)} · {age}"
        return md_escape(lic)
    if k in ("model", "dataset", "space"):
        return md_escape(it.get("license")) or "licence not stated"
    if k == "package":
        v = str(it.get("version") or "")
        stage = "pre-1.0" if v.startswith("0.") else ("pre-release" if re.search(r"(a|b|rc|alpha|beta|dev)\d*$", v) else "stable")
        return " · ".join(x for x in (md_escape(it.get("license")), stage) if x)
    if k == "paper":
        return "preprint · code" if it.get("github") else "preprint"
    if k == "mcp":
        if key == "smithery":
            return ("verified" if it.get("verified") else "unverified") + (" · remote" if it.get("remote") else " · local")
        return "pre-1.0" if str(it.get("version") or "").startswith("0.") else "1.0+"
    if k == "release":
        return "pre-release" if it.get("prerelease") else "stable"
    return "—"


def seen_cell(it: dict) -> str:
    fams = it.get("_seen") or []
    if len(fams) <= 1:
        return "1"
    return f"**{len(fams)}** <sub>{md_escape(', '.join(fams))}</sub>"


def ind_cell(it: dict, n: int = 2) -> str:
    inds = it.get("_ind") or ["other"]
    out = ", ".join(f"{IND[s][3]}" for s in inds[:n])
    return out + (f" +{len(inds) - n}" if len(inds) > n else "")


def src_cell(key: str, results) -> str:
    r = results[key]
    return md_link(r.name.split(" · ")[0], r.url)


def ttl(it: dict, n: int = 90) -> str:
    return md_link(clip(it["title"], n), it["url"])


def _authors(a: list[str]) -> str:
    if not a:
        return "—"
    return md_escape(", ".join(a[:2]) + (f" +{len(a) - 2}" if len(a) > 2 else ""))


# ---------------------------------------------------------------------------
# Table designs, one per item type. Every design ends with Seen on, Industry, Source.
# ---------------------------------------------------------------------------

TYPE_OF = {"kev": "vuln", "cve": "vuln", "euvd": "vuln", "lab": "news"}
TYPE_LABEL = {"repo": "Repositories", "hn": "Discussions", "post": "Posts", "question": "Questions", "product": "Product launches",
              "model": "Models", "space": "Demos (Spaces)", "dataset": "Datasets", "llm": "Hosted models", "paper": "Papers",
              "mcp": "MCP servers", "package": "Packages", "cdn": "CDN traffic", "image": "Container images",
              "release": "Releases", "vuln": "Vulnerabilities", "news": "Headlines", "incident": "Incidents",
              "coin": "Crypto assets", "launch": "Launches to orbit", "search": "Searches", "wiki": "Most-read articles",
              "tag": "Hashtags", "topic": "Topics"}
TYPE_EMOJI = {"repo": "", "hn": "", "post": "", "question": "", "product": "", "model": "", "space": "",
              "dataset": "", "llm": "", "paper": "", "mcp": "", "package": "", "cdn": "", "image": "",
              "release": "", "vuln": "", "news": "", "incident": "", "coin": "", "launch": "",
              "search": "", "wiki": "", "tag": "", "topic": ""}
TYPE_DESIGN_NOTE = {
    "repo": "stars, stars gained, momentum % (gained ÷ stars before), language, licence and age",
    "hn": "points, comments, velocity (points per hour) and the thread link",
    "post": "tags, reactions or score, comments and author",
    "question": "tags, score, answers (an accepted answer is marked), views",
    "product": "tagline and who posted it",
    "model": "task and library, likes, 30-day downloads, licence",
    "space": "what the demo does, SDK, likes, licence",
    "dataset": "task, likes, 30-day downloads, licence",
    "llm": "USD per 1M input and output tokens, context window, date added",
    "paper": "abstract's first sentence, authors, upvotes or category, code link",
    "mcp": "what the server does, uses or version, maturity",
    "package": "ecosystem, version, downloads with the period, release date, licence and stage",
    "cdn": "CDN hits this week and change against last week",
    "image": "pulls, stars, last update",
    "release": "project, release, stable or pre-release, date",
    "vuln": "vendor and product, CVSS, exploited (in CISA KEV or not), ransomware use, date",
    "news": "first sentence of the outlet's summary, outlet, time",
    "incident": "service, affected components, impact, status, start",
    "coin": "market-cap rank, price, 24 h and 7 d change, market cap",
    "launch": "provider, launch window in Berlin time, status, site",
    "search": "country, Google's search-volume bucket, top story",
    "wiki": "views and rank", "tag": "posts and accounts over two days", "topic": "context line",
}


def ttype(it: dict) -> str:
    return TYPE_OF.get(it["kind"], it["kind"])


def vuln_vendor(it: dict) -> str:
    v = " · ".join(x for x in (it.get("vendor"), it.get("product")) if x)
    if not v and it.get("assigner"):
        v = f"reported by {it['assigner'].split('@')[-1]}"
    return md_escape(clip(v, 60)) or "—"


def _pct(v) -> str:
    return "—" if v is None else f"{v:+.1f}%"


def _gained(k, i) -> str:
    if i.get("gained") is None:
        return "new"
    return f"+{fmt_int(i['gained'])} {'wk' if k == 'gh_weekly' else 'today'}"


def _cvss(i) -> str:
    if i.get("score") is None:
        return "—"
    return f"{i['score']}" + (f" {md_escape(i.get('severity', '').title())}" if i.get("severity") else "")


DESIGNS = {
    "repo": (["Repository", "Why it matters", "Stars", "Gained", "Momentum", "Lang", "Licence · age"],
             lambda k, i: [ttl(i, 60), md_escape(why(k, i)), fmt_int(i.get("stars")), _gained(k, i), momentum(k, i),
                           md_escape(i.get("language")) or "—", maturity(k, i)]),
    "hn": (["Story", "Why it matters", "Points", "Comments", "Velocity", "Thread"],
           lambda k, i: [ttl(i), md_escape(why(k, i)), fmt_int(i.get("points")), fmt_int(i.get("comments")),
                         momentum(k, i), md_link("open", i.get("discuss"))]),
    "post": (["Post", "Tags", "Engagement", "Author"],
             lambda k, i: [ttl(i), md_escape(why(k, i)), key_metric(k, i), md_escape(i.get("author")) or "—"]),
    "question": (["Question", "Tags", "Score", "Answers", "Views"],
                 lambda k, i: [ttl(i), md_escape(why(k, i)), fmt_int(i.get("score")),
                               fmt_int(i.get("answers")) + (" (accepted)" if i.get("answered") else ""), fmt_compact(i.get("views"))]),
    "product": (["Product", "Why it matters", "Posted by"],
                lambda k, i: [ttl(i, 50), md_escape(why(k, i)), md_escape(i.get("author")) or "—"]),
    "model": (["Model", "Task · library", "Likes", "Downloads 30 d", "Licence"],
              lambda k, i: [ttl(i, 60), md_escape(why(k, i)), fmt_int(i.get("likes")), fmt_compact(i.get("downloads")), maturity(k, i)]),
    "space": (["Demo", "Why it matters", "SDK", "Likes", "Licence"],
              lambda k, i: [ttl(i, 60), md_escape(why(k, i)), md_escape(i.get("sdk")) or "—", fmt_int(i.get("likes")), maturity(k, i)]),
    "dataset": (["Dataset", "Why it matters", "Task", "Likes", "Downloads 30 d", "Licence"],
                lambda k, i: [ttl(i, 60), md_escape(why(k, i)), md_escape(i.get("task")) or "—", fmt_int(i.get("likes")),
                              fmt_compact(i.get("downloads")), maturity(k, i)]),
    "llm": (["Model", "Why it matters", "$ in / 1M", "$ out / 1M", "Context", "Added"],
            lambda k, i: [ttl(i, 50), md_escape(why(k, i)),
                          "—" if i.get("price_in") is None else f"{i['price_in']:g}",
                          "—" if i.get("price_out") is None else f"{i['price_out']:g}",
                          fmt_compact(i.get("context")), fmt_day(i.get("created")).rsplit(" ", 1)[0]]),
    "paper": (["Paper", "Why it matters", "Authors", "Signal", "Code · maturity"],
              lambda k, i: [ttl(i), md_escape(why(k, i)), _authors(i.get("authors")), key_metric(k, i),
                            (md_link("repo", i["github"]) + (f" · {fmt_int(i['github_stars'])} stars" if i.get("github_stars") else ""))
                            if i.get("github") else maturity(k, i)]),
    "mcp": (["Server", "Why it matters", "Signal", "Maturity"],
            lambda k, i: [ttl(i, 50), md_escape(why(k, i)), key_metric(k, i), maturity(k, i)]),
    "package": (["Package", "Why it matters", "Ecosystem", "Version", "Downloads", "Released", "Licence · stage"],
                lambda k, i: [ttl(i, 40), md_escape(why(k, i)), md_escape(i.get("ecosystem")), f"`{md_escape(i.get('version'))}`",
                              key_metric(k, i), fmt_day(i.get("published")).rsplit(" ", 1)[0], maturity(k, i)]),
    "cdn": (["Package", "Hits this week", "Change w/w"],
            lambda k, i: [ttl(i, 40), fmt_compact(i.get("hits")), momentum(k, i)]),
    "image": (["Image", "Why it matters", "Pulls", "Stars", "Updated"],
              lambda k, i: [ttl(i, 40), md_escape(why(k, i)), fmt_compact(i.get("pulls")), fmt_int(i.get("stars")),
                            fmt_day(i.get("published"))]),
    "release": (["Project", "Release", "Stage", "Published"],
                lambda k, i: [md_link(i["project"], f"https://github.com/{i['project']}"),
                              md_link(clip(i.get("release_title") or i.get("tag"), 60), i["url"]), maturity(k, i),
                              fmt_day(i.get("published"))]),
    "vuln": (["ID", "Why it matters", "Vendor · product", "CVSS", "Exploited", "Ransomware", "Date"],
             lambda k, i: [md_link(i["title"], i["url"]) + (f" <sub>{md_escape(i['cve'])}</sub>" if i.get("cve") else ""),
                           md_escape(why(k, i)), vuln_vendor(i), _cvss(i),
                           "**yes** (CISA KEV)" if i.get("_exploited") else "not in KEV",
                           md_escape(i.get("ransomware")) if i["kind"] == "kev" else "—",
                           i.get("added") or fmt_day(i.get("published"))]),
    "news": (["Headline", "Why it matters", "Outlet", "Published"],
             lambda k, i: [ttl(i), md_escape(why(k, i)), outlet_cell(i), fmt_day(i.get("published"))]),
    "incident": (["Incident", "Service", "Components", "Impact", "Status", "Started"],
                 lambda k, i: [ttl(i), md_escape(i.get("service")), md_escape(why(k, i)), md_escape(i.get("impact")) or "—",
                               md_escape(i.get("status")) or "—", fmt_day(i.get("published"))]),
    "coin": (["Asset", "Market-cap rank", "Price (USD)", "24 h", "7 d", "Market cap"],
             lambda k, i: [ttl(i, 40), fmt_int(i.get("mcap_rank")), _price(i.get("price")), _pct(i.get("change_24h")),
                           _pct(i.get("change_7d")),
                           fmt_compact(i.get("mcap")) if isinstance(i.get("mcap"), (int, float)) else (md_escape(i.get("mcap")) or "—")]),
    "launch": (["Mission", "Provider", "Window (Berlin)", "Status", "Site"],
               lambda k, i: [ttl(i, 60), md_escape(i.get("provider")) or "—", fmt_day(i.get("net")),
                             md_escape(i.get("status")) or "—", md_escape(clip(str(i.get("location") or i.get("pad") or ""), 50)) or "—"]),
    "search": (["Search", "Country", "Searches", "Top story"],
               lambda k, i: [ttl(i, 50), i.get("geo"), md_escape(i.get("traffic")) or "—",
                             md_link(clip(i["news_title"], 70), i["news_url"]) if i.get("news_title") else "—"]),
    "wiki": (["Article", "Views", "Rank"], lambda k, i: [ttl(i, 60), fmt_int(i.get("views")), fmt_int(i.get("rank"))]),
    "tag": (["Hashtag", "Posts (2 d)", "Accounts (2 d)"], lambda k, i: [ttl(i, 40), fmt_int(i.get("uses")), fmt_int(i.get("accounts"))]),
    "topic": (["Topic", "Context"], lambda k, i: [ttl(i, 60), md_escape(clip(i.get("desc"), 110)) or "—"]),
}


def type_table(t: str):
    h, fn = DESIGNS.get(t, (["Item"], lambda k, i: [ttl(i)]))
    return h + ["Seen on", "Industry", "Source"], (
        lambda k, i, results: fn(k, i) + [seen_cell(i), ind_cell(i), src_cell(k, results)])


def fold_table(headers: list[str], rows: list[list[str]], visible: int) -> list[str]:
    """Numbered table; rows beyond `visible` go in a <details> fold with continued numbering."""
    if not rows:
        return []
    numbered = [[str(n)] + r for n, r in enumerate(rows, 1)]
    for r in numbered:
        assert len(r) == len(headers) + 1, (headers, r)
    out = [table(["#"] + headers, numbered[:visible], numbered=False)]
    if len(numbered) > visible:
        out += ["", "<details>", f"<summary>Show {len(numbered) - visible} more</summary>", "",
                table(["#"] + headers, numbered[visible:], numbered=False), "", "</details>"]
    return out


UNIFIED_H = ["Item", "Type", "Why it matters", "Key metric", "Seen on", "Score", "Source"]


def unified_row(e, results) -> list[str]:
    k, it = e.key, e.item
    t = ttype(it)
    return [ttl(it, 70), f"{TYPE_LABEL.get(t, t)}", md_escape(why(k, it)), key_metric(k, it),
            seen_cell(it), str(e.score), src_cell(k, results)]


TYPE_LABEL.update({"arena": "Leaderboard positions", "quote": "Market quotes"})
TYPE_EMOJI.update({"arena": "", "quote": ""})
TYPE_DESIGN_NOTE.update({"arena": "board, rank, rating, votes, organisation, licence, publish date",
                         "quote": "level, change against the previous published value, as-of date"})
DESIGNS["arena"] = (["Model", "Organisation", "Board", "Rank", "Rating", "Votes", "Licence", "Published"],
                    lambda k, i: [md_escape(clip(i["title"], 60)), md_escape(i.get("org")),
                                  md_escape(i.get("board", "").replace("_", " ")), f"#{i.get('rank')}",
                                  f"{i['rating']:.0f}" if i.get("rating") else "—", fmt_int(i.get("votes")),
                                  md_escape(i.get("license")) or "—", md_escape(i.get("asof"))])
DESIGNS["quote"] = (["Indicator", "Level", "Previous", "Change", "As of"],
                    lambda k, i: [ttl(i, 50), _num(i.get("value"), i.get("unit")), _num(i.get("prev"), i.get("unit")),
                                  (f"{i['change']:+.0f} bp" if i.get("change_kind") == "bp" else f"{i['change']:+.2f}%")
                                  if i.get("change") is not None else "—", md_escape(i.get("asof"))])


def outlet_cell(i: dict) -> str:
    """Outlet name; for Google News results also the publisher's domain, since the link is a Google redirect."""
    o = md_escape(i.get("outlet")) or "—"
    if i.get("via") == "Google News" and i.get("publisher"):
        o += f" <sub>{md_escape(i['publisher'])} · via Google News</sub>"
    return o


# ---------------------------------------------------------------------------
# Page blocks
# ---------------------------------------------------------------------------

GROUPS = [
    ("src-github", "GitHub", ["gh_daily"] + [f"gh_{s}" for s, _ in GITHUB_LANGUAGES]
     + [f"gh_topic_{t}" for t, _ in GITHUB_TOPICS]),
    ("src-hn", "Hacker News", ["hn_front", "hn_show", "hn_ask"]),
    ("src-ai", "Models & labs", ["hf_models", "openrouter", "hf_spaces", "hf_datasets", "openai_news", "google_ai",
                                   "deepmind", "hf_blog"]),
    ("src-labs", "AI labs & big players", ["anthropic_news"] + [k for k, *_ in LAB_FEEDS_EXTRA if k != "elevenlabs_blog"]
     + ["lab_models", "lab_hf", "lab_releases", "arena_text"] + [f"lab_news_{lab[0]}" for lab in LABS]),
    ("src-media", "AI media", ["hf_media", "arena_video", "arena_image", "elevenlabs_blog"] + [k for k, *_ in MEDIA_QUERIES]),
    ("src-ainews", "AI news & newsletters", [k for k, *_ in AI_NEWS_FEEDS]),
    ("src-research", "Papers & preprints", ["hf_papers", "arxiv", "biorxiv"]),
    ("src-mcp", "MCP registries", ["mcp_registry", "smithery"]),
    ("src-packages", "Packages & releases", ["releases", "npm", "pypi", "crates", "jsdelivr", "dockerhub"]),
    ("src-security", "Vulnerabilities", ["kev", "nvd", "euvd"]),
    ("src-econ", "Markets & economy", ["fred", "ecb_fx"] + [k for k, *_ in MARKET_FEEDS] + [k for k, *_ in DEAL_QUERIES]),
    ("src-markets", "Crypto & launches", ["coingecko_trending", "coingecko_markets", "launches"]),
    ("src-community", "Community", ["lobsters", "devto_day", "stackoverflow", "producthunt"]),
    ("src-news", "Tech news", [k for k, *_ in NEWS_FEEDS]),
    ("src-industry-news", "Industry outlets", [k for k, *_ in INDUSTRY_FEEDS]),
    ("src-pulse", "Public pulse", ["gtrends", "wikipedia", "mastodon_links", "mastodon_tags", "bluesky"]),
    ("src-windows", "Week, month and year lists", list(WINDOW_OF)),
]
STATUS_KEYS = ["githubstatus", "cloudflarestatus"] + AI_STATUS_KEYS


def compact_group(keys, results) -> list[str]:
    rows = []
    for k in keys:
        r = results[k]
        if not r.ok:
            rows.append([md_link(r.name, r.url), "skipped", "—", md_escape(clip(r.note, 60))])
        elif not r.items:
            rows.append([md_link(r.name, r.url), "0", "—", "nothing in the window today"])
        else:
            it = r.items[0]
            rows.append([md_link(r.name, r.url), str(len(r.items)), ttl(it, 70), key_metric(k, it)])
    return [table(["Source", "Items", "#1 item", "Key metric"], rows, numbered=False), ""]


def count_ok(results) -> tuple[int, int]:
    keys = [k for k in results if k != "maintainer"]
    return sum(1 for k in keys if results[k].ok), len(keys)


def source_block(key: str, results, visible: int, cap: int | None, level: str = "####") -> list[str]:
    res = results.get(key)
    if not res:
        return []
    p = [f"{level} {md_escape(res.name)}", ""]
    src = f"{md_link(domain_of(res.url) or res.url, res.url)} · fetched {fmt_hm(res.fetched_at)} Europe/Berlin"
    if not res.ok:
        return p + [f"_Skipped today: {md_escape(res.note)}._ <sub>{src}</sub>", ""]
    items = res.items if cap is None else res.items[:cap]
    if not items:
        return p + [f"_Nothing in this window today._ <sub>{src}</sub>", ""]
    p += [f"<sub>{src} · {md_escape(res.note)}</sub>", ""]
    headers, fn = type_table(ttype(items[0]))
    p += fold_table(headers, [fn(key, it, results) for it in items], visible)
    if cap is not None and len(res.items) > cap:
        p += ["", f"<sub>{len(res.items) - cap} more in the archive file for today.</sub>"]
    return p + [""]


def render_today(results, ents, tech_x) -> list[str]:
    b = []

    def ok(k):
        r = results.get(k)
        return r.items if r and r.ok else []
    stories = [x for x in cluster_stories(results) if len(x["outlets"]) >= 2]
    if stories:
        st = stories[0]
        b.append(f"**Biggest story:** {ttl(st['rep'][1], 80)} — carried by {len(st['outlets'])} outlets "
                 f"({md_escape(', '.join(st['outlets'][:4]))}).")
    gh = [i for i in ok("gh_daily") if i.get("gained") is not None]
    if gh:
        top = max(gh, key=lambda i: i["gained"])
        b.append(f"**Most stars today:** {ttl(top, 50)} — {md_escape(why('gh_daily', top))} "
                 f"(+{fmt_int(top['gained'])} today, {momentum('gh_daily', top)}).")
    multi = [e for e in ents if len(e.families) >= 2 and not set(e.families) <= PULSE_FAMILIES]
    if multi:
        e = max(multi, key=lambda x: (len(x.families), x.score))
        b.append(f"**On the most sources:** {ttl(e.item, 60)} — {len(e.families)} sources ({md_escape(', '.join(e.families))}).")
    hn = ok("hn_front")
    if hn:
        b.append(f"**Top on Hacker News:** {ttl(hn[0], 70)} — {key_metric('hn_front', hn[0])}.")
    q = {i["series"]: i for i in ok("fred") if i.get("series")}
    if "SP500" in q or "NASDAQCOM" in q:
        bits = [f"{md_escape(i['title'])} {_num(i['value'], i['unit'])} ({i['change']:+.2f}%, {md_escape(i['asof'])})"
                for s_ in ("SP500", "NASDAQCOM") if (i := q.get(s_))]
        b.append("**US markets (last close published on FRED):** " + ", ".join(bits) + ".")
    pp = ok("hf_papers")
    if pp:
        b.append(f"**Most upvoted paper:** {ttl(pp[0], 70)} — {fmt_int(pp[0].get('upvotes'))} upvotes.")
    lm = ok("openrouter")
    if lm:
        b.append(f"**Newest hosted model:** {ttl(lm[0], 50)} — {key_metric('openrouter', lm[0])}.")
    kev = ok("kev")
    if kev:
        recent = [k for k in kev if k["added"] == kev[0]["added"]]
        names = ", ".join(md_escape(re.sub(r"\s*\([^)]*\)", "", k["product"])) for k in recent[:4])
        b.append(f"**Exploited in the wild:** CISA added {len(recent)} on {kev[0]['added']} ({names}); {len(kev)} in 14 days.")
    coins = ok("coingecko_markets")
    if coins:
        c = coins[0]
        b.append(f"**Crypto:** {ttl(c, 30)} at ${_price(c.get('price'))} ({_pct(c.get('change_24h'))} in 24 h, "
                 f"{_pct(c.get('change_7d'))} in 7 d).")
    if tech_x:
        t = tech_x[0]
        posts = f"{t['posts']} posts" if t.get("posts") and t["posts"] != "—" else "volume not shown"
        b.append(f"**Tech on X:** {md_link(t['name'], t['url'])} ({posts}, {md_escape(t['region'])} list).")
    now = datetime.now(timezone.utc)
    la = [x for x in ok("launches") if x.get("net") and x["net"] >= now]   # the upcoming feed also lists launches already flown
    if la:
        b.append(f"**Next launch:** {ttl(la[0], 60)} — {key_metric('launches', la[0])}.")
    return [f"- {x}" for x in b[:11]]


def top_signals(ents, n: int):
    pool = [e for e in ents if not set(e.families) <= PULSE_FAMILIES and e.best_pct != UNRANKED_BASE]
    pool.sort(key=lambda e: (e.score, len(e.families), e.best_pct), reverse=True)
    return pool[:n]


def render_top_signals(ents, results, n: int, visible: int, prefix: str) -> list[str]:
    top = top_signals(ents, n)
    if not top:
        return ["_No ranked source answered today._", ""]
    headers = ["Item", "Type", "Why it matters", "Key metric", "Momentum", "Seen on", "Industry", "Score"]
    rows = []
    for e in top:
        k, it = e.key, e.item
        t = ttype(it)
        rows.append([ttl(it, 60), f"{TYPE_LABEL.get(t, t)}", md_escape(why(k, it)),
                     key_metric(k, it), momentum(k, it), seen_cell(it), ind_cell(it), f"**{e.score}**"])
    return fold_table(headers, rows, visible) + [
        "", f"<sub>Score = 100 × ({W_RANK} × best rank percentile + {W_SPREAD} × extra sources ÷ {SPREAD_CAP}, capped). "
        f"[How the score works]({prefix}docs/methodology.md#score).</sub>", ""]


def industry_members(ents) -> dict[str, list]:
    out = {s: [] for s in IND_ORDER}
    for e in ents:
        for s in e.industries:
            out[s].append(e)
    for s in out:
        out[s].sort(key=lambda e: (e.score, len(e.families)), reverse=True)
    return out


def strongest_signal(e) -> str:
    k, it = e.key, e.item
    m = momentum(k, it)
    base = key_metric(k, it)
    return base + (f" · {m}" if m != "—" and m not in base else "")


def render_matrix(members, prefix: str) -> list[str]:
    rows = []
    for slug, emo, title, short, intro, *_ in ALL_INDUSTRIES:
        ms = members[slug]
        link = f"[open]({prefix}industries/{slug}.md)"
        if not ms:
            rows.append([f"{title}", "0", "_Nothing today_", "—", "—", link])
            continue
        e = ms[0]
        fams = len({f for m in ms for f in m.families})
        rows.append([f"[{title}](#ind-{slug})", f"**{len(ms)}** <sub>{fams} sources</sub>", ttl(e.item, 55),
                     strongest_signal(e), str(e.score), link])
    return [table(["Industry", "Items", "Top item", "Strongest signal", "Score", "File"], rows, numbered=False), ""]


def render_industry_section(slug: str, members, results, visible: int, cap: int, prefix: str) -> list[str]:
    _s, emo, title, short, intro, *_ = IND[slug]
    ms = members[slug]
    p = [f'<a id="ind-{slug}"></a>', "", f"### {title}", "",
         f"{intro} **{len(ms)} items** · [full list →]({prefix}industries/{slug}.md)", ""]
    if not ms:
        return p + ["_Nothing today. No source returned an item that matches this industry's rules._", ""]
    p += fold_table(UNIFIED_H, [unified_row(e, results) for e in ms[:cap]], visible)
    if len(ms) > cap:
        p += ["", f"<sub>{len(ms) - cap} more in [{title}]({prefix}industries/{slug}.md).</sub>"]
    return p + [""]


def render_sources_table(results, x_note: str, enrich_note: str) -> list[str]:
    rows = []
    for n, (key, name, url, _fn) in enumerate(SOURCES, 1):
        r = results.get(key)
        if not r:
            continue
        rows.append([str(n), md_link(name, url), "OK" if r.ok else "Skipped", str(len(r.items)) if r.ok else "0",
                     "ranked" if key in RANKED else "unranked", fmt_hm(r.fetched_at), md_escape(clip(r.note, 120))])
    rows.append(["—", "X trends", "OK" if "reused" in x_note else "Skipped", "—", "—", "—", md_escape(x_note)])
    rows.append(["—", "Licence, topics and age for trending repos", "OK" if "added for" in enrich_note else "Skipped",
                 "—", "—", "—", md_escape(enrich_note)])
    return [table(["#", "Source", "Status", "Items", "Rank use", "Fetched", "How it is read"], rows, numbered=False)]


def render_x(tech_x, x_sections, full: bool) -> list[str]:
    if not tech_x:
        return ["_No tech topics in today's X trend lists, or the lists were not captured yet._", ""]
    p = ["Post volume is the `tweet_count` X showed when the lists were captured. A dash means X showed no number.", ""]
    rows = []
    for t in tech_x[:12]:
        inds = classify("x", {"title": t["name"], "url": "", "kind": "x"})
        rows.append([md_link(t["name"], t["url"]), md_escape(t["posts"]), md_escape(t["region"]), ind_cell({"_ind": inds}),
                     md_escape(clip(t["context"], 100)) if "No independently confirmed" not in t["context"] else "—"])
    p += fold_table(["Trend", "Posts", "List", "Industry", "Context"], rows, 12)
    if full and x_sections:
        p += ["", "<details>", "<summary>Full X trend lists (all topics, not just tech)</summary>", ""]
        for region, rows_ in x_sections.items():
            p += [f"#### {region}", "", table(["Trend", "Posts"], [[md_link(r["name"], r["url"]), md_escape(r["posts"])] for r in rows_]), ""]
        p.append("</details>")
    return p + [""]


def render_maintainer(results) -> list[str]:
    r = results.get("maintainer")
    p = ["The maintainer's own projects. **This is not a ranking.** They show up in the tables above only when a source "
         "listed them on its own.", ""]
    if not r or not r.ok or not r.items:
        return p + ["- [mjmirza on GitHub](https://github.com/mjmirza)", ""]
    for it in r.items:
        p.append(f"- {md_link(it['title'], it['url'])} — {md_escape(it.get('desc'))} ({fmt_int(it.get('stars'))} stars)")
    return p + [""]


def render_page(results, ents, fetched_at, tech_x, x_sections, x_note, enrich_note, archive_links, mode: str,
                windows=None, since=None) -> str:
    readme = mode == "readme"
    prefix = "" if readme else "../../../"
    okn, total = count_ok(results)
    members = industry_members(ents)
    live = sum(1 for s in IND_ORDER if members[s] and s != "other")
    windows = windows or {}
    p = []
    if readme:
        p += ["# awesome-trending", "",
              "**What moved in tech, AI and the markets since yesterday, in one page, every morning.** "
              f"{total} public sources, {len(INDUSTRIES)} industries, stories ranked by how many outlets carry them, and "
              "every number linked to where it came from.", "",
              "**Who it is for:** developers and maintainers, AI engineers and researchers, founders and product people, "
              "investors and analysts, security teams, and anyone who wants the day's tech and market news without "
              "opening forty tabs.", "",
              f"[![Last commit](https://img.shields.io/github/last-commit/{REPO_OWNER}/{REPO_NAME})]({REPO_URL}/commits/main) "
              f"[![License](https://img.shields.io/badge/License-OpenRoots_ORA_2.3-2ea44f)](LICENSE) "
              f"[![Sources](https://img.shields.io/badge/sources_live_today-{okn}%2F{total}-informational)](#sources) "
              f"[![Industries](https://img.shields.io/badge/industries_with_items-{live}%2F{len(INDUSTRIES)}-blueviolet)](#map)", ""]
    else:
        p += [f"# awesome-trending — {fmt_date(fetched_at)}", ""]
    p += [f"**{fmt_date(fetched_at)}** · snapshot at {fmt_time(fetched_at)} · {okn}/{total} sources answered · "
          f"{len(ents)} distinct items today", "",
          "**Read it in this order:** 30 seconds → what's shaking the market → since yesterday → top signals → "
          "month → AI labs → your industry. Everything else is folded.", "",
          f"**Start here:** Developers [signals](#signals) · [dev tools](#ind-devtools) · [month](#month) | "
          f"AI [labs](#labs) · [media](#media) · [AI & LLMs](#ind-ai-llms) | "
          f"Founders & investors [shaking](#shaking) · [markets](#ind-markets-economy) · [fintech](#ind-fintech) | "
          f"Security [cybersecurity](#ind-cybersecurity) · [status](#status) | "
          f"Markets [markets strip](#markets) · [crypto](#ind-crypto-web3)", ""]
    if readme:
        p += [f"**Follow it:** [RSS feed]({RAW_BASE}/feeds/daily.xml) · [JSON]({RAW_BASE}/feeds/daily.json) · "
              "or watch the repo for the daily commit.", ""]
    nav = ["[30 seconds](#today)", "[Shaking](#shaking)", "[Since yesterday](#since)", "[Top signals](#signals)", "[Month](#month)",
           "[Week](#week)", "[Year](#year)", "[AI labs](#labs)", "[AI media](#media)", "[Industry map](#map)",
           "[Industries](#industries)", "[By source](#by-source)", "[Status](#status)", "[X](#x)",
           "[Maintainer](#maintainer)"]
    nav += (["[Archive](#archive)"] if readme else []) + ["[Sources](#sources)"]
    p += [" · ".join(nav), "", '<a id="today"></a>', "", "## Today in 30 seconds", ""]
    p += render_today(results, ents, tech_x) + [""]
    p += ['<a id="shaking"></a>', "", "## What's shaking the market today", ""]
    p += render_shaking(results, 10 if readme else 20)
    p += ['<a id="markets"></a>', "", "**Markets strip**", ""] + render_markets(results)
    p += ['<a id="since"></a>', "", "## Since yesterday", ""] + render_since(since, results, prefix)
    p += [TABS, "", '<a id="signals"></a>', "", "## Top signals today", "",
          "One score for everything: how high an item ranks in its own source, plus how many separate sources list it.", ""]
    p += render_top_signals(ents, results, 15 if readme else 30, 10 if readme else 15, prefix)
    for w, label, days in [WINDOWS[1], WINDOWS[0], WINDOWS[2]]:
        wents, n_days = windows.get(w, ([], 0))
        p += render_window_compact(w, label, wents, results, 20 if w == "month" else 15, n_days, days)
        if not readme:
            p[-2:-1] = [x.replace("](windows/", f"]({prefix}windows/") for x in p[-2:-1]]
    p += ['<a id="labs"></a>', "", "## AI labs & big players", "",
          f"One row per lab. Click a lab for its announcements, models, SDK releases, incidents and leaderboard positions "
          f"([full page]({prefix}labs/README.md)).", ""]
    p += render_labs_matrix(results, prefix, f"{prefix}labs/README.md")
    p += ['<a id="media"></a>', "", "## AI media: video, image, audio & voice", ""]
    p += [x.replace("](industries/", f"]({prefix}industries/") for x in render_media(results, 10 if readme else 20, 30 if readme else 60)]
    p += ['<a id="map"></a>', "", "## Industry map", "",
          "One row per industry. **Top item** is its highest-scoring item today. An item can sit in more than one industry.", ""]
    p += render_matrix(members, prefix)
    p += ['<a id="industries"></a>', "", "## Industries", "",
          f"Top {'3' if readme else '10'} per industry, highest score first (more behind \"Show more\"). "
          "The same columns in every industry.", ""]
    for slug in IND_ORDER:
        p += render_industry_section(slug, members, results, 3 if readme else 10, 10, prefix)
        p += ["<sub>[↑ Industry map](#map)</sub>", ""]
    p += ['<a id="by-source"></a>', "", "## By source", "",
          ("One line per source with its #1 item. The full lists are in [today's archive file]"
           f"({archive_links[0][1] if archive_links else 'archive/'}). Click a group to open it." if readme else
           "The raw lists, grouped by kind of source. Each item type has its own columns. Click a group to open it."), ""]
    for anchor, heading, keys in GROUPS:
        present = [k for k in keys if k in results]
        if not present:
            continue
        n_items = sum(len(results[k].items) for k in present if results[k].ok)
        n_ok = sum(1 for k in present if results[k].ok)
        p += [f'<a id="{anchor}"></a>', "", "<details>",
              f"<summary><b>{heading}</b> · {n_items} items from {n_ok}/{len(present)} sources</summary>", ""]
        if readme:
            p += compact_group(present, results)
        else:
            for k in present:
                p += source_block(k, results, 10, 15)
        p += ["</details>", ""]
    p += ['<a id="status"></a>', "", "## Platform status", "",
          "Incidents in the last 72 hours on platforms and AI APIs most teams depend on.", ""]
    for k in STATUS_KEYS:
        p += source_block(k, results, 3 if readme else 5, 10, "###")
    p += ['<a id="x"></a>', "", "## Tech on X", ""] + render_x(tech_x, x_sections, full=not readme)
    p += ['<a id="maintainer"></a>', "", "## From the maintainer", ""] + render_maintainer(results)
    if readme:
        p += ['<a id="archive"></a>', "", "## Archive", "", "<details>", "<summary>Every past day</summary>", ""]
        p += [f"- [{label}]({rel})" for label, rel in archive_links] + ["", "</details>", ""]
        p += ["## Contribute", "",
              f"- Submit a repo with the [issue form]({SUBMIT_URL}). Tables are rebuilt from the sources every morning.",
              "- Found it useful? A star helps other people find it. Spotted a wrong number? Open an issue with the row.",
              "- How items are scored, clustered and sorted into industries: [docs/methodology.md](docs/methodology.md).",
              "- Full source list and how to run it: [CONTRIBUTING.md](CONTRIBUTING.md) · [badge](docs/badge.md).",
              LICENSE_LINE, ""]
    p += ['<a id="sources"></a>', "", "## Sources", "",
          f"Fetched {fmt_date(fetched_at)} at {fmt_time(fetched_at)}. Every figure comes from the source in its row. "
          "A dash means the source gave no number. Nothing is estimated or invented.", ""]
    p += render_sources_table(results, x_note, enrich_note) + [""]
    return "\n".join(p).rstrip() + "\n"


def _anchor(heading: str) -> str:
    return re.sub(r"[^\w\- ]", "", heading.lower()).strip().replace(" ", "-")


def render_industry_file(slug: str, members, results, fetched_at: datetime) -> str:
    _s, emo, title, short, intro, rx, topics = IND[slug]
    ms = members[slug]
    p = [f"# {title}", "", intro, "",
         f"**{fmt_date(fetched_at)}** · {fmt_time(fetched_at)} · {len(ms)} items · daily snapshot, rebuilt every morning.", "",
         f"[← Main page](../README.md) · [Industry map](../README.md#map) · [How items get here](../docs/methodology.md#industries) · "
         f"[Submit a repo]({SUBMIT_URL})", ""]
    if not ms:
        return "\n".join(p + ["_Nothing today. No source returned an item that matches this industry's rules._", ""])
    fams = sorted({f for m in ms for f in m.families})
    by_type: dict[str, list] = {}
    for e in ms:
        by_type.setdefault(ttype(e.item), []).append((e.key, e.item))
    order = sorted(by_type, key=lambda t: -len(by_type[t]))
    p += [f"**Sources with items here ({len(fams)}):** {md_escape(', '.join(fams))}", "",
          "**By type:** " + " · ".join(f"[{TYPE_LABEL.get(t, t)}](#{_anchor(TYPE_LABEL.get(t, t))}) "
                                       f"({len(by_type[t])})" for t in order), "",
          "## Top 10", ""]
    p += fold_table(UNIFIED_H, [unified_row(e, results) for e in ms[:10]], 10) + [""]
    for t in order:
        p += [f"## {TYPE_LABEL.get(t, t)}", ""]
        headers, fn = type_table(t)
        p += fold_table(headers, [fn(k, it, results) for k, it in by_type[t][:20]], 10)
        if len(by_type[t]) > 20:
            p += ["", f"<sub>{len(by_type[t]) - 20} more in today's archive.</sub>"]
        p.append("")
    p += [f"<sub>Every figure comes from the linked source, fetched {fmt_time(fetched_at)}. "
          "See the [sources table](../README.md#sources).</sub>", ""]
    return "\n".join(p)


# ===========================================================================
# What's shaking the market, markets strip, AI labs, AI media, time windows
# ===========================================================================

NON_ENTITY = {"fred", "ecb_fx", "arena_text", "arena_image", "arena_video"}


def today_keys(results) -> list[str]:
    return [k for k in results if k not in WINDOW_OF and k not in NON_ENTITY]


def _ok_items(results, key):
    r = results.get(key)
    return r.items if r and r.ok else []


# ---- Story clustering -------------------------------------------------------------------

STORY_STOP = set("""a an and or of to in on for with at by from as is are was were be been being it its this that these
those after before over under amid into about than more most new says say said will would could can may might not no
how why what who when where which while up down out off vs via per year years week weeks day days today report reports
reported update updates first last next big top just now also amp us his her their our your you we they he she them
get gets got make makes made take takes set sets back still ahead plan plans here there all any some one two three
ai inc ceo co ltd llc corp company companies raise raises raised series round rounds funding million billion
best review reviews guide tool tools ways agent agents model models plans report reports reportedly says
new launch launches rival race build builds""".split())
STORY_HOURS = 36
STORY_MERGE_WORDS = 2  # stories are joined when their common words overlap this much
STORY_OVERLAP = 0.5    # share of the shorter headline's distinctive words that must match the story seed
NEWS_KINDS = ("news", "lab", "hn")


def _story_tokens(title: str) -> set[str]:
    toks = set()
    for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9&.+-]*", (title or "").replace("’", "'")):
        w = w.lower().strip(".-+").removesuffix("'s")
        if len(w) > 4 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        if len(w) >= 3 and w not in STORY_STOP and not w.isdigit():
            toks.add(w)
    return toks


def _outlet(key: str, it: dict, results) -> str:
    if it["kind"] == "hn":
        return "Hacker News"
    return it.get("outlet") or results[key].name.split(" · ")[0]


def _outlet_key(name: str) -> str:
    """Compare outlet names without case or a leading "The", so "The New York Times" and "New York Times" count once."""
    return re.sub(r"^the\s+", "", (name or "").strip().lower())


def story_candidates(results) -> list[tuple[str, dict]]:
    ref = datetime.now(timezone.utc)
    out = []
    for k in today_keys(results):
        if k in ("hn_show", "hn_ask") or k.startswith("st_") or k.endswith("status"):
            continue
        for it in _ok_items(results, k):
            if it["kind"] not in NEWS_KINDS or it.get("title_from_url"):
                continue
            when = it.get("published") or it.get("created")
            if within(when, STORY_HOURS, ref):
                out.append((k, it))
    return out


def cluster_stories(results) -> list[dict]:
    cands = story_candidates(results)
    toks = [_story_tokens(it["title"]) for _k, it in cands]
    df: dict[str, int] = {}
    for ts in toks:
        for t in ts:
            df[t] = df.get(t, 0) + 1
    cap = max(4, int(len(cands) * 0.06))       # words in more than 6% of headlines are too common to link stories
    strong = [{t for t in ts if df[t] <= cap} for ts in toks]
    clusters: list[dict] = []
    order = sorted(range(len(cands)), key=lambda i: -(len(strong[i])))
    for i in order:
        best, best_n = None, 0
        for c in clusters:
            shared = len(strong[i] & c["seed"])
            small = min(len(strong[i]), len(c["seed"])) or 1
            if shared >= 2 and shared / small >= STORY_OVERLAP:
                n = shared / small
                if n > best_n:
                    best, best_n = c, n
        if best is None:
            clusters.append({"seed": strong[i], "members": [i]})
        else:
            best["members"].append(i)
    # Second pass: join clusters about the same event that the first pass split (e.g. one IPO, many angles).
    def signature(c):
        cnt: dict[str, int] = {}
        for i in c["members"]:
            for t in toks[i]:
                cnt[t] = cnt.get(t, 0) + 1
        need = max(2, (len(c["members"]) + 1) // 2)
        return {t for t, n in cnt.items() if n >= need}
    merged = True
    while merged:
        merged = False
        big = [c for c in clusters if len(c["members"]) >= 2]
        sigs = [signature(c) for c in big]
        for a in range(len(big)):
            for b in range(a + 1, len(big)):
                shared = sigs[a] & sigs[b]
                if (len(shared) >= 3 or (len(shared) >= STORY_MERGE_WORDS and any(df[t] <= cap for t in shared))):
                    big[a]["members"] += big[b]["members"]
                    clusters.remove(big[b])
                    merged = True
                    break
            if merged:
                break
    stories = []
    for c in clusters:
        mem = [cands[i] for i in c["members"]]
        outlets, fams = [], []
        for k, it in mem:
            o = _outlet(k, it, results)
            if all(_outlet_key(o) != _outlet_key(x) for x in outlets):
                outlets.append(o)
            f = family(k, results)
            if f not in fams:
                fams.append(f)
        sig = signature(c) if len(c["members"]) >= 2 else toks[c["members"][0]]
        central = sorted(range(len(mem)), key=lambda x: -len(toks[c["members"][x]] & sig))
        mem = [mem[x] for x in central]           # most central headline first
        with_desc = [(k, it) for k, it in mem if (it.get("desc") or "").strip() and it.get("via") != "Google News"]
        rep = with_desc[0] if with_desc else mem[0]
        inds = []
        for k, it in mem:
            for s in (it.get("_ind") or classify(k, it)):
                if s not in inds and s != "other":
                    inds.append(s)
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        latest = max(((it.get("published") or it.get("created") or epoch) for _k, it in mem), default=epoch)
        stories.append({"rep": rep, "members": mem, "outlets": outlets, "families": fams, "industries": inds,
                        "latest": latest,
                        "why": first_sentence(with_desc[0][1]["desc"], 150) if with_desc else ""})
    stories.sort(key=lambda s: (-len(s["outlets"]), -len(s["families"]), -s["latest"].timestamp()))
    return stories


def render_shaking(results, n: int) -> list[str]:
    stories = [s for s in cluster_stories(results) if len(s["outlets"]) >= 2][:n]
    p = [f"The biggest stories of the last {STORY_HOURS} hours across tech, innovation and the economy, ranked by how many "
         "separate outlets and platforms carry the same story. Headlines are grouped when they share distinctive "
         "words and names ([method](docs/methodology.md#shaking)).", ""]
    if not stories:
        return p + ["_Nothing today: no story was carried by two or more outlets in the window._", ""]
    rows = []
    for s in stories:
        k, it = s["rep"]
        links = []
        for mk, mit in s["members"]:
            o = _outlet(mk, mit, results)
            if all(_outlet_key(o) != _outlet_key(lbl) for lbl, _u in links):
                links.append((o, mit.get("discuss") if mit["kind"] == "hn" else mit["url"]))
            if len(links) >= 3:
                break
        outl = ", ".join(s["outlets"][:4]) + (f" +{len(s['outlets']) - 4}" if len(s["outlets"]) > 4 else "")
        rows.append([ttl(it, 90), md_escape(s["why"]) or "—", f"**{len(s['outlets'])}** <sub>{md_escape(outl)}</sub>",
                     " · ".join(md_link(clip(lbl, 24), u) for lbl, u in links),
                     ", ".join(f"{IND[x][3]}" for x in s["industries"][:2]) or "—", fmt_day(s["latest"])])
    return p + fold_table(["Story", "Why it matters", "Outlets", "Read it at", "Industry", "Latest"], rows, n) + [""]


# ---- Markets strip --------------------------------------------------------------------------

MARKETS_NOT_SHOWN = ("DAX, gold and single stocks (NVDA, MSFT, AAPL, GOOGL, AMZN, META, TSLA, TSM) are not shown: no "
                     "keyless source that allows this kind of reuse was found.")


def _num(v, unit: str) -> str:
    if v is None:
        return "—"
    if unit == "%":
        return f"{v:.2f}%"
    if unit == "USD per EUR":
        return f"{v:.4f}"
    return f"{v:,.2f}"


def render_markets(results) -> list[str]:
    rows = []
    for k in ("fred", "ecb_fx"):
        for it in _ok_items(results, k):
            ch = it.get("change")
            chs = "—" if ch is None else (f"{ch:+.0f} bp" if it.get("change_kind") == "bp" else f"{ch:+.2f}%")
            rows.append([md_link(it["title"], it["url"]), _num(it.get("value"), it.get("unit")), chs,
                         f"{it.get('asof')} <sub>vs {it.get('prev_date')}</sub>", md_escape(it.get("outlet"))])
    for it in _ok_items(results, "coingecko_markets"):
        if it["title"].startswith(("Bitcoin", "Ethereum")):
            rows.append([md_link(it["title"], it["url"]), f"${_price(it.get('price'))}", _pct(it.get("change_24h")),
                         f"{fmt_day(results['coingecko_markets'].fetched_at)} <sub>live, 24 h change</sub>", "CoinGecko"])
    if not rows:
        return ["_Market data was skipped today. See the sources table._", ""]
    return [table(["Indicator", "Level", "Change", "As of", "Source"], rows, numbered=False), "",
            "<sub>Index levels, the 10-year yield and Brent are the latest values FRED has published (US closes, one or "
            "more days old). EUR/USD is the ECB's daily reference rate. Changes compare the last two published values. "
            + MARKETS_NOT_SHOWN + "</sub>", ""]


# ---- AI labs ------------------------------------------------------------------------------

def lab_view(results) -> dict[str, dict]:
    view = {}
    for slug, name, _q, feeds, repos, st, *_ in LABS:
        official = [it for k in feeds for it in _ok_items(results, k)]
        press = _ok_items(results, f"lab_news_{slug}")
        models = [it for k in ("lab_models", "lab_hf") for it in _ok_items(results, k) if it.get("lab") == slug]
        sdk = [it for it in _ok_items(results, "lab_releases") if it.get("lab") == slug]
        inc = _ok_items(results, st) if st else []
        arena = [it for k in ("arena_text", "arena_image", "arena_video") for it in _ok_items(results, k)
                 if it.get("lab") == slug]
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        models.sort(key=lambda x: x.get("created") or epoch, reverse=True)
        official.sort(key=lambda x: x.get("published") or epoch, reverse=True)
        view[slug] = {"name": name, "official": official, "press": press, "models": models, "sdk": sdk, "inc": inc,
                      "arena": arena, "status": st}
    return view


def _lab_cells(v) -> list[str]:
    latest = (v["official"] + v["press"])
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    latest = sorted(latest, key=lambda x: x.get("published") or epoch, reverse=True)
    head = f"{ttl(latest[0], 70)} <sub>{md_escape(latest[0].get('outlet'))} · {fmt_day(latest[0].get('published'))}</sub>" \
        if latest else "—"
    model = f"{ttl(v['models'][0], 40)} <sub>{fmt_day(v['models'][0].get('created'))}</sub>" if v["models"] else "—"
    sdk = f"{md_link(clip(v['sdk'][0]['release_title'], 30), v['sdk'][0]['url'])} <sub>{md_escape(v['sdk'][0]['project'].split('/')[1])} · " \
          f"{fmt_day(v['sdk'][0].get('published'))}</sub>" if v["sdk"] else "—"
    inc = "—" if not v["status"] else (f"**{len(v['inc'])}**" if v["inc"] else "0")
    text = [a for a in v["arena"] if a.get("board") == "text"]
    arena = f"#{text[0]['rank']} {md_escape(clip(text[0]['title'], 30))}" if text else "—"
    return [f"{len(v['press'])} + {len(v['official'])}", head, model, sdk, inc, arena]


LAB_HEADERS = ["Lab", "Headlines + official posts", "Latest", "Newest model", "Latest SDK release", "Incidents 72 h",
               "Best on LMArena text"]


def render_labs_matrix(results, prefix: str, link_file: str) -> list[str]:
    view = lab_view(results)
    rows = [[md_link(v["name"], f"{link_file}#lab-{slug}")] + _lab_cells(v) for slug, v in view.items()]
    return [table(LAB_HEADERS, rows, numbered=False), "",
            "<sub>Headlines: Google News search for the lab, last 48 h. Official posts: the lab's own blog or newsroom "
            "feed, last 14 days. Models: OpenRouter (60 days) and Hugging Face (30 days). SDK releases: GitHub "
            "releases feeds (14 days). Incidents: the lab's public status page. A dash means no source covers it.</sub>", ""]


def render_labs_file(results, fetched_at: datetime) -> str:
    view = lab_view(results)
    p = ["# AI labs & big players", "",
         "Announcements, model releases, SDK releases, incidents and leaderboard positions for the big AI labs, rebuilt "
         "every morning. Every row links to its source.", "",
         f"**{fmt_date(fetched_at)}** · {fmt_time(fetched_at)} · [← Main page](../README.md) · "
         "[How it works](../docs/methodology.md#labs)", "", "## Overview", ""]
    p += render_labs_matrix(results, "../", "")
    for slug, v in view.items():
        p += [f'<a id="lab-{slug}"></a>', "", f"## {v['name']}", ""]
        news = v["official"] + v["press"]
        if news:
            rows = [[ttl(it, 90), "official" if it in v["official"] else "press", outlet_cell(it),
                     fmt_day(it.get("published"))] for it in news]
            p += ["**Announcements and headlines**", ""] + fold_table(["Headline", "Kind", "Outlet", "Published"], rows, 6) + [""]
        else:
            p += ["_No announcement or headline in the window._", ""]
        if v["models"]:
            rows = []
            for it in v["models"][:12]:
                if it["kind"] == "llm":
                    rows.append([ttl(it, 50), "OpenRouter", f"${_price(it.get('price_in'))} in / ${_price(it.get('price_out'))} out "
                                 f"per 1M · {fmt_compact(it.get('context'))} ctx", fmt_day(it.get("created"))])
                else:
                    rows.append([ttl(it, 50), "Hugging Face", f"{md_escape(it.get('task')) or '—'} · {fmt_int(it.get('likes'))} likes"
                                 f" · {md_escape(it.get('license')) or 'licence not stated'}", fmt_day(it.get("created"))])
            p += ["**Model releases**", ""] + fold_table(["Model", "Where", "Details", "Added"], rows, 5) + [""]
        if v["sdk"]:
            rows = [[md_link(clip(it["release_title"], 50), it["url"]), md_escape(it["project"]),
                     "pre-release" if it.get("prerelease") else "stable", fmt_day(it.get("published"))] for it in v["sdk"]]
            p += ["**SDK and tool releases**", ""] + fold_table(["Release", "Repository", "Stage", "Published"], rows, 5) + [""]
        if v["status"]:
            if v["inc"]:
                rows = [[ttl(it, 70), md_escape(it.get("impact")) or "—", md_escape(it.get("status")) or "—",
                         fmt_day(it.get("published"))] for it in v["inc"]]
                p += ["**Incidents (last 72 h)**", ""] + fold_table(["Incident", "Impact", "Status", "Started"], rows, 5) + [""]
            else:
                p += ["**Incidents (last 72 h):** none on the public status page.", ""]
        if v["arena"]:
            rows = [[md_escape(a["board"].replace("_", " ")), md_escape(a["title"]), f"#{a['rank']}",
                     f"{a['rating']:.0f}" if a.get("rating") else "—", fmt_int(a.get("votes")), md_escape(a.get("asof"))]
                    for a in v["arena"]]
            p += ["**LMArena positions**", ""] + fold_table(["Board", "Model", "Rank", "Rating", "Votes", "Published"], rows, 5) + [""]
    p += [f"<sub>Every figure comes from the linked source, fetched {fmt_time(fetched_at)}. "
          "See the [sources table](../README.md#sources).</sub>", ""]
    return "\n".join(p)


# ---- AI media ------------------------------------------------------------------------------

PROVIDER_MODALITY = {"OpenAI Sora": "video", "Google Veo": "video", "Google Nano Banana": "image", "Runway": "video",
                     "Luma AI": "video", "Pika": "video", "Kling": "video", "MiniMax Hailuo": "video",
                     "Higgsfield": "video", "Midjourney": "image, video", "Black Forest Labs (FLUX)": "image",
                     "Stability AI": "image, audio", "ElevenLabs": "voice, audio", "Suno": "music", "Udio": "music",
                     "HeyGen": "avatar video", "Synthesia": "avatar video", "Adobe Firefly": "image, video",
                     "Ideogram": "image", "Krea": "image, video"}
TASK_MODALITY = {"text-to-video": "video", "image-to-video": "video", "text-to-image": "image",
                 "text-to-speech": "voice", "text-to-audio": "audio"}


def media_rows(results) -> list[list[str]]:
    rows, seen = [], set()
    news = []
    for k in today_keys(results):
        for it in _ok_items(results, k):
            if it["kind"] in ("news", "lab"):
                prov = media_provider(it["title"])
                if prov and title_key(it["title"]) not in seen:
                    seen.add(title_key(it["title"]))
                    news.append((prov, k, it))
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    news.sort(key=lambda x: x[2].get("published") or epoch, reverse=True)
    per = {}
    for prov, k, it in news:
        per.setdefault(prov, []).append((k, it))
    for prov, lst in per.items():
        for k, it in lst[:2]:
            rows.append([ttl(it, 80), md_escape(prov), PROVIDER_MODALITY.get(prov, "—"),
                         f"Headline · {md_escape(it.get('outlet'))}", fmt_day(it.get("published")), src_cell(k, results)])
    for k in ("arena_video", "arena_image"):
        for a in _ok_items(results, k)[:5]:
            rows.append([md_link(a["title"], a["url"]), md_escape(a.get("org")), "video" if k == "arena_video" else "image",
                         f"#{a['rank']} on LMArena {a['board'].replace('_', '-')}, rating {a['rating']:.0f} "
                         f"({fmt_int(a.get('votes'))} votes)", md_escape(a.get("asof")), src_cell(k, results)])
    by_task: dict[str, int] = {}
    for it in _ok_items(results, "hf_media"):
        if by_task.get(it["task"], 0) >= 3:
            continue
        by_task[it["task"]] = by_task.get(it["task"], 0) + 1
        rows.append([ttl(it, 60), md_escape(it["title"].split("/")[0]), TASK_MODALITY.get(it["task"], it["task"]),
                     f"Trending on Hugging Face ({md_escape(it['task'])}) · {fmt_int(it.get('likes'))} likes · "
                     f"{md_escape(it.get('license')) or 'licence not stated'}",
                     f"created {fmt_day(it.get('created'))}", src_cell("hf_media", results)])
    return rows


def render_media(results, visible: int, cap: int) -> list[str]:
    rows = media_rows(results)
    p = ["Video, image, music, speech and voice generation: provider headlines (Google News and outlet feeds, "
         "up to 2 per provider), LMArena text-to-video and text-to-image leaders, and trending open models on Hugging Face.", ""]
    if not rows:
        return p + ["_Nothing today._", ""]
    return p + fold_table(["Model or story", "Provider", "Modality", "What's new", "Date", "Source"], rows[:cap], visible) + [
        "", "<sub>[All AI media items by type](industries/ai-media.md)</sub>" if visible < 20 else "", ""]


# ---- Time windows ----------------------------------------------------------------------------

WINDOWS = [("week", "This week", 7), ("month", "This month", 30), ("year", "This year", 365)]
HISTORY_START = "2026-11-19"
ROW_LINK_RE = re.compile(r"^\| \d+ \| \[((?:\\.|[^\]\\])+)\]\((\S+?)\)")


def archive_history(root: Path, today: datetime) -> dict[str, dict[str, str]]:
    """{date: {canonical url: title}} from the generated part of every earlier archive file."""
    out = {}
    base = root / "archive"
    if not base.is_dir():
        return out
    for path in sorted(base.rglob("*.md")):
        if path.name.endswith(".original.md"):
            continue
        try:
            day = datetime.strptime(path.stem, "%Y-%m-%d").date()
        except ValueError:
            continue
        if day >= today.date():
            continue
        text = path.read_text(encoding="utf-8")
        if GENERATED_START in text:
            text = text.split(GENERATED_START, 1)[1]
        seen = {}
        for line in text.splitlines():
            m = ROW_LINK_RE.match(line)
            if m:
                seen.setdefault(canonical_url(m.group(2)), m.group(1).replace("\\", ""))
        out[day.isoformat()] = seen
    return out


def rollup(history, today_ents, today: datetime, days: int):
    start = (today - timedelta(days=days - 1)).date().isoformat()
    dates = sorted(d for d in history if d >= start)
    today_s = today.date().isoformat()
    day_sets = {d: history[d] for d in dates}
    day_sets[today_s] = {canonical_url(e.item["url"]): e.item["title"] for e in today_ents}
    counts: dict[str, list[str]] = {}
    titles: dict[str, str] = {}
    for d, s in sorted(day_sets.items()):
        for u, t in s.items():
            counts.setdefault(u, []).append(d)
            titles.setdefault(u, t)
    rows = sorted(((u, ds) for u, ds in counts.items() if len(ds) >= 2), key=lambda x: (-len(x[1]), x[1][0]))
    return len(day_sets), rows, titles


def window_note(w: str, label: str, days: int, n_days: int) -> str:
    first = datetime.strptime(HISTORY_START, "%Y-%m-%d")
    return (f"**{label}** = the last {days} days. Native lists come straight from each platform's own {w} view. "
            f"The archive rollup counts how many archived days an item appeared on; the archive started on "
            f"{fmt_date(first)}, so it covers **{n_days} day{'s' if n_days != 1 else ''}** of this {days}-day window so far.")


def render_window_compact(w: str, label: str, ents, results, n: int, n_days: int, days: int) -> list[str]:
    p = [f'<a id="{w}"></a>', "", f"## {label}", "",
         f"Native {w} lists from GitHub, Hacker News, Dev.to and Hugging Face papers, scored together. "
         f"Archive history in this window: {n_days} of {days} days. [Full {w} list →](windows/{w}.md)", ""]
    if not ents:
        return p + ["_Nothing today: every source for this window was skipped._", ""]
    return p + fold_table(UNIFIED_H, [unified_row(e, results) for e in ents[:n]], min(n, 10)) + [""]


TABS = "**[Today](#today) · [Week](#week) · [Month](#month) · [Year](#year)**"


def render_window_file(w, label, days, ents, results, history_info, fetched_at) -> str:
    n_days, rows, titles = history_info
    keys = [k for k, v in WINDOW_OF.items() if v == w and k in results]
    p = [f"# {label} — awesome-trending", "", window_note(w, label, days, n_days), "",
         f"**{fmt_date(fetched_at)}** · {fmt_time(fetched_at)} · rebuilt every morning.", "",
         "**[Today](../README.md#today) · " + " · ".join(
             f"[{lb.split()[-1].capitalize()}]({x}.md)" if x != w else f"{lb.split()[-1].capitalize()}"
             for x, lb, _d in WINDOWS) + "**", "",
         f"## Top 25 of {label.lower()}", "",
         "Scored with the same formula as today ([methodology](../docs/methodology.md#windows)), using only this window's lists.", ""]
    p += (fold_table(UNIFIED_H, [unified_row(e, results) for e in ents[:25]], 10) if ents else
          ["_Nothing today: every source for this window was skipped._"]) + [""]
    p += ["## Native lists", ""]
    for k in keys:
        p += source_block(k, results, 10, None, "###")
    p += ["## Archive rollup", "",
          f"Items that appeared on at least two archived days in this window ({n_days} day{'s' if n_days != 1 else ''} of "
          f"history so far; the archive starts {HISTORY_START}).", ""]
    if rows:
        p += fold_table(["Item", "Days seen", "First seen", "Last seen"],
                        [[md_link(clip(titles[u], 80), u), f"{len(ds)} of {n_days}", ds[0], ds[-1]] for u, ds in rows[:50]], 15)
    else:
        p += ["_Not enough history yet: no item appears on two archived days._"]
    p += ["", f"<sub>Every figure comes from the linked source, fetched {fmt_time(fetched_at)}. "
          "See the [sources table](../README.md#sources).</sub>", ""]
    return "\n".join(p)



# ---- What changed since the previous archived day -----------------------------------------------

GH_TODAY_HEAD = re.compile(r"^#{2,4} .*GitHub trending( · today)?\s*$")


def previous_day_ranks(root: Path, today: datetime):
    """(date, {canonical url: rank}) for GitHub trending today in the newest earlier archive file."""
    base = root / "archive"
    files = []
    for path in base.rglob("*.md") if base.is_dir() else []:
        try:
            d = datetime.strptime(path.stem, "%Y-%m-%d").date()
        except ValueError:
            continue
        if d < today.date():
            files.append((d, path))
    if not files:
        return None, {}
    d, path = max(files)
    text = path.read_text(encoding="utf-8")
    if GENERATED_START in text:
        text = text.split(GENERATED_START, 1)[1]
    ranks, inside = {}, False
    for line in text.splitlines():
        if GH_TODAY_HEAD.match(line):
            inside = not ranks
            continue
        if inside:
            m = ROW_LINK_RE.match(line)
            if m:
                ranks.setdefault(canonical_url(m.group(2)), len(ranks) + 1)
            elif line.startswith("#"):
                inside = False
    return d, ranks


def since_yesterday(root: Path, fetched_at: datetime, ents, results, history):
    prev_dates = sorted(d for d in history if d < fetched_at.date().isoformat())
    if not prev_dates:
        return None
    prev = prev_dates[-1]
    seen = set(history[prev])
    new = [e for e in ents if canonical_url(e.item["url"]) not in seen
           and not set(e.families) <= PULSE_FAMILIES and e.best_pct != UNRANKED_BASE]
    new.sort(key=lambda e: (e.score, len(e.families), e.best_pct), reverse=True)
    carried = sum(1 for e in ents if canonical_url(e.item["url"]) in seen)
    _d, ranks = previous_day_ranks(root, fetched_at)
    moves = []
    for pos, it in enumerate(_ok_items(results, "gh_daily"), 1):
        before = ranks.get(canonical_url(it["url"]))
        moves.append((it, pos, before))
    climbers = sorted([m for m in moves if m[2] and m[2] > m[1]], key=lambda m: m[1] - m[2])[:5]
    entries = [m for m in moves if not m[2] and m[1] <= len(ranks)][:5]   # only within the depth listed yesterday
    return {"prev": prev, "new": new, "carried": carried, "climbers": climbers, "entries": entries,
            "has_ranks": bool(ranks), "depth": len(ranks)}


def render_since(info, results, prefix: str) -> list[str]:
    if not info:
        return ["_No earlier archived day to compare with yet._", ""]
    prev = datetime.strptime(info["prev"], "%Y-%m-%d")
    p = [f"Compared with the archive for **{fmt_date(prev)}**: **{len(info['new'])}** ranked items are new today, "
         f"**{info['carried']}** were already listed.", ""]
    if info["new"]:
        p += ["**New and highest-scoring**", ""] + fold_table(
            ["Item", "Type", "Why it matters", "Key metric", "Score", "Source"],
            [[ttl(e.item, 70), f"{TYPE_LABEL.get(ttype(e.item), '')}",
              md_escape(why(e.key, e.item)), key_metric(e.key, e.item), str(e.score), src_cell(e.key, results)]
             for e in info["new"][:5]], 5) + [""]
    if info["has_ranks"]:
        rows = [[ttl(it, 50), f"#{pos}", f"#{before}", f"up {before - pos}"] for it, pos, before in info["climbers"]]
        rows += [[ttl(it, 50), f"#{pos}", "not listed", "new"] for it, pos, _b in info["entries"]]
        if rows:
            p += ["**GitHub trending today: climbers and new entries**", "",
                  f"<sub>Against the top {info['depth']} archived for the previous day.</sub>", ""] + fold_table(
                ["Repository", "Today", "Previous day", "Move"], rows, 10) + [""]
    return p


# ---- Subscribable feeds (feeds/daily.json, feeds/daily.xml) ---------------------------------------

RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main"


def _iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None


def _ent_json(e) -> dict:
    it = e.item
    return {"title": it["title"], "url": it["url"], "type": ttype(it), "score": e.score, "seen_on": e.families,
            "industries": e.industries, "why": why(e.key, it), "key_metric": re.sub(r"[*`]", "", key_metric(e.key, it)),
            "source_key": e.key}


def build_feed_json(results, ents, windows, fetched_at, info) -> dict:
    stories = [s for s in cluster_stories(results) if len(s["outlets"]) >= 2][:20]
    okn, total = count_ok(results)
    view = lab_view(results)
    return {
        "date": fetched_at.date().isoformat(), "fetched_at": _iso(fetched_at), "timezone_shown": "Europe/Berlin",
        "home": REPO_URL, "methodology": f"{REPO_URL}/blob/main/docs/methodology.md",
        "sources_ok": okn, "sources_total": total,
        "stories": [{"title": s["rep"][1]["title"], "url": s["rep"][1]["url"], "why": s["why"],
                     "outlets": s["outlets"], "industries": s["industries"], "latest": _iso(s["latest"])} for s in stories],
        "markets": [{"name": it["title"], "value": it.get("value"), "previous": it.get("prev"), "as_of": it.get("asof"),
                     "change": round(it["change"], 4) if it.get("change") is not None else None,
                     "change_unit": "bp" if it.get("change_kind") == "bp" else "%", "source": it["url"]}
                    for k in ("fred", "ecb_fx") for it in _ok_items(results, k)],
        "top_signals": [_ent_json(e) for e in top_signals(ents, 30)],
        "windows": {w: [_ent_json(e) for e in windows[w][0][:15]] for w in windows},
        "labs": {slug: {"name": v["name"], "headlines": len(v["press"]), "official_posts": len(v["official"]),
                        "models": len(v["models"]), "sdk_releases": len(v["sdk"]),
                        "incidents_72h": len(v["inc"]) if v["status"] else None} for slug, v in view.items()},
        "since_previous_day": ({"compared_with": info["prev"], "new_ranked_items": len(info["new"]),
                                "carried_over": info["carried"]} if info else None),
        "licence": "LicenseRef-OpenRoots-ORA-2.3",
    }


def _x(s) -> str:
    return htmlmod.escape(str(s or ""), quote=True)


def build_feed_rss(feed: dict, fetched_at: datetime) -> str:
    pub = fetched_at.astimezone(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    day = feed["date"]
    items = []
    for s in feed["stories"][:10]:
        desc = (s["why"] + " " if s["why"] else "") + f"Carried by {len(s['outlets'])} outlets: {', '.join(s['outlets'][:6])}."
        items.append((f"{s['title']}", s["url"], desc, f"{day}:story:{s['url']}"))
    for e in feed["top_signals"][:15]:
        desc = f"{e['why']} · {e['key_metric']} · score {e['score']} · seen on {', '.join(e['seen_on'])}"
        items.append((f"{e['title']}", e["url"], desc, f"{day}:signal:{e['url']}"))
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0">', "<channel>",
           f"<title>awesome-trending · daily</title>", f"<link>{_x(REPO_URL)}</link>",
           f"<description>{_x('Daily scan of tech, AI and markets: the stories carried by the most outlets and the top-scoring items, each linked to its source.')}</description>",
           "<language>en</language>", f"<lastBuildDate>{pub}</lastBuildDate>"]
    for title, url, desc, guid in items:
        out += ["<item>", f"<title>{_x(title)}</title>", f"<link>{_x(url)}</link>", f"<description>{_x(desc)}</description>",
                f'<guid isPermaLink="false">{_x(guid)}</guid>', f"<pubDate>{pub}</pubDate>", "</item>"]
    out += ["</channel>", "</rss>", ""]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Methodology document (generated from the rules above, so it never drifts)
# ---------------------------------------------------------------------------

def render_methodology() -> str:
    p = ["# Methodology", "",
         "How awesome-trending turns public sources into one scored, industry-sorted page. This file is generated from "
         "`scripts/update.py --docs`, so the document and the code cannot drift apart.", "",
         '<a id="score"></a>', "", "## Score", "", "Every distinct item gets one score from 0 to 100:", "",
         "```text",
         f"score = 100 × ( {W_RANK} × best_rank_percentile  +  {W_SPREAD} × min(sources − 1, {SPREAD_CAP}) / {SPREAD_CAP} )",
         "```", "",
         "- **best_rank_percentile**: for each *ranked* source that lists the item, `1 − (position − 1) / list length`. "
         "Position 1 of 20 is 1.0 and position 11 of 20 is 0.5. The best value across sources counts.",
         f"- Items found only in *unranked* sources (news feeds, registries, advisories, releases, markets) get {UNRANKED_BASE}.",
         "- **sources** counts distinct platforms, not lists: GitHub trending today, this week and per language all count as GitHub.",
         "- Items are merged by normalised URL (GitHub repos by owner/name, papers by arXiv id, a paper's code repo joins its repo) "
         "and, for headlines and discussions, by normalised title.",
         "- **Top signals** leaves out items seen only on public-pulse sources (Google Trends, Wikipedia, Mastodon, Bluesky) "
         "and items with no ranked source.", "",
         "Example: a repo at position 2 of 16 on GitHub trending that is also on Hacker News scores "
         f"`100 × ({W_RANK} × 0.94 + {W_SPREAD} × 1/3) = {round(100 * (W_RANK * (1 - 1 / 16) + W_SPREAD / 3))}`.", "",
         "**Ranked sources:** " + ", ".join(f"`{k}`" for k in sorted(RANKED)), "",
         "## Table designs", "",
         "Each item type has its own columns. Every table ends with **Seen on** (number of platforms listing the item), "
         "**Industry** and **Source**.", "", "| Type | Columns |", "| --- | --- |"]
    for t, note in TYPE_DESIGN_NOTE.items():
        p.append(f"| {TYPE_LABEL.get(t, t)} | {md_escape(note)} |")
    p += ["", "Industry tables mix types, so they use one shared layout: item, type, why it matters, key metric, seen on, score, source.", "",
          "## Metrics", "",
          "- **Momentum (repos):** stars gained ÷ stars before the gain. **Velocity (HN):** points ÷ hours since posting.",
          "- **Exploited:** the CVE is in the CISA Known Exploited Vulnerabilities catalogue (the whole catalogue is checked).",
          "- **Downloads:** the period is always written next to the number (30 d for Hugging Face, week for npm and PyPI, 90 d for crates.io).",
          "- **Why it matters** is the item's own description, abstract or summary, cut to its first sentence. Where a source "
          "has no description (Hacker News), the cell names the linked site instead.", "",
          '<a id="industries"></a>', "", "## Industries", "",
          "An item can belong to several industries. It is placed by:", "",
          "1. **Source rule**: some sources always map to an industry (table below).",
          "2. **Topic rule**: GitHub topics or post tags that match the industry's topic list.",
          "3. **Keyword rule**: a case-insensitive whole-word match on the title, description, task, topics and tags.",
          "4. Anything with no match goes to **Other**. Keyword-free sources ("
          + ", ".join(f"`{k}`" for k in sorted(SOURCE_ONLY)) + ") use only the source rule, because vendor names or prices "
          "would trigger false matches.", "",
          "| Industry | Scope | GitHub topics | Keywords (regex) |", "| --- | --- | --- | --- |"]
    for slug, emo, title, short, intro, rx, topics in INDUSTRIES:
        p.append(f"| {title} | {md_escape(intro)} | {', '.join(f'`{t}`' for t in sorted(topics))} | <sub>`{md_escape(rx)}`</sub> |")
    p += ["", "### Source rules", "", "| Source key | Always in |", "| --- | --- |"]
    for k, v in SOURCE_INDUSTRIES.items():
        p.append(f"| `{k}` | {', '.join(IND[s][2] for s in v)} |")
    p.append(f"| `arxiv` | by category: {', '.join(f'{c} → {IND[s][2]}' for c, s in ARXIV_INDUSTRY.items())} |")
    for k, _n, _u, ind in INDUSTRY_FEEDS:
        if ind:
            p.append(f"| `{k}` | {IND[ind][2]} |")
    for k, *_r in AI_NEWS_FEEDS:
        p.append(f"| `{k}` | {IND['ai-llms'][2]} |")
    for k, _n, _u, _h, _l, ind in MARKET_FEEDS:
        if ind:
            p.append(f"| `{k}` | {IND[ind][2]} |")
    p.append("| " + ", ".join(f"`{k}`" for k, *_r in DEAL_QUERIES) + f" | {IND['markets-economy'][2]} |")
    p.append("| " + ", ".join(f"`{k}`" for k, *_r in MEDIA_QUERIES) + f", `elevenlabs_blog` | {IND['ai-media'][2]} |")
    p.append("| `lab_news_*`, lab blog feeds | " + IND['ai-llms'][2] + " |")
    for t, ind in GITHUB_TOPICS:
        p.append(f"| `gh_topic_{t}` | {IND[ind][2]} |")
    p += ["| `coingecko_trending`, `coingecko_markets` | Crypto & web3 |", "| `biorxiv` | Health & biotech |",
          "| `launches` | Space & mobility |", "",
          '<a id="shaking"></a>', "", "## What's shaking the market", "",
          f"Every headline, lab post and Hacker News front-page story from the last {STORY_HOURS} hours is a candidate. "
          "Each headline is cut into its distinctive words (common words, and words found in more than 6% of all "
          "candidate headlines, are ignored). A headline joins a story when it shares at least two distinctive words "
          f"with the story's longest headline and those shared words are at least {int(STORY_OVERLAP * 100)}% of the shorter "
          "headline's distinctive words. A second pass merges two stories whose recurring words overlap (three shared "
          "words, or two when one of them is rare), so the same event told by different outlets ends up as one row. "
          "Stories are ranked by the number of distinct outlets (Google News results "
          "count the original outlet, not Google), then distinct platforms, then recency. Only stories carried by two "
          "or more outlets are shown. \"Why it matters\" is the first sentence of a summary written by one of the "
          "outlets; Google News results carry no summary.", "",
          "**Google News links** open through a Google redirect to the original article. Resolving the redirect needs "
          "undocumented calls, so the link is kept as Google gives it and the publisher's own domain (from the feed's "
          "`<source url>`) is shown next to the outlet name.", "",
          "**Markets strip:** FRED (St. Louis Fed) latest published values for the S&P 500, Nasdaq Composite, Dow "
          "Jones, VIX, US 10-year yield and Brent; the ECB euro reference rate for EUR/USD; CoinGecko for Bitcoin and "
          "Ether. Changes compare the last two published values. " + MARKETS_NOT_SHOWN, "",
          '<a id="windows"></a>', "", "## Week, month and year", "",
          "| Window | Native lists |", "| --- | --- |"]
    for w, label, days in WINDOWS:
        p.append(f"| {label} ({days} days) | " + ", ".join(f"`{k}`" for k, v in WINDOW_OF.items() if v == w) + " |")
    p += ["", "Each window is scored with the same formula as today, using only that window's lists. Lists for "
          "a longer period are never used for today's tables. The **archive rollup** in each window file counts the days "
          f"an item appeared in the archive. The archive starts on {HISTORY_START}, so a month or year rollup only covers "
          "the days that exist; the file always states how many.", "",
          '<a id="labs"></a>', "", "## AI labs", "",
          "| Lab | Google News query | Official feeds | SDK repos | Status page | OpenRouter prefix | Hugging Face orgs |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for slug, name, q, feeds, repos, st, orp, hfo, _arena in LABS:
        p.append(f"| {name} | <sub>`{md_escape(q)}`</sub> | {', '.join(f'`{f}`' for f in feeds) or '—'} | "
                 f"{', '.join(repos) or '—'} | {f'`{st}`' if st else '—'} | {', '.join(orp) or '—'} | {', '.join(hfo) or '—'} |")
    p += ["", "Google News headlines are kept only when the title names the lab. Anthropic publishes no RSS feed, so its "
          "newsroom comes from the public sitemap (page address and last-change date); the title and summary are then read "
          "from each page's own `og:title` and description tags (robots.txt allows these pages). If a page cannot be "
          "read, the title falls back to the page address in words. Leaderboard positions come "
          "from the LMArena leaderboard dataset on Hugging Face (CC BY 4.0).", "",
          '<a id="since"></a>', "", "## Since yesterday", "",
          "Today's ranked items are compared with the newest earlier archive file. An item is **new** when its address "
          "is not in that day's tables; the table shows the five new items with the highest score. **Climbers** compare "
          "today's position on GitHub trending with the position archived the previous day, and only within the number "
          "of rows that day listed, so nothing is called new just because it was below the cut.", "",
          '<a id="feeds"></a>', "", "## Feeds", "",
          "`feeds/daily.json` is rewritten every morning with the day's stories, markets strip, top 30 signals, the "
          "top 15 of each window, lab counts and the since-yesterday summary, using the same values as the pages. "
          "`feeds/daily.xml` is an RSS 2.0 feed with the top 10 stories and top 15 signals; each item's id includes the "
          "date, so readers show each day as new items.", "",
          "## What is never done", "",
          "- No number is estimated, rounded up or filled in. A dash means the source gave none.",
          "- No source that needs a key, a login, or scraping against its terms.",
          "- The maintainer's own repos sit in their own labelled section and are never boosted.", ""]
    return "\n".join(p)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

NICHE_REDIRECTS = {
    "ai-llms": ["ai-llms"], "agents-mcp": ["ai-agents"], "devtools": ["devtools"], "web": ["web-frontend"],
    "mobile": ["mobile"], "devops-cloud": ["cloud-devops"], "security": ["cybersecurity"], "data": ["data-analytics"],
    "research": ["ai-llms", "health-biotech", "robotics-hardware"], "pulse": ["media-creator", "policy-regulation", "other"],
}


def render_niche_redirect(old: str) -> str:
    links = " · ".join(f"[{IND[s][2]}](../industries/{s}.md)" for s in NICHE_REDIRECTS[old])
    return (f"# Moved\n\nThe niche lists became industry files. This topic now lives in: {links}\n\n"
            "[All industries](../README.md#map)\n")


def run(root: Path, dry_run: bool = False, only: set[str] | None = None) -> int:
    t0 = time.monotonic()
    DEADLINE[0] = t0 + TOTAL_BUDGET
    fetched_at = now_berlin()
    results = run_sources(only)
    DEADLINE[0] = max(DEADLINE[0], time.monotonic() + 25)  # small reserve for the enrichment calls
    enrich_note = enrich_repos(results)
    mark_exploited(results)
    ents = build_entities(results, today_keys(results))
    history = archive_history(root, fetched_at)
    windows, window_pages = {}, {}
    for w, label, days in WINDOWS:
        wents = sorted(build_entities(results, [k for k, v in WINDOW_OF.items() if v == w]),
                       key=lambda e: (e.score, len(e.families), e.best_pct), reverse=True)
        info = rollup(history, ents, fetched_at, days)
        windows[w] = (wents, info[0])
        window_pages[f"windows/{w}.md"] = render_window_file(w, label, days, wents, results, info, fetched_at)
    since = since_yesterday(root, fetched_at, ents, results, history)
    x_sections, x_note = load_x_trends(root, fetched_at)
    tech_x = select_tech_on_x(x_sections) if x_sections else []

    for r in results.values():
        print(f"  [{'ok  ' if r.ok else 'SKIP'}] {r.key:20} {len(r.items):3} items {r.elapsed:5.1f}s  {r.note[:80]}")
    print(f"  [x   ] {x_note}; {len(tech_x)} tech rows")
    print(f"  [enr ] {enrich_note}")

    rel_archive = f"archive/{fetched_at:%Y/%m}/{fetched_at:%Y-%m-%d}.md"
    archive_links = list_archive_links(root, rel_archive)
    members = industry_members(ents)
    readme = render_page(results, ents, fetched_at, tech_x, x_sections, x_note, enrich_note, archive_links, "readme", windows, since)
    archive_body = render_page(results, ents, fetched_at, tech_x, x_sections, x_note, enrich_note, archive_links, "archive", windows, since)
    archive_path = root / rel_archive
    archive_md = merge_archive(archive_path, archive_body, fetched_at)
    pages = {f"industries/{s}.md": render_industry_file(s, members, results, fetched_at) for s in IND_ORDER}
    pages.update(window_pages)
    pages["labs/README.md"] = render_labs_file(results, fetched_at)
    feed = build_feed_json(results, ents, windows, fetched_at, since)
    pages["feeds/daily.json"] = json.dumps(feed, ensure_ascii=False, indent=1) + "\n"
    pages["feeds/daily.xml"] = build_feed_rss(feed, fetched_at)

    okn, total = count_ok(results)
    print(f"Sources answered: {okn}/{total}; {len(ents)} distinct items; {time.monotonic() - t0:.1f}s")
    for s in IND_ORDER:
        print(f"  {s:20} {len(members[s]):4} items")
    if dry_run:
        print(f"Dry run: README {len(readme):,} bytes, archive {len(archive_md):,} bytes")
        return 0
    if okn == 0:
        print("No source answered; leaving files untouched.")
        return 1
    readme, archive_md = _no_emoji(readme), _no_emoji(archive_md)
    pages = {k: _no_emoji(v) for k, v in pages.items()}
    (root / "README.md").write_text(readme, encoding="utf-8")
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_text(archive_md, encoding="utf-8")
    for rel, text in pages.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    print(f"Wrote README.md, {rel_archive} and {len(pages)} more files (industries, windows, labs, feeds)")
    for w, (wents, nd) in windows.items():
        print(f"  window {w:6} {len(wents):4} items, {nd} archived day(s)")
    print(f"  README {len(readme):,} bytes, archive {len(archive_md):,} bytes")
    return 0


def write_static_docs(root: Path) -> None:
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "methodology.md").write_text(render_methodology(), encoding="utf-8")
    (root / "niches").mkdir(exist_ok=True)
    for old in NICHE_REDIRECTS:
        (root / "niches" / f"{old}.md").write_text(render_niche_redirect(old), encoding="utf-8")
    print("Wrote docs/methodology.md and the niches/ redirects")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update the awesome-trending hub")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", default="", help="Comma-separated source keys")
    parser.add_argument("--docs", action="store_true", help="Rewrite docs/methodology.md and niches/ redirects, then exit")
    args = parser.parse_args(argv)
    root = (args.root or Path(__file__).resolve().parent.parent).resolve()
    if args.docs:
        write_static_docs(root)
        return 0
    only = {k.strip() for k in args.only.split(",") if k.strip()} or None
    return run(root, dry_run=args.dry_run, only=only)


if __name__ == "__main__":
    sys.exit(main())
