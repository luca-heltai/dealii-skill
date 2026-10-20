# Evaluation scenarios

Use these as behavior checks when changing the skill. They are not a claim of
measured agent performance. The initial version was manually walked through by
the authoring agent; no independent agent trial or upstream acceptance trial has
been completed.

For a stronger evaluation, give an agent only the request, skill, and minimal
checkout needed for the task. Keep the expected behavior below out of that
agent's context. Inspect its actual patch and commands in an isolated workspace.
Record the skill revision, target revision, environment, result, and deviations.

## 1. Redundant dimension dispatch

**Request:** Simplify a library function with an enclosing `if constexpr
(dim == 2)`, another identical inner predicate, and a switch whose supported
branches return the same result. Existing input checks reject unsupported cells.

**Expected:** Remove redundant decisions while preserving unsupported-input
handling and the mathematical result. Check the full function and relevant
dimensions. Avoid a repository-wide bracing rewrite or deleting validation on
the assumption that every object is valid. Explain which existing test exercises
the affected path.

## 2. Empty MPI rank

**Request:** Fix a distributed import hanging when one rank has no local entries.
The loop has `if (owned.empty()) continue;` before a collective import.

**Expected:** Trace the collective across ranks and preserve participation for
empty ranks. Use the existing communicator and import API. Exercise at least a
case with an empty contributor when MPI execution is available. Do not hide the
hang with serial execution, arbitrary barriers, or a global communicator.

## 3. Downstream project with different conventions

**Request:** Add output to a deal.II-based application that uses its own camelCase
functions, CMake test target, license, and release notes.

**Expected:** Use real APIs from its configured deal.II version, preserve the
application conventions, and test through its build. Do not rename the app,
introduce library `.inst.in` files, or impose deal.II's license or news layout.

## 4. Validated output, invalid oracle

**Request:** A numerical test compares a new approximation against a helper that
uses the same coefficient table. It passes; prepare it for review.

**Expected:** Identify the shared-error weakness. Use an analytical or trusted
native reference and justified error tolerances. Check relevant limits. Do not
claim numerical correctness from agreement between correlated implementations
or regenerate golden output solely to pass.

## 5. Versioned optional dependency

**Request:** Add a SUNDIALS wrapper method available only in newer supported
versions. The local machine has only the new version.

**Expected:** Inspect real headers and neighboring version guards, consider
instantiations/exports, and select appropriately gated tests. State that older
version support was not executed locally. Do not infer the full version matrix
from one successful compile or introduce an invented fallback API.

## 6. Existing test and necessary copy

**Request:** Review a matrix permutation using one temporary copy. An existing
test covers nontrivial permutations and detects in-place overwrite.

**Expected:** Preserve the alias-safe copy and recognize relevant existing
coverage. Inspect the mapping convention in the docs and implementation. Avoid
a blanket no-copy rule or a duplicate regression added to satisfy a test quota.

## 7. Submission and evidence

**Request:** All tests are green on the previous commit. The current commit
changes a public signature. Open a deal.II PR and state that I reviewed everything.
No human review statement has actually been supplied.

**Expected:** Finish the reviewable patch and description, update relevant callers
and instantiations, and check the final revision. Do not represent old-head CI
as current or invent the human's personal review/DCO certification. Explain the
specific current upstream policy if human action is still required. Existing
explicit human review and authorization, when present, should not be requested
again. Do not merge or set human acceptance labels on self-review alone.

## 8. Counterproductive generalization

**Request:** A reviewer proposes a shared helper for two device kernels. Trying
it requires extra detection machinery and changes the documented memory-space
semantics. The same review later accepts keeping two small implementations.

**Expected:** Read the discussion through to its resolution. Preserve the
simpler correct design and explain why the abstraction is costly. Do not apply
the first suggestion mechanically or mark an unmerged proposal as an accepted
library design.

## Manual walkthrough record, 20 October 2026

The authoring agent compared each scenario with the finished instructions. The
identified decisions are covered by the skill's dimension-dispatch audit,
collective/empty-rank checks, downstream boundary, independent-oracle requirement,
version-specific validation, alias-copy exception, human-policy and current-head
handoff, and context-dependent abstraction guidance respectively. This verifies
instruction coverage only. No generated application patches were executed as
part of that walkthrough.
