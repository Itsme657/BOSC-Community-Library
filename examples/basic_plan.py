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
    print("Plan needs updates:")
    for error in plan.validation_errors():
        print(f"- {error}")
