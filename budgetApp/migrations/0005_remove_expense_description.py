# Generated by Django 4.1.7 on 2023-04-15 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgetApp', '0004_alter_expense_description_alter_expense_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='description',
        ),
    ]
