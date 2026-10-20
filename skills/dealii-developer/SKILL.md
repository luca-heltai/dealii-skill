---
name: dealii-developer
description: Implement, review, test, and prepare C++ changes for deal.II or applications using deal.II, following its interfaces, numerical contracts, and review conventions. Use for deal.II contribution work, not generic C++ tasks with no deal.II dependency.
---

# deal.II developer

Produce a small, explainable change that an experienced deal.II developer can
review without repairing generated scaffolding. Acceptance remains a maintainer
decision. Passing tests and using this skill do not guarantee acceptance.

## Establish the actual contract

Read the target repository's instructions, contribution policy, PR template,
formatter configuration, and adjacent implementations. Inspect the branch, base,
working tree, configured build, installed deal.II version, and dependency versions
before editing. Preserve unrelated work.

For **deal.II itself**, follow that checkout's conventions and testsuite. For a
**downstream application**, preserve its architecture, naming, build system,
licensing, and tests. Apply deal.II API and numerical contracts at the boundary;
do not transplant library internals or its entire contribution workflow.

Use [library conventions](references/library-conventions.md) for library changes.
Use [review patterns](references/review-patterns.md) when choosing an interface,
fixing review feedback, or checking a suspicious generated implementation.
Use [validation and PR preparation](references/validation-and-pr.md) for tests,
build integration, and the final handoff. Read only the relevant reference.

Check declarations and real call sites for every API you introduce. Versioned
headers and the configured build are stronger evidence than remembered API names
or an example from another release. Separate official requirements from local
idioms and design choices inferred from reviews. Current project guidance takes
precedence over the historical examples bundled here.

## Choose the smallest complete design

Identify the failing behavior or missing capability, the mathematical or API
contract, and a representative caller. For a bug, construct the smallest useful
reproducer that still exercises the failure. For a feature, show the intended
call before building an abstraction around it.

- Reuse the existing owner of an operation: `ReferenceCell` for reference-cell
  topology, established vector import/communication facilities for distribution,
  existing traits and compatibility wrappers for type detection. Search first.
- Make names express the whole operation, including analysis, mutation, and
  communication when those affect callers. Put inputs before outputs in new
  library interfaces; return a small computed value directly when appropriate.
- Use `AdditionalData` for passive options where neighboring classes do so.
  Keep one source of defaults. Distinguish options from an active controller.
- State supported dimensions, `dim` versus `spacedim`, reference cells, scalar
  types, memory spaces, and vector backends. Implement the claimed combinations
  or explicitly constrain them. Avoid hard-coded hypercube assumptions in mixed
  mesh code and narrowing global indices to local-sized integers.
- Preserve overload resolution, defaults, observable behavior, ownership, and
  caller synchronization unless changing them is the explicit purpose. An API
  cleanup is not permission to change what existing callers compute.
- Keep independent cleanups in separate patches. The upstream guide suggests
  roughly 1,000 changed/new lines as a rule of thumb, not a hard acceptance limit.
  Split large changes into coherent pieces that can each be reviewed and tested.

Abstraction is justified by actual common semantics. Do not invent a framework
for one use, duplicate library facilities, or force two substantially different
algorithms into a base class just to reduce line count. Explain a necessary
exception using concrete callers, costs, or dependency constraints.

## Preserve numerical and parallel semantics

Use `Assert` and the established exception types for debug preconditions and
internal invariants; use `AssertThrow` or the existing runtime error path when
failure must also be detected in Release. Assertions must not contain work the
algorithm needs when assertions are disabled.

Treat MPI collectives as part of control flow. Check every rank, including ranks
with no local cells or entries, reaches the required collectives on the correct
communicator. Avoid rank-dependent early exits around collective operations.
Distinguish locally owned, locally relevant, and ghost entries; preserve the
backend's read/write, compression, and ghost-update protocol. Pass the relevant
communicator instead of hard-coding `MPI_COMM_WORLD` in reusable code.

For device and threaded paths, inspect the actual backend semantics. A host loop
over device memory, an unneeded fence, or shared mutable scratch storage can
invalidate an otherwise plausible refactor. Preserve existing concurrency
guarantees and validate affected call sites. Avoid repeated allocation or copies
in assembly and matrix-free kernels; measure claimed performance improvements.

## Remove generated artifacts before review

Read the complete final diff, including tests, documentation, instantiations, and
reference output. For each changed block, be able to explain its necessity and
the evidence that it preserves or implements the contract.

Actively look for these concrete failures:

- A condition implied by an enclosing branch; nested `if constexpr` testing the
  same dimension; switches with identical branches or only a default action.
  Simplify without deleting required validation or changing unsupported cases.
- A new trait, loop, table, wrapper, allocation, or parameter that duplicates an
  existing operation. Prefer the established operation when semantics match.
- Speculative fallback paths, swallowed errors, unsupported-case success, unused
  options, or broad exception handling added to make a test pass.
- Unnecessary includes, dependencies, public members, compatibility aliases,
  casts, and copies. Every remaining one needs a concrete purpose.
- A comment that repeats syntax, describes an old implementation, refers to a
  nonexistent argument, or claims support, accuracy, or speed without evidence.
  Document the user contract and the non-obvious reason for the implementation.
- Tests that only reproduce the implementation's arithmetic, compare two paths
  sharing the same bug, or replace golden output without checking correctness.
- Repeated coefficients or defaults that can drift; generated prose, placeholder
  sections, praise, and completion claims unsupported by actual checks.

This is semantic review, not a vocabulary filter or an AI detector. Valid
mathematical explanations and useful defensive checks should remain. If a part
cannot be explained, investigate or remove it before claiming review readiness.

## Validate and hand off honestly

Choose checks for the changed behavior and relevant configurations. For a
regression, establish that the test detects the old bug when feasible. Use an
independent expected result: an analytical case, invariant, trusted native
routine, or justified reference. Record when baseline replay is unavailable.

Use the repository's formatter and testing workflow. Recheck the final revision
after fixes. Distinguish successful compilation, actual execution, output
comparison, and current-head CI. Report skipped configurations and blockers;
never describe unexecuted GPU, MPI, dependency-version, or module paths as tested.

Write a concise PR description explaining the trigger, resulting behavior,
relevant validation, and any limitations. Preserve the target's required
template. Update API documentation, tutorial explanations, instantiations,
module exports, and release notes when the change requires them.

deal.II's checked contribution policy requires a human submitting author who has
read and understood the entire patch and accepts responsibility under the DCO;
it rejects autonomous-agent contributions. Prepare code and a PR draft for that
human. Do not certify human review, add a human sign-off, or submit an upstream
contribution as an autonomous agent. Recheck the current policy before submission.
Follow the target's current AI disclosure instructions; do not invent a mandatory
transcript requirement. Publishing a separate artifact repository does not
certify a future upstream contribution.

When responding to review, address the underlying issue across equivalent changed
sites, update related documentation and tests, and rerun affected checks. Explain
a disagreement with evidence. Do not merge, enable auto-merge, or mark a human
acceptance gate on the strength of an agent's self-review.
