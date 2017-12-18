
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:24:10 2017

@author: chuan
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import datestr2num
import matplotlib
from matplotlib.font_manager import *  
#import numpy as np
#%%
#数据读取    
hs300 = pd.read_csv("hs300.csv")
hsa = pd.read_csv("hsa.csv")
hxhs = pd.read_csv("hxhs.csv",encoding="utf-8")
htbr = pd.read_csv("htbr.csv",encoding="utf-8")

#%%
#长度不一致的处理办法
a = list(hsa['tradeDate'])
b = list(hs300['tradeDate'])
aa = set(a)
bb = set(b)
print (list(bb.difference(aa)))
hsa=hsa.drop(len(hsa)-1,axis=0)
#回测必须利用前一天的ETF数据，删除指数数据的第一行

#%%
def trading(capitalbase=100000,lb=135,ub=140):
    positions = []
    
    cash = capitalbase
    
    hxhs_flag = 0
    
    htbr_flag = 1
    
    price_temp1 = []
    price_temp2 = []
    buy_num1 = 0
    buy_num2 = 0
    positions_temp = capitalbase
    for row in hsa.iterrows():
        date = row[1][1]
        price_temp1 = htbr[htbr.tradeDate>date].closePrice.values[0]
        price_temp2 = hxhs[hxhs.tradeDate>date].closePrice.values[0]
        if(row[1][2])<135 and htbr_flag==0 :
            #AH溢价指数低于135时买入华泰柏瑞沪深300ETF
            #print(hsa[hsa.tradeDate<'2016-01-05'].tail(1).closeIndex)
            print('=======================================')
            buy_num1 = int(capitalbase/price_temp1/100)
            print(date,'突破指数下限，以价格%s 元买入华泰柏瑞沪深300ETF%d 手'%(price_temp1,buy_num1))
            htbr_flag = 1
            cash = positions_temp-buy_num1*100*price_temp1
            if hxhs_flag == 1:
                print(date,'卖出华夏恒生ETF')
                hxhs_flag = 0
        if(row[1][2])>140 and hxhs_flag==0 :
            print('=======================================')
            buy_num2 = int(cash/price_temp2/100)
            print(date,'突破指数上限，以价格%s 元买入华夏恒生ETF%d 手'%(price_temp2,buy_num2))
            hxhs_flag = 1
            cash = positions_temp-buy_num2*100*price_temp2
            if htbr_flag == 1:
                print(date,'卖出华泰柏瑞沪深300ETF')
                htbr_flag = 0
        else:
            print(date,'当天无交易！')
        positions_temp = htbr_flag*buy_num1*100*price_temp1+hxhs_flag*buy_num2*100*price_temp2+cash
        positions.append(positions_temp)
        print(date,'当日账户权益为%d'%positions_temp)
    
    return positions
#%%
    
positions = trading()

strategy_positions = pd.DataFrame(positions)
return_strategy = (strategy_positions/strategy_positions.shift())-1
return_strategy = return_strategy.cumsum()

hsa_closeIndex = pd.DataFrame(hsa.closeIndex)
return_hsa = (hsa_closeIndex/hsa_closeIndex.shift())-1
return_hsa = return_hsa.cumsum()

matplotlib.use('qt4agg')
myfont = FontProperties(fname='C:\Windows\Fonts\simhei.ttf')
matplotlib.rcParams['axes.unicode_minus']=False     
plt.figure(figsize=(10,5))
plt.title(u"累计收益率",fontproperties=myfont)
x_date = [datestr2num(i) for i in hsa.tradeDate]
plt.plot_date(x_date,return_hsa,'-')
plt.plot_date(x_date,return_strategy,'-',color='r')
plt.legend(['恒生指数','策略累计收益率'],prop=myfont)

#date = pd.to_datetime(hsa.tradeDate)
#hsa_hist = pd.DataFrame({'closeIndex':hsa.closeIndex},index=hsa.tradeDate)
#plt.plot(hsa_hist)
#plt.show()
