# Contributing to PromptProof

Thanks for helping out. This is a small tool on purpose — contributions that
keep it small, dependency-free and honest are the most valuable kind.

## Reporting issues

Open an issue and include:

- what you ran (the exact command and a minimal shots JSON that triggers it),
- what you expected, and what happened instead,
- your Python version and operating system.

## Pull requests

1. Fork the repository and create a topic branch.
2. Keep the change focused: one fix or one feature per PR.
3. Add or update tests for anything you change, and make sure the whole
   suite passes:

   ```bash
   python -m unittest discover -s tests -v
   ```

4. Stay within the Python standard library for runtime code — new runtime
   dependencies will be declined to protect the zero-install promise.
5. Use Angular-style commit messages: `feat: ...`, `fix: ...`,
   `docs: ...`, `refactor: ...`, `test: ...`.

## Style

- Type hints on public functions, short docstrings that say *why*, not just
  *what*.
- User-facing text in README files exists in three languages
  (Simplified Chinese, Traditional Chinese, English) — if you change one,
  change all three, or note in the PR that a translation needs help.
