# Research snapshot: deal.II contribution and review patterns

## Scope and coverage

Repository: [dealii/dealii](https://github.com/dealii/dealii). Window: PRs merged
from **20 October 2025, 00:00 UTC**, through the collection on **20 October 2026**.
The last calendar day is incomplete. Monthly GitHub queries use inclusive date
ranges, with non-overlapping intervals. The snapshot is collected over multiple
API requests, not as an atomic transaction.

| Collected quantity | Count |
| --- | ---: |
| Merged PRs, enumerated and deduplicated | 1,082 |
| Distinct author logins | 65 |
| Review submissions on those PRs, lifetime metadata | 3,251 |
| Inline review threads, lifetime metadata | 1,699 |
| Inline comments created within the window on merged PRs | 2,574 |
| Merged PRs with those in-window comments | 332 |
| Merged PRs with zero inline threads in metadata | 747 |
| Closed, unmerged PRs with closure in the window | 61 |
| Detailed retrieval sample, merged | 72 |
| Detailed retrieval sample, closed without merge | 5 |

There is one supplementary open PR, #20217. It is not part of the merged or
closed-unmerged sample. Review submissions include approvals, requests for
changes, comments, and automated reviews; they are not a count of objections.
Zero inline threads does not imply zero review, unchanged acceptance, or
absence of discussion comments.

Monthly merged counts are 30, 43, 85, 73, 68, 99, 110, 142, 164, 97, 65, 63,
and 43, for October 2025 through October 2026 respectively. Both Octobers are
partial months. The median additions-plus-deletions count is 38; 66 PRs exceed
1,000 by that metric. This is descriptive metadata, not a quality threshold.

## Method

1. Enumerate all merged PRs with GitHub GraphQL search, partitioned by merge
   month. Paginate each interval, check its returned count, and deduplicate PR
   numbers. Retain titles, dates, authors, labels, change sizes, head and merge
   revisions, and discussion counts. An independent REST search count checks
   the annual totals. Inventory bodies are excluded from the published data.
2. Collect the repository's inline review comments updated since the window
   start, with REST pagination. Filter by PR membership and **creation date**
   when counting in-period comments. The raw endpoint also returns comments on
   open/unmerged PRs and older comments edited during the window; those do not
   enter the 2,574 count.
3. Retrieve full paginated issue discussions, review submissions, inline
   comments, and changed-file metadata/patches for a targeted sample. Per merge
   month, select the top three PRs by thread count, then discussion count, then
   PR number; also select a middle-number PR among those with 1–5 threads and
   one among those with zero threads, when available. Add purposive technical
   cases and five contrasting closed PRs. All selection reasons are retained.
4. Screen sample titles, changed-file lists, and substantive review excerpts;
   examine selected discussions and patch excerpts more closely to formulate
   the findings. Follow replies, accepted alternatives, and relevant post-merge
   comments before turning a suggestion into guidance. This is **targeted
   qualitative reading**, not full manual annotation of every downloaded
   comment or line of every patch. No frequency or statistical confidence is
   assigned to the patterns.
5. Compare the findings to the contribution policy, coding conventions,
   testsuite documentation, documentation guide, PR template, and formatting
   scripts at upstream commit `9e5d24772d9f2a115e4822b94a4fcaaf8a8a309d`.
   Official requirements and inferred practices are kept distinct in the skill.

The 77-PR retrieval sample contains 1,614 lifetime inline comments, 558 issue
comments, and 840 review submissions. Older discussion is retained as context
for long-lived PRs merged during the window; it is not recounted as new review
activity during the year. Comments after merge are explicitly identified when
used. A bot suggestion is not treated as a maintainer requirement. Links and
metadata for 25 curated findings and 46 source comments are in `findings.json`.

## Findings that affect implementation

The most useful unit of guidance is a **decision with a reason and an exception**.
Formatting is only one part of contribution quality. The detailed, linked
[pattern reference](../skills/dealii-developer/references/review-patterns.md)
records the concrete sources.

- **Scope controls review cost.** #18948 was asked to separate independent matrix
  functionality. #19784 received the same advice. #20116 was reduced to a subset
  the author had manually inspected after reviewers found repeated dimension
  predicates and other generated artifacts. The guideline to keep patches around
  1,000 changed/new lines is explicitly a rule of thumb, not a hard limit.
- **Interfaces communicate semantics.** #18911 discusses names that include
  analysis/state updates, meaningful norm enums, avoiding vector copies, and
  inputs before outputs. Passive options and active controllers have different
  roles. Naming consistency helps users reason about behavior.
- **Reuse belongs at the semantic owner.** #19149 replaces local detection
  machinery with existing utilities. #19161 locates shared topology knowledge in
  `ReferenceCell`. #19784 centralizes repeated coefficients. #20161 explicitly
  allows complexity costs to outweigh deduplication.
- **Parallel contracts dominate local simplification.** A post-merge comment on
  #19149 identifies a rank-local `continue` before a collective. In #18941, an
  initially similar concern is withdrawn after checking that local work precedes
  one reduction. #18938 asks for an explicit communicator; #19647 restores
  thread-safety required by existing callers. These are different mechanisms.
- **Types and configurations carry meaning.** #19069 addresses 64-to-32-bit
  narrowing; #19080 distinguishes local sizes from global indices. #19544 shows
  include, optional-MPI, and module-build problems. An implementation that builds
  in one convenient configuration is insufficient evidence for broad support.
- **Tests need an oracle and a relevant path.** #19011 changes approximation
  output into interpretable errors against `std::exp`; #19796 uses an analytical
  solution. #19019 asks for a reproducible in-tree test. #18941 also shows why
  existing tests can make an additional regression unnecessary.
- **Documentation is an interface.** #18948 catches a parameter copied from a
  different overload; #19161 removes descriptions of obsolete code. #18907 and
  #19828 receive mathematical corrections. #20281 declines platform instructions
  the reviewer could not validate.

The corresponding do/don't pairs are not stylistic slogans: preserve semantics
while simplifying; reuse facilities when they actually match; retain alias-safe
copies; check runtime errors in the intended build modes; measure optimizations;
and state only the support and validation that exist.

## What was actually rejected

Do not infer rejection from the `merged=false` field alone:

| PR | Observed disposition | What it supports |
| --- | --- | --- |
| [#19984](https://github.com/dealii/dealii/pull/19984#issuecomment-4856584239) | Explicit rejection of an autonomous-account contribution | Human accountability is an enforced policy, not a cosmetic disclosure preference. |
| [#19052](https://github.com/dealii/dealii/pull/19052#issuecomment-3929030847) | Compatibility objections; closure in favor of preserving a behavior-selecting option | Simplifying an API does not justify silently changing established distributed semantics. |
| [#18880](https://github.com/dealii/dealii/pull/18880#issuecomment-3433124381) | Superseded by merged #18911 | The earlier review remains useful context, but closure was not rejection of the feature. |
| [#19407](https://github.com/dealii/dealii/pull/19407#issuecomment-4076368661) | Superseded by #19408 | A replacement PR can carry a simpler solution. |
| [#18406](https://github.com/dealii/dealii/pull/18406#issuecomment-3629521278) | Author withdrawal amid review-size/timeline disagreement, with favorable technical reviews also recorded | Large coupled changes impose review costs; this is not evidence that the algorithm was rejected. |

For merged PRs, the pattern table identifies **challenged intermediate code**,
not whole-PR rejection. The supplementary, still-open #20217 illustrates a
reviewer reconsidering a proposed abstraction; its ultimate acceptance is unknown.

## Reducing AI slop

#20116 is unusually direct evidence: the discussion explicitly identifies
generated artifacts, demonstrates redundant conditions and default-only
switches, and records narrowing the patch for manual inspection. The problem
was not merely word choice. The resulting skill asks the agent to audit the
complete diff for unnecessary branches, abstractions, includes, copies, stale
comments, weak tests, and unsupported claims, while preserving useful defensive
checks and mathematical explanation.

#19916's discussion also distinguishes optional AI-use disclosure from the
legal and personal responsibility of the submitting author. The current
`CONTRIBUTING.md` is authoritative. The skill does not claim to eliminate all
defects, detect AI authorship, supply human certification, or guarantee acceptance
without revision. Those claims would themselves be unsupported output.

## Limits and validation

The sample deliberately favors discussion-rich and technically varied PRs; it is
not a probability sample. Some areas and authors are more visible. Unmerged PRs
are only a small qualitative contrast, and no causal rejection rate is estimated.
Historical review comments are not present-day project policy. Some suggestions
were revised, deferred, or turned out not to work on the supported standard.

File lists are checked against the API's `changed_files` count for the sample.
REST patch fields may be missing or truncated for large/binary changes, and a
PR patch is not a complete archive of intermediate revisions. No claim is made
to have reconstructed every edit across review rounds, executed historical CI,
or rebuilt all sampled changes. Current-head/merge metadata is retained for
follow-up inspection of exact source revisions.

Validation of the **skill package** covers frontmatter, local links, corpus
counts and dates, selection membership, source-comment provenance, and collector
pagination/cache behavior. Evaluation scenarios are supplied for further agent
testing; manual scenario walkthroughs do not establish a measured improvement
in acceptance or a zero-defect rate. The most valuable next validation is real
maintainer use with recorded avoidable review corrections.

Checks completed for the initial package:

- The skill-creator `quick_validate.py` accepts the skill.
- `python3 scripts/validate_package.py` validates the 1,082-PR inventory,
  77 sample entries, 25 findings, and relative package links. With the local raw
  snapshot present, it also checks source-comment provenance and sampled file
  counts against the downloaded responses.
- `python3 -m unittest discover -s tests -v` passes four collector tests covering
  REST pagination, GraphQL pagination/date ranges, incomplete/oversized searches,
  published body exclusion, and invalid-cache refresh. The single-range query
  regression prevents GitHub's repeated date qualifiers from broadening a search.
- Independent annual REST searches report 1,082 merged and 61 closed-unmerged
  PRs with `incomplete_results=false`.

These checks validate packaging and research integrity, not the numerical
correctness of historical PRs or the future behavior of an agent using the skill.

## Reproduce or update

Requires Python 3.9+ and an authenticated `gh` with read access to public GitHub
metadata. Collection performs read-only API calls; ordinary skill use does not
run it. Use a fresh output directory for a new snapshot and run each collection
stage sequentially against that directory. Raw responses contain discussion
bodies and are intentionally ignored by Git. Do not commit them wholesale.

```sh
python3 scripts/collect_reviews.py inventory --output research-refresh
python3 scripts/collect_reviews.py closed --output research-refresh
python3 scripts/collect_reviews.py inline --output research-refresh
python3 scripts/collect_reviews.py details --output research-refresh --selection research/selection.json
python3 scripts/collect_reviews.py details --output research-refresh --numbers 20217
```

Dates default to this snapshot; pass `--start YYYY-MM-DD --end YYYY-MM-DD` for a
new window (`--end` is exclusive). The shown selection replays this snapshot's
sample; curate a new selection when changing the window. Do not silently relabel cached data as a fresh
analysis. Searches stop if an interval exceeds GitHub's 1,000-result limit or a
paginated count is inconsistent; split the interval before continuing.

`inventory.json`, `closed-unmerged.json`, and search-bin files record the broad
metadata. `selection.json` records the detailed retrieval sample. `summary.json`
records collection time and coverage. `findings.json` records the manually
curated observations and source provenance. A refreshed dataset needs renewed
reading and curation; downloading more comments does not validate old guidance.
