"""Tests for Top signals tie-breaking on per-source engagement."""

from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update  # noqa: E402


NOW = datetime(2026, 11, 25, 8, 12, tzinfo=timezone.utc)


def _ent(key: str, it: dict, score: int = 60, best_pct: float = 1.0,
         families: list[str] | None = None) -> update.Entity:
    e = update.Entity()
    e.hits.append((key, it, best_pct, 1))
    e.families = families or ["GitHub"]
    e.score = score
    e.best_pct = best_pct
    return e


def _repo(title: str, gained: int, stars: int = 1000) -> dict:
    return update.item("repo", title, f"https://github.com/{title}", stars=stars, gained=gained)


def _hn(title: str, points: int, hours_ago: float) -> dict:
    created = NOW - timedelta(hours=hours_ago)
    return update.item("hn", title, f"https://news.ycombinator.com/item?id={title}",
                       points=points, comments=10, created=created)


class EngagementHelpersTest(unittest.TestCase):
    def test_repo_uses_stars_gained(self):
        pair = update.raw_engagement("gh_daily", _repo("o/a", 1826), NOW)
        self.assertEqual(pair, (1826.0, "repo_gained"))

    def test_hn_uses_points_per_hour(self):
        pair = update.raw_engagement("hn_front", _hn("story", 80, 2), NOW)
        self.assertIsNotNone(pair)
        val, group = pair
        self.assertEqual(group, "hn_velocity")
        self.assertAlmostEqual(val, 40.0)

    def test_product_hunt_votes(self):
        it = update.item("product", "Widget", "https://www.producthunt.com/posts/widget", votes=320)
        self.assertEqual(update.raw_engagement("producthunt", it, NOW), (320.0, "product_votes"))

    def test_missing_metric_is_none(self):
        it = update.item("product", "Widget", "https://www.producthunt.com/posts/widget")
        self.assertIsNone(update.raw_engagement("producthunt", it, NOW))

    def test_percentiles_are_deterministic_and_tied(self):
        self.assertEqual(update.engagement_percentiles([10.0]), [1.0])
        got = update.engagement_percentiles([1826.0, 360.0, 38.0, 34.0])
        self.assertEqual(len(got), 4)
        for a, b in zip(got, (1.0, 2 / 3, 1 / 3, 0.0)):
            self.assertAlmostEqual(a, b)
        self.assertEqual(update.engagement_percentiles([5.0, 5.0, 1.0]), [1.0, 1.0, 0.0])


