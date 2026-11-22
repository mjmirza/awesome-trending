# awesome-trending

**What moved in tech, AI and the markets since yesterday, in one page, every morning.** 179 public sources, 23 industries, stories ranked by how many outlets carry them, and every number linked to where it came from.

**Who it is for:** developers and maintainers, AI engineers and researchers, founders and product people, investors and analysts, security teams, and anyone who wants the day's tech and market news without opening forty tabs.

[![Last commit](https://img.shields.io/github/last-commit/mjmirza/awesome-trending)](https://github.com/mjmirza/awesome-trending/commits/main) [![License](https://img.shields.io/badge/License-OpenRoots_ORA_2.3-2ea44f)](LICENSE) [![Sources](https://img.shields.io/badge/sources_live_today-176%2F179-informational)](#sources) [![Industries](https://img.shields.io/badge/industries_with_items-23%2F23-blueviolet)](#map)

**22 November 2026** · snapshot at 08:12 Europe/Berlin (UTC+1) · 176/179 sources answered · 1176 distinct items today

**Read it in this order:** 30 seconds → what's shaking the market → since yesterday → top signals → month → AI labs → your industry. Everything else is folded.

**Start here:** Developers [signals](#signals) · [dev tools](#ind-devtools) · [month](#month) | AI [labs](#labs) · [media](#media) · [AI & LLMs](#ind-ai-llms) | Founders & investors [shaking](#shaking) · [markets](#ind-markets-economy) · [fintech](#ind-fintech) | Security [cybersecurity](#ind-cybersecurity) · [status](#status) | Markets [markets strip](#markets) · [crypto](#ind-crypto-web3)

**Follow it:** [RSS feed](https://raw.githubusercontent.com/mjmirza/awesome-trending/main/feeds/daily.xml) · [JSON](https://raw.githubusercontent.com/mjmirza/awesome-trending/main/feeds/daily.json) · or watch the repo for the daily commit.

[30 seconds](#today) · [Shaking](#shaking) · [Since yesterday](#since) · [Top signals](#signals) · [Month](#month) · [Week](#week) · [Year](#year) · [AI labs](#labs) · [AI media](#media) · [Industry map](#map) · [Industries](#industries) · [By source](#by-source) · [Status](#status) · [X](#x) · [Maintainer](#maintainer) · [Archive](#archive) · [Sources](#sources)

<a id="today"></a>

## Today in 30 seconds

- **Biggest story:** [Amazon Nearing $7.5 Billion Purchase of Decart](https://www.theinformation.com/briefings/amazon-nearing-7-5-billion-purchase-decart) — carried by 6 outlets (BigGo Finance, Livemint, https://ascendants.in/, 조선일보).
- **Most stars today:** [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) — A Claude Code skill bundle for bug hunting and external red-team work - 82 skills, 15 slash commands, 681… (+1,803 today, +12.3%).
- **On the most sources:** [Researcher plants 2m canaries into the AI supply chain. A…](https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/) — 3 sources (Lobsters, Ars Technica, Mastodon).
- **Top on Hacker News:** [Hurried Announcement: Alessandro Masullo GRH](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/) — 2,404 pts · 1,169 comments.
- **US markets (last close published on FRED):** S&P 500 7,175.83 (-2.02%, 2026-11-19), Nasdaq Composite 23,879.20 (-2.25%, 2026-11-19).
- **Most upvoted paper:** [WeVisForensics: Self-Evolving Agent for Omni AI-Generated Video…](https://huggingface.co/papers/2611.21373) — 54 upvotes.
- **Newest hosted model:** [Thinking Machines: Inkling 2 Mini](https://openrouter.ai/thinkingmachines/inkling-2-mini) — $0.075 in / $0.3 out per 1M · 1M ctx.
- **Exploited in the wild:** CISA added 4 on 2026-11-20 (Roller, VMware vCenter, NetWeaver, Expressway Series); 20 in 14 days.
- **Crypto:** [Bitcoin (BTC)](https://www.coingecko.com/en/coins/bitcoin) at $59,041.00 (+1.3% in 24 h, -8.4% in 7 d).
- **Next launch:** [Falcon 9 Block 5 \| NROL-136](https://ll.thespacedevs.com/2.2.0/launch/951a341f-236b-42fe-a667-4ab2fcf36eac/) — NET 22 Nov 13:23 · Go.

<a id="shaking"></a>

## What's shaking the market today

The biggest stories of the last 36 hours across tech, innovation and the economy, ranked by how many separate outlets and platforms carry the same story. Headlines are grouped when they share distinctive words and names ([method](docs/methodology.md#shaking)).

| # | Story | Why it matters | Outlets | Read it at | Industry | Latest |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [Amazon Nearing $7.5 Billion Purchase of Decart](https://www.theinformation.com/briefings/amazon-nearing-7-5-billion-purchase-decart) | Amazon is nearing a deal to buy Decart, an Israeli AI startup developing video models, for $7.5 billion, the Financial Times reported on… | **6** <sub>BigGo Finance, Livemint, https://ascendants.in/, 조선일보 +2</sub> | [BigGo Finance](https://news.google.com/rss/articles/CBMidkFVX3lxTE1jSUczV0Q5bWpYN2tEOVdJS2t2X0tPNlZxcW1DNnM4dVFUU21kTk1MNEE2UGR5WXBPYVd0QjBRSmNyUXp4TkV1b1R5eURwT0NGbzVDdUxOdGE2ay1PcW41SjFQSm12el83OS1pUWM1QnNCSWVhbGc?oc=5) · [Livemint](https://news.google.com/rss/articles/CBMi7gFBVV95cUxOSHZLSHVPQmpHOC1fSzZPN1UtSGRLTWpfenEtZDhsdm5MWE0yTmJydjFWTnA4TFNmR0lNZWw4QlgwcU4ycDFOY2czaDNEeXcwVXVzMjlwT05YSEhRd0tqM3hydW1LMjFaUkloSGtJZWxhRmpsWW15TGdad2l6M0RKS2VUREFWUXRnVVhRUmNQNzZpWTBBNnlISGVYVHAtcDZwamlvckhnUEVPOGVmTm9mVi1GQTl3alo4Q0lkcGV1ZEdDeGJKTEFGcHhsRnFINjNlaHgyRzNWY2ZvS3ItZkJocUVSX1BpN3B2a2lDd0NB0gHzAUFVX3lxTE9XNUxPUXkzcC1YSE90Z0VGZlpTTGtPTThua25OdWQ1RmlndkoybXZqSVNKRC1RNHRSNmJ3cHZoTkNQZHhON2kteEtjaTdVa0Q1d2ZiRkpaYmIwSzh6UVQwaVBPYzFfTmdKa2ZOb3gwZFJiaFItUUJKOEVVZEZUY1BxZjhGNmc0czRmdnU0aEpDeFozYUlSUkFjdW1SQnUwNnA2UncyZ3ZtOGUwZVVfUWVrYTdlSk9VTzE3TTJjNkd3Y2hqNkROTHpRWExXZUJfdWpwa1pHQTJuMXdfME1JVzRZVmlrRThqWGYxNkgxaG13eVhaUQ?oc=5) · [https://ascendants.in/](https://news.google.com/rss/articles/CBMingFBVV95cUxPVGlNaUlMd0NiXzFqbTB1WDNhMWFPNmU4c0JIbmFCNDE3a004NVUyUTFtSDlGS1lkQnRfZ0hscVhnNzVOOWpxZVVjS3lwTUt4MTdVdThWU2Fpc2FqUVJoWFJqM2NjVDVHOG1jOXNZeHpCSlRDV3NJYmdzSmlHUmQzeksya253TVVHbkVub0diOVEzUzQ1aTlUcDdFRVNrQQ?oc=5) | AI, Markets | 22 Nov 07:29 |
| 2 | [How Jensen Huang Made Humiliation Routine at Nvidia](https://www.nytimes.com/2026/11/20/technology/jensen-huang-nvidia-culture.html) | The Nvidia co-founder’s belittling behavior toward employees goes back decades. | **3** <sub>Techmeme, The New York Times, Financial Times</sub> | [The New York Times](https://news.google.com/rss/articles/CBMihAFBVV95cUxOV2xjNVlQNGJaN0dDY0FnLXZORHhwdG9nRlRaSU0zRHpSOXkzZ1VQQkNuQ0VaZzJ5ODc0blhmUFZzOVdRXzhLUmYtcUZMd2hOam1yWmxfMVpoZGpfaFJ2MXh6aTBUTF9UNGFJWksydE9SdWMzRWJCeGRqRHJnT0k0Y3I5ak0?oc=5) · [Financial Times](https://www.ft.com/content/f4a9e8ac-9ba2-40ac-8d27-8ce2b9639e2a?syn-25a6b1a6=1) · [Techmeme](https://www.techmeme.com/261121/p11#a261121p11) | AI, Chips | 22 Nov 08:09 |
| 3 | [A joint statement by the Lean and Mathlib communities says "we have full confidence that…](https://www.techmeme.com/261122/p3#a261122p3) | Lean community blog : A joint statement by the Lean and Mathlib communities says “we have full confidence that Alpöge's proof of the… | **3** <sub>Techmeme, Hacker News, The Information</sub> | [Hacker News](https://news.ycombinator.com/item?id=50590441) · [Techmeme](https://www.techmeme.com/261122/p3#a261122p3) · [The Information](https://www.theinformation.com/briefings/anthropic-mathematician-says-proved-riemann-hypothesis) | AI | 22 Nov 07:00 |
| 4 | [Sources: Alice Huang associate Li Ming, whom Singapore charged with fraud in 2025, was…](https://www.techmeme.com/261122/p1#a261122p1) | Stu Woo / Wall Street Journal : Sources: Alice Huang associate Li Ming, whom Singapore charged with fraud in 2025, was central to… | **3** <sub>Techmeme, Bloomberg, Financial Times</sub> | [Techmeme](https://www.techmeme.com/261122/p1#a261122p1) · [Bloomberg](https://www.bloomberg.com/news/newsletters/2026-11-21/new-us-ai-chip-rules-against-china-threaten-pain-for-southeast-asia) · [Financial Times](https://www.ft.com/content/f3ad8a81-3890-4a8a-8853-ff0a94b08ba9?syn-25a6b1a6=1) | AI, Markets | 22 Nov 06:45 |
| 5 | [Tech suppliers raise AI server prices up to 45% months after deals are signed](https://www.ft.com/content/dd2a6594-6146-4ff1-ac8e-54749c1fc99f?syn-25a6b1a6=1) | Dell, HPE, Lenovo and Supermicro demand more for equipment, with the increased costs hitting trading firms | **2** <sub>Techmeme, Financial Times</sub> | [Financial Times](https://www.ft.com/content/dd2a6594-6146-4ff1-ac8e-54749c1fc99f?syn-25a6b1a6=1) · [Techmeme](https://www.techmeme.com/261122/p2#a261122p2) | AI, Markets | 22 Nov 06:50 |
| 6 | [Meta ads is now available in AWS Quick](https://aws.amazon.com/blogs/machine-learning/meta-ads-is-now-available-in-aws-quick/) | AWS Quick now has a Meta ads AI connector. | **2** <sub>AWS Machine Learning blog, Amazon Web Services</sub> | [AWS Machine Learning…](https://aws.amazon.com/blogs/machine-learning/meta-ads-is-now-available-in-aws-quick/) · [Amazon Web Services](https://news.google.com/rss/articles/CBMijgFBVV95cUxNRkFtaHMtN1FWSllFbWladFBrVjJkNkRoaTZKTzNraF9taVZPaUxQRXdNMm5ER3Ftb3U3Yy11WU1fT21HS0ZNSFJReGR4ZVdnSTRuS205bmFkcmtzWjF5VVR0T3ExdWZVU2dNSXRmSF9zTkVoV0hCVEptc0VyQnZKYjNBOWxjenhMdEJfdHVB?oc=5) | AI, Cloud | 22 Nov 02:59 |
| 7 | [Signal restricts mobile screenshots as it confronts ‘existential threat’ of AI…](https://techcrunch.com/2026/11/21/signal-restricts-mobile-screenshots-as-it-confronts-existential-threat-of-ai-surveillance/) | Signal is limiting users' ability to take screenshots in both its Android and iOS apps. | **2** <sub>TechCrunch, Decrypt</sub> | [TechCrunch](https://techcrunch.com/2026/11/21/signal-restricts-mobile-screenshots-as-it-confronts-existential-threat-of-ai-surveillance/) · [Decrypt](https://decrypt.co/383750/signal-os-level-ai-existential-threat-blocks-screenshots) | AI, Mobile | 21 Nov 22:37 |
| 8 | [Crowdstrike’s Talks With Zscaler Show AI-Led Cyber Consolidation](https://www.bloomberg.com/news/articles/2026-11-21/crowdstrike-s-talks-with-zscaler-show-ai-led-cyber-consolidation) | A wave of multibillion-dollar takeovers is reshaping the cybersecurity industry as the biggest companies race to expand their defenses… | **2** <sub>Bloomberg, The Information</sub> | [Bloomberg](https://www.bloomberg.com/news/articles/2026-11-21/crowdstrike-s-talks-with-zscaler-show-ai-led-cyber-consolidation) · [The Information](https://www.theinformation.com/briefings/crowdstrike-talks-buy-zscaler) | AI, Security | 21 Nov 20:02 |
| 9 | [Trump says there could be a 'positive spin' from the latest FBI database hack](https://www.cnbc.com/2026/11/21/trump-fbi-database-hack.html) | This would make the second recent intrusion into the FBI system. | **2** <sub>CNBC, TechCrunch</sub> | [CNBC](https://www.cnbc.com/2026/11/21/trump-fbi-database-hack.html) · [TechCrunch](https://techcrunch.com/2026/11/21/trump-says-reported-fbi-database-hack-is-not-good/) | Data, Markets | 21 Nov 19:44 |
| 10 | [FBI reportedly hacked again, this time targeting nationwide police database](https://www.bleepingcomputer.com/news/security/fbi-reportedly-hacked-again-this-time-targeting-nationwide-police-database/) | FBI systems have reportedly been breached for the second time in two months, this time targeting the agency's National Crime Information… | **2** <sub>BleepingComputer, The Verge</sub> | [BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-reportedly-hacked-again-this-time-targeting-nationwide-police-database/) · [The Verge](https://www.theverge.com/tech/1039543/fbi-usda-hacked) | Security, Data | 21 Nov 18:42 |

<a id="markets"></a>

**Markets strip**

| Indicator | Level | Change | As of | Source |
| --- | --- | --- | --- | --- |
| [S&P 500](https://fred.stlouisfed.org/series/SP500) | 7,175.83 | -2.02% | 2026-11-19 <sub>vs 2026-11-18</sub> | FRED |
| [Nasdaq Composite](https://fred.stlouisfed.org/series/NASDAQCOM) | 23,879.20 | -2.25% | 2026-11-19 <sub>vs 2026-11-18</sub> | FRED |
| [Dow Jones Industrial Average](https://fred.stlouisfed.org/series/DJIA) | 48,147.33 | -1.93% | 2026-11-20 <sub>vs 2026-11-19</sub> | FRED |
| [VIX volatility index](https://fred.stlouisfed.org/series/VIXCLS) | 28.44 | +15.80% | 2026-11-19 <sub>vs 2026-11-18</sub> | FRED |
| [US 10-year Treasury yield](https://fred.stlouisfed.org/series/DGS10) | 5.04% | -3 bp | 2026-11-19 <sub>vs 2026-11-18</sub> | FRED |
| [Brent crude oil](https://fred.stlouisfed.org/series/DCOILBRENTEU) | 92.94 | +0.04% | 2026-11-17 <sub>vs 2026-11-16</sub> | FRED |
| [EUR/USD (ECB reference rate)](https://data.ecb.europa.eu/data/datasets/EXR) | 1.0990 | -0.02% | 2026-11-20 <sub>vs 2026-11-19</sub> | ECB |
| [Bitcoin (BTC)](https://www.coingecko.com/en/coins/bitcoin) | $59,041.00 | +1.3% | 22 Nov 08:12 <sub>live, 24 h change</sub> | CoinGecko |
| [Ethereum (ETH)](https://www.coingecko.com/en/coins/ethereum) | $1,659.37 | +1.5% | 22 Nov 08:12 <sub>live, 24 h change</sub> | CoinGecko |

<sub>Index levels, the 10-year yield and Brent are the latest values FRED has published (US closes, one or more days old). EUR/USD is the ECB's daily reference rate. Changes compare the last two published values. DAX, gold and single stocks (NVDA, MSFT, AAPL, GOOGL, AMZN, META, TSLA, TSM) are not shown: no keyless source that allows this kind of reuse was found.</sub>

<a id="since"></a>

## Since yesterday

Compared with the archive for **21 November 2026**: **73** ranked items are new today, **668** were already listed.

**New and highest-scoring**

| # | Item | Type | Why it matters | Key metric | Score | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [My monitor was cutting my download speed by 75%](https://blog.tymscar.com/posts/studiodisplayethernet/) | Discussions | Link to blog.tymscar.com | 555 pts · 265 comments | 73 | [Hacker News](https://news.ycombinator.com/) |
| 2 | [Show HN: Zero C# – C# without a runtime or GC](https://onurgumus.github.io/zero-csharp/index.html) | Discussions | Link to onurgumus.github.io | 151 pts · 104 comments | 60 | [Hacker News](https://news.ycombinator.com/) |
| 3 | [Does anybody read their emails anymore?](https://news.ycombinator.com/item?id=50591050) | Discussions | Discussion thread on HN | 5 pts · 14 comments | 60 | [Hacker News](https://news.ycombinator.com/ask) |
| 4 | [The Chairs Are Back. The Coffee Is On. ](https://dev.to/thethirdcup/the-chairs-are-back-the-coffee-is-on-243p) | Posts | #community, #discuss, #ai | 94 reactions · 38 comments | 60 | [Dev.to](https://dev.to/top/day) |
| 5 | [Is it significant to use size_t in place of int?](https://stackoverflow.com/questions/80018068/is-it-significant-to-use-size-t-in-place-of-int) | Questions | #c++ | -1 score · 0 answers · 19 views | 60 | [Stack Overflow](https://stackoverflow.com/questions?tab=Hot) |

**[Today](#today) · [Week](#week) · [Month](#month) · [Year](#year)**

<a id="signals"></a>

## Top signals today

One score for everything: how high an item ranks in its own source, plus how many separate sources list it.

| # | Item | Type | Why it matters | Key metric | Momentum | Seen on | Industry | Score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Researcher plants 2m canaries into the AI supply chain. A…](https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/) | Posts | #ai, #security | 11 score · 3 comments | — | **3** <sub>Lobsters, Ars Technica, Mastodon</sub> | AI, Security +1 | **77** |
| 2 | [My monitor was cutting my download speed by 75%](https://blog.tymscar.com/posts/studiodisplayethernet/) | Discussions | Link to blog.tymscar.com | 555 pts · 265 comments | 27 pts/h | **2** <sub>Hacker News, Lobsters</sub> | Other | **73** |
| 3 | [Pill to treat pancreatic cancer hailed as 'biggest…](https://www.theguardian.com/society/2026/nov/20/pill-pancreatic-cancer-breakthrough-daraxonrasib) | Discussions | Link to theguardian.com | 884 pts · 203 comments | 26 pts/h | **2** <sub>Hacker News, Mastodon</sub> | Health | **68** |
| 4 | [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | Repositories | A Claude Code skill bundle for bug hunting and external red-team work - 82 skills, 15 slash commands, 681… | 16.4k stars · +1,803 today | +12.3% | 1 | AI, Agents +2 | **60** |
| 5 | [cursor/plugins](https://github.com/cursor/plugins) | Repositories | Cursor plugin specification and official plugins | 18.2k stars · +260 today | +1.5% | 1 | Dev tools | **60** |
| 6 | [janhq/jan](https://github.com/janhq/jan) | Repositories | Jan is an open source alternative to ChatGPT that runs 100% offline on your computer. | 46k stars · +45 today | +0.1% | 1 | AI, Dev tools +1 | **60** |
| 7 | [datazip-inc/olake-go](https://github.com/datazip-inc/olake-go) | Repositories | OLake Go: open-source replication from databases, Kafka and S3 to Apache Iceberg and Parquet. | 2.2k stars · +93 today | +4.4% | 1 | Dev tools, Data | **60** |
| 8 | [Hurried Announcement: Alessandro Masullo GRH](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/) | Discussions | Link to math216.wordpress.com | 2,404 pts · 1,169 comments | 66 pts/h | 1 | Other | **60** |
| 9 | [Show HN: Zero C# – C# without a runtime or GC](https://onurgumus.github.io/zero-csharp/index.html) | Discussions | Link to onurgumus.github.io | 151 pts · 104 comments | 10 pts/h | 1 | Other | **60** |
| 10 | [Does anybody read their emails anymore?](https://news.ycombinator.com/item?id=50591050) | Discussions | Discussion thread on HN | 5 pts · 14 comments | 0 pts/h | 1 | Other | **60** |

<details>
<summary>Show 5 more</summary>

| # | Item | Type | Why it matters | Key metric | Momentum | Seen on | Industry | Score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini) | Models | image-text-to-text · transformers | 3,301 likes · 7.9k dl/30d | — | 1 | AI | **60** |
| 12 | [huggingface/moe-blogpost](https://huggingface.co/spaces/huggingface/moe-blogpost) | Demos (Spaces) | A hands-on guide to training Mixture-of-Experts models | 812 likes | — | 1 | AI | **60** |
| 13 | [Vyber07/cyber-security](https://huggingface.co/datasets/Vyber07/cyber-security) | Datasets | Cybersecurity AI Knowledge Base — PhD-Level Dataset Overview This is the most… | 1,380 likes · 28.7k dl/30d | — | 1 | AI, Security +2 | **60** |
| 14 | [WeVisForensics: Self-Evolving Agent for Omni AI-Generated…](https://huggingface.co/papers/2611.21373) | Papers | Recent advances in video generation call for reliable detection grounded in explicit forensic evidence. | 54 upvotes | — | 1 | AI, Agents +1 | **60** |
| 15 | [Brave Search](https://smithery.ai/server/brave) | MCP servers | Search the web with Brave's independent index — web, news, images, and videos. | 87,579 uses | — | 1 | Agents | **60** |

</details>

<sub>Score = 100 × (0.6 × best rank percentile + 0.4 × extra sources ÷ 3, capped). [How the score works](docs/methodology.md#score).</sub>

<a id="month"></a>

## This month

Native month lists from GitHub, Hacker News, Dev.to and Hugging Face papers, scored together. Archive history in this window: 4 of 30 days. [Full month list →](windows/month.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | Repositories | Anti-AI-slop design skill for Claude Code, Cursor, and Codex. | 59.2k stars · +28,684 this month | 1 | 60 | [GitHub trending](https://github.com/trending?since=monthly) |
| 2 | [storytold/craft-anything](https://github.com/storytold/craft-anything) | Repositories | Craft Anything: understand how any software works, and craft your own. | 40.6k stars · created 31 Oct | 1 | 60 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 3 | [Jensen Huang resigns](https://apnews.com/article/nvidia-megaspeed-china-singapore-huang-5403f152a601cf82ce939f1d24fffa0f) | Discussions | Link to apnews.com | 4,060 pts · 3,493 comments | 1 | 60 | [Hacker News](https://news.ycombinator.com/best) |
| 4 | [We're Building AI to Replace Ourselves. What's the Plan?](https://dev.to/sylwia-lask/were-building-ai-to-replace-ourselves-whats-the-plan-4oll) | Posts | #discuss, #ai | 238 reactions · 219 comments | 1 | 60 | [Dev.to](https://dev.to/top/month) |
| 5 | [TeleChat to Xing4: Advancing Frontier Agentic Models on Domestic…](https://huggingface.co/papers/2611.22115) | Papers | We present Xing 4, a series of large language models that extends the TeleChat lineage through coordinated… | 167 upvotes | 1 | 60 | [Hugging Face](https://huggingface.co/papers) |
| 6 | [ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go) | Repositories | dsh-go — DeepSeek Harness 装进口袋：手机本机运行，也能遥控你的电脑。 | 29.8k stars · created 25 Oct | 1 | 58 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 7 | [Patrick Stewart has died](https://www.nytimes.com/2026/10/29/arts/television/patrick-stewart-dead.html) | Discussions | Link to nytimes.com | 3,314 pts · 769 comments | 1 | 57 | [Hacker News](https://news.ycombinator.com/best) |
| 8 | [Jeveration: System One Models Now Generate](https://huggingface.co/papers/2611.24738) | Papers | System One models such as Jev return decisions through fast, parallel prediction. | 149 upvotes | 1 | 57 | [Hugging Face](https://huggingface.co/papers) |
| 9 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | Repositories | A coding-agent skill for multi-phase security audits with independently verified, machine-readable findings | 76.8k stars · +41,810 this month | 1 | 56 | [GitHub trending](https://github.com/trending?since=monthly) |
| 10 | [Your DEV posts have a beautiful new share card ](https://dev.to/devteam/your-dev-posts-have-a-beautiful-new-share-card-4be8) | Posts | #devto, #showdev, #opensource | 176 reactions · 36 comments | 1 | 56 | [Dev.to](https://dev.to/top/month) |

<details>
<summary>Show 10 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | [deepseek-ai/dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) | Repositories | Towards a More Autonomous Agent System | 24.2k stars · created 31 Oct | 1 | 55 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 12 | [sshole](https://sshhole.com) | Discussions | Link to sshhole.com | 3,007 pts · 751 comments | 1 | 54 | [Hacker News](https://news.ycombinator.com/best) |
| 13 | [Gamer: A Generalist Vision-Language-Action Foundation Model for…](https://huggingface.co/papers/2611.18397) | Papers | We introduce Gamer, a generalist agent framework built for long-horizon tasks in complex interactive… | 148 upvotes | 1 | 54 | [Hugging Face](https://huggingface.co/papers) |
| 14 | [milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) | Repositories | Open-source Grok Bot alternative with a virtual machine that bots can use | 26.6k stars · +21,249 this month | 1 | 53 | [GitHub trending](https://github.com/trending?since=monthly) |
| 15 | [heydamir/unslop](https://github.com/heydamir/unslop) | Repositories | A Claude skill that turns vibecoded, AI-looking UI into a designed interface | 19.9k stars · created 29 Oct | 1 | 53 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 16 | [Is Coding with AI Actually Faster and Cheaper?](https://dev.to/sylwia-lask/is-coding-with-ai-actually-faster-and-cheaper-2810) | Posts | #ai, #programming, #productivity | 231 reactions · 196 comments | 1 | 52 | [Dev.to](https://dev.to/top/month) |
| 17 | [Astra can read and write weights to improve Qwen](https://rikiyat.github.io/blog/weight-space-programming/) | Discussions | Link to rikiyat.github.io | 2,971 pts · 902 comments | 1 | 51 | [Hacker News](https://news.ycombinator.com/best) |
| 18 | [Advances in Agentic Computer Graphics](https://huggingface.co/papers/2611.01860) | Papers | Computer graphics is built on code. | 148 upvotes | 1 | 51 | [Hugging Face](https://huggingface.co/papers) |
| 19 | [anefzaoui/misterdownloadmanager](https://github.com/anefzaoui/misterdownloadmanager) | Repositories | misterdownloadmanager: The ultimate open-source, clean-room download manager written from scratch in pure… | 16k stars · created 29 Oct | 1 | 50 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 20 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | Repositories | The best way to control Claude Code, Codex and more from any computer or phone | 70.1k stars · +40,025 this month | 1 | 49 | [GitHub trending](https://github.com/trending?since=monthly) |

</details>

<a id="week"></a>

## This week

Native week lists from GitHub, Hacker News, Dev.to and Hugging Face papers, scored together. Archive history in this window: 4 of 7 days. [Full week list →](windows/week.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | Repositories | The workspace to stay in the loop and on top of agents - shape, decide, plan, annotate, review code, share… | 14.2k stars · +3,396 this week | 1 | 60 | [GitHub trending](https://github.com/trending?since=weekly) |
| 2 | [ItsNotRexed/Leonida](https://github.com/ItsNotRexed/Leonida) | Repositories | Leonida Is A Native PC Recompilation Of The Xbox Version Of Grand Theft Auto 6 | 7.7k stars · created 20 Nov | 1 | 60 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 3 | [Levent Alpöge claims proof of the Generalized Riemann Hypothesis \[pdf\]](https://alpo.ge/remark.pdf) | Discussions | Link to alpo.ge | 2,868 pts · 2,049 comments | 1 | 60 | [Hacker News](https://news.ycombinator.com/best) |
| 4 | [Is Coding with AI Actually Faster and Cheaper?](https://dev.to/sylwia-lask/is-coding-with-ai-actually-faster-and-cheaper-2810) | Posts | #ai, #programming, #productivity | 231 reactions · 196 comments | 1 | 60 | [Dev.to](https://dev.to/top/week) |
| 5 | [TeleChat to Xing4: Advancing Frontier Agentic Models on Domestic…](https://huggingface.co/papers/2611.22115) | Papers | We present Xing 4, a series of large language models that extends the TeleChat lineage through coordinated… | 167 upvotes | 1 | 60 | [Hugging Face](https://huggingface.co/papers) |
| 6 | [erkamyaman/rust-anything](https://github.com/erkamyaman/rust-anything) | Repositories | Rewrite your whole app in Rust, one piece at a time, checked against the original's recorded behavior at… | 7.6k stars · created 16 Nov | 1 | 58 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 7 | [krisgfx9/Wireless-Device-Battery-Monitor](https://github.com/krisgfx9/Wireless-Device-Battery-Monitor) | Repositories | Show the battery level of wireless mice, headsets, keyboards and controllers on the Windows 10/11 taskbar. | 5.9k stars · created 16 Nov | 1 | 57 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 8 | [Jeveration: System One Models Now Generate](https://huggingface.co/papers/2611.24738) | Papers | System One models such as Jev return decisions through fast, parallel prediction. | 149 upvotes | 1 | 57 | [Hugging Face](https://huggingface.co/papers) |
| 9 | [bookwjitchieni1986/blender-ai-mcp-addon](https://github.com/bookwjitchieni1986/blender-ai-mcp-addon) | Repositories | AI assistant and MCP server for Blender: visual chat, scene tools, multi-agent workflows. | 2.7k stars · created 19 Nov | 1 | 56 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 10 | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Repositories | A library of Agent Skills designed to work with the Stitch MCP server. | 11.6k stars · +2,431 this week | 1 | 55 | [GitHub trending](https://github.com/trending?since=weekly) |

<details>
<summary>Show 5 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | [iamajmeena/neonclipping](https://github.com/iamajmeena/neonclipping) | Repositories | Paste a link, get captioned 9:16 clips in ~2 min. | 1.8k stars · created 19 Nov | 1 | 54 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 12 | [Hurried Announcement: Alessandro Masullo GRH](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/) | Discussions | Link to math216.wordpress.com | 2,405 pts · 1,169 comments | 1 | 54 | [Hacker News](https://news.ycombinator.com/best) |
| 13 | [The CodeNewbie Podcast is Back for Season 28!](https://dev.to/codenewbie/the-codenewbie-podcast-is-back-for-season-28-2484) | Posts | #codenewbie, #ai, #podcast | 88 reactions · 12 comments | 1 | 54 | [Dev.to](https://dev.to/top/week) |
| 14 | [Gamer: A Generalist Vision-Language-Action Foundation Model for…](https://huggingface.co/papers/2611.18397) | Papers | We introduce Gamer, a generalist agent framework built for long-horizon tasks in complex interactive… | 148 upvotes | 1 | 54 | [Hugging Face](https://huggingface.co/papers) |
| 15 | [sybil-solutions/inference-optimisation-skill](https://github.com/sybil-solutions/inference-optimisation-skill) | Repositories | Agent skill for hill-climbing local LLM serving speed (decode, speculative decoding, prefill, KV, startup… | 1.8k stars · created 16 Nov | 1 | 52 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |

</details>

<a id="year"></a>

## This year

Native year lists from GitHub, Hacker News, Dev.to and Hugging Face papers, scored together. Archive history in this window: 4 of 365 days. [Full year list →](windows/year.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [morluto/rea](https://github.com/morluto/rea) | Repositories | Reverse engineer anything with agents, from app behavior down to native binaries. | 473.1k stars · created 14 Apr | 1 | 60 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 2 | [Don't post generated/AI-edited comments. HN is for conversation…](https://news.ycombinator.com/newsguidelines.html#generated) | Discussions | Discussion thread on HN | 4,229 pts · 1,668 comments | 1 | 60 | [Hacker News](https://news.ycombinator.com/best) |
| 3 | [A New Chapter: DEV is Joining Forces with Major League Hacking (MLH)](https://dev.to/devteam/a-new-chapter-dev-is-joining-forces-with-major-league-hacking-mlh-3kfd) | Posts | #news, #devto, #hackathon | 449 reactions · 125 comments | 1 | 60 | [Dev.to](https://dev.to/top/year) |
| 4 | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Repositories | Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. | 151.7k stars · created 3 Apr | 1 | 58 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 5 | [Jensen Huang resigns](https://apnews.com/article/nvidia-megaspeed-china-singapore-huang-5403f152a601cf82ce939f1d24fffa0f) | Discussions | Link to apnews.com | 4,060 pts · 3,493 comments | 1 | 57 | [Hacker News](https://news.ycombinator.com/best) |
| 6 | [How to Become a Tech Conference Speaker (And Why You Might Regret It)](https://dev.to/sylwia-lask/how-to-become-a-tech-conference-speaker-and-why-you-might-regret-it-2ink) | Posts | #career, #speaking, #techtalks | 231 reactions · 120 comments | 1 | 56 | [Dev.to](https://dev.to/top/year) |
| 7 | [tt-a1i/archify](https://github.com/tt-a1i/archify) | Repositories | Turn any idea, plan, or codebase into a beautiful interactive diagram. | 98.6k stars · created 15 Apr | 1 | 55 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 8 | [Ghostty is leaving GitHub](https://mitchellh.com/writing/ghostty-leaving-github) | Discussions | Link to mitchellh.com | 3,521 pts · 1,051 comments | 1 | 54 | [Hacker News](https://news.ycombinator.com/best) |
| 9 | [koala73/worldmonitor](https://github.com/koala73/worldmonitor) | Repositories | Real-time global intelligence dashboard. | 91k stars · created 8 Jan | 1 | 53 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 10 | [We're Building AI to Replace Ourselves. What's the Plan?](https://dev.to/sylwia-lask/were-building-ai-to-replace-ourselves-whats-the-plan-4oll) | Posts | #discuss, #ai | 238 reactions · 219 comments | 1 | 52 | [Dev.to](https://dev.to/top/year) |

<details>
<summary>Show 5 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | [Show HN: Gemini Pro 3 imagines the HN front page 10 years from now](https://dosaygo-studio.github.io/hn-front-page-2035/news) | Discussions | Link to dosaygo-studio.github.io | 3,346 pts · 965 comments | 1 | 51 | [Hacker News](https://news.ycombinator.com/best) |
| 12 | [blader/humanizer](https://github.com/blader/humanizer) | Repositories | Agent skill that removes signs of AI-generated writing from text | 72.1k stars · created 18 Jan | 1 | 50 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 13 | [Niko1221/Strata](https://github.com/Niko1221/Strata) | Repositories | Qwen3.8-Flash-Next on any consumer hardware: one-click install for Windows / Linux. | 46.6k stars · created 24 Sep | 1 | 48 | [GitHub](https://docs.github.com/en/rest/search/search#search-repositories) |
| 14 | [Patrick Stewart has died](https://www.nytimes.com/2026/10/29/arts/television/patrick-stewart-dead.html) | Discussions | Link to nytimes.com | 3,314 pts · 769 comments | 1 | 48 | [Hacker News](https://news.ycombinator.com/best) |
| 15 | [Join our April Fools Challenge for a chance at TEA-RRIFIC prizes!!!](https://dev.to/devteam/join-our-april-fools-challenge-for-a-chance-at-tea-rrific-prizes-1ofa) | Posts | #devchallenge, #418challenge, #jokes | 331 reactions · 94 comments | 1 | 48 | [Dev.to](https://dev.to/top/year) |

</details>

<a id="labs"></a>

## AI labs & big players

One row per lab. Click a lab for its announcements, models, SDK releases, incidents and leaderboard positions ([full page](labs/README.md)).

| Lab | Headlines + official posts | Latest | Newest model | Latest SDK release | Incidents 72 h | Best on LMArena text |
| --- | --- | --- | --- | --- | --- | --- |
| [Anthropic](labs/README.md#lab-anthropic) | 8 + 8 | [Ross Gerber Urges Patience on Anthropic Stock - Anthropic (NASDAQ:ANT)](https://news.google.com/rss/articles/CBMitwFBVV95cUxOLTF6X0Z0VmU4eFBNWGh4NlhDX2VzODFSNXZtZVJHWEZ3NTI0ejYzamFWNDZSV240ZHhIVDhKdEVGakVpYUYxWFA4d19KYkZfQmM3RVBJR1hUajZpQTdLY1BaQ0Q0b29BYm5YUzd4RmhqdXVCRzBUQnIwa1FxNm1LeWgySWM5Q05rd2wzcVpYSWZWdU4zME9zMzRvMHZXQmlXU1RJWi1ab0lMNGN0VWNmcnVIQzFWaE0?oc=5) <sub>Benzinga · 22 Nov 08:07</sub> | [Anthropic: Claude Fable 5.2](https://openrouter.ai/anthropic/claude-fable-5.2) <sub>9 Nov 20:49</sub> | [v2.1.330](https://github.com/anthropics/claude-code/releases/tag/v2.1.330) <sub>claude-code · 20 Nov 23:32</sub> | **1** | — |
| [OpenAI](labs/README.md#lab-openai) | 8 + 4 | [OpenAI patent describes earbuds that read silently mouthed words](https://news.google.com/rss/articles/CBMiigFBVV95cUxNNWZEUUhPZjkyS1BRWllRRHc2UnV0eXNsT1FkOUc5V0NuZXN5OXkxTDlPNFh2QjhnQlQ2MlRqV211U3BQRnVjZEtneTlhdDVBMEZLZEdqdjJ0YUdpWEhIOFZiT0UzRUVqMWd0YUFWY1RhaUo3UkQ0QUZrQkRLdVUzdzRGVXN1a2NycVE?oc=5) <sub>PPC Land · 22 Nov 07:55</sub> | [OpenAI: GPT-6.2 Astra Pro](https://openrouter.ai/openai/gpt-6.2-astra-pro) <sub>17 Nov 19:00</sub> | [0.173.0-alpha.4](https://github.com/openai/codex/releases/tag/rust-v0.173.0-alpha.4) <sub>codex · 21 Nov 01:40</sub> | **1** | — |
| [Google DeepMind & Gemini](labs/README.md#lab-google) | 8 + 11 | [GTA 6-style AI photos flood Instagram: Gemini and ChatGPT prompts to…](https://news.google.com/rss/articles/CBMimAJBVV95cUxQeWRZMUZzbWU3bmZEQ09fVk9HcWZYT1NOQWE2QnFMNkxybEpELWhNak5BcDRFVF8tZ2RhTXBOaDZNaUZQSUpNTVRMVEFNSFVjUU1PNE96Zi1aVmdiZWUwVEl5MkREeGV3RVpaNnd5NU1QcFV1dWI1SUQ4cWRfX2NMM3phdVlVcU9yekFIX05NN0h2NjdlbzNkZzAybUdUSUoxeWJ6ZnA4eUVmVERkV2ZHbU1UZm5aUjY4TFI3Z19WNkQwYjhUTnBtcFpNUXpKY3pRUDhwVGhIcEJZOVFfMU1rVmpCRnU1b0RSNEdzMEpRUlg2LWh0YXZUcC1FdzZPOG9Dbk9ySXBMVkZDcUxHRVA3ampTYVY3NW1L0gGeAkFVX3lxTE5udGx1TmVwdmc3VURObV9xM2VfSVhTa194ZkxWRkNuVENHeF9LdXFfWnVWNk12bHQ0dHMyRllHWEFoaVJNclplcVpINEEwMDZId3ctR3U3Z01fNFBjUGEyc2JGbTFQd0UzcnhfdXBqTXZxLTJNelJGUGk4ek1VVWM0UWtNZXlfUm84LWtYYlpXQXZUWHdCOGMxOUFMNnJQNzRsaUU3V2I0RkNuZktzSVctT1RRTTdXWkJPTGF1WWlNTnNTY0d5dTJCSG1OUVh3QVE2LVQ4RERSLWFyUlhfLWszUmpaSXF3dWFrZFo4Z3JHTHQwamUyazBjMnNnT3FfU3Y4ZUNOUlk2T0l5dmR5SHBzTnhpXzZXTm5ZWGRaNUE?oc=5) <sub>The Times of India · 22 Nov 06:47</sub> | [Google: Gemini 4 Neon](https://openrouter.ai/google/gemini-4-neon) <sub>18 Nov 14:02</sub> | [Release…](https://github.com/google-gemini/gemini-cli/releases/tag/v0.71.0-nightly.20261122.geecccfcd5) <sub>gemini-cli · 22 Nov 02:20</sub> | — | — |
| [Meta AI](labs/README.md#lab-meta) | 8 + 0 | [Meta AI Chief Mocks Apple Over Rumored Agent](https://news.google.com/rss/articles/CBMihwFBVV95cUxNUDBRUU9Yd0YzaFhwUjJKQ1UyR3NndWZoSE1DNVhIalVscnN2VTZwZ2t5V0xybVlBNW0tdnRPZVdpMHhnLVFDdHhNT2x3SUNHWlE3SFJsREdRU3NTcU9XWU44VGEtMmxhUlZYdFVTVWg0Ymw2emxURHZNUWxRaXBVVWJkN3ZjMEE?oc=5) <sub>Wisevoter · 22 Nov 07:10</sub> | [facebook/meta-encoder-v1](https://huggingface.co/facebook/meta-encoder-v1) <sub>12 Nov 03:00</sub> | — | — | — |
| [Microsoft AI](labs/README.md#lab-microsoft) | 8 + 1 | [As NASA's Voyager 1 reaches one light-day from Earth, Microsoft AI…](https://news.google.com/rss/articles/CBMitAJBVV95cUxPVFRZQzloamJkRE40M2pJREVaeHlxbC10ejRFcXZkWFU1Sk1aY2ltWVppRnJrb0Njek9TRlVVa21WdFpORTZwdDV2aVcwLUJyNml6NVlJenBLeXcyWk9zYThseU9xa0d0b1J6amV5cmFzV0lUY3F3RzVHWm1ib3RkUkhUTDdxVFlHbTFnb0xJT0M1dGhqYVlzMHJJdmt4TkstZXcyWmV2YmVVdU1fZk9VaFl3RWJUbFhVX3R4S09uMW1lWGtINXEzcjE4NndIWGstcnVndERBM2M5MjUybWZoaS1HUTVrd1NjMXpuQXhpbXJCd1FXUlZENm42NnZpbUVWRFFZQnNDNmFfYjBPY19VMnZiaGxyX1RmS1JEZDdEcVZvZVZ0MG0yQTdfVFp0X09lTnE2edIBugJBVV95cUxQTUNKVlFja3M0cmVqY3ZWSXlXVnZac0swMlJ4SDhrcFBkR1lOTVJlMFlHczJtMzRsYnVYSnJwdWVLczdPaXowRTdDMS1JOVp6QzVGb2h0ZzRlVGZNY1g2LU55LWpXcFQ4S3BIRVBSSWJ4OENleVBOZnN0c3ZZZDlCbkM3ZFpWLWhROFd3UlJvRm5OeWl2U3NCcm1JOEs3WGU5LUJKMmVTWnV1cllqZVV3MFZqM2lxV3hlMG9ZVUlaODhFVV80RTI3d1JhQ202SjlLX0tibGlfUFgwLTVNQWZ3MFNlTjNEMnlTR2FvbDNsMXltazZTSmtFaXBvQlJrdENJQ21ONEtockxkSG9GMnBpN1ZBdUdLSjJmMFdOWDlmSlU5VEdXX0VyNTJ5WXJCZkdsUXJ3Y2YxOVVodw?oc=5) <sub>The Times of India · 22 Nov 04:09</sub> | [microsoft/Aion-1.0-Instruct-2.3B-ONNX-W…](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B-ONNX-WebGPU) <sub>18 Nov 18:08</sub> | — | — | — |
| [xAI](labs/README.md#lab-xai) | 8 + 0 | [Elon Musk’s AI ‘Grok’ Officially Arrives on iPhone CarPlay](https://news.google.com/rss/articles/CBMiqgFBVV95cUxOaURsZWl5cHZETElmRVBZams2dlpFNEZ4SjlWMm1BR1A4VktqZVVYS0ZVU01xRWQxengzQzNUV1diMlNIRlZPTGFIeHZjUzhIaUZtRWh1cTNTWmhsdWpIUVZob2x4aHB3UDRDUTVURUstY0NRdG96LXBudmNHWkVlTmhrWWI4S29rRkY0UGhzV1d0eFhoMGVaRUpQNUF2d1lLMkpvODJPOXNDQQ?oc=5) <sub>آي-فون إسلام · 21 Nov 09:36</sub> | — | — | — | — |
| [Mistral AI](labs/README.md#lab-mistral) | 8 + 0 | [Deutsche Telekom stock backs Mistral AI partnership with T.Capital](https://news.google.com/rss/articles/CBMiyAFBVV95cUxQWE51S0ZBMThLbkZEa0NFaHVWUmdla011N2U0UkM3LVZha1UybVpGTEVRMW5wZGJwb0oxVTV3dzNneXc5bGZqVWlxLV9SbndkS2JfaGZCTGw1aHQ5VFhmdUhmODRJYXNmTEtBYlFSa0Nrc0ZDcFlkUkhIN0FsVlR0NHpESHJhdk5vejM3Z005SkViQm14ZVgzSHNuOWhqTW1zY1p0dDloNFc2ZGh4dnloRXpCWFRRQUhET0F5RlpqVWduQzR5eU10Nw?oc=5) <sub>ad-hoc-news.de · 21 Nov 11:56</sub> | [Mistral: Pixtral Large 2502](https://openrouter.ai/mistralai/pixtral-large-2502) <sub>20 Nov 01:51</sub> | — | **1** | — |
| [Cohere](labs/README.md#lab-cohere) | 3 + 0 | [Pichette tells committee his blind trust is not yet in place amid…](https://news.google.com/rss/articles/CBMivgFBVV95cUxPNVNBZmtXUlItT2N0NVUwamFLclVWQWhkN2ZzbVNUdlBvQkhLMEJYNC02Zkh6RWg3akFRZ2JWcGtrSVU5bFctX2lJdUxUNnBmODFKVWkzdWlkMEY5VkFScUtCN0NlblVQNGtpVVhPT3h2SUxtSmk1NFFxdF9qUHR4aXZCVHZKVm1EV3czWFZRUGdlVTNnZDlWRVRTekFIRUtyNzZYTW1DdUU3TE9ncjNiRFdZdUdfdm5jb2FmdzdR?oc=5) <sub>The Hub \| More Signal. Less Noise. · 21 Nov 12:00</sub> | — | [7.3.3](https://github.com/cohere-ai/cohere-python/releases/tag/7.3.3) <sub>cohere-python · 19 Nov 16:50</sub> | 0 | — |
| [NVIDIA](labs/README.md#lab-nvidia) | 8 + 5 | [How Jensen Huang Made Humiliation Routine at Nvidia](https://news.google.com/rss/articles/CBMihAFBVV95cUxOV2xjNVlQNGJaN0dDY0FnLXZORHhwdG9nRlRaSU0zRHpSOXkzZ1VQQkNuQ0VaZzJ5ODc0blhmUFZzOVdRXzhLUmYtcUZMd2hOam1yWmxfMVpoZGpfaFJ2MXh6aTBUTF9UNGFJWksydE9SdWMzRWJCeGRqRHJnT0k0Y3I5ak0?oc=5) <sub>The New York Times · 22 Nov 08:09</sub> | [nvidia/Llama-3.2-1B-Qwen3.8-27B-Draft](https://huggingface.co/nvidia/Llama-3.2-1B-Qwen3.8-27B-Draft) <sub>11 Nov 21:26</sub> | [v1.3.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0) <sub>TensorRT-LLM · 20 Nov 03:45</sub> | — | — |
| [Amazon & AWS](labs/README.md#lab-amazon) | 8 + 5 | [Amazon to Acquire Israeli AI Startup Decart for $7.5 Billion](https://news.google.com/rss/articles/CBMiiAFBVV95cUxOeTlfTHFQZjVqbmhvOGYwWGN6RThtLXhSZlR2bzRTM21NZXpvTU16cUNBYUN2aGRXMllJczZXaXl3TWNZZGdEVXh2M0IwN2hQNzR4cVdzaHBidGFNVXFIRGFnc1h5d3owM0NpZXdDN1k5TDNMZGJnenloVjJ2ZDF0Q3o0cGtZLW9I?oc=5) <sub>조선일보 · 22 Nov 07:29</sub> | — | — | — | — |
| [Apple](labs/README.md#lab-apple) | 8 + 5 | [Does Apple Intelligence Drain Your Battery? When, Why and How to Check](https://news.google.com/rss/articles/CBMiW0FVX3lxTE0yckliOGZsM2tyZW5VV290MjVDR3NxZmZvVVZjV1k5Skp1bkRMcFdmeWc5NUEyLXk4YUZOX0czcTQzUFhZanRpR1lVQi1GWVdibnRQVWhPNDZpM0k?oc=5) <sub>Fello AI · 22 Nov 07:08</sub> | [apple/DepthPro2-focal](https://huggingface.co/apple/DepthPro2-focal) <sub>19 Nov 19:02</sub> | — | — | — |
| [DeepSeek](labs/README.md#lab-deepseek) | 8 + 0 | [Unsloth revises DeepSeek GGUF benchmarks with longer contexts and…](https://news.google.com/rss/articles/CBMiQkFVX3lxTE9OcUVlTm5FNjB4LU1kSllkXzdqWUJFVkNLLUczcVNReUpYQVI5cmFXdHlGWTlKLUtyY1paMWlha1lGQQ?oc=5) <sub>Digg · 22 Nov 02:08</sub> | [DeepSeek: DeepSeek V4.1 Flash 1017](https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017) <sub>17 Oct 10:27</sub> | — | — | — |
| [Qwen & Alibaba](labs/README.md#lab-qwen) | 8 + 0 | [Alibaba's Qwen4-Max Rollout Runs Into a Compute Wall](https://news.google.com/rss/articles/CBMiwgFBVV95cUxPdm1SS1NneHJJLTkyWFRVbS1OMGZxZV9OaXhfcDhVNkVaeEFNNG9hbW9OTXRTRW4yR2h6MjgxZ0c5d3FrZVk2ZTRmVVoxMDJKcGd6bGtLejUtbmNYV0FfNjBjSm13LUlJMHJhOE5KRnBGbF8zS1J4OFJJMHBiUUtaZ3FoMUpGRzFqNlY3OWFtUDlqcTRBSWp2d3MtMUhURDYtcEdmN29zQ19HTVpxVXNHQ2g2WG9FZEktaExnOERPYjdOUQ?oc=5) <sub>ad-hoc-news.de · 22 Nov 03:11</sub> | [Qwen: Qwen4 Max](https://openrouter.ai/qwen/qwen4-max) <sub>16 Nov 03:18</sub> | [Release…](https://github.com/QwenLM/qwen-code/releases/tag/v0.28.3-nightly.20261121.56ef346859) <sub>qwen-code · 21 Nov 23:28</sub> | — | — |
| [Moonshot AI (Kimi)](labs/README.md#lab-moonshot) | 8 + 0 | [Moonshot Launches Kimi K3, an Open-Weight AI Model with 2.8 Trillion…](https://news.google.com/rss/articles/CBMirgFBVV95cUxNY1pCaFBqckY2SWhrWVhqQkR6N2RuN0lUM1JJd0d0cUE4WGV3U0VSM3Yxamh6YTBDT3A3TV8zaFp4ZGZ4VTRtWHRLb2J1SGI4ZzM0N2tyMzZHYkRuRnVIUFJKSmRfNHpWR2NaM0FMSmstTk5lNUJ0bDFMeW5tWFNRd25QUkFKZ2R3c3NZVHZPS2ZrVElCc0RwdlJKeTBob0pFV1ZBUG5adEl1UW9uaWc?oc=5) <sub>VOI.ID · 22 Nov 04:34</sub> | [moonshotai/Kimi-K3.1-Pro](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) <sub>2 Nov 05:13</sub> | — | — | — |
| [Zhipu (Z.ai, GLM)](labs/README.md#lab-zhipu) | 1 + 0 | [Tencent Hy4 vs GLM-5.5: One of These Models Does Not Exist](https://news.google.com/rss/articles/CBMiY0FVX3lxTE1renlMeUtkUmZldkszc0l1T3hNcV9FWVQwZHR6b0FaQ3Nqd2NlSGxMTHNXVFR0dGVQRDQyZDVHSG1TYVNBM0dzMUZ4VEJjNERHaUl4WF9HVlpPeFc4ODFoZlZoVQ?oc=5) <sub>OrcaRouter · 20 Nov 14:59</sub> | [Z.ai: GLM 5.3 FlashX Legal](https://openrouter.ai/z-ai/glm-5.3-flashx-legal) <sub>2 Nov 14:29</sub> | — | — | — |
| [Perplexity](labs/README.md#lab-perplexity) | 2 + 0 | [Judge Pauses Discovery in Amazon v. Perplexity](https://news.google.com/rss/articles/CBMikgFBVV95cUxQTjNPVW1HclB6bHJLYWNndFcxbzFSNFVvVEVzYTBRSnZRVmdoMm5lOGxlZHA5bF9ya1U0UERlRTczTkF2MG9hWnBMVl9jZTNiTzBoekNVOU13Rk44aXUtSG5qNGtId0FpY0dJdDdsQVMyeVh0WmdQYUpsVnhMUDB1WGF2VkVnUl9WNTlxdmRTeHg2dw?oc=5) <sub>Wisevoter · 21 Nov 01:43</sub> | — | — | 0 | — |
| [Hugging Face](labs/README.md#lab-huggingface) | 4 + 4 | [Hugging Face: Thinking Machines Lab releases Inkling 2 Mini, with AI…](https://news.google.com/rss/articles/CBMiREFVX3lxTE1hNS0xYWVJUnlsVDFLYmVpTnprLUs1SE9ILUt1TXBlSWZnX2JJcENrRUFBZkJySVFNdHpsZmhNRnhMU3JD?oc=5) <sub>Digg · 21 Nov 19:56</sub> | — | [Release v5.24.0](https://github.com/huggingface/transformers/releases/tag/v5.24.0) <sub>transformers · 21 Nov 13:43</sub> | — | — |
| [Stability AI](labs/README.md#lab-stability) | 0 + 0 | — | [stabilityai/sdxl-turbo-amdnpu-medusa](https://huggingface.co/stabilityai/sdxl-turbo-amdnpu-medusa) <sub>9 Nov 13:06</sub> | — | — | — |

<sub>Headlines: Google News search for the lab, last 48 h. Official posts: the lab's own blog or newsroom feed, last 14 days. Models: OpenRouter (60 days) and Hugging Face (30 days). SDK releases: GitHub releases feeds (14 days). Incidents: the lab's public status page. A dash means no source covers it.</sub>

<a id="media"></a>

## AI media: video, image, audio & voice

Video, image, music, speech and voice generation: provider headlines (Google News and outlet feeds, up to 2 per provider), LMArena text-to-video and text-to-image leaders, and trending open models on Hugging Face.

| # | Model or story | Provider | Modality | What's new | Date | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [China's MiniMax founder loses over 90% of fortune as AI competition intensifies](https://news.google.com/rss/articles/CBMiVEFVX3lxTE9tTzl2TTNfbXJYRnlJUzI5LUFKUjJKckUtSFFxRkFSV0t4eXFtMU95b1hRemtPWUNpVEVpTS0xNFFYZmYwb2dJTzA1UXRrX1lYZWYxNg?oc=5) | MiniMax Hailuo | video | Headline · AzerNews | 22 Nov 06:00 | [Google News](https://news.google.com/search?q=Hailuo+OR+MiniMax+video+OR+Higgsfield+OR+Midjourney&hl=en-US&gl=US&ceid=US%3Aen) |
| 2 | [MiniMax Says Its AI Broke 4 Old NIST Crypto Candidates](https://news.google.com/rss/articles/CBMiigFBVV95cUxPT2JNNGhQSUVnNHR2VGxvOC1iaVpra1hwaElTYlZPaC0wUUJNcF9FRzI0UlZ6YUliWl9JblpHM25iVFlEOFl2dFlselY0NW5jaVc0SEVvbmJEV05VOGx5b2NGVWo0enhjS3BvVVdGYXJlMlE4aWM5UDZzN0xrRktISVhhYUkteVNzR1E?oc=5) | MiniMax Hailuo | video | Headline · FourWeekMBA | 21 Nov 19:40 | [Google News](https://news.google.com/search?q=Hailuo+OR+MiniMax+video+OR+Higgsfield+OR+Midjourney&hl=en-US&gl=US&ceid=US%3Aen) |
| 3 | [Suno Launches AI Music Video Generator That Can Make Characters Sing Along to…](https://news.google.com/rss/articles/CBMilAFBVV95cUxQc2JScnE1ZE5jV1ZPd1NyMEdNdFQ2NG1NSS1LbVEtSDFNcHEzR1lvRU9LVm1OYTNIMkRfTXpTRUVyc2NyZllGUU1WR3VyMnRmTk9ZNzZwazZkWThJTk5QcFNKZjF3WWZVY2RvekZLeFFra1JyY2diekRWUU9uUkItQnJ4WEI4dkFTbFZFa2xaQmZoZDFk?oc=5) | Suno | music | Headline · SoaplandTV | 20 Nov 23:00 | [Google News](https://news.google.com/search?q=Hailuo+OR+MiniMax+video+OR+Higgsfield+OR+Midjourney&hl=en-US&gl=US&ceid=US%3Aen) |
| 4 | [Best AI Music Video Generators for Suno Artists in 2026: Full Songs, Lip Sync…](https://news.google.com/rss/articles/CBMieEFVX3lxTFBVaVVDSkw2Z3hZUHFpbXViWExhSTdPQlRZdHY2Sndyci1USmM3VGp4WFI2aVNycUVpVERTSllqOXlqSVRlMjE5OW9LejBBaEN2ZkZYTTBSa1ByRXdIRkdNQTRHNEE0b1JEb3ZVTHN3MkR5eEVEVWp2MA?oc=5) | Suno | music | Headline · SIDE-LINE | 20 Nov 09:53 | [Google News](https://news.google.com/search?q=%22Luma+AI%22+OR+%22Pika%22+AI+video+OR+%22Kling%22+AI&hl=en-US&gl=US&ceid=US%3Aen) |
| 5 | [Gucci's Vision Pro Runway Show Offers Immersive Access, But The Luxury…](https://www.uploadvr.com/guccis-vision-pro-runway-show-offers-immersive-access-but-the-luxury-experience-falls-short/) | Runway | video | Headline · UploadVR | 20 Nov 19:00 | [UploadVR](https://www.uploadvr.com/rss/) |
| 6 | [Runway Expands AI Video & Praxis-1 World Models to Robotics](https://news.google.com/rss/articles/CBMijgFBVV95cUxNR3JRcjBranNOdlVGNV9USkhTYXNKVGQyaEwzTzg2TXFDalpKcUg0dlVqdFR5eVNNeEJRZnJOOW1CSGwyYl9nQkY1SGhRUjRVd2ZjaU4wZ25aVUdmMndMRGd4UVBpbGx1RnhWakluTmdZNEhwbzNNcDRIUnFMeHN1ajdLUkpaZ1Y1MzI4ZHFn?oc=5) | Runway | video | Headline · AI Magazine | 20 Nov 11:09 | [Google News](https://news.google.com/search?q=%22Luma+AI%22+OR+%22Pika%22+AI+video+OR+%22Kling%22+AI&hl=en-US&gl=US&ceid=US%3Aen) |
| 7 | [HeyGen Alternative Platforms For Training Teams: 2027 Comparison](https://news.google.com/rss/articles/CBMingFBVV95cUxQTnc2YS1yRXFRT1cySVE2QkhmRXRkZWRQTnhhbm5reEZSWGRZeUdWbUNWU1hWYkNxcHlRN0NIMGEwOXY5ME5wVVhlbkRnOVJWQmJVb1hicHBKVi0xbTlqTFR0bFR4VVI3TUt0VnBsZzg3bFptS1Z4aVBBVjNOWHlGRGJxNndlNGwxLU9iU2RYVXA0R0JKcnNmZHhqYmQ0QQ?oc=5) | HeyGen | avatar video | Headline · TechRound | 20 Nov 14:32 | [Google News](https://news.google.com/search?q=Udio+OR+HeyGen+OR+Synthesia+OR+%22Nano+Banana%22&hl=en-US&gl=US&ceid=US%3Aen) |
| 8 | [How AI Image Generation Is Transforming Digital Creativity: A Practical Look…](https://news.google.com/rss/articles/CBMitgFBVV95cUxPRVhPamlrbUtwc0V3dHJVSUFxNE4tckpXZmhQaDBCTU9Yd1pOSWpKSGNjZFZfNjRCODRjbklLWE5PaGhCSkRzWXBzWmRNaUpKVzBveGdUSzNsTVhKQnZaUkIzdEtWcmI3cEVrc1RUNkN0OENBNXdHQ2cxQ3ZyR1d6Z1FLYzNuYmxXTndpc2FUSEgyMWg5Wml3dDBzZ1VpUmk5YV84SXc4Z1F2SUVDNTVWYmVIYnJVUQ?oc=5) | Google Nano Banana | image | Headline · TechBullion | 20 Nov 14:10 | [Google News](https://news.google.com/search?q=Udio+OR+HeyGen+OR+Synthesia+OR+%22Nano+Banana%22&hl=en-US&gl=US&ceid=US%3Aen) |
| 9 | [Google Pics updates to Nano Banana 2.1 with more detail and control](https://news.google.com/rss/articles/CBMiqgFBVV95cUxNaXpZempGR1R3VXZxY1JlQjNTeTFfS0hiN05ObGZDVmdEbmxZUjNEbmRxRl9jQTlIbzlhbGF0V1c0akZvVjcySkpySTUxQktGZUJZZjZBWk5oQVZGSHlweGRWMmd4a3RreEJkV2dYZFllaWhkTnd2bUhvaXplV1M1ek5WbHo4dllVS3JIYVF4dEJWZmlHNXBEU042NGRKN3FXaXpwX244YkFoZw?oc=5) | Google Nano Banana | image | Headline · Foro3D | 20 Nov 14:03 | [Google News](https://news.google.com/search?q=Udio+OR+HeyGen+OR+Synthesia+OR+%22Nano+Banana%22&hl=en-US&gl=US&ceid=US%3Aen) |
| 10 | [Synthesia: AI Video Avatars, US$4bn Value & the Fortune 100](https://news.google.com/rss/articles/CBMiiwFBVV95cUxQUk9KOWFydzVVQkdaeDAyb0tvVkVkMU9SWDVhNTlZY0w4MXVYNVc1NjctWEozRlVHcWw2V19qTVc0RThWX0tpYnJKT3JoWHQ3TkJoSEVQMkl5NU1qMElFVnFIUkRyYjNjaUFCeEs1RzZfNTlySGlQV1EyTjA2dHJBN1pBYTZUNFFwZlpV?oc=5) | Synthesia | avatar video | Headline · AI Magazine | 20 Nov 12:19 | [Google News](https://news.google.com/search?q=Udio+OR+HeyGen+OR+Synthesia+OR+%22Nano+Banana%22&hl=en-US&gl=US&ceid=US%3Aen) |

<details>
<summary>Show 20 more</summary>

| # | Model or story | Provider | Modality | What's new | Date | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 11 | [WeMM-Video-2B vs Pika Enact: Two Models, No Product](https://news.google.com/rss/articles/CBMigAFBVV95cUxOYU11R2lmRnFkY25ibm8yT01QcUpmM1FTWWduLUVxSFBmeGJDMERwRDBuZ1hTemQ3V2syQ2JhRE41QUZQSGcwNW81My13c0Y2UzczbFNDblo4bVZMZW1jaDcxRnphQ1E1V1BiSl9ya3lLZ3luOVRHSG1sM1RpQThQOQ?oc=5) | Pika | video | Headline · OrcaRouter | 20 Nov 07:16 | [Google News](https://news.google.com/search?q=%22Luma+AI%22+OR+%22Pika%22+AI+video+OR+%22Kling%22+AI&hl=en-US&gl=US&ceid=US%3Aen) |
| 12 | [GPT-Image-2.5 Sunburst](https://lmarena.ai/leaderboard) | openai | image | #1 on LMArena text-to-image, rating 1429 (73,040 votes) | 2026-11-20 | [LMArena](https://lmarena.ai/leaderboard/text-to-image) |
| 13 | [GPT-Image-2.6 Sunburst (Medium)](https://lmarena.ai/leaderboard) | openai | image | #2 on LMArena text-to-image, rating 1412 (7,168 votes) | 2026-11-20 | [LMArena](https://lmarena.ai/leaderboard/text-to-image) |
| 14 | [GPT-Image-2.5 Flare](https://lmarena.ai/leaderboard) | openai | image | #3 on LMArena text-to-image, rating 1400 (72,202 votes) | 2026-11-20 | [LMArena](https://lmarena.ai/leaderboard/text-to-image) |
| 15 | [MAI-Image-2.7](https://lmarena.ai/leaderboard) | microsoft-ai | image | #4 on LMArena text-to-image, rating 1385 (4,485 votes) | 2026-11-20 | [LMArena](https://lmarena.ai/leaderboard/text-to-image) |
| 16 | [GPT-Image-2 (Medium)](https://lmarena.ai/leaderboard) | openai | image | #5 on LMArena text-to-image, rating 1382 (112,925 votes) | 2026-11-20 | [LMArena](https://lmarena.ai/leaderboard/text-to-image) |
| 17 | [apple/FastFrames-L](https://huggingface.co/apple/FastFrames-L) | apple | video | Trending on Hugging Face (text-to-video) · 499 likes · apple-amlr | created 16 Nov 18:21 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 18 | [Comfy-Org/PAN2](https://huggingface.co/Comfy-Org/PAN2) | Comfy-Org | video | Trending on Hugging Face (text-to-video) · 53 likes · apache-2.0 | created 15 Nov 11:42 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 19 | [apple/FastFrames-S](https://huggingface.co/apple/FastFrames-S) | apple | video | Trending on Hugging Face (text-to-video) · 129 likes · apple-amlr | created 16 Nov 18:21 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 20 | [Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5) | Lightricks | video | Trending on Hugging Face (image-to-video) · 12,966 likes · other | created 23 Jul 09:55 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 21 | [Comfy-Org/Wan-2.2](https://huggingface.co/Comfy-Org/Wan-2.2) | Comfy-Org | video | Trending on Hugging Face (image-to-video) · 1,058 likes · apache-2.0 | created 27 Jul 08:56 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 22 | [Wuli-art/Gemma4-for-MiniMax-H3-Prompt-Extend](https://huggingface.co/Wuli-art/Gemma4-for-MiniMax-H3-Prompt-Extend) | Wuli-art | video | Trending on Hugging Face (image-to-video) · 21 likes · apache-2.0 | created 16 Nov 03:49 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 23 | [chatrlabs/Qwen-Image-2.1-Uncensored-Omni-Quantized](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-Quantized) | chatrlabs | image | Trending on Hugging Face (text-to-image) · 748 likes · other | created 3 Nov 17:13 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 24 | [MiniMaxAI/MiniMax-H3-Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) | MiniMaxAI | image | Trending on Hugging Face (text-to-image) · 1,694 likes · other | created 3 Nov 07:34 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 25 | [lodestones/Kromoss](https://huggingface.co/lodestones/Kromoss) | lodestones | image | Trending on Hugging Face (text-to-image) · 431 likes · apache-2.0 | created 19 Oct 03:34 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 26 | [n4ze3m/tiny-voca](https://huggingface.co/n4ze3m/tiny-voca) | n4ze3m | voice | Trending on Hugging Face (text-to-speech) · 380 likes · apache-2.0 | created 14 Nov 16:46 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 27 | [Zyphra/ZONOS3-Mini](https://huggingface.co/Zyphra/ZONOS3-Mini) | Zyphra | voice | Trending on Hugging Face (text-to-speech) · 573 likes · apache-2.0 | created 9 Nov 06:03 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 28 | [software-mansion/Reverb-TTS](https://huggingface.co/software-mansion/Reverb-TTS) | software-mansion | voice | Trending on Hugging Face (text-to-speech) · 116 likes · cc-by-nc-4.0 | created 1 Oct 23:47 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 29 | [MiniMaxAI/MiniMax-Music3](https://huggingface.co/MiniMaxAI/MiniMax-Music3) | MiniMaxAI | audio | Trending on Hugging Face (text-to-audio) · 1,551 likes · licence not stated | created 7 Aug 14:23 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 30 | [stabilityai/stable-audio-open-1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) | stabilityai | audio | Trending on Hugging Face (text-to-audio) · 2,027 likes · other | created 24 May 07:11 | [Hugging Face](https://huggingface.co/models?sort=trending) |

</details>

<sub>[All AI media items by type](industries/ai-media.md)</sub>

<a id="map"></a>

## Industry map

One row per industry. **Top item** is its highest-scoring item today. An item can sit in more than one industry.

| Industry | Items | Top item | Strongest signal | Score | File |
| --- | --- | --- | --- | --- | --- |
| [AI & LLMs](#ind-ai-llms) | **561** <sub>73 sources</sub> | [Researcher plants 2m canaries into the AI supply…](https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/) | 11 score · 3 comments | 77 | [open](industries/ai-llms.md) |
| [AI agents & MCP](#ind-ai-agents) | **139** <sub>31 sources</sub> | [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 16.4k stars · +1,803 today · +12.3% | 60 | [open](industries/ai-agents.md) |
| [AI media: video, image, audio & voice](#ind-ai-media) | **81** <sub>10 sources</sub> | [WeVisForensics: Self-Evolving Agent for Omni…](https://huggingface.co/papers/2611.21373) | 54 upvotes | 60 | [open](industries/ai-media.md) |
| [Developer tools](#ind-devtools) | **162** <sub>30 sources</sub> | [cursor/plugins](https://github.com/cursor/plugins) | 18.2k stars · +260 today · +1.5% | 60 | [open](industries/devtools.md) |
| [Cloud & DevOps](#ind-cloud-devops) | **94** <sub>31 sources</sub> | [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 16.4k stars · +1,803 today · +12.3% | 60 | [open](industries/cloud-devops.md) |
| [Cybersecurity](#ind-cybersecurity) | **89** <sub>34 sources</sub> | [Researcher plants 2m canaries into the AI supply…](https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/) | 11 score · 3 comments | 77 | [open](industries/cybersecurity.md) |
| [Data & analytics](#ind-data-analytics) | **44** <sub>16 sources</sub> | [datazip-inc/olake-go](https://github.com/datazip-inc/olake-go) | 2.2k stars · +93 today · +4.4% | 60 | [open](industries/data-analytics.md) |
| [Web & frontend](#ind-web-frontend) | **42** <sub>14 sources</sub> | [swiper](https://www.jsdelivr.com/package/npm/swiper) | 4.6B hits/week · +1.9% w/w | 60 | [open](industries/web-frontend.md) |
| [Mobile](#ind-mobile) | **28** <sub>15 sources</sub> | [Signal Blocks AI Agents From Reading Private Chats…](https://thehackernews.com/2026/11/signal-blocks-ai-agents-from-reading.html) | The Hacker News · 21 Nov 09:49 | 53 | [open](industries/mobile.md) |
| [Markets & economy](#ind-markets-economy) | **172** <sub>37 sources</sub> | [LosaLosSantos/aurelio-finance](https://github.com/LosaLosSantos/aurelio-finance) | 352 stars · created 6 Oct | 60 | [open](industries/markets-economy.md) |
| [Fintech & payments](#ind-fintech) | **54** <sub>26 sources</sub> | [LosaLosSantos/aurelio-finance](https://github.com/LosaLosSantos/aurelio-finance) | 352 stars · created 6 Oct | 60 | [open](industries/fintech.md) |
| [Crypto & web3](#ind-crypto-web3) | **46** <sub>7 sources</sub> | [Official Trump (TRUMP)](https://www.coingecko.com/en/coins/official-trump) | $0.888278 · +5.5% 24h | 60 | [open](industries/crypto-web3.md) |
| [Health & biotech](#ind-health-biotech) | **49** <sub>18 sources</sub> | [Pill to treat pancreatic cancer hailed as 'biggest…](https://www.theguardian.com/society/2026/nov/20/pill-pancreatic-cancer-breakthrough-daraxonrasib) | 884 pts · 203 comments · 26 pts/h | 68 | [open](industries/health-biotech.md) |
| [Robotics & hardware](#ind-robotics-hardware) | **40** <sub>17 sources</sub> | [KingKongRobotics/jumper](https://github.com/KingKongRobotics/jumper) | 3.2k stars · created 28 Sep | 60 | [open](industries/robotics-hardware.md) |
| [Semiconductors & chips](#ind-semiconductors) | **74** <sub>26 sources</sub> | [NixOS bring-up on an Alibaba RISC-V board](https://feyor.sh/blog/nixos-bringup-on-an-alibaba-riscv-board/) | 9 score · 1 comments | 52 | [open](industries/semiconductors.md) |
| [Climate & energy](#ind-climate-energy) | **37** <sub>16 sources</sub> | [Why Is the World Still Counting on Unproven Carbon…](https://www.propublica.org/article/carbon-capture-and-storage-climate-models) | ProPublica · 21 Nov 11:00 | 30 | [open](industries/climate-energy.md) |
| [E-commerce & retail](#ind-ecommerce-retail) | **49** <sub>22 sources</sub> | [Amazon closes in on $7.5bn deal to buy AI start-up…](https://news.google.com/rss/articles/CBMihAFBVV95cUxNTEFvVDlwcmNmNEl1WGpwZ3A3TzF3ZkNLSDFrUHA3XzY3REJxa3Jyc3pjUnVLdXdydFp3eTBYR1E1elQzVllDV1JQVzJENFNhV3RjVWl1eFB3dWFZS1BQWlRpTC1WZWZ1OV9CZmdhQnNtdmUxb25DWS16SEVodXVlRnBFUFQ?oc=5) | Financial Times · 21 Nov 18:21 | 28 | [open](industries/ecommerce-retail.md) |
| [Gaming & XR](#ind-gaming-xr) | **38** <sub>16 sources</sub> | [metacritic gta vi](https://trends.google.com/trending?geo=US&q=metacritic%20gta%20vi) | 10000+ searches (US) | 60 | [open](industries/gaming-xr.md) |
| [Enterprise SaaS & productivity](#ind-enterprise-saas) | **24** <sub>11 sources</sub> | [Vyber07/cyber-security](https://huggingface.co/datasets/Vyber07/cyber-security) | 1,380 likes · 28.7k dl/30d | 60 | [open](industries/enterprise-saas.md) |
| [Education](#ind-education) | **26** <sub>12 sources</sub> | [Posterior Matching Distillation](https://huggingface.co/papers/2611.26629) | 37 upvotes | 57 | [open](industries/education.md) |
| [Media & creator economy](#ind-media-creator) | **46** <sub>23 sources</sub> | [Change one letter, ruin a movie](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/645e79ca5148) | — | 60 | [open](industries/media-creator.md) |
| [Space & mobility](#ind-space-mobility) | **43** <sub>16 sources</sub> | [AI patching likely behind outages](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/2fff3b60524e) | — | 32 | [open](industries/space-mobility.md) |
| [Policy & regulation](#ind-policy-regulation) | **43** <sub>23 sources</sub> | [Researcher plants 2m canaries into the AI supply…](https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/) | 11 score · 3 comments | 77 | [open](industries/policy-regulation.md) |
| [Other](#ind-other) | **82** <sub>14 sources</sub> | [My monitor was cutting my download speed by 75%](https://blog.tymscar.com/posts/studiodisplayethernet/) | 555 pts · 265 comments · 27 pts/h | 73 | [open](industries/other.md) |

<a id="industries"></a>

## Industries

Top 3 per industry, highest score first (more behind "Show more"). The same columns in every industry.

<a id="ind-ai-llms"></a>

### AI & LLMs

Foundation models, inference, ML research and the labs behind them. **561 items** · [full list →](industries/ai-llms.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Researcher plants 2m canaries into the AI supply chain. A privacy…](https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/) | Posts | #ai, #security | 11 score · 3 comments | **3** <sub>Lobsters, Ars Technica, Mastodon</sub> | 77 | [Lobsters](https://lobste.rs/) |
| 2 | [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | Repositories | A Claude Code skill bundle for bug hunting and external red-team work - 82 skills, 15 slash commands, 681… | 16.4k stars · +1,803 today | 1 | 60 | [GitHub trending](https://github.com/trending?since=daily) |
| 3 | [janhq/jan](https://github.com/janhq/jan) | Repositories | Jan is an open source alternative to ChatGPT that runs 100% offline on your computer. | 46k stars · +45 today | 1 | 60 | [GitHub trending](https://github.com/trending/rust?since=daily) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini) | Models | image-text-to-text · transformers | 3,301 likes · 7.9k dl/30d | 1 | 60 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 5 | [huggingface/moe-blogpost](https://huggingface.co/spaces/huggingface/moe-blogpost) | Demos (Spaces) | A hands-on guide to training Mixture-of-Experts models | 812 likes | 1 | 60 | [Hugging Face](https://huggingface.co/spaces?sort=trending) |
| 6 | [Vyber07/cyber-security](https://huggingface.co/datasets/Vyber07/cyber-security) | Datasets | Cybersecurity AI Knowledge Base — PhD-Level Dataset Overview This is the most… | 1,380 likes · 28.7k dl/30d | 1 | 60 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |
| 7 | [WeVisForensics: Self-Evolving Agent for Omni AI-Generated Video…](https://huggingface.co/papers/2611.21373) | Papers | Recent advances in video generation call for reliable detection grounded in explicit forensic evidence. | 54 upvotes | 1 | 60 | [Hugging Face](https://huggingface.co/papers) |
| 8 | [The Chairs Are Back. The Coffee Is On. ](https://dev.to/thethirdcup/the-chairs-are-back-the-coffee-is-on-243p) | Posts | #community, #discuss, #ai | 94 reactions · 38 comments | 1 | 60 | [Dev.to](https://dev.to/top/day) |
| 9 | [LosaLosSantos/aurelio-finance](https://github.com/LosaLosSantos/aurelio-finance) | Repositories | Open-source personal finance app with an AI financial advisor: track your net worth, investments, ETFs, cash… | 352 stars · created 6 Oct | 1 | 60 | [GitHub](https://github.com/topics/fintech) |
| 10 | [Posterior Matching Distillation](https://huggingface.co/papers/2611.26629) | Papers | Diffusion distillation accelerates image and video generation by compressing a pretrained teacher's… | 37 upvotes | **2** <sub>Hugging Face, arXiv</sub> | 57 | [Hugging Face](https://huggingface.co/papers) |

</details>

<sub>551 more in [AI & LLMs](industries/ai-llms.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-ai-agents"></a>

### AI agents & MCP

Agent frameworks, skills, tool use and Model Context Protocol servers. **139 items** · [full list →](industries/ai-agents.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | Repositories | A Claude Code skill bundle for bug hunting and external red-team work - 82 skills, 15 slash commands, 681… | 16.4k stars · +1,803 today | 1 | 60 | [GitHub trending](https://github.com/trending?since=daily) |
| 2 | [WeVisForensics: Self-Evolving Agent for Omni AI-Generated Video…](https://huggingface.co/papers/2611.21373) | Papers | Recent advances in video generation call for reliable detection grounded in explicit forensic evidence. | 54 upvotes | 1 | 60 | [Hugging Face](https://huggingface.co/papers) |
| 3 | [Brave Search](https://smithery.ai/server/brave) | MCP servers | Search the web with Brave's independent index — web, news, images, and videos. | 87,579 uses | 1 | 60 | [Smithery](https://smithery.ai/) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk) | Packages | Model Context Protocol implementation for TypeScript | 93.8M dl/week | 1 | 60 | [npm](https://www.npmjs.com/) |
| 5 | [ai](https://www.npmjs.com/package/ai) | Packages | AI SDK by Vercel - build apps like ChatGPT, Claude, Gemini, and more with a single interface for any model… | 48.5M dl/week | 1 | 57 | [npm](https://www.npmjs.com/) |
| 6 | [obra/superpowers](https://github.com/obra/superpowers) | Repositories | An agentic skills framework & software development methodology that works. | 323.9k stars · +883 today | 1 | 56 | [GitHub trending](https://github.com/trending?since=daily) |
| 7 | [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) | Repositories | "CLI-Anything: Making ALL Software Agent-Native" -- CLI-Hub: https://clianything.cc/ | 62.2k stars · +769 today | 1 | 54 | [GitHub trending](https://github.com/trending?since=daily) |
| 8 | [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | Repositories | Knowledge infrastructure to make your agents smarter. | 206.4k stars · +1,006 today | 1 | 54 | [GitHub trending](https://github.com/trending?since=daily) |
| 9 | [vxcontrol/pentagi](https://github.com/vxcontrol/pentagi) | Repositories | Fully autonomous AI Agents system capable of performing complex penetration testing tasks | 34.8k stars · +60 today | 1 | 54 | [GitHub trending](https://github.com/trending/go?since=daily) |
| 10 | [uk-due-diligence](https://smithery.ai/server/bouch/uk-due-diligence) | MCP servers | Tools across five UK public registers. | 60,881 uses | 1 | 54 | [Smithery](https://smithery.ai/) |

</details>

<sub>129 more in [AI agents & MCP](industries/ai-agents.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-ai-media"></a>

### AI media: video, image, audio & voice

Generative video, image, music, speech and voice models and the companies that make them. **81 items** · [full list →](industries/ai-media.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [WeVisForensics: Self-Evolving Agent for Omni AI-Generated Video…](https://huggingface.co/papers/2611.21373) | Papers | Recent advances in video generation call for reliable detection grounded in explicit forensic evidence. | 54 upvotes | 1 | 60 | [Hugging Face](https://huggingface.co/papers) |
| 2 | [Posterior Matching Distillation](https://huggingface.co/papers/2611.26629) | Papers | Diffusion distillation accelerates image and video generation by compressing a pretrained teacher's… | 37 upvotes | **2** <sub>Hugging Face, arXiv</sub> | 57 | [Hugging Face](https://huggingface.co/papers) |
| 3 | [Angais/pixel-art-atlas-1.4m](https://huggingface.co/datasets/Angais/pixel-art-atlas-1.4m) | Datasets | Pixel Art Atlas · 1.4M Synthetic Sprites 1,409,404 synthetic game sprites with English… | 666 likes · 74k dl/30d | 1 | 55 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [MiniMaxAI/minimax-h3-image](https://huggingface.co/spaces/MiniMaxAI/minimax-h3-image) | Demos (Spaces) | Text-to-image and multi-image editing in 6 steps | 250 likes | 1 | 50 | [Hugging Face](https://huggingface.co/spaces?sort=trending) |
| 5 | [apple/FastFrames-L](https://huggingface.co/apple/FastFrames-L) | Models | text-to-video | 499 likes · 0 dl/30d | 1 | 44 | [Hugging Face](https://huggingface.co/models?sort=trending) |
| 6 | [Coda-DaVinci: Reimagining Video Generation with Code2Video](https://huggingface.co/papers/2611.26595) | Papers | Code2Video uses agent-authored 3D proxies to guide video generation, enabling explicit control over… | 35 upvotes | 1 | 40 | [Hugging Face](https://huggingface.co/papers) |
| 7 | [openvinotoolkit/openvino](https://github.com/openvinotoolkit/openvino) | Repositories | OpenVINO™ is an open source toolkit for optimizing and deploying AI inference | 12k stars · +200 today | 1 | 34 | [GitHub trending](https://github.com/trending?since=daily) |
| 8 | [zhouxiaoka/autoclip](https://github.com/zhouxiaoka/autoclip) | Repositories | AutoClip｜一个链接，一键出片。开源 AI 视频剪辑桌面工具，将播客、访谈、课程等长视频自动剪成短视频，生成字幕、封面和发布文案，适配抖音、小红书、TikTok、Reels 与 YouTube… | 13k stars · +683 today | 1 | 24 | [GitHub trending](https://github.com/trending?since=daily) |
| 9 | [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | Repositories | Mastra is the modern TypeScript framework for AI-powered applications and agents. | 29.7k stars · +30 today | 1 | 24 | [GitHub trending](https://github.com/trending/typescript?since=daily) |
| 10 | [Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5) | Models | image-to-video · diffusion-single-file | 12,966 likes · 3M dl/30d | 1 | 16 | [Hugging Face](https://huggingface.co/models?sort=trending) |

</details>

<sub>71 more in [AI media: video, image, audio & voice](industries/ai-media.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-devtools"></a>

### Developer tools

Languages, editors, CLIs, package ecosystems and the software toolchain. **162 items** · [full list →](industries/devtools.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [cursor/plugins](https://github.com/cursor/plugins) | Repositories | Cursor plugin specification and official plugins | 18.2k stars · +260 today | 1 | 60 | [GitHub trending](https://github.com/trending?since=daily) |
| 2 | [janhq/jan](https://github.com/janhq/jan) | Repositories | Jan is an open source alternative to ChatGPT that runs 100% offline on your computer. | 46k stars · +45 today | 1 | 60 | [GitHub trending](https://github.com/trending/rust?since=daily) |
| 3 | [datazip-inc/olake-go](https://github.com/datazip-inc/olake-go) | Repositories | OLake Go: open-source replication from databases, Kafka and S3 to Apache Iceberg and Parquet. | 2.2k stars · +93 today | 1 | 60 | [GitHub trending](https://github.com/trending/go?since=daily) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk) | Packages | Model Context Protocol implementation for TypeScript | 93.8M dl/week | 1 | 60 | [npm](https://www.npmjs.com/) |
| 5 | [Is it significant to use size_t in place of int?](https://stackoverflow.com/questions/80018068/is-it-significant-to-use-size-t-in-place-of-int) | Questions | #c++ | -1 score · 0 answers · 19 views | 1 | 60 | [Stack Overflow](https://stackoverflow.com/questions?tab=Hot) |
| 6 | [heise3/ExtremaRank](https://github.com/heise3/ExtremaRank) | Repositories | Native R and Python sample-deletion robustness for omics: candidate certificates, minimum deletion bounds… | 288 stars · created 3 Oct | 1 | 60 | [GitHub](https://github.com/topics/bioinformatics) |
| 7 | [LosaLosSantos/aurelio-finance](https://github.com/LosaLosSantos/aurelio-finance) | Repositories | Open-source personal finance app with an AI financial advisor: track your net worth, investments, ETFs, cash… | 352 stars · created 6 Oct | 1 | 60 | [GitHub](https://github.com/topics/fintech) |
| 8 | [Advice for the next 100 Rust GUIs](https://linebender.org/blog/next-100-guis/) | Discussions | Link to linebender.org | 136 pts · 37 comments | **2** <sub>Hacker News, Lobsters</sub> | 57 | [Hacker News](https://news.ycombinator.com/) |
| 9 | [ai](https://www.npmjs.com/package/ai) | Packages | AI SDK by Vercel - build apps like ChatGPT, Claude, Gemini, and more with a single interface for any model… | 48.5M dl/week | 1 | 57 | [npm](https://www.npmjs.com/) |
| 10 | [What does return(0); do in C programming](https://stackoverflow.com/questions/80018059/what-does-return0-do-in-c-programming) | Questions | #c | -3 score · 0 answers · 62 views | 1 | 55 | [Stack Overflow](https://stackoverflow.com/questions?tab=Hot) |

</details>

<sub>152 more in [Developer tools](industries/devtools.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-cloud-devops"></a>

### Cloud & DevOps

Infrastructure, containers, CI/CD, self-hosting, outages and operations. **94 items** · [full list →](industries/cloud-devops.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | Repositories | A Claude Code skill bundle for bug hunting and external red-team work - 82 skills, 15 slash commands, 681… | 16.4k stars · +1,803 today | 1 | 60 | [GitHub trending](https://github.com/trending?since=daily) |
| 2 | [janhq/jan](https://github.com/janhq/jan) | Repositories | Jan is an open source alternative to ChatGPT that runs 100% offline on your computer. | 46k stars · +45 today | 1 | 60 | [GitHub trending](https://github.com/trending/rust?since=daily) |
| 3 | [LosaLosSantos/aurelio-finance](https://github.com/LosaLosSantos/aurelio-finance) | Repositories | Open-source personal finance app with an AI financial advisor: track your net worth, investments, ETFs, cash… | 352 stars · created 6 Oct | 1 | 60 | [GitHub](https://github.com/topics/fintech) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | Repositories | Knowledge infrastructure to make your agents smarter. | 206.4k stars · +1,006 today | 1 | 54 | [GitHub trending](https://github.com/trending?since=daily) |
| 5 | [vxcontrol/pentagi](https://github.com/vxcontrol/pentagi) | Repositories | Fully autonomous AI Agents system capable of performing complex penetration testing tasks | 34.8k stars · +60 today | 1 | 54 | [GitHub trending](https://github.com/trending/go?since=daily) |
| 6 | [Tencent/LoopForge](https://github.com/Tencent/LoopForge) | Repositories | Self-hosted workflows for coding-agent delivery. | 5.6k stars · +228 today | 1 | 48 | [GitHub trending](https://github.com/trending/go?since=daily) |
| 7 | [reality-opened/openreality](https://github.com/reality-opened/openreality) | Repositories | Open Reality: phone video to AI-queryable 3D scenes. | 661 stars · created 1 Sep | 1 | 48 | [GitHub](https://github.com/topics/robotics) |
| 8 | [talharaziq/Advanced-Bioinformatics](https://github.com/talharaziq/Advanced-Bioinformatics) | Repositories | A free, hands-on bioinformatics roadmap from Linux, Python & R to RNA-seq, genomics, Bioconductor, and… | 100 stars · created 21 Oct | 1 | 48 | [GitHub](https://github.com/topics/bioinformatics) |
| 9 | [t8y2/dbx](https://github.com/t8y2/dbx) | Repositories | 25 MB lightweight cross-platform database client for 100+ databases, including MySQL, PostgreSQL, SQLite… | 31.1k stars · +48 today | 1 | 42 | [GitHub trending](https://github.com/trending/rust?since=daily) |
| 10 | [Day 89: A Dead Service and a Private Container That Serves](https://dev.to/ndcodes/day-89-a-marker-in-the-file-and-a-grant-somewhere-else-1deo) | Posts | #devops, #ansible, #azure | 19 reactions · 0 comments | 1 | 42 | [Dev.to](https://dev.to/top/day) |

</details>

<sub>84 more in [Cloud & DevOps](industries/cloud-devops.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-cybersecurity"></a>

### Cybersecurity

Exploited and new vulnerabilities, attacks, defence and security tooling. **89 items** · [full list →](industries/cybersecurity.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Researcher plants 2m canaries into the AI supply chain. A privacy…](https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/) | Posts | #ai, #security | 11 score · 3 comments | **3** <sub>Lobsters, Ars Technica, Mastodon</sub> | 77 | [Lobsters](https://lobste.rs/) |
| 2 | [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | Repositories | A Claude Code skill bundle for bug hunting and external red-team work - 82 skills, 15 slash commands, 681… | 16.4k stars · +1,803 today | 1 | 60 | [GitHub trending](https://github.com/trending?since=daily) |
| 3 | [Vyber07/cyber-security](https://huggingface.co/datasets/Vyber07/cyber-security) | Datasets | Cybersecurity AI Knowledge Base — PhD-Level Dataset Overview This is the most… | 1,380 likes · 28.7k dl/30d | 1 | 60 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [vxcontrol/pentagi](https://github.com/vxcontrol/pentagi) | Repositories | Fully autonomous AI Agents system capable of performing complex penetration testing tasks | 34.8k stars · +60 today | 1 | 54 | [GitHub trending](https://github.com/trending/go?since=daily) |
| 5 | [Signal Blocks AI Agents From Reading Private Chats via Screenshots…](https://thehackernews.com/2026/11/signal-blocks-ai-agents-from-reading.html) | Headlines | Signal has announced that it will restrict screenshots by default to stop artificial intelligence (AI)… | The Hacker News · 21 Nov 09:49 | **2** <sub>The Hacker News, Mastodon</sub> | 53 | [The Hacker News](https://feeds.feedburner.com/TheHackersNews) |
| 6 | [nginx/nginx](https://github.com/nginx/nginx) | Repositories | The official NGINX Open Source repository. | 32.8k stars · +189 today | 1 | 38 | [GitHub trending](https://github.com/trending?since=daily) |
| 7 | [Thousands of UK fridges secured from hackers in secret operation](https://www.bbc.co.uk/news/articles/c6eq49zyx7p4o) | Headlines | — | BBC News · — | 1 | 35 | [Mastodon](https://mastodon.social/explore/links) |
| 8 | [GnuPG Security Advisory for GPGME](https://lists.gnupg.org/pipermail/gnupg-announce/2026q4/000517.html) | Discussions | Link to lists.gnupg.org | 248 pts · 98 comments | 1 | 33 | [Hacker News](https://news.ycombinator.com/) |
| 9 | [AI patching likely behind outages](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/2fff3b60524e) | Topics | Officials say rushed fixes for AI-found flaws, not hackers, likely downed Microsoft, FAA, banks. | — | 1 | 32 | [Bluesky](https://bsky.app/) |
| 10 | [FBI crime database reportedly hacked](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/906b49a87470) | Topics | The FBI is probing an apparent breach of its National Crime Information Center used by police. | — | 1 | 16 | [Bluesky](https://bsky.app/) |

</details>

<sub>79 more in [Cybersecurity](industries/cybersecurity.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-data-analytics"></a>

### Data & analytics

Databases, datasets, pipelines, analytics and BI. **44 items** · [full list →](industries/data-analytics.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [datazip-inc/olake-go](https://github.com/datazip-inc/olake-go) | Repositories | OLake Go: open-source replication from databases, Kafka and S3 to Apache Iceberg and Parquet. | 2.2k stars · +93 today | 1 | 60 | [GitHub trending](https://github.com/trending/go?since=daily) |
| 2 | [Vyber07/cyber-security](https://huggingface.co/datasets/Vyber07/cyber-security) | Datasets | Cybersecurity AI Knowledge Base — PhD-Level Dataset Overview This is the most… | 1,380 likes · 28.7k dl/30d | 1 | 60 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |
| 3 | [Angais/pixel-art-atlas-1.4m](https://huggingface.co/datasets/Angais/pixel-art-atlas-1.4m) | Datasets | Pixel Art Atlas · 1.4M Synthetic Sprites 1,409,404 synthetic game sprites with English… | 666 likes · 74k dl/30d | 1 | 55 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [malisper/pgrust](https://github.com/malisper/pgrust) | Repositories | Postgres rewritten in Rust, now faster than Postgres and Clickhouse | 6k stars · +17 today | 1 | 54 | [GitHub trending](https://github.com/trending/rust?since=daily) |
| 5 | [nvidia/USDCraft-10K](https://huggingface.co/datasets/nvidia/USDCraft-10K) | Datasets | USDCraft-10K: Simulation-Ready Articulated 3D Assets in OpenUSD USDCraft-10K is a… | 142 likes · 59.7k dl/30d | 1 | 50 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |
| 6 | [pola-rs/polars](https://github.com/pola-rs/polars) | Repositories | Extremely fast Query Engine for DataFrames, written in Rust | 40.4k stars · +23 today | 1 | 48 | [GitHub trending](https://github.com/trending/rust?since=daily) |
| 7 | [talharaziq/Advanced-Bioinformatics](https://github.com/talharaziq/Advanced-Bioinformatics) | Repositories | A free, hands-on bioinformatics roadmap from Linux, Python & R to RNA-seq, genomics, Bioconductor, and… | 100 stars · created 21 Oct | 1 | 48 | [GitHub](https://github.com/topics/bioinformatics) |
| 8 | [hasan6969macho-bit/vectorbt-avoria-analysis](https://github.com/hasan6969macho-bit/vectorbt-avoria-analysis) | Repositories | Vectorbt research code for Avoria analysis, built for reproducible strategy experiments. | 150 stars · created 18 Nov | 1 | 48 | [GitHub](https://github.com/topics/fintech) |
| 9 | [nvidia/simready-assets](https://huggingface.co/datasets/nvidia/simready-assets) | Datasets | Welcome to NVIDIA SimReady Assets Welcome to NVIDIA's open-source SimReady Assets… | 1,720 likes · 1.7M dl/30d | 1 | 45 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |
| 10 | [t8y2/dbx](https://github.com/t8y2/dbx) | Repositories | 25 MB lightweight cross-platform database client for 100+ databases, including MySQL, PostgreSQL, SQLite… | 31.1k stars · +48 today | 1 | 42 | [GitHub trending](https://github.com/trending/rust?since=daily) |

</details>

<sub>34 more in [Data & analytics](industries/data-analytics.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-web-frontend"></a>

### Web & frontend

Browsers, front-end frameworks, CSS, web platform and the CDN layer. **42 items** · [full list →](industries/web-frontend.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [swiper](https://www.jsdelivr.com/package/npm/swiper) | CDN traffic | Served from the jsDelivr CDN | 4.6B hits/week | 1 | 60 | [jsDelivr](https://www.jsdelivr.com/statistics) |
| 2 | [bootstrap](https://www.jsdelivr.com/package/npm/bootstrap) | CDN traffic | Served from the jsDelivr CDN | 3.4B hits/week | 1 | 56 | [jsDelivr](https://www.jsdelivr.com/statistics) |
| 3 | [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | Repositories | Knowledge infrastructure to make your agents smarter. | 206.4k stars · +1,006 today | 1 | 54 | [GitHub trending](https://github.com/trending?since=daily) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [vxcontrol/pentagi](https://github.com/vxcontrol/pentagi) | Repositories | Fully autonomous AI Agents system capable of performing complex penetration testing tasks | 34.8k stars · +60 today | 1 | 54 | [GitHub trending](https://github.com/trending/go?since=daily) |
| 5 | [hls.js](https://www.jsdelivr.com/package/npm/hls.js) | CDN traffic | Served from the jsDelivr CDN | 2B hits/week | 1 | 52 | [jsDelivr](https://www.jsdelivr.com/statistics) |
| 6 | [prebid-universal-creative](https://www.jsdelivr.com/package/npm/prebid-universal-creative) | CDN traffic | Served from the jsDelivr CDN | 1.5B hits/week | 1 | 48 | [jsDelivr](https://www.jsdelivr.com/statistics) |
| 7 | [Monuments of India, Part 3: Sixteen Statues Sculpted from…](https://dev.to/amananandrai/monuments-of-india-part-3-sixteen-statues-sculpted-from-photographs-a-rebuilt-mysore-palace-and-3bm) | Posts | #javascript, #threejs, #webdev | 14 reactions · 2 comments | 1 | 48 | [Dev.to](https://dev.to/top/day) |
| 8 | [How do I run a Python file from a Local HTML file](https://stackoverflow.com/questions/80018046/how-do-i-run-a-python-file-from-a-local-html-file) | Questions | #javascript, #python, #html | 2 score · 2 answers · 56 views | 1 | 45 | [Stack Overflow](https://stackoverflow.com/questions?tab=Hot) |
| 9 | [emoji-datasource-apple](https://www.jsdelivr.com/package/npm/emoji-datasource-apple) | CDN traffic | Served from the jsDelivr CDN | 1.5B hits/week | 1 | 44 | [jsDelivr](https://www.jsdelivr.com/statistics) |
| 10 | [t8y2/dbx](https://github.com/t8y2/dbx) | Repositories | 25 MB lightweight cross-platform database client for 100+ databases, including MySQL, PostgreSQL, SQLite… | 31.1k stars · +48 today | 1 | 42 | [GitHub trending](https://github.com/trending/rust?since=daily) |

</details>

<sub>32 more in [Web & frontend](industries/web-frontend.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-mobile"></a>

### Mobile

iOS, Android, phones, wearables and app stores. **28 items** · [full list →](industries/mobile.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Signal Blocks AI Agents From Reading Private Chats via Screenshots…](https://thehackernews.com/2026/11/signal-blocks-ai-agents-from-reading.html) | Headlines | Signal has announced that it will restrict screenshots by default to stop artificial intelligence (AI)… | The Hacker News · 21 Nov 09:49 | **2** <sub>The Hacker News, Mastodon</sub> | 53 | [The Hacker News](https://feeds.feedburner.com/TheHackersNews) |
| 2 | [Why there are still no non-WebKit browsers on iOS](https://blog.mozilla.org/en/mozilla/internet-policy/apple-ios-browser-engine-rules/) | Discussions | Link to blog.mozilla.org | 547 pts · 290 comments | 1 | 42 | [Hacker News](https://news.ycombinator.com/) |
| 3 | [appwrite/appwrite](https://github.com/appwrite/appwrite) | Repositories | The open-source cloud for agents & devs. | 58.5k stars · +51 today | 1 | 30 | [GitHub trending](https://github.com/trending/typescript?since=daily) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [chat](https://www.npmjs.com/package/chat) | Packages | Chat SDK — universal TypeScript toolkit for building multi-platform chat bots and AI agents on Slack, Teams… | 8.1M dl/week | 1 | 21 | [npm](https://www.npmjs.com/) |
| 5 | [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) | Repositories | Avoid common App Store and Google Play rejections. | 3.5k stars · +720 today | 1 | 19 | [GitHub trending](https://github.com/trending?since=daily) |
| 6 | [The Gemini app is now available on lower-memory Android devices.](https://blog.google/innovation-and-ai/products/gemini-app/gemini-lower-memory-devices/) | Headlines | The Google Gemini app now supports lower-memory Android devices. | Google AI blog · 18 Nov 18:00 | 1 | 15 | [Google AI blog](https://blog.google/technology/ai/rss/) |
| 7 | [Beat Watcher](https://www.producthunt.com/products/beat-watcher) | Product launches | Fast Apple Watch heart rate alerts you can share with family | Featured launch | 1 | 15 | [Product Hunt](https://www.producthunt.com/) |
| 8 | [Hollr](https://www.producthunt.com/products/hollr-3) | Product launches | Push-to-talk for your family, on iPhone and Apple Watch | Featured launch | 1 | 15 | [Product Hunt](https://www.producthunt.com/) |
| 9 | [Signal restricts mobile screenshots as it confronts ‘existential…](https://techcrunch.com/2026/11/21/signal-restricts-mobile-screenshots-as-it-confronts-existential-threat-of-ai-surveillance/) | Headlines | Signal is limiting users' ability to take screenshots in both its Android and iOS apps. | TechCrunch · 21 Nov 22:37 | 1 | 15 | [TechCrunch](https://techcrunch.com/feed/) |
| 10 | [BADBOX botnet returns with record-breaking 40 billion daily ad…](https://www.bleepingcomputer.com/news/security/badbox-30-botnet-returns-with-record-breaking-40-billion-daily-ad-requests/) | Headlines | The BADBOX malware found in a broad range of generic Android TV boxes has returned to large-scale ad-fraud… | BleepingComputer · 21 Nov 16:17 | 1 | 15 | [BleepingComputer](https://www.bleepingcomputer.com/feed/) |

</details>

<sub>18 more in [Mobile](industries/mobile.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-markets-economy"></a>

### Markets & economy

Stocks, rates, inflation, central banks, earnings, funding rounds, M&A, IPOs and layoffs. **172 items** · [full list →](industries/markets-economy.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [LosaLosSantos/aurelio-finance](https://github.com/LosaLosSantos/aurelio-finance) | Repositories | Open-source personal finance app with an AI financial advisor: track your net worth, investments, ETFs, cash… | 352 stars · created 6 Oct | 1 | 60 | [GitHub](https://github.com/topics/fintech) |
| 2 | [hasan6969macho-bit/vectorbt-avoria-analysis](https://github.com/hasan6969macho-bit/vectorbt-avoria-analysis) | Repositories | Vectorbt research code for Avoria analysis, built for reproducible strategy experiments. | 150 stars · created 18 Nov | 1 | 48 | [GitHub](https://github.com/topics/fintech) |
| 3 | [AI sell-off overshadows Anthropic IPO](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/a4c88fc56c85) | Topics | The Nasdaq erases 2026 gains in a $4 trillion wipeout despite Anthropic's stock market debut. | — | 1 | 44 | [Bluesky](https://bsky.app/) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [juspay/hyperswitch](https://github.com/juspay/hyperswitch) | Repositories | Open source, composable payments platform \| PCI compliant \| SaaS and Self-host options \| Enables… | 45.9k stars · +7 today | 1 | 36 | [GitHub trending](https://github.com/trending/rust?since=daily) |
| 5 | [Agent News](https://smithery.ai/server/theagenttimes/news) | MCP servers | The intelligence layer agents use before they act, sourced answers on the agent economy. | 43,392 uses | 1 | 30 | [Smithery](https://smithery.ai/) |
| 6 | [aowang-ai/awesome-finance-agents](https://github.com/aowang-ai/awesome-finance-agents) | Repositories | A curated, bilingual list of open-source finance agents, organized by financial function and reliability. | 109 stars · created 11 Oct | 1 | 30 | [GitHub](https://github.com/topics/fintech) |
| 7 | [Amazon closes in on $7.5bn deal to buy AI start-up Decart](https://news.google.com/rss/articles/CBMihAFBVV95cUxNTEFvVDlwcmNmNEl1WGpwZ3A3TzF3ZkNLSDFrUHA3XzY3REJxa3Jyc3pjUnVLdXdydFp3eTBYR1E1elQzVllDV1JQVzJENFNhV3RjVWl1eFB3dWFZS1BQWlRpTC1WZWZ1OV9CZmdhQnNtdmUxb25DWS16SEVodXVlRnBFUFQ?oc=5) | Headlines | Headline via Google News (Financial Times) | Financial Times · 21 Nov 18:21 | **2** <sub>Google News, Financial Times</sub> | 28 | [Google News](https://news.google.com/search?q=%22Amazon%22+AI+%28Bedrock+OR+Nova+OR+AWS%29&hl=en-US&gl=US&ceid=US%3Aen) |
| 8 | [jeokeo011222/quantbot](https://github.com/jeokeo011222/quantbot) | Repositories | QuantBot（AI 量化机器人）的全量源码。基于 **Go+React + TypeScript + Vite** 构建，通过 **Wails** 与 Go 后端通信，提供 A… | 95 stars · created 27 Aug | 1 | 24 | [GitHub](https://github.com/topics/fintech) |
| 9 | [Active Feature Acquisition by Distilling an Oracle Teacher](https://arxiv.org/abs/2611.26598) | Papers | Acquiring every feature of an instance is often costly: a measurement can carry a monetary price, a time… | cs.LG · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 10 | [Bond yield dynamics: a multi-country multi-horizon string model](https://arxiv.org/abs/2611.26466) | Papers | This article extends the forward rate curve model of Baaquie and Bouchaud (2004) and Le Coz and Bouchaud… | q-fin.ST · new | 1 | 15 | [arXiv](https://arxiv.org/) |

</details>

<sub>162 more in [Markets & economy](industries/markets-economy.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-fintech"></a>

### Fintech & payments

Banking, payments, lending, trading, insurance and finance infrastructure. **54 items** · [full list →](industries/fintech.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [LosaLosSantos/aurelio-finance](https://github.com/LosaLosSantos/aurelio-finance) | Repositories | Open-source personal finance app with an AI financial advisor: track your net worth, investments, ETFs, cash… | 352 stars · created 6 Oct | 1 | 60 | [GitHub](https://github.com/topics/fintech) |
| 2 | [Ngochiendev/vietqr-core](https://github.com/Ngochiendev/vietqr-core) | Repositories | Thư viện .NET & Web API hiệu năng cao xử lý mã QR thanh toán VietQR chuẩn NAPAS247 & EMVCo. | 154 stars · created 28 Oct | 1 | 54 | [GitHub](https://github.com/topics/fintech) |
| 3 | [hasan6969macho-bit/vectorbt-avoria-analysis](https://github.com/hasan6969macho-bit/vectorbt-avoria-analysis) | Repositories | Vectorbt research code for Avoria analysis, built for reproducible strategy experiments. | 150 stars · created 18 Nov | 1 | 48 | [GitHub](https://github.com/topics/fintech) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Stellar-Kolo/kolo-frontend](https://github.com/Stellar-Kolo/kolo-frontend) | Repositories | Kolo's Stellar community savings web app: Next.js member and admin dashboards, with wallet and Soroban… | 132 stars · created 9 Oct | 1 | 42 | [GitHub](https://github.com/topics/fintech) |
| 5 | [juspay/hyperswitch](https://github.com/juspay/hyperswitch) | Repositories | Open source, composable payments platform \| PCI compliant \| SaaS and Self-host options \| Enables… | 45.9k stars · +7 today | 1 | 36 | [GitHub trending](https://github.com/trending/rust?since=daily) |
| 6 | [Stellar-Pathfinder/stellar-pathfinder](https://github.com/Stellar-Pathfinder/stellar-pathfinder) | Repositories | A corridor-integrity monitor for the Stellar network. | 131 stars · created 6 Oct | 1 | 36 | [GitHub](https://github.com/topics/fintech) |
| 7 | [AI patching likely behind outages](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/2fff3b60524e) | Topics | Officials say rushed fixes for AI-found flaws, not hackers, likely downed Microsoft, FAA, banks. | — | 1 | 32 | [Bluesky](https://bsky.app/) |
| 8 | [aowang-ai/awesome-finance-agents](https://github.com/aowang-ai/awesome-finance-agents) | Repositories | A curated, bilingual list of open-source finance agents, organized by financial function and reliability. | 109 stars · created 11 Oct | 1 | 30 | [GitHub](https://github.com/topics/fintech) |
| 9 | [jeokeo011222/quantbot](https://github.com/jeokeo011222/quantbot) | Repositories | QuantBot（AI 量化机器人）的全量源码。基于 **Go+React + TypeScript + Vite** 构建，通过 **Wails** 与 Go 后端通信，提供 A… | 95 stars · created 27 Aug | 1 | 24 | [GitHub](https://github.com/topics/fintech) |
| 10 | [siqiwang0712-commits/financial-risk-agent](https://github.com/siqiwang0712-commits/financial-risk-agent) | Repositories | Evidence-grounded financial risk analysis from corporate filings, combining constrained LLM interpretation… | 75 stars · created 4 Sep | 1 | 18 | [GitHub](https://github.com/topics/fintech) |

</details>

<sub>44 more in [Fintech & payments](industries/fintech.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-crypto-web3"></a>

### Crypto & web3

Cryptocurrencies, blockchains, DeFi, stablecoins and tokenisation. **46 items** · [full list →](industries/crypto-web3.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Official Trump (TRUMP)](https://www.coingecko.com/en/coins/official-trump) | Crypto assets | Market-cap rank #134 | $0.888278 · +5.5% 24h | 1 | 60 | [CoinGecko](https://www.coingecko.com/en/highlights/trending-crypto) |
| 2 | [Bitcoin (BTC)](https://www.coingecko.com/en/coins/bitcoin) | Crypto assets | Market-cap rank #1 | $59,069.10 · +2.0% 24h | 1 | 56 | [CoinGecko](https://www.coingecko.com/en/highlights/trending-crypto) |
| 3 | [Pudgy Penguins (PENGU)](https://www.coingecko.com/en/coins/pudgy-penguins) | Crypto assets | Market-cap rank #130 | $0.004209 · -0.1% 24h | 1 | 52 | [CoinGecko](https://www.coingecko.com/en/highlights/trending-crypto) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [hasan6969macho-bit/vectorbt-avoria-analysis](https://github.com/hasan6969macho-bit/vectorbt-avoria-analysis) | Repositories | Vectorbt research code for Avoria analysis, built for reproducible strategy experiments. | 150 stars · created 18 Nov | 1 | 48 | [GitHub](https://github.com/topics/fintech) |
| 5 | [EVAA Protocol (EVAA)](https://www.coingecko.com/en/coins/evaa-protocol) | Crypto assets | Market-cap rank #676 | $3.39 · -44.4% 24h | 1 | 48 | [CoinGecko](https://www.coingecko.com/en/highlights/trending-crypto) |
| 6 | [Venice Token (VVV)](https://www.coingecko.com/en/coins/venice-token) | Crypto assets | Market-cap rank #60 | $24.89 · +13.6% 24h | 1 | 44 | [CoinGecko](https://www.coingecko.com/en/highlights/trending-crypto) |
| 7 | [Pearl (PEARL)](https://www.coingecko.com/en/coins/pearl-2) | Crypto assets | Market-cap rank #77 | $1.96 · +8.8% 24h | 1 | 40 | [CoinGecko](https://www.coingecko.com/en/highlights/trending-crypto) |
| 8 | [juspay/hyperswitch](https://github.com/juspay/hyperswitch) | Repositories | Open source, composable payments platform \| PCI compliant \| SaaS and Self-host options \| Enables… | 45.9k stars · +7 today | 1 | 36 | [GitHub trending](https://github.com/trending/rust?since=daily) |
| 9 | [Stellar-Pathfinder/stellar-pathfinder](https://github.com/Stellar-Pathfinder/stellar-pathfinder) | Repositories | A corridor-integrity monitor for the Stellar network. | 131 stars · created 6 Oct | 1 | 36 | [GitHub](https://github.com/topics/fintech) |
| 10 | [Akedo (AKE)](https://www.coingecko.com/en/coins/akedo) | Crypto assets | Market-cap rank #326 | $0.002797 · -44.5% 24h | 1 | 36 | [CoinGecko](https://www.coingecko.com/en/highlights/trending-crypto) |

</details>

<sub>36 more in [Crypto & web3](industries/crypto-web3.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-health-biotech"></a>

### Health & biotech

Medicine, biology, pharma, health systems and medtech. **49 items** · [full list →](industries/health-biotech.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Pill to treat pancreatic cancer hailed as 'biggest breakthrough in…](https://www.theguardian.com/society/2026/nov/20/pill-pancreatic-cancer-breakthrough-daraxonrasib) | Discussions | Link to theguardian.com | 884 pts · 203 comments | **2** <sub>Hacker News, Mastodon</sub> | 68 | [Hacker News](https://news.ycombinator.com/) |
| 2 | [heise3/ExtremaRank](https://github.com/heise3/ExtremaRank) | Repositories | Native R and Python sample-deletion robustness for omics: candidate certificates, minimum deletion bounds… | 288 stars · created 3 Oct | 1 | 60 | [GitHub](https://github.com/topics/bioinformatics) |
| 3 | [NingyuSUN/bioai-evidence-validator](https://github.com/NingyuSUN/bioai-evidence-validator) | Repositories | Evidence validation and policy engine for AI-assisted biological curation | 108 stars · created 17 Sep | 1 | 54 | [GitHub](https://github.com/topics/bioinformatics) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Paper Search](https://smithery.ai/server/adamamer20/paper-search-mcp-openai) | MCP servers | Search and download academic papers from arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, Semantic Scholar… | 59,106 uses | 1 | 48 | [Smithery](https://smithery.ai/) |
| 5 | [talharaziq/Advanced-Bioinformatics](https://github.com/talharaziq/Advanced-Bioinformatics) | Repositories | A free, hands-on bioinformatics roadmap from Linux, Python & R to RNA-seq, genomics, Bioconductor, and… | 100 stars · created 21 Oct | 1 | 48 | [GitHub](https://github.com/topics/bioinformatics) |
| 6 | [JkingYu/DiffExplorer](https://github.com/JkingYu/DiffExplorer) | Repositories | Differential analysis tool for coding-free researchers – instant statistical results and charts, ready for… | 96 stars · created 8 Sep | 1 | 42 | [GitHub](https://github.com/topics/bioinformatics) |
| 7 | [styczynski/bioseqdb](https://github.com/styczynski/bioseqdb) | Repositories | Genomic sequence storage, indexing and alignment inside PostgreSQL: https://bioseqdb.com/ | 96 stars · created 27 Sep | 1 | 36 | [GitHub](https://github.com/topics/bioinformatics) |
| 8 | [ssinder/bioinformatics-agent-skills](https://github.com/ssinder/bioinformatics-agent-skills) | Repositories | Agent Skills for computational biology — RNA-seq, single-cell, protein structure, molecular dynamics… | 77 stars · created 25 Oct | 1 | 30 | [GitHub](https://github.com/topics/bioinformatics) |
| 9 | [poplarity/GelFigure](https://github.com/poplarity/GelFigure) | Repositories | Turn a raw agarose gel image into a publication-ready figure in the browser. | 71 stars · created 18 Oct | 1 | 24 | [GitHub](https://github.com/topics/bioinformatics) |
| 10 | [sagirimo/BioDSH](https://github.com/sagirimo/BioDSH) | Repositories | The bioinformatics agent desktop for clinicians and wet-lab scientists — built on DeepSeek Harness. | 69 stars · created 31 Aug | 1 | 18 | [GitHub](https://github.com/topics/bioinformatics) |

</details>

<sub>39 more in [Health & biotech](industries/health-biotech.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-robotics-hardware"></a>

### Robotics & hardware

Robots, drones, embedded devices and consumer hardware. **40 items** · [full list →](industries/robotics-hardware.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [KingKongRobotics/jumper](https://github.com/KingKongRobotics/jumper) | Repositories |  Jumper — an crab robot. | 3.2k stars · created 28 Sep | 1 | 60 | [GitHub](https://github.com/topics/robotics) |
| 2 | [Mind2Act World: A Diagnostic Benchmark for Embodied Mind, Physical…](https://huggingface.co/papers/2611.26444) | Papers | Embodied intelligence aims to let robots perform complex physical tasks with human-like adaptability and… | 51 upvotes | 1 | 56 | [Hugging Face](https://huggingface.co/papers) |
| 3 | [Russia's war in Ukraine](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/8e54d320a7c8) | Topics | Overnight drone and missile strikes, Zaporizhzhia casualties, Kharkiv gains, and reported Russian troop… | — | 1 | 56 | [Bluesky](https://bsky.app/) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [OpenWAM-Official/OpenWAM](https://github.com/OpenWAM-Official/OpenWAM) | Repositories | Official repository for "OpenWAM: An Open, Modular Exploration Towards Systematic World–Action Model… | 1.2k stars · created 6 Sep | 1 | 54 | [GitHub](https://github.com/topics/robotics) |
| 5 | [NixOS bring-up on an Alibaba RISC-V board](https://feyor.sh/blog/nixos-bringup-on-an-alibaba-riscv-board/) | Posts | #hardware, #nix | 9 score · 1 comments | 1 | 52 | [Lobsters](https://lobste.rs/) |
| 6 | [nvidia/USDCraft-10K](https://huggingface.co/datasets/nvidia/USDCraft-10K) | Datasets | USDCraft-10K: Simulation-Ready Articulated 3D Assets in OpenUSD USDCraft-10K is a… | 142 likes · 59.7k dl/30d | 1 | 50 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |
| 7 | [reality-opened/openreality](https://github.com/reality-opened/openreality) | Repositories | Open Reality: phone video to AI-queryable 3D scenes. | 661 stars · created 1 Sep | 1 | 48 | [GitHub](https://github.com/topics/robotics) |
| 8 | [robosimstudio/robosimstudio](https://github.com/robosimstudio/robosimstudio) | Repositories | An open agentic toolkit for physics-based Real2Sim of Robot Manipulation Tasks | 645 stars · created 12 Oct | 1 | 42 | [GitHub](https://github.com/topics/robotics) |
| 9 | [Ask HN: What is your current hardware set up?](https://news.ycombinator.com/item?id=50587796) | Discussions | Discussion thread on HN | 5 pts · 6 comments | 1 | 38 | [Hacker News](https://news.ycombinator.com/ask) |
| 10 | [muellerberndt/cadence](https://github.com/muellerberndt/cadence) | Repositories | A brain that learns from live experience. | 643 stars · created 7 Sep | 1 | 36 | [GitHub](https://github.com/topics/robotics) |

</details>

<sub>30 more in [Robotics & hardware](industries/robotics-hardware.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-semiconductors"></a>

### Semiconductors & chips

Chip design, fabs, GPUs, accelerators and the supply chain. **74 items** · [full list →](industries/semiconductors.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [NixOS bring-up on an Alibaba RISC-V board](https://feyor.sh/blog/nixos-bringup-on-an-alibaba-riscv-board/) | Posts | #hardware, #nix | 9 score · 1 comments | 1 | 52 | [Lobsters](https://lobste.rs/) |
| 2 | [Open-Source FPGA The "startup idea" to "go big fast"](https://news.ycombinator.com/item?id=50595097) | Discussions | Discussion thread on HN | 2 pts · 10 comments | 1 | 45 | [Hacker News](https://news.ycombinator.com/ask) |
| 3 | [nvidia/simready-assets](https://huggingface.co/datasets/nvidia/simready-assets) | Datasets | Welcome to NVIDIA SimReady Assets Welcome to NVIDIA's open-source SimReady Assets… | 1,720 likes · 1.7M dl/30d | 1 | 45 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [bendlang/bend](https://github.com/bendlang/bend) | Repositories | Bend 2: a fast language that blocks AI mistakes via proof. | 25.7k stars · +51 today | 1 | 36 | [GitHub trending](https://github.com/trending/typescript?since=daily) |
| 5 | [How Jensen Huang Made Humiliation Routine at Nvidia](https://news.google.com/rss/articles/CBMihAFBVV95cUxOV2xjNVlQNGJaN0dDY0FnLXZORHhwdG9nRlRaSU0zRHpSOXkzZ1VQQkNuQ0VaZzJ5ODc0blhmUFZzOVdRXzhLUmYtcUZMd2hOam1yWmxfMVpoZGpfaFJ2MXh6aTBUTF9UNGFJWksydE9SdWMzRWJCeGRqRHJnT0k0Y3I5ak0?oc=5) | Headlines | Headline via Google News (The New York Times) | The New York Times · 22 Nov 08:09 | **2** <sub>Google News, New York Times</sub> | 28 | [Google News](https://news.google.com/search?q=Nvidia+AI&hl=en-US&gl=US&ceid=US%3Aen) |
| 6 | [Amazon closes in on $7.5bn deal to buy AI start-up Decart](https://news.google.com/rss/articles/CBMihAFBVV95cUxNTEFvVDlwcmNmNEl1WGpwZ3A3TzF3ZkNLSDFrUHA3XzY3REJxa3Jyc3pjUnVLdXdydFp3eTBYR1E1elQzVllDV1JQVzJENFNhV3RjVWl1eFB3dWFZS1BQWlRpTC1WZWZ1OV9CZmdhQnNtdmUxb25DWS16SEVodXVlRnBFUFQ?oc=5) | Headlines | Headline via Google News (Financial Times) | Financial Times · 21 Nov 18:21 | **2** <sub>Google News, Financial Times</sub> | 28 | [Google News](https://news.google.com/search?q=%22Amazon%22+AI+%28Bedrock+OR+Nova+OR+AWS%29&hl=en-US&gl=US&ceid=US%3Aen) |
| 7 | [torch](https://pypi.org/project/torch/) | Packages | Tensors and Dynamic neural networks in Python with strong GPU acceleration | 12.4M dl/week | 1 | 15 | [PyPI](https://pypi.org/) |
| 8 | [Current and former officials from the US and other countries…](https://www.techmeme.com/261122/p5#a261122p5) | Headlines | New York Times : Current and former officials from the US and other countries describe the Chinese spy… | Techmeme · 22 Nov 08:00 | 1 | 15 | [Techmeme](https://www.techmeme.com/feed.xml) |
| 9 | [Sources: Alice Huang associate Li Ming, whom Singapore charged with…](https://www.techmeme.com/261122/p1#a261122p1) | Headlines | Stu Woo / Wall Street Journal : Sources: Alice Huang associate Li Ming, whom Singapore charged with fraud in… | Techmeme · 22 Nov 06:45 | 1 | 15 | [Techmeme](https://www.techmeme.com/feed.xml) |
| 10 | [A tale of two Nvidias](https://techcrunch.com/2026/11/21/a-tale-of-two-nvidias/) | Headlines | We got two very different pictures of Nvidia — the company’s latest earnings report vs. | TechCrunch · 21 Nov 22:07 | 1 | 15 | [TechCrunch](https://techcrunch.com/feed/) |

</details>

<sub>64 more in [Semiconductors & chips](industries/semiconductors.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-climate-energy"></a>

### Climate & energy

Clean energy, grids, EVs, batteries, oil and gas, and climate. **37 items** · [full list →](industries/climate-energy.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Why Is the World Still Counting on Unproven Carbon Capture Technology?](https://www.propublica.org/article/carbon-capture-and-storage-climate-models) | Headlines | — | ProPublica · 21 Nov 11:00 | 1 | 30 | [Mastodon](https://mastodon.social/explore/links) |
| 2 | [UK, EU seal reset deal](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/def246ceebd1) | Topics | Andy Burnham's Brussels summit brings youth mobility, food trade and carbon market agreements. | — | 1 | 20 | [Bluesky](https://bsky.app/) |
| 3 | [The Democrats’ First Move After Their Big Win? A Giveaway to Big Oil.](https://newrepublic.com/article/217872/democrats-permitting-reform-baaja-big-oil-giveaway) | Headlines | — | The New Republic · 13 Nov 12:00 | 1 | 15 | [Mastodon](https://mastodon.social/explore/links) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Geehy Launches G32R502 1kW Bidirectional Inverter Solution](https://www.eetimes.com/geehy-launches-the-g32r502-1kw-fully-digital-bidirectional-energy-storage-inverter-solution/) | Headlines | Explore Geehy’s G32R502 1kW bidirectional energy storage inverter reference design, featuring digital… | EE Times · 20 Nov 08:00 | 1 | 15 | [EE Times](https://www.eetimes.com/feed/) |
| 5 | [Why tribal rights have become key to the energy permitting debate](https://www.canarymedia.com/articles/land-use/tribal-rights-energy-permitting-debate) | Headlines | For months, the climate world and the broader Democratic coalition have argued over whether the sweeping… | Canary Media · 20 Nov 22:30 | 1 | 15 | [Canary Media](https://www.canarymedia.com/rss.rss) |
| 6 | [Trump EPA keeps trying to kill Solar for All despite court losses](https://www.canarymedia.com/articles/solar/trump-epa-solar-for-all) | Headlines | This analysis and news roundup come from the Canary Media Weekly newsletter. | Canary Media · 20 Nov 18:22 | 1 | 15 | [Canary Media](https://www.canarymedia.com/rss.rss) |
| 7 | [New York awards ports $230M in repurposed offshore wind grants](https://www.canarymedia.com/articles/offshore-wind/new-york-ports-get-230m-boost-for-offshore-wind-other-industries) | Headlines | New York state is upgrading its ports for what it hopes will be a return to U.S. | Canary Media · 20 Nov 17:15 | 1 | 15 | [Canary Media](https://www.canarymedia.com/rss.rss) |
| 8 | [Senate OKs permitting bill that would boost clean and dirty energy](https://www.canarymedia.com/articles/clean-energy/senate-oks-permitting-bill-that-would-boost-clean-and-dirty-energy) | Headlines | A bipartisan bill that would make it easier to build energy infrastructure — both dirty and clean — has… | Canary Media · 20 Nov 15:00 | 1 | 15 | [Canary Media](https://www.canarymedia.com/rss.rss) |
| 9 | [It’s official: 2026 is the year of lost solar in North Carolina](https://www.canarymedia.com/articles/solar/2026-year-of-lost-solar-north-carolina) | Headlines | This spring, when North Carolina’s top utility regulator abruptly canceled bidding for new Duke Energy large… | Canary Media · 20 Nov 09:30 | 1 | 15 | [Canary Media](https://www.canarymedia.com/rss.rss) |
| 10 | [It’s another banner year for batteries in the US](https://www.canarymedia.com/articles/batteries/another-banner-year-us-energy-storage-installations) | Headlines | See more from Canary Media’s ​“Chart of the Week” column . | Canary Media · 20 Nov 09:30 | 1 | 15 | [Canary Media](https://www.canarymedia.com/rss.rss) |

</details>

<sub>27 more in [Climate & energy](industries/climate-energy.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-ecommerce-retail"></a>

### E-commerce & retail

Online and physical retail, marketplaces, logistics and shopping. **49 items** · [full list →](industries/ecommerce-retail.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Amazon closes in on $7.5bn deal to buy AI start-up Decart](https://news.google.com/rss/articles/CBMihAFBVV95cUxNTEFvVDlwcmNmNEl1WGpwZ3A3TzF3ZkNLSDFrUHA3XzY3REJxa3Jyc3pjUnVLdXdydFp3eTBYR1E1elQzVllDV1JQVzJENFNhV3RjVWl1eFB3dWFZS1BQWlRpTC1WZWZ1OV9CZmdhQnNtdmUxb25DWS16SEVodXVlRnBFUFQ?oc=5) | Headlines | Headline via Google News (Financial Times) | Financial Times · 21 Nov 18:21 | **2** <sub>Google News, Financial Times</sub> | 28 | [Google News](https://news.google.com/search?q=%22Amazon%22+AI+%28Bedrock+OR+Nova+OR+AWS%29&hl=en-US&gl=US&ceid=US%3Aen) |
| 2 | [Held While Waiting: What LLM Agent Sessions Reserve on Serverless…](https://arxiv.org/abs/2611.26480) | Papers | LLM agents spend nearly all their time waiting for the model. | cs.PF · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 3 | [Bowmark web data: LinkedIn, Amazon, YouTube, Reddit, Airbnb, Instagram](https://github.com/bowmark-ai/skill) | MCP servers | Web scraping and automation for AI agents: live prices, quotes, bookings, anything behind a login. | v8.234.0 · 22 Nov 06:36 | 1 | 15 | [MCP Registry](https://registry.modelcontextprotocol.io/) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Amazon is complaining about NYC Council on shipping labels, too](https://www.theverge.com/tech/1039564/amazon-nyc-council-packages-shipping-label) | Headlines | Amazon is leaving no venue unexplored in its fight against the New York City Council and the Delivery… | The Verge · 21 Nov 22:59 | 1 | 15 | [The Verge](https://www.theverge.com/rss/index.xml) |
| 5 | [Amazon’s first digital photo frame is up to 50 percent off for Black…](https://www.theverge.com/gadgets/1038762/amazon-alexa-photo-frame-black-friday-2026-deal-sale) | Headlines | Amazon only announced its first digital photo frame less than a month ago, but it’s already getting a… | The Verge · 21 Nov 17:00 | 1 | 15 | [The Verge](https://www.theverge.com/rss/index.xml) |
| 6 | [2026 marked a turning point for artificial dye removal from food](https://www.modernretail.co/podcasts/2026-artificial-dye-removal-from-food/?utm_campaign=modernretaildis&utm_medium=rss&utm_source=general-rss) | Headlines | U.S. food brands and retailers are phasing out artificial dyes as policy shifts and consumer demand increases. | Modern Retail · 21 Nov 06:00 | 1 | 15 | [Modern Retail](https://www.modernretail.co/feed/) |
| 7 | [Big-Box Briefing: Target faces off with Trader Joe’s, Quince and…](https://www.modernretail.co/operations/big-box-briefing-targets-retail-reset-means-facing-off-with-trader-joes-quince-and-homegoods/?utm_campaign=modernretaildis&utm_medium=rss&utm_source=general-rss) | Headlines | Target’s third-quarter earnings, released on Wednesday, gave investors confidence that it’s finding its… | Modern Retail · 20 Nov 15:30 | 1 | 15 | [Modern Retail](https://www.modernretail.co/feed/) |
| 8 | [On is making a bigger play for American shoppers, one store at a time](https://www.modernretail.co/operations/on-is-making-a-bigger-play-for-american-shoppers-one-store-at-a-time/?utm_campaign=modernretaildis&utm_medium=rss&utm_source=general-rss) | Headlines | Swiss sportswear brand On is gearing up for a bigger U.S. | Modern Retail · 20 Nov 06:00 | 1 | 15 | [Modern Retail](https://www.modernretail.co/feed/) |
| 9 | [Walmart’s convenience lures high-income shoppers](https://www.modernretail.co/operations/walmarts-convenience-lures-high-income-shoppers/?utm_campaign=modernretaildis&utm_medium=rss&utm_source=general-rss) | Headlines | For years, Walmart has won on cost. | Modern Retail · 20 Nov 06:00 | 1 | 15 | [Modern Retail](https://www.modernretail.co/feed/) |
| 10 | [Retailers ride the Grand Theft Auto VI wave with special promos](https://www.modernretail.co/marketing/retailers-ride-the-grand-theft-auto-vi-wave-with-special-promos/?utm_campaign=modernretaildis&utm_medium=rss&utm_source=general-rss) | Headlines | Retailers and brands mark GTA VI’s launch with food, delivery, tech and even cannabis promos as gamers take… | Modern Retail · 19 Nov 06:00 | 1 | 15 | [Modern Retail](https://www.modernretail.co/feed/) |

</details>

<sub>39 more in [E-commerce & retail](industries/ecommerce-retail.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-gaming-xr"></a>

### Gaming & XR

Games, studios, engines, consoles and VR/AR. **38 items** · [full list →](industries/gaming-xr.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [metacritic gta vi](https://trends.google.com/trending?geo=US&q=metacritic%20gta%20vi) | Searches | ‘Grand Theft Auto 6’ Is Being Review Bombed On Metacritic | 10000+ searches (US) | 1 | 60 | [Google Trends](https://trends.google.com/trending) |
| 2 | [Grand Theft Auto VI](https://en.wikipedia.org/wiki/Grand_Theft_Auto_VI) | Most-read articles | — | 393.3k views | 1 | 60 | [Wikipedia](https://en.wikipedia.org/wiki/Special:TopViews) |
| 3 | [vicki gta 6 voice actor](https://trends.google.com/trending?geo=US&q=vicki%20gta%206%20voice%20actor) | Searches | Who is Taryn Manning? GTA 6 Vicki actor and singer | 500+ searches (US) | 1 | 57 | [Google Trends](https://trends.google.com/trending) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Dead Keys: I Brought Back the Typing Games. Kiro Did the Heavy…](https://dev.to/earlgreyhot1701d/dead-keys-i-brought-back-the-typing-games-kiro-did-the-heavy-lifting-5gc2) | Posts | #ai, #kiro, #gamedev | 22 reactions · 7 comments | 1 | 54 | [Dev.to](https://dev.to/top/day) |
| 5 | [gta 6 chapter 2 mission list](https://trends.google.com/trending?geo=US&q=gta%206%20chapter%202%20mission%20list) | Searches | GTA 6: A guide to every mission and chapter | 500+ searches (US) | 1 | 51 | [Google Trends](https://trends.google.com/trending) |
| 6 | [criminal profile gta 6](https://trends.google.com/trending?geo=US&q=criminal%20profile%20gta%206) | Searches | GTA 6 Criminal Profile: How the system works | 200+ searches (US) | 1 | 48 | [Google Trends](https://trends.google.com/trending) |
| 7 | [Ocarina of Time remake](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/fb7b005a5b87) | Topics | Players stream Nintendo's new version of the Zelda classic, which scored 96 on Metacritic. | — | 1 | 40 | [Bluesky](https://bsky.app/) |
| 8 | [donnie gta 6](https://trends.google.com/trending?geo=US&q=donnie%20gta%206) | Searches | GTA 6's First Major Death Might Be The Most Disturbing In The Entire Franchise | 200+ searches (US) | 1 | 39 | [Google Trends](https://trends.google.com/trending) |
| 9 | [Grand Theft Auto](https://en.wikipedia.org/wiki/Grand_Theft_Auto) | Most-read articles | — | 103.3k views | 1 | 28 | [Wikipedia](https://en.wikipedia.org/wiki/Special:TopViews) |
| 10 | [GTA 6 Leaker Dangles a PC Port Behind a $15 Million Crypto Pump](https://decrypt.co/383756/gta-6-leaker-dangles-pc-port-15-million-crypto-pump) | Headlines | The anonymous leaker, Cyberleek, released a 209 GB Xbox build but is withholding the executable that could… | Decrypt · 21 Nov 19:01 | 1 | 15 | [Decrypt](https://decrypt.co/feed) |

</details>

<sub>28 more in [Gaming & XR](industries/gaming-xr.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-enterprise-saas"></a>

### Enterprise SaaS & productivity

Business software, productivity, collaboration and the enterprise market. **24 items** · [full list →](industries/enterprise-saas.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Vyber07/cyber-security](https://huggingface.co/datasets/Vyber07/cyber-security) | Datasets | Cybersecurity AI Knowledge Base — PhD-Level Dataset Overview This is the most… | 1,380 likes · 28.7k dl/30d | 1 | 60 | [Hugging Face](https://huggingface.co/datasets?sort=trending) |
| 2 | [toeverything/AFFiNE](https://github.com/toeverything/AFFiNE) | Repositories | There can be more than Notion and Miro. | 76.4k stars · +574 today | 1 | 42 | [GitHub trending](https://github.com/trending?since=daily) |
| 3 | [Day 89: A Dead Service and a Private Container That Serves](https://dev.to/ndcodes/day-89-a-marker-in-the-file-and-a-grant-somewhere-else-1deo) | Posts | #devops, #ansible, #azure | 19 reactions · 0 comments | 1 | 42 | [Dev.to](https://dev.to/top/day) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Tracer-Cloud/opensre](https://github.com/Tracer-Cloud/opensre) | Repositories | The open-source agent for CI/CD reliability. | 14.1k stars · +450 today | 1 | 36 | [GitHub trending](https://github.com/trending?since=daily) |
| 5 | [juspay/hyperswitch](https://github.com/juspay/hyperswitch) | Repositories | Open source, composable payments platform \| PCI compliant \| SaaS and Self-host options \| Enables… | 45.9k stars · +7 today | 1 | 36 | [GitHub trending](https://github.com/trending/rust?since=daily) |
| 6 | [A VS Code extension to turn ANY free chatbot website into an AI…](https://dev.to/effessdev/a-vs-code-extension-to-turn-any-free-chatbot-website-into-an-ai-agent-kind-of-1n21) | Posts | #ai, #programming, #opensource | 40 reactions · 42 comments | 1 | 36 | [Dev.to](https://dev.to/top/day) |
| 7 | [cfahlgren1/slack-moji](https://huggingface.co/spaces/cfahlgren1/slack-moji) | Demos (Spaces) | Describe an emoji. A tiny model paints it in your browser. | 76 likes | 1 | 35 | [Hugging Face](https://huggingface.co/spaces?sort=trending) |
| 8 | [Microsoft 365 Outage - Post Incident Report](https://tianyin.github.io/misc/pir_microsoft_365_11-12-2026.pdf) | Posts | #distributed, #pdf | 14 score · 7 comments | 1 | 24 | [Lobsters](https://lobste.rs/) |
| 9 | [chat](https://www.npmjs.com/package/chat) | Packages | Chat SDK — universal TypeScript toolkit for building multi-platform chat bots and AI agents on Slack, Teams… | 8.1M dl/week | 1 | 21 | [npm](https://www.npmjs.com/) |
| 10 | [0xPlaygrounds/rig](https://github.com/0xPlaygrounds/rig) | Repositories |  Build modular and scalable LLM Applications in Rust | 9.2k stars · +12 today | 1 | 18 | [GitHub trending](https://github.com/trending/rust?since=daily) |

</details>

<sub>14 more in [Enterprise SaaS & productivity](industries/enterprise-saas.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-education"></a>

### Education

Schools, universities, edtech, courses and learning resources. **26 items** · [full list →](industries/education.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Posterior Matching Distillation](https://huggingface.co/papers/2611.26629) | Papers | Diffusion distillation accelerates image and video generation by compressing a pretrained teacher's… | 37 upvotes | **2** <sub>Hugging Face, arXiv</sub> | 57 | [Hugging Face](https://huggingface.co/papers) |
| 2 | [talharaziq/Advanced-Bioinformatics](https://github.com/talharaziq/Advanced-Bioinformatics) | Repositories | A free, hands-on bioinformatics roadmap from Linux, Python & R to RNA-seq, genomics, Bioconductor, and… | 100 stars · created 21 Oct | 1 | 48 | [GitHub](https://github.com/topics/bioinformatics) |
| 3 | [cueback: What If Tutorials Waited for You?](https://dev.to/arjuncodess/cueback-what-if-tutorials-waited-for-you-4fec) | Posts | #devchallenge, #presagechallenge, #electron | 6 reactions · 0 comments | 1 | 18 | [Dev.to](https://dev.to/top/day) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Active Feature Acquisition by Distilling an Oracle Teacher](https://arxiv.org/abs/2611.26598) | Papers | Acquiring every feature of an instance is often costly: a measurement can carry a monetary price, a time… | cs.LG · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 5 | [AutoMaster: Autonomous Post-Training by Making the Same Model a…](https://arxiv.org/abs/2611.26510) | Papers | Task success alone does not specify which behaviors post-training should reinforce. | cs.CL · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 6 | [GLiDE: A Fast, Calibrated Decision Model Distilled from Reasoning…](https://arxiv.org/abs/2611.26509) | Papers | Decision models enable fast, confidence-aware decisions by scoring candidate answers in a single forward… | cs.AI · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 7 | [A Tutorial on Complementarity-Based Contact Models for Robotics](https://arxiv.org/abs/2611.26600) | Papers | Simulating rigid-body dynamics with contact is fundamental to robotics, from motion synthesis and control to… | cs.RO · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 8 | [Opinion: When should medical school start?](https://www.statnews.com/2026/11/21/stat-letters-to-editor-medical-school-pediatric-emergency-care/?utm_campaign=rss) | Headlines | STAT readers weigh in on shortening medical school, fixing pediatric emergency care, and more. | STAT News · 21 Nov 13:00 | 1 | 15 | [STAT News](https://www.statnews.com/feed/) |
| 9 | [ICE detention of Princeton scientist rattles academia](https://www.statnews.com/2026/11/20/princeton-researcher-eva-yi-xie-ice-detention-rattles-interational-scholars/?utm_campaign=rss) | Headlines | A graduate student who is a scientific researcher at Princeton was detained by ICE while traveling home… | STAT News · 20 Nov 22:19 | 1 | 15 | [STAT News](https://www.statnews.com/feed/) |
| 10 | [Google Says Schools Can’t Have Search Without AI. Some Are Finding a…](https://www.edsurge.com/news/google-says-schools-cant-have-search-without-ai-some-are-finding-a-way) | Headlines | Districts and filtering companies were blocking AI search results long before Google’s new policy. | EdSurge · 19 Nov 01:00 | 1 | 15 | [EdSurge](https://www.edsurge.com/articles_rss) |

</details>

<sub>16 more in [Education](industries/education.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-media-creator"></a>

### Media & creator economy

News media, video, streaming, music, social platforms and creators. **46 items** · [full list →](industries/media-creator.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Change one letter, ruin a movie](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/645e79ca5148) | Topics | Users swap a single letter in famous film titles to make silly versions like "Ghostbasters." | — | 1 | 60 | [Bluesky](https://bsky.app/) |
| 2 | [talharaziq/Advanced-Bioinformatics](https://github.com/talharaziq/Advanced-Bioinformatics) | Repositories | A free, hands-on bioinformatics roadmap from Linux, Python & R to RNA-seq, genomics, Bioconductor, and… | 100 stars · created 21 Oct | 1 | 48 | [GitHub](https://github.com/topics/bioinformatics) |
| 3 | [List of highest-grossing Indian films](https://en.wikipedia.org/wiki/List_of_highest-grossing_Indian_films) | Most-read articles | — | 122.7k views | 1 | 44 | [Wikipedia](https://en.wikipedia.org/wiki/Special:TopViews) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | Repositories | AI agent skill that researches any topic across Reddit, X, YouTube, HN, Polymarket, and the web - then… | 72.2k stars · +560 today | 1 | 42 | [GitHub trending](https://github.com/trending?since=daily) |
| 5 | [The Body (TV series)](https://en.wikipedia.org/wiki/The_Body_%28TV_series%29) | Most-read articles | — | 109.8k views | 1 | 32 | [Wikipedia](https://en.wikipedia.org/wiki/Special:TopViews) |
| 6 | [XiaoYouChR/Ghost-Downloader-3](https://github.com/XiaoYouChR/Ghost-Downloader-3) | Repositories | The only downloader you need. | 14.6k stars · +779 today | 1 | 30 | [GitHub trending](https://github.com/trending?since=daily) |
| 7 | [zhouxiaoka/autoclip](https://github.com/zhouxiaoka/autoclip) | Repositories | AutoClip｜一个链接，一键出片。开源 AI 视频剪辑桌面工具，将播客、访谈、课程等长视频自动剪成短视频，生成字幕、封面和发布文案，适配抖音、小红书、TikTok、Reels 与 YouTube… | 13k stars · +683 today | 1 | 24 | [GitHub trending](https://github.com/trending?since=daily) |
| 8 | [XXX (2002 film)](https://en.wikipedia.org/wiki/XXX_%282002_film%29) | Most-read articles | — | 92.3k views | 1 | 16 | [Wikipedia](https://en.wikipedia.org/wiki/Special:TopViews) |
| 9 | [TideCache: Efficient Hybrid LLM Serving with Transparent Cache…](https://arxiv.org/abs/2611.26619) | Papers | Hybrid architectures have become mainstream among open-weight language models. | cs.DC · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 10 | [Replication of Agentic Security Events: Audit and Investigation…](https://arxiv.org/abs/2611.26553) | Papers | Agents based on large language models (LLMs) can now delete files and send payments on behalf of their users. | cs.CR · new | 1 | 15 | [arXiv](https://arxiv.org/) |

</details>

<sub>36 more in [Media & creator economy](industries/media-creator.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-space-mobility"></a>

### Space & mobility

Launches, satellites, aviation, autonomous vehicles and transport. **43 items** · [full list →](industries/space-mobility.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [AI patching likely behind outages](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/2fff3b60524e) | Topics | Officials say rushed fixes for AI-found flaws, not hackers, likely downed Microsoft, FAA, banks. | — | 1 | 32 | [Bluesky](https://bsky.app/) |
| 2 | [UK, EU seal reset deal](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/def246ceebd1) | Topics | Andy Burnham's Brussels summit brings youth mobility, food trade and carbon market agreements. | — | 1 | 20 | [Bluesky](https://bsky.app/) |
| 3 | [n8n-io/n8n stable](https://github.com/n8n-io/n8n/releases/tag/stable) | Releases | New release of n8n-io/n8n | stable · 20 Nov 09:37 | 1 | 15 | [GitHub releases](https://github.com/) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Tesla launches FSD v15, targets its biggest weaknesses, from signs…](https://electrek.co/2026/11/21/tesla-fsd-v15-rollout-25x-safety-reality-view/) | Headlines | Tesla has started rolling out “Full Self-Driving” v15, and its list of improvements reads like a list of… | Electrek · 21 Nov 20:56 | 1 | 15 | [Electrek](https://electrek.co/feed/) |
| 5 | [Waymo Pulls Robotaxis from Highways](https://cleantechnica.com/2026/11/21/waymo-pulls-robotaxis-from-highways/) | Headlines | Waymo has apparently run into some issues with its robotaxis on highways in California, and it has pulled… | CleanTechnica · 21 Nov 06:21 | 1 | 15 | [CleanTechnica](https://cleantechnica.com/feed/) |
| 6 | [Tractor Supply joins Uber Marketplace, adding delivery options for…](https://www.digitalcommerce360.com/2026/11/17/tractor-supply-joins-uber-marketplace-adding-delivery-options-for-rural-customers/) | Headlines | Tractor Supply Co. is adding Uber as a delivery partner, making its products available through the Uber… | Digital Commerce 360 · 17 Nov 19:00 | 1 | 15 | [Digital Commerce 360](https://www.digitalcommerce360.com/feed/) |
| 7 | [The sweet spot for constellation size](https://spacenews.com/the-sweet-spot-for-constellation-size/) | Headlines | In this episode of Space Minds, SpaceNews’ Mike Gruss speaks with Jan Smolders, the chief commercial officer… | SpaceNews · 19 Nov 18:25 | 1 | 15 | [SpaceNews](https://spacenews.com/feed/) |
| 8 | [Making the case for optical](https://spacenews.com/making-the-case-for-optical/) | Headlines | In this episode of Space Minds, SpaceNews’ Mike Gruss speaks with Jean-François Morizur, the co-founder and… | SpaceNews · 19 Nov 16:38 | 1 | 15 | [SpaceNews](https://spacenews.com/feed/) |
| 9 | [Flexell Space and ALATYR Sign MoU to Explore Solar Power Solutions…](https://spacenews.com/flexell-space-and-alatyr-sign-mou-to-explore-solar-power-solutions-for-orbital-data-centers/) | Headlines | – Collaboration to assess next-generation ultralight solar cells for space-based computing infrastructure… | SpaceNews · 18 Nov 23:02 | 1 | 15 | [SpaceNews](https://spacenews.com/feed/) |
| 10 | [All Points Logistics Announces Partnership with Expeditors for Space…](https://spacenews.com/all-points-logistics-announces-partnership-with-expeditors-for-space-prep-logistics-center-at-kennedy-space-center/) | Headlines | MERRITT ISLAND, FL, November 18, 2026 — All Points Logistics has announced a partnership with Expeditors… | SpaceNews · 18 Nov 21:31 | 1 | 15 | [SpaceNews](https://spacenews.com/feed/) |

</details>

<sub>33 more in [Space & mobility](industries/space-mobility.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-policy-regulation"></a>

### Policy & regulation

Laws, regulators, courts, antitrust, privacy and digital policy. **43 items** · [full list →](industries/policy-regulation.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Researcher plants 2m canaries into the AI supply chain. A privacy…](https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/) | Posts | #ai, #security | 11 score · 3 comments | **3** <sub>Lobsters, Ars Technica, Mastodon</sub> | 77 | [Lobsters](https://lobste.rs/) |
| 2 | [toeverything/AFFiNE](https://github.com/toeverything/AFFiNE) | Repositories | There can be more than Notion and Miro. | 76.4k stars · +574 today | 1 | 42 | [GitHub trending](https://github.com/trending?since=daily) |
| 3 | [AltRA-Test: An Alternative Annotator Test for LLM Judges Without…](https://huggingface.co/papers/2611.26073) | Papers | Large language models (LLMs) are increasingly used as judges and graders to replace human annotators… | 23 upvotes | 1 | 20 | [Hugging Face](https://huggingface.co/papers) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) | Repositories | Avoid common App Store and Google Play rejections. | 3.5k stars · +720 today | 1 | 19 | [GitHub trending](https://github.com/trending?since=daily) |
| 5 | [Active Feature Acquisition by Distilling an Oracle Teacher](https://arxiv.org/abs/2611.26598) | Papers | Acquiring every feature of an instance is often costly: a measurement can carry a monetary price, a time… | cs.LG · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 6 | [Hybrid Retrieval for Government Scheme Search in English and Marathi](https://arxiv.org/abs/2611.26514) | Papers | Retrieving government schemes requires matching citizens' information needs to formal administrative… | cs.LG · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 7 | [Bond yield dynamics: a multi-country multi-horizon string model](https://arxiv.org/abs/2611.26466) | Papers | This article extends the forward rate curve model of Baaquie and Bouchaud (2004) and Le Coz and Bouchaud… | q-fin.ST · new | 1 | 15 | [arXiv](https://arxiv.org/) |
| 8 | [The UN fails to agree on rules regulating ‘killer robots’](https://www.theverge.com/tech/1039554/un-regulations-killer-robots) | Headlines | One of the items on the agenda for UN diplomats meeting in Geneva this week was working towards rules… | The Verge · 21 Nov 21:03 | 1 | 15 | [The Verge](https://www.theverge.com/rss/index.xml) |
| 9 | [Trump EPA keeps trying to kill Solar for All despite court losses](https://www.canarymedia.com/articles/solar/trump-epa-solar-for-all) | Headlines | This analysis and news roundup come from the Canary Media Weekly newsletter. | Canary Media · 20 Nov 18:22 | 1 | 15 | [Canary Media](https://www.canarymedia.com/rss.rss) |
| 10 | [Senate OKs permitting bill that would boost clean and dirty energy](https://www.canarymedia.com/articles/clean-energy/senate-oks-permitting-bill-that-would-boost-clean-and-dirty-energy) | Headlines | A bipartisan bill that would make it easier to build energy infrastructure — both dirty and clean — has… | Canary Media · 20 Nov 15:00 | 1 | 15 | [Canary Media](https://www.canarymedia.com/rss.rss) |

</details>

<sub>33 more in [Policy & regulation](industries/policy-regulation.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="ind-other"></a>

### Other

Items that no rule matched. They still count; nothing is dropped. **82 items** · [full list →](industries/other.md)

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [My monitor was cutting my download speed by 75%](https://blog.tymscar.com/posts/studiodisplayethernet/) | Discussions | Link to blog.tymscar.com | 555 pts · 265 comments | **2** <sub>Hacker News, Lobsters</sub> | 73 | [Hacker News](https://news.ycombinator.com/) |
| 2 | [Hurried Announcement: Alessandro Masullo GRH](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/) | Discussions | Link to math216.wordpress.com | 2,404 pts · 1,169 comments | 1 | 60 | [Hacker News](https://news.ycombinator.com/) |
| 3 | [Show HN: Zero C# – C# without a runtime or GC](https://onurgumus.github.io/zero-csharp/index.html) | Discussions | Link to onurgumus.github.io | 151 pts · 104 comments | 1 | 60 | [Hacker News](https://news.ycombinator.com/) |

<details>
<summary>Show 7 more</summary>

| # | Item | Type | Why it matters | Key metric | Seen on | Score | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Does anybody read their emails anymore?](https://news.ycombinator.com/item?id=50591050) | Discussions | Discussion thread on HN | 5 pts · 14 comments | 1 | 60 | [Hacker News](https://news.ycombinator.com/ask) |
| 5 | [#TextilesASong](https://mastodon.social/tags/textilesasong) | Hashtags | — | 353 posts / 2 days | 1 | 60 | [Mastodon](https://mastodon.social/explore/tags) |
| 6 | ['I'm not MAGA,' Elon Musk says after Republicans' midterm thrashing](https://www.pbs.org/newshour/politics/im-not-maga-elon-musk-says-after-republicans-midterm-thrashing) | Headlines | — | PBS News · 19 Nov 18:09 | 1 | 60 | [Mastodon](https://mastodon.social/explore/links) |
| 7 | [Lean verification of the Riemann Hypothesis](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) | Discussions | Link to leanprover-community.github.io | 954 pts · 810 comments | 1 | 57 | [Hacker News](https://news.ycombinator.com/) |
| 8 | [TODOs JJ Style](https://bwc9876.dev/blog/jj_todo/) | Posts | #vcs | 47 score · 9 comments | 1 | 56 | [Lobsters](https://lobste.rs/) |
| 9 | [Riemann hypothesis](https://en.wikipedia.org/wiki/Riemann_hypothesis) | Most-read articles | — | 388.3k views | 1 | 56 | [Wikipedia](https://en.wikipedia.org/wiki/Special:TopViews) |
| 10 | [#Caturday](https://mastodon.social/tags/caturday) | Hashtags | — | 720 posts / 2 days | 1 | 56 | [Mastodon](https://mastodon.social/explore/tags) |

</details>

<sub>72 more in [Other](industries/other.md).</sub>

<sub>[↑ Industry map](#map)</sub>

<a id="by-source"></a>

## By source

One line per source with its #1 item. The full lists are in [today's archive file](archive/2026/11/2026-11-22.md). Click a group to open it.

<a id="src-github"></a>

<details>
<summary><b>GitHub</b> · 86 items from 8/8 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [GitHub trending · today](https://github.com/trending?since=daily) | 16 | [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 16.4k stars · +1,803 today |
| [GitHub trending · Python](https://github.com/trending/python?since=daily) | 10 | [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 16.4k stars · +1,803 today |
| [GitHub trending · TypeScript](https://github.com/trending/typescript?since=daily) | 10 | [cursor/plugins](https://github.com/cursor/plugins) | 18.2k stars · +260 today |
| [GitHub trending · Rust](https://github.com/trending/rust?since=daily) | 10 | [janhq/jan](https://github.com/janhq/jan) | 46k stars · +45 today |
| [GitHub trending · Go](https://github.com/trending/go?since=daily) | 10 | [datazip-inc/olake-go](https://github.com/datazip-inc/olake-go) | 2.2k stars · +93 today |
| [GitHub · young repos tagged robotics](https://github.com/topics/robotics) | 10 | [KingKongRobotics/jumper](https://github.com/KingKongRobotics/jumper) | 3.2k stars · created 28 Sep |
| [GitHub · young repos tagged bioinformatics](https://github.com/topics/bioinformatics) | 10 | [heise3/ExtremaRank](https://github.com/heise3/ExtremaRank) | 288 stars · created 3 Oct |
| [GitHub · young repos tagged fintech](https://github.com/topics/fintech) | 10 | [LosaLosSantos/aurelio-finance](https://github.com/LosaLosSantos/aurelio-finance) | 352 stars · created 6 Oct |

</details>

<a id="src-hn"></a>

<details>
<summary><b>Hacker News</b> · 35 items from 3/3 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [Hacker News · front page](https://news.ycombinator.com/) | 20 | [Hurried Announcement: Alessandro Masullo GRH](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/) | 2,404 pts · 1,169 comments |
| [Hacker News · Show HN (last 24 h)](https://news.ycombinator.com/show) | 7 | [Show HN: Zero C# – C# without a runtime or GC](https://onurgumus.github.io/zero-csharp/index.html) | 151 pts · 104 comments |
| [Hacker News · Ask HN (last 24 h)](https://news.ycombinator.com/ask) | 8 | [Does anybody read their emails anymore?](https://news.ycombinator.com/item?id=50591050) | 5 pts · 14 comments |

</details>

<a id="src-ai"></a>

<details>
<summary><b>Models & labs</b> · 63 items from 8/8 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [Hugging Face · trending models](https://huggingface.co/models?sort=trending) | 15 | [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini) | 3,301 likes · 7.9k dl/30d |
| [OpenRouter · newest models](https://openrouter.ai/models) | 10 | [Thinking Machines: Inkling 2 Mini](https://openrouter.ai/thinkingmachines/inkling-2-mini) | $0.075 in / $0.3 out per 1M · 1M ctx |
| [Hugging Face · trending Spaces](https://huggingface.co/spaces?sort=trending) | 12 | [huggingface/moe-blogpost](https://huggingface.co/spaces/huggingface/moe-blogpost) | 812 likes |
| [Hugging Face · trending datasets](https://huggingface.co/datasets?sort=trending) | 12 | [Vyber07/cyber-security](https://huggingface.co/datasets/Vyber07/cyber-security) | 1,380 likes · 28.7k dl/30d |
| [OpenAI News](https://openai.com/news/rss.xml) | 4 | [Combatting adversarial distillation](https://openai.com/index/combatting-adversarial-distillation) | OpenAI News · 20 Nov 11:00 |
| [Google AI blog](https://blog.google/technology/ai/rss/) | 4 | [Introducing Tool Retrieval in the Gemini API](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/) | Google AI blog · 19 Nov 19:00 |
| [Google DeepMind blog](https://deepmind.google/blog/rss.xml) | 2 | [Introducing Gemini 4 Neon](https://deepmind.google/blog/introducing-gemini-4-neon/) | Google DeepMind blog · 18 Nov 22:35 |
| [Hugging Face blog](https://huggingface.co/blog/feed.xml) | 4 | [Welcome Inkling 2 Mini, Cutting-edge Performance for your Local Setup](https://huggingface.co/blog/inkling2mini) | Hugging Face blog · 20 Nov 01:00 |

</details>

<a id="src-labs"></a>

<details>
<summary><b>AI labs & big players</b> · 209 items from 27/28 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [Anthropic · newsroom (public sitemap)](https://www.anthropic.com/news) | 8 | [Anthropic announces closing of initial public offering, including…](https://www.anthropic.com/news/ipo-close) | Anthropic · 20 Nov 13:41 |
| [Google · Gemini blog](https://blog.google/products/gemini/rss/) | 5 | [Get your year-end tasks done with new Connected Apps.](https://blog.google/products-and-platforms/products/search/connected-apps-holiday-errands/) | Google · 20 Nov 19:00 |
| [Microsoft Source · AI](https://news.microsoft.com/source/topics/ai/feed/) | 1 | [Microsoft and Salesforce Announce Copilotforce, Bringing Trusted…](https://news.microsoft.com/source/2026/11/17/microsoft-and-salesforce-announce-copilotforce-bringing-trusted-customer-context-and-action-into-microsoft-ai-experiences/) | Microsoft Source · 17 Nov 19:10 |
| [NVIDIA blog](https://blogs.nvidia.com/feed/) | 5 | [NVIDIA and Microsoft Expand Accelerated Computing From Azure to…](https://blogs.nvidia.com/blog/microsoft-ignite-accelerated-computing-azure-windows-pcs/) | NVIDIA blog · 19 Nov 21:00 |
| [AWS Machine Learning blog](https://aws.amazon.com/blogs/machine-learning/feed/) | 5 | [Meta ads is now available in AWS Quick](https://aws.amazon.com/blogs/machine-learning/meta-ads-is-now-available-in-aws-quick/) | AWS Machine Learning blog · 22 Nov 02:59 |
| [Apple Machine Learning Research](https://machinelearning.apple.com/rss.xml) | 5 | [Depth Pro 2: Sharp and Temporally Consistent Metric Monocular Depth](https://machinelearning.apple.com/research/depth-pro-2-monocular) | Apple Machine Learning Research · 20 Nov 01:00 |
| [OpenRouter · models added by the big labs (last 60 days)](https://openrouter.ai/models) | 27 | [Mistral: Pixtral Large 2502](https://openrouter.ai/mistralai/pixtral-large-2502) | $2 in / $6 out per 1M · 128k ctx |
| [Hugging Face · newest open-weight models from the big labs (last 30 days)](https://huggingface.co/models?sort=created) | 19 | [apple/DepthPro2-focal](https://huggingface.co/apple/DepthPro2-focal) | 20 likes · 236 dl/30d |
| [GitHub releases · AI lab SDKs and tools (last 14 days)](https://github.com/) | 20 | [google-gemini/gemini-cli Release v0.71.0-nightly.20261122.geecccfcd5](https://github.com/google-gemini/gemini-cli/releases/tag/v0.71.0-nightly.20261122.geecccfcd5) | Release… · 22 Nov 02:20 |
| [LMArena · text leaderboard](https://lmarena.ai/leaderboard/text) | skipped | — | HTTP 502 |
| [Google News · Anthropic](https://news.google.com/search?q=%22Anthropic%22+OR+%22Claude+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [Ross Gerber Urges Patience on Anthropic Stock - Anthropic (NASDAQ:ANT)](https://news.google.com/rss/articles/CBMitwFBVV95cUxOLTF6X0Z0VmU4eFBNWGh4NlhDX2VzODFSNXZtZVJHWEZ3NTI0ejYzamFWNDZSV240ZHhIVDhKdEVGakVpYUYxWFA4d19KYkZfQmM3RVBJR1hUajZpQTdLY1BaQ0Q0b29BYm5YUzd4RmhqdXVCRzBUQnIwa1FxNm1LeWgySWM5Q05rd2wzcVpYSWZWdU4zME9zMzRvMHZXQmlXU1RJWi1ab0lMNGN0VWNmcnVIQzFWaE0?oc=5) | Benzinga · 22 Nov 08:07 |
| [Google News · OpenAI](https://news.google.com/search?q=%22OpenAI%22&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [OpenAI patent describes earbuds that read silently mouthed words](https://news.google.com/rss/articles/CBMiigFBVV95cUxNNWZEUUhPZjkyS1BRWllRRHc2UnV0eXNsT1FkOUc5V0NuZXN5OXkxTDlPNFh2QjhnQlQ2MlRqV211U3BQRnVjZEtneTlhdDVBMEZLZEdqdjJ0YUdpWEhIOFZiT0UzRUVqMWd0YUFWY1RhaUo3UkQ0QUZrQkRLdVUzdzRGVXN1a2NycVE?oc=5) | PPC Land · 22 Nov 07:55 |
| [Google News · Google DeepMind & Gemini](https://news.google.com/search?q=%22Google+DeepMind%22+OR+%22Gemini%22+Google+AI&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [GTA 6-style AI photos flood Instagram: Gemini and ChatGPT prompts to…](https://news.google.com/rss/articles/CBMimAJBVV95cUxQeWRZMUZzbWU3bmZEQ09fVk9HcWZYT1NOQWE2QnFMNkxybEpELWhNak5BcDRFVF8tZ2RhTXBOaDZNaUZQSUpNTVRMVEFNSFVjUU1PNE96Zi1aVmdiZWUwVEl5MkREeGV3RVpaNnd5NU1QcFV1dWI1SUQ4cWRfX2NMM3phdVlVcU9yekFIX05NN0h2NjdlbzNkZzAybUdUSUoxeWJ6ZnA4eUVmVERkV2ZHbU1UZm5aUjY4TFI3Z19WNkQwYjhUTnBtcFpNUXpKY3pRUDhwVGhIcEJZOVFfMU1rVmpCRnU1b0RSNEdzMEpRUlg2LWh0YXZUcC1FdzZPOG9Dbk9ySXBMVkZDcUxHRVA3ampTYVY3NW1L0gGeAkFVX3lxTE5udGx1TmVwdmc3VURObV9xM2VfSVhTa194ZkxWRkNuVENHeF9LdXFfWnVWNk12bHQ0dHMyRllHWEFoaVJNclplcVpINEEwMDZId3ctR3U3Z01fNFBjUGEyc2JGbTFQd0UzcnhfdXBqTXZxLTJNelJGUGk4ek1VVWM0UWtNZXlfUm84LWtYYlpXQXZUWHdCOGMxOUFMNnJQNzRsaUU3V2I0RkNuZktzSVctT1RRTTdXWkJPTGF1WWlNTnNTY0d5dTJCSG1OUVh3QVE2LVQ4RERSLWFyUlhfLWszUmpaSXF3dWFrZFo4Z3JHTHQwamUyazBjMnNnT3FfU3Y4ZUNOUlk2T0l5dmR5SHBzTnhpXzZXTm5ZWGRaNUE?oc=5) | The Times of India · 22 Nov 06:47 |
| [Google News · Meta AI](https://news.google.com/search?q=%22Meta+AI%22+OR+%22Meta+Superintelligence%22+OR+%22Llama%22+Meta&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [Meta AI Chief Mocks Apple Over Rumored Agent](https://news.google.com/rss/articles/CBMihwFBVV95cUxNUDBRUU9Yd0YzaFhwUjJKQ1UyR3NndWZoSE1DNVhIalVscnN2VTZwZ2t5V0xybVlBNW0tdnRPZVdpMHhnLVFDdHhNT2x3SUNHWlE3SFJsREdRU3NTcU9XWU44VGEtMmxhUlZYdFVTVWg0Ymw2emxURHZNUWxRaXBVVWJkN3ZjMEE?oc=5) | Wisevoter · 22 Nov 07:10 |
| [Google News · Microsoft AI](https://news.google.com/search?q=%22Microsoft+AI%22+OR+%22Microsoft+Copilot%22&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [As NASA's Voyager 1 reaches one light-day from Earth, Microsoft AI…](https://news.google.com/rss/articles/CBMitAJBVV95cUxPVFRZQzloamJkRE40M2pJREVaeHlxbC10ejRFcXZkWFU1Sk1aY2ltWVppRnJrb0Njek9TRlVVa21WdFpORTZwdDV2aVcwLUJyNml6NVlJenBLeXcyWk9zYThseU9xa0d0b1J6amV5cmFzV0lUY3F3RzVHWm1ib3RkUkhUTDdxVFlHbTFnb0xJT0M1dGhqYVlzMHJJdmt4TkstZXcyWmV2YmVVdU1fZk9VaFl3RWJUbFhVX3R4S09uMW1lWGtINXEzcjE4NndIWGstcnVndERBM2M5MjUybWZoaS1HUTVrd1NjMXpuQXhpbXJCd1FXUlZENm42NnZpbUVWRFFZQnNDNmFfYjBPY19VMnZiaGxyX1RmS1JEZDdEcVZvZVZ0MG0yQTdfVFp0X09lTnE2edIBugJBVV95cUxQTUNKVlFja3M0cmVqY3ZWSXlXVnZac0swMlJ4SDhrcFBkR1lOTVJlMFlHczJtMzRsYnVYSnJwdWVLczdPaXowRTdDMS1JOVp6QzVGb2h0ZzRlVGZNY1g2LU55LWpXcFQ4S3BIRVBSSWJ4OENleVBOZnN0c3ZZZDlCbkM3ZFpWLWhROFd3UlJvRm5OeWl2U3NCcm1JOEs3WGU5LUJKMmVTWnV1cllqZVV3MFZqM2lxV3hlMG9ZVUlaODhFVV80RTI3d1JhQ202SjlLX0tibGlfUFgwLTVNQWZ3MFNlTjNEMnlTR2FvbDNsMXltazZTSmtFaXBvQlJrdENJQ21ONEtockxkSG9GMnBpN1ZBdUdLSjJmMFdOWDlmSlU5VEdXX0VyNTJ5WXJCZkdsUXJ3Y2YxOVVodw?oc=5) | The Times of India · 22 Nov 04:09 |
| [Google News · xAI](https://news.google.com/search?q=%22xAI%22+Musk+AI&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [Elon Musk’s AI ‘Grok’ Officially Arrives on iPhone CarPlay](https://news.google.com/rss/articles/CBMiqgFBVV95cUxOaURsZWl5cHZETElmRVBZams2dlpFNEZ4SjlWMm1BR1A4VktqZVVYS0ZVU01xRWQxengzQzNUV1diMlNIRlZPTGFIeHZjUzhIaUZtRWh1cTNTWmhsdWpIUVZob2x4aHB3UDRDUTVURUstY0NRdG96LXBudmNHWkVlTmhrWWI4S29rRkY0UGhzV1d0eFhoMGVaRUpQNUF2d1lLMkpvODJPOXNDQQ?oc=5) | آي-فون إسلام · 21 Nov 09:36 |
| [Google News · Mistral AI](https://news.google.com/search?q=%22Mistral+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [Deutsche Telekom stock backs Mistral AI partnership with T.Capital](https://news.google.com/rss/articles/CBMiyAFBVV95cUxQWE51S0ZBMThLbkZEa0NFaHVWUmdla011N2U0UkM3LVZha1UybVpGTEVRMW5wZGJwb0oxVTV3dzNneXc5bGZqVWlxLV9SbndkS2JfaGZCTGw1aHQ5VFhmdUhmODRJYXNmTEtBYlFSa0Nrc0ZDcFlkUkhIN0FsVlR0NHpESHJhdk5vejM3Z005SkViQm14ZVgzSHNuOWhqTW1zY1p0dDloNFc2ZGh4dnloRXpCWFRRQUhET0F5RlpqVWduQzR5eU10Nw?oc=5) | ad-hoc-news.de · 21 Nov 11:56 |
| [Google News · Cohere](https://news.google.com/search?q=%22Cohere%22+AI&hl=en-US&gl=US&ceid=US%3Aen) | 3 | [Pichette tells committee his blind trust is not yet in place amid…](https://news.google.com/rss/articles/CBMivgFBVV95cUxPNVNBZmtXUlItT2N0NVUwamFLclVWQWhkN2ZzbVNUdlBvQkhLMEJYNC02Zkh6RWg3akFRZ2JWcGtrSVU5bFctX2lJdUxUNnBmODFKVWkzdWlkMEY5VkFScUtCN0NlblVQNGtpVVhPT3h2SUxtSmk1NFFxdF9qUHR4aXZCVHZKVm1EV3czWFZRUGdlVTNnZDlWRVRTekFIRUtyNzZYTW1DdUU3TE9ncjNiRFdZdUdfdm5jb2FmdzdR?oc=5) | The Hub \| More Signal. Less Noise. · 21 Nov 12:00 |
| [Google News · NVIDIA](https://news.google.com/search?q=Nvidia+AI&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [How Jensen Huang Made Humiliation Routine at Nvidia](https://news.google.com/rss/articles/CBMihAFBVV95cUxOV2xjNVlQNGJaN0dDY0FnLXZORHhwdG9nRlRaSU0zRHpSOXkzZ1VQQkNuQ0VaZzJ5ODc0blhmUFZzOVdRXzhLUmYtcUZMd2hOam1yWmxfMVpoZGpfaFJ2MXh6aTBUTF9UNGFJWksydE9SdWMzRWJCeGRqRHJnT0k0Y3I5ak0?oc=5) | The New York Times · 22 Nov 08:09 |
| [Google News · Amazon & AWS](https://news.google.com/search?q=%22Amazon%22+AI+%28Bedrock+OR+Nova+OR+AWS%29&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [Amazon to Acquire Israeli AI Startup Decart for $7.5 Billion](https://news.google.com/rss/articles/CBMiiAFBVV95cUxOeTlfTHFQZjVqbmhvOGYwWGN6RThtLXhSZlR2bzRTM21NZXpvTU16cUNBYUN2aGRXMllJczZXaXl3TWNZZGdEVXh2M0IwN2hQNzR4cVdzaHBidGFNVXFIRGFnc1h5d3owM0NpZXdDN1k5TDNMZGJnenloVjJ2ZDF0Q3o0cGtZLW9I?oc=5) | 조선일보 · 22 Nov 07:29 |
| [Google News · Apple](https://news.google.com/search?q=%22Apple+Intelligence%22+OR+%22Apple+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [Does Apple Intelligence Drain Your Battery? When, Why and How to Check](https://news.google.com/rss/articles/CBMiW0FVX3lxTE0yckliOGZsM2tyZW5VV290MjVDR3NxZmZvVVZjV1k5Skp1bkRMcFdmeWc5NUEyLXk4YUZOX0czcTQzUFhZanRpR1lVQi1GWVdibnRQVWhPNDZpM0k?oc=5) | Fello AI · 22 Nov 07:08 |
| [Google News · DeepSeek](https://news.google.com/search?q=DeepSeek&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [Unsloth revises DeepSeek GGUF benchmarks with longer contexts and…](https://news.google.com/rss/articles/CBMiQkFVX3lxTE9OcUVlTm5FNjB4LU1kSllkXzdqWUJFVkNLLUczcVNReUpYQVI5cmFXdHlGWTlKLUtyY1paMWlha1lGQQ?oc=5) | Digg · 22 Nov 02:08 |
| [Google News · Qwen & Alibaba](https://news.google.com/search?q=Qwen+OR+%22Alibaba%22+AI+model&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [Alibaba's Qwen4-Max Rollout Runs Into a Compute Wall](https://news.google.com/rss/articles/CBMiwgFBVV95cUxPdm1SS1NneHJJLTkyWFRVbS1OMGZxZV9OaXhfcDhVNkVaeEFNNG9hbW9OTXRTRW4yR2h6MjgxZ0c5d3FrZVk2ZTRmVVoxMDJKcGd6bGtLejUtbmNYV0FfNjBjSm13LUlJMHJhOE5KRnBGbF8zS1J4OFJJMHBiUUtaZ3FoMUpGRzFqNlY3OWFtUDlqcTRBSWp2d3MtMUhURDYtcEdmN29zQ19HTVpxVXNHQ2g2WG9FZEktaExnOERPYjdOUQ?oc=5) | ad-hoc-news.de · 22 Nov 03:11 |
| [Google News · Moonshot AI (Kimi)](https://news.google.com/search?q=%22Moonshot+AI%22+OR+Kimi+AI&hl=en-US&gl=US&ceid=US%3Aen) | 8 | [Moonshot Launches Kimi K3, an Open-Weight AI Model with 2.8 Trillion…](https://news.google.com/rss/articles/CBMirgFBVV95cUxNY1pCaFBqckY2SWhrWVhqQkR6N2RuN0lUM1JJd0d0cUE4WGV3U0VSM3Yxamh6YTBDT3A3TV8zaFp4ZGZ4VTRtWHRLb2J1SGI4ZzM0N2tyMzZHYkRuRnVIUFJKSmRfNHpWR2NaM0FMSmstTk5lNUJ0bDFMeW5tWFNRd25QUkFKZ2R3c3NZVHZPS2ZrVElCc0RwdlJKeTBob0pFV1ZBUG5adEl1UW9uaWc?oc=5) | VOI.ID · 22 Nov 04:34 |
| [Google News · Zhipu (Z.ai, GLM)](https://news.google.com/search?q=Zhipu+OR+%22Z.ai%22+GLM&hl=en-US&gl=US&ceid=US%3Aen) | 1 | [Tencent Hy4 vs GLM-5.5: One of These Models Does Not Exist](https://news.google.com/rss/articles/CBMiY0FVX3lxTE1renlMeUtkUmZldkszc0l1T3hNcV9FWVQwZHR6b0FaQ3Nqd2NlSGxMTHNXVFR0dGVQRDQyZDVHSG1TYVNBM0dzMUZ4VEJjNERHaUl4WF9HVlpPeFc4ODFoZlZoVQ?oc=5) | OrcaRouter · 20 Nov 14:59 |
| [Google News · Perplexity](https://news.google.com/search?q=%22Perplexity+AI%22+OR+%22Perplexity%22+Comet&hl=en-US&gl=US&ceid=US%3Aen) | 2 | [Judge Pauses Discovery in Amazon v. Perplexity](https://news.google.com/rss/articles/CBMikgFBVV95cUxQTjNPVW1HclB6bHJLYWNndFcxbzFSNFVvVEVzYTBRSnZRVmdoMm5lOGxlZHA5bF9ya1U0UERlRTczTkF2MG9hWnBMVl9jZTNiTzBoekNVOU13Rk44aXUtSG5qNGtId0FpY0dJdDdsQVMyeVh0WmdQYUpsVnhMUDB1WGF2VkVnUl9WNTlxdmRTeHg2dw?oc=5) | Wisevoter · 21 Nov 01:43 |
| [Google News · Hugging Face](https://news.google.com/search?q=%22Hugging+Face%22&hl=en-US&gl=US&ceid=US%3Aen) | 4 | [Hugging Face: Thinking Machines Lab releases Inkling 2 Mini, with AI…](https://news.google.com/rss/articles/CBMiREFVX3lxTE1hNS0xYWVJUnlsVDFLYmVpTnprLUs1SE9ILUt1TXBlSWZnX2JJcENrRUFBZkJySVFNdHpsZmhNRnhMU3JD?oc=5) | Digg · 21 Nov 19:56 |
| [Google News · Stability AI](https://news.google.com/search?q=%22Stability+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | 0 | — | nothing in the window today |

</details>

<a id="src-media"></a>

<details>
<summary><b>AI media</b> · 72 items from 8/9 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [Hugging Face · trending video, image and audio models](https://huggingface.co/models?sort=trending) | 30 | [apple/FastFrames-L](https://huggingface.co/apple/FastFrames-L) | 499 likes · 0 dl/30d |
| [LMArena · text-to-video leaderboard](https://lmarena.ai/leaderboard/text-to-video) | skipped | — | HTTP 502 |
| [LMArena · text-to-image leaderboard](https://lmarena.ai/leaderboard/text-to-image) | 10 | [GPT-Image-2.5 Sunburst](https://lmarena.ai/leaderboard) | rating 1429 · 73,040 votes |
| [ElevenLabs blog](https://elevenlabs.io/blog/rss.xml) | 5 | [Introducing video ad variants and localization in Ads Engine](https://elevenlabs.io/blog/video-variants-localization-ads-engine) | ElevenLabs blog · 20 Nov 22:12 |
| [Google News · AI media (Sora, Veo, Runway)](https://news.google.com/search?q=Sora+OpenAI+video+OR+%22Google+Veo%22+OR+%22Runway%22+AI+video&hl=en-US&gl=US&ceid=US%3Aen) | 1 | [Grok Imagine Video Generation: Prompts, 1080p & Pricing](https://news.google.com/rss/articles/CBMiX0FVX3lxTE5KYWd2cGpKLUVReWhBRDkteU83YmRIMkZ4TDZrbE9GUE9WRUxPNzFNWGZfQ09XTGh1ZU0zY0xqWXdwYVpXcmVoUzU3SFEyTWxucFpfNE1odW9NRERZRmdV?oc=5) | Fello AI · 21 Nov 05:22 |
| [Google News · AI media (Luma, Pika, Kling)](https://news.google.com/search?q=%22Luma+AI%22+OR+%22Pika%22+AI+video+OR+%22Kling%22+AI&hl=en-US&gl=US&ceid=US%3Aen) | 5 | [Best AI Video Generators in 2026: The Best Tools for Creating Videos…](https://news.google.com/rss/articles/CBMiaEFVX3lxTE1LeURxUjdPQWZhVVZWUkRwSXlCczl4Q1FITFVyUzY1WXJxdmEzRWVfN0paNEVmeUJTekoydlBwSjRlYzZIbjc0bGxmWkNORzdJa2FpN0g4OEVLcnlYVHZJcnBnR2FLYmhn0gFuQVVfeXFMT2dSVnFUVjlSMzNrMEVCdWM2UVhMTE03dEFXaTdsMXBSSHFsdlBUV1hVSVdja0VpanotMUNWbm1hUGpHZVVlbWdGMUhUTUhEcGNraDh0bGhBZTE1ZnprZWVYN2wwa1hEa3Z6clREY3c?oc=5) | TechloMedia · 22 Nov 00:26 |
| [Google News · AI media (Hailuo, Higgsfield, Midjourney)](https://news.google.com/search?q=Hailuo+OR+MiniMax+video+OR+Higgsfield+OR+Midjourney&hl=en-US&gl=US&ceid=US%3Aen) | 10 | [China's MiniMax founder loses over 90% of fortune as AI competition…](https://news.google.com/rss/articles/CBMiVEFVX3lxTE9tTzl2TTNfbXJYRnlJUzI5LUFKUjJKckUtSFFxRkFSV0t4eXFtMU95b1hRemtPWUNpVEVpTS0xNFFYZmYwb2dJTzA1UXRrX1lYZWYxNg?oc=5) | AzerNews · 22 Nov 06:00 |
| [Google News · AI media (FLUX, ElevenLabs, Suno)](https://news.google.com/search?q=%22Black+Forest+Labs%22+OR+FLUX+image+model+OR+ElevenLabs+OR+Suno&hl=en-US&gl=US&ceid=US%3Aen) | 1 | [Best AI Image Generator: Ranked by Blind Votes, Picked by Job](https://news.google.com/rss/articles/CBMiW0FVX3lxTE9pVXV1Q3VycnVLbkk2alBZY1VHUUZrUnczZjJDMkhnTE5RMmRQVzdyV0FKdnZ1OFl6anFCUjY5SGpZU1RTZklxbXJPRGV3UjlYWndzOUJqeFI5Z28?oc=5) | Fello AI · 19 Nov 12:36 |
| [Google News · AI media (Udio, HeyGen, Synthesia)](https://news.google.com/search?q=Udio+OR+HeyGen+OR+Synthesia+OR+%22Nano+Banana%22&hl=en-US&gl=US&ceid=US%3Aen) | 10 | [Best AI Video Generators in 2026: The Best Tools for Creating Videos…](https://news.google.com/rss/articles/CBMiaEFVX3lxTE1LeURxUjdPQWZhVVZWUkRwSXlCczl4Q1FITFVyUzY1WXJxdmEzRWVfN0paNEVmeUJTekoydlBwSjRlYzZIbjc0bGxmWkNORzdJa2FpN0g4OEVLcnlYVHZJcnBnR2FLYmhn0gFuQVVfeXFMT2dSVnFUVjlSMzNrMEVCdWM2UVhMTE03dEFXaTdsMXBSSHFsdlBUV1hVSVdja0VpanotMUNWbm1hUGpHZVVlbWdGMUhUTUhEcGNraDh0bGhBZTE1ZnprZWVYN2wwa1hEa3Z6clREY3c?oc=5) | TechloMedia · 22 Nov 00:26 |

</details>

<a id="src-ainews"></a>

<details>
<summary><b>AI news & newsletters</b> · 39 items from 10/10 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [The Decoder](https://the-decoder.com/feed/) | 6 | [Nvidia researchers argue huge AI context windows are a dead end](https://the-decoder.com/nvidia-researchers-argue-huge-ai-context-windows-are-a-dead-end/) | The Decoder · 21 Nov 17:23 |
| [TechCrunch · AI](https://techcrunch.com/category/artificial-intelligence/feed/) | 6 | [Signal restricts mobile screenshots as it confronts ‘existential…](https://techcrunch.com/2026/11/21/signal-restricts-mobile-screenshots-as-it-confronts-existential-threat-of-ai-surveillance/) | TechCrunch · 21 Nov 22:37 |
| [MIT Technology Review · AI](https://www.technologyreview.com/topic/artificial-intelligence/feed) | 6 | [The most misunderstood graph in AI just got a major update](https://www.technologyreview.com/2026/11/20/1149399/the-most-misunderstood-graph-in-ai-just-got-a-major-update/) | MIT Technology Review · 20 Nov 19:15 |
| [Import AI](https://importai.substack.com/feed) | 1 | [Import AI 481: AI sub-contractors; a wet lab for AI; and subterfuge…](https://importai.substack.com/p/import-ai-481-ai-sub-contractors) | Import AI · 16 Nov 15:01 |
| [Latent Space](https://www.latent.space/feed) | 6 | [\[AINews\] Riemann Hypothesis proved...twice independently](https://latent.space/p/ainews-riemann-hypothesis-proved-twice-independently/) | Latent Space · 21 Nov 06:02 |
| [Ben's Bites](https://www.bensbites.com/feed) | 2 | [My wife thinks AI is a person](https://www.bensbites.com/p/my-wife-thinks-ai-is-a-person) | Ben's Bites · 19 Nov 15:08 |
| [Last Week in AI](https://lastweekin.ai/feed) | 1 | [Last Week in AI #348 - IPO-&gt;Correction, new GPTs and Geminis…](https://lastweekin.ai/p/last-week-in-ai-348-ipo-correction) | Last Week in AI · 21 Nov 09:41 |
| [TLDR AI](https://tldr.tech/api/rss/ai) | 5 | [Gemini tool retrieval , Stripe evals methods , agent swarms ](https://tldr.tech/ai/2026-11-20) | TLDR AI · 20 Nov 01:00 |
| [The Rundown AI](https://www.therundown.ai/feed) | 6 | [GTA 6 rakes in $2.4B overnight](https://www.therundown.ai/articles/gta-6-rakes-in-2-4b-overnight) | The Rundown AI · 20 Nov 16:30 |
| [Interconnects](https://www.interconnects.ai/feed) | 0 | — | nothing in the window today |

</details>

<a id="src-research"></a>

<details>
<summary><b>Papers & preprints</b> · 76 items from 3/3 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [Hugging Face · daily papers](https://huggingface.co/papers) | 15 | [WeVisForensics: Self-Evolving Agent for Omni AI-Generated Video…](https://huggingface.co/papers/2611.21373) | 54 upvotes |
| [arXiv · newest by category](https://arxiv.org/) | 45 | [PlayCraft: Designing Engaging Games from Agent Play Experience](https://arxiv.org/abs/2611.26624) | cs.AI · new |
| [bioRxiv and medRxiv · newest preprints](https://www.biorxiv.org/) | 16 | [Trajectory fit alone does not identify causal edges: a white-box…](https://doi.org/10.64898/2026.09.22.753490) | bioRxiv · bioinformatics · new |

</details>

<a id="src-mcp"></a>

<details>
<summary><b>MCP registries</b> · 22 items from 2/2 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [MCP Registry · new and updated servers (24 h)](https://registry.modelcontextprotocol.io/) | 12 | [guessit-js](https://github.com/opensubtitles/guessit-js) | v5.3.0 · 22 Nov 08:04 |
| [Smithery · most-used MCP servers](https://smithery.ai/) | 10 | [Brave Search](https://smithery.ai/server/brave) | 87,579 uses |

</details>

<a id="src-packages"></a>

<details>
<summary><b>Packages & releases</b> · 102 items from 6/6 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [GitHub releases · major projects (last 72 h)](https://github.com/) | 17 | [ggml-org/llama.cpp b12628](https://github.com/ggml-org/llama.cpp/releases/tag/b12628) | b12628 · 22 Nov 07:58 |
| [npm · top packages for MCP, AI agents and LLMs](https://www.npmjs.com/) | 20 | [@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk) | 93.8M dl/week |
| [PyPI · latest releases of key AI and Python packages](https://pypi.org/) | 14 | [transformers](https://pypi.org/project/transformers/) | 27.6M dl/week |
| [crates.io · most downloaded recently](https://crates.io/) | 24 | [hashbrown](https://crates.io/crates/hashbrown) | 952.1M dl/90d |
| [jsDelivr · top npm packages by CDN hits this week](https://www.jsdelivr.com/statistics) | 15 | [swiper](https://www.jsdelivr.com/package/npm/swiper) | 4.6B hits/week |
| [Docker Hub · official images updated in the last 48 h](https://hub.docker.com/search?badges=official) | 12 | [postgres](https://hub.docker.com/_/postgres) | 12.6B pulls |

</details>

<a id="src-security"></a>

<details>
<summary><b>Vulnerabilities</b> · 30 items from 3/3 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [CISA KEV · known exploited vulnerabilities (last 14 days)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | 20 | [CVE-2026-129448](https://nvd.nist.gov/vuln/detail/CVE-2026-129448) | CVSS not scored · exploited |
| [NVD · critical CVEs published in the last 48 h](https://nvd.nist.gov/vuln/search) | 6 | [CVE-2026-125294](https://nvd.nist.gov/vuln/detail/CVE-2026-125294) | CVSS 9.8 |
| [ENISA EUVD · latest vulnerabilities](https://euvd.enisa.europa.eu/) | 4 | [EUVD-2026-131461](https://euvd.enisa.europa.eu/vulnerability/EUVD-2026-131461) | CVSS 9.4 |

</details>

<a id="src-econ"></a>

<details>
<summary><b>Markets & economy</b> · 150 items from 23/23 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [FRED · US markets and rates (St. Louis Fed)](https://fred.stlouisfed.org/) | 6 | [S&P 500](https://fred.stlouisfed.org/series/SP500) | 7175.83 (2026-11-19) |
| [ECB · euro reference rate (USD)](https://data.ecb.europa.eu/data/datasets/EXR) | 1 | [EUR/USD (ECB reference rate)](https://data.ecb.europa.eu/data/datasets/EXR) | 1.099 (2026-11-20) |
| [CNBC · top news](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114) | 8 | [Quantum computing’s first real-world payoff may come in energy, not…](https://www.cnbc.com/2026/11/22/quantum-computing-energy-applications.html) | CNBC · 22 Nov 07:00 |
| [CNBC · markets](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258) | 2 | [Tech outages are fueling a new doomsday economy](https://www.cnbc.com/2026/11/21/emergency-prep-spending-tech-outages.html) | CNBC · 21 Nov 16:04 |
| [CNBC · technology](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910) | 8 | [Quantum computing’s first real-world payoff may come in energy, not…](https://www.cnbc.com/2026/11/22/quantum-computing-energy-applications.html) | CNBC · 22 Nov 07:00 |
| [MarketWatch · top stories](https://feeds.content.dowjones.io/public/rss/mw_topstories) | 8 | [My husband is happily retired at 64 and thinks I should keep…](https://www.marketwatch.com/story/my-husband-is-happily-retired-at-64-and-thinks-i-should-keep-working-is-he-being-fair-325c5f38?mod=mw_rss_topstories) | MarketWatch · 22 Nov 02:15 |
| [Bloomberg · markets](https://feeds.bloomberg.com/markets/news.rss) | 8 | [China’s $1.7 Trillion AI Rout Turns Hot Trade Into Losing Bet](https://www.bloomberg.com/news/articles/2026-11-22/china-s-1-7-trillion-ai-rout-turns-hot-trade-into-losing-bet) | Bloomberg · 22 Nov 01:00 |
| [Bloomberg · technology](https://feeds.bloomberg.com/technology/news.rss) | 8 | [China Objects to US Curbs on Telecoms’ Access to Phone Numbers](https://www.bloomberg.com/news/articles/2026-11-22/china-objects-to-us-curbs-on-telecoms-access-to-phone-numbers) | Bloomberg · 22 Nov 03:44 |
| [Bloomberg · economics](https://feeds.bloomberg.com/economics/news.rss) | 6 | [US Consumers Are Holding Up Against Inflation Going Into Holiday…](https://www.bloomberg.com/news/articles/2026-11-21/us-consumers-are-holding-up-against-inflation-going-into-holiday-season) | Bloomberg · 21 Nov 22:00 |
| [Financial Times · home](https://www.ft.com/rss/home) | 8 | [A rocky road to Irish unity](https://www.ft.com/content/4d467ab8-00a7-4937-8775-30a42a00131f?syn-25a6b1a6=1) | Financial Times · 22 Nov 06:00 |
| [Financial Times · technology](https://www.ft.com/technology?format=rss) | 8 | [Tech suppliers raise AI server prices up to 45% months after deals…](https://www.ft.com/content/dd2a6594-6146-4ff1-ac8e-54749c1fc99f?syn-25a6b1a6=1) | Financial Times · 22 Nov 06:00 |
| [New York Times · business](https://rss.nytimes.com/services/xml/rss/nyt/Business.xml) | 8 | [Why Nostalgia for Tamagotchis, the Virtual Pets, Won’t Die](https://www.nytimes.com/2026/11/21/arts/tamagotchis-comeback.html) | New York Times · 22 Nov 02:05 |
| [New York Times · technology](https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml) | 8 | [Why Nostalgia for Tamagotchis, the Virtual Pets, Won’t Die](https://www.nytimes.com/2026/11/21/arts/tamagotchis-comeback.html) | New York Times · 22 Nov 02:05 |
| [BBC · business](https://feeds.bbci.co.uk/news/business/rss.xml) | 4 | [Sessions offer advice on rising energy costs](https://www.bbc.co.uk/news/articles/cmy49l3x893jo?at_medium=RSS&at_campaign=rss) | BBC · 21 Nov 13:09 |
| [The Guardian · business](https://www.theguardian.com/uk/business/rss) | 8 | [Unreal deals: the scam websites targeting Black Friday bargain hunters](https://www.theguardian.com/money/2026/nov/22/black-friday-scam-deals--ai-fake-storefront) | The Guardian · 22 Nov 08:00 |
| [The Economist · finance and economics](https://www.economist.com/finance-and-economics/rss.xml) | 6 | [Bond yields are rising everywhere—except China](https://www.economist.com/finance-and-economics/2026/11/19/bond-yields-are-rising-everywhere-except-china) | The Economist · 19 Nov 11:04 |
| [The Information](https://www.theinformation.com/feed) | 8 | [Amazon Nearing $7.5 Billion Purchase of Decart](https://www.theinformation.com/briefings/amazon-nearing-7-5-billion-purchase-decart) | The Information · 21 Nov 19:38 |
| [Crunchbase News](https://news.crunchbase.com/feed/) | 6 | [The Week’s 10 Biggest Funding Rounds: $400M For Neurotech Leads…](https://news.crunchbase.com/venture/biggest-startup-rounds-science-neurotech-model-ml-galvanize-therapeutics/) | Crunchbase News · 20 Nov 21:15 |
| [TechCrunch · venture](https://techcrunch.com/category/venture/feed/) | 1 | [Anthropic rival says companies can (mostly) skip the pricey models](https://techcrunch.com/2026/11/19/anthropic-rival-says-companies-can-mostly-skip-the-pricey-models/) | TechCrunch · 20 Nov 01:26 |
| [European Central Bank · press](https://www.ecb.europa.eu/rss/press.html) | 6 | [Christine Lagarde: Acting in time](https://www.ecb.europa.eu//press/key/date/2026/html/ecb.sp261120~e52bcc4db2.en.html) | European Central Bank · 20 Nov 09:30 |
| [Federal Reserve · press releases](https://www.federalreserve.gov/feeds/press_all.xml) | 4 | [Federal Reserve announces College Fed Challenge winners](https://www.federalreserve.gov/newsevents/pressreleases/other20261120b.htm) | Federal Reserve · 20 Nov 22:15 |
| [Google News · funding rounds and acquisitions](https://news.google.com/search?q=startup+raises+funding+round+OR+tech+acquisition+acquires&hl=en-US&gl=US&ceid=US%3Aen) | 10 | [Amazon to Acquire Israeli AI Startup Decart for $7.5 Billion](https://news.google.com/rss/articles/CBMiiAFBVV95cUxOeTlfTHFQZjVqbmhvOGYwWGN6RThtLXhSZlR2bzRTM21NZXpvTU16cUNBYUN2aGRXMllJczZXaXl3TWNZZGdEVXh2M0IwN2hQNzR4cVdzaHBidGFNVXFIRGFnc1h5d3owM0NpZXdDN1k5TDNMZGJnenloVjJ2ZDF0Q3o0cGtZLW9I?oc=5) | 조선일보 · 22 Nov 07:29 |
| [Google News · IPOs and layoffs](https://news.google.com/search?q=tech+IPO+shares+debut+OR+tech+layoffs+job+cuts&hl=en-US&gl=US&ceid=US%3Aen) | 10 | [EU mulls tax on Big Tech to boost budget](https://news.google.com/rss/articles/CBMirwFBVV95cUxNZEs5WGlWS1BsMjFXeE1ibUtNVmlyWS0yckNiSGJhS0JOVlNBenVtVFVuSnBPdEVObE9YX2Z2alV3Z3VDWlktNWlfR2ROUGxzQnJfWV96ZW55RFdkYmMxenhBbGJ0UDFNSnBaLUdjbEtaWDU1NlItWHQyZzlRMkk4RVJOV2RLUWlEck51MmpsMzRadGNoT21ocHFXTkw3bk1LUTVqUHZYZjJxbzhzXzRr0gG0AUFVX3lxTFAwMm1XamdGbGlucjRvN3FKRjFFdklETEt3X0t4ZW1rQWJiQUJ4TnFWb3hUTWMyNmJBWjZCazNTVGh0QUJOYlRTN1hUVklsaV9lc3AtcUNGWVhGYWJURzFKdzVMTndnUjlxUU53MXh4LTBFOWF6VnpzSmZWdGVZdGYwTTdiRG5vZnUxMHJiNEhiNGdZVXh4VGd0VjlVVG5hY296MHV4a1hvQlJoTEVDNWxWZ2FhSg?oc=5) | The Economic Times · 21 Nov 12:01 |

</details>

<a id="src-markets"></a>

<details>
<summary><b>Crypto & launches</b> · 40 items from 3/3 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [CoinGecko · trending coins (searches, 24 h)](https://www.coingecko.com/en/highlights/trending-crypto) | 15 | [Official Trump (TRUMP)](https://www.coingecko.com/en/coins/official-trump) | $0.888278 · +5.5% 24h |
| [CoinGecko · top 15 by market cap](https://www.coingecko.com/) | 15 | [Bitcoin (BTC)](https://www.coingecko.com/en/coins/bitcoin) | $59,041.00 · +1.3% 24h |
| [Launch Library 2 · next orbital launches](https://thespacedevs.com/llapi) | 10 | [Falcon 9 Block 5 \| NROL-136](https://ll.thespacedevs.com/2.2.0/launch/951a341f-236b-42fe-a667-4ab2fcf36eac/) | NET 22 Nov 13:23 · Go |

</details>

<a id="src-community"></a>

<details>
<summary><b>Community</b> · 52 items from 4/4 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [Lobsters · hottest](https://lobste.rs/) | 15 | [My Monitor Was Cutting My Download Speed by 75%](https://blog.tymscar.com/posts/studiodisplayethernet/) | 87 score · 7 comments |
| [Dev.to · top today](https://dev.to/top/day) | 10 | [The Chairs Are Back. The Coffee Is On. ](https://dev.to/thethirdcup/the-chairs-are-back-the-coffee-is-on-243p) | 94 reactions · 38 comments |
| [Stack Overflow · hot questions](https://stackoverflow.com/questions?tab=Hot) | 12 | [Is it significant to use size_t in place of int?](https://stackoverflow.com/questions/80018068/is-it-significant-to-use-size-t-in-place-of-int) | -1 score · 0 answers · 19 views |
| [Product Hunt · newest featured](https://www.producthunt.com/) | 15 | [Beat Watcher](https://www.producthunt.com/products/beat-watcher) | Featured launch |

</details>

<a id="src-news"></a>

<details>
<summary><b>Tech news</b> · 33 items from 9/9 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [Techmeme](https://www.techmeme.com/feed.xml) | 6 | [Current and former officials from the US and other countries…](https://www.techmeme.com/261122/p5#a261122p5) | Techmeme · 22 Nov 08:00 |
| [The Verge](https://www.theverge.com/rss/index.xml) | 6 | [Amazon is complaining about NYC Council on shipping labels, too](https://www.theverge.com/tech/1039564/amazon-nyc-council-packages-shipping-label) | The Verge · 21 Nov 22:59 |
| [TechCrunch](https://techcrunch.com/feed/) | 6 | [Signal restricts mobile screenshots as it confronts ‘existential…](https://techcrunch.com/2026/11/21/signal-restricts-mobile-screenshots-as-it-confronts-existential-threat-of-ai-surveillance/) | TechCrunch · 21 Nov 22:37 |
| [Ars Technica](https://feeds.arstechnica.com/arstechnica/technology-lab) | 1 | [Researcher plants 2m canaries into the AI supply chain. A privacy…](https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/) | Ars Technica · 20 Nov 21:59 |
| [LWN.net](https://lwn.net/headlines/rss) | 0 | — | nothing in the window today |
| [The Hacker News](https://feeds.feedburner.com/TheHackersNews) | 6 | [OpenRouter Drops 3 Providers After Researchers Catch Months of…](https://thehackernews.com/2026/11/openrouter-drops-3-providers-after.html) | The Hacker News · 22 Nov 06:06 |
| [BleepingComputer](https://www.bleepingcomputer.com/feed/) | 4 | [Rackspace Spot breach let hackers access customer Kubernetes secrets](https://www.bleepingcomputer.com/news/security/rackspace-spot-breach-let-hackers-access-customer-kubernetes-secrets/) | BleepingComputer · 21 Nov 23:59 |
| [GitHub Changelog](https://github.blog/changelog/feed/) | 2 | [Security advisory permissions are now generally available](https://github.blog/changelog/2026-11-20-security-advisory-permissions-are-now-generally-available) | GitHub Changelog · 20 Nov 22:49 |
| [Simon Willison](https://simonwillison.net/atom/everything/) | 2 | [Muru](https://simonwillison.net/2026/Nov/21/muru/) | Simon Willison · 22 Nov 00:56 |

</details>

<a id="src-industry-news"></a>

<details>
<summary><b>Industry outlets</b> · 179 items from 33/34 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [Finextra](https://www.finextra.com/rss/headlines.aspx) | 6 | [Closing the Dispute Gap: How Closer Collaboration Can Reduce…](https://www.finextra.com/event-info/646/closing-the-dispute-gap-how-closer-collaboration-can-reduce-chargebacks?utm_medium=rssfinextra&utm_source=finextrafeed) | Finextra · 17 Feb 16:00 |
| [PYMNTS](https://www.pymnts.com/feed/) | skipped | — | invalid XML (not well-formed (invalid token): line 121… |
| [CoinDesk](https://www.coindesk.com/arc/outboundfeeds/rss/) | 6 | [Bitcoin rebounds above $60,000 after $1.8 billion crypto liquidation…](https://www.coindesk.com/markets/2026/11/21/bitcoin-bounces-9-from-two-year-low-to-retake-usd60-000-as-traders-eye-monday-s-stock-open) | CoinDesk · 21 Nov 18:50 |
| [Decrypt](https://decrypt.co/feed) | 6 | [GTA 6 Leaker Dangles a PC Port Behind a $15 Million Crypto Pump](https://decrypt.co/383756/gta-6-leaker-dangles-pc-port-15-million-crypto-pump) | Decrypt · 21 Nov 19:01 |
| [STAT News](https://www.statnews.com/feed/) | 6 | [Opinion: When should medical school start?](https://www.statnews.com/2026/11/21/stat-letters-to-editor-medical-school-pediatric-emergency-care/?utm_campaign=rss) | STAT News · 21 Nov 13:00 |
| [The Robot Report](https://www.therobotreport.com/feed/) | 6 | [The manufacturing data gap holding back physical AI](https://www.therobotreport.com/the-manufacturing-data-gap-holding-back-physical-ai/) | The Robot Report · 21 Nov 23:25 |
| [IEEE Spectrum Robotics](https://spectrum.ieee.org/feeds/topic/robotics.rss) | 4 | [Video Friday: Drone Squeezes Itself to Fit Through Tight Spaces](https://spectrum.ieee.org/video-friday-morphing-robots-quadrotor) | IEEE Spectrum Robotics · 20 Nov 18:30 |
| [IEEE Spectrum Semiconductors](https://spectrum.ieee.org/feeds/topic/semiconductors.rss) | 2 | [Z2RAM Claims SRAM Memory Speeds at Much Greater Density](https://spectrum.ieee.org/sram-memory-z2ram) | IEEE Spectrum Semiconductors · 21 Nov 15:00 |
| [EE Times](https://www.eetimes.com/feed/) | 6 | [Pat Gelsinger Goes Hunting for Europe’s Unbuilt Tech Companies](https://www.eetimes.com/pat-gelsinger-goes-hunting-for-europes-unbuilt-tech-companies/) | EE Times · 20 Nov 23:23 |
| [SemiWiki](https://semiwiki.com/feed/) | 5 | [TSMC’s Supplier Awards Put Manufacturing Execution in Focus](https://semiwiki.com/semiconductor-manufacturers/tsmc/376475-tsmcs-supplier-awards-put-manufacturing-execution-in-focus/) | SemiWiki · 20 Nov 17:00 |
| [Canary Media](https://www.canarymedia.com/rss.rss) | 6 | [Why tribal rights have become key to the energy permitting debate](https://www.canarymedia.com/articles/land-use/tribal-rights-energy-permitting-debate) | Canary Media · 20 Nov 22:30 |
| [Electrek](https://electrek.co/feed/) | 6 | [Rumor: Hyundai is getting ready to roll out an all-new, all-electric…](https://electrek.co/2026/11/21/rumor-hyundai-is-getting-ready-to-roll-out-an-all-new-all-electric-work-truck/) | Electrek · 22 Nov 03:13 |
| [CleanTechnica](https://cleantechnica.com/feed/) | 6 | [Ford Begins Producing Its Own LFP Batteries](https://cleantechnica.com/2026/11/21/ford-begins-producing-its-own-lfp-batteries/) | CleanTechnica · 22 Nov 05:49 |
| [EIA Today in Energy](https://www.eia.gov/rss/todayinenergy.xml) | 3 | [Oil flows through Middle East chokepoints increased in the third…](https://www.eia.gov/todayinenergy/detail.php?id=) | EIA Today in Energy · 19 Nov 15:00 |
| [Modern Retail](https://www.modernretail.co/feed/) | 6 | [2026 marked a turning point for artificial dye removal from food](https://www.modernretail.co/podcasts/2026-artificial-dye-removal-from-food/?utm_campaign=modernretaildis&utm_medium=rss&utm_source=general-rss) | Modern Retail · 21 Nov 06:00 |
| [Retail Dive](https://www.retaildive.com/feeds/news/) | 6 | [The Container Store is back online after cybersecurity incident](https://www.retaildive.com/news/container-store-neighborhood-intelligence-cybersecurity-incident/875342/) | Retail Dive · 20 Nov 18:41 |
| [Digital Commerce 360](https://www.digitalcommerce360.com/feed/) | 3 | [3 online sales factors to watch in 2026 holiday shopping forecasts](https://www.digitalcommerce360.com/2026/11/19/holiday-shopping-forecast/) | Digital Commerce 360 · 19 Nov 20:59 |
| [GamesIndustry.biz](https://www.gamesindustry.biz/feed) | 6 | [GTA 6 hits $3.79 billion in its first day on sale, becoming "the…](https://www.gamesindustry.biz/gta-6-hits-379-billion-in-its-first-day-on-sale-becoming-the-biggest-entertainment-launch-in-history) | GamesIndustry.biz · 20 Nov 21:24 |
| [Game Developer](https://www.gamedeveloper.com/rss.xml) | 6 | [Grand Theft Auto VI is now the biggest video game launch in history](https://www.gamedeveloper.com/business/grand-theft-auto-vi-is-officially-the-biggest-video-game-launch-ever) | Game Developer · 20 Nov 22:50 |
| [UploadVR](https://www.uploadvr.com/rss/) | 6 | [Gucci's Vision Pro Runway Show Offers Immersive Access, But The…](https://www.uploadvr.com/guccis-vision-pro-runway-show-offers-immersive-access-but-the-luxury-experience-falls-short/) | UploadVR · 20 Nov 19:00 |
| [TechCrunch Enterprise](https://techcrunch.com/category/enterprise/feed/) | 3 | [Microsoft CEO Satya Nadella explains why he asked 60K employees to…](https://techcrunch.com/2026/11/18/microsoft-ceo-satya-nadella-explains-why-he-asked-60k-employees-to-quit/) | TechCrunch Enterprise · 19 Nov 01:42 |
| [EdSurge](https://www.edsurge.com/articles_rss) | 6 | [Google Says Schools Can’t Have Search Without AI. Some Are Finding a…](https://www.edsurge.com/news/google-says-schools-cant-have-search-without-ai-some-are-finding-a-way) | EdSurge · 19 Nov 01:00 |
| [Class Central](https://www.classcentral.com/report/feed/) | 3 | [The Investor That Ended Up Running Groupon Now Owns 14.7% of Coursera](https://www.classcentral.com/report/coursera-pale-fire-poison-pill/) | Class Central · 17 Nov 13:14 |
| [Nieman Lab](https://www.niemanlab.org/feed/) | 6 | [The Nieman Lab News-About-News Quiz, November 20, 2026](https://www.niemanlab.org/2026/11/the-nieman-lab-news-about-news-quiz-november-20-2026/) | Nieman Lab · 20 Nov 15:00 |
| [Tubefilter](https://www.tubefilter.com/feed/) | 6 | [Top 5 Branded Videos of the Week: Tech, physics, Christmas, oh my](https://www.tubefilter.com/2026/11/21/top-5-branded-videos-veritasium-bikelife-mom-ryan-trahan-marques-brownlee/) | Tubefilter · 21 Nov 21:00 |
| [SpaceNews](https://spacenews.com/feed/) | 6 | [The sweet spot for constellation size](https://spacenews.com/the-sweet-spot-for-constellation-size/) | SpaceNews · 19 Nov 18:25 |
| [NASA news releases](https://www.nasa.gov/news-release/feed/) | 6 | [APOD: 2026 November 22 – Swirls and Colors on Jupiter from Juno](https://science.nasa.gov/image-article/apod-2026-november-22-swirls-and-colors-on-jupiter-from-juno/) | NASA news releases · 22 Nov 06:05 |
| [TechCrunch Transportation](https://techcrunch.com/category/transportation/feed/) | 6 | [Uber tests rides for kids as young as 10, with extra pay for drivers](https://techcrunch.com/2026/11/19/uber-tests-rides-for-kids-as-young-as-10-with-extra-pay-for-drivers/) | TechCrunch Transportation · 19 Nov 22:33 |
| [EFF Deeplinks](https://www.eff.org/rss/updates.xml) | 6 | [EFF to Congress: Mass Surveillance Is Too Important to Shove into…](https://www.eff.org/deeplinks/2026/11/eff-congress-mass-surveillance-too-important-shove-must-pass-bill) | EFF Deeplinks · 20 Nov 22:52 |
| [European Commission press corner](https://ec.europa.eu/commission/presscorner/api/rss?language=en) | 6 | [Statement by President von der Leyen on the signature of the…](https://ec.europa.eu/commission/presscorner/detail/en/statement_26_2557) | European Commission press corner · 21 Nov 12:28 |
| [9to5Mac](https://9to5mac.com/feed/) | 6 | [iOS 27: My favorite new iPhone features (other than AI)](https://9to5mac.com/2026/11/21/ios-27-my-favorite-new-iphone-features-other-than-ai/) | 9to5Mac · 21 Nov 23:22 |
| [Android Police](https://www.androidpolice.com/feed/) | 6 | [How to reduce Google Maps battery drain on Android](https://www.androidpolice.com/reduce-google-maps-battery-drain-with-these-tweaks/) | Android Police · 22 Nov 01:00 |
| [Tech.eu](https://tech.eu/feed/) | 6 | [Startup ecosystem calls to withdraw and re-table EU Inc proposal…](https://tech.eu/2026/11/20/startup-ecosystem-calls-to-withdraw-and-re-table-eu-inc-proposal/) | Tech.eu · 20 Nov 16:09 |
| [Sifted](https://sifted.eu/feed) | 6 | [Exclusive: Storonsky-backed Aikido seeks €4bn valuation](https://sifted.eu/articles/exclusive-aikido-4bn-valuation/) | Sifted · 20 Nov 17:04 |

</details>

<a id="src-pulse"></a>

<details>
<summary><b>Public pulse</b> · 77 items from 5/5 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [Google Trends · daily searches (US and DE)](https://trends.google.com/trending) | 20 | [metacritic gta vi](https://trends.google.com/trending?geo=US&q=metacritic%20gta%20vi) | 10000+ searches (US) |
| [Wikipedia · most read yesterday (English)](https://en.wikipedia.org/wiki/Special:TopViews) | 15 | [Grand Theft Auto VI](https://en.wikipedia.org/wiki/Grand_Theft_Auto_VI) | 393.3k views |
| [Mastodon · most shared links (mastodon.social)](https://mastodon.social/explore/links) | 12 | ['I'm not MAGA,' Elon Musk says after Republicans' midterm thrashing](https://www.pbs.org/newshour/politics/im-not-maga-elon-musk-says-after-republicans-midterm-thrashing) | PBS News · 19 Nov 18:09 |
| [Mastodon · trending hashtags (mastodon.social)](https://mastodon.social/explore/tags) | 15 | [#TextilesASong](https://mastodon.social/tags/textilesasong) | 353 posts / 2 days |
| [Bluesky · trending topics](https://bsky.app/) | 15 | [Change one letter, ruin a movie](https://bsky.app/profile/did:plc:qrz3lhbyuxbeilrc6nekdqme/feed/645e79ca5148) | — |

</details>

<a id="src-windows"></a>

<details>
<summary><b>Week, month and year lists</b> · 250 items from 13/13 sources</summary>

| Source | Items | #1 item | Key metric |
| --- | --- | --- | --- |
| [GitHub trending · this week](https://github.com/trending?since=weekly) | 13 | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | 14.2k stars · +3,396 this week |
| [GitHub · new repos gaining stars (created in the last 7 days)](https://docs.github.com/en/rest/search/search#search-repositories) | 40 | [ItsNotRexed/Leonida](https://github.com/ItsNotRexed/Leonida) | 7.7k stars · created 20 Nov |
| [Hacker News · best of the week](https://news.ycombinator.com/best) | 10 | [Levent Alpöge claims proof of the Generalized Riemann Hypothesis \[pdf\]](https://alpo.ge/remark.pdf) | 2,868 pts · 2,049 comments |
| [Dev.to · top this week](https://dev.to/top/week) | 10 | [Is Coding with AI Actually Faster and Cheaper?](https://dev.to/sylwia-lask/is-coding-with-ai-actually-faster-and-cheaper-2810) | 231 reactions · 196 comments |
| [Hugging Face · papers of the week](https://huggingface.co/papers) | 20 | [TeleChat to Xing4: Advancing Frontier Agentic Models on Domestic…](https://huggingface.co/papers/2611.22115) | 167 upvotes |
| [GitHub trending · this month](https://github.com/trending?since=monthly) | 17 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 59.2k stars · +28,684 this month |
| [GitHub · most-starred repos created in the last 30 days](https://docs.github.com/en/rest/search/search#search-repositories) | 25 | [storytold/craft-anything](https://github.com/storytold/craft-anything) | 40.6k stars · created 31 Oct |
| [Hacker News · best of the last 30 days](https://news.ycombinator.com/best) | 20 | [Jensen Huang resigns](https://apnews.com/article/nvidia-megaspeed-china-singapore-huang-5403f152a601cf82ce939f1d24fffa0f) | 4,060 pts · 3,493 comments |
| [Dev.to · top this month](https://dev.to/top/month) | 15 | [We're Building AI to Replace Ourselves. What's the Plan?](https://dev.to/sylwia-lask/were-building-ai-to-replace-ourselves-whats-the-plan-4oll) | 238 reactions · 219 comments |
| [Hugging Face · papers of the month](https://huggingface.co/papers) | 20 | [TeleChat to Xing4: Advancing Frontier Agentic Models on Domestic…](https://huggingface.co/papers/2611.22115) | 167 upvotes |
| [GitHub · most-starred repos created in the last 365 days](https://docs.github.com/en/rest/search/search#search-repositories) | 25 | [morluto/rea](https://github.com/morluto/rea) | 473.1k stars · created 14 Apr |
| [Hacker News · best of the last 365 days](https://news.ycombinator.com/best) | 20 | [Don't post generated/AI-edited comments. HN is for conversation…](https://news.ycombinator.com/newsguidelines.html#generated) | 4,229 pts · 1,668 comments |
| [Dev.to · top this year](https://dev.to/top/year) | 15 | [A New Chapter: DEV is Joining Forces with Major League Hacking (MLH)](https://dev.to/devteam/a-new-chapter-dev-is-joining-forces-with-major-league-hacking-mlh-3kfd) | 449 reactions · 125 comments |

</details>

<a id="status"></a>

## Platform status

Incidents in the last 72 hours on platforms and AI APIs most teams depend on.

### GitHub status · incidents (last 72 h)

<sub>[githubstatus.com](https://www.githubstatus.com) · fetched 08:12 Europe/Berlin · Statuspage public API</sub>

| # | Incident | Service | Components | Impact | Status | Started | Seen on | Industry | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Disruption with some GitHub services](https://stspg.io/pvjz2g01trc7) | GitHub | — | minor | resolved | 19 Nov 18:06 | 1 | Cloud | [GitHub status](https://www.githubstatus.com) |
| 2 | [Degraded availability for GPT-6 Luna in Copilot](https://stspg.io/vv0kzmyd9wqs) | GitHub | Copilot AI Model Providers | minor | resolved | 19 Nov 16:56 | 1 | Cloud | [GitHub status](https://www.githubstatus.com) |

### Cloudflare status · incidents (last 72 h)

<sub>[cloudflarestatus.com](https://www.cloudflarestatus.com) · fetched 08:12 Europe/Berlin · Statuspage public API</sub>

| # | Incident | Service | Components | Impact | Status | Started | Seen on | Industry | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Network Performance Issues in Chicago datacenter (ORD)](https://www.cloudflarestatus.com/incidents/d2m4kw94ut4f) | Cloudflare | Durable Objects, D1, Chicago, United States - (ORD) | minor | resolved | 22 Nov 01:32 | 1 | Cloud | [Cloudflare status](https://www.cloudflarestatus.com) |
| 2 | [Network Performance Issues in Washington, DC datacenter (IAD)](https://www.cloudflarestatus.com/incidents/oz6to8yacrxe) | Cloudflare | Network | minor | resolved | 20 Nov 21:35 | 1 | Cloud | [Cloudflare status](https://www.cloudflarestatus.com) |
| 3 | [Cache Purging Delays in Milan](https://www.cloudflarestatus.com/incidents/akjr7qn5o622) | Cloudflare | CDN Cache Purge | none | resolved | 20 Nov 21:51 | 1 | Cloud | [Cloudflare status](https://www.cloudflarestatus.com) |

<details>
<summary>Show 6 more</summary>

| # | Incident | Service | Components | Impact | Status | Started | Seen on | Industry | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | [Cache Purging Delays in Amsterdam](https://www.cloudflarestatus.com/incidents/xsgbfncq7of7) | Cloudflare | CDN Cache Purge | minor | resolved | 20 Nov 19:00 | 1 | Cloud | [Cloudflare status](https://www.cloudflarestatus.com) |
| 5 | [Cloudflare Dashboard and Cloudflare API service issues in EU region](https://www.cloudflarestatus.com/incidents/iysf3fasf7wn) | Cloudflare | — | major | resolved | 20 Nov 19:24 | 1 | Cloud | [Cloudflare status](https://www.cloudflarestatus.com) |
| 6 | [Network Performance Issues in Miami](https://www.cloudflarestatus.com/incidents/4lv21sf5fzhm) | Cloudflare | Miami, United States - (MIA) | minor | resolved | 20 Nov 06:00 | 1 | Cloud | [Cloudflare status](https://www.cloudflarestatus.com) |
| 7 | [R2 and Durable Objects availability issues](https://www.cloudflarestatus.com/incidents/pfwuex7qix27) | Cloudflare | Durable Objects, R2 | minor | resolved | 20 Nov 03:52 | 1 | Cloud | [Cloudflare status](https://www.cloudflarestatus.com) |
| 8 | [Observability ingestion delay and query failures](https://www.cloudflarestatus.com/incidents/ljrvdciu7syf) | Cloudflare | Workers, Workers Observability | minor | resolved | 19 Nov 17:30 | 1 | Cloud | [Cloudflare status](https://www.cloudflarestatus.com) |
| 9 | [Durable Objects and D1 – Increased Errors](https://www.cloudflarestatus.com/incidents/5pe5mb9fefi8) | Cloudflare | Durable Objects, D1 | minor | resolved | 19 Nov 14:05 | 1 | Cloud | [Cloudflare status](https://www.cloudflarestatus.com) |

</details>

### Anthropic status · incidents (last 72 h)

<sub>[status.anthropic.com](https://status.anthropic.com) · fetched 08:12 Europe/Berlin · Statuspage public API</sub>

| # | Incident | Service | Components | Impact | Status | Started | Seen on | Industry | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Elevated errors for Claude Mythos 5.2 and Claude Fable 5.2](https://stspg.io/nlb5fptv28h5) | Anthropic | claude.ai, Claude API (api.anthropic.com), Claude Code | major | resolved | 19 Nov 10:10 | 1 | AI | [Anthropic status](https://status.anthropic.com) |

### OpenAI status · incidents (last 72 h)

<sub>[status.openai.com](https://status.openai.com) · fetched 08:12 Europe/Berlin · Statuspage public API</sub>

| # | Incident | Service | Components | Impact | Status | Started | Seen on | Industry | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Elevated error rates for gpt-6 Luna API requests](https://status.openai.com) | OpenAI | — | major | resolved | 19 Nov 17:01 | 1 | AI | [OpenAI status](https://status.openai.com) |

### Mistral AI status · incidents (last 72 h)

<sub>[status.mistral.ai](https://status.mistral.ai) · fetched 08:12 Europe/Berlin · Statuspage public API</sub>

| # | Incident | Service | Components | Impact | Status | Started | Seen on | Industry | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Vibe Work issues with GLM 5.3 Short](https://status.mistral.ai/incidents/b8cc1988-7510-45cc-bb41-bd2d10e730ec) | Mistral AI | — | minor | monitoring | 19 Nov 16:06 | 1 | AI | [Mistral AI status](https://status.mistral.ai) |

### Cohere status · incidents (last 72 h)

_Nothing in this window today._ <sub>[status.cohere.com](https://status.cohere.com) · fetched 08:12 Europe/Berlin</sub>

### Perplexity status · incidents (last 72 h)

_Nothing in this window today._ <sub>[status.perplexity.com](https://status.perplexity.com) · fetched 08:12 Europe/Berlin</sub>

### ElevenLabs status · incidents (last 72 h)

<sub>[status.elevenlabs.io](https://status.elevenlabs.io) · fetched 08:12 Europe/Berlin · Statuspage public API</sub>

| # | Incident | Service | Components | Impact | Status | Started | Seen on | Industry | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Degraded performance of Voice Library voices](https://status.elevenlabs.io) | ElevenLabs | — | minor | resolved | 19 Nov 11:25 | 1 | AI media | [ElevenLabs status](https://status.elevenlabs.io) |

<a id="x"></a>

## Tech on X

_No tech topics in today's X trend lists, or the lists were not captured yet._

<a id="maintainer"></a>

## From the maintainer

The maintainer's own projects. **This is not a ranking.** They show up in the tables above only when a source listed them on its own.

- [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) — Avoid common App Store and Google Play rejections. Open playbook and pre-submission guard with 124 documented rejection patterns and fixes, privacy manifest and Data safety checks, 111 tracked deadlines (EU AI Act, DSA, COPPA, age laws), and a skill for AI coding agents. (3,550 stars)
- [mjmirza/hetzner-mcp](https://github.com/mjmirza/hetzner-mcp) — Enterprise-grade Model Context Protocol server for the full Hetzner platform. Cloud, Storage Box, and Robot dedicated servers. Cost-guarded, security-hardened, every endpoint live-tested. (19 stars)
- [mjmirza/patterns](https://github.com/mjmirza/patterns) — Master level software patterns reference. 18 dimensions per entry, every claim cited and verified. (19 stars)

<a id="archive"></a>

## Archive

<details>
<summary>Every past day</summary>

- [22 November 2026](archive/2026/11/2026-11-22.md)
- [21 November 2026](archive/2026/11/2026-11-21.md)
- [20 November 2026](archive/2026/11/2026-11-20.md)
- [19 November 2026](archive/2026/11/2026-11-19.md)

</details>

## Contribute

- Submit a repo with the [issue form](https://github.com/mjmirza/awesome-trending/issues/new?template=submit-repo.yml). Tables are rebuilt from the sources every morning.
- Found it useful? A star helps other people find it. Spotted a wrong number? Open an issue with the row.
- How items are scored, clustered and sorted into industries: [docs/methodology.md](docs/methodology.md).
- Full source list and how to run it: [CONTRIBUTING.md](CONTRIBUTING.md) · [badge](docs/badge.md).
- License: [OpenRoots Agent License 2.3](LICENSE) (SPDX `LicenseRef-OpenRoots-ORA-2.3`). Free and unconditional at or below USD 20,000,000 annual revenue, and for any individual, nonprofit, school, or government body at any size. Above that threshold, a small self-reported royalty applies, capped per year. AI training on this work is not granted by either tier and needs a separate Compute license; human reading and search indexing are unaffected. Canonical text: [openroots.org/licenses/ora/2.3](https://openroots.org/licenses/ora/2.3).

<a id="sources"></a>

## Sources

Fetched 22 November 2026 at 08:12 Europe/Berlin (UTC+1). Every figure comes from the source in its row. A dash means the source gave no number. Nothing is estimated or invented.

| # | Source | Status | Items | Rank use | Fetched | How it is read |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [GitHub trending · today](https://github.com/trending?since=daily) | OK | 16 | ranked | 08:12 | 16 repos in the order GitHub shows them |
| 2 | [GitHub trending · this week](https://github.com/trending?since=weekly) | OK | 13 | ranked | 08:12 | 13 repos in the order GitHub shows them |
| 3 | [GitHub trending · Python](https://github.com/trending/python?since=daily) | OK | 10 | ranked | 08:12 | 10 repos in the order GitHub shows them |
| 4 | [GitHub trending · TypeScript](https://github.com/trending/typescript?since=daily) | OK | 10 | ranked | 08:12 | 10 repos in the order GitHub shows them |
| 5 | [GitHub trending · Rust](https://github.com/trending/rust?since=daily) | OK | 10 | ranked | 08:12 | 10 repos in the order GitHub shows them |
| 6 | [GitHub trending · Go](https://github.com/trending/go?since=daily) | OK | 10 | ranked | 08:12 | 10 repos in the order GitHub shows them |
| 7 | [GitHub · new repos gaining stars (created in the last 7 days)](https://docs.github.com/en/rest/search/search#search-repositories) | OK | 40 | ranked | 08:12 | GitHub search API, sorted by stars; 40 repos that state a licence and a description |
| 8 | [Maintainer repos (not a ranking)](https://github.com/mjmirza) | OK | 3 | unranked | 08:12 | GitHub search API, repo: qualifiers |
| 9 | [Hacker News · front page](https://news.ycombinator.com/) | OK | 20 | ranked | 08:12 | Algolia HN API, front_page tag, sorted by points |
| 10 | [Hacker News · Show HN (last 24 h)](https://news.ycombinator.com/show) | OK | 7 | ranked | 08:12 | Algolia HN API, show_hn posts from the last 24 h, sorted by points |
| 11 | [Hacker News · Ask HN (last 24 h)](https://news.ycombinator.com/ask) | OK | 8 | ranked | 08:12 | Algolia HN API, ask_hn posts from the last 24 h, sorted by comments |
| 12 | [Hacker News · best of the week](https://news.ycombinator.com/best) | OK | 10 | ranked | 08:12 | Algolia HN API, stories from the last 7 days with 300+ points |
| 13 | [Hugging Face · trending models](https://huggingface.co/models?sort=trending) | OK | 15 | ranked | 08:12 | Hub API sort=trendingScore; downloads are the Hub's last-30-days count |
| 14 | [Hugging Face · trending Spaces](https://huggingface.co/spaces?sort=trending) | OK | 12 | ranked | 08:12 | Hub API sort=trendingScore |
| 15 | [Hugging Face · trending datasets](https://huggingface.co/datasets?sort=trending) | OK | 12 | ranked | 08:12 | Hub API sort=trendingScore; downloads are the Hub's last-30-days count |
| 16 | [Hugging Face · daily papers](https://huggingface.co/papers) | OK | 15 | ranked | 08:12 | daily_papers API, sorted by community upvotes |
| 17 | [arXiv · newest by category](https://arxiv.org/) | OK | 45 | unranked | 08:12 | export API, newest submissions in cs.AI, cs.CL, cs.LG, cs.CV, cs.CR, cs.SE, cs.RO, q-bio.*, q-fin.* |
| 18 | [MCP Registry · new and updated servers (24 h)](https://registry.modelcontextprotocol.io/) | OK | 12 | unranked | 08:12 | official registry API, 370 distinct servers published or updated in the last 24 h |
| 19 | [Smithery · most-used MCP servers](https://smithery.ai/) | OK | 10 | ranked | 08:12 | public registry API, first 50 listed servers sorted by use count (20,738 servers listed) |
| 20 | [OpenRouter · newest models](https://openrouter.ai/models) | OK | 10 | unranked | 08:12 | public models API (476 models listed), newest first; prices in USD per 1M tokens |
| 21 | [OpenAI News](https://openai.com/news/rss.xml) | OK | 4 | unranked | 08:12 | feed, items from the last 168 h (32 found) |
| 22 | [Google AI blog](https://blog.google/technology/ai/rss/) | OK | 4 | unranked | 08:12 | feed, items from the last 168 h (5 found) |
| 23 | [Google DeepMind blog](https://deepmind.google/blog/rss.xml) | OK | 2 | unranked | 08:12 | feed, items from the last 168 h (2 found) |
| 24 | [Hugging Face blog](https://huggingface.co/blog/feed.xml) | OK | 4 | unranked | 08:12 | feed, items from the last 168 h (8 found) |
| 25 | [npm · top packages for MCP, AI agents and LLMs](https://www.npmjs.com/) | OK | 20 | ranked | 08:12 | registry search API, keywords mcp, ai-agent and llm; weekly downloads as npm reports them |
| 26 | [PyPI · latest releases of key AI and Python packages](https://pypi.org/) | OK | 14 | unranked | 08:12 | PyPI JSON API for versions; weekly downloads from pypistats.org |
| 27 | [crates.io · most downloaded recently](https://crates.io/) | OK | 24 | unranked | 08:12 | summary API; 'recent downloads' is crates.io's 90-day count |
| 28 | [jsDelivr · top npm packages by CDN hits this week](https://www.jsdelivr.com/statistics) | OK | 15 | ranked | 08:12 | public data API, period=week; change is against the previous week |
| 29 | [Docker Hub · official images updated in the last 48 h](https://hub.docker.com/search?badges=official) | OK | 12 | unranked | 08:12 | Hub API, library namespace ordered by last update, sorted by total pulls |
| 30 | [GitHub releases · major projects (last 72 h)](https://github.com/) | OK | 17 | unranked | 08:12 | public releases.atom feeds of 28 projects |
| 31 | [CISA KEV · known exploited vulnerabilities (last 14 days)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | OK | 20 | unranked | 08:12 | catalog version 2026.11.20, 1,790 entries in total |
| 32 | [NVD · critical CVEs published in the last 48 h](https://nvd.nist.gov/vuln/search) | OK | 6 | unranked | 08:12 | CVE API 2.0, 6 CVEs with a CVSS v3 severity of CRITICAL published in the window |
| 33 | [ENISA EUVD · latest vulnerabilities](https://euvd.enisa.europa.eu/) | OK | 4 | unranked | 08:12 | EU Vulnerability Database public API, sorted by base score |
| 34 | [GitHub status · incidents (last 72 h)](https://www.githubstatus.com) | OK | 2 | unranked | 08:12 | Statuspage public API |
| 35 | [Cloudflare status · incidents (last 72 h)](https://www.cloudflarestatus.com) | OK | 9 | unranked | 08:12 | Statuspage public API |
| 36 | [Dev.to · top today](https://dev.to/top/day) | OK | 10 | ranked | 08:12 | Forem API top=1 |
| 37 | [Dev.to · top this week](https://dev.to/top/week) | OK | 10 | ranked | 08:12 | Forem API top=7 |
| 38 | [Lobsters · hottest](https://lobste.rs/) | OK | 15 | ranked | 08:12 | official hottest.json |
| 39 | [Stack Overflow · hot questions](https://stackoverflow.com/questions?tab=Hot) | OK | 12 | ranked | 08:12 | Stack Exchange API 2.3, sort=hot (quota left today: 269) |
| 40 | [Product Hunt · newest featured](https://www.producthunt.com/) | OK | 15 | unranked | 08:12 | public Atom feed (the feed carries no vote counts) |
| 41 | [Techmeme](https://www.techmeme.com/feed.xml) | OK | 6 | unranked | 08:12 | feed, items from the last 36 h (15 found) |
| 42 | [The Verge](https://www.theverge.com/rss/index.xml) | OK | 6 | unranked | 08:12 | feed, items from the last 36 h (10 found) |
| 43 | [TechCrunch](https://techcrunch.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 36 h (10 found) |
| 44 | [Ars Technica](https://feeds.arstechnica.com/arstechnica/technology-lab) | OK | 1 | unranked | 08:12 | feed, items from the last 36 h (1 found) |
| 45 | [LWN.net](https://lwn.net/headlines/rss) | OK | 0 | unranked | 08:12 | feed, items from the last 36 h (0 found) |
| 46 | [The Hacker News](https://feeds.feedburner.com/TheHackersNews) | OK | 6 | unranked | 08:12 | feed, items from the last 36 h (7 found) |
| 47 | [BleepingComputer](https://www.bleepingcomputer.com/feed/) | OK | 4 | unranked | 08:12 | feed, items from the last 36 h (4 found) |
| 48 | [GitHub Changelog](https://github.blog/changelog/feed/) | OK | 2 | unranked | 08:12 | feed, items from the last 36 h (2 found) |
| 49 | [Simon Willison](https://simonwillison.net/atom/everything/) | OK | 2 | unranked | 08:12 | feed, items from the last 36 h (2 found) |
| 50 | [Google Trends · daily searches (US and DE)](https://trends.google.com/trending) | OK | 20 | ranked | 08:12 | Trending now RSS; search volume is Google's approximate bucket |
| 51 | [Wikipedia · most read yesterday (English)](https://en.wikipedia.org/wiki/Special:TopViews) | OK | 15 | ranked | 08:12 | Wikimedia pageviews API, 21 November 2026 (UTC day), main page and special pages left out |
| 52 | [Mastodon · trending hashtags (mastodon.social)](https://mastodon.social/explore/tags) | OK | 15 | ranked | 08:12 | instance trends API; uses and accounts summed over the last two days |
| 53 | [Mastodon · most shared links (mastodon.social)](https://mastodon.social/explore/links) | OK | 12 | ranked | 08:12 | instance trends API; shares summed over the last two days |
| 54 | [Bluesky · trending topics](https://bsky.app/) | OK | 15 | ranked | 08:12 | public AppView API getTrendingTopics |
| 55 | [Finextra](https://www.finextra.com/rss/headlines.aspx) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (40 found) |
| 56 | [PYMNTS](https://www.pymnts.com/feed/) | Skipped | 0 | unranked | 08:12 | invalid XML (not well-formed (invalid token): line 121, column 177) |
| 57 | [CoinDesk](https://www.coindesk.com/arc/outboundfeeds/rss/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (25 found) |
| 58 | [Decrypt](https://decrypt.co/feed) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (37 found) |
| 59 | [STAT News](https://www.statnews.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (20 found) |
| 60 | [The Robot Report](https://www.therobotreport.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (13 found) |
| 61 | [IEEE Spectrum Robotics](https://spectrum.ieee.org/feeds/topic/robotics.rss) | OK | 4 | unranked | 08:12 | feed, items from the last 168 h (4 found) |
| 62 | [IEEE Spectrum Semiconductors](https://spectrum.ieee.org/feeds/topic/semiconductors.rss) | OK | 2 | unranked | 08:12 | feed, items from the last 168 h (2 found) |
| 63 | [EE Times](https://www.eetimes.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (10 found) |
| 64 | [SemiWiki](https://semiwiki.com/feed/) | OK | 5 | unranked | 08:12 | feed, items from the last 168 h (5 found) |
| 65 | [Canary Media](https://www.canarymedia.com/rss.rss) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (17 found) |
| 66 | [Electrek](https://electrek.co/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (86 found) |
| 67 | [CleanTechnica](https://cleantechnica.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (45 found) |
| 68 | [EIA Today in Energy](https://www.eia.gov/rss/todayinenergy.xml) | OK | 3 | unranked | 08:12 | feed, items from the last 168 h (3 found) |
| 69 | [Modern Retail](https://www.modernretail.co/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (10 found) |
| 70 | [Retail Dive](https://www.retaildive.com/feeds/news/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (10 found) |
| 71 | [Digital Commerce 360](https://www.digitalcommerce360.com/feed/) | OK | 3 | unranked | 08:12 | feed, items from the last 168 h (3 found) |
| 72 | [GamesIndustry.biz](https://www.gamesindustry.biz/feed) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (41 found) |
| 73 | [Game Developer](https://www.gamedeveloper.com/rss.xml) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (17 found) |
| 74 | [UploadVR](https://www.uploadvr.com/rss/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (14 found) |
| 75 | [TechCrunch Enterprise](https://techcrunch.com/category/enterprise/feed/) | OK | 3 | unranked | 08:12 | feed, items from the last 168 h (3 found) |
| 76 | [EdSurge](https://www.edsurge.com/articles_rss) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (6 found) |
| 77 | [Class Central](https://www.classcentral.com/report/feed/) | OK | 3 | unranked | 08:12 | feed, items from the last 168 h (3 found) |
| 78 | [Nieman Lab](https://www.niemanlab.org/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (8 found) |
| 79 | [Tubefilter](https://www.tubefilter.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (12 found) |
| 80 | [SpaceNews](https://spacenews.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (8 found) |
| 81 | [NASA news releases](https://www.nasa.gov/news-release/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (10 found) |
| 82 | [TechCrunch Transportation](https://techcrunch.com/category/transportation/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (8 found) |
| 83 | [EFF Deeplinks](https://www.eff.org/rss/updates.xml) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (12 found) |
| 84 | [European Commission press corner](https://ec.europa.eu/commission/presscorner/api/rss?language=en) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (10 found) |
| 85 | [9to5Mac](https://9to5mac.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (100 found) |
| 86 | [Android Police](https://www.androidpolice.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (10 found) |
| 87 | [Tech.eu](https://tech.eu/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (20 found) |
| 88 | [Sifted](https://sifted.eu/feed) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (24 found) |
| 89 | [GitHub · young repos tagged robotics](https://github.com/topics/robotics) | OK | 10 | ranked | 08:12 | GitHub search API: topic:robotics, created in the last 90 days, 50+ stars, licence and description stated |
| 90 | [GitHub · young repos tagged bioinformatics](https://github.com/topics/bioinformatics) | OK | 10 | ranked | 08:12 | GitHub search API: topic:bioinformatics, created in the last 90 days, 50+ stars, licence and description stated |
| 91 | [GitHub · young repos tagged fintech](https://github.com/topics/fintech) | OK | 10 | ranked | 08:12 | GitHub search API: topic:fintech, created in the last 90 days, 50+ stars, licence and description stated |
| 92 | [CoinGecko · trending coins (searches, 24 h)](https://www.coingecko.com/en/highlights/trending-crypto) | OK | 15 | ranked | 08:12 | public API search/trending (ranked by CoinGecko search activity) |
| 93 | [CoinGecko · top 15 by market cap](https://www.coingecko.com/) | OK | 15 | unranked | 08:12 | public API coins/markets, USD |
| 94 | [bioRxiv and medRxiv · newest preprints](https://www.biorxiv.org/) | OK | 16 | unranked | 08:12 | public details API, first preprints posted 2026-11-20 to 2026-11-21 |
| 95 | [Launch Library 2 · next orbital launches](https://thespacedevs.com/llapi) | OK | 10 | unranked | 08:12 | Launch Library 2 public API (The Space Devs), next 10 launches |
| 96 | [Google · Gemini blog](https://blog.google/products/gemini/rss/) | OK | 5 | unranked | 08:12 | feed, items from the last 336 h (19 found) |
| 97 | [Microsoft Source · AI](https://news.microsoft.com/source/topics/ai/feed/) | OK | 1 | unranked | 08:12 | feed, items from the last 336 h (1 found) |
| 98 | [NVIDIA blog](https://blogs.nvidia.com/feed/) | OK | 5 | unranked | 08:12 | feed, items from the last 336 h (18 found) |
| 99 | [AWS Machine Learning blog](https://aws.amazon.com/blogs/machine-learning/feed/) | OK | 5 | unranked | 08:12 | feed, items from the last 336 h (20 found) |
| 100 | [Apple Machine Learning Research](https://machinelearning.apple.com/rss.xml) | OK | 5 | unranked | 08:12 | feed, items from the last 336 h (9 found) |
| 101 | [ElevenLabs blog](https://elevenlabs.io/blog/rss.xml) | OK | 5 | unranked | 08:12 | feed, items from the last 336 h (33 found) |
| 102 | [Anthropic · newsroom (public sitemap)](https://www.anthropic.com/news) | OK | 8 | unranked | 08:12 | public sitemap.xml, news pages changed in the last 14 days; titles and summaries from each page's own meta tags (8 of… |
| 103 | [Google News · Anthropic](https://news.google.com/search?q=%22Anthropic%22+OR+%22Claude+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 40 of 40 headlines name the subject |
| 104 | [Google News · OpenAI](https://news.google.com/search?q=%22OpenAI%22&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 37 of 40 headlines name the subject |
| 105 | [Google News · Google DeepMind & Gemini](https://news.google.com/search?q=%22Google+DeepMind%22+OR+%22Gemini%22+Google+AI&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 36 of 40 headlines name the subject |
| 106 | [Google News · Meta AI](https://news.google.com/search?q=%22Meta+AI%22+OR+%22Meta+Superintelligence%22+OR+%22Llama%22+Meta&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 32 of 40 headlines name the subject |
| 107 | [Google News · Microsoft AI](https://news.google.com/search?q=%22Microsoft+AI%22+OR+%22Microsoft+Copilot%22&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 25 of 26 headlines name the subject |
| 108 | [Google News · xAI](https://news.google.com/search?q=%22xAI%22+Musk+AI&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 9 of 13 headlines name the subject |
| 109 | [Google News · Mistral AI](https://news.google.com/search?q=%22Mistral+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 13 of 20 headlines name the subject |
| 110 | [Google News · Cohere](https://news.google.com/search?q=%22Cohere%22+AI&hl=en-US&gl=US&ceid=US%3Aen) | OK | 3 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 3 of 6 headlines name the subject |
| 111 | [Google News · NVIDIA](https://news.google.com/search?q=Nvidia+AI&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 29 of 40 headlines name the subject |
| 112 | [Google News · Amazon & AWS](https://news.google.com/search?q=%22Amazon%22+AI+%28Bedrock+OR+Nova+OR+AWS%29&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 26 of 30 headlines name the subject |
| 113 | [Google News · Apple](https://news.google.com/search?q=%22Apple+Intelligence%22+OR+%22Apple+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 30 of 33 headlines name the subject |
| 114 | [Google News · DeepSeek](https://news.google.com/search?q=DeepSeek&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 19 of 35 headlines name the subject |
| 115 | [Google News · Qwen & Alibaba](https://news.google.com/search?q=Qwen+OR+%22Alibaba%22+AI+model&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 19 of 27 headlines name the subject |
| 116 | [Google News · Moonshot AI (Kimi)](https://news.google.com/search?q=%22Moonshot+AI%22+OR+Kimi+AI&hl=en-US&gl=US&ceid=US%3Aen) | OK | 8 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 10 of 26 headlines name the subject |
| 117 | [Google News · Zhipu (Z.ai, GLM)](https://news.google.com/search?q=Zhipu+OR+%22Z.ai%22+GLM&hl=en-US&gl=US&ceid=US%3Aen) | OK | 1 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 1 of 7 headlines name the subject |
| 118 | [Google News · Perplexity](https://news.google.com/search?q=%22Perplexity+AI%22+OR+%22Perplexity%22+Comet&hl=en-US&gl=US&ceid=US%3Aen) | OK | 2 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 2 of 6 headlines name the subject |
| 119 | [Google News · Hugging Face](https://news.google.com/search?q=%22Hugging+Face%22&hl=en-US&gl=US&ceid=US%3Aen) | OK | 4 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 4 of 30 headlines name the subject |
| 120 | [Google News · Stability AI](https://news.google.com/search?q=%22Stability+AI%22&hl=en-US&gl=US&ceid=US%3Aen) | OK | 0 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only); 0 of 4 headlines name the subject |
| 121 | [Anthropic status · incidents (last 72 h)](https://status.anthropic.com) | OK | 1 | unranked | 08:12 | Statuspage public API |
| 122 | [OpenAI status · incidents (last 72 h)](https://status.openai.com) | OK | 1 | unranked | 08:12 | Statuspage public API |
| 123 | [Mistral AI status · incidents (last 72 h)](https://status.mistral.ai) | OK | 1 | unranked | 08:12 | Statuspage public API |
| 124 | [Cohere status · incidents (last 72 h)](https://status.cohere.com) | OK | 0 | unranked | 08:12 | Statuspage public API |
| 125 | [Perplexity status · incidents (last 72 h)](https://status.perplexity.com) | OK | 0 | unranked | 08:12 | Statuspage public API |
| 126 | [ElevenLabs status · incidents (last 72 h)](https://status.elevenlabs.io) | OK | 1 | unranked | 08:12 | Statuspage public API |
| 127 | [GitHub releases · AI lab SDKs and tools (last 14 days)](https://github.com/) | OK | 20 | unranked | 08:12 | public releases.atom feeds of 16 lab repositories, up to 2 releases each |
| 128 | [OpenRouter · models added by the big labs (last 60 days)](https://openrouter.ai/models) | OK | 27 | unranked | 08:12 | public models API, models whose id starts with a tracked lab, newest first |
| 129 | [Hugging Face · newest open-weight models from the big labs (last 30 days)](https://huggingface.co/models?sort=created) | OK | 19 | unranked | 08:12 | Hub API, newest models of 16 lab organisations |
| 130 | [LMArena · text leaderboard](https://lmarena.ai/leaderboard/text) | Skipped | 0 | unranked | 08:12 | HTTP 502 |
| 131 | [LMArena · text-to-image leaderboard](https://lmarena.ai/leaderboard/text-to-image) | OK | 10 | unranked | 08:12 | LMArena leaderboard dataset on Hugging Face (CC BY 4.0), 'text_to_image' overall, published 2026-11-20 |
| 132 | [LMArena · text-to-video leaderboard](https://lmarena.ai/leaderboard/text-to-video) | Skipped | 0 | unranked | 08:12 | HTTP 502 |
| 133 | [Google News · AI media (Sora, Veo, Runway)](https://news.google.com/search?q=Sora+OpenAI+video+OR+%22Google+Veo%22+OR+%22Runway%22+AI+video&hl=en-US&gl=US&ceid=US%3Aen) | OK | 1 | unranked | 08:12 | Google News RSS search, last 72 h, newest first (headline and outlet only); 1 of 5 headlines name the subject |
| 134 | [Google News · AI media (Luma, Pika, Kling)](https://news.google.com/search?q=%22Luma+AI%22+OR+%22Pika%22+AI+video+OR+%22Kling%22+AI&hl=en-US&gl=US&ceid=US%3Aen) | OK | 5 | unranked | 08:12 | Google News RSS search, last 72 h, newest first (headline and outlet only); 5 of 8 headlines name the subject |
| 135 | [Google News · AI media (Hailuo, Higgsfield, Midjourney)](https://news.google.com/search?q=Hailuo+OR+MiniMax+video+OR+Higgsfield+OR+Midjourney&hl=en-US&gl=US&ceid=US%3Aen) | OK | 10 | unranked | 08:12 | Google News RSS search, last 72 h, newest first (headline and outlet only); 16 of 18 headlines name the subject |
| 136 | [Google News · AI media (FLUX, ElevenLabs, Suno)](https://news.google.com/search?q=%22Black+Forest+Labs%22+OR+FLUX+image+model+OR+ElevenLabs+OR+Suno&hl=en-US&gl=US&ceid=US%3Aen) | OK | 1 | unranked | 08:12 | Google News RSS search, last 72 h, newest first (headline and outlet only); 1 of 17 headlines name the subject |
| 137 | [Google News · AI media (Udio, HeyGen, Synthesia)](https://news.google.com/search?q=Udio+OR+HeyGen+OR+Synthesia+OR+%22Nano+Banana%22&hl=en-US&gl=US&ceid=US%3Aen) | OK | 10 | unranked | 08:12 | Google News RSS search, last 72 h, newest first (headline and outlet only); 10 of 15 headlines name the subject |
| 138 | [Hugging Face · trending video, image and audio models](https://huggingface.co/models?sort=trending) | OK | 30 | unranked | 08:12 | Hub API sort=trendingScore, top 6 for each of text-to-video, image-to-video, text-to-image, text-to-speech… |
| 139 | [The Decoder](https://the-decoder.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (10 found) |
| 140 | [TechCrunch · AI](https://techcrunch.com/category/artificial-intelligence/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (20 found) |
| 141 | [MIT Technology Review · AI](https://www.technologyreview.com/topic/artificial-intelligence/feed) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (7 found) |
| 142 | [Import AI](https://importai.substack.com/feed) | OK | 1 | unranked | 08:12 | feed, items from the last 168 h (1 found) |
| 143 | [Latent Space](https://www.latent.space/feed) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (9 found) |
| 144 | [Ben's Bites](https://www.bensbites.com/feed) | OK | 2 | unranked | 08:12 | feed, items from the last 168 h (2 found) |
| 145 | [Last Week in AI](https://lastweekin.ai/feed) | OK | 1 | unranked | 08:12 | feed, items from the last 168 h (1 found) |
| 146 | [TLDR AI](https://tldr.tech/api/rss/ai) | OK | 5 | unranked | 08:12 | feed, items from the last 168 h (5 found) |
| 147 | [The Rundown AI](https://www.therundown.ai/feed) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (9 found) |
| 148 | [Interconnects](https://www.interconnects.ai/feed) | OK | 0 | unranked | 08:12 | feed, items from the last 168 h (0 found) |
| 149 | [CNBC · top news](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (30 found) |
| 150 | [CNBC · markets](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258) | OK | 2 | unranked | 08:12 | feed, items from the last 36 h (2 found) |
| 151 | [CNBC · technology](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (10 found) |
| 152 | [MarketWatch · top stories](https://feeds.content.dowjones.io/public/rss/mw_topstories) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (10 found) |
| 153 | [Bloomberg · markets](https://feeds.bloomberg.com/markets/news.rss) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (20 found) |
| 154 | [Bloomberg · technology](https://feeds.bloomberg.com/technology/news.rss) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (10 found) |
| 155 | [Bloomberg · economics](https://feeds.bloomberg.com/economics/news.rss) | OK | 6 | unranked | 08:12 | feed, items from the last 36 h (6 found) |
| 156 | [Financial Times · home](https://www.ft.com/rss/home) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (9 found) |
| 157 | [Financial Times · technology](https://www.ft.com/technology?format=rss) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (14 found) |
| 158 | [New York Times · business](https://rss.nytimes.com/services/xml/rss/nyt/Business.xml) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (19 found) |
| 159 | [New York Times · technology](https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (9 found) |
| 160 | [BBC · business](https://feeds.bbci.co.uk/news/business/rss.xml) | OK | 4 | unranked | 08:12 | feed, items from the last 36 h (4 found) |
| 161 | [The Guardian · business](https://www.theguardian.com/uk/business/rss) | OK | 8 | unranked | 08:12 | feed, items from the last 36 h (21 found) |
| 162 | [The Economist · finance and economics](https://www.economist.com/finance-and-economics/rss.xml) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (7 found) |
| 163 | [The Information](https://www.theinformation.com/feed) | OK | 8 | unranked | 08:12 | feed, items from the last 72 h (20 found) |
| 164 | [Crunchbase News](https://news.crunchbase.com/feed/) | OK | 6 | unranked | 08:12 | feed, items from the last 72 h (6 found) |
| 165 | [TechCrunch · venture](https://techcrunch.com/category/venture/feed/) | OK | 1 | unranked | 08:12 | feed, items from the last 72 h (1 found) |
| 166 | [European Central Bank · press](https://www.ecb.europa.eu/rss/press.html) | OK | 6 | unranked | 08:12 | feed, items from the last 168 h (6 found) |
| 167 | [Federal Reserve · press releases](https://www.federalreserve.gov/feeds/press_all.xml) | OK | 4 | unranked | 08:12 | feed, items from the last 168 h (4 found) |
| 168 | [Google News · funding rounds and acquisitions](https://news.google.com/search?q=startup+raises+funding+round+OR+tech+acquisition+acquires&hl=en-US&gl=US&ceid=US%3Aen) | OK | 10 | unranked | 08:12 | Google News RSS search, last 48 h, newest first (headline and outlet only) |
| 169 | [Google News · IPOs and layoffs](https://news.google.com/search?q=tech+IPO+shares+debut+OR+tech+layoffs+job+cuts&hl=en-US&gl=US&ceid=US%3Aen) | OK | 10 | unranked | 08:13 | Google News RSS search, last 48 h, newest first (headline and outlet only) |
| 170 | [FRED · US markets and rates (St. Louis Fed)](https://fred.stlouisfed.org/) | OK | 6 | unranked | 08:12 | fredgraph.csv, last two published observations (FRED publishes with a delay of one or more days) |
| 171 | [ECB · euro reference rate (USD)](https://data.ecb.europa.eu/data/datasets/EXR) | OK | 1 | unranked | 08:12 | ECB Data Portal API, daily euro foreign exchange reference rate |
| 172 | [GitHub trending · this month](https://github.com/trending?since=monthly) | OK | 17 | ranked | 08:12 | 17 repos in the order GitHub shows them |
| 173 | [GitHub · most-starred repos created in the last 30 days](https://docs.github.com/en/rest/search/search#search-repositories) | OK | 25 | ranked | 08:12 | GitHub search API, created since 2026-10-23, sorted by stars; 25 repos that state a licence and a description |
| 174 | [GitHub · most-starred repos created in the last 365 days](https://docs.github.com/en/rest/search/search#search-repositories) | OK | 25 | ranked | 08:12 | GitHub search API, created since 2025-11-22, sorted by stars; 25 repos that state a licence and a description |
| 175 | [Hacker News · best of the last 30 days](https://news.ycombinator.com/best) | OK | 20 | ranked | 08:12 | Algolia HN API, stories from the last 30 days with 500+ points, sorted by points |
| 176 | [Hacker News · best of the last 365 days](https://news.ycombinator.com/best) | OK | 20 | ranked | 08:12 | Algolia HN API, stories from the last 365 days with 1,500+ points, sorted by points |
| 177 | [Dev.to · top this month](https://dev.to/top/month) | OK | 15 | ranked | 08:12 | Forem API top=30 |
| 178 | [Dev.to · top this year](https://dev.to/top/year) | OK | 15 | ranked | 08:12 | Forem API top=365 |
| 179 | [Hugging Face · papers of the week](https://huggingface.co/papers) | OK | 20 | ranked | 08:12 | daily_papers API week=2026-W47, sorted by community upvotes |
| 180 | [Hugging Face · papers of the month](https://huggingface.co/papers) | OK | 20 | ranked | 08:12 | daily_papers API month=2026-11, sorted by community upvotes |
| — | X trends | OK | — | — | — | reused the X trend tables stored in today's archive (no new X call) |
| — | Licence, topics and age for trending repos | OK | — | — | — | licence and topics added for 69 of 69 repos via the GitHub search API |
