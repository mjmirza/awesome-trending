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

**Ranked sources:** `bluesky`, `coingecko_trending`, `devto_day`, `devto_week`, `gh_daily`, `gh_go`, `gh_new`, `gh_python`, `gh_rust`, `gh_topic_bioinformatics`, `gh_topic_fintech`, `gh_topic_robotics`, `gh_typescript`, `gh_weekly`, `gtrends`, `hf_datasets`, `hf_models`, `hf_papers`, `hf_spaces`, `hn_ask`, `hn_best`, `hn_front`, `hn_show`, `jsdelivr`, `lobsters`, `mastodon_links`, `mastodon_tags`, `npm`, `smithery`, `stackoverflow`, `wikipedia`

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
4. Anything with no match goes to **Other**. Keyword-free sources (`cloudflarestatus`, `coingecko_markets`, `coingecko_trending`, `euvd`, `githubstatus`, `jsdelivr`, `kev`, `launches`, `nvd`) use only the source rule, because vendor names or prices would trigger false matches.

| Industry | Scope | GitHub topics | Keywords (regex) |
| --- | --- | --- | --- |
| 🤖 AI & LLMs | Foundation models, inference, ML research and the labs behind them. | `ai`, `artificial-intelligence`, `computer-vision`, `deep-learning`, `generative-ai`, `large-language-models`, `llama`, `llm`, `llms`, `machine-learning`, `nlp`, `openai`, `pytorch`, `transformers` | <sub>`\b(ai\|a\.i\.\|artificial intelligence\|llms?\|gpt[-\w.]*\|chatgpt\|openai\|anthropic\|claude\|gemini\|llama\|qwen\|mistral\|deepseek\|transformers?\|diffusion\|inference\|fine-?tun\w*\|machine learning\|deep learning\|neural\|embeddings?\|rag\|vllm\|ollama\|pytorch\|tensorflow\|multimodal\|vision-language\|language models?\|reasoning model\|text-generation\|text-to-\w+\|image-text-to-text\|hugging ?face\|openvino\|copilot)\b`</sub> |
| 🧠 AI agents & MCP | Agent frameworks, skills, tool use and Model Context Protocol servers. | `agent-skills`, `agentic-ai`, `agents`, `ai-agent`, `ai-agents`, `autonomous-agents`, `claude-code`, `llm-agents`, `mcp`, `mcp-server`, `model-context-protocol` | <sub>`\b(agents?\|agentic\|mcp\|model context protocol\|agent skills?\|skills? (bundle\|library\|framework)\|claude code\|codex\|coding agents?\|autonomous agents?\|crewai\|langgraph\|autogen\|tool[- ]calling\|a2a\|computer[- ]use\|browser[- ]use\|sandbox(es\|ed)?)\b`</sub> |
| 🧰 Developer tools | Languages, editors, CLIs, package ecosystems and the software toolchain. | `cli`, `compiler`, `developer-tools`, `devtools`, `git`, `golang`, `neovim`, `programming-language`, `python`, `rust`, `terminal`, `typescript`, `vscode` | <sub>`\b(cli\|ide\|editor\|vs ?code\|vim\|neovim\|emacs\|plugins?\|sdk\|compiler\|debugg\w*\|linters?\|terminal\|git\|package manager\|npm\|pypi\|crates?\.io\|cargo\|rustc?\|golang\|python\|typescript\|javascript\|zig\|ruff\|deno\|bun\|node\.?js\|refactor\w*\|developers?\|devtools?\|programming\|open[- ]source)\b`</sub> |
| ☁️ Cloud & DevOps | Infrastructure, containers, CI/CD, self-hosting, outages and operations. | `aws`, `cloud`, `devops`, `docker`, `homelab`, `infrastructure`, `kubernetes`, `linux`, `observability`, `self-hosted`, `terraform` | <sub>`\b(devops\|kubernetes\|k8s\|docker\|containers?\|helm\|terraform\|ansible\|ci/?cd\|aws\|azure\|gcp\|google cloud\|cloud\|serverless\|nginx\|linux\|kernel\|self-host\w*\|homelab\|observability\|grafana\|prometheus\|sre\|outages?\|incident\|hetzner\|cloudflare\|data ?cent(er\|re)s?\|infrastructure)\b`</sub> |
| 🔒 Cybersecurity | Exploited and new vulnerabilities, attacks, defence and security tooling. | `ai-security`, `bug-bounty`, `ctf`, `cybersecurity`, `infosec`, `malware`, `osint`, `penetration-testing`, `pentesting`, `red-team`, `security`, `vulnerability` | <sub>`\b(security\|vulnerab\w*\|cve-\d+\|exploit\w*\|malware\|ransomware\|phishing\|breach\w*\|pentest\w*\|red[- ]team\|bug[- ]?bount\w*\|bug hunt\w*\|zero-day\|0-day\|backdoor\|cryptography\|authentication bypass\|xss\|rce\|privilege escalation\|supply[- ]chain attack\|cyber\w*\|infosec\|hackers?\|spyware\|botnet\|ddos)\b`</sub> |
| 📊 Data & analytics | Databases, datasets, pipelines, analytics and BI. | `analytics`, `big-data`, `data-engineering`, `data-science`, `database`, `dataset`, `etl`, `postgresql`, `sql`, `vector-database` | <sub>`\b(databases?\|postgres\w*\|sqlite\|mysql\|duckdb\|clickhouse\|polars\|pandas\|spark\|kafka\|airflow\|parquet\|iceberg\|etl\|data pipelines?\|datasets?\|data engineering\|vector (db\|database)\|analytics\|olap\|warehouse)\b`</sub> |
| 🌐 Web & frontend | Browsers, front-end frameworks, CSS, web platform and the CDN layer. | `css`, `frontend`, `javascript`, `nextjs`, `react`, `svelte`, `tailwindcss`, `vue`, `web`, `webassembly` | <sub>`\b(frontend\|front-end\|web apps?\|web development\|web framework\|web platform\|web standards?\|browsers?\|css\|html\|react\|next\.js\|nextjs\|vue\|svelte\|angular\|tailwind\|webassembly\|wasm\|chrome\|firefox\|safari\|webgpu)\b`</sub> |
| 📱 Mobile | iOS, Android, phones, wearables and app stores. | `android`, `flutter`, `ios`, `kotlin`, `mobile`, `react-native`, `swift`, `swiftui` | <sub>`\b(ios\|ipados\|android\|iphone\|ipad\|app store\|google play\|mobile\|react native\|flutter\|swiftui\|swift\|kotlin\|jetpack\|xcode\|testflight\|smartphones?\|samsung galaxy\|pixel \d+\|whatsapp\|apple watch\|wearables?)\b`</sub> |
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
| `gh_topic_robotics` | Robotics & hardware |
| `gh_topic_bioinformatics` | Health & biotech |
| `gh_topic_fintech` | Fintech & payments |
| `coingecko_trending`, `coingecko_markets` | Crypto & web3 |
| `biorxiv` | Health & biotech |
| `launches` | Space & mobility |

## What is never done

- No number is estimated, rounded up or filled in. A dash means the source gave none.
- No source that needs a key, a login, or scraping against its terms.
- The maintainer's own repos sit in their own labelled section and are never boosted.
