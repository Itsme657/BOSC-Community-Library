"""Core helpers for BOSC Community Library examples."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NetworkPlan:
    """Minimal planning metadata for a community wireless deployment."""

    name: str
    region: str
    estimated_users: int
    has_privacy_review: bool

    def is_ready_for_review(self) -> bool:
        return (
            bool(self.name.strip())
            and bool(self.region.strip())
            and self.estimated_users > 0
            and self.has_privacy_review
        )
