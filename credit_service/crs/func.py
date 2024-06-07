from decimal import Decimal

def cal_due(principal_balance, apr, days_in_billing_cycle=30):
    daily_apr = round(apr / Decimal('365'), 3)
    apr_accrued = daily_apr * principal_balance * days_in_billing_cycle
    min_due = (principal_balance * Decimal('0.03')) + apr_accrued
    return min_due, apr_accrued
