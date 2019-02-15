#!/usr/bin/python
import pandas as pd
import numpy as np

#Import price data
d = pd.read_csv('price_data.csv')
#rename columns
d.columns = ['Date','Open','High','Low',
			'Close','Volume','MarketCap']

data = d.iloc[::-1]

o=[data.iloc[x]['Open'] for x in range(0, len(data))]
h=[data.iloc[x]['High'] for x in range(0, len(data))]
l=[data.iloc[x]['Low'] for x in range(0, len(data))]
c=[data.iloc[x]['Close'] for x in range(0, len(data))]
t=[data.iloc[x]['Date'] for x in range(0, len(data))]
v=[data.iloc[x]['Volume'] for x in range(0, len(data))]

#get daily volume and calculate volume moving average
vol=[]
twentyeightDayVol=[]
for i in range(0,len(data)):
	#scale volume so it will fit on plot
	vol.append(float(v[i]) / (9**7))
	vol[i] = float(round(vol[i],3))
for i in range(0,len(data)):
	if i < 27:
		twentyeightDayVol.append("0")
	else:
		twentyeightDayVol.append((np.sum(vol[i-28:i])/28))
	twentyeightDayVol[i] = round(float(twentyeightDayVol[i]),3)

#Generate Moving Average Values
nineDay=[]
tenDay=[]
twelveDay=[]
twentysixDay=[]
thirtyDay=[]
fiftyDay=[]
sixtyDay=[]
onetwentyDay=[]
for i in range(0,len(c)):
	if i < 8:
		nineDay.append("0")
	else:
		nineDay.append((np.sum(c[i-9:i])/9))
	if i < 9:
		tenDay.append("0")
	else:
		tenDay.append((np.sum(c[i-10:i])/10))
	if i < 11:
		twelveDay.append("0")
	else:
		twelveDay.append((np.sum(c[i-12:i])/12))
	if i < 25:
		twentysixDay.append("0")
	else:
		twentysixDay.append((np.sum(c[i-26:i])/26))
	if i < 29:
		thirtyDay.append("0")
	else:
		thirtyDay.append((np.sum(c[i-30:i])/30))
	if i < 49:
		fiftyDay.append("0")
	else:
		fiftyDay.append((np.sum(c[i-50:i])/50))
	if i < 59:
		sixtyDay.append("0")
	else:
		sixtyDay.append((np.sum(c[i-60:i])/60))
	if i < 119:
		onetwentyDay.append("0")
	else:
		onetwentyDay.append((np.sum(c[i-120:i])/120))

	nineDay[i] = round(float(nineDay[i]),2)
	tenDay[i] = round(float(tenDay[i]),2)
	twelveDay[i] = round(float(twelveDay[i]),2)
	twentysixDay[i] = round(float(twentysixDay[i]),2)
	thirtyDay[i] = round(float(thirtyDay[i]),2)
	fiftyDay[i] = round(float(fiftyDay[i]),2)
	sixtyDay[i] = round(float(sixtyDay[i]),2)
	onetwentyDay[i] = round(float(onetwentyDay[i]),2)

mas = []
mas.append(nineDay)
mas.append(tenDay)
mas.append(twelveDay)
mas.append(twentysixDay)
mas.append(thirtyDay)
mas.append(fiftyDay)
mas.append(sixtyDay)
mas.append(onetwentyDay)

#create dataFrame for moving averages
#and save to .csv file which will be referenced
#in main plotting code
df = pd.DataFrame(mas).T
df.to_csv("mas.csv", header=["nine","ten","twelve","twentysix",
			"thirty","fifty","sixty","onetwenty"])
dat = pd.read_csv("mas.csv")

#Generate exponential moving average values
k = float(2) / 10
S = (dat.iloc[9]["nine"] * (1 - k)) + (c[10] * k)

nineEMA=[]
for m in range(0,len(c)):
	if m < 9:
		nineEMA.append("0")
	elif m == 9:
		nineEMA.append(S)
	else:
		nineEMA.append((float(nineEMA[m - 1]) * (1 - k)) + (c[m] * k))
	nineEMA[m] = round(float(nineEMA[m]),2)

k = float(2) / 11
S = (dat.iloc[10]["ten"] * (1 - k)) + (c[11] * k)
tenEMA=[]
for m in range(0,len(c)):
	if m < 10:
		tenEMA.append("0")
	elif m == 10:
		tenEMA.append(S)
	else:
		tenEMA.append((float(tenEMA[m - 1]) * (1 - k)) + (c[m] * k))
	tenEMA[m] = round(float(tenEMA[m]),2)

