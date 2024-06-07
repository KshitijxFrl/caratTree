from django.db import models
import json
import uuid

# Create your models here.

# user/customer model
class User(models.Model):
    aadhar_id = models.UUIDField(primary_key=True)  
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    annual_income = models.IntegerField()
    credit_score = models.IntegerField(null=True, blank=True)
    
    

# loan model
class Loan(models.Model):
    LOAN_TYPE_CHOICES = [
        ('Credit Card', 'Credit Card'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPE_CHOICES, default = "Credit Card")
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period = models.IntegerField()
    disbursement_date = models.DateField()
    loan_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_closed = models.BooleanField(default=False)
    emi_schedule = models.TextField(default='[]')

    

# Payment model
class Payment(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_processed = models.BooleanField(default=False)




# billing corn job
class BillingDetail(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    billing_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    principal_balance = models.DecimalField(max_digits=10, decimal_places=2)
    apr_accrued = models.DecimalField(max_digits=10, decimal_places=2)
    min_due = models.DecimalField(max_digits=10, decimal_places=2)

class DuePayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)    