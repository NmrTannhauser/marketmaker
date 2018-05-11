from django.db import models
from django.contrib.auth.models import User

class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amountBTC = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    amountBTCtoken = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    percentBTC = models.DecimalField(default=0, max_digits = 4, decimal_places = 2)
    amountETH = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    amountETHtoken = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    percentETH = models.DecimalField(default=0, max_digits = 4, decimal_places = 2)
    amountWAVES = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    amountWAVEStoken = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    percentWAVES = models.DecimalField(default=0, max_digits = 4, decimal_places = 2)
    status = models.BooleanField(default=False)
    def __str__(self):
        return 'bb'

class Sell(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    SamountBTC = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    SamountBTCtoken = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    SpercentBTC = models.DecimalField(default=0, max_digits = 4, decimal_places = 2)
    SamountETH = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    SamountETHtoken = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    SpercentETH = models.DecimalField(default=0, max_digits = 4, decimal_places = 2)
    SamountWAVES = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    SamountWAVEStoken = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    SpercentWAVES = models.DecimalField(default=0, max_digits = 4, decimal_places = 2)
    status = models.BooleanField(default=False)
    def __str__(self):
        return 'ss'

class Timeprice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeprice = models.DecimalField(default = 60, max_digits = 6, decimal_places = 0)

    def __str__(self):
        return 'pr'

class Timecheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timecheck = models.DecimalField(default = 60, max_digits = 6, decimal_places = 0)

    def __str__(self):
        return 'ch'

class Buyback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timebuyback = models.DecimalField(default = 60, max_digits = 6, decimal_places = 0)
    bbamountBTC = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    bbamountETH = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    bbamountWAVES = models.DecimalField(default=0, max_digits = 16, decimal_places = 8)
    statusbb = models.BooleanField(default=False)
    def __str__(self):
        return 'bk'

class Threshhold(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    threshhold = models.DecimalField(default=0, max_digits = 4, decimal_places = 2)
    def __str__(self):
        return 'th'
