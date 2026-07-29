def calculate_emi(principal, annual_rate, tenure_months):
    if annual_rate == 0:
        return principal / tenure_months
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return principal / tenure_months
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    return round(emi, 2)

def calculate_loan_details(principal, annual_rate, tenure_months):
    emi = calculate_emi(principal, annual_rate, tenure_months)
    total_payment = round(emi * tenure_months, 2)
    total_interest = round(total_payment - principal, 2)
    return {
        "emi": emi,
        "total_payment": total_payment,
        "total_interest": total_interest
    }