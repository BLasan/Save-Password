# Generated by Django 3.0.6 on 2020-05-21 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_view', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='salt',
            field=models.BinaryField(),
        ),
    ]
