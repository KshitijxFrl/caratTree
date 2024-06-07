from celery import shared_task
import csv
from .models import User


@shared_task
def cc_score(aadhar_id):
    user = User.objects.get(aadhar_id=aadhar_id)
    total_balance = 0
    # please make sure path is correct
    with open('.\transactions_data_backend.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user'] == str(aadhar_id):
                if row['transaction_type'] == 'CREDIT':
                    total_balance += int(row['amount'])
                else:
                    total_balance -= int(row['amount'])
    
    if total_balance >= 1000000:
        credit_score = 900
    elif total_balance <= 10000:
        credit_score = 300
    else:
        credit_score = 300 + ((total_balance - 10000) // 15000) * 10
    
    user.credit_score = credit_score
    user.save()

