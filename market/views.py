from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
import threading
import time
from time import sleep
from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from market.forms import ThreshholdForm
from market.forms import BuybackForm, TimecheckForm, TimepriceForm, BuyForm, SellForm, StatusForm, WavesClientForm
from market.models import Buy, Sell, Timeprice, Timecheck, Buyback, Threshhold, WavesClient
from django.http import JsonResponse

def getPrivateKey():
    a = WavesClient.objects.all()[0]
    return a.privateKey

def setOffline():
    buy = Buy.objects.all()[0]
    buy.status = False
    buy.save()
    return

@login_required
def waves(request):
    if request.method != 'POST':
        try:
            wv = WavesClient.objects.filter(user=request.user)[0]
            wavesform = WavesClientForm(instance = wv)
        except IndexError:
            wavesform = WavesClientForm()
    else:
        try:
            wf = WavesClient.objects.filter(user=request.user)[0]
            wf.privateKey = request.POST['privateKey']
            wf.save()
        except IndexError:    
            wavesform = WavesClientForm(request.POST)
            if wavesform.is_valid():
                wv = wavesform.save(commit = False)
                wv.user = request.user
                wv.save()
    context = {'wavesform': wavesform}
    return render(request, 'html/waves.html', context)


def getJson(request):
    buy = Buy.objects.all()[0]
    sell = Sell.objects.all()[0]
    timePrice = Timeprice.objects.all()[0]
    timeCheck = Timecheck.objects.all()[0]
    buyBack = Buyback.objects.all()[0]
    threshHold = Threshhold.objects.all()[0]
    returnator = {
        'status': float(buy.status),
        'Buy': {
            'amountBTC': float(buy.amountBTC),
            'amountBTCtoken': float(buy.amountBTCtoken),
            'percentBTC': float(buy.percentBTC),
            'amountETH': float(buy.amountETH),
            'amountETHtoken': float(buy.amountETHtoken),
            'percentETH': float(buy.percentETH),
            'amountWAVES': float(buy.amountWAVES),
            'amountWAVEStoken': float(buy.amountWAVEStoken),
            'percentWAVES': float(buy.percentWAVES),
            },
        'Sell': {
            'amountBTC': float(sell.SamountBTC),
            'amountBTCtoken': float(sell.SamountBTCtoken),
            'percentBTC': float(sell.SpercentBTC),
            'amountETH': float(sell.SamountETH),
            'amountETHtoken': float(sell.SamountETHtoken),
            'percentETH': float(sell.SpercentETH),
            'amountWAVES': float(sell.SamountWAVES),
            'amountWAVEStoken': float(sell.SamountWAVEStoken),
            'percentWAVES': float(sell.SpercentWAVES),
            },
        'TimeCheck': int(timeCheck.timecheck),
        'TimePrice': int(timePrice.timeprice),
        'ThreshHold': int(threshHold.threshhold),
        'BuyBack': {
            'BTC':float(buyBack.bbamountBTC),
            'ETH':float(buyBack.bbamountETH),
            'WAVES':float(buyBack.bbamountWAVES),
            'Time':int(buyBack.timebuyback),
            'Status':float(buyBack.statusbb)
            }
        }
    context = {'rr': JsonResponse(returnator)}
    # return render(request, 'html/json.html',context)
    return JsonResponse(returnator)

