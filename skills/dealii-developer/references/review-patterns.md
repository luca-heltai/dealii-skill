# What reviews actually ask for

These are paraphrased observations from public reviews, not additional official
policy. Follow the whole discussion and final design. A reviewer can revise a
suggestion, and merged code can still contain a bug. The research methodology and
coverage are in the repository's `research/REPORT.md`.

## Patterns to resolve before requesting review

| Pattern challenged | Useful correction | Evidence and limit |
| --- | --- | --- |
| Unrelated additions mixed into a feature | Split independent behavior into a separate PR; keep each patch coherent | [#18948](https://github.com/dealii/dealii/pull/18948#discussion_r2449158416) separated variadic Kronecker work from matrix permutation. [#19784](https://github.com/dealii/dealii/pull/19784#discussion_r3365071603) repeated the request for an unrelated fix. Small neighboring improvements are sometimes accepted; this is a reviewability principle. |
| Generated control flow with redundant conditions, empty/default-only switches, or inconsistent branches | Simplify the decision tree and review every affected function | [#20116](https://github.com/dealii/dealii/pull/20116#discussion_r3846185329) explicitly identified a repeated dimension condition. The author then [limited the PR to a manually reviewed subset](https://github.com/dealii/dealii/pull/20116#issuecomment-5413019093). This was a merged contribution after revision, not rejection of the entire feature. |
| Function names omit state changes; options use opaque integer selectors | Express the complete action, use meaningful enum types, and separate input/output roles | [#18911](https://github.com/dealii/dealii/pull/18911#discussion_r2456951779), [norm selector](https://github.com/dealii/dealii/pull/18911#discussion_r2456964281), and [argument order](https://github.com/dealii/dealii/pull/18911#discussion_r2457042583). A longer name is useful when it removes ambiguity. |
| Extra template detection machinery beside an existing facility | Search for and reuse the established detection abstraction in its shared location | [#19149](https://github.com/dealii/dealii/pull/19149#discussion_r2679152351) requested `is_supported_operation`; [the follow-up](https://github.com/dealii/dealii/pull/19149#discussion_r2680642401) separated a missing module export. Do not emulate a missing export with a new local type system. |
| Same topology, coefficients, or algorithm repeated in multiple locations | Place shared knowledge with its existing owner and derive dependent values | [#19161](https://github.com/dealii/dealii/pull/19161#discussion_r2677015682) discusses `ReferenceCell`; [#19784](https://github.com/dealii/dealii/pull/19784#discussion_r3317539453) discusses coefficients. Distinct algorithm semantics may justify separate implementations. |
| Copies or allocation whose cost exceeds their purpose | Use const references or compute directly; retain copies required for alias safety | [#18911](https://github.com/dealii/dealii/pull/18911#discussion_r2457009114) avoids copying vectors for a norm. [#18948](https://github.com/dealii/dealii/pull/18948#discussion_r2449183738) accepts a temporary matrix that prevents input/output aliasing. Never turn this into a universal ban on copies. |
| Parallel control flow reasons only about local data | Audit collectives, communicator ownership, and ranks with empty contributions | [#19149 follow-up](https://github.com/dealii/dealii/pull/19149#discussion_r2784106464) identified a local `continue` before a collective. This comment came **after** merge and is evidence that merge is not a correctness oracle. |
| Hard-coded global communicator in reusable functionality | Accept/use the communicator associated with the caller's objects | [#18938](https://github.com/dealii/dealii/pull/18938#discussion_r2465719864). A serial/self communicator or an application-level choice can have a legitimate purpose. |
| Index conversions hide unsupported problem sizes | Preserve semantic widths and assert a justified narrow range | [#19069](https://github.com/dealii/dealii/pull/19069#discussion_r2611769519) asks for overflow checking. [#19080](https://github.com/dealii/dealii/pull/19080#discussion_r2617584470) distinguishes local sizes from global indices. A cast alone is not a fix. |
| Debug checks silently disappear for an error that must remain detectable | Use the intended runtime error path and test the affected build modes | [#19019](https://github.com/dealii/dealii/pull/19019#discussion_r2712568586) explicitly requests `AssertThrow` for invalid radii. Other internal invariants appropriately use debug assertions. |
| Test output lists plausible values without demonstrating accuracy | Compare against a trusted mathematical/native reference and print interpretable errors | [#19011 test review](https://github.com/dealii/dealii/pull/19011#discussion_r2535153906) and [the author's response](https://github.com/dealii/dealii/pull/19011#discussion_r2538902951) describe relative errors against the exponential and limit cases. [#19796](https://github.com/dealii/dealii/pull/19796#discussion_r3369252303) changes a test to use an analytical solution. |
| Tests or snippets cannot be reproduced in the project testsuite | Use the existing test layout, header, concise purpose comment, and appropriate variants | [#19019](https://github.com/dealii/dealii/pull/19019#issuecomment-3575290178) requests an in-PR regression test following its neighbor. [#19149](https://github.com/dealii/dealii/pull/19149#discussion_r2679157534) asks what the test checks. Existing coverage may make a new test unnecessary. |
| Documentation describes storage accidents, old code, or a different parameter | Describe the observable contract and explain only useful implementation choices | [#19161](https://github.com/dealii/dealii/pull/19161#discussion_r2675196473) removes obsolete history; [#18948](https://github.com/dealii/dealii/pull/18948#discussion_r2449164615) catches an unrelated argument in copied documentation. |
| Automatic includes, missing direct includes, and module-only failures | Inspect actual dependencies and the project/module wrapper conventions | [#19544](https://github.com/dealii/dealii/pull/19544#discussion_r3173468198) asks to remove unwanted includes; [its module fix](https://github.com/dealii/dealii/pull/19544#discussion_r3175307184) concerns include spelling. Avoid copying a local workaround without understanding the affected build. |
| Performance intuition presented as proof | Preserve correctness and thread behavior; measure the path being optimized | [#19647](https://github.com/dealii/dealii/pull/19647#issuecomment-4407382754) restores required thread safety after CI exposed callers. [#19944](https://github.com/dealii/dealii/pull/19944#issuecomment-4826219397) reports a performance tester result. An optimized operation can still violate its callers' contract. |
| Scientific prose improves fluency while changing the mathematics | Verify the PDE, spaces, operators, and assumptions before polishing | [#18907](https://github.com/dealii/dealii/pull/18907#discussion_r2687692986) asks for the time-dependent equations before the harmonic form. [#19828](https://github.com/dealii/dealii/pull/19828#discussion_r3446386692) corrects what the deformation tensor replaces. |
| AI-generated work is submitted without accountable human review | Prepare work for an author who understands and owns the entire patch | [#19984](https://github.com/dealii/dealii/pull/19984#issuecomment-4856584239) is an explicit autonomous-account rejection. The controlling source is the current `CONTRIBUTING.md`, not a speculative detector of AI writing. |

## Counterexamples that prevent bad rules

**Do not enforce every review suggestion mechanically.** In
[#19011](https://github.com/dealii/dealii/pull/19011#discussion_r2548470068), a
reviewer explicitly questioned the language-version availability of a proposed
variable-template deletion. The
[subsequent response](https://github.com/dealii/dealii/pull/19011#discussion_r2549124912)
reported that it did not work. Verify proposed syntax on the supported toolchain.

**Do not impose deal.II naming on a standard-library replacement.**
[#19704](https://github.com/dealii/dealii/pull/19704#discussion_r3256156671)
explicitly distinguishes reviewing a `std::inplace_vector` compatibility
implementation from checking ordinary deal.II naming. Standard conformance can
override a local aesthetic preference.

**Do not create a mandatory new regression for every edit.** In
[#18941](https://github.com/dealii/dealii/pull/18941#discussion_r2467573234), the
existing `parallel_block_vector_04` already checked the concern. Add tests for
missing behavior, not test-count targets.

**Do not infer collectivity from a name.** A concern about short-circuiting in
[#18941](https://github.com/dealii/dealii/pull/18941#discussion_r2449222066) was
[withdrawn after checking the code](https://github.com/dealii/dealii/pull/18941#discussion_r2449861273):
local inspection preceded one collective reduction. In contrast, the later
#19149 `continue` really bypassed a collective. Trace the operations.

**Do not equate reuse with maximum abstraction.**
[#20161](https://github.com/dealii/dealii/pull/20161#discussion_r3923274264)
weighs reduced duplication against extra complication and permits the latter to
decide the design. A supplementary **open, unmerged** case,
[#20217](https://github.com/dealii/dealii/pull/20217#discussion_r4317836783),
records a reviewer revising a proposed `ReferenceCell` approach after trying it.
That is evidence about review reasoning, not proof of an accepted final solution.

**Do not use one bracing suggestion as an absolute style rule.** In
[#20116](https://github.com/dealii/dealii/pull/20116#issuecomment-5417756969), the
author explains the agreed treatment after earlier suggestions. Follow the final
local style and formatter; concentrate semantic review on duplicated decisions.

**Do not call every closure a rejection.** #18880 was
[superseded by #18911](https://github.com/dealii/dealii/pull/18880#issuecomment-3433124381);
#19407 was [superseded by #19408](https://github.com/dealii/dealii/pull/19407#issuecomment-4076368661).
#19052 contains a
[backward-compatibility objection](https://github.com/dealii/dealii/pull/19052#issuecomment-3785445278)
and was [closed in favor of the option-preserving path](https://github.com/dealii/dealii/pull/19052#issuecomment-3929030847).
#18406 includes favorable technical reviews and an author withdrawal amid a
[discussion of review size and delay](https://github.com/dealii/dealii/pull/18406#issuecomment-3629521278).
These dispositions have different meanings.

**Do not require untested platform instructions or verbose installation prose.**
[#20281](https://github.com/dealii/dealii/pull/20281#discussion_r4256943415)
declines instructions the reviewer could not validate. Its
[maintenance rationale](https://github.com/dealii/dealii/pull/20281#discussion_r4256878951)
favors short, general instructions.

**Do not turn disclosure discussion into an invented policy.**
[#19916](https://github.com/dealii/dealii/pull/19916#issuecomment-4857239007)
explicitly made the disclosure section optional during review. Read the current
template and contribution policy; never require full private conversations on
the basis of a historical suggestion.
