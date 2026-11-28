"""Tests for weighting a source's rank score by that source's reach."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update  # noqa: E402


def _results(*lists) -> dict:
    """Build a results map from (key, name, items) tuples."""
    out = {}
    for key, name, items in lists:
        r = update.SourceResult(key, name, "https://example.com")
        r.ok = True
        r.items = items
        out[key] = r
    return out


def _score_of(ents, title: str) -> int:
    for e in ents:
        if e.item["title"] == title:
            return e.score
    raise AssertionError(f"missing {title}")


class RawVolumeTest(unittest.TestCase):
    def test_hn_uses_points_not_velocity(self):
        it = update.item("hn", "story", "https://news.ycombinator.com/item?id=1", points=7)
        self.assertEqual(update.raw_volume("hn_ask", it), (7.0, "hn_points"))

    def test_repo_prefers_gained_then_stars(self):
        gained = update.item("repo", "o/a", "https://github.com/o/a", stars=1000, gained=48)
        self.assertEqual(update.raw_volume("gh_daily", gained), (48.0, "repo_gained"))
        stars = update.item("repo", "o/b", "https://github.com/o/b", stars=288)
        self.assertEqual(update.raw_volume("gh_topic_robotics", stars), (288.0, "repo_stars"))

    def test_zero_question_score_is_kept(self):
        it = update.item("question", "q", "https://stackoverflow.com/q/1", score=0)
        self.assertEqual(update.raw_volume("stackoverflow", it), (0.0, "question_score"))


class ReachFromVolumeTest(unittest.TestCase):
    def test_typical_strong_figure_is_full_credit(self):
        self.assertAlmostEqual(
            update.reach_from_volume((100.0, "hn_points")), 1.0)
        self.assertAlmostEqual(
            update.reach_from_volume((200.0, "repo_gained")), 1.0)

    def test_above_scale_is_capped_at_one(self):
        self.assertEqual(update.reach_from_volume((495.0, "hn_points")), 1.0)
        self.assertEqual(update.reach_from_volume((1608.0, "repo_gained")), 1.0)

    def test_zero_hits_the_floor(self):
        self.assertEqual(update.reach_from_volume((0.0, "question_score")),
                         update.REACH_FLOOR)

    def test_quiet_hn_is_below_full_credit(self):
        reach = update.reach_from_volume((7.0, "hn_points"))
        expected = math.log1p(7) / math.log1p(update.VOLUME_SCALE["hn_points"])
        self.assertAlmostEqual(reach, expected)
        self.assertLess(reach, 0.5)
        self.assertGreater(reach, update.REACH_FLOOR)

    def test_missing_or_unknown_group_is_none(self):
        self.assertIsNone(update.reach_from_volume(None))
        self.assertIsNone(update.reach_from_volume((10.0, "not_a_group")))


class SourceReachTest(unittest.TestCase):
    def test_uses_the_number_one_item_for_the_whole_list(self):
        items = [
            update.item("hn", "strong", "https://news.ycombinator.com/item?id=1", points=495),
            update.item("hn", "weaker", "https://news.ycombinator.com/item?id=2", points=20),
        ]
        self.assertEqual(update.source_reach("hn_front", items), 1.0)

    def test_empty_or_metricless_list_gets_the_default(self):
        self.assertEqual(update.source_reach("hn_front", []), update.REACH_DEFAULT)
        bare = [update.item("mcp", "alpha", "https://example.com/a")]
        self.assertEqual(update.source_reach("smithery", bare), update.REACH_DEFAULT)


class BuildEntitiesReachTest(unittest.TestCase):
    def test_tiny_source_number_one_scores_below_big_source_number_one(self):
        results = _results(
            ("hn_front", "Hacker News · front page", [
                update.item("hn", "big-hn", "https://news.ycombinator.com/item?id=1",
                            points=495, comments=259),
            ]),
            ("hn_ask", "Hacker News · Ask HN", [
                update.item("hn", "tiny-ask", "https://news.ycombinator.com/item?id=2",
                            points=7, comments=10),
            ]),
            ("stackoverflow", "Stack Overflow", [
                update.item("question", "zero-so", "https://stackoverflow.com/q/1",
                            score=0, answers=1, views=40),
            ]),
        )
        ents = update.build_entities(results)
        big = _score_of(ents, "big-hn")
        tiny = _score_of(ents, "tiny-ask")
        zero = _score_of(ents, "zero-so")
        self.assertEqual(big, 60)
        self.assertEqual(tiny, round(100 * update.W_RANK * update.source_reach(
            "hn_ask", results["hn_ask"].items)))
        self.assertEqual(zero, round(100 * update.W_RANK * update.REACH_FLOOR))
        self.assertLess(tiny, big)
        self.assertLess(zero, tiny)
        scores = {e.score for e in ents}
        self.assertGreater(len(scores), 1, "scores should no longer be a single tie")

    def test_number_two_on_a_strong_list_can_beat_a_tiny_number_one(self):
        results = _results(
            ("gh_daily", "GitHub trending · today", [
                update.item("repo", "hot/repo", "https://github.com/hot/repo",
                            stars=26400, gained=1608),
                update.item("repo", "second/repo", "https://github.com/second/repo",
                            stars=20100, gained=243),
            ]),
            ("hn_ask", "Hacker News · Ask HN", [
                update.item("hn", "tiny-ask", "https://news.ycombinator.com/item?id=2",
                            points=7, comments=10),
            ]),
        )
        ents = update.build_entities(results)
        self.assertEqual(_score_of(ents, "hot/repo"), 60)
        second = _score_of(ents, "second/repo")
        tiny = _score_of(ents, "tiny-ask")
        # Position 2 of 2, reach 1.0 -> percentile 0.5, score 30.
        # A 7-point Ask HN #1 is lower than a mid-list item on a strong source.
        self.assertEqual(second, round(100 * update.W_RANK * 0.5))
        self.assertLess(tiny, second)

    def test_unranked_items_keep_the_base_score(self):
        results = _results(
            ("kev", "CISA KEV", [
                update.item("kev", "CVE-2026-1", "https://example.com/cve",
                            name="Example"),
            ]),
        )
        ents = update.build_entities(results)
        self.assertEqual(ents[0].best_pct, update.UNRANKED_BASE)
        self.assertEqual(ents[0].score, round(100 * update.W_RANK * update.UNRANKED_BASE))


if __name__ == "__main__":
    unittest.main()
