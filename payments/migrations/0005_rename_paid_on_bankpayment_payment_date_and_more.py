# Generated by Django 4.0.3 on 2022-06-11 10:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_rename_scheme_name_supportedcardscheme_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bankpayment',
            old_name='paid_on',
            new_name='payment_date',
        ),
        migrations.RemoveField(
            model_name='bankpayment',
            name='bank_city',
        ),
        migrations.RemoveField(
            model_name='bankpayment',
            name='bank_country',
        ),
        migrations.RemoveField(
            model_name='bankpayment',
            name='bank_region',
        ),
        migrations.AddField(
            model_name='bankpayment',
            name='bank_full_address',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bankpayment',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
