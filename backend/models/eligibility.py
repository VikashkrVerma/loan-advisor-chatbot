from .products import get_all_products

def check_eligibility(product, profile):
    """
    Returns (is_eligible, reason)
    """
    amount = profile.get("amount")
    tenure = profile.get("tenure")
    if amount < product["min_amount"] or amount > product["max_amount"]:
        return False, f"Amount must be between {product['min_amount']} and {product['max_amount']}"
    if tenure < product["min_tenure"] or tenure > product["max_tenure"]:
        return False, f"Tenure must be between {product['min_tenure']} and {product['max_tenure']} months"

    if product["purpose"] != "any" and profile.get("purpose") != product["purpose"]:
        return False, f"This product is for {product['purpose']} purpose only"

    elig = product.get("eligibility", {})
    if "min_salary" in elig and profile.get("monthly_income", 0) < elig["min_salary"]:
        return False, f"Minimum salary required is {elig['min_salary']}"
    if "max_emi_ratio" in elig:
        income = profile.get("monthly_income", 0)
        existing_emi = profile.get("existing_emi", 0)
        if income == 0 or (existing_emi / income) > elig["max_emi_ratio"]:
            return False, f"Existing EMI exceeds {elig['max_emi_ratio']*100}% of income"
    if "employment_type" in elig and profile.get("employment_type") != elig["employment_type"]:
        return False, f"Employment type must be {elig['employment_type']}"
    if "min_business_income" in elig and profile.get("business_income", 0) < elig["min_business_income"]:
        return False, f"Business income must be at least {elig['min_business_income']}"
    
    return True, "Eligible"