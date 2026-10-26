# PrettyTable inline HTML text validation

Source: [9a675a1b20e4008b3202e121eb2aff6c362a7bb9](https://github.com/prettytable/prettytable/compare/5fec60c0fd85530e5299d8c6e39dc030bfd7ce9f...jipeng6036-del:fix/html-inline-cell-text), tree `3ca97240b8fd227c60964fa78e7d5790a179ebe2`.

The change preserves text inside inline HTML tags until the enclosing cell closes. The same HTML fixture produces empty header/cell text on the baseline and complete `Name`, `Alice Example`, and `Engineer` text on the candidate.

- Windows CPython 3.11, 3.12, 3.13, 3.14: official tox test environments, 354 tests each.
- Linux CPython 3.14.9: official tox tests (354), mypy and full lint environment pass. The submodule hook has no matching files; no hooks were disabled.
- 17 new regression cases: baseline 12 fail / 5 controls pass; candidate 17 pass.
- Full checks used identical tracked source bytes to the committed tree, verified for all 45 blobs and file modes. The normal commit also ran the installed prek Git hook.
- Final commit rebuilt sdist/wheel as `3.18.1.dev18`; Twine checks both, and a new independent wheel installation verifies installed source blobs and actual HTML → text/CSV disk output → CSV reload.

`source-binding.json` records the source IDs and exact local coverage. `file-candidate-final` and `file-baseline` contain the actual input/output files and reload results. macOS, PyPy, Python 3.15/3.16 and free-threaded interpreters were not run locally; no upstream CI result is implied. Local machine paths in logs were replaced with placeholders. This branch contains only allowlisted PrettyTable evidence.
