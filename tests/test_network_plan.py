from src import NetworkPlan


def test_network_plan_ready_when_required_fields_are_valid():
    plan = NetworkPlan(
        name="Hilltop community mesh",
        region="Central",
        estimated_users=120,
        has_privacy_review=True,
    )

    assert plan.is_ready_for_review()
    assert plan.validation_errors() == []


def test_network_plan_reports_review_blockers():
    plan = NetworkPlan(
        name=" ",
        region=" ",
        estimated_users=0,
        has_privacy_review=False,
    )

    assert not plan.is_ready_for_review()
    assert plan.validation_errors() == [
        "network plan name is required",
        "deployment region is required",
        "estimated users must be greater than zero",
        "privacy review must be completed before review",
    ]
