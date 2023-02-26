# Generated by Django 4.0.3 on 2022-06-01 21:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0031_alter_pointofinterest_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyCategoryAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.amenity')),
            ],
        ),
        migrations.AddField(
            model_name='propertycategory',
            name='amenities',
            field=models.ManyToManyField(blank=True, related_name='property_categories', through='properties.PropertyCategoryAmenity', to='properties.amenity'),
        ),
        migrations.AddField(
            model_name='propertycategoryamenity',
            name='property_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.propertycategory'),
        ),
    ]
