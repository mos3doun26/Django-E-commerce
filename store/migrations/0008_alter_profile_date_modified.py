# Generated by Django 5.1.2 on 2024-11-04 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_profile_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
