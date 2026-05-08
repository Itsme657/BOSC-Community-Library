from src import NetworkPlan


plan = NetworkPlan(
    name="Community library wireless access",
    region="Central",
    estimated_users=75,
    has_privacy_review=True,
)

print(plan.is_ready_for_review())
