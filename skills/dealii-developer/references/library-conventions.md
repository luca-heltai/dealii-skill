# Library conventions and design contracts

These apply to deal.II library code. A downstream project's own conventions govern
its implementation. Inspect the version in the working checkout before applying
any historical detail below.

## Authoritative sources

The research snapshot uses upstream commit
`9e5d24772d9f2a115e4822b94a4fcaaf8a8a309d` (20 October 2026):

- [Contributing](https://github.com/dealii/dealii/blob/9e5d24772d9f2a115e4822b94a4fcaaf8a8a309d/CONTRIBUTING.md)
- [Coding conventions](https://github.com/dealii/dealii/blob/9e5d24772d9f2a115e4822b94a4fcaaf8a8a309d/doc/doxygen/headers/coding_conventions.h)
- [Testsuite](https://github.com/dealii/dealii/blob/9e5d24772d9f2a115e4822b94a4fcaaf8a8a309d/doc/developers/testsuite.html)
- [Writing documentation](https://github.com/dealii/dealii/blob/9e5d24772d9f2a115e4822b94a4fcaaf8a8a309d/doc/developers/writing-documentation.html)
- [Changed-file formatter](https://github.com/dealii/dealii/blob/9e5d24772d9f2a115e4822b94a4fcaaf8a8a309d/contrib/utilities/indent)
- [Formatter version checks](https://github.com/dealii/dealii/blob/9e5d24772d9f2a115e4822b94a4fcaaf8a8a309d/contrib/utilities/indent_common.sh)
- [PR template](https://github.com/dealii/dealii/blob/9e5d24772d9f2a115e4822b94a4fcaaf8a8a309d/.github/pull_request_template.md)

## Style decisions that change code

Use CamelCase for classes and the established namespace/type spelling; use
`lower_case_with_underscores` for functions and variables. Iterator aliases and
standard-library compatibility implementations have deliberate exceptions.
Do not mechanically rename an established public interface.

Use descriptive names; short names are appropriate for simple counting indices.
Counts normally start with `n_`, setters with `set_`, flag clearing with `clear_`.
Use `&&`, `||`, and `!`, and prefer `using` aliases over `typedef`.

Make unchanged inputs and non-mutating member functions `const`. Pass expensive
objects by reference when ownership/copying is not required. Small value types
can be passed and returned by value. Initialize local variables near their use;
reuse allocating scratch objects outside hot loops where appropriate.

Inputs normally precede outputs; trailing defaulted inputs are an established
exception. Name a function for what it actually does, including state updates.
Keep passive configuration together as neighboring `AdditionalData` types do;
an active solver controller serves a different purpose.

Keep implementation helpers outside the public API, using the surrounding
`internal` namespace organization. Follow the neighboring class layout, exception
declarations, constructor initialization lists, namespace macros, and include
structure. The checked coding-conventions document uses constructor initializer
lists for ordinary member defaults; the surrounding current code matters when
adapting an existing class. Do not create competing defaults in both places.

Use unsigned types for quantities constrained to be nonnegative, but retain the
correct semantic width: global DoF indices are not necessarily `unsigned int`.
Use `types::global_dof_index`, container size/difference types, and the owning
API's types where appropriate. Do not silence a narrowing warning with a cast
without establishing the range.

Use topology facilities instead of hand-written numbers. `GeometryInfo<dim>`
describes hypercubes; `ReferenceCell` handles the actual reference-cell type in
mixed/simplex contexts. Use available cell/face/vertex index ranges instead of
assuming `2*dim` or a particular vertex ordering.

Let the repository formatter handle spacing. The snapshot's tooling requires
clang-format 16.0 and also checks licenses and author information; do not freeze
that version for future checkouts. The documented implementation style includes
three blank lines between functions. Formatting cannot detect redundant control
flow or establish semantic equivalence.

## Defensive programming without accidental Release changes

Check preconditions, meaningful postconditions, and internal invariants using
the established assertion macros and exceptions. Prefer specialized checks such
as `AssertDimension` and `AssertIndexRange` where they describe the invariant.
Use runtime error handling when invalid input or I/O failure must be detected in
optimized builds too. Do not catch and ignore an error to simulate support.

No required computation or mutation may depend on a debug-only assertion being
evaluated. Evaluate needed work first; assert about its result separately.
The correct unsupported/unreachable path depends on the function's contract and
existing implementation. Do not impose one default-switch macro everywhere.

## Template definitions, instantiation, and optional features

The official conventions distinguish three cases:

| Supported template arguments | Usual location |
| --- | --- |
| All combinations enumerable and explicitly instantiated | Definition in `.cc`; declarations in the header |
| Common combinations prebuilt; users may instantiate others | `.templates.h`, included by `.cc` for common instantiations |
| Open-ended arguments requiring visible definitions | Definitions in the public header, following local Doxygen guards |

Inspect `.inst.in`, the generated instantiations, configuration guards, and
module partitions affected by a new signature or public type. Follow the existing
supported language standard and `std_cxx*` wrappers; a suggestion in a review can
still require a feature unavailable in the supported compiler matrix.

Include what an implementation uses and respect forward-declaration conventions
for public return types. Avoid accidental transitive-include dependencies and
IDE-added includes. Include MPI through the established deal.II wrapper where
appropriate. Distinguish an optional dependency's executable, library/API, and
version-dependent capability.

## Documentation is part of the interface

Document public declarations where users encounter them. Specify the operation,
parameter meaning, supported cases, ownership/lifetime, mutation, and relevant
collectivity or thread-safety constraints. Avoid copying irrelevant details from
another overload or retaining comments about deleted code. Explain non-obvious
implementation choices near the implementation.

For tutorials, explain the PDE, discretization, assumptions, solver choice, and
interpretation of results at the reader's level. A mathematical mistake cannot
be fixed by polishing the prose. Keep physical claims tied to the actual model.
Use Doxygen links and existing documentation conventions; verify generated
documentation when markup, formulas, or extraction behavior changes.
