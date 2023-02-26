# Generated by Django 4.0.3 on 2022-06-15 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0007_listingparameter_listing_parameter_unique_constraint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listingparameter',
            name='value',
        ),
        migrations.AlterField(
            model_name='listingparameter',
            name='name',
            field=models.CharField(choices=[('NEW_AGENT_PROMOTION', 'New Agent Promotion'), ('HOLIDAY_PROMOTION', 'Holiday Promotion')], default='NEW_AGENT_PROMOTION', max_length=100, verbose_name='listing parameter name'),
        ),
    ]
