# Contributing

This repository is a daily directory, not a dump of everything on the internet. Every morning `scripts/update.py` reads the public sources below, then rewrites `README.md`, today's file in `archive/`, and the files in `niches/`.

## How to help

- **Submit a repo** with the [issue form](https://github.com/mjmirza/awesome-trending/issues/new?template=submit-repo.yml). Give the URL, pick a niche, and write one line on why it belongs.
- Only public repositories, papers, or posts. No private links.
- Do not open a pull request just to add your repo to a table. The tables are rebuilt from the sources every day.
- **Suggest a source** by opening an issue. A source is only added if it is public, needs no API key or login, allows this kind of use in its terms, and answers reliably.
- The [Featured in awesome-trending](docs/badge.md) badge is only for repos that actually appeared here.

## Rules every page follows

- Numbers come from the source named in the row. A dash means the source gave no number. Nothing is estimated or invented.
- Each section says where it came from and when it was fetched. The bottom of every daily page has a sources table marked OK or Skipped.
- An item listed by more than one source appears once, with an "also:" note naming the other sources.
- The layout stays the same every day: a 30-second summary, a jump table, short tables, and long lists folded inside `<details>`.
- The README shows the top rows. The daily archive file has every row. The niche files group the same items by topic.

## Sources (54)

All of them are free, public and keyless. If one fails, it is marked Skipped for that day and the rest still publish.

| # | Section | Source | Key |
| --- | --- | --- | --- |
| 1 | 🐙 GitHub | [GitHub trending · today](https://github.com/trending?since=daily) | `gh_daily` |
| 2 | 🐙 GitHub | [GitHub trending · this week](https://github.com/trending?since=weekly) | `gh_weekly` |
| 3 | 🐙 GitHub | [GitHub trending · Python](https://github.com/trending/python?since=daily) | `gh_python` |
| 4 | 🐙 GitHub | [GitHub trending · TypeScript](https://github.com/trending/typescript?since=daily) | `gh_typescript` |
| 5 | 🐙 GitHub | [GitHub trending · Rust](https://github.com/trending/rust?since=daily) | `gh_rust` |
| 6 | 🐙 GitHub | [GitHub trending · Go](https://github.com/trending/go?since=daily) | `gh_go` |
| 7 | 🐙 GitHub | [GitHub · new repos gaining stars (created in the last 7 days)](https://docs.github.com/en/rest/search/search#search-repositories) | `gh_new` |
| 8 | 👤 From the maintainer | [Maintainer repos (not a ranking)](https://github.com/mjmirza) | `maintainer` |
| 9 | 🔥 Hacker News | [Hacker News · front page](https://news.ycombinator.com/) | `hn_front` |
| 10 | 🔥 Hacker News | [Hacker News · Show HN (last 24 h)](https://news.ycombinator.com/show) | `hn_show` |
| 11 | 🔥 Hacker News | [Hacker News · Ask HN (last 24 h)](https://news.ycombinator.com/ask) | `hn_ask` |
| 12 | 🔥 Hacker News | [Hacker News · best of the week](https://news.ycombinator.com/best) | `hn_best` |
| 13 | 🤖 AI models & labs | [Hugging Face · trending models](https://huggingface.co/models?sort=trending) | `hf_models` |
| 14 | 🤖 AI models & labs | [Hugging Face · trending Spaces](https://huggingface.co/spaces?sort=trending) | `hf_spaces` |
| 15 | 🤖 AI models & labs | [Hugging Face · trending datasets](https://huggingface.co/datasets?sort=trending) | `hf_datasets` |
| 16 | 📄 Research | [Hugging Face · daily papers](https://huggingface.co/papers) | `hf_papers` |
| 17 | 📄 Research | [arXiv · newest by category](https://arxiv.org/) | `arxiv` |
| 18 | 🧠 Agents & MCP | [MCP Registry · new and updated servers (24 h)](https://registry.modelcontextprotocol.io/) | `mcp_registry` |
| 19 | 🧠 Agents & MCP | [Smithery · most-used MCP servers](https://smithery.ai/) | `smithery` |
| 20 | 🤖 AI models & labs | [OpenRouter · newest models](https://openrouter.ai/models) | `openrouter` |
| 21 | 🤖 AI models & labs | [OpenAI News](https://openai.com/news/rss.xml) | `openai_news` |
| 22 | 🤖 AI models & labs | [Google AI blog](https://blog.google/technology/ai/rss/) | `google_ai` |
| 23 | 🤖 AI models & labs | [Google DeepMind blog](https://deepmind.google/blog/rss.xml) | `deepmind` |
| 24 | 🤖 AI models & labs | [Hugging Face blog](https://huggingface.co/blog/feed.xml) | `hf_blog` |
| 25 | 📦 Packages & releases | [npm · top packages for MCP, AI agents and LLMs](https://www.npmjs.com/) | `npm` |
| 26 | 📦 Packages & releases | [PyPI · latest releases of key AI and Python packages](https://pypi.org/) | `pypi` |
| 27 | 📦 Packages & releases | [crates.io · most downloaded recently](https://crates.io/) | `crates` |
| 28 | 📦 Packages & releases | [jsDelivr · top npm packages by CDN hits this week](https://www.jsdelivr.com/statistics) | `jsdelivr` |
| 29 | 📦 Packages & releases | [Docker Hub · official images updated in the last 48 h](https://hub.docker.com/search?badges=official) | `dockerhub` |
| 30 | 📦 Packages & releases | [GitHub releases · major projects (last 72 h)](https://github.com/) | `releases` |
| 31 | 🔒 Security | [CISA KEV · known exploited vulnerabilities (last 14 days)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | `kev` |
| 32 | 🔒 Security | [NVD · critical CVEs published in the last 48 h](https://nvd.nist.gov/vuln/search) | `nvd` |
| 33 | 🔒 Security | [ENISA EUVD · latest vulnerabilities](https://euvd.enisa.europa.eu/) | `euvd` |
| 34 | ☁️ Platform status | [GitHub status · incidents (last 72 h)](https://www.githubstatus.com) | `githubstatus` |
| 35 | ☁️ Platform status | [Cloudflare status · incidents (last 72 h)](https://www.cloudflarestatus.com) | `cloudflarestatus` |
| 36 | ✍️ Community | [Dev.to · top today](https://dev.to/top/day) | `devto_day` |
| 37 | ✍️ Community | [Dev.to · top this week](https://dev.to/top/week) | `devto_week` |
| 38 | ✍️ Community | [Lobsters · hottest](https://lobste.rs/) | `lobsters` |
| 39 | ✍️ Community | [Stack Overflow · hot questions](https://stackoverflow.com/questions?tab=Hot) | `stackoverflow` |
| 40 | ✍️ Community | [Product Hunt · newest featured](https://www.producthunt.com/) | `producthunt` |
| 41 | 🗞️ Tech news | [Techmeme](https://www.techmeme.com/feed.xml) | `techmeme` |
| 42 | 🗞️ Tech news | [The Verge](https://www.theverge.com/rss/index.xml) | `verge` |
| 43 | 🗞️ Tech news | [TechCrunch](https://techcrunch.com/feed/) | `techcrunch` |
| 44 | 🗞️ Tech news | [Ars Technica](https://feeds.arstechnica.com/arstechnica/technology-lab) | `ars` |
| 45 | 🗞️ Tech news | [LWN.net](https://lwn.net/headlines/rss) | `lwn` |
| 46 | 🗞️ Tech news | [The Hacker News](https://feeds.feedburner.com/TheHackersNews) | `thn` |
| 47 | 🗞️ Tech news | [BleepingComputer](https://www.bleepingcomputer.com/feed/) | `bleeping` |
| 48 | 🗞️ Tech news | [GitHub Changelog](https://github.blog/changelog/feed/) | `ghchangelog` |
| 49 | 🗞️ Tech news | [Simon Willison](https://simonwillison.net/atom/everything/) | `simonw` |
| 50 | 🌍 Public pulse | [Google Trends · daily searches (US and DE)](https://trends.google.com/trending) | `gtrends` |
| 51 | 🌍 Public pulse | [Wikipedia · most read yesterday (English)](https://en.wikipedia.org/wiki/Special:TopViews) | `wikipedia` |
| 52 | 🌍 Public pulse | [Mastodon · trending hashtags (mastodon.social)](https://mastodon.social/explore/tags) | `mastodon_tags` |
| 53 | 🌍 Public pulse | [Mastodon · most shared links (mastodon.social)](https://mastodon.social/explore/links) | `mastodon_links` |
| 54 | 🌍 Public pulse | [Bluesky · trending topics](https://bsky.app/) | `bluesky` |
| — | 🐦 Tech on X | X trend lists already saved in that day's archive file (no extra X call) | — |

Not used, and why:

- **Reddit**: its terms do not allow this kind of automated reuse.
- **Product Hunt API, Glama, GitHub Security Advisories API, Libraries.io**: need a token or an account, or hit low anonymous limits.
- **Papers with Code**: now redirects to Hugging Face papers, which is already a source.
- **Anthropic news**: no public RSS feed.
- **VS Code Marketplace, Ollama library**: no documented public API; reading them would mean scraping.

## Run it yourself

```bash
python3 scripts/update.py --dry-run   # fetch everything, print a report, write nothing
python3 scripts/update.py             # fetch and write README.md, archive/ and niches/
python3 scripts/update.py --only hn_front,kev --dry-run   # test a few sources by key
```

Python 3.9+ and the standard library only. Each request has a 15-second timeout and one retry, hosts are spaced out politely (arXiv every 3 seconds, NVD every 6.5), and the whole fetch stops after about 150 seconds.

## Licence

Contributions are accepted under the [OpenRoots Agent License 2.3](LICENSE) (SPDX `LicenseRef-OpenRoots-ORA-2.3`).
