# BOSC Community Library

BOSC Community Library is an open source knowledge and tooling repository for community-centered wireless communication systems. It helps contributors document reusable patterns, review secure communication practices, and share examples that can grow into production-ready community infrastructure.

## Project Goals

- Provide transparent documentation for community wireless system design.
- Encourage secure, scalable, and maintainable technical contributions.
- Offer examples and tests that make contributor work easy to review.
- Maintain a healthy open source process with clear expectations.

## Repository Structure

```text
.github/       Issue and pull request templates
docs/          Architecture notes, governance, and technical guides
examples/      Small usage examples and reference scenarios
src/           Library source files
tests/         Automated checks and test fixtures
```

## Maintainer Standard

This repository is curated as a professional open source environment. Changes should be small, traceable, reviewed, and aligned with `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `GOVERNANCE.md`.

## Basic Usage

Use `NetworkPlan` to capture early deployment metadata and surface review blockers before a proposal is ready for maintainers.

```python
from src import NetworkPlan

plan = NetworkPlan(
    name="Community library wireless access",
    region="Central",
    estimated_users=75,
    has_privacy_review=True,
)

if plan.is_ready_for_review():
    print("Plan is ready for maintainer review.")
else:
    print(plan.validation_errors())
```

## Localized Resource Support

This library now includes `Resource` and `ResourceIndex` to store searchable community resources in multiple locales.

```python
from src import Resource, ResourceIndex

index = ResourceIndex()
index.add_resource(
    Resource(
        resource_id="sec-check",
        title="Security Checklist",
        url="https://example.com/security",
        category="Tools",
        tags=("security", "checklist"),
        locale="en",
        description="Guide for reviewing security controls.",
        translations={
            "es": {
                "title": "Lista de verificación de seguridad",
                "description": "Guía para revisar los controles de seguridad.",
            }
        },
    )
)

results = index.search(query="seguridad", locale="es")
print([resource.resource_id for resource in results])
```

## Performance Improvements

The `ResourceIndex` now prefilters by category and tag indexes to reduce search cost for larger collections.

## License

This project is licensed under the Apache License 2.0. See `LICENSE` for details.
