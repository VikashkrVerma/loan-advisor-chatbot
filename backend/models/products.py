PRODUCTS = [
    {
        "id": "personal_loan",
        "name": "Personal Loan",
        "min_amount": 50000,
        "max_amount": 5000000,
        "min_tenure": 12,
        "max_tenure": 60,
        "interest_rate": 12.0,
        "purpose": "any",
        "eligibility": {"min_salary": 30000, "max_emi_ratio": 0.4}
    },
    {
        "id": "salary_advance",
        "name": "Salary Advance",
        "min_amount": 10000,
        "max_amount": 500000,
        "min_tenure": 1,
        "max_tenure": 6,
        "interest_rate": 8.0,
        "purpose": "any",
        "eligibility": {"employment_type": "salaried", "max_tenure": 6}
    },
    {
        "id": "bnpl",
        "name": "BNPL",
        "min_amount": 1000,
        "max_amount": 100000,
        "min_tenure": 1,
        "max_tenure": 3,
        "interest_rate": 0.0,
        "purpose": "any",
        "eligibility": {}
    },
    {
        "id": "sme_loan",
        "name": "SME Loan",
        "min_amount": 100000,
        "max_amount": 10000000,
        "min_tenure": 12,
        "max_tenure": 120,
        "interest_rate": 15.0,
        "purpose": "business",
        "eligibility": {"min_business_income": 500000}
    },
    {
        "id": "topup_loan",
        "name": "Top-up Loan",
        "min_amount": 20000,
        "max_amount": 1000000,
        "min_tenure": 6,
        "max_tenure": 24,
        "interest_rate": 14.0,
        "purpose": "any",
        "eligibility": {"existing_loan_good": True}
    },
    {
        "id": "secured_loan",
        "name": "Secured Loan",
        "min_amount": 200000,
        "max_amount": 20000000,
        "min_tenure": 24,
        "max_tenure": 180,
        "interest_rate": 9.5,
        "purpose": "any",
        "eligibility": {"collateral": True}
    }
]

def get_all_products():
    return PRODUCTS

def get_product_by_id(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None