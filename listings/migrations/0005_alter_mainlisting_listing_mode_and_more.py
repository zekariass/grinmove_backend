# Generated by Django 4.0.3 on 2022-06-16 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_rename_method_payment_payment_method'),
        ('listings', '0004_alter_mainlisting_listing_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainlisting',
            name='listing_mode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings_in_this_mode', to='listings.listingmode'),
        ),
        migrations.AlterField(
            model_name='mainlisting',
            name='listing_state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings_in_this_state', to='listings.listingstate'),
        ),
        migrations.AlterField(
            model_name='mainlisting',
            name='listing_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings_in_this_type', to='listings.listingtype'),
        ),
        migrations.AlterField(
            model_name='mainlisting',
            name='payment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listing', to='payments.payment'),
        ),
    ]
