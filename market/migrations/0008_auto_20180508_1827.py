# Generated by Django 2.0.4 on 2018-05-08 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_auto_20180508_0111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buy',
            name='priceBTC',
        ),
        migrations.RemoveField(
            model_name='buy',
            name='priceETH',
        ),
        migrations.RemoveField(
            model_name='buy',
            name='priceWAVES',
        ),
        migrations.RemoveField(
            model_name='sell',
            name='SpriceBTC',
        ),
        migrations.RemoveField(
            model_name='sell',
            name='SpriceETH',
        ),
        migrations.RemoveField(
            model_name='sell',
            name='SpriceWAVES',
        ),
    ]