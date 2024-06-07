from django.core.management.base import BaseCommand
from django.utils import timezone
from crs.models import Loan, BillingDetail, DuePayment
from crs.func import cal_due  
from datetime import timedelta


class Command(BaseCommand):
    help = 'Run the billing process for loans'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        loans = Loan.objects.filter(is_closed=False)

        for loan in loans:
            last_billing = BillingDetail.objects.filter(loan=loan).order_by('-billing_date').first()
            if last_billing:
                next_billing_date = last_billing.billing_date + timedelta(days=30)
            else:
                next_billing_date = loan.disbursement_date + timedelta(days=30)

            if next_billing_date <= today:
                principal_balance = loan.loan_amount
                apr = loan.interest_rate
                min_due, apr_accrued = cal_due(principal_balance, apr)

                billing_detail = BillingDetail.objects.create(
                    loan=loan,
                    billing_date=today,
                    due_date=today + timedelta(days=15),
                    principal_balance=principal_balance,
                    apr_accrued=apr_accrued,
                    min_due=min_due
                )

                DuePayment.objects.create(
                    loan=loan,
                    due_date=today + timedelta(days=15),
                    amount_due=min_due,
                    is_paid=False
                )

                self.stdout.write(self.style.SUCCESS(f'Generating loan bill:- {loan.loan_id}'))
            else:
                self.stdout.write(self.style.WARNING(f'No due for loan:- {loan.loan_id}'))
