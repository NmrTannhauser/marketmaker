# Generated by Django 2.0.4 on 2018-05-08 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0010_buyback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Threshhold',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshhold', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
            ],
        ),
    ]