#!/usr/bin/env python3
"""Validate local package links and the published research's structural claims."""
import collections
import datetime as dt
import json
from pathlib import Path
import re


def validate(root):
    def read(name):
        return json.loads((root / "research" / name).read_text())

    inventory, closed, summary = read("inventory.json"), read("closed-unmerged.json"), read("summary.json")
    selected, findings = read("selection.json"), read("findings.json")
    ids = {p["number"] for p in inventory}
    closed_ids = {p["number"] for p in closed}
    assert len(ids) == len(inventory) == summary["merged_prs"]
    assert len(closed_ids) == len(closed) == summary["closed_unmerged_prs"]
    assert not ids & closed_ids
    assert all(p["mergedAt"] and "2025-10-20" <= p["mergedAt"][:10] <= "2026-10-20" for p in inventory)
    assert all(not p["mergedAt"] and "2025-10-20" <= p["closedAt"][:10] <= "2026-10-20" for p in closed)
    assert dict(collections.Counter(p["mergedAt"][:7] for p in inventory)) == summary["by_merge_month"]
    assert sum(p["reviewThreads"]["totalCount"] == 0 for p in inventory) == summary["zero_inline_threads"]
    assert len({p["author"]["login"] if p["author"] else "[deleted]" for p in inventory}) == summary["authors"]
    assert sum(p["reviews"]["totalCount"] for p in inventory) == summary["review_submissions"]
    assert sum(p["reviewThreads"]["totalCount"] for p in inventory) == summary["review_threads"]
    assert len(selected) == len({s["number"] for s in selected})
    assert sum(s["number"] in ids for s in selected) == summary["details_sample_merged_prs"]
    assert sum(s["number"] in closed_ids for s in selected) == summary["details_sample_closed_unmerged_prs"]
    assert all(s["number"] in ids | closed_ids and s["reasons"] for s in selected)
    assert all("body" not in p for p in inventory + closed)
    for name, items, key in [("search-bins.json", inventory, "mergedAt"),
                             ("closed-search-bins.json", closed, "closedAt")]:
        bins = read(name)
        assert len(bins) == 13
        assert sum(b["count"] for b in bins) == len(items)
        for b in bins:
            # A single date range is required: repeated qualifiers can override.
            ranges = re.findall(r"(?:merged|closed):(\d{4}-\d\d-\d\d)\.\.(\d{4}-\d\d-\d\d)", b["query"])
            assert len(ranges) == 1
            start, end = ranges[0]
            assert sum(start <= p[key][:10] <= end for p in items) == b["count"]
    assert len({f["id"] for f in findings}) == len(findings)
    for f in findings:
        for s in f["sources"]:
            assert s["pr"] in ids | closed_ids | set(summary["supplementary_open_prs"])
            assert s["url"].startswith(f"https://github.com/dealii/dealii/pull/{s['pr']}#")
            assert s["comment_after_merge"] == bool(s["pr_merged_at"] and s["created_at"] > s["pr_merged_at"])
            assert s["comment_predates_window"] == (s["created_at"] < "2025-10-20")
            dt.datetime.fromisoformat(s["created_at"].replace("Z", "+00:00"))
            assert s["reviewer"] != "Copilot" and not s["reviewer"].endswith("[bot]")
    # All relative Markdown links should resolve inside this package.
    for path in root.rglob("*.md"):
        if "raw" in path.relative_to(root).parts or ".git" in path.relative_to(root).parts:
            continue
        for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if re.match(r"[a-zA-Z]+://|#", link):
                continue
            destination = (path.parent / link.split("#")[0]).resolve()
            assert destination.is_relative_to(root.resolve()) and destination.exists(), (path, link)
    # When the ignored raw snapshot is available, verify sourced IDs and counters.
    raw = root / "research" / "raw"
    if (raw / "inline-comments.json").exists():
        comments = json.loads((raw / "inline-comments.json").read_text())
        within = [c for c in comments if int(c["pull_request_url"].split("/")[-1]) in ids
                  and "2025-10-20" <= c["created_at"][:10] <= "2026-10-20"]
        assert len(within) == summary["inline_comments_in_window_on_merged_prs"]
        for f in findings:
            for s in f["sources"]:
                pr = json.loads((raw / f"pr-{s['pr']}.json").read_text())
                candidates = pr["comments"] + pr["inline"]
                assert any(c["html_url"] == s["url"] and c["created_at"] == s["created_at"]
                           and c["user"]["login"] == s["reviewer"] for c in candidates), s
        for s in selected:
            pr = json.loads((raw / f"pr-{s['number']}.json").read_text())
            assert len(pr["files"]) == pr["pr"]["changed_files"]
        for path in [root / "README.md", root / "research/REPORT.md",
                     *list((root / "skills").rglob("*.md"))]:
            for url, number in re.findall(
                    r"(https://github\.com/dealii/dealii/pull/(\d+)#(?:discussion_r|issuecomment-)\d+)",
                    path.read_text()):
                data = json.loads((raw / f"pr-{number}.json").read_text())
                assert any(c["html_url"] == url for c in data["inline"] + data["comments"]), (path, url)
    print(f"Validated {len(inventory)} merged PRs, {len(selected)} sample entries, "
          f"{len(findings)} findings, and package links.")


if __name__ == "__main__":
    validate(Path(__file__).resolve().parents[1])
