from ..models.products import get_all_products
from ..models.eligibility import check_eligibility
from .calculator import calculate_loan_details

def recommend_products(profile):
    products = get_all_products()
    eligible_list = []
    for product in products:
        is_eligible, reason = check_eligibility(product, profile)
        if is_eligible:
            details = calculate_loan_details(
                profile["amount"],
                product["interest_rate"],
                profile["tenure"]
            )
            eligible_list.append({
                "product": product,
                "details": details,
                "reason": reason
            })

    scored = []
    for item in eligible_list:
        product = item["product"]
        details = item["details"]
        score = 0
        income = profile.get("monthly_income", 0)
        if income > 0 and details["emi"] <= 0.4 * income:
            score += 10
        score += max(0, 20 - details["total_interest"] / 10000)
        if product["purpose"] == profile.get("purpose", "any") or product["purpose"] == "any":
            score += 5
        if product["min_tenure"] <= profile["tenure"] <= product["max_tenure"]:
            score += 5
        scored.append({
            "product": product,
            "details": details,
            "score": score,
            "reason": item["reason"]
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:3]  # top 3