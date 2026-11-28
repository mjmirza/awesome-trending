"""A JSON error body is a skipped source, not an empty day."""

from __future__ import annotations

import sys
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update  # noqa: E402


def _source(key: str):
    for src_key, _name, _url, fn in update.SOURCES:
        if src_key == key:
            return fn
    raise AssertionError(key)


class JsonListTest(unittest.TestCase):
    def test_empty_list_is_a_real_result(self):
        self.assertEqual(update.json_list({"items": [], "message": "OK"}, "items"), [])
        self.assertEqual(update.json_list([], None), [])

    def test_missing_list_uses_the_api_message(self):
        body = {"error_id": 502, "error_message": "too many requests from this IP", "error_name": "throttle_violation"}
        with self.assertRaises(update.FetchError) as ctx:
            update.json_list(body, "items")
        self.assertIn("too many requests from this IP", str(ctx.exception))

    def test_coingecko_status_and_crates_errors(self):
        limited = {"status": {"error_code": 429, "error_message": "Rate Limit Exceeded"}}
        with self.assertRaises(update.FetchError) as ctx:
            update.json_list(limited, "coins")
        self.assertEqual(str(ctx.exception), "Rate Limit Exceeded")

        blocked = {"errors": [{"detail": "blocked"}]}
        with self.assertRaises(update.FetchError) as ctx:
            update.json_list(blocked, "most_recently_downloaded")
        self.assertEqual(str(ctx.exception), "blocked")

    def test_non_list_value_is_a_failure(self):
        with self.assertRaises(update.FetchError) as ctx:
            update.json_list({"items": {"error": "nope"}}, "items")
        self.assertEqual(str(ctx.exception), "response had no items list")

    def test_bare_error_object_is_a_failure(self):
        with self.assertRaises(update.FetchError) as ctx:
            update.json_list({"error": "rate limit"})
        self.assertEqual(str(ctx.exception), "rate limit")


