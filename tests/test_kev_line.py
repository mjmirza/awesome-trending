"""Tests for the CISA KEV line in Today in 30 seconds."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update  # noqa: E402


def _kev(cve: str, vendor: str, product: str, added: str = "2026-11-27") -> dict:
    return update.item("kev", cve, f"https://nvd.nist.gov/vuln/detail/{cve}", vendor=vendor, product=product,
                       added=added)


class KevLineTest(unittest.TestCase):
    def setUp(self) -> None:
        update.KEV_RECENT.clear()

    def test_bare_product_gets_vendor(self) -> None:
        self.assertEqual(update.kev_product_name(_kev("CVE-1", "Drupal", "Core")), "Drupal Core")

    def test_product_that_names_vendor_is_kept(self) -> None:
        self.assertEqual(update.kev_product_name(_kev("CVE-1", "OSGeo", "GeoServer")), "OSGeo GeoServer")
        self.assertEqual(update.kev_product_name(_kev("CVE-1", "Microsoft", "Microsoft Windows")), "Microsoft Windows")

    def test_multi_word_product_is_kept(self) -> None:
        self.assertEqual(update.kev_product_name(_kev("CVE-1", "Danfoss", "AK-SM 800A Series")), "AK-SM 800A Series")
        self.assertEqual(update.kev_product_name(
            _kev("CVE-1", "Hewlett Packard Enterprise (HPE)", "Juniper Session Smart Router")),
            "Juniper Session Smart Router")

    def test_line_groups_by_named_product(self) -> None:
        kev = [_kev("CVE-1", "OSGeo", "GeoServer"), _kev("CVE-2", "OSGeo", "GeoServer"), _kev("CVE-3", "Drupal", "Core")]
        line = update.kev_line(kev)
        self.assertIn("CISA added 3 on 2026-11-27 (OSGeo GeoServer (2 CVEs), Drupal Core)", line)


if __name__ == "__main__":
    unittest.main()
