#!/usr/bin/env python3
import os
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc as candlestick
from matplotlib import style
import re
import pandas as pd
import numpy as np

#import historical price data
dat  = pd.DataFrame(pd.read_csv('price_data.csv'))
#rename columns
dat.columns = ['Date','Open','High','Low',
                'Close','Volume','MarketCap']
#reverse dataFrame order for all cols along index axis
data = dat.iloc[::-1]

#fetch current price
def getPrice():
    global btcPrice
    #bitstamp = 'https://bitstamp.net/api/ticker/'
    cmc = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
    try:
        req = requests.get(cmc)
        price = float(json.loads(req.text)[0]['price_usd'])
        btcPrice = "%.2f" % price
    #if unable to connect, use latest data from spreadsheet
    except requests.ConnectionError:
        btcPrice = data.iloc[-1]['Close']

def main():
    #prompt user for number of candles to display
    print('\n\nYou have ' + str(len(data)-51) +
        ' candles available to view.\nEnter "0" to view all.\n')
    while True:
        toShow = raw_input('How many candles to display? ')
        if toShow == "0":
            toShow = int(len(data)-51)
            print("\tGenerating plot now...")
            break
        elif not re.match('^[0-9]+$',toShow):
            print("\tPositive integers only please and thank you.\n")
        elif int(toShow) < 52 and int(toShow) > 0:
            print("\tCannot display less than 52 candles.\n")
        elif int(toShow) > int(len(data)-51):
            print("\tCannot display more than " + 
                str(len(data)-51) + " candles.\n")
        else:
            toShow = int(toShow)
            print("\tGenerating plot now...")
            break

    #most recent price from data
    last = data.iloc[-1]['Close']

    #fetch current price
    getPrice()

#make arrays of open, high, low, close, date, and volume
    o=[data.iloc[j]['Open'] for j in range(0, len(data))]
    h=[data.iloc[j]['High'] for j in range(0, len(data))]
    l=[data.iloc[j]['Low'] for j in range(0, len(data))]
    c=[data.iloc[j]['Close'] for j in range(0, len(data))]
    t=[data.iloc[j]['Date'] for j in range(0, len(data))]
    v=[data.iloc[j]['Volume'] for j in range(0, len(data))]

#scale down volume array values so they will
#fit nicely on a graph without too much fuss.
    vol=[]
    for i in range(0,len(data)):
        vol.append(float(v[i]) / (9**7))
        vol[i] = float(round(vol[i],3))

#replace the last close price with current price
    c[-1] = float(btcPrice)

#Below various arrays are generated for TD indicator values.
#They will (and must) be the same length as any data column
#(e.g., open, low, volume, etc.).