class TopSignalsTieBreakTest(unittest.TestCase):
    def test_github_gained_reorders_tied_scores(self):
        ents = [
            _ent("gh_daily", _repo("low/stars", 34)),
            _ent("gh_daily", _repo("mid/stars", 360)),
            _ent("gh_daily", _repo("high/stars", 1826)),
        ]
        top = update.top_signals(ents, 3, now=NOW)
        self.assertEqual([e.item["title"] for e in top],
                         ["high/stars", "mid/stars", "low/stars"])

    def test_normalise_per_type_so_raw_units_do_not_dominate(self):
        # 1826 stars gained would beat 80 points/hour if compared raw.
        # After per-type normalisation both leaders score 1.0, so recency decides.
        older = NOW - timedelta(hours=10)
        newer = NOW - timedelta(hours=2)
        repo = _repo("hot/repo", 1826)
        repo["created"] = older
        hn = _hn("hot-hn", 160, 2)  # 80 pts/h
        hn["created"] = newer
        cold = _repo("cold/repo", 10)
        cold["created"] = newer
        ents = [
            _ent("gh_daily", repo, families=["GitHub"]),
            _ent("hn_front", hn, families=["Hacker News"]),
            _ent("gh_daily", cold, families=["GitHub"]),
        ]
        top = update.top_signals(ents, 3, now=NOW)
        titles = [e.item["title"] for e in top]
        self.assertEqual(titles[0], "hot-hn", "type leaders tie on engagement; newer HN item should win")
        self.assertEqual(titles[1], "hot/repo")
        self.assertEqual(titles[2], "cold/repo")

    def test_fallback_to_recency_then_source_order(self):
        older = update.item("news", "old-headline", "https://example.com/old",
                            published=NOW - timedelta(hours=8))
        newer = update.item("news", "new-headline", "https://example.com/new",
                            published=NOW - timedelta(hours=1))
        # Unranked news is excluded from Top signals (best_pct == UNRANKED_BASE).
        # Use ranked items that have no engagement figure.
        a = update.item("mcp", "alpha", "https://example.com/a")
        b = update.item("mcp", "beta", "https://example.com/b")
        a["published"] = NOW - timedelta(hours=8)
        b["published"] = NOW - timedelta(hours=1)
        ents = [
            _ent("smithery", a, families=["Smithery"]),
            _ent("smithery", b, families=["Smithery"]),
        ]
        top = update.top_signals(ents, 2, now=NOW)
        self.assertEqual([e.item["title"] for e in top], ["beta", "alpha"])

        bare_a = update.item("mcp", "first", "https://example.com/1")
        bare_b = update.item("mcp", "second", "https://example.com/2")
        ents = [
            _ent("smithery", bare_a, families=["Smithery"]),
            _ent("smithery", bare_b, families=["Smithery"]),
        ]
        top = update.top_signals(ents, 2, now=NOW)
        self.assertEqual([e.item["title"] for e in top], ["first", "second"])

    def test_primary_score_still_wins(self):
        low = _ent("gh_daily", _repo("spread/repo", 1), score=60, families=["GitHub"])
        high = _ent("gh_daily", _repo("shared/repo", 1), score=73, families=["GitHub"])
        # give the low-score item more gained stars
        low.item["gained"] = 5000
        top = update.top_signals([low, high], 2, now=NOW)
        self.assertEqual([e.item["title"] for e in top], ["shared/repo", "spread/repo"])

    def test_today_like_order_differs_from_source_order(self):
        """Replay the 15 score-60 items from 25 Nov 2026, with no recency dates.

        Before: source order, because every row scored 60.
        After: type leaders (engagement 1.0) stay ahead of weaker same-type
        rows, so jan (+34 stars) and the slower HN threads drop.
        """
        ents = [
            _ent("gh_daily", _repo("elementalsouls/Claude-BugHunter", 1826, 21900)),
            _ent("gh_daily", _repo("cursor/plugins", 360, 19300)),
            _ent("gh_rust", _repo("janhq/jan", 34, 46100)),
            _ent("gh_go", _repo("datazip-inc/olake-go", 38, 2300)),
            _ent("hn_front", update.item("hn", "Matrix Multiplication",
                                         "https://news.ycombinator.com/item?id=matrix",
                                         points=474, comments=232), families=["Hacker News"]),
            _ent("hn_front", update.item("hn", "Ask HN: Anthropic",
                                         "https://news.ycombinator.com/item?id=ask",
                                         points=242, comments=183), families=["Hacker News"]),
            _ent("hn_show", update.item("hn", "Show HN: Mason",
                                        "https://masondata.ai/",
                                        points=93, comments=17), families=["Hacker News"]),
            _ent("hf_models", update.item("model", "thinkingmachines/Inkling-2-Mini",
                                          "https://huggingface.co/thinkingmachines/Inkling-2-Mini",
                                          likes=5838, downloads=69000), families=["Hugging Face"]),
            _ent("hf_spaces", update.item("space", "JCisHERE/wan2-2-i2v-v3",
                                          "https://huggingface.co/spaces/JCisHERE/wan2-2-i2v-v3",
                                          likes=730), families=["Hugging Face"]),
            _ent("hf_datasets", update.item("dataset", "Vyber07/cyber-security",
                                            "https://huggingface.co/datasets/Vyber07/cyber-security",
                                            likes=1744, downloads=35300), families=["Hugging Face"]),
            _ent("hf_papers", update.item("paper", "ACAP",
                                          "https://huggingface.co/papers/2611.31205",
                                          upvotes=44), families=["Hugging Face"]),
            _ent("smithery", update.item("mcp", "Brave Search",
                                         "https://registry.smithery.ai/servers/brave",
                                         uses=87579), families=["Smithery"]),
            _ent("npm", update.item("package", "@modelcontextprotocol/sdk",
                                    "https://www.npmjs.com/package/@modelcontextprotocol/sdk",
                                    weekly=93_200_000), families=["npm"]),
            _ent("jsdelivr", update.item("cdn", "swiper",
                                         "https://www.jsdelivr.com/package/npm/swiper",
                                         hits=4_600_000_000), families=["jsDelivr"]),
            _ent("devto_day", update.item("post", "The Third Cup",
                                          "https://dev.to/thethirdcup/after",
                                          reactions=72, comments=32), families=["Dev.to"]),
        ]
        before = [e.item["title"] for e in ents]
        # Old sort: (score, families, best_pct) — all equal, so source order.
        old = sorted(ents, key=lambda e: (e.score, len(e.families), e.best_pct), reverse=True)
        self.assertEqual([e.item["title"] for e in old], before)

        after = [e.item["title"] for e in update.top_signals(ents, 15, now=NOW)]
        self.assertNotEqual(after, before)
        # Type leaders (engagement 1.0) keep source order among themselves
        # because no recency is set, then weaker GitHub/HN rows follow.
        self.assertEqual(after[0], "elementalsouls/Claude-BugHunter")
        self.assertLess(after.index("datazip-inc/olake-go"), after.index("janhq/jan"))
        self.assertLess(after.index("Matrix Multiplication"), after.index("Ask HN: Anthropic"))
        self.assertGreater(after.index("janhq/jan"), after.index("Brave Search"))
        self.assertGreater(after.index("janhq/jan"), after.index("swiper"))
        # Running twice with the same clock is deterministic.
        again = [e.item["title"] for e in update.top_signals(ents, 15, now=NOW)]
        self.assertEqual(after, again)
        print("BEFORE:", before)
        print("AFTER: ", after)


if __name__ == "__main__":
    unittest.main()
