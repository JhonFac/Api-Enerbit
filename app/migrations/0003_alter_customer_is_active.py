# Generated by Django 4.0.4 on 2023-11-04 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_customer_is_active_alter_workorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]