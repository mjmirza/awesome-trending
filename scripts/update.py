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
    "api.github.com": 3.0,      # search API: 10 calls a minute without a token
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
        if key.startswith("gh_") and key != "gh_new" and not key.startswith("gh_topic_") and res.ok:
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
        if key.startswith("gh_") and key != "gh_new" and not key.startswith("gh_topic_"):
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
    ("ai-llms", "🤖", "AI & LLMs", "AI",
     "Foundation models, inference, ML research and the labs behind them.",
     r"\b(ai|a\.i\.|artificial intelligence|llms?|gpt[-\w.]*|chatgpt|openai|anthropic|claude|gemini|llama|qwen|mistral|"
     r"deepseek|transformers?|diffusion|inference|fine-?tun\w*|machine learning|deep learning|neural|embeddings?|"
     r"rag|vllm|ollama|pytorch|tensorflow|multimodal|vision-language|language models?|reasoning model|"
     r"text-generation|text-to-\w+|image-text-to-text|hugging ?face|openvino|copilot)\b",
     {"machine-learning", "deep-learning", "llm", "llms", "artificial-intelligence", "ai", "nlp", "pytorch",
      "transformers", "large-language-models", "generative-ai", "computer-vision", "openai", "llama"}),
    ("ai-agents", "🧠", "AI agents & MCP", "Agents",
     "Agent frameworks, skills, tool use and Model Context Protocol servers.",
     r"\b(agents?|agentic|mcp|model context protocol|agent skills?|skills? (bundle|library|framework)|"
     r"claude code|codex|coding agents?|autonomous agents?|crewai|langgraph|autogen|tool[- ]calling|a2a|"
     r"computer[- ]use|browser[- ]use|sandbox(es|ed)?)\b",
     {"ai-agents", "agents", "mcp", "mcp-server", "model-context-protocol", "agent-skills", "claude-code",
      "agentic-ai", "ai-agent", "llm-agents", "autonomous-agents"}),
    ("devtools", "🧰", "Developer tools", "Dev tools",
     "Languages, editors, CLIs, package ecosystems and the software toolchain.",
     r"\b(cli|ide|editor|vs ?code|vim|neovim|emacs|plugins?|sdk|compiler|debugg\w*|linters?|terminal|git|"
     r"package manager|npm|pypi|crates?\.io|cargo|rustc?|golang|python|typescript|javascript|zig|ruff|deno|"
     r"bun|node\.?js|refactor\w*|developers?|devtools?|programming|open[- ]source)\b",
     {"cli", "developer-tools", "devtools", "rust", "golang", "python", "typescript", "compiler", "neovim",
      "vscode", "terminal", "git", "programming-language"}),
    ("cloud-devops", "☁️", "Cloud & DevOps", "Cloud",
     "Infrastructure, containers, CI/CD, self-hosting, outages and operations.",
     r"\b(devops|kubernetes|k8s|docker|containers?|helm|terraform|ansible|ci/?cd|aws|azure|gcp|google cloud|"
     r"cloud|serverless|nginx|linux|kernel|self-host\w*|homelab|observability|grafana|prometheus|sre|outages?|"
     r"incident|hetzner|cloudflare|data ?cent(er|re)s?|infrastructure)\b",
     {"kubernetes", "docker", "devops", "terraform", "self-hosted", "cloud", "aws", "observability",
      "infrastructure", "homelab", "linux"}),
    ("cybersecurity", "🔒", "Cybersecurity", "Security",
     "Exploited and new vulnerabilities, attacks, defence and security tooling.",
     r"\b(security|vulnerab\w*|cve-\d+|exploit\w*|malware|ransomware|phishing|breach\w*|pentest\w*|red[- ]team|"
     r"bug[- ]?bount\w*|bug hunt\w*|zero-day|0-day|backdoor|cryptography|authentication bypass|xss|rce|"
     r"privilege escalation|supply[- ]chain attack|cyber\w*|infosec|hackers?|spyware|botnet|ddos)\b",
     {"security", "cybersecurity", "pentesting", "penetration-testing", "red-team", "bug-bounty", "malware",
      "vulnerability", "infosec", "ai-security", "osint", "ctf"}),
    ("data-analytics", "📊", "Data & analytics", "Data",
     "Databases, datasets, pipelines, analytics and BI.",
     r"\b(databases?|postgres\w*|sqlite|mysql|duckdb|clickhouse|polars|pandas|spark|kafka|airflow|parquet|"
     r"iceberg|etl|data pipelines?|datasets?|data engineering|vector (db|database)|analytics|olap|warehouse)\b",
     {"database", "data-engineering", "analytics", "postgresql", "sql", "etl", "data-science", "dataset",
      "vector-database", "big-data"}),
    ("web-frontend", "🌐", "Web & frontend", "Web",
     "Browsers, front-end frameworks, CSS, web platform and the CDN layer.",
     r"\b(frontend|front-end|web apps?|web development|web framework|web platform|web standards?|browsers?|css|"
     r"html|react|next\.js|nextjs|vue|svelte|angular|tailwind|webassembly|wasm|chrome|firefox|safari|webgpu)\b",
     {"react", "nextjs", "vue", "svelte", "css", "frontend", "web", "tailwindcss", "webassembly", "javascript"}),
    ("mobile", "📱", "Mobile", "Mobile",
     "iOS, Android, phones, wearables and app stores.",
     r"\b(ios|ipados|android|iphone|ipad|app store|google play|mobile|react native|flutter|swiftui|swift|kotlin|"
     r"jetpack|xcode|testflight|smartphones?|samsung galaxy|pixel \d+|whatsapp|apple watch|wearables?)\b",
     {"ios", "android", "flutter", "react-native", "swift", "kotlin", "mobile", "swiftui"}),
    ("fintech", "💳", "Fintech & payments", "Fintech",
     "Banking, payments, lending, trading, insurance and finance infrastructure.",
     r"\b(fintech|payments?|banks?|banking|neobank|stripe|paypal|visa|mastercard|klarna|adyen|lending|loans?|"
     r"credit cards?|trading|brokerage|insurtech|insurance|remittances?|open banking|financial)\b",
     {"fintech", "payments", "banking", "trading", "finance", "quantitative-finance", "algorithmic-trading"}),
    ("crypto-web3", "🪙", "Crypto & web3", "Crypto",
     "Cryptocurrencies, blockchains, DeFi, stablecoins and tokenisation.",
     r"\b(crypto\w*|bitcoin|btc|ethereum|eth|solana|blockchains?|web3|defi|stablecoins?|tokens? (sale|launch)|"
     r"nfts?|coinbase|binance|monero|xrp|tokeni[sz]\w*)\b",
     {"blockchain", "cryptocurrency", "ethereum", "bitcoin", "solana", "web3", "defi", "smart-contracts", "crypto"}),
    ("health-biotech", "🧬", "Health & biotech", "Health",
     "Medicine, biology, pharma, health systems and medtech.",
     r"\b(health\w*|medic\w*|clinical|patients?|hospitals?|biotech\w*|pharma\w*|drugs?|fda|genom\w*|proteins?|"
     r"bioinformatics|biology|cancer|vaccines?|medicare|medicaid|disease|neuro\w*|medrxiv|biorxiv)\b",
     {"bioinformatics", "healthcare", "medical", "biology", "genomics", "health", "medical-imaging"}),
    ("robotics-hardware", "🦾", "Robotics & hardware", "Robotics",
     "Robots, drones, embedded devices and consumer hardware.",
     r"\b(robot\w*|humanoids?|drones?|embedded|firmware|arduino|raspberry pi|esp32|microcontrollers?|"
     r"hardware|3d print\w*|lidar|actuators?|exoskeleton\w*)\b",
     {"robotics", "ros", "ros2", "embedded", "hardware", "arduino", "esp32", "drones", "3d-printing", "iot"}),
    ("semiconductors", "🔌", "Semiconductors & chips", "Chips",
     "Chip design, fabs, GPUs, accelerators and the supply chain.",
     r"\b(semiconductors?|chips?|chipmakers?|gpus?|tpus?|npus?|asics?|fpgas?|nvidia|nvda|amd|intel|tsmc|"
     r"qualcomm|risc-v|wafers?|fabs?|foundry|lithography|asml|hbm|cuda|silicon)\b",
     {"fpga", "risc-v", "verilog", "cuda", "gpu", "semiconductor", "vlsi", "chip-design"}),
    ("climate-energy", "⚡", "Climate & energy", "Energy",
     "Clean energy, grids, EVs, batteries, oil and gas, and climate.",
     r"\b(climate|energy|solar|wind (power|farms?|turbines?)|battery storage|energy storage|power grids?|evs?|electric vehicles?|"
     r"ev charging|hydrogen|nuclear|carbon|emissions|oil|natural gas|lng|renewables?|heat pumps?|power plants?|utilities)\b",
     {"climate", "energy", "solar", "climate-change", "electric-vehicles", "renewable-energy", "sustainability"}),
    ("ecommerce-retail", "🛒", "E-commerce & retail", "Retail",
     "Online and physical retail, marketplaces, logistics and shopping.",
     r"\b(e-?commerce|retail\w*|shopping|shoppers?|black friday|cyber monday|amazon|shopify|walmart|"
     r"marketplaces?|checkout|merchants?|logistics|grocer\w*|consumer brands?)\b",
     {"ecommerce", "e-commerce", "shopify", "retail", "marketplace"}),
    ("gaming-xr", "🎮", "Gaming & XR", "Gaming",
     "Games, studios, engines, consoles and VR/AR.",
     r"\b(video ?games?|gaming|gamers?|game (studio|engine|developers?)|playstation|ps5|xbox|nintendo|switch 2|steam|"
     r"epic games|unreal engine|unity|godot|esports|gta ?(6|vi)|grand theft auto|rockstar|ubisoft|"
     r"vr|xr|virtual reality|mixed reality|vr headsets?|vision pro|meta quest)\b",
     {"game", "gamedev", "game-development", "godot", "unity", "unreal-engine", "vr", "xr", "game-engine"}),
    ("enterprise-saas", "🏢", "Enterprise SaaS & productivity", "SaaS",
     "Business software, productivity, collaboration and the enterprise market.",
     r"\b(saas|enterprise software|enterprise ai|crm|erp|salesforce|workday|servicenow|sap|productivity apps?|"
     r"notion|slack|microsoft 365|no-?code|low-?code|b2b|knowledge base|workflow automation)\b",
     {"saas", "productivity", "crm", "erp", "workflow", "automation", "no-code", "low-code", "notion"}),
    ("education", "🎓", "Education", "Education",
     "Schools, universities, edtech, courses and learning resources.",
     r"\b(education\w*|edtech|schools?|students?|teachers?|universit(y|ies)|courses?|learning resources|"
     r"tutorials?|mooc|curriculum|classrooms?|lessons?)\b",
     {"education", "learning", "tutorial", "course", "edtech", "roadmap", "interview"}),
    ("media-creator", "🎬", "Media & creator economy", "Media",
     "News media, video, streaming, music, social platforms and creators.",
     r"\b(media|newsrooms?|newspapers?|journalis\w*|youtube|tiktok|instagram|creators?|influencers?|podcasts?|"
     r"streaming|netflix|spotify|music|films?|movies?|tv|publishers?|social media|bluesky)\b",
     {"video", "youtube", "streaming", "music", "media", "social-media", "podcast"}),
    ("space-mobility", "🚀", "Space & mobility", "Space",
     "Launches, satellites, aviation, autonomous vehicles and transport.",
     r"\b(space ?x|spacex|spaceflight|starship|starlink|rockets?|satellites?|orbit(al)?|nasa|esa|moon|lunar|mars|"
     r"astronauts?|aviation|aircraft|airlines?|faa|autonomous (vehicles?|driving)|robotaxis?|waymo|"
     r"self-driving|uber|lyft|transportation|mobility)\b",
     {"space", "aerospace", "satellite", "autonomous-driving", "self-driving-car", "astronomy"}),
    ("policy-regulation", "⚖️", "Policy & regulation", "Policy",
     "Laws, regulators, courts, antitrust, privacy and digital policy.",
     r"\b(regulat\w*|laws?|legislat\w*|courts?|lawsuits?|sues?|judges?|antitrust|competition authority|"
     r"ftc|fcc|doj|european commission|commissioner|eu ai act|dma|dsa|gdpr|privacy|public policy|tech policy|government|"
     r"ministers?|congress|senate|parliament|tariffs?|sanctions|export controls?)\b",
     {"privacy", "gdpr", "regulation", "policy", "legal", "compliance"}),
]
OTHER = ("other", "📦", "Other", "Other", "Items that no rule matched. They still count; nothing is dropped.", r"$^", set())
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
    "thn": ["cybersecurity"], "bleeping": ["cybersecurity"],
}
# Sources where only the source rule applies (keyword rules would misfire on vendor names or prices).
SOURCE_ONLY = {"kev", "nvd", "euvd", "coingecko_trending", "coingecko_markets", "launches",
               "githubstatus", "cloudflarestatus", "jsdelivr"}
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
          "bluesky"} | {f"gh_{s}" for s, _ in GITHUB_LANGUAGES} | {f"gh_topic_{t}" for t, _ in GITHUB_TOPICS}
