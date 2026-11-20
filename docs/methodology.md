# Methodology

How awesome-trending turns public sources into one scored, industry-sorted page. This file is generated from `scripts/update.py --docs`, so the document and the code cannot drift apart.

<a id="score"></a>

## Score

Every distinct item gets one score from 0 to 100:

```text
score = 100 × ( 0.6 × best_rank_percentile  +  0.4 × min(sources − 1, 3) / 3 )
```

- **best_rank_percentile**: for each *ranked* source that lists the item, `1 − (position − 1) / list length`. Position 1 of 20 is 1.0 and position 11 of 20 is 0.5. The best value across sources counts.
- Items found only in *unranked* sources (news feeds, registries, advisories, releases, markets) get 0.25.
- **sources** counts distinct platforms, not lists: GitHub trending today, this week and per language all count as GitHub.
- Items are merged by normalised URL (GitHub repos by owner/name, papers by arXiv id, a paper's code repo joins its repo) and, for headlines and discussions, by normalised title.
- **Top signals** leaves out items seen only on public-pulse sources (Google Trends, Wikipedia, Mastodon, Bluesky) and items with no ranked source.

Example: a repo at position 2 of 16 on GitHub trending that is also on Hacker News scores `100 × (0.6 × 0.94 + 0.4 × 1/3) = 70`.

**Ranked sources:** `bluesky`, `coingecko_trending`, `devto_day`, `devto_month`, `devto_week`, `devto_year`, `gh_daily`, `gh_go`, `gh_monthly`, `gh_new`, `gh_new_month`, `gh_new_year`, `gh_python`, `gh_rust`, `gh_topic_bioinformatics`, `gh_topic_fintech`, `gh_topic_robotics`, `gh_typescript`, `gh_weekly`, `gtrends`, `hf_datasets`, `hf_models`, `hf_papers`, `hf_papers_month`, `hf_papers_week`, `hf_spaces`, `hn_ask`, `hn_best`, `hn_front`, `hn_month`, `hn_show`, `hn_year`, `jsdelivr`, `lobsters`, `mastodon_links`, `mastodon_tags`, `npm`, `smithery`, `stackoverflow`, `wikipedia`

## Table designs

Each item type has its own columns. Every table ends with **Seen on** (number of platforms listing the item), **Industry** and **Source**.

| Type | Columns |
| --- | --- |
| 🐙 Repositories | stars, stars gained, momentum % (gained ÷ stars before), language, licence and age |
| 💬 Discussions | points, comments, velocity (points per hour) and the thread link |
| ✍️ Posts | tags, reactions or score, comments and author |
| ❓ Questions | tags, score, answers (✓ = accepted), views |
| 🛍️ Product launches | tagline and who posted it |
| 🤗 Models | task and library, likes, 30-day downloads, licence |
| 🧪 Demos (Spaces) | what the demo does, SDK, likes, licence |
| 🗃️ Datasets | task, likes, 30-day downloads, licence |
| 🧩 Hosted models | USD per 1M input and output tokens, context window, date added |
| 📄 Papers | abstract's first sentence, authors, upvotes or category, code link |
| 🔌 MCP servers | what the server does, uses or version, maturity |
| 📦 Packages | ecosystem, version, downloads with the period, release date, licence and stage |
| 📶 CDN traffic | CDN hits this week and change against last week |
| 🐳 Container images | pulls, stars, last update |
| 🏷️ Releases | project, release, stable or pre-release, date |
| 🛡️ Vulnerabilities | vendor and product, CVSS, exploited (in CISA KEV or not), ransomware use, date |
| 🗞️ Headlines | first sentence of the outlet's summary, outlet, time |
| 🚨 Incidents | service, affected components, impact, status, start |
| 🪙 Crypto assets | market-cap rank, price, 24 h and 7 d change, market cap |
| 🛰️ Launches to orbit | provider, launch window in Berlin time, status, site |
| 🔎 Searches | country, Google's search-volume bucket, top story |
| 📖 Most-read articles | views and rank |
| #️⃣ Hashtags | posts and accounts over two days |
| 🦋 Topics | context line |
| 🏁 Leaderboard positions | board, rank, rating, votes, organisation, licence, publish date |
| 💹 Market quotes | level, change against the previous published value, as-of date |

Industry tables mix types, so they use one shared layout: item, type, why it matters, key metric, seen on, score, source.

## Metrics

- **Momentum (repos):** stars gained ÷ stars before the gain. **Velocity (HN):** points ÷ hours since posting.
- **Exploited:** the CVE is in the CISA Known Exploited Vulnerabilities catalogue (the whole catalogue is checked).
- **Downloads:** the period is always written next to the number (30 d for Hugging Face, week for npm and PyPI, 90 d for crates.io).
- **Why it matters** is the item's own description, abstract or summary, cut to its first sentence. Where a source has no description (Hacker News), the cell names the linked site instead.

<a id="industries"></a>

## Industries

An item can belong to several industries. It is placed by:

1. **Source rule**: some sources always map to an industry (table below).
2. **Topic rule**: GitHub topics or post tags that match the industry's topic list.
3. **Keyword rule**: a case-insensitive whole-word match on the title, description, task, topics and tags.
4. Anything with no match goes to **Other**. Keyword-free sources (`arena_image`, `arena_text`, `arena_video`, `cloudflarestatus`, `coingecko_markets`, `coingecko_trending`, `ecb_fx`, `euvd`, `fred`, `githubstatus`, `jsdelivr`, `kev`, `launches`, `nvd`, `st_anthropic`, `st_cohere`, `st_elevenlabs`, `st_mistral`, `st_openai`, `st_perplexity`) use only the source rule, because vendor names or prices would trigger false matches.

| Industry | Scope | GitHub topics | Keywords (regex) |
| --- | --- | --- | --- |
| 🤖 AI & LLMs | Foundation models, inference, ML research and the labs behind them. | `ai`, `artificial-intelligence`, `computer-vision`, `deep-learning`, `generative-ai`, `large-language-models`, `llama`, `llm`, `llms`, `machine-learning`, `nlp`, `openai`, `pytorch`, `transformers` | <sub>`\b(ai\|a\.i\.\|artificial intelligence\|llms?\|gpt[-\w.]*\|chatgpt\|openai\|anthropic\|claude\|gemini\|llama\|qwen\|mistral\|deepseek\|transformers?\|diffusion\|inference\|fine-?tun\w*\|machine learning\|deep learning\|neural\|embeddings?\|rag\|vllm\|ollama\|pytorch\|tensorflow\|multimodal\|vision-language\|language models?\|reasoning model\|text-generation\|text-to-\w+\|image-text-to-text\|hugging ?face\|openvino\|copilot)\b`</sub> |
| 🧠 AI agents & MCP | Agent frameworks, skills, tool use and Model Context Protocol servers. | `agent-skills`, `agentic-ai`, `agents`, `ai-agent`, `ai-agents`, `autonomous-agents`, `claude-code`, `llm-agents`, `mcp`, `mcp-server`, `model-context-protocol` | <sub>`\b(agents?\|agentic\|mcp\|model context protocol\|agent skills?\|skills? (bundle\|library\|framework)\|claude code\|codex\|coding agents?\|autonomous agents?\|crewai\|langgraph\|autogen\|tool[- ]calling\|a2a\|computer[- ]use\|browser[- ]use\|sandbox(es\|ed)?)\b`</sub> |
| 🎥 AI media: video, image, audio & voice | Generative video, image, music, speech and voice models and the companies that make them. | `comfyui`, `diffusion-models`, `image-generation`, `music-generation`, `speech-synthesis`, `stable-diffusion`, `text-to-image`, `text-to-speech`, `text-to-video`, `tts`, `video-generation`, `voice-cloning` | <sub>`\b(text-to-(video\|image\|speech\|audio\|music)\|image-to-video\|video generat\w*\|image generat\w*\|ai video\|ai images?\|generative video\|sora\|veo ?\d*\|runway(ml)?\|kling\|hailuo\|higgsfield\|midjourney\|black forest labs\|flux\.\d\|stable diffusion\|stability ai\|elevenlabs?\|suno\|udio\|heygen\|synthesia\|nano banana\|firefly\|ideogram\|luma ai\|dream machine\|tts\|speech synthesis\|voice clon\w*\|voice ai\|music generat\w*\|lip-?sync\|diffusion models?\|comfyui)\b`</sub> |
| 🧰 Developer tools | Languages, editors, CLIs, package ecosystems and the software toolchain. | `cli`, `compiler`, `developer-tools`, `devtools`, `git`, `golang`, `neovim`, `programming-language`, `python`, `rust`, `terminal`, `typescript`, `vscode` | <sub>`\b(cli\|ide\|editor\|vs ?code\|vim\|neovim\|emacs\|plugins?\|sdk\|compiler\|debugg\w*\|linters?\|terminal\|git\|package manager\|npm\|pypi\|crates?\.io\|cargo\|rustc?\|golang\|python\|typescript\|javascript\|zig\|ruff\|deno\|bun\|node\.?js\|refactor\w*\|developers?\|devtools?\|programming\|open[- ]source)\b`</sub> |
| ☁️ Cloud & DevOps | Infrastructure, containers, CI/CD, self-hosting, outages and operations. | `aws`, `cloud`, `devops`, `docker`, `homelab`, `infrastructure`, `kubernetes`, `linux`, `observability`, `self-hosted`, `terraform` | <sub>`\b(devops\|kubernetes\|k8s\|docker\|containers?\|helm\|terraform\|ansible\|ci/?cd\|aws\|azure\|gcp\|google cloud\|cloud\|serverless\|nginx\|linux\|kernel\|self-host\w*\|homelab\|observability\|grafana\|prometheus\|sre\|outages?\|incident\|hetzner\|cloudflare\|data ?cent(er\|re)s?\|infrastructure)\b`</sub> |
| 🔒 Cybersecurity | Exploited and new vulnerabilities, attacks, defence and security tooling. | `ai-security`, `bug-bounty`, `ctf`, `cybersecurity`, `infosec`, `malware`, `osint`, `penetration-testing`, `pentesting`, `red-team`, `security`, `vulnerability` | <sub>`\b(security\|vulnerab\w*\|cve-\d+\|exploit\w*\|malware\|ransomware\|phishing\|breach\w*\|pentest\w*\|red[- ]team\|bug[- ]?bount\w*\|bug hunt\w*\|zero-day\|0-day\|backdoor\|cryptography\|authentication bypass\|xss\|rce\|privilege escalation\|supply[- ]chain attack\|cyber\w*\|infosec\|hackers?\|spyware\|botnet\|ddos)\b`</sub> |
| 📊 Data & analytics | Databases, datasets, pipelines, analytics and BI. | `analytics`, `big-data`, `data-engineering`, `data-science`, `database`, `dataset`, `etl`, `postgresql`, `sql`, `vector-database` | <sub>`\b(databases?\|postgres\w*\|sqlite\|mysql\|duckdb\|clickhouse\|polars\|pandas\|spark\|kafka\|airflow\|parquet\|iceberg\|etl\|data pipelines?\|datasets?\|data engineering\|vector (db\|database)\|analytics\|olap\|warehouse)\b`</sub> |
| 🌐 Web & frontend | Browsers, front-end frameworks, CSS, web platform and the CDN layer. | `css`, `frontend`, `javascript`, `nextjs`, `react`, `svelte`, `tailwindcss`, `vue`, `web`, `webassembly` | <sub>`\b(frontend\|front-end\|web apps?\|web development\|web framework\|web platform\|web standards?\|browsers?\|css\|html\|react\|next\.js\|nextjs\|vue\|svelte\|angular\|tailwind\|webassembly\|wasm\|chrome\|firefox\|safari\|webgpu)\b`</sub> |
| 📱 Mobile | iOS, Android, phones, wearables and app stores. | `android`, `flutter`, `ios`, `kotlin`, `mobile`, `react-native`, `swift`, `swiftui` | <sub>`\b(ios\|ipados\|android\|iphone\|ipad\|app store\|google play\|mobile\|react native\|flutter\|swiftui\|swift\|kotlin\|jetpack\|xcode\|testflight\|smartphones?\|samsung galaxy\|pixel \d+\|whatsapp\|apple watch\|wearables?)\b`</sub> |
| 💹 Markets & economy | Stocks, rates, inflation, central banks, earnings, funding rounds, M&A, IPOs and layoffs. | `economics`, `finance`, `quantitative-finance`, `stock-market`, `trading` | <sub>`\b(stocks?\|shares (fell\|rose\|jumped\|slid\|surged\|sank\|climbed\|dropped)\|wall street\|nasdaq\|s&p 500\|s&p\|dow jones\|dax\|ftse\|nikkei\|bonds?\|treasur(y\|ies)\|yields?\|interest rates?\|rate (cut\|hike)s?\|inflation\|cpi\|gdp\|recession\|central banks?\|federal reserve\|the fed\|ecb\|earnings\|quarterly results\|revenue\|profits?\|valuations?\|ipos?\|acquisitions?\|acquires?\|acquired\|mergers?\|m&a\|takeover\|funding rounds?\|raises \$[\d.]+\|series [a-f]\|venture capital\|investors?\|layoffs?\|job cuts\|tariffs?\|econom(y\|ic\|ies)\|oil prices?\|gold prices?\|dollar\|bitcoin etf\|market cap)\b`</sub> |
| 💳 Fintech & payments | Banking, payments, lending, trading, insurance and finance infrastructure. | `algorithmic-trading`, `banking`, `finance`, `fintech`, `payments`, `quantitative-finance`, `trading` | <sub>`\b(fintech\|payments?\|banks?\|banking\|neobank\|stripe\|paypal\|visa\|mastercard\|klarna\|adyen\|lending\|loans?\|credit cards?\|trading\|brokerage\|insurtech\|insurance\|remittances?\|open banking\|financial)\b`</sub> |
| 🪙 Crypto & web3 | Cryptocurrencies, blockchains, DeFi, stablecoins and tokenisation. | `bitcoin`, `blockchain`, `crypto`, `cryptocurrency`, `defi`, `ethereum`, `smart-contracts`, `solana`, `web3` | <sub>`\b(crypto\w*\|bitcoin\|btc\|ethereum\|eth\|solana\|blockchains?\|web3\|defi\|stablecoins?\|tokens? (sale\|launch)\|nfts?\|coinbase\|binance\|monero\|xrp\|tokeni[sz]\w*)\b`</sub> |
| 🧬 Health & biotech | Medicine, biology, pharma, health systems and medtech. | `bioinformatics`, `biology`, `genomics`, `health`, `healthcare`, `medical`, `medical-imaging` | <sub>`\b(health\w*\|medic\w*\|clinical\|patients?\|hospitals?\|biotech\w*\|pharma\w*\|drugs?\|fda\|genom\w*\|proteins?\|bioinformatics\|biology\|cancer\|vaccines?\|medicare\|medicaid\|disease\|neuro\w*\|medrxiv\|biorxiv)\b`</sub> |
| 🦾 Robotics & hardware | Robots, drones, embedded devices and consumer hardware. | `3d-printing`, `arduino`, `drones`, `embedded`, `esp32`, `hardware`, `iot`, `robotics`, `ros`, `ros2` | <sub>`\b(robot\w*\|humanoids?\|drones?\|embedded\|firmware\|arduino\|raspberry pi\|esp32\|microcontrollers?\|hardware\|3d print\w*\|lidar\|actuators?\|exoskeleton\w*)\b`</sub> |
| 🔌 Semiconductors & chips | Chip design, fabs, GPUs, accelerators and the supply chain. | `chip-design`, `cuda`, `fpga`, `gpu`, `risc-v`, `semiconductor`, `verilog`, `vlsi` | <sub>`\b(semiconductors?\|chips?\|chipmakers?\|gpus?\|tpus?\|npus?\|asics?\|fpgas?\|nvidia\|nvda\|amd\|intel\|tsmc\|qualcomm\|risc-v\|wafers?\|fabs?\|foundry\|lithography\|asml\|hbm\|cuda\|silicon)\b`</sub> |
| ⚡ Climate & energy | Clean energy, grids, EVs, batteries, oil and gas, and climate. | `climate`, `climate-change`, `electric-vehicles`, `energy`, `renewable-energy`, `solar`, `sustainability` | <sub>`\b(climate\|energy\|solar\|wind (power\|farms?\|turbines?)\|battery storage\|energy storage\|power grids?\|evs?\|electric vehicles?\|ev charging\|hydrogen\|nuclear\|carbon\|emissions\|oil\|natural gas\|lng\|renewables?\|heat pumps?\|power plants?\|utilities)\b`</sub> |
| 🛒 E-commerce & retail | Online and physical retail, marketplaces, logistics and shopping. | `e-commerce`, `ecommerce`, `marketplace`, `retail`, `shopify` | <sub>`\b(e-?commerce\|retail\w*\|shopping\|shoppers?\|black friday\|cyber monday\|amazon\|shopify\|walmart\|marketplaces?\|checkout\|merchants?\|logistics\|grocer\w*\|consumer brands?)\b`</sub> |
| 🎮 Gaming & XR | Games, studios, engines, consoles and VR/AR. | `game`, `game-development`, `game-engine`, `gamedev`, `godot`, `unity`, `unreal-engine`, `vr`, `xr` | <sub>`\b(video ?games?\|gaming\|gamers?\|game (studio\|engine\|developers?)\|playstation\|ps5\|xbox\|nintendo\|switch 2\|steam\|epic games\|unreal engine\|unity\|godot\|esports\|gta ?(6\|vi)\|grand theft auto\|rockstar\|ubisoft\|vr\|xr\|virtual reality\|mixed reality\|vr headsets?\|vision pro\|meta quest)\b`</sub> |
| 🏢 Enterprise SaaS & productivity | Business software, productivity, collaboration and the enterprise market. | `automation`, `crm`, `erp`, `low-code`, `no-code`, `notion`, `productivity`, `saas`, `workflow` | <sub>`\b(saas\|enterprise software\|enterprise ai\|crm\|erp\|salesforce\|workday\|servicenow\|sap\|productivity apps?\|notion\|slack\|microsoft 365\|no-?code\|low-?code\|b2b\|knowledge base\|workflow automation)\b`</sub> |
| 🎓 Education | Schools, universities, edtech, courses and learning resources. | `course`, `edtech`, `education`, `interview`, `learning`, `roadmap`, `tutorial` | <sub>`\b(education\w*\|edtech\|schools?\|students?\|teachers?\|universit(y\|ies)\|courses?\|learning resources\|tutorials?\|mooc\|curriculum\|classrooms?\|lessons?)\b`</sub> |
| 🎬 Media & creator economy | News media, video, streaming, music, social platforms and creators. | `media`, `music`, `podcast`, `social-media`, `streaming`, `video`, `youtube` | <sub>`\b(media\|newsrooms?\|newspapers?\|journalis\w*\|youtube\|tiktok\|instagram\|creators?\|influencers?\|podcasts?\|streaming\|netflix\|spotify\|music\|films?\|movies?\|tv\|publishers?\|social media\|bluesky)\b`</sub> |
| 🚀 Space & mobility | Launches, satellites, aviation, autonomous vehicles and transport. | `aerospace`, `astronomy`, `autonomous-driving`, `satellite`, `self-driving-car`, `space` | <sub>`\b(space ?x\|spacex\|spaceflight\|starship\|starlink\|rockets?\|satellites?\|orbit(al)?\|nasa\|esa\|moon\|lunar\|mars\|astronauts?\|aviation\|aircraft\|airlines?\|faa\|autonomous (vehicles?\|driving)\|robotaxis?\|waymo\|self-driving\|uber\|lyft\|transportation\|mobility)\b`</sub> |
| ⚖️ Policy & regulation | Laws, regulators, courts, antitrust, privacy and digital policy. | `compliance`, `gdpr`, `legal`, `policy`, `privacy`, `regulation` | <sub>`\b(regulat\w*\|laws?\|legislat\w*\|courts?\|lawsuits?\|sues?\|judges?\|antitrust\|competition authority\|ftc\|fcc\|doj\|european commission\|commissioner\|eu ai act\|dma\|dsa\|gdpr\|privacy\|public policy\|tech policy\|government\|ministers?\|congress\|senate\|parliament\|tariffs?\|sanctions\|export controls?)\b`</sub> |

### Source rules

| Source key | Always in |
| --- | --- |
| `hf_models` | AI & LLMs |
| `hf_spaces` | AI & LLMs |
| `hf_datasets` | AI & LLMs, Data & analytics |
| `hf_papers` | AI & LLMs |
| `openrouter` | AI & LLMs |
| `openai_news` | AI & LLMs |
| `google_ai` | AI & LLMs |
| `deepmind` | AI & LLMs |
| `hf_blog` | AI & LLMs |
| `mcp_registry` | AI agents & MCP |
| `smithery` | AI agents & MCP |
| `npm` | Developer tools |
| `pypi` | Developer tools |
| `crates` | Developer tools |
| `stackoverflow` | Developer tools |
| `ghchangelog` | Developer tools |
| `jsdelivr` | Web & frontend |
| `dockerhub` | Cloud & DevOps |
| `githubstatus` | Cloud & DevOps |
| `cloudflarestatus` | Cloud & DevOps |
| `lwn` | Cloud & DevOps |
| `kev` | Cybersecurity |
| `nvd` | Cybersecurity |
| `euvd` | Cybersecurity |
| `hf_media` | AI media: video, image, audio & voice |
| `arena_image` | AI media: video, image, audio & voice |
| `arena_video` | AI media: video, image, audio & voice |
| `arena_text` | AI & LLMs |
| `lab_models` | AI & LLMs |
| `lab_hf` | AI & LLMs |
| `lab_releases` | AI & LLMs |
| `anthropic_news` | AI & LLMs |
| `st_anthropic` | AI & LLMs |
| `st_openai` | AI & LLMs |
| `st_mistral` | AI & LLMs |
| `st_cohere` | AI & LLMs |
| `st_perplexity` | AI & LLMs |
| `st_elevenlabs` | AI media: video, image, audio & voice |
| `fred` | Markets & economy |
| `ecb_fx` | Markets & economy |
| `thn` | Cybersecurity |
| `bleeping` | Cybersecurity |
| `arxiv` | by category: cs.AI → AI & LLMs, cs.CL → AI & LLMs, cs.LG → AI & LLMs, cs.CV → AI & LLMs, cs.CR → Cybersecurity, cs.SE → Developer tools, cs.RO → Robotics & hardware, q-bio → Health & biotech, q-fin → Fintech & payments |
| `finextra` | Fintech & payments |
| `pymnts` | Fintech & payments |
| `coindesk` | Crypto & web3 |
| `decrypt` | Crypto & web3 |
| `statnews` | Health & biotech |
| `robotreport` | Robotics & hardware |
| `ieee_robotics` | Robotics & hardware |
| `ieee_semis` | Semiconductors & chips |
| `eetimes` | Semiconductors & chips |
| `semiwiki` | Semiconductors & chips |
| `canary` | Climate & energy |
| `electrek` | Climate & energy |
| `cleantechnica` | Climate & energy |
| `eia` | Climate & energy |
| `modernretail` | E-commerce & retail |
| `retaildive` | E-commerce & retail |
| `dc360` | E-commerce & retail |
| `gamesindustry` | Gaming & XR |
| `gamedeveloper` | Gaming & XR |
| `uploadvr` | Gaming & XR |
| `tc_enterprise` | Enterprise SaaS & productivity |
| `edsurge` | Education |
| `classcentral` | Education |
| `niemanlab` | Media & creator economy |
| `tubefilter` | Media & creator economy |
| `spacenews` | Space & mobility |
| `nasa` | Space & mobility |
| `tc_transport` | Space & mobility |
| `eff` | Policy & regulation |
| `ec_press` | Policy & regulation |
| `ninetofivemac` | Mobile |
| `androidpolice` | Mobile |
| `decoder` | AI & LLMs |
| `tc_ai` | AI & LLMs |
| `mittr_ai` | AI & LLMs |
| `importai` | AI & LLMs |
| `latent` | AI & LLMs |
| `bensbites` | AI & LLMs |
| `lwiai` | AI & LLMs |
| `tldr_ai` | AI & LLMs |
| `rundown` | AI & LLMs |
| `interconnects` | AI & LLMs |
| `cnbc_top` | Markets & economy |
| `cnbc_markets` | Markets & economy |
| `mw_top` | Markets & economy |
| `bbg_markets` | Markets & economy |
| `bbg_econ` | Markets & economy |
| `ft_home` | Markets & economy |
| `nyt_biz` | Markets & economy |
| `bbc_biz` | Markets & economy |
| `guardian_biz` | Markets & economy |
| `economist_fin` | Markets & economy |
| `crunchbase` | Markets & economy |
| `tc_venture` | Markets & economy |
| `ecb_press` | Markets & economy |
| `fed_press` | Markets & economy |
| `deals_funding`, `deals_ipo` | Markets & economy |
| `media_news_1`, `media_news_2`, `media_news_3`, `media_news_4`, `media_news_5`, `elevenlabs_blog` | AI media: video, image, audio & voice |
| `lab_news_*`, lab blog feeds | AI & LLMs |
| `gh_topic_robotics` | Robotics & hardware |
| `gh_topic_bioinformatics` | Health & biotech |
| `gh_topic_fintech` | Fintech & payments |
| `coingecko_trending`, `coingecko_markets` | Crypto & web3 |
| `biorxiv` | Health & biotech |
| `launches` | Space & mobility |

<a id="shaking"></a>

## What's shaking the market

Every headline, lab post and Hacker News front-page story from the last 36 hours is a candidate. Each headline is cut into its distinctive words (common words, and words found in more than 6% of all candidate headlines, are ignored). A headline joins a story when it shares at least two distinctive words with the story's longest headline and those shared words are at least 50% of the shorter headline's distinctive words. Stories are ranked by the number of distinct outlets (Google News results count the original outlet, not Google), then distinct platforms, then recency. Only stories carried by two or more outlets are shown. "Why it matters" is the first sentence of a summary written by one of the outlets; Google News results carry no summary.

**Markets strip:** FRED (St. Louis Fed) latest published values for the S&P 500, Nasdaq Composite, Dow Jones, VIX, US 10-year yield and Brent; the ECB euro reference rate for EUR/USD; CoinGecko for Bitcoin and Ether. Changes compare the last two published values. DAX, gold and single stocks (NVDA, MSFT, AAPL, GOOGL, AMZN, META, TSLA, TSM) are not shown: no keyless source that allows this kind of reuse was found.

<a id="windows"></a>

## Week, month and year

| Window | Native lists |
| --- | --- |
| This week (7 days) | `gh_weekly`, `gh_new`, `hn_best`, `devto_week`, `hf_papers_week` |
| This month (30 days) | `gh_monthly`, `gh_new_month`, `hn_month`, `devto_month`, `hf_papers_month` |
| This year (365 days) | `gh_new_year`, `hn_year`, `devto_year` |

Each window is scored with the same formula as today, using only that window's lists. Lists for a longer period are never used for today's tables. The **archive rollup** in each window file counts the days an item appeared in the archive. The archive starts on 2026-11-19, so a month or year rollup only covers the days that exist; the file always states how many.

<a id="labs"></a>

## AI labs

| Lab | Google News query | Official feeds | SDK repos | Status page | OpenRouter prefix | Hugging Face orgs |
| --- | --- | --- | --- | --- | --- | --- |
| Anthropic | <sub>`"Anthropic" OR "Claude AI"`</sub> | `anthropic_news` | anthropics/anthropic-sdk-python, anthropics/claude-code | `st_anthropic` | anthropic | — |
| OpenAI | <sub>`"OpenAI"`</sub> | `openai_news` | openai/openai-python, openai/codex | `st_openai` | openai | openai |
| Google DeepMind & Gemini | <sub>`"Google DeepMind" OR "Gemini" Google AI`</sub> | `google_ai`, `deepmind`, `gemini_blog` | googleapis/python-genai, google-gemini/gemini-cli | — | google | google |
| Meta AI | <sub>`"Meta AI" OR "Meta Superintelligence" OR "Llama" Meta`</sub> | — | — | — | meta-llama | meta-llama, facebook |
| Microsoft AI | <sub>`"Microsoft AI" OR "Microsoft Copilot"`</sub> | `ms_ai` | microsoft/semantic-kernel | — | microsoft | microsoft |
| xAI | <sub>`"xAI" Musk AI`</sub> | — | xai-org/xai-sdk-python | — | x-ai | xai-org |
| Mistral AI | <sub>`"Mistral AI"`</sub> | — | mistralai/client-python | `st_mistral` | mistralai | mistralai |
| Cohere | <sub>`"Cohere" AI`</sub> | — | cohere-ai/cohere-python | `st_cohere` | cohere | CohereLabs |
| NVIDIA | <sub>`Nvidia AI`</sub> | `nvidia_blog` | NVIDIA/TensorRT-LLM | — | nvidia | nvidia |
| Amazon & AWS | <sub>`"Amazon" AI (Bedrock OR Nova OR AWS)`</sub> | `aws_ml` | — | — | amazon | amazon |
| Apple | <sub>`"Apple Intelligence" OR "Apple AI"`</sub> | `apple_ml` | ml-explore/mlx | — | — | apple |
| DeepSeek | <sub>`DeepSeek`</sub> | — | — | — | deepseek | deepseek-ai |
| Qwen & Alibaba | <sub>`Qwen OR "Alibaba" AI model`</sub> | — | QwenLM/qwen-code | — | qwen | Qwen |
| Moonshot AI (Kimi) | <sub>`"Moonshot AI" OR Kimi AI`</sub> | — | MoonshotAI/kimi-cli | — | moonshotai | moonshotai |
| Zhipu (Z.ai, GLM) | <sub>`Zhipu OR "Z.ai" GLM`</sub> | — | — | — | z-ai | zai-org |
| Perplexity | <sub>`"Perplexity AI" OR "Perplexity" Comet`</sub> | — | — | `st_perplexity` | perplexity | — |
| Hugging Face | <sub>`"Hugging Face"`</sub> | `hf_blog` | huggingface/transformers | — | — | — |
| Stability AI | <sub>`"Stability AI"`</sub> | — | Stability-AI/generative-models | — | — | stabilityai |

Google News headlines are kept only when the title names the lab. Anthropic publishes no RSS feed, so its newsroom comes from the public sitemap (page address and last-change date). Leaderboard positions come from the LMArena leaderboard dataset on Hugging Face (CC BY 4.0).

## What is never done

- No number is estimated, rounded up or filled in. A dash means the source gave none.
- No source that needs a key, a login, or scraping against its terms.
- The maintainer's own repos sit in their own labelled section and are never boosted.
