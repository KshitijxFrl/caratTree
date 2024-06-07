# Generated by Django 4.1.3 on 2024-06-06 11:44

from django.db import migrations, models
import uuid

import uuid

def generate_unique_loan_id(apps, schema_editor):
    Loan = apps.get_model('crs', 'Loan')
    for loan in Loan.objects.all():
        loan.loan_id = uuid.uuid4()
        loan.save()



class Migration(migrations.Migration):
    dependencies = [
        ("crs", "0003_remove_loan_interest_accrued_remove_loan_is_closed_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="loan",
            name="loan_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.RunPython(generate_unique_loan_id, reverse_code=migrations.RunPython.noop),
    ]