PULSE_FAMILIES = {"Google Trends", "Wikipedia", "Mastodon", "Bluesky"}
UNRANKED_BASE = 0.25
W_RANK, W_SPREAD, SPREAD_CAP = 0.6, 0.4, 3


def family(key: str, results) -> str:
    for prefix, name in (("gh_", "GitHub"), ("hn_", "Hacker News"), ("hf_", "Hugging Face"), ("devto", "Dev.to"),
                         ("mastodon", "Mastodon"), ("coingecko", "CoinGecko")):
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


def build_entities(results) -> list["Entity"]:
    order = [k for k, *_ in SOURCES if k in results and results[k].ok and k != "maintainer"]
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
    if k == "repo":
        s = f"⭐ {fmt_compact(it.get('stars'))}"
        if it.get("gained") is not None:
            s += f" · +{fmt_int(it['gained'])} {'this week' if key == 'gh_weekly' else 'today'}"
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
    out = ", ".join(f"{IND[s][1]} {IND[s][3]}" for s in inds[:n])
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
TYPE_EMOJI = {"repo": "🐙", "hn": "💬", "post": "✍️", "question": "❓", "product": "🛍️", "model": "🤗", "space": "🧪",
              "dataset": "🗃️", "llm": "🧩", "paper": "📄", "mcp": "🔌", "package": "📦", "cdn": "📶", "image": "🐳",
              "release": "🏷️", "vuln": "🛡️", "news": "🗞️", "incident": "🚨", "coin": "🪙", "launch": "🛰️",
              "search": "🔎", "wiki": "📖", "tag": "#️⃣", "topic": "🦋"}