#In order for the long/short count to progress beyond 0,
#It must be preceeded by a bullish/bearish price flip.
#In the absence of such a flip, the count, if 0,
#remains at 0 regardless of other conditions.
#If count > 0, a price flip is not required for the count to progress.
    shortVal=[]
    longVal =[]
    shortCount = 0
    longCount = 0
    for k in range(0,len(c)): #generate TD buy/sell setups
        if k <= 3:
            longCount = 0
            shortCount = 0
        if shortCount > 8:
            shortCount = 0
        if longCount > 8:
            longCount = 0
        if k > 3:
            if c[k] < c[k-4]:
                longCount+=1
            else:
                longCount = 0
            if c[k] > c[k-4]:
                shortCount+=1
            else:
                shortCount = 0
        longVal.append(longCount)
        shortVal.append(shortCount)

    buyVal =[]
    sellVal=[]
    buyCount=0
    sellCount=0
    for y in range(0,len(c)): #generate TD buy countdown
        if y < 11:
            buyCount = 0
        if y>= 11:
            if buyCount == 0:
                if h[y] >= l[y-3] or h[y] >= l[y-4] or h[y] >= l[y-5] or h[y] >= l[y-6] or h[y] >= l[y-7]:
                    if 8 in longVal[y-16:y] or 9 in longVal[y-15:y]:
                        if c[y] < l[y-2]:
                            buyCount += 1
            if buyVal[-1] == 13 or shortVal[y] > 8:
                buyCount = 0
            if buyCount != 0:
                if c[y] < l[y-2]:
                    buyCount += 1
                if longVal[y] == 9:
                    buyCount = 0
        buyVal.append(buyCount)

    for y in range(0,len(c)): #generate TD sell countdown
        if y < 11:
            sellCount = 0
        if y>= 11:
            if sellCount == 0:
                if l[y] <= h[y-3] or l[y] <= h[y-4] or l[y] <= h[y-5] or l[y] <= h[y-6] or l[y] <= h[y-7]:
                    if 8 in shortVal[y-16:y] or 9 in shortVal[y-15:y]:
                        if c[y] > h[y-2]:
                            sellCount = 1
            if sellVal[-1] == 13 or longVal[y] > 8:
                sellCount = 0
            if sellCount != 0:
                if c[y] > h[y-2]:
                    sellCount += 1
                if shortVal[y] == 9:
                    sellCount = 0
        sellVal.append(sellCount)

    agbuyVal =[]
    agsellVal=[]
    agbuyCount=0
    agsellCount=0
    for y in range(0,len(c)): #generate aggressive TD buy countdown
        if y < 11:
            agbuyCount = 0
        if y>= 11:
            if agbuyCount == 0:
                if h[y] >= l[y-3] or h[y] >= l[y-4] or h[y] >= l[y-5] or h[y] >= l[y-6] or h[y] >= l[y-7]:
                    if 8 in longVal[y-16:y] or 9 in longVal[y-15:y]:
                        if l[y] < l[y-2]:
                            agbuyCount += 1
            if agbuyVal[-1] == 13 or shortVal[y] > 8:
                agbuyCount = 0
            if agbuyCount != 0:
                if l[y] < l[y-2]:
                    agbuyCount += 1
                if longVal[y] == 9:
                    agbuyCount = 0
        agbuyVal.append(agbuyCount)

    for y in range(0,len(c)): #generate aggressive TD sell countdown
        if y < 11:
            agsellCount = 0
        if y>= 11:
            if agsellCount == 0:
                if l[y] <= h[y-3] or l[y] <= h[y-4] or l[y] <= h[y-5] or l[y] <= h[y-6] or l[y] <= h[y-7]:
                    if 8 in shortVal[y-16:y] or 9 in shortVal[y-15:y]:
                        if h[y] > h[y-2]:
                             agsellCount = 1
            if agsellVal[-1] == 13 or longVal[y] > 8:
                agsellCount = 0
            if agsellCount != 0:
                if h[y] > h[y-2]:
                    agsellCount += 1
                if shortVal[y] == 9:
                    agsellCount = 0
        agsellVal.append(agsellCount)

    #read in the output of script "other_indicators.py"
    try:
        os.system("./other_indicators.py") #Linux
    except:
        os.system("python other_indicators.py") #Windows
    #the csv files below are generated by the script 'other_indicators.py'
    mas  = pd.read_csv("mas.csv")
    emas = pd.read_csv("emas.csv")

    #get Moving Average values
    tenDay       =[mas.iloc[i]["ten"] for i in range(0,len(mas))]
    twelveDay    =[mas.iloc[i]["twelve"] for i in range(0,len(mas))]
    twentysixDay =[mas.iloc[i]["twentysix"] for i in range(0,len(mas))]
    thirtyDay    =[mas.iloc[i]["thirty"] for i in range(0,len(mas))]
    fiftyDay     =[mas.iloc[i]["fifty"] for i in range(0,len(mas))]
    sixtyDay     =[mas.iloc[i]["sixty"] for i in range(0,len(mas))]
    onetwentyDay =[mas.iloc[i]["onetwenty"] for i in range(0,len(mas))]

    #get Exponential Moving Average values
    tenEMA       =[emas.iloc[i]["ten"] for i in range(0,len(mas))]
    twelveEMA    =[emas.iloc[i]["twelve"] for i in range(0,len(mas))]
    twentysixEMA =[emas.iloc[i]["twentysix"] for i in range(0,len(mas))]
    thirtyEMA    =[emas.iloc[i]["thirty"] for i in range(0,len(mas))]
    fiftyEMA     =[emas.iloc[i]["fifty"] for i in range(0,len(mas))]
    sixtyEMA     =[emas.iloc[i]["sixty"] for i in range(0,len(mas))]
    onetwentyEMA =[emas.iloc[i]["onetwenty"] for i in range(0,len(mas))]

    #get macd + macd histo values
    #scale values up to make them more easily visible in plot
    macd = [emas.iloc[i]["macdHisto"] * 2.5 for i in range(0,len(emas))]

    twentyeightDayVol=[emas.iloc[i]["twentyeightDayVol"] for i in range(0,len(emas))]

    #truncate data sets based on user input for number of candles
    d = len(c) - toShow
    if d > 1:
        del o[:d]
        del h[:d]
        del l[:d]
        del c[:d]
        del t[:d]
        del vol[:d]
        del longVal[:d]
        del shortVal[:d]
        del buyVal[:d]
        del agbuyVal[:d]
        del sellVal[:d]
        del agsellVal[:d]
        del tenDay[:d]
        del twelveDay[:d]
        del twentysixDay[:d]
        del thirtyDay[:d]
        del fiftyDay[:d]
        del sixtyDay[:d]
        del onetwentyDay[:d]
        del tenEMA[:d]
        del twelveEMA[:d]
        del twentysixEMA[:d]
        del thirtyEMA[:d]
        del fiftyEMA[:d]
        del sixtyEMA[:d]
        del onetwentyEMA[:d]
        del macd[:d]
        del twentyeightDayVol[:d]

    idx_min = int(np.argmin(l)) #find local low
    idx_max = int(np.argmax(h)) #find local high

    #create open,high,low,close array to be used in candlestick below
    x=0
    ohlc=[]
    while x < len(l):
        append_it = x, o[x], h[x], l[x], c[x]
        ohlc.append(append_it)
        x+=1

    #begin plot code...
    style.use('fivethirtyeight')
    fig = plt.figure()

    ax1 = plt.subplot2grid((1,1), (0,0)) #((dimensions), (define origin))

    #display only every 3rd x-axis label
    ax1.xaxis.set_ticks(np.arange(0,len(o),3.0))
    a = ax1.get_xticks().tolist()
    for p in range(0, len(a)):
        a[p] = t[p * 3]
    ax1.set_xticklabels(a)

    #rotate x-axis labels to make them fit on screen
    ticks = ax1.get_xticklabels()
    for label in ticks:
        label.set_rotation(60) #units here are degrees
        label.set_fontsize(8)

    #plot title, axes labels, axes scales
    plt.title("BTC/USD, Daily")
    plt.xlim(-0.55, len(o) + 0.01)
    plt.ylim(-1200, h[idx_max] * 1.14)

    #show a grid on plot
    ax1.grid(True,color='#2E2E2E',linestyle='--')

    #generate candlesticks
    lines, patches = candlestick(ax1,ohlc,width=0.6,colorup='g',colordown='r')
    for line, patch in zip(lines, patches):
        line.set_color('#848484')
        line.set_linewidth(1.1)
        patch.set_edgecolor('#1C1C1C')
        patch.set_linewidth(0)
        patch.set_antialiased(False)
        patch.set_zorder(3) #put candles behind TD indicator values

    #display td countdown values
    for z in range(0,len(c)):
        if int(sellVal[z]) > 10 and int(sellVal[z]) != int(sellVal[z-1]):
            ax1.annotate(str(sellVal[z]), xy = (z-0.48, h[z]*1.01),
            xytext = (z-0.48, h[z]*1.01), size=11,
            color='#FE642E', weight='bold')
        if int(buyVal[z]) > 10 and int(buyVal[z]) != int(buyVal[z-1]):
            ax1.annotate(str(buyVal[z]), xy = (z-0.4, l[z]/1.005),
            xytext = (z-0.4, l[z]/1.005), size=11,
            color='#A9F5A9', weight='bold')
        #insert arrows when countdown completes
        if sellVal[z] == 13:
            plt.arrow(z, h[z]*1.07, 0.0, -150, fc="#FE642E",#light red
            ec="#FE642E", head_width=0.8, head_length=150)
        if buyVal[z] == 13:
            plt.arrow(z, l[z]/1.07, 0.0, 150, fc="#A9F5A9",#light green
            ec="#A9F5A9", head_width=0.8, head_length=150)

    #display td aggressive countdown values
    for z in range(0,len(c)):
        if int(agsellVal[z]) > 10 and int(agsellVal[z]) != int(agsellVal[z-1]):
            ax1.annotate(str(agsellVal[z]), xy = (z-0.45, l[z]/1.01),
            xytext = (z-0.45, l[z]/1.02), size=12,
            color='#DF0101', weight='bold')
        if int(agbuyVal[z]) > 10 and int(agbuyVal[z]) != int(agbuyVal[z-1]):
            ax1.annotate(str(agbuyVal[z]), xy = (z-0.4, l[z]*1.0089),
            xytext = (z-0.4, h[z]*1.02), size=12,
            color='#01DF01', weight='bold')
        #insert arrows when countdown completes
        if agsellVal[z] == 13:
            plt.arrow(z, l[z]/1.07, 0.0, -100, fc="red",
            ec="red", head_width=0.8, head_length=150)
        if agbuyVal[z] == 13:
            plt.arrow(z, h[z]*1.07, 0.0, 100, fc="green",
            ec="green", head_width=0.8, head_length=150)

    #display td setup values
    for r in range(0,len(c)):
        if int(shortVal[r]) > 0:
            ax1.annotate(str(shortVal[r]), xy = (r, h[r]/1.0004),
            xytext = (r-0.13, h[r]/1.0004), color='#FA5858',
            size=10,weight='bold')
        if int(longVal[r]) > 0:
            ax1.annotate(str(longVal[r]), xy = (r, l[r]*1.0004),
            xytext = (r-0.13, l[r]*1.0004), color='#2EFE64',
            size=10,weight='bold')
        #insert arrows when setup completes
        if shortVal[r] == 9:
             plt.arrow(r, h[r]*1.04, 0.0, -100, fc="#FA5858",
             ec="#FA5858", head_width=0.8, head_length=150)
        if longVal[r] == 9:
           plt.arrow(r, l[r]/1.08, 0.0, 100, fc="#58FA58",
           ec="#58FA58", head_width=0.8, head_length=150)

    #display the latest price next to final candle
    if btcPrice < last:
        ax1.annotate(btcPrice, xy = (x, float(btcPrice)),
        xytext= (x-0.1, float(btcPrice)), color='#FE2E2E',
        size=10, weight='bold')
    elif btcPrice >= last:
        ax1.annotate(btcPrice, xy = (x, float(btcPrice)),
        xytext= (x-0.1, float(btcPrice)), color='#088A29',
        size=10, weight='bold')

    #display the highest and lowest prices for the time interval specified
    #ax1.annotate("L: $" + str(l[idx_min]), xy = (0, h[idx_max]*0.9),
    #    xytext= (0, h[idx_max]*0.9), color='#FE2E2E', size=10, weight='bold')
    #ax1.annotate("H: $" + str(h[idx_max]), xy = (0, h[idx_max]*0.98),
    #    xytext= (0, h[idx_max]*0.98), color='#2EFE2E', size=10, weight='bold')


    r = np.arange(len(macd))
    
    """
    COMMENT/UNCOMMENT ANNOTATE-PLOT PAIRS BELOW TO ADD/REMOVE 
    MOVING AVERAGES AND EXPONENTIAL MOVING AVERAGES
    """
    ax1.annotate("10 day EMA", xy = (r[-1]/1.1, h[idx_max]*1.02),
        xytext= (r[-1]/1.1, h[idx_max]*1.02),
        color='purple', size=10, weight='bold')
    ax1.plot(r,tenEMA, color="purple", linewidth="1.5")

    ax1.annotate("30 day EMA", xy = (r[-1]/1.1, h[idx_max]*0.98),
        xytext= (r[-1]/1.1, h[idx_max]*0.98),
        color='blue', size=10, weight='bold')
    ax1.plot(r,thirtyEMA, color="blue", linewidth="1.5")

    #ax1.annotate("50 day EMA", xy = (r[-1]/1.1, h[idx_max]*0.94),
    #    xytext= (r[-1]/1.1, h[idx_max]*0.94),
    #    color='green', size=10, weight='bold')
    #ax1.plot(r,fiftyEMA, color="green", linewidth="1.5")

    #ax1.annotate("10 day MA", xy = (r[-1]/1.1, h[idx_max]*0.90),
    #    xytext= (r[-1]/1.1, h[idx_max]*0.90),
    #    color='red', size=10, weight='bold')
    #ax1.plot(r,tenDay, color="red",linewidth="1.5")

    #ax1.annotate("30 day MA", xy = (r[-1]/1.1, h[idx_max]*0.86),
    #    xytext= (r[-1]/1.1, h[idx_max]*0.96),
    #    color='orange', size=10, weight='bold')
    #ax1.plot(r,thirtyDay, color="orange",linewidth="1.5")
    
    #ax1.annotate("50 day MA", xy = (r[-1]/1.1, h[idx_max]*0.82),
    #    xytext= (r[-1]/1.1, h[idx_max]*0.82),
    #    color='yellow', size=10, weight='bold')
    #ax1.plot(r,fiftyDay, color="yellow",linewidth="1.5")

    """
    COMMENT/UNCOMMENT NEXT 2 LINES TO TOGGLE VOLUME INDICATOR ON/OFF
    """
    plt.plot(r,twentyeightDayVol, color="r", linewidth="1.5")
    ax1.bar(r, vol, color="white")
    
    """
    COMMENT/UNCOMMENT TO TOGGLE MACD INDICATOR ON/OFF
    """
    ax1.bar(r, macd, color="blue")
    
    ax1.set_facecolor('#000000')

    #adjust plot size to fit screen
    plt.subplots_adjust(left=0.06,right=0.94,bottom=0.15,
                        top=0.94,wspace=0.20,hspace=0.20)

    #make chart full screen by default
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    plt.show()

main()
