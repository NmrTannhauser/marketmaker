# Generated by Django 2.0.4 on 2018-05-07 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_auto_20180507_2239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sell',
            old_name='amountBTC',
            new_name='SamountBTC',
        ),
        migrations.RenameField(
            model_name='sell',
            old_name='amountETH',
            new_name='SamountETH',
        ),
        migrations.RenameField(
            model_name='sell',
            old_name='amountWAVES',
            new_name='SamountWAVES',
        ),
        migrations.RenameField(
            model_name='sell',
            old_name='percentBTC',
            new_name='SpercentBTC',
        ),
        migrations.RenameField(
            model_name='sell',
            old_name='percentETH',
            new_name='SpercentETH',
        ),
        migrations.RenameField(
            model_name='sell',
            old_name='percentWAVES',
            new_name='SpercentWAVES',
        ),
        migrations.RenameField(
            model_name='sell',
            old_name='priceBTC',
            new_name='SpriceBTC',
        ),
        migrations.RenameField(
            model_name='sell',
            old_name='priceETH',
            new_name='SpriceETH',
        ),
        migrations.RenameField(
            model_name='sell',
            old_name='priceWAVES',
            new_name='SpriceWAVES',
        ),
    ]
