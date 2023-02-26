# Generated by Django 4.0.3 on 2022-08-03 15:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0015_savedlisting_unique_saved_listing_per_user_constraint'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0.0, verbose_name='listing featuring price')),
                ('price_state', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], max_length=50, verbose_name='listing featuring price')),
                ('description', models.TextField(blank=True, null=True)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.RenameField(
            model_name='featuredlisting',
            old_name='feature_payment',
            new_name='payment',
        ),
        migrations.RemoveField(
            model_name='featuredlisting',
            name='expire_on',
        ),
        migrations.AlterField(
            model_name='featuredlisting',
            name='featured_listing_state',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('EXPIRED', 'Expired')], max_length=50, verbose_name='featured listing state'),
        ),
        migrations.DeleteModel(
            name='FeaturedListingState',
        ),
        migrations.AddField(
            model_name='featuredlisting',
            name='feature_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.featureprice'),
        ),
    ]
