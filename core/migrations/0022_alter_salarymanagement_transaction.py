# Generated by Django 5.0.4 on 2024-05-12 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_remove_salarymanagement_withdrawal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salarymanagement',
            name='transaction',
            field=models.JSONField(blank=True),
        ),
    ]
