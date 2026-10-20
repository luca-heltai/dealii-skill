# deal.II Developer skill

A reusable agent skill for implementing, reviewing, and preparing contributions
to [deal.II](https://github.com/dealii/dealii) and applications that use it.

The aim is to remove avoidable review work: redundant generated code, invented
APIs, unnecessary abstractions, weak numerical tests, misleading documentation,
and claims unsupported by executed checks. Acceptance remains a maintainer
decision; no skill can promise an unchanged merge or prove the absence of all
AI-generated defects.

## Use

Install the folder [`skills/dealii-developer`](skills/dealii-developer) in your
agent's skills directory using its normal skill installer. For a repository-based
installer, use repository `luca-heltai/dealii-skill` and path
`skills/dealii-developer`. The skill uses standard `SKILL.md` instructions and
relative references; GitHub access is not required during ordinary use when the
target checkout provides the necessary source and policy.

Example requests:

```text
Use $dealii-developer to fix this deal.II regression. Preserve unrelated work,
reproduce the failure, and prepare the patch and PR description for my review.
```

```text
Use $dealii-developer to review this downstream solver change. Follow this
project's conventions and check its deal.II, numerical, and MPI contracts.
```

The skill adapts to the task. A downstream application keeps its own style,
architecture, license, and tests. Library-specific rules apply to library code.

## What is included

- [`SKILL.md`](skills/dealii-developer/SKILL.md): the working instructions.
- [Library conventions](skills/dealii-developer/references/library-conventions.md):
  official sources and the details that affect implementation decisions.
- [Review patterns](skills/dealii-developer/references/review-patterns.md):
  observed objections, useful corrections, and counterexamples with direct links.
- [Validation and PR preparation](skills/dealii-developer/references/validation-and-pr.md):
  numerical oracles, test integration, configuration coverage, and honest reporting.
- [Research report](research/REPORT.md): coverage, sampling, findings, and limits.
- [Evaluation scenarios](evaluations/scenarios.md): concrete situations for
  testing and improving the skill.

## Evidence and responsibility

The 20 October 2026 snapshot inventories **1,082 merged PRs from 65 authors**,
collects **2,574 in-period inline comments on those PRs**, and retrieves a
77-PR discussion sample: 72 merged and 5 closed without merge. The report
distinguishes corpus collection, targeted reading, final changes, and later
follow-up defects. One additional open PR is explicitly labeled as supplementary
context. This is qualitative guidance, not an exhaustive line-by-line review of
all 1,082 PRs or a measurement of rejection probability.

deal.II's checked contribution policy requires a human author who understands
the entire patch and takes responsibility under the DCO. It rejects autonomous
agent contributions. This skill prepares work for that author; it cannot supply
their review or certification. Recheck the target's current policy before use.

This is an independent project for maintainer discussion, not an official
deal.II policy or endorsement. Improve it with specific review evidence and
observed behavior. Prefer correcting a demonstrated failure over adding another
universal checklist item.

Original skill text and tooling are provided under the [MIT license](LICENSE).
Upstream material remains under its own terms; linked discussions are paraphrased,
and raw discussion bodies are not distributed in this repository.
