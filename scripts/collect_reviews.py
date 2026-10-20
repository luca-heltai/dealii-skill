#!/usr/bin/env python3
"""Collect a bounded, paginated GitHub research snapshot using authenticated gh.

Raw discussion bodies stay ignored. Published evidence should paraphrase them.
Run from the repository root. Existing raw responses are reused; use a fresh
output directory for a new snapshot. This script performs read-only API calls.
"""
import argparse
import concurrent.futures
import datetime as dt
import json
from pathlib import Path
import subprocess
import time


def api(endpoint, **fields):
    cmd = ["gh", "api", endpoint, "--method", "POST" if endpoint == "graphql" else "GET"]
    for key, value in fields.items():
        cmd += ["-f", f"{key}={value}"]
    for attempt in range(4):
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if isinstance(data, dict) and data.get("errors"):
                raise RuntimeError(data["errors"])
            return data
        if attempt == 3:
            raise RuntimeError(result.stderr)
        time.sleep(2 ** attempt)


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def pages(endpoint):
    rows, page = [], 1
    while True:
        chunk = api(endpoint, per_page=100, page=page)
        rows.extend(chunk)
        if len(chunk) < 100:
            return rows
        page += 1


QUERY = """query($q:String!, $cursor:String) {
  search(query:$q, type:ISSUE, first:100, after:$cursor) {
    issueCount pageInfo {hasNextPage endCursor}
    nodes { ... on PullRequest {
      number title url mergedAt closedAt createdAt updatedAt body
      author {login} additions deletions changedFiles
      baseRefName headRefOid mergeCommit {oid}
      labels(first:100) {nodes {name}}
      comments {totalCount} reviews {totalCount} reviewThreads {totalCount}
    }}
  }
}"""


def inventory(start, end, output, merged=True):
    rows, bins = {}, []
    current = start
    while current < end:
        following = min(end, (current.replace(day=28) + dt.timedelta(days=4)).replace(day=1))
        qualifier = "is:merged merged" if merged else "is:unmerged is:closed closed"
        q = f"repo:dealii/dealii is:pr {qualifier}:{current}..{following - dt.timedelta(days=1)}"
        cache = output / "raw" / f"{'merged' if merged else 'closed'}-{current}.json"
        batch = None
        if cache.exists():
            batch = json.loads(cache.read_text())
            date_key = "mergedAt" if merged else "closedAt"
            if not all(r.get(date_key) and str(current) <= r[date_key][:10] < str(following)
                       and (bool(r.get("mergedAt")) == merged) for r in batch):
                batch = None
        if batch is None:
            batch, cursor, expected = [], None, None
            while True:
                fields = {"query": QUERY, "q": q}
                if cursor:
                    fields["cursor"] = cursor
                data = api("graphql", **fields)["data"]["search"]
                expected = data["issueCount"]
                if expected > 1000:
                    raise RuntimeError(f"Split search interval: {q} returns {expected}")
                batch.extend(data["nodes"])
                if not data["pageInfo"]["hasNextPage"]:
                    break
                cursor = data["pageInfo"]["endCursor"]
            if len(batch) != expected:
                raise RuntimeError(f"Incomplete search: {q}: {len(batch)} != {expected}")
            save(cache, batch)
        bins.append({"query": q, "count": len(batch)})
        rows.update({r["number"]: r for r in batch})
        print(f"{current}: {len(batch)}", flush=True)
        current = following
    save(output / ("inventory.json" if merged else "closed-unmerged.json"),
         [{k: v for k, v in r.items() if k != "body"} for r in rows.values()])
    save(output / ("search-bins.json" if merged else "closed-search-bins.json"), bins)
    return list(rows.values())


def inline(start, output):
    path = output / "raw" / "inline-comments.json"
    if path.exists():
        return json.loads(path.read_text())
    rows = pages(f"repos/dealii/dealii/pulls/comments?since={start}T00:00:00Z&sort=created&direction=asc")
    save(path, rows)
    print(f"Downloaded {len(rows)} inline comments", flush=True)
    return rows


def detail(number, output):
    path = output / "raw" / f"pr-{number}.json"
    if path.exists():
        return
    prefix = f"repos/dealii/dealii"
    data = {"number": number,
            "pr": api(f"{prefix}/pulls/{number}"),
            "comments": pages(f"{prefix}/issues/{number}/comments"),
            "reviews": pages(f"{prefix}/pulls/{number}/reviews"),
            "files": pages(f"{prefix}/pulls/{number}/files"),
            "inline": pages(f"{prefix}/pulls/{number}/comments")}
    save(path, data)
    print(f"PR #{number}: {len(data['inline'])} inline, {len(data['comments'])} discussion", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["inventory", "inline", "details", "closed"])
    parser.add_argument("--start", default="2025-10-20")
    parser.add_argument("--end", default="2026-10-21", help="Exclusive UTC calendar date")
    parser.add_argument("--output", type=Path, default=Path("research"))
    parser.add_argument("--numbers", nargs="*", type=int, default=[])
    parser.add_argument("--selection", type=Path, help="JSON selection file containing number fields")
    args = parser.parse_args()
    if args.mode in {"inventory", "closed"}:
        inventory(dt.date.fromisoformat(args.start), dt.date.fromisoformat(args.end), args.output,
                  merged=args.mode == "inventory")
    elif args.mode == "inline":
        inline(args.start, args.output)
    else:
        numbers = args.numbers
        if args.selection:
            numbers = list(dict.fromkeys(numbers + [row["number"] for row in json.loads(args.selection.read_text())]))
        if not numbers:
            parser.error("details requires --numbers or --selection")
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(lambda n: detail(n, args.output), numbers))


if __name__ == "__main__":
    main()
