# Generated by Django 4.1.3 on 2024-06-06 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("crs", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Loan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("loan_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("interest_rate", models.DecimalField(decimal_places=2, max_digits=5)),
                ("term_period", models.IntegerField()),
                ("disbursement_date", models.DateField()),
                (
                    "principal_balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "interest_accrued",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("is_closed", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="crs.user"
                    ),
                ),
            ],
        ),
    ]
