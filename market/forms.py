from django import forms

from .models import Buy
from .models import Sell
from .models import Timeprice
from .models import Timecheck
from .models import Buyback
from .models import Threshhold
from .models import WavesClient

class WavesClientForm(forms.ModelForm):
    class Meta:
        model = WavesClient
        fields = {'privateKey'}
        labels = {
            'privateKey':'privateKey'
        }

class BuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = {'amountBTC','amountBTCtoken','percentBTC',
                'amountETH','amountETHtoken','percentETH',
                'amountWAVES','amountWAVEStoken','percentWAVES'}
        labels = {
            'amountBTC':'Объем BTC',
            'amountBTCtoken':'Объем в токенах за BTC',
            'percentBTC':'Процент BTC',
            'amountETH':'Объем ETH',
            'amountETHtoken':'Объем в токенах за ETH',
            'percentETH':'Процент ETH',
            'amountWAVES':'Объем WAVES',
            'amountWAVEStoken':'Объем в токенах за WAVES',
            'percentWAVES':'Процент WAVES'
        }


class SellForm(forms.ModelForm):
    class Meta:
        model = Sell
        fields = {'SamountBTC','SamountBTCtoken','SpercentBTC',
                'SamountETH','SamountETHtoken','SpercentETH',
                'SamountWAVES','SamountWAVEStoken','SpercentWAVES'}
        labels = {
            'SamountBTC':'Объем BTC',
            'SamountBTCtoken':'Объем в токенах за BTC',
            'SpercentBTC':'Процент BTC',
            'SamountETH':'Объем ETH',
            'SamountETHtoken':'Объем в токенах за ETH',
            'SpercentETH':'Процент ETH',
            'SamountWAVES':'Объем WAVES',
            'SamountWAVEStoken':'Объем в токенах за WAVES',
            'SpercentWAVES':'Процент Waves'
        }

class StatusForm(forms.Form):
    choiceType = (
        ('on', 'Включить'),
        ('off', 'Отключить'),
        )
    status = forms.MultipleChoiceField(label='Режим работы', choices=choiceType, widget=forms.RadioSelect)

class TimepriceForm(forms.ModelForm):
    class Meta:
        model = Timeprice
        fields = {'timeprice'}
        labels = {
            'timeprice' : 'Проверять цены каждые:'
        }

class TimecheckForm(forms.ModelForm):
    class Meta:
        model = Timecheck
        fields = {'timecheck'}
        labels = {
            'timecheck' : 'Проверять объем каждые:'
        }

class BuybackForm(forms.ModelForm):
    class Meta:
        model = Buyback
        fields = {'timebuyback', 'bbamountBTC', 'bbamountETH','bbamountWAVES'}
        labels = {
        'timebuyback': 'Выкупить через:',
        'bbamountBTC': 'для BTC:',
        'bbamountETH': 'для ETH:',
        'bbamountWAVES': 'для WAVES:',
        }

class ThreshholdForm(forms.ModelForm):
    class Meta:
        model = Threshhold
        fields = {'threshhold'}
        labels = {
            'threshhold': 'Порог изменения цены:'
        }