@login_required
def reviewIndex(request):
    if request.method != 'POST':
        try:
            buyer = Buy.objects.filter(user=request.user)[0]
            status =  buyer.status
            buyForm = BuyForm(instance = buyer)
            sellForm = SellForm(instance = Sell.objects.filter(user=request.user)[0])
        except IndexError:
            status = False
            buyForm = BuyForm()
            sellForm = SellForm()
        try:
            statusForm = StatusForm()
            statusForm.fields['status'].initial = ['on' if status else 'off']
        except IndexError:
            statusForm = StatusForm()
        try:
            timepriceForm = TimepriceForm(instance = Timeprice.objects.filter(user=request.user)[0])
        except IndexError:
            timepriceForm = TimepriceForm()
        try:
            timecheckForm = TimecheckForm(instance = Timecheck.objects.filter(user=request.user)[0])
        except IndexError:
            timecheckForm = TimecheckForm()
        try:
            buybackForm = BuybackForm(instance = Buyback.objects.filter(user=request.user)[0])
        except IndexError:
            buybackForm = BuybackForm()
        try:
            threshholdform = ThreshholdForm(instance = Threshhold.objects.filter(user=request.user)[0])
        except IndexError:
            threshholdform = ThreshholdForm()
    else:
        # если POST
        if request.POST['submit'] == 'pricetime':
            try:
                pt = Timeprice.objects.filter(user=request.user)[0]
                pt.timeprice = request.POST['timeprice']
                pt.save()
            except IndexError:
                priceTimeForm = TimepriceForm(request.POST)
                if priceTimeForm.is_valid():
                    pt = priceTimeForm.save(commit = False)
                    pt.user = request.user
                    pt.save()
        elif request.POST['submit'] == 'timecheck':
            try:
                tc = Timecheck.objects.filter(user=request.user)[0]
                tc.timecheck = request.POST['timecheck']
                tc.save()
            except IndexError:
                timeCheckForm = TimecheckForm(request.POST)
                if timeCheckForm.is_valid():
                    tc = timeCheckForm.save(commit = False)
                    tc.user = request.user
                    tc.save()
        elif request.POST['submit'] == 'buyback':
            try:
                bk = Buyback.objects.filter(user=request.user)[0]
                bk.timebuyback = request.POST['timebuyback']
                bk.bbamountBTC = request.POST['bbamountBTC']
                bk.bbamountETH = request.POST['bbamountETH']
                bk.bbamountWAVES = request.POST['bbamountWAVES']
                bk.statusbb = True
                bk.save()
            except IndexError:
                buybackForm = BuybackForm(request.POST)
                buybackForm.statusbb = True
                if buybackForm.is_valid():
                    bk = buybackForm.save(commit = False)
                    bk.user = request.user
                    bk.save()
        elif request.POST['submit'] == 'threshhold':
            try:
                th = Threshhold.objects.filter(user=request.user)[0]
                th.threshhold = request.POST['threshhold']
                th.save()
            except IndexError:
                threshholdform = ThreshholdForm(request.POST)
                if threshholdform.is_valid():
                    th = threshholdform.save(commit = False)
                    th.user = request.user
                    th.save()
        elif request.POST['submit'] == 'clear':
            try:
                Buy.objects.all()[0].delete()
                Sell.objects.all()[0].delete()
                buyForm = BuyForm()
                sellForm = SellForm()
                statusForm = StatusForm(request.POST)
                bb = buyForm.save(commit = False)
                ss = sellForm.save(commit = False)
                bb.user = request.user
                ss.user = request.user
                bb.status = True if request.POST['status'] == 'on' else False
                ss.status = True if request.POST['status'] == 'on' else False
                bb.save()
                ss.save()
            except IndexError:{}
            buyForm = BuyForm()
            sellForm = SellForm()
            status = True if request.POST['status'] == 'on' else False
        elif request.POST['submit'] == 'cancelbuyback':
            try:
                bk = Buyback.objects.filter(user=request.user)[0]
                bk.statusbb = False
                bk.save()
            except IndexError:
                buybackForm = BuybackForm(request.POST)
                buybackForm.staus = False
                if buybackForm.is_valid():
                    bk = buybackForm.save(commit = False)
                    bk.user = request.user
                    bk.save()
        else:
            try:
                buyer = Buy.objects.all()[0]
                buyer.amountBTC = request.POST['amountBTC']
                buyer.amountBTCtoken = request.POST['amountBTCtoken']
                buyer.percentBTC = request.POST['percentBTC']
                buyer.amountETH = request.POST['amountETH']
                buyer.amountETHtoken = request.POST['amountETHtoken']
                buyer.percentETH = request.POST['percentETH']
                buyer.amountWAVES = request.POST['amountWAVES']
                buyer.amountWAVEStoken = request.POST['amountWAVEStoken']
                buyer.percentWAVES = request.POST['percentWAVES']
                buyer.status = True if request.POST['status'] == 'on' else False
                status = buyer.status
                buyer.save()
                seller = Sell.objects.all()[0]
                seller.SamountBTC = request.POST['SamountBTC']
                seller.SamountBTCtoken = request.POST['SamountBTCtoken']
                seller.SpercentBTC = request.POST['SpercentBTC']
                seller.SamountETH = request.POST['SamountETH']
                seller.SamountETHtoken = request.POST['SamountETHtoken']
                seller.SpercentETH = request.POST['SpercentETH']
                seller.SamountWAVES = request.POST['SamountWAVES']
                seller.SamountWAVEStoken = request.POST['SamountWAVEStoken']
                seller.SpercentWAVES = request.POST['SpercentWAVES']
                seller.status = True if request.POST['status'] == 'on' else False
                seller.save()

            except IndexError:
                buyForm = BuyForm(request.POST)
                sellForm = SellForm(request.POST)
                statusForm = StatusForm()
                if buyForm.is_valid() and sellForm.is_valid():
                    bb = buyForm.save(commit = False)
                    ss = sellForm.save(commit=False)
                    bb.user = request.user
                    ss.user = request.user
                    bb.status = True if request.POST['status'] == 'on' else False
                    ss.status = True if request.POST['status'] == 'on' else False
                    status = bb.status
                    bb.save()
                    ss.save()
        return HttpResponseRedirect(reverse('robot:index'))
    try:
        price = prices()
        priceBTC =price[0][0].replace(',','.')
        priceETH =price[0][9].replace(',','.')
        priceWAVES =price[0][12].replace(',','.')
    except Exception as e:
        priceBTC = 0
        priceETH = 0
        priceWAVES = 0
    context = {'threshholdform':threshholdform,'buybackForm':buybackForm, 'timecheckForm': timecheckForm, 'timepriceForm': timepriceForm, 'buyForm': buyForm, 'status': status,'statusForm': statusForm,'sellForm': sellForm,'BTC': priceBTC, 'ETH': priceETH, 'WAVES': priceWAVES}
    return render(request, 'html/reviewIndex.html', context)

def prices():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    store = file.Storage('/home/projects/market/credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/home/projects/market/client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    # Call the Sheets API
    SPREADSHEET_ID = '15RUQce2liQe5ojMzgynm8ghs3E7fwwkf5gm3mMyGV_8'
    RANGE_NAME = 'Portfolio!C6:Q6'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values

#authentification

def login(request):
    return render(request, 'html/login.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('robot:profile'))


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid() and formAccount.is_valid():
            newUser = form.save()
            authenticatedUser = authenticate(username=newUser.username, password=request.POST['password1'])
            auth_login(request, authenticatedUser)
            return HttpResponseRedirect(reverse('robot:index'))
    context = {'form': form}
    return render(request, 'html/register.html', context)
