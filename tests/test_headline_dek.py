"""Feed summaries that repeat the headline must keep the dek."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update  # noqa: E402


NVIDIA_TITLE = (
    "Sources: Nvidia tells its manufacturing partners to halt AI server shipments to "
    "Malaysia, Singapore, Thailand, and Indonesia as the US steps up export controls "
    "(Financial Times)"
)
NVIDIA_SUMMARY = (
    "Financial Times : Sources: Nvidia tells its manufacturing partners to halt AI server "
    "shipments to Malaysia, Singapore, Thailand, and Indonesia as the US steps up export "
    "controls — Move comes as US steps up export controls to prevent Chinese access to AI "
    "computing power — Nvidia has told its manufacturing partners …"
)
WSJ_TITLE = (
    "Memory chip shortages prompt companies worldwide to set up procurement war rooms; "
    "some chip prices have risen 10x in a year, driving up electronics prices "
    "(Wall Street Journal)"
)
WSJ_SUMMARY = (
    "Wall Street Journal : Memory chip shortages prompt companies worldwide to set up "
    "procurement war rooms; some chip prices have risen 10x in a year, driving up "
    "electronics prices — A global shortage has companies scrambling—and it's sent prices "
    "on electronics soaring — At Blackmagic Design …"
)


class HeadlineDekTest(unittest.TestCase):
    def test_techmeme_dek_is_the_sentence_after_the_headline(self):
        dek = update.headline_dek(NVIDIA_TITLE, NVIDIA_SUMMARY)
        self.assertEqual(
            dek,
            "Move comes as US steps up export controls to prevent Chinese access to AI computing power",
        )

    def test_inner_emdash_stays_and_a_later_blurb_is_dropped(self):
        dek = update.headline_dek(WSJ_TITLE, WSJ_SUMMARY)
        self.assertEqual(
            dek,
            "A global shortage has companies scrambling—and it's sent prices on electronics soaring",
        )

    def test_clip_used_to_keep_only_the_repeated_headline(self):
        # The old 140-character clip ran before the dek was split off, so the
        # stored summary was the outlet line and the dek was thrown away.
        self.assertNotIn("Move comes as", update.clip(NVIDIA_SUMMARY, 140))
        kept = update.clip(update.summary_text(NVIDIA_TITLE, NVIDIA_SUMMARY), 140)
        self.assertTrue(kept.startswith("Move comes as US steps up export controls"))

    def test_plain_summary_is_unchanged(self):
        title = "A normal headline about chip supply"
        summary = "Memory prices rose again this quarter. Buyers are waiting."
        self.assertIsNone(update.headline_dek(title, summary))
        self.assertEqual(update.summary_text(title, summary), summary)

    def test_unrelated_emdash_is_not_a_dek(self):
        title = "Something else entirely happened today"
        summary = "Alpha team — beta result is not this headline."
        self.assertIsNone(update.headline_dek(title, summary))
        self.assertEqual(update.summary_text(title, summary), summary)

    def test_short_shared_prefix_is_not_the_same_headline(self):
        title = "The Fed holds interest rates steady at the current level"
        summary = "The — something unrelated that should stay put for readers."
        self.assertIsNone(update.headline_dek(title, summary))

    def test_why_shows_the_dek_not_the_outlet_line(self):
        it = update.item("news", NVIDIA_TITLE, "https://www.techmeme.com/x", desc=NVIDIA_SUMMARY)
        self.assertEqual(
            update.why("techmeme", it),
            "Move comes as US steps up export controls to prevent Chinese access to AI computing power",
        )

    def test_story_why_uses_the_dek_instead_of_skipping_the_summary(self):
        it = {"title": NVIDIA_TITLE, "desc": NVIDIA_SUMMARY, "via": None}
        self.assertEqual(
            update.story_why([("techmeme", it)]),
            "Move comes as US steps up export controls to prevent Chinese access to AI computing power",
        )

    def test_story_why_still_skips_a_summary_that_only_repeats_the_headline(self):
        it = {"title": "Nvidia halts server shipments abroad", "desc": "Financial Times : Nvidia halts server shipments abroad", "via": None}
        self.assertEqual(update.story_why([("techmeme", it)]), "")


if __name__ == "__main__":
    unittest.main()
