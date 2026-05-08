from src import NetworkPlan


def test_network_plan_ready_when_required_fields_are_valid():
    plan = NetworkPlan(
        name="Hilltop community mesh",
        region="Central",
        estimated_users=120,
        has_privacy_review=True,
    )

    assert plan.is_ready_for_review()


def test_network_plan_requires_privacy_review():
    plan = NetworkPlan(
        name="Hilltop community mesh",
        region="Central",
        estimated_users=120,
        has_privacy_review=False,
    )

    assert not plan.is_ready_for_review()
