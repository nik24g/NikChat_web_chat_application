# Generated by Django 3.2.4 on 2021-07-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aroom', '0003_auto_20210716_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date',
            field=models.DateField(),
        ),
    ]
