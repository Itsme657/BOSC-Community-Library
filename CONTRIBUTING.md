# Contributing to BOSC Community Library

Thank you for contributing. This guide explains how to prepare changes that are technically useful, reviewable, and aligned with the repository's open source standards.

## Development Workflow

1. Fork the repository and create a feature branch from `main`.
2. Keep commits small and focused.
3. Update documentation when behavior, architecture, or contributor workflows change.
4. Add tests for source changes or examples that introduce new behavior.
5. Open a pull request using `.github/PULL_REQUEST_TEMPLATE.md`.

## Local Setup

```powershell
git clone https://github.com/bos-com/BOSC-Community-Library.git
cd BOSC-Community-Library
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

If a tool is not yet available in the project, document the command you expected to run and the reason it is blocked.

## Technical Standards

- Prefer simple, documented designs over clever abstractions.
- Use structured configuration or data formats where possible.
- Treat wireless communication examples as safety-sensitive: avoid leaking secrets, keys, personal identifiers, exact private locations, or unreviewed security claims.
- Validate inputs at boundaries and document assumptions.
- Keep examples reproducible without specialized hardware unless the requirement is clearly stated.

## Commit Guidelines

Use clear commit messages:

```text
area: concise description
```

Examples:

```text
docs: add community review checklist
tests: cover channel planning validation
```

## Pull Request Review

Maintainers review for:

- Correctness and reproducibility.
- Security, privacy, and legal risk.
- Accessibility and clarity of documentation.
- Test coverage appropriate to the change.
- Consistency with existing repository patterns.

## Security and Responsible Disclosure

Do not publish exploit details, active credentials, private network identifiers, or sensitive infrastructure information in public issues. Open a private report with maintainers when possible and include enough detail to reproduce the concern safely.

## Legal and Licensing

By contributing, you agree that your contribution may be distributed under the Apache License 2.0. Only submit work you created or have permission to contribute. Cite external sources and licenses in documentation when used.

## Community Health

Follow `CODE_OF_CONDUCT.md`. Assume good intent, ask clarifying questions, and make review feedback specific enough for contributors to act on.
