# Generated by Django 4.0.3 on 2022-05-11 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0015_allpurposeproperty_building_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HouseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShareHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_number_of_rooms', models.IntegerField(default=1)),
                ('number_of_rooms_to_share', models.IntegerField(default=1)),
                ('total_number_of_bed_rooms', models.IntegerField(default=1)),
                ('number_of_bed_rooms_to_share', models.IntegerField(default=1)),
                ('total_number_of_baths', models.IntegerField(default=1)),
                ('number_of_baths_to_share', models.IntegerField(default=1)),
                ('floor', models.IntegerField(default=0, verbose_name='Home floor level')),
                ('area', models.FloatField(default=0.0)),
                ('is_furnished', models.BooleanField(default=False, verbose_name='is the home furnished?')),
                ('is_new', models.BooleanField(default=False, verbose_name='is the home new?')),
                ('house_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='share_houses', to='properties.housetype', verbose_name='share house type')),
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='properties.property', verbose_name='parent property')),
            ],
        ),
    ]
