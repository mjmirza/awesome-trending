# Contributing

This repository is a daily directory, not a dump of everything on the internet. Every morning `scripts/update.py` reads the public sources below, sorts every item into industries, scores it, and rewrites `README.md`, today's file in `archive/` and the files in `industries/`.

## How to help

- **Submit a repo** with the [issue form](https://github.com/mjmirza/awesome-trending/issues/new?template=submit-repo.yml). Give the URL, pick an industry, and write one line on why it belongs.
- Only public repositories, papers, or posts. No private links.
- Do not open a pull request just to add your repo to a table. The tables are rebuilt from the sources every day.
- **Suggest a source** by opening an issue. A source is only added if it is public, needs no API key or login, allows this kind of use in its terms, and answers reliably.
- **Suggest a keyword** for an industry by opening an issue. The rules are plain regular expressions in `INDUSTRIES` inside `scripts/update.py`.
- The [Featured in awesome-trending](docs/badge.md) badge is only for repos that actually appeared here.

## Rules every page follows

- Numbers come from the source named in the row. A dash means the source gave no number. Nothing is estimated or invented.
- "Why it matters" is the first sentence of the item's own description, abstract or summary, shortened. It is never written by hand.
- Each item gets one score from 0 to 100. The formula and every weight are in [docs/methodology.md](docs/methodology.md#score).
- An item listed by more than one source appears once per table, with **Seen on** counting the distinct platforms.
- The layout stays the same every day: today in 30 seconds, top signals, the industry map, industry sections, source sections, status, the maintainer's picks, the archive.
- Long lists are folded inside `<details>`. The README shows the top rows, the archive file for the day has the rest.

## Industries (21 plus Other)

An item can belong to several industries. It is matched by keyword and topic rules on its title, description, tags and topics, plus a few sources that only cover one industry (CISA KEV is Cybersecurity, CoinGecko is Crypto, Launch Library is Space). Anything that matches nothing goes to Other. Full rules: [docs/methodology.md](docs/methodology.md#industries).

| | Industry | Covers |
| --- | --- | --- |
| 🤖 | [AI & LLMs](industries/ai-llms.md) | AI |
| 🧠 | [AI agents & MCP](industries/ai-agents.md) | Agents |
| 🧰 | [Developer tools](industries/devtools.md) | Dev tools |
| ☁️ | [Cloud & DevOps](industries/cloud-devops.md) | Cloud |
| 🔒 | [Cybersecurity](industries/cybersecurity.md) | Security |
| 📊 | [Data & analytics](industries/data-analytics.md) | Data |
| 🌐 | [Web & frontend](industries/web-frontend.md) | Web |
| 📱 | [Mobile](industries/mobile.md) | Mobile |
| 💳 | [Fintech & payments](industries/fintech.md) | Fintech |
| 🪙 | [Crypto & web3](industries/crypto-web3.md) | Crypto |
| 🧬 | [Health & biotech](industries/health-biotech.md) | Health |
| 🦾 | [Robotics & hardware](industries/robotics-hardware.md) | Robotics |
| 🔌 | [Semiconductors & chips](industries/semiconductors.md) | Chips |
| ⚡ | [Climate & energy](industries/climate-energy.md) | Energy |
| 🛒 | [E-commerce & retail](industries/ecommerce-retail.md) | Retail |
| 🎮 | [Gaming & XR](industries/gaming-xr.md) | Gaming |
| 🏢 | [Enterprise SaaS & productivity](industries/enterprise-saas.md) | SaaS |
| 🎓 | [Education](industries/education.md) | Education |
| 🎬 | [Media & creator economy](industries/media-creator.md) | Media |
| 🚀 | [Space & mobility](industries/space-mobility.md) | Space |
| ⚖️ | [Policy & regulation](industries/policy-regulation.md) | Policy |
| 📦 | [Other](industries/other.md) | Other |

The old `niches/` files now only point to the matching industry file.

## Sources (94)

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
| 8 | 🐙 GitHub | [GitHub · young repos tagged robotics](https://github.com/topics/robotics) | `gh_topic_robotics` |
| 9 | 🐙 GitHub | [GitHub · young repos tagged bioinformatics](https://github.com/topics/bioinformatics) | `gh_topic_bioinformatics` |
| 10 | 🐙 GitHub | [GitHub · young repos tagged fintech](https://github.com/topics/fintech) | `gh_topic_fintech` |
| 11 | 💬 Hacker News | [Hacker News · front page](https://news.ycombinator.com/) | `hn_front` |
| 12 | 💬 Hacker News | [Hacker News · Show HN (last 24 h)](https://news.ycombinator.com/show) | `hn_show` |
| 13 | 💬 Hacker News | [Hacker News · Ask HN (last 24 h)](https://news.ycombinator.com/ask) | `hn_ask` |
| 14 | 💬 Hacker News | [Hacker News · best of the week](https://news.ycombinator.com/best) | `hn_best` |
| 15 | 🤗 Models & labs | [Hugging Face · trending models](https://huggingface.co/models?sort=trending) | `hf_models` |
| 16 | 🤗 Models & labs | [Hugging Face · trending Spaces](https://huggingface.co/spaces?sort=trending) | `hf_spaces` |
| 17 | 🤗 Models & labs | [Hugging Face · trending datasets](https://huggingface.co/datasets?sort=trending) | `hf_datasets` |
| 18 | 🤗 Models & labs | [OpenRouter · newest models](https://openrouter.ai/models) | `openrouter` |
| 19 | 🤗 Models & labs | [OpenAI News](https://openai.com/news/rss.xml) | `openai_news` |
| 20 | 🤗 Models & labs | [Google AI blog](https://blog.google/technology/ai/rss/) | `google_ai` |
| 21 | 🤗 Models & labs | [Google DeepMind blog](https://deepmind.google/blog/rss.xml) | `deepmind` |
| 22 | 🤗 Models & labs | [Hugging Face blog](https://huggingface.co/blog/feed.xml) | `hf_blog` |
| 23 | 📄 Papers & preprints | [Hugging Face · daily papers](https://huggingface.co/papers) | `hf_papers` |
| 24 | 📄 Papers & preprints | [arXiv · newest by category](https://arxiv.org/) | `arxiv` |
| 25 | 📄 Papers & preprints | [bioRxiv and medRxiv · newest preprints](https://www.biorxiv.org/) | `biorxiv` |
| 26 | 🔌 MCP registries | [MCP Registry · new and updated servers (24 h)](https://registry.modelcontextprotocol.io/) | `mcp_registry` |
| 27 | 🔌 MCP registries | [Smithery · most-used MCP servers](https://smithery.ai/) | `smithery` |
| 28 | 📦 Packages & releases | [npm · top packages for MCP, AI agents and LLMs](https://www.npmjs.com/) | `npm` |
| 29 | 📦 Packages & releases | [PyPI · latest releases of key AI and Python packages](https://pypi.org/) | `pypi` |
| 30 | 📦 Packages & releases | [crates.io · most downloaded recently](https://crates.io/) | `crates` |
| 31 | 📦 Packages & releases | [jsDelivr · top npm packages by CDN hits this week](https://www.jsdelivr.com/statistics) | `jsdelivr` |
| 32 | 📦 Packages & releases | [Docker Hub · official images updated in the last 48 h](https://hub.docker.com/search?badges=official) | `dockerhub` |
| 33 | 📦 Packages & releases | [GitHub releases · major projects (last 72 h)](https://github.com/) | `releases` |
| 34 | 🛡️ Vulnerabilities | [CISA KEV · known exploited vulnerabilities (last 14 days)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | `kev` |
| 35 | 🛡️ Vulnerabilities | [NVD · critical CVEs published in the last 48 h](https://nvd.nist.gov/vuln/search) | `nvd` |
| 36 | 🛡️ Vulnerabilities | [ENISA EUVD · latest vulnerabilities](https://euvd.enisa.europa.eu/) | `euvd` |
| 37 | 🪙 Markets & launches | [CoinGecko · trending coins (searches, 24 h)](https://www.coingecko.com/en/highlights/trending-crypto) | `coingecko_trending` |
| 38 | 🪙 Markets & launches | [CoinGecko · top 15 by market cap](https://www.coingecko.com/) | `coingecko_markets` |
| 39 | 🪙 Markets & launches | [Launch Library 2 · next orbital launches](https://thespacedevs.com/llapi) | `launches` |
| 40 | ✍️ Community | [Dev.to · top today](https://dev.to/top/day) | `devto_day` |
| 41 | ✍️ Community | [Dev.to · top this week](https://dev.to/top/week) | `devto_week` |
| 42 | ✍️ Community | [Lobsters · hottest](https://lobste.rs/) | `lobsters` |
| 43 | ✍️ Community | [Stack Overflow · hot questions](https://stackoverflow.com/questions?tab=Hot) | `stackoverflow` |
| 44 | ✍️ Community | [Product Hunt · newest featured](https://www.producthunt.com/) | `producthunt` |
| 45 | 🗞️ Tech news | [Techmeme](https://www.techmeme.com/feed.xml) | `techmeme` |
| 46 | 🗞️ Tech news | [The Verge](https://www.theverge.com/rss/index.xml) | `verge` |
| 47 | 🗞️ Tech news | [TechCrunch](https://techcrunch.com/feed/) | `techcrunch` |
| 48 | 🗞️ Tech news | [Ars Technica](https://feeds.arstechnica.com/arstechnica/technology-lab) | `ars` |
| 49 | 🗞️ Tech news | [LWN.net](https://lwn.net/headlines/rss) | `lwn` |
| 50 | 🗞️ Tech news | [The Hacker News](https://feeds.feedburner.com/TheHackersNews) | `thn` |
| 51 | 🗞️ Tech news | [BleepingComputer](https://www.bleepingcomputer.com/feed/) | `bleeping` |
| 52 | 🗞️ Tech news | [GitHub Changelog](https://github.blog/changelog/feed/) | `ghchangelog` |
| 53 | 🗞️ Tech news | [Simon Willison](https://simonwillison.net/atom/everything/) | `simonw` |
| 54 | 🏭 Industry outlets | [Finextra](https://www.finextra.com/rss/headlines.aspx) | `finextra` |
| 55 | 🏭 Industry outlets | [PYMNTS](https://www.pymnts.com/feed/) | `pymnts` |
| 56 | 🏭 Industry outlets | [CoinDesk](https://www.coindesk.com/arc/outboundfeeds/rss/) | `coindesk` |
| 57 | 🏭 Industry outlets | [Decrypt](https://decrypt.co/feed) | `decrypt` |
| 58 | 🏭 Industry outlets | [STAT News](https://www.statnews.com/feed/) | `statnews` |
| 59 | 🏭 Industry outlets | [The Robot Report](https://www.therobotreport.com/feed/) | `robotreport` |
| 60 | 🏭 Industry outlets | [IEEE Spectrum Robotics](https://spectrum.ieee.org/feeds/topic/robotics.rss) | `ieee_robotics` |
| 61 | 🏭 Industry outlets | [IEEE Spectrum Semiconductors](https://spectrum.ieee.org/feeds/topic/semiconductors.rss) | `ieee_semis` |
| 62 | 🏭 Industry outlets | [EE Times](https://www.eetimes.com/feed/) | `eetimes` |
| 63 | 🏭 Industry outlets | [SemiWiki](https://semiwiki.com/feed/) | `semiwiki` |
| 64 | 🏭 Industry outlets | [Canary Media](https://www.canarymedia.com/rss.rss) | `canary` |
| 65 | 🏭 Industry outlets | [Electrek](https://electrek.co/feed/) | `electrek` |
| 66 | 🏭 Industry outlets | [CleanTechnica](https://cleantechnica.com/feed/) | `cleantechnica` |
| 67 | 🏭 Industry outlets | [EIA Today in Energy](https://www.eia.gov/rss/todayinenergy.xml) | `eia` |
| 68 | 🏭 Industry outlets | [Modern Retail](https://www.modernretail.co/feed/) | `modernretail` |
| 69 | 🏭 Industry outlets | [Retail Dive](https://www.retaildive.com/feeds/news/) | `retaildive` |
| 70 | 🏭 Industry outlets | [Digital Commerce 360](https://www.digitalcommerce360.com/feed/) | `dc360` |
| 71 | 🏭 Industry outlets | [GamesIndustry.biz](https://www.gamesindustry.biz/feed) | `gamesindustry` |
| 72 | 🏭 Industry outlets | [Game Developer](https://www.gamedeveloper.com/rss.xml) | `gamedeveloper` |
| 73 | 🏭 Industry outlets | [UploadVR](https://www.uploadvr.com/rss/) | `uploadvr` |
| 74 | 🏭 Industry outlets | [TechCrunch Enterprise](https://techcrunch.com/category/enterprise/feed/) | `tc_enterprise` |
| 75 | 🏭 Industry outlets | [EdSurge](https://www.edsurge.com/articles_rss) | `edsurge` |
| 76 | 🏭 Industry outlets | [Class Central](https://www.classcentral.com/report/feed/) | `classcentral` |
| 77 | 🏭 Industry outlets | [Nieman Lab](https://www.niemanlab.org/feed/) | `niemanlab` |
| 78 | 🏭 Industry outlets | [Tubefilter](https://www.tubefilter.com/feed/) | `tubefilter` |
| 79 | 🏭 Industry outlets | [SpaceNews](https://spacenews.com/feed/) | `spacenews` |
| 80 | 🏭 Industry outlets | [NASA news releases](https://www.nasa.gov/news-release/feed/) | `nasa` |
| 81 | 🏭 Industry outlets | [TechCrunch Transportation](https://techcrunch.com/category/transportation/feed/) | `tc_transport` |
| 82 | 🏭 Industry outlets | [EFF Deeplinks](https://www.eff.org/rss/updates.xml) | `eff` |
| 83 | 🏭 Industry outlets | [European Commission press corner](https://ec.europa.eu/commission/presscorner/api/rss?language=en) | `ec_press` |
| 84 | 🏭 Industry outlets | [9to5Mac](https://9to5mac.com/feed/) | `ninetofivemac` |
| 85 | 🏭 Industry outlets | [Android Police](https://www.androidpolice.com/feed/) | `androidpolice` |
| 86 | 🏭 Industry outlets | [Tech.eu](https://tech.eu/feed/) | `techeu` |
| 87 | 🏭 Industry outlets | [Sifted](https://sifted.eu/feed) | `sifted` |
| 88 | 🌍 Public pulse | [Google Trends · daily searches (US and DE)](https://trends.google.com/trending) | `gtrends` |
| 89 | 🌍 Public pulse | [Wikipedia · most read yesterday (English)](https://en.wikipedia.org/wiki/Special:TopViews) | `wikipedia` |
| 90 | 🌍 Public pulse | [Mastodon · trending hashtags (mastodon.social)](https://mastodon.social/explore/tags) | `mastodon_tags` |
| 91 | 🌍 Public pulse | [Mastodon · most shared links (mastodon.social)](https://mastodon.social/explore/links) | `mastodon_links` |
| 92 | 🌍 Public pulse | [Bluesky · trending topics](https://bsky.app/) | `bluesky` |
| 93 | 🚨 Platform status | [GitHub status · incidents (last 72 h)](https://www.githubstatus.com) | `githubstatus` |
| 94 | 🚨 Platform status | [Cloudflare status · incidents (last 72 h)](https://www.cloudflarestatus.com) | `cloudflarestatus` |
| — | 🐦 Tech on X | X trend lists already saved in that day's archive file (no extra X call) | — |

Not used, and why:

- **Reddit**: its terms do not allow this kind of automated reuse.
- **Product Hunt API, Glama, GitHub Security Advisories API, Libraries.io**: need a token or an account, or hit low anonymous limits.
- **Papers with Code**: now redirects to Hugging Face papers, which is already a source.
- **Anthropic news**: no public RSS feed.
- **Fierce Biotech, MobiHealthNews, Euractiv, Federal Register, FTC press releases**: their feeds refuse automated requests (HTTP 403).
- **Steam charts**: the public endpoint returns app ids only, no game names.
- **DeFiLlama**: the protocol list is a 6 MB download, too heavy for a daily run.
- **Tom's Hardware**: the feed is over 1 MB per fetch.
- **VS Code Marketplace, Ollama library**: no documented public API; reading them would mean scraping.

## Run it yourself

```bash
python3 scripts/update.py --dry-run   # fetch everything, print a report, write nothing
python3 scripts/update.py             # fetch and write README.md, archive/ and industries/
python3 scripts/update.py --only hn_front,kev --dry-run   # test a few sources by key
python3 scripts/update.py --docs      # rewrite docs/methodology.md and the niches/ pointers (only after a rule change)
```

Python 3.9+ and the standard library only. Each request has a 15-second timeout and one retry, hosts are spaced out politely (arXiv every 3 seconds, NVD every 6.5, the GitHub search API every 3), and the whole fetch stops after about 150 seconds.

## Licence

Contributions are accepted under the [OpenRoots Agent License 2.3](LICENSE) (SPDX `LicenseRef-OpenRoots-ORA-2.3`).