k = float(2) / 13
S = (dat.iloc[12]["twelve"] * (1 - k)) + (c[13] * k)

twelveEMA=[]
for m in range(0,len(c)):
	if m < 12:
		twelveEMA.append("0")
	elif m == 12:
		twelveEMA.append(S)
	else:
		twelveEMA.append((float(twelveEMA[m - 1]) * (1 - k)) + (c[m] * k))
	twelveEMA[m] = round(float(twelveEMA[m]),2)

k = float(2) / 27
S = (dat.iloc[26]["twentysix"] * (1 - k)) + (c[27] * k)

twentysixEMA=[]
for m in range(0,len(c)):
	if m < 26:
		twentysixEMA.append("0")
	elif m == 26:
		twentysixEMA.append(S)
	else:
		twentysixEMA.append((float(twentysixEMA[m - 1]) * (1 - k)) + (c[m] * k))
	twentysixEMA[m] = round(float(twentysixEMA[m]),2)

k = float(2) / 31
S = (dat.iloc[30]["thirty"] * (1 - k)) + (c[31] * k) 

thirtyEMA=[]
for m in range(0,len(c)):
	if m < 30:
		thirtyEMA.append("0")
	elif m == 30:
		thirtyEMA.append(S)
	else:
		thirtyEMA.append((float(thirtyEMA[m - 1]) * (1 - k)) + (c[m] * k)) 
	thirtyEMA[m] = round(float(thirtyEMA[m]),2)

k = float(2) / 51
S = (dat.iloc[50]["fifty"] * (1 - k)) + (c[51] * k)

fiftyEMA=[]
for m in range(0,len(c)):
	if m < 50:
		fiftyEMA.append("0")
	elif m == 50:
		fiftyEMA.append(S)
	else:
		fiftyEMA.append((float(fiftyEMA[m - 1]) * (1 - k)) + (c[m] * k))
	fiftyEMA[m] = round(float(fiftyEMA[m]),2)

k = float(2) / 61
S = (dat.iloc[60]["sixty"] * (1 - k)) + (c[61] * k)
sixtyEMA=[]
for m in range(0,len(c)):
	if m < 60:
		sixtyEMA.append("0")
	elif m == 60:
		sixtyEMA.append(S)
	else:
		sixtyEMA.append((float(sixtyEMA[m-1]) * (1-k)) + (c[m]*k))
	sixtyEMA[m] = round(float(sixtyEMA[m]),2)

k = float(2) / 121
S = (dat.iloc[120]["onetwenty"] * (1-k)) + (c[121]*k)
onetwentyEMA=[]
for m in range(0,len(c)):
	if m < 120:
		onetwentyEMA.append("0")
	elif m == 120:
		onetwentyEMA.append(S)
	else:
		onetwentyEMA.append((float(onetwentyEMA[m-1]) * (1-k)) + (c[m]*k))
	onetwentyEMA[m] = round(float(onetwentyEMA[m]),2)

macd=[]
for n in range(0,len(dat)):
	if n < 26:
		macd.append("0")
	else:
		macd.append(twelveEMA[n] - twentysixEMA[n])

k = float(2) / 10
signal=[]
macdHisto=[]
for l in range(0,len(dat)):
	if l < 26:
		signal.append("0")
		macdHisto.append("0")
	elif l == 26:
		signal.append(np.sum(macd[26:35])/9)
		macdHisto.append(macd[26] - signal[26])
	else:
		signal.append((float(signal[l-1]) * (1-k)) + (macd[l]*k))
		macdHisto.append(macd[l] - signal[l])

emas = []
emas.append(nineEMA)
emas.append(tenEMA)
emas.append(twelveEMA)
emas.append(twentysixEMA)
emas.append(thirtyEMA)
emas.append(fiftyEMA)
emas.append(sixtyEMA)
emas.append(onetwentyEMA)
emas.append(macd)
emas.append(signal)
emas.append(macdHisto)
emas.append(twentyeightDayVol)

#create dataFrame with exponential moving averages,
#MACD values, and volume trend values.
#save to a .csv file which will be referenced in main plotting code
df = pd.DataFrame(emas).T 
df.to_csv("emas.csv", header=["nine","ten","twelve","twentysix","thirty",
								"fifty","sixty","onetwenty","macd","signal",
								"macdHisto","twentyeightDayVol"])
dat = pd.read_csv("emas.csv")
