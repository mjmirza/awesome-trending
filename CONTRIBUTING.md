# Contributing

This repository is a daily directory, not a dump of everything on the internet. Every morning `scripts/update.py` reads the public sources below, sorts every item into industries, scores it, groups headlines into stories, and rewrites `README.md`, today's file in `archive/`, the files in `industries/` and `windows/`, and `labs/README.md`.

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
- The layout stays the same every day: today in 30 seconds, what's shaking the market (with the markets strip), top signals, this month, this week, this year, AI labs, AI media, the industry map, industry sections, source sections, status, the maintainer's picks, the archive.
- Week, month and year lists come from each platform's own period view. Archive rollups only count days that exist in `archive/` (it starts on 19 November 2026), and every window file says how many days that is.
- Long lists are folded inside `<details>`. The README shows the top rows, the archive file for the day has the rest.

## Industries (23 plus Other)

An item can belong to several industries. It is matched by keyword and topic rules on its title, description, tags and topics, plus a few sources that only cover one industry (CISA KEV is Cybersecurity, CoinGecko is Crypto, Launch Library is Space). Anything that matches nothing goes to Other. Full rules: [docs/methodology.md](docs/methodology.md#industries).

| | Industry | Covers |
| --- | --- | --- |
| 🤖 | [AI & LLMs](industries/ai-llms.md) | AI |
| 🧠 | [AI agents & MCP](industries/ai-agents.md) | Agents |
| 🎥 | [AI media: video, image, audio & voice](industries/ai-media.md) | AI media |
| 🧰 | [Developer tools](industries/devtools.md) | Dev tools |
| ☁️ | [Cloud & DevOps](industries/cloud-devops.md) | Cloud |
| 🔒 | [Cybersecurity](industries/cybersecurity.md) | Security |
| 📊 | [Data & analytics](industries/data-analytics.md) | Data |
| 🌐 | [Web & frontend](industries/web-frontend.md) | Web |
| 📱 | [Mobile](industries/mobile.md) | Mobile |
| 💹 | [Markets & economy](industries/markets-economy.md) | Markets |
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

## Sources (179)

All of them are free, public and keyless. If one fails, it is marked Skipped for that day and the rest still publish.

| # | Section | Source | Key |
| --- | --- | --- | --- |
| 1 | 🐙 GitHub | [GitHub trending · today](https://github.com/trending?since=daily) | `gh_daily` |
| 2 | 🐙 GitHub | [GitHub trending · Python](https://github.com/trending/python?since=daily) | `gh_python` |
| 3 | 🐙 GitHub | [GitHub trending · TypeScript](https://github.com/trending/typescript?since=daily) | `gh_typescript` |
| 4 | 🐙 GitHub | [GitHub trending · Rust](https://github.com/trending/rust?since=daily) | `gh_rust` |
| 5 | 🐙 GitHub | [GitHub trending · Go](https://github.com/trending/go?since=daily) | `gh_go` |
| 6 | 🐙 GitHub | [GitHub · young repos tagged robotics](https://github.com/topics/robotics) | `gh_topic_robotics` |
| 7 | 🐙 GitHub | [GitHub · young repos tagged bioinformatics](https://github.com/topics/bioinformatics) | `gh_topic_bioinformatics` |
| 8 | 🐙 GitHub | [GitHub · young repos tagged fintech](https://github.com/topics/fintech) | `gh_topic_fintech` |
| 9 | 💬 Hacker News | [Hacker News · front page](https://news.ycombinator.com/) | `hn_front` |
| 10 | 💬 Hacker News | [Hacker News · Show HN (last 24 h)](https://news.ycombinator.com/show) | `hn_show` |
| 11 | 💬 Hacker News | [Hacker News · Ask HN (last 24 h)](https://news.ycombinator.com/ask) | `hn_ask` |
| 12 | 🤗 Models & labs | [Hugging Face · trending models](https://huggingface.co/models?sort=trending) | `hf_models` |
| 13 | 🤗 Models & labs | [Hugging Face · trending Spaces](https://huggingface.co/spaces?sort=trending) | `hf_spaces` |
| 14 | 🤗 Models & labs | [Hugging Face · trending datasets](https://huggingface.co/datasets?sort=trending) | `hf_datasets` |
| 15 | 🤗 Models & labs | [OpenRouter · newest models](https://openrouter.ai/models) | `openrouter` |
| 16 | 🤗 Models & labs | [OpenAI News](https://openai.com/news/rss.xml) | `openai_news` |
| 17 | 🤗 Models & labs | [Google AI blog](https://blog.google/technology/ai/rss/) | `google_ai` |
| 18 | 🤗 Models & labs | [Google DeepMind blog](https://deepmind.google/blog/rss.xml) | `deepmind` |
| 19 | 🤗 Models & labs | [Hugging Face blog](https://huggingface.co/blog/feed.xml) | `hf_blog` |
| 20 | 🏛️ AI labs & big players | [Google · Gemini blog](https://blog.google/products/gemini/rss/) | `gemini_blog` |
| 21 | 🏛️ AI labs & big players | [Microsoft Source · AI](https://news.microsoft.com/source/topics/ai/feed/) | `ms_ai` |
| 22 | 🏛️ AI labs & big players | [NVIDIA blog](https://blogs.nvidia.com/feed/) | `nvidia_blog` |
| 23 | 🏛️ AI labs & big players | [AWS Machine Learning blog](https://aws.amazon.com/blogs/machine-learning/feed/) | `aws_ml` |
| 24 | 🏛️ AI labs & big players | [Apple Machine Learning Research](https://machinelearning.apple.com/rss.xml) | `apple_ml` |
| 25 | 🏛️ AI labs & big players | [Anthropic · newsroom (public sitemap)](https://www.anthropic.com/news) | `anthropic_news` |
| 26 | 🏛️ AI labs & big players | [Google News · Anthropic](https://news.google.com/search?q=%22Anthropic%22+OR+%22Claude+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_anthropic` |
| 27 | 🏛️ AI labs & big players | [Google News · OpenAI](https://news.google.com/search?q=%22OpenAI%22&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_openai` |
| 28 | 🏛️ AI labs & big players | [Google News · Google DeepMind & Gemini](https://news.google.com/search?q=%22Google+DeepMind%22+OR+%22Gemini%22+Google+AI&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_google` |
| 29 | 🏛️ AI labs & big players | [Google News · Meta AI](https://news.google.com/search?q=%22Meta+AI%22+OR+%22Meta+Superintelligence%22+OR+%22Llama%22+Meta&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_meta` |
| 30 | 🏛️ AI labs & big players | [Google News · Microsoft AI](https://news.google.com/search?q=%22Microsoft+AI%22+OR+%22Microsoft+Copilot%22&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_microsoft` |
| 31 | 🏛️ AI labs & big players | [Google News · xAI](https://news.google.com/search?q=%22xAI%22+Musk+AI&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_xai` |
| 32 | 🏛️ AI labs & big players | [Google News · Mistral AI](https://news.google.com/search?q=%22Mistral+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_mistral` |
| 33 | 🏛️ AI labs & big players | [Google News · Cohere](https://news.google.com/search?q=%22Cohere%22+AI&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_cohere` |
| 34 | 🏛️ AI labs & big players | [Google News · NVIDIA](https://news.google.com/search?q=Nvidia+AI&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_nvidia` |
| 35 | 🏛️ AI labs & big players | [Google News · Amazon & AWS](https://news.google.com/search?q=%22Amazon%22+AI+%28Bedrock+OR+Nova+OR+AWS%29&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_amazon` |
| 36 | 🏛️ AI labs & big players | [Google News · Apple](https://news.google.com/search?q=%22Apple+Intelligence%22+OR+%22Apple+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_apple` |
| 37 | 🏛️ AI labs & big players | [Google News · DeepSeek](https://news.google.com/search?q=DeepSeek&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_deepseek` |
| 38 | 🏛️ AI labs & big players | [Google News · Qwen & Alibaba](https://news.google.com/search?q=Qwen+OR+%22Alibaba%22+AI+model&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_qwen` |
| 39 | 🏛️ AI labs & big players | [Google News · Moonshot AI (Kimi)](https://news.google.com/search?q=%22Moonshot+AI%22+OR+Kimi+AI&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_moonshot` |
| 40 | 🏛️ AI labs & big players | [Google News · Zhipu (Z.ai, GLM)](https://news.google.com/search?q=Zhipu+OR+%22Z.ai%22+GLM&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_zhipu` |
| 41 | 🏛️ AI labs & big players | [Google News · Perplexity](https://news.google.com/search?q=%22Perplexity+AI%22+OR+%22Perplexity%22+Comet&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_perplexity` |
| 42 | 🏛️ AI labs & big players | [Google News · Hugging Face](https://news.google.com/search?q=%22Hugging+Face%22&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_huggingface` |
| 43 | 🏛️ AI labs & big players | [Google News · Stability AI](https://news.google.com/search?q=%22Stability+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | `lab_news_stability` |
| 44 | 🏛️ AI labs & big players | [GitHub releases · AI lab SDKs and tools (last 14 days)](https://github.com/) | `lab_releases` |
| 45 | 🏛️ AI labs & big players | [OpenRouter · models added by the big labs (last 60 days)](https://openrouter.ai/models) | `lab_models` |
| 46 | 🏛️ AI labs & big players | [Hugging Face · newest open-weight models from the big labs (last 30 days)](https://huggingface.co/models?sort=created) | `lab_hf` |
| 47 | 🏛️ AI labs & big players | [LMArena · text leaderboard](https://lmarena.ai/leaderboard/text) | `arena_text` |
| 48 | 🎥 AI media | [ElevenLabs blog](https://elevenlabs.io/blog/rss.xml) | `elevenlabs_blog` |
| 49 | 🎥 AI media | [LMArena · text-to-image leaderboard](https://lmarena.ai/leaderboard/text-to-image) | `arena_image` |
| 50 | 🎥 AI media | [LMArena · text-to-video leaderboard](https://lmarena.ai/leaderboard/text-to-video) | `arena_video` |
| 51 | 🎥 AI media | [Google News · AI media (Sora, Veo, Runway)](https://news.google.com/search?q=Sora+OpenAI+video+OR+%22Google+Veo%22+OR+%22Runway%22+AI+video&hl=en-US&gl=US&ceid=US%3Aen) | `media_news_1` |
| 52 | 🎥 AI media | [Google News · AI media (Luma, Pika, Kling)](https://news.google.com/search?q=%22Luma+AI%22+OR+%22Pika%22+AI+video+OR+%22Kling%22+AI&hl=en-US&gl=US&ceid=US%3Aen) | `media_news_2` |
| 53 | 🎥 AI media | [Google News · AI media (Hailuo, Higgsfield, Midjourney)](https://news.google.com/search?q=Hailuo+OR+MiniMax+video+OR+Higgsfield+OR+Midjourney&hl=en-US&gl=US&ceid=US%3Aen) | `media_news_3` |
| 54 | 🎥 AI media | [Google News · AI media (FLUX, ElevenLabs, Suno)](https://news.google.com/search?q=%22Black+Forest+Labs%22+OR+FLUX+image+model+OR+ElevenLabs+OR+Suno&hl=en-US&gl=US&ceid=US%3Aen) | `media_news_4` |
| 55 | 🎥 AI media | [Google News · AI media (Udio, HeyGen, Synthesia)](https://news.google.com/search?q=Udio+OR+HeyGen+OR+Synthesia+OR+%22Nano+Banana%22&hl=en-US&gl=US&ceid=US%3Aen) | `media_news_5` |
| 56 | 🎥 AI media | [Hugging Face · trending video, image and audio models](https://huggingface.co/models?sort=trending) | `hf_media` |
| 57 | 🧠 AI news & newsletters | [The Decoder](https://the-decoder.com/feed/) | `decoder` |
| 58 | 🧠 AI news & newsletters | [TechCrunch · AI](https://techcrunch.com/category/artificial-intelligence/feed/) | `tc_ai` |
| 59 | 🧠 AI news & newsletters | [MIT Technology Review · AI](https://www.technologyreview.com/topic/artificial-intelligence/feed) | `mittr_ai` |
| 60 | 🧠 AI news & newsletters | [Import AI](https://importai.substack.com/feed) | `importai` |
| 61 | 🧠 AI news & newsletters | [Latent Space](https://www.latent.space/feed) | `latent` |
| 62 | 🧠 AI news & newsletters | [Ben's Bites](https://www.bensbites.com/feed) | `bensbites` |
| 63 | 🧠 AI news & newsletters | [Last Week in AI](https://lastweekin.ai/feed) | `lwiai` |
| 64 | 🧠 AI news & newsletters | [TLDR AI](https://tldr.tech/api/rss/ai) | `tldr_ai` |
| 65 | 🧠 AI news & newsletters | [The Rundown AI](https://www.therundown.ai/feed) | `rundown` |
| 66 | 🧠 AI news & newsletters | [Interconnects](https://www.interconnects.ai/feed) | `interconnects` |
| 67 | 📄 Papers & preprints | [Hugging Face · daily papers](https://huggingface.co/papers) | `hf_papers` |
| 68 | 📄 Papers & preprints | [arXiv · newest by category](https://arxiv.org/) | `arxiv` |
| 69 | 📄 Papers & preprints | [bioRxiv and medRxiv · newest preprints](https://www.biorxiv.org/) | `biorxiv` |
| 70 | 🔌 MCP registries | [MCP Registry · new and updated servers (24 h)](https://registry.modelcontextprotocol.io/) | `mcp_registry` |
| 71 | 🔌 MCP registries | [Smithery · most-used MCP servers](https://smithery.ai/) | `smithery` |
| 72 | 📦 Packages & releases | [npm · top packages for MCP, AI agents and LLMs](https://www.npmjs.com/) | `npm` |
| 73 | 📦 Packages & releases | [PyPI · latest releases of key AI and Python packages](https://pypi.org/) | `pypi` |
| 74 | 📦 Packages & releases | [crates.io · most downloaded recently](https://crates.io/) | `crates` |
| 75 | 📦 Packages & releases | [jsDelivr · top npm packages by CDN hits this week](https://www.jsdelivr.com/statistics) | `jsdelivr` |
| 76 | 📦 Packages & releases | [Docker Hub · official images updated in the last 48 h](https://hub.docker.com/search?badges=official) | `dockerhub` |
| 77 | 📦 Packages & releases | [GitHub releases · major projects (last 72 h)](https://github.com/) | `releases` |
| 78 | 🛡️ Vulnerabilities | [CISA KEV · known exploited vulnerabilities (last 14 days)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | `kev` |
| 79 | 🛡️ Vulnerabilities | [NVD · critical CVEs published in the last 48 h](https://nvd.nist.gov/vuln/search) | `nvd` |
| 80 | 🛡️ Vulnerabilities | [ENISA EUVD · latest vulnerabilities](https://euvd.enisa.europa.eu/) | `euvd` |
| 81 | 💹 Markets & economy | [CNBC · top news](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114) | `cnbc_top` |
| 82 | 💹 Markets & economy | [CNBC · markets](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258) | `cnbc_markets` |
| 83 | 💹 Markets & economy | [CNBC · technology](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910) | `cnbc_tech` |
| 84 | 💹 Markets & economy | [MarketWatch · top stories](https://feeds.content.dowjones.io/public/rss/mw_topstories) | `mw_top` |
| 85 | 💹 Markets & economy | [Bloomberg · markets](https://feeds.bloomberg.com/markets/news.rss) | `bbg_markets` |
| 86 | 💹 Markets & economy | [Bloomberg · technology](https://feeds.bloomberg.com/technology/news.rss) | `bbg_tech` |
| 87 | 💹 Markets & economy | [Bloomberg · economics](https://feeds.bloomberg.com/economics/news.rss) | `bbg_econ` |
| 88 | 💹 Markets & economy | [Financial Times · home](https://www.ft.com/rss/home) | `ft_home` |
| 89 | 💹 Markets & economy | [Financial Times · technology](https://www.ft.com/technology?format=rss) | `ft_tech` |
| 90 | 💹 Markets & economy | [New York Times · business](https://rss.nytimes.com/services/xml/rss/nyt/Business.xml) | `nyt_biz` |
| 91 | 💹 Markets & economy | [New York Times · technology](https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml) | `nyt_tech` |
| 92 | 💹 Markets & economy | [BBC · business](https://feeds.bbci.co.uk/news/business/rss.xml) | `bbc_biz` |
| 93 | 💹 Markets & economy | [The Guardian · business](https://www.theguardian.com/uk/business/rss) | `guardian_biz` |
| 94 | 💹 Markets & economy | [The Economist · finance and economics](https://www.economist.com/finance-and-economics/rss.xml) | `economist_fin` |
| 95 | 💹 Markets & economy | [The Information](https://www.theinformation.com/feed) | `theinformation` |
| 96 | 💹 Markets & economy | [Crunchbase News](https://news.crunchbase.com/feed/) | `crunchbase` |
| 97 | 💹 Markets & economy | [TechCrunch · venture](https://techcrunch.com/category/venture/feed/) | `tc_venture` |
| 98 | 💹 Markets & economy | [European Central Bank · press](https://www.ecb.europa.eu/rss/press.html) | `ecb_press` |
| 99 | 💹 Markets & economy | [Federal Reserve · press releases](https://www.federalreserve.gov/feeds/press_all.xml) | `fed_press` |
| 100 | 💹 Markets & economy | [Google News · funding rounds and acquisitions](https://news.google.com/search?q=startup+raises+funding+round+OR+tech+acquisition+acquires&hl=en-US&gl=US&ceid=US%3Aen) | `deals_funding` |
| 101 | 💹 Markets & economy | [Google News · IPOs and layoffs](https://news.google.com/search?q=tech+IPO+shares+debut+OR+tech+layoffs+job+cuts&hl=en-US&gl=US&ceid=US%3Aen) | `deals_ipo` |
| 102 | 💹 Markets & economy | [FRED · US markets and rates (St. Louis Fed)](https://fred.stlouisfed.org/) | `fred` |
| 103 | 💹 Markets & economy | [ECB · euro reference rate (USD)](https://data.ecb.europa.eu/data/datasets/EXR) | `ecb_fx` |
| 104 | 🪙 Crypto & launches | [CoinGecko · trending coins (searches, 24 h)](https://www.coingecko.com/en/highlights/trending-crypto) | `coingecko_trending` |
| 105 | 🪙 Crypto & launches | [CoinGecko · top 15 by market cap](https://www.coingecko.com/) | `coingecko_markets` |
| 106 | 🪙 Crypto & launches | [Launch Library 2 · next orbital launches](https://thespacedevs.com/llapi) | `launches` |
| 107 | ✍️ Community | [Dev.to · top today](https://dev.to/top/day) | `devto_day` |
| 108 | ✍️ Community | [Lobsters · hottest](https://lobste.rs/) | `lobsters` |
| 109 | ✍️ Community | [Stack Overflow · hot questions](https://stackoverflow.com/questions?tab=Hot) | `stackoverflow` |
| 110 | ✍️ Community | [Product Hunt · newest featured](https://www.producthunt.com/) | `producthunt` |
| 111 | 🗞️ Tech news | [Techmeme](https://www.techmeme.com/feed.xml) | `techmeme` |
| 112 | 🗞️ Tech news | [The Verge](https://www.theverge.com/rss/index.xml) | `verge` |
| 113 | 🗞️ Tech news | [TechCrunch](https://techcrunch.com/feed/) | `techcrunch` |
| 114 | 🗞️ Tech news | [Ars Technica](https://feeds.arstechnica.com/arstechnica/technology-lab) | `ars` |
| 115 | 🗞️ Tech news | [LWN.net](https://lwn.net/headlines/rss) | `lwn` |
| 116 | 🗞️ Tech news | [The Hacker News](https://feeds.feedburner.com/TheHackersNews) | `thn` |
| 117 | 🗞️ Tech news | [BleepingComputer](https://www.bleepingcomputer.com/feed/) | `bleeping` |
| 118 | 🗞️ Tech news | [GitHub Changelog](https://github.blog/changelog/feed/) | `ghchangelog` |
| 119 | 🗞️ Tech news | [Simon Willison](https://simonwillison.net/atom/everything/) | `simonw` |
| 120 | 🏭 Industry outlets | [Finextra](https://www.finextra.com/rss/headlines.aspx) | `finextra` |
| 121 | 🏭 Industry outlets | [PYMNTS](https://www.pymnts.com/feed/) | `pymnts` |
| 122 | 🏭 Industry outlets | [CoinDesk](https://www.coindesk.com/arc/outboundfeeds/rss/) | `coindesk` |
| 123 | 🏭 Industry outlets | [Decrypt](https://decrypt.co/feed) | `decrypt` |
| 124 | 🏭 Industry outlets | [STAT News](https://www.statnews.com/feed/) | `statnews` |
| 125 | 🏭 Industry outlets | [The Robot Report](https://www.therobotreport.com/feed/) | `robotreport` |
| 126 | 🏭 Industry outlets | [IEEE Spectrum Robotics](https://spectrum.ieee.org/feeds/topic/robotics.rss) | `ieee_robotics` |
| 127 | 🏭 Industry outlets | [IEEE Spectrum Semiconductors](https://spectrum.ieee.org/feeds/topic/semiconductors.rss) | `ieee_semis` |
| 128 | 🏭 Industry outlets | [EE Times](https://www.eetimes.com/feed/) | `eetimes` |
| 129 | 🏭 Industry outlets | [SemiWiki](https://semiwiki.com/feed/) | `semiwiki` |
| 130 | 🏭 Industry outlets | [Canary Media](https://www.canarymedia.com/rss.rss) | `canary` |
| 131 | 🏭 Industry outlets | [Electrek](https://electrek.co/feed/) | `electrek` |
| 132 | 🏭 Industry outlets | [CleanTechnica](https://cleantechnica.com/feed/) | `cleantechnica` |
| 133 | 🏭 Industry outlets | [EIA Today in Energy](https://www.eia.gov/rss/todayinenergy.xml) | `eia` |
| 134 | 🏭 Industry outlets | [Modern Retail](https://www.modernretail.co/feed/) | `modernretail` |
| 135 | 🏭 Industry outlets | [Retail Dive](https://www.retaildive.com/feeds/news/) | `retaildive` |
| 136 | 🏭 Industry outlets | [Digital Commerce 360](https://www.digitalcommerce360.com/feed/) | `dc360` |
| 137 | 🏭 Industry outlets | [GamesIndustry.biz](https://www.gamesindustry.biz/feed) | `gamesindustry` |
| 138 | 🏭 Industry outlets | [Game Developer](https://www.gamedeveloper.com/rss.xml) | `gamedeveloper` |
| 139 | 🏭 Industry outlets | [UploadVR](https://www.uploadvr.com/rss/) | `uploadvr` |
| 140 | 🏭 Industry outlets | [TechCrunch Enterprise](https://techcrunch.com/category/enterprise/feed/) | `tc_enterprise` |
| 141 | 🏭 Industry outlets | [EdSurge](https://www.edsurge.com/articles_rss) | `edsurge` |
| 142 | 🏭 Industry outlets | [Class Central](https://www.classcentral.com/report/feed/) | `classcentral` |
| 143 | 🏭 Industry outlets | [Nieman Lab](https://www.niemanlab.org/feed/) | `niemanlab` |
| 144 | 🏭 Industry outlets | [Tubefilter](https://www.tubefilter.com/feed/) | `tubefilter` |
| 145 | 🏭 Industry outlets | [SpaceNews](https://spacenews.com/feed/) | `spacenews` |
| 146 | 🏭 Industry outlets | [NASA news releases](https://www.nasa.gov/news-release/feed/) | `nasa` |
| 147 | 🏭 Industry outlets | [TechCrunch Transportation](https://techcrunch.com/category/transportation/feed/) | `tc_transport` |
| 148 | 🏭 Industry outlets | [EFF Deeplinks](https://www.eff.org/rss/updates.xml) | `eff` |
| 149 | 🏭 Industry outlets | [European Commission press corner](https://ec.europa.eu/commission/presscorner/api/rss?language=en) | `ec_press` |
| 150 | 🏭 Industry outlets | [9to5Mac](https://9to5mac.com/feed/) | `ninetofivemac` |
| 151 | 🏭 Industry outlets | [Android Police](https://www.androidpolice.com/feed/) | `androidpolice` |
| 152 | 🏭 Industry outlets | [Tech.eu](https://tech.eu/feed/) | `techeu` |
| 153 | 🏭 Industry outlets | [Sifted](https://sifted.eu/feed) | `sifted` |
| 154 | 🌍 Public pulse | [Google Trends · daily searches (US and DE)](https://trends.google.com/trending) | `gtrends` |
| 155 | 🌍 Public pulse | [Wikipedia · most read yesterday (English)](https://en.wikipedia.org/wiki/Special:TopViews) | `wikipedia` |
| 156 | 🌍 Public pulse | [Mastodon · trending hashtags (mastodon.social)](https://mastodon.social/explore/tags) | `mastodon_tags` |
| 157 | 🌍 Public pulse | [Mastodon · most shared links (mastodon.social)](https://mastodon.social/explore/links) | `mastodon_links` |
| 158 | 🌍 Public pulse | [Bluesky · trending topics](https://bsky.app/) | `bluesky` |
| 159 | 🗓️ Week, month and year lists | [GitHub trending · this week](https://github.com/trending?since=weekly) | `gh_weekly` |
| 160 | 🗓️ Week, month and year lists | [GitHub · new repos gaining stars (created in the last 7 days)](https://docs.github.com/en/rest/search/search#search-repositories) | `gh_new` |
| 161 | 🗓️ Week, month and year lists | [Hacker News · best of the week](https://news.ycombinator.com/best) | `hn_best` |
| 162 | 🗓️ Week, month and year lists | [Dev.to · top this week](https://dev.to/top/week) | `devto_week` |
| 163 | 🗓️ Week, month and year lists | [GitHub trending · this month](https://github.com/trending?since=monthly) | `gh_monthly` |
| 164 | 🗓️ Week, month and year lists | [GitHub · most-starred repos created in the last 30 days](https://docs.github.com/en/rest/search/search#search-repositories) | `gh_new_month` |
| 165 | 🗓️ Week, month and year lists | [GitHub · most-starred repos created in the last 365 days](https://docs.github.com/en/rest/search/search#search-repositories) | `gh_new_year` |
| 166 | 🗓️ Week, month and year lists | [Hacker News · best of the last 30 days](https://news.ycombinator.com/best) | `hn_month` |
| 167 | 🗓️ Week, month and year lists | [Hacker News · best of the last 365 days](https://news.ycombinator.com/best) | `hn_year` |
| 168 | 🗓️ Week, month and year lists | [Dev.to · top this month](https://dev.to/top/month) | `devto_month` |
| 169 | 🗓️ Week, month and year lists | [Dev.to · top this year](https://dev.to/top/year) | `devto_year` |
| 170 | 🗓️ Week, month and year lists | [Hugging Face · papers of the week](https://huggingface.co/papers) | `hf_papers_week` |
| 171 | 🗓️ Week, month and year lists | [Hugging Face · papers of the month](https://huggingface.co/papers) | `hf_papers_month` |
| 172 | 🚨 Platform status | [GitHub status · incidents (last 72 h)](https://www.githubstatus.com) | `githubstatus` |
| 173 | 🚨 Platform status | [Cloudflare status · incidents (last 72 h)](https://www.cloudflarestatus.com) | `cloudflarestatus` |
| 174 | 🚨 Platform status | [Anthropic status · incidents (last 72 h)](https://status.anthropic.com) | `st_anthropic` |
| 175 | 🚨 Platform status | [OpenAI status · incidents (last 72 h)](https://status.openai.com) | `st_openai` |
| 176 | 🚨 Platform status | [Mistral AI status · incidents (last 72 h)](https://status.mistral.ai) | `st_mistral` |
| 177 | 🚨 Platform status | [Cohere status · incidents (last 72 h)](https://status.cohere.com) | `st_cohere` |
| 178 | 🚨 Platform status | [Perplexity status · incidents (last 72 h)](https://status.perplexity.com) | `st_perplexity` |
| 179 | 🚨 Platform status | [ElevenLabs status · incidents (last 72 h)](https://status.elevenlabs.io) | `st_elevenlabs` |
| — | 🐦 Tech on X | X trend lists already saved in that day's archive file (no extra X call) | — |

Not used, and why:

- **Reddit**: its terms do not allow this kind of automated reuse.
- **Product Hunt API, Glama, GitHub Security Advisories API, Libraries.io**: need a token or an account, or hit low anonymous limits.
- **Papers with Code**: now redirects to Hugging Face papers, which is already a source.
- **Anthropic RSS**: Anthropic publishes no feed, so its newsroom is read from the public sitemap instead.
- **VS Code Marketplace, Ollama library**: no documented public API; reading them would mean scraping.
- **Fierce Biotech, MobiHealthNews, Euractiv, Federal Register, FTC press releases**: their feeds refuse automated requests (HTTP 403).
- **Steam charts**: the public endpoint returns app ids only, no game names.
- **DeFiLlama**: the protocol list is a 6 MB download, too heavy for a daily run.
- **Tom's Hardware, Semafor, Axios**: the feeds are about 1 MB per fetch.
- **Reuters**: no public RSS feed any more (the old feed addresses return 404).
- **Yahoo Finance quotes and news RSS**: the quote endpoint is undocumented and Yahoo's terms do not allow automated reuse; the news RSS returns 404.
- **Stooq quotes**: did not answer from the runner (timeouts).
- **DAX, gold and single stock quotes** (NVDA, MSFT, AAPL, GOOGL, AMZN, META, TSLA, TSM): no keyless source that allows reuse was found. US indices come from FRED instead.
- **WSJ feeds, MarketWatch market pulse, Layoffs.fyi feed, Qwen blog feed**: stopped updating (last items between 2020 and 2025).
- **VentureBeat AI**: answers automated requests with HTTP 429. **AI News (artificialintelligence-news.com)**: bot check page.
- **Meta AI blog, Mistral news, Runway news, Black Forest Labs blog**: no RSS feed (404). They are covered by Google News search and LMArena.
- **Microsoft AI blog**: the feed is retired (HTTP 410); the Microsoft Source AI feed is used instead.
- **Status pages for xAI, Google Gemini, Hugging Face, Groq and Replicate**: no public Statuspage JSON (missing or HTML only).
- **fal.ai and Replicate model lists, Artificial Analysis**: only an undocumented internal endpoint, or an API key is needed.
- **Open LLM Leaderboard**: retired. The LMArena leaderboard dataset (CC BY 4.0) is used instead.

## Run it yourself

```bash
python3 scripts/update.py --dry-run   # fetch everything, print a report, write nothing
python3 scripts/update.py             # fetch and write README.md, archive/, industries/, windows/ and labs/
python3 scripts/update.py --only hn_front,kev --dry-run   # test a few sources by key
python3 scripts/update.py --docs      # rewrite docs/methodology.md and the niches/ pointers (only after a rule change)
```

Python 3.9+ and the standard library only. Each request has a 15-second timeout and one retry, hosts are spaced out politely (arXiv every 3 seconds, NVD every 6.5, the GitHub search API every 6.2, Google News every 1.6), up to 16 sources run at once, and the whole fetch stops after about 150 seconds.

## Licence

Contributions are accepted under the [OpenRoots Agent License 2.3](LICENSE) (SPDX `LicenseRef-OpenRoots-ORA-2.3`).