TYPE_DESIGN_NOTE = {
    "repo": "stars, stars gained, momentum % (gained ÷ stars before), language, licence and age",
    "hn": "points, comments, velocity (points per hour) and the thread link",
    "post": "tags, reactions or score, comments and author",
    "question": "tags, score, answers (✓ = accepted), views",
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
                               fmt_int(i.get("answers")) + (" ✓" if i.get("answered") else ""), fmt_compact(i.get("views"))]),
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
                            (md_link("repo", i["github"]) + (f" ⭐ {fmt_int(i['github_stars'])}" if i.get("github_stars") else ""))
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
             lambda k, i: [ttl(i), md_escape(why(k, i)), md_escape(i.get("outlet")), fmt_day(i.get("published"))]),
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
    return [ttl(it, 70), f"{TYPE_EMOJI.get(t, '')} {TYPE_LABEL.get(t, t)}", md_escape(why(k, it)), key_metric(k, it),
            seen_cell(it), str(e.score), src_cell(k, results)]


# ---------------------------------------------------------------------------
# Page blocks
# ---------------------------------------------------------------------------

GROUPS = [
    ("src-github", "🐙 GitHub", ["gh_daily", "gh_new", "gh_weekly"] + [f"gh_{s}" for s, _ in GITHUB_LANGUAGES]
     + [f"gh_topic_{t}" for t, _ in GITHUB_TOPICS]),
    ("src-hn", "💬 Hacker News", ["hn_front", "hn_show", "hn_best", "hn_ask"]),
    ("src-ai", "🤗 Models & labs", ["hf_models", "openrouter", "hf_spaces", "hf_datasets", "openai_news", "google_ai",
                                   "deepmind", "hf_blog"]),
    ("src-research", "📄 Papers & preprints", ["hf_papers", "arxiv", "biorxiv"]),
    ("src-mcp", "🔌 MCP registries", ["mcp_registry", "smithery"]),
    ("src-packages", "📦 Packages & releases", ["releases", "npm", "pypi", "crates", "jsdelivr", "dockerhub"]),
    ("src-security", "🛡️ Vulnerabilities", ["kev", "nvd", "euvd"]),
    ("src-markets", "🪙 Markets & launches", ["coingecko_trending", "coingecko_markets", "launches"]),
    ("src-community", "✍️ Community", ["lobsters", "devto_day", "devto_week", "stackoverflow", "producthunt"]),
    ("src-news", "🗞️ Tech news", [k for k, *_ in NEWS_FEEDS]),
    ("src-industry-news", "🏭 Industry outlets", [k for k, *_ in INDUSTRY_FEEDS]),
    ("src-pulse", "🌍 Public pulse", ["gtrends", "wikipedia", "mastodon_links", "mastodon_tags", "bluesky"]),
]
STATUS_KEYS = ["githubstatus", "cloudflarestatus"]


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
    gh = [i for i in ok("gh_daily") if i.get("gained") is not None]
    if gh:
        top = max(gh, key=lambda i: i["gained"])
        b.append(f"🐙 **Most stars today:** {ttl(top, 50)} — {md_escape(why('gh_daily', top))} "
                 f"(+{fmt_int(top['gained'])} today, {momentum('gh_daily', top)}).")
    multi = [e for e in ents if len(e.families) >= 2 and not set(e.families) <= PULSE_FAMILIES]
    if multi:
        e = max(multi, key=lambda x: (len(x.families), x.score))
        b.append(f"🔁 **On the most sources:** {ttl(e.item, 60)} — {len(e.families)} sources ({md_escape(', '.join(e.families))}).")
    hn = ok("hn_front")
    if hn:
        b.append(f"💬 **Top on Hacker News:** {ttl(hn[0], 70)} — {key_metric('hn_front', hn[0])}.")
    pp = ok("hf_papers")
    if pp:
        b.append(f"📄 **Most upvoted paper:** {ttl(pp[0], 70)} — {fmt_int(pp[0].get('upvotes'))} upvotes.")
    lm = ok("openrouter")
    if lm:
        b.append(f"🧩 **Newest hosted model:** {ttl(lm[0], 50)} — {key_metric('openrouter', lm[0])}.")
    kev = ok("kev")
    if kev:
        recent = [k for k in kev if k["added"] == kev[0]["added"]]
        names = ", ".join(md_escape(re.sub(r"\s*\([^)]*\)", "", k["product"])) for k in recent[:4])
        b.append(f"🛡️ **Exploited in the wild:** CISA added {len(recent)} on {kev[0]['added']} ({names}); {len(kev)} in 14 days.")
    coins = ok("coingecko_markets")
    if coins:
        c = coins[0]
        b.append(f"🪙 **Crypto:** {ttl(c, 30)} at ${_price(c.get('price'))} ({_pct(c.get('change_24h'))} in 24 h, "
                 f"{_pct(c.get('change_7d'))} in 7 d).")
    la = ok("launches")
    if la:
        b.append(f"🛰️ **Next launch:** {ttl(la[0], 60)} — {key_metric('launches', la[0])}.")
    if tech_x:
        t = tech_x[0]
        posts = f"{t['posts']} posts" if t.get("posts") and t["posts"] != "—" else "volume not shown"
        b.append(f"🐦 **Tech on X:** {md_link(t['name'], t['url'])} ({posts}, {md_escape(t['region'])} list).")
    return [f"- {x}" for x in b[:10]]


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
        rows.append([ttl(it, 60), f"{TYPE_EMOJI.get(t, '')} {TYPE_LABEL.get(t, t)}", md_escape(why(k, it)),
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
            rows.append([f"{emo} {title}", "0", "_Nothing today_", "—", "—", link])
            continue
        e = ms[0]
        fams = len({f for m in ms for f in m.families})
        rows.append([f"{emo} [{title}](#ind-{slug})", f"**{len(ms)}** <sub>{fams} sources</sub>", ttl(e.item, 55),
                     strongest_signal(e), str(e.score), link])
    return [table(["Industry", "Items", "Top item", "Strongest signal", "Score", "File"], rows, numbered=False), ""]


def render_industry_section(slug: str, members, results, visible: int, cap: int, prefix: str) -> list[str]:
    _s, emo, title, short, intro, *_ = IND[slug]
    ms = members[slug]
    p = [f'<a id="ind-{slug}"></a>', "", f"### {emo} {title}", "",
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
        rows.append([str(n), md_link(name, url), "✅ OK" if r.ok else "⏭️ Skipped", str(len(r.items)) if r.ok else "0",
                     "ranked" if key in RANKED else "unranked", fmt_hm(r.fetched_at), md_escape(clip(r.note, 120))])
    rows.append(["—", "X trends", "✅ OK" if "reused" in x_note else "⏭️ Skipped", "—", "—", "—", md_escape(x_note)])
    rows.append(["—", "Licence, topics and age for trending repos", "✅ OK" if "added for" in enrich_note else "⏭️ Skipped",
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


def render_page(results, ents, fetched_at, tech_x, x_sections, x_note, enrich_note, archive_links, mode: str) -> str:
    readme = mode == "readme"
    prefix = "" if readme else "../../../"
    okn, total = count_ok(results)
    members = industry_members(ents)
    live = sum(1 for s in IND_ORDER if members[s] and s != "other")
    p = []
    if readme:
        p += ["# awesome-trending", "",
              f"A daily market scan of technology: {len(INDUSTRIES)} industries, {total} public sources, one page. "
              "Every number links to where it came from.", "",
              f"[![Last commit](https://img.shields.io/github/last-commit/{REPO_OWNER}/{REPO_NAME})]({REPO_URL}/commits/main) "
              f"[![License](https://img.shields.io/badge/License-OpenRoots_ORA_2.3-2ea44f)](LICENSE) "
              f"[![Sources](https://img.shields.io/badge/sources_live_today-{okn}%2F{total}-informational)](#sources) "
              f"[![Industries](https://img.shields.io/badge/industries_with_items-{live}%2F{len(INDUSTRIES)}-blueviolet)](#map)", ""]
    else:
        p += [f"# awesome-trending — {fmt_date(fetched_at)}", ""]
    p += [f"**{fmt_date(fetched_at)}** · snapshot at {fmt_time(fetched_at)} · {okn}/{total} sources answered · "
          f"{len(ents)} distinct items", "",
          "**Read it in this order:** ⚡ 30 seconds → 🏆 top signals → 🗺️ industry map → your industry. Everything else is folded.", ""]
    nav = ["[⚡ 30 seconds](#today)", "[🏆 Top signals](#signals)", "[🗺️ Industry map](#map)", "[🏭 Industries](#industries)",
           "[📡 By source](#by-source)", "[🚨 Status](#status)", "[🐦 X](#x)", "[👤 Maintainer](#maintainer)"]
    nav += (["[📚 Archive](#archive)"] if readme else []) + ["[✅ Sources](#sources)"]
    p += [" · ".join(nav), "", '<a id="today"></a>', "", "## ⚡ Today in 30 seconds", ""]
    p += render_today(results, ents, tech_x) + [""]
    p += ['<a id="signals"></a>', "", "## 🏆 Top signals today", "",
          "One score for everything: how high an item ranks in its own source, plus how many separate sources list it.", ""]
    p += render_top_signals(ents, results, 15 if readme else 30, 10 if readme else 15, prefix)
    p += ['<a id="map"></a>', "", "## 🗺️ Industry map", "",
          "One row per industry. **Top item** is its highest-scoring item today. An item can sit in more than one industry.", ""]
    p += render_matrix(members, prefix)
    p += ['<a id="industries"></a>', "", "## 🏭 Industries", "",
          f"Top {'5' if readme else '10'} per industry, highest score first. The same columns in every industry.", ""]
    for slug in IND_ORDER:
        p += render_industry_section(slug, members, results, 5 if readme else 10, 10, prefix)
        p += ["<sub>[↑ Industry map](#map)</sub>", ""]
    p += ['<a id="by-source"></a>', "", "## 📡 By source", "",
          "The raw lists, grouped by kind of source. Each item type has its own columns. Click a group to open it.", ""]
    for anchor, heading, keys in GROUPS:
        present = [k for k in keys if k in results]
        if not present:
            continue
        n_items = sum(len(results[k].items) for k in present if results[k].ok)
        n_ok = sum(1 for k in present if results[k].ok)
        p += [f'<a id="{anchor}"></a>', "", "<details>",
              f"<summary><b>{heading}</b> · {n_items} items from {n_ok}/{len(present)} sources</summary>", ""]
        for k in present:
            p += source_block(k, results, 3 if readme else 10, 3 if readme else 25)
        p += ["</details>", ""]
    p += ['<a id="status"></a>', "", "## 🚨 Platform status", "", "Incidents in the last 72 hours on platforms most teams depend on.", ""]
    for k in STATUS_KEYS:
        p += source_block(k, results, 5, 10, "###")
    p += ['<a id="x"></a>', "", "## 🐦 Tech on X", ""] + render_x(tech_x, x_sections, full=not readme)
    p += ['<a id="maintainer"></a>', "", "## 👤 From the maintainer", ""] + render_maintainer(results)
    if readme:
        p += ['<a id="archive"></a>', "", "## 📚 Archive", "", "<details>", "<summary>Every past day</summary>", ""]
        p += [f"- [{label}]({rel})" for label, rel in archive_links] + ["", "</details>", ""]
        p += ["## 🤝 Contribute", "",
              f"- Submit a repo with the [issue form]({SUBMIT_URL}). Tables are rebuilt from the sources every morning.",
              "- How items are scored and sorted into industries: [docs/methodology.md](docs/methodology.md).",
              "- Full source list and how to run it: [CONTRIBUTING.md](CONTRIBUTING.md) · [badge](docs/badge.md).",
              LICENSE_LINE, ""]
    p += ['<a id="sources"></a>', "", "## ✅ Sources", "",
          f"Fetched {fmt_date(fetched_at)} at {fmt_time(fetched_at)}. Every figure comes from the source in its row. "
          "A dash means the source gave no number. Nothing is estimated or invented.", ""]
    p += render_sources_table(results, x_note, enrich_note) + [""]
    return "\n".join(p).rstrip() + "\n"


def _anchor(heading: str) -> str:
    return re.sub(r"[^\w\- ]", "", heading.lower()).strip().replace(" ", "-")


def render_industry_file(slug: str, members, results, fetched_at: datetime) -> str:
    _s, emo, title, short, intro, rx, topics = IND[slug]
    ms = members[slug]
    p = [f"# {emo} {title}", "", intro, "",
         f"**{fmt_date(fetched_at)}** · {fmt_time(fetched_at)} · {len(ms)} items · daily snapshot, rebuilt every morning.", "",
         f"[⬅ Main page](../README.md) · [Industry map](../README.md#map) · [How items get here](../docs/methodology.md#industries) · "
         f"[Submit a repo]({SUBMIT_URL})", ""]
    if not ms:
        return "\n".join(p + ["_Nothing today. No source returned an item that matches this industry's rules._", ""])
    fams = sorted({f for m in ms for f in m.families})
    by_type: dict[str, list] = {}
    for e in ms:
        by_type.setdefault(ttype(e.item), []).append((e.key, e.item))
    order = sorted(by_type, key=lambda t: -len(by_type[t]))
    p += [f"**Sources with items here ({len(fams)}):** {md_escape(', '.join(fams))}", "",
          "**By type:** " + " · ".join(f"{TYPE_EMOJI.get(t, '')} [{TYPE_LABEL.get(t, t)}](#{_anchor(TYPE_LABEL.get(t, t))}) "
                                       f"({len(by_type[t])})" for t in order), "",
          "## 🏆 Top 10", ""]
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
        p.append(f"| {TYPE_EMOJI.get(t, '')} {TYPE_LABEL.get(t, t)} | {md_escape(note)} |")
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
        p.append(f"| {emo} {title} | {md_escape(intro)} | {', '.join(f'`{t}`' for t in sorted(topics))} | <sub>`{md_escape(rx)}`</sub> |")
    p += ["", "### Source rules", "", "| Source key | Always in |", "| --- | --- |"]
    for k, v in SOURCE_INDUSTRIES.items():
        p.append(f"| `{k}` | {', '.join(IND[s][2] for s in v)} |")
    p.append(f"| `arxiv` | by category: {', '.join(f'{c} → {IND[s][2]}' for c, s in ARXIV_INDUSTRY.items())} |")
    for k, _n, _u, ind in INDUSTRY_FEEDS:
        if ind:
            p.append(f"| `{k}` | {IND[ind][2]} |")
    for t, ind in GITHUB_TOPICS:
        p.append(f"| `gh_topic_{t}` | {IND[ind][2]} |")
    p += ["| `coingecko_trending`, `coingecko_markets` | Crypto & web3 |", "| `biorxiv` | Health & biotech |",
          "| `launches` | Space & mobility |", "",
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
    links = " · ".join(f"[{IND[s][1]} {IND[s][2]}](../industries/{s}.md)" for s in NICHE_REDIRECTS[old])
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
    ents = build_entities(results)
    x_sections, x_note = load_x_trends(root, fetched_at)
    tech_x = select_tech_on_x(x_sections) if x_sections else []

    for r in results.values():
        print(f"  [{'ok  ' if r.ok else 'SKIP'}] {r.key:20} {len(r.items):3} items {r.elapsed:5.1f}s  {r.note[:80]}")
    print(f"  [x   ] {x_note}; {len(tech_x)} tech rows")
    print(f"  [enr ] {enrich_note}")

    rel_archive = f"archive/{fetched_at:%Y/%m}/{fetched_at:%Y-%m-%d}.md"
    archive_links = list_archive_links(root, rel_archive)
    members = industry_members(ents)
    readme = render_page(results, ents, fetched_at, tech_x, x_sections, x_note, enrich_note, archive_links, "readme")
    archive_body = render_page(results, ents, fetched_at, tech_x, x_sections, x_note, enrich_note, archive_links, "archive")
    archive_path = root / rel_archive
    archive_md = merge_archive(archive_path, archive_body, fetched_at)
    pages = {f"industries/{s}.md": render_industry_file(s, members, results, fetched_at) for s in IND_ORDER}

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
    (root / "README.md").write_text(readme, encoding="utf-8")
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_text(archive_md, encoding="utf-8")
    for rel, text in pages.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    print(f"Wrote README.md, {rel_archive} and {len(pages)} industry files")
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
