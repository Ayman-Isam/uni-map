# Generated by Django 4.2.2 on 2023-12-08 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_marker_contact_marker_logo_alter_marker_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marker',
            name='website',
            field=models.CharField(max_length=100),
        ),
    ]
