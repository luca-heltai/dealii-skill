"""Regression tests for API pagination and date-window collection integrity."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("collector", Path(__file__).resolve().parents[1] / "scripts/collect_reviews.py")
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


def response(nodes, count=None, more=False, cursor="next"):
    return {"data": {"search": {"nodes": nodes, "issueCount": len(nodes) if count is None else count,
                               "pageInfo": {"hasNextPage": more, "endCursor": cursor}}}}


class CollectionTests(unittest.TestCase):
    def test_rest_pagination_includes_tail(self):
        with patch.object(collector, "api", side_effect=[list(range(100)), [100, 101]]) as api:
            self.assertEqual(collector.pages("endpoint"), list(range(102)))
            self.assertEqual(api.call_args_list[1].kwargs["page"], 2)

    def test_graphql_window_pagination_and_body_exclusion(self):
        rows = [{"number": n, "mergedAt": "2025-10-21T00:00:00Z", "body": "private-to-raw"} for n in [1, 2]]
        with tempfile.TemporaryDirectory() as temp, patch.object(collector, "api", side_effect=[
            response(rows[:1], 2, True), response(rows[1:], 2)]) as api:
            output = Path(temp)
            result = collector.inventory(dt.date(2025, 10, 20), dt.date(2025, 11, 1), output)
            self.assertEqual(len(result), 2)
            self.assertEqual(api.call_args_list[0].kwargs["q"],
                             "repo:dealii/dealii is:pr is:merged merged:2025-10-20..2025-10-31")
            self.assertEqual(api.call_args_list[1].kwargs["cursor"], "next")
            self.assertNotIn("body", json.loads((output / "inventory.json").read_text())[0])

    def test_incomplete_and_oversized_searches_fail(self):
        for result in [response([], 2), response([], 1001)]:
            with tempfile.TemporaryDirectory() as temp, patch.object(collector, "api", return_value=result):
                with self.assertRaises(RuntimeError):
                    collector.inventory(dt.date(2025, 10, 20), dt.date(2025, 11, 1), Path(temp))

    def test_out_of_window_cache_is_refetched(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            collector.save(output / "raw/closed-2025-10-20.json", [
                {"number": 1, "closedAt": "2024-01-01T00:00:00Z", "mergedAt": None}])
            with patch.object(collector, "api", return_value=response([])) as api:
                self.assertEqual(collector.inventory(dt.date(2025, 10, 20), dt.date(2025, 11, 1), output, merged=False), [])
                api.assert_called_once()


if __name__ == "__main__":
    unittest.main()
