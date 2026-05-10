"""Core helpers for BOSC Community Library examples."""

from dataclasses import dataclass
from typing import Final


MINIMUM_REVIEW_USERS: Final = 1


@dataclass(frozen=True)
class NetworkPlan:
    """Minimal planning metadata for a community wireless deployment."""

    name: str
    region: str
    estimated_users: int
    has_privacy_review: bool

    def validation_errors(self) -> list[str]:
        """Return review blockers for incomplete or unsafe planning metadata."""

        errors: list[str] = []

        if not self.name.strip():
            errors.append("network plan name is required")

        if not self.region.strip():
            errors.append("deployment region is required")

        if self.estimated_users < MINIMUM_REVIEW_USERS:
            errors.append("estimated users must be greater than zero")

        if not self.has_privacy_review:
            errors.append("privacy review must be completed before review")

        return errors

    def is_ready_for_review(self) -> bool:
        return not self.validation_errors()