class SourcePayloadTest(unittest.TestCase):
    def setUp(self):
        self.kev_all = set(update.KEV_ALL)
        self.kev_recent = dict(update.KEV_RECENT)

    def tearDown(self):
        update.KEV_ALL.clear()
        update.KEV_ALL.update(self.kev_all)
        update.KEV_RECENT.clear()
        update.KEV_RECENT.update(self.kev_recent)

    def test_throttled_stackoverflow_is_skipped(self):
        body = {"error_id": 502, "error_message": "too many requests from this IP", "error_name": "throttle_violation"}
        with patch.object(update, "fetch_json", return_value=body):
            with self.assertRaises(update.FetchError):
                update.src_stackoverflow()
            results = update.run_sources({"stackoverflow"})
        res = results["stackoverflow"]
        self.assertFalse(res.ok)
        self.assertEqual(res.items, [])
        text = "\n".join(update.source_block("stackoverflow", results, 5, None))
        self.assertIn("Skipped today: too many requests from this IP", text)

    def test_stackoverflow_keeps_questions_and_drops_downvoted(self):
        body = {"items": [
            {"title": "How does X work?", "link": "https://stackoverflow.com/q/1", "score": 3,
             "answer_count": 1, "view_count": 10, "tags": ["python"], "is_answered": True, "creation_date": 1700000000},
            {"title": "Downvoted", "link": "https://stackoverflow.com/q/2", "score": -2,
             "answer_count": 0, "view_count": 1, "tags": [], "is_answered": False, "creation_date": 1700000000},
        ], "quota_remaining": 42}
        with patch.object(update, "fetch_json", return_value=body):
            items, note = update.src_stackoverflow()
        self.assertEqual([it["title"] for it in items], ["How does X work?"])
        self.assertIn("42", note)

    def test_empty_hits_list_is_not_a_failure(self):
        with patch.object(update, "fetch_json", return_value={"hits": []}):
            items, note = update.src_hn_front()
        self.assertEqual(items, [])
        self.assertIn("Algolia", note)

    def test_hn_error_object_is_a_failure(self):
        with patch.object(update, "fetch_json", return_value={"message": "Invalid query"}):
            with self.assertRaises(update.FetchError) as ctx:
                update.src_hn_front()
        self.assertIn("Invalid query", str(ctx.exception))

    def test_kev_error_does_not_look_like_an_empty_catalog(self):
        with patch.object(update, "fetch_json", return_value={"message": "temporarily unavailable"}):
            with self.assertRaises(update.FetchError) as ctx:
                update.src_kev()
        self.assertIn("temporarily unavailable", str(ctx.exception))
        self.assertEqual(update.KEV_ALL, self.kev_all)

    def test_kev_catalog_still_parses(self):
        added = (update.now_berlin().date() - timedelta(days=1)).isoformat()
        body = {"catalogVersion": "2026.11.28", "count": 1, "vulnerabilities": [{
            "cveID": "CVE-2026-99999", "vendorProject": "Example", "product": "Widget",
            "vulnerabilityName": "Example Widget flaw", "dateAdded": added, "dueDate": added,
            "knownRansomwareCampaignUse": "Unknown", "shortDescription": "A flaw.",
        }]}
        with patch.object(update, "fetch_json", return_value=body):
            items, note = update.src_kev()
        self.assertEqual([it["title"] for it in items], ["CVE-2026-99999"])
        self.assertIn("CVE-2026-99999", update.KEV_ALL)
        self.assertIn("2026.11.28", note)

    def test_status_page_with_no_incidents_stays_empty(self):
        with patch.object(update, "fetch_json", return_value={"incidents": []}):
            items, note = _source("githubstatus")()
        self.assertEqual(items, [])
        self.assertIn("Statuspage", note)

    def test_status_page_error_object_is_a_failure(self):
        with patch.object(update, "fetch_json", return_value={"error": "bad gateway"}):
            with self.assertRaises(update.FetchError) as ctx:
                _source("githubstatus")()
        self.assertEqual(str(ctx.exception), "bad gateway")

    def test_one_hub_error_does_not_drop_the_other_tasks(self):
        def fake(url, **_kw):
            if "text-to-video" in url:
                return {"error": "rate limit"}
            return [{"id": "org/m", "library_name": "pytorch", "downloads": 3, "likes": 1, "tags": [],
                     "createdAt": "2026-11-28T00:00:00Z"}]

        with patch.object(update, "fetch_json", side_effect=fake):
            items, _note = update.src_hf_media()
        tasks = {it["task"] for it in items}
        self.assertNotIn("text-to-video", tasks)
        self.assertEqual(tasks, {"image-to-video", "text-to-image", "text-to-speech", "text-to-audio"})

    def test_hub_errors_on_every_task_skip_the_source(self):
        with patch.object(update, "fetch_json", return_value={"error": "rate limit"}):
            with self.assertRaises(update.FetchError) as ctx:
                update.src_hf_media()
        self.assertIn("did not respond", str(ctx.exception))

    def test_wikipedia_retries_when_the_first_body_is_an_error(self):
        calls = []

        def fake(url, **_kw):
            calls.append(url)
            if len(calls) == 1:
                return {"error": "not ready"}
            return {"items": [{"articles": [
                {"article": "Main_Page", "views": 9, "rank": 1},
                {"article": "Category:Programming", "views": 4, "rank": 2},
                {"article": "Python", "views": 50, "rank": 3},
            ]}]}

        with patch.object(update, "fetch_json", side_effect=fake):
            items, _note = update.src_wikipedia()
        self.assertEqual(len(calls), 2)
        self.assertEqual([it["title"] for it in items], ["Python"])

    def test_wikipedia_does_not_retry_a_real_empty_day(self):
        calls = []

        def fake(url, **_kw):
            calls.append(url)
            return {"items": [{"articles": []}]}

        with patch.object(update, "fetch_json", side_effect=fake):
            items, _note = update.src_wikipedia()
        self.assertEqual(len(calls), 1)
        self.assertEqual(items, [])


if __name__ == "__main__":
    unittest.main()
