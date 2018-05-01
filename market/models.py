from django.db import models

class Buy(models.Model):
    coin = models.CharField(max_length=10)
    amount = models.FloatField()
    price = models.FloatField()
    percent = models.FloatField()
    def __str__(self):
        return self.coin
class Sell(models.Model):
    coin = models.CharField(max_length=10)
    amount = models.FloatField()
    price = models.FloatField()
    percent = models.FloatField()
    def __str__(self):
        return self.coin
