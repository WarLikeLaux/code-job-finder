SALARY_LOWER_BOUND_MULTIPLIER = 0.8
SALARY_UPPER_BOUND_MULTIPLIER = 1.2
RUBLE_CURRENCY_CODES = ("RUR", "RUB")


def predict_rub_salary(currency, salary_from, salary_to):
    if currency.upper() not in RUBLE_CURRENCY_CODES:
        return None
    if not salary_from:
        return salary_to * SALARY_LOWER_BOUND_MULTIPLIER
    if not salary_to:
        return salary_from * SALARY_UPPER_BOUND_MULTIPLIER
    return (salary_to + salary_from) / 2
