# Validation and PR preparation

## Select checks from the actual change

| Change | Evidence to seek |
| --- | --- |
| Numerical bug | Small reproducer, independently justified expected result, old/fixed comparison when feasible |
| Refactor | Preserved behavior and supported cases; tests exercising changed branches |
| Public API | Representative existing and new callers, overload/default compatibility, instantiation and link checks |
| Distributed behavior | Correct collectives and communicator, empty-rank case, relevant MPI sizes, backend ghost protocol |
| GPU/threaded kernel | Compilation/execution on the relevant backend when available; memory-space and synchronization checks |
| Optimization | Correctness plus a representative baseline/candidate measurement; avoid machine-independent speed claims |
| Optional dependency or modules | Enabled/disabled and affected versions/exports; report unavailable matrix entries |
| Documentation only | Accurate source/API references and applicable formatting/rendering checks |

Choose relevant combinations; this is not a demand to rebuild the entire matrix
for every patch. Do not add a redundant test when an existing regression already
catches the failure. Conversely, a default serial run cannot validate an MPI
failure or a device-specific kernel.

## deal.II testsuite details

Read the checkout's `doc/developers/testsuite.html` and an adjacent test. Existing
tests normally pair a source file with `.output` or an explicitly chosen
`.run_only` variant. Follow category, license-header, `deallog`, and initialization
conventions. Put a short comment at the top stating the behavior checked.

Feature requirements, MPI ranks, threads, expected failures, and Debug/Release
variants can be encoded in the output filename. Copy a *relevant* neighboring
example and check the current grammar; do not invent a suffix. After adding a
test, refresh the category configuration as needed and verify discovery with
`ctest -N -R '<test expression>'` in the actual tests build. Then run the focused
tests, using the build's existing resource limits and MPI launch configuration.
Use the project's own workflow in downstream applications.

Record the testsuite stages separately:

- **BUILD:** the intended test variant compiled and linked.
- **RUN:** the executable actually exercised the changed path and completed with
  the expected status.
- **DIFF:** its output agreed with a justified reference under the configured
  comparison rules, when output comparison is part of that test.

An empty test selection is not a pass. A run-only test intentionally has no
reference-output comparison; do not claim a DIFF result for it. Test program
assertions alone may disappear in Release. Ensure numerical checks or reference
output still exercise the intended contract in the configurations claimed.

For a new reference output, compute the expectation independently, explain
tolerances and important edge cases, and inspect the generated differences.
Do not regenerate output just to turn a failure green. Print useful error
quantities when validating approximations; include inputs at limits when those
are part of the contract. Unchanged golden files during a refactor are helpful
evidence, not a proof that all behavior is preserved.

## Formatting, CI, and description

For the library, inspect and use `contrib/utilities/indent` or the corresponding
build target. Its `REPORT_ONLY=true` mode reports without rewriting source files.
Verify the branch base and preserve unrelated edits before using a mutating
formatter. Inspect the final diff, license headers, direct includes, `.inst.in`,
module exports, Doxygen changes, and applicable `doc/news/changes/{minor,major}`
entries. A downstream project may use a different release-note system.

Recheck CI against the actual head SHA. `ready to test`, `/rebuild`, an older
green revision, or a skipped/cancelled/pending job is not a passing result. Re-read
the current workflow before using labels; local campaign labels are not universal
library requirements. Keep human acceptance and merge decisions with humans.

A short description usually needs only:

> A concrete input or call previously caused [observed failure]. The change
> [explains the resulting behavior and the essential design choice].
>
> Validation: [actual configurations and checks]. [Relevant limitation, if any].

Replace the brackets with evidence; remove unused sections. Preserve required
license/DCO/template text from the target repository. Do not claim that an agent
has performed the submitting human's personal review or legal certification.
The checked deal.II policy requires that review before submission. AI disclosure
is governed by the current policy/template; a historical discussion of disclosure
does not make every proposed field mandatory.

Review feedback is input to reasoning. Verify proposed code against the language
standard, runtime contract, and final discussion before applying it. Address
equivalent instances within the patch and update dependent documentation/tests.
Explain valid exceptions; do not turn a review response into unrelated cleanup.
