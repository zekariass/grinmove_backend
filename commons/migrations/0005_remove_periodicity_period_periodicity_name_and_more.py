# Generated by Django 4.0.3 on 2022-07-02 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0004_remove_address_latitute_address_latitude'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='periodicity',
        #     name='period',
        # ),
        # migrations.AddField(
        #     model_name='periodicity',
        #     name='name',
        #     field=models.CharField(default=None, max_length=30, unique=True, verbose_name='period label or name'),
        #     preserve_default=False,
        # ),
        migrations.AlterField(
            model_name='periodicity',
            name='num_of_days',
            field=models.IntegerField(blank=True, null=True, verbose_name='number of days in this period'),
        ),
    ]
