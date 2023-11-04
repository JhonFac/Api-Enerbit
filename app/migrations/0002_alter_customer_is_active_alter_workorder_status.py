# Generated by Django 4.0.4 on 2023-11-04 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Done', 'Done'), ('Cancelled', 'Cancelled')], default='New', max_length=20),
        ),
    ]