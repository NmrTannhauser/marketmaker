from django.contrib import admin
from .models import Buy
from .models import Sell
from .models import Timeprice
from .models import Timecheck
from .models import Buyback
from .models import Threshhold

admin.site.register(Buy)
admin.site.register(Sell)
admin.site.register(Timeprice)
admin.site.register(Timecheck)
admin.site.register(Buyback)
admin.site.register(Threshhold)
