# Generated by Django 3.0.6 on 2020-05-21 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_view', '0002_auto_20200521_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.BinaryField(max_length=100),
        ),
    ]
