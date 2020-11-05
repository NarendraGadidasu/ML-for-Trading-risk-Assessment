# -*- coding: utf-8 -*-

"""
Student Name: Damodara Venkata Narendra, Gadidasu (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: dgadidasu3 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903457715 (replace with your GT ID) 

"""


import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt

def author():
    return 'dgadidasu3'

def gen_indicators(symbol = 'JPM', start_date = dt.datetime(2008, 1, 1), end_date = dt.datetime(2009, 12, 31), sv = 100000, lb = 2):
    prices = get_data([symbol], pd.date_range(start_date-pd.to_timedelta(lb, unit = 'd'), end_date))
    prices.ffill(inplace = True)
    prices.bfill(inplace=True)
    prices.sort_index(inplace=True)
    prices = prices.loc[:,[symbol]]
    
    ind = pd.DataFrame(index = prices.index)
    ind['price'] = prices
    
    sma = prices.copy()
    sma.loc[:,:] = 0
    sma = prices.rolling(window = lb, min_periods = lb).mean()
    
    rolling_std = prices.rolling(window = lb, min_periods = lb).std()
    
    ind['rolling_std'] = rolling_std
    
    top_band = sma+(2*rolling_std)
    bottom_band = sma-(2*rolling_std)
    bbp = (prices - top_band)/(top_band - bottom_band)

    ind['top_band'] = top_band
    ind['bottom_band'] = bottom_band
    ind['bbp'] = bbp
    
    ind['sma'] = sma
    
    sma = prices/sma
    
    ind['sma_ratio'] = sma
    
    momentum = (prices/prices.shift(lb-1))-1
    
    ind['momentum'] = momentum
    
    ind = ind.loc[start_date:,:]
    
    ind = ind.dropna()
    
    return ind

def test_code():
    in_sd = dt.datetime(2008, 1, 1)
    in_ed = dt.datetime(2009, 12, 31)
    ind = gen_indicators('JPM', in_sd, in_ed, sv = 100000, lb = 14)
    fig, ax1 = plt.subplots(figsize=(9,9))
    lns1 = ax1.plot(ind.index, ind['price'],label='price',color='b')
    lns2 = ax1.plot(ind.index, ind['sma'],label='sma',color='r')
    ax1.set_ylabel('price, sma')
    
    plt.xticks(rotation=30)
    
    ax2 = ax1.twinx()
    
    lns3 = ax2.plot(ind.index, ind['sma_ratio'],label='sma_ratio',color='orange')
    ax2.set_ylabel('sma_ratio')
    
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    
    plt.savefig('indicators_sma_ratio.png')
    plt.close()
    
    fig = plt.figure(figsize = (18,9))
    
    ax1 = fig.add_subplot(121)
    
    lns1 = ax1.plot(ind.index, ind['price'],label='price',color='b')
    lns2 = ax1.plot(ind.index, ind['sma'],label='sma',color='r')
    lns3 = ax1.plot(ind.index, ind['top_band'],label='top_band',color='g')
    lns4 = ax1.plot(ind.index, ind['bottom_band'],label='bottom_band',color='orange')
    ax1.set_ylabel('price, sma, bollinger_bands')
    
    lns = lns1+lns2+lns3+lns4
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    
    plt.xticks(rotation=30)
    
    ax2 = fig.add_subplot(122)
    lns5 = ax2.plot(ind.index, ind['rolling_std'],label='rolling_std',color='b')
    lns6 = ax2.plot(ind.index, ind['bbp'],label='bbp',color='r')
    
    ax2.set_ylabel('rolling_std, bbp')
    
    lns = lns5+lns6
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=0)
    
    plt.xticks(rotation=30)
    
    plt.savefig('indicators_bbp.png')
    plt.close()
    
    fig, ax1 = plt.subplots(figsize=(9,9))
    lns1 = ax1.plot(ind.index, ind['price'],label='price',color='b')
    ax1.set_ylabel('price')
    
    plt.xticks(rotation=30)
    
    ax2 = ax1.twinx()
    
    lns2 = ax2.plot(ind.index, ind['momentum'],label='momentum',color='orange')
    ax2.set_ylabel('momentum')
    
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    
    plt.savefig('indicators_momentum.png')
    plt.close()

if __name__ == '__main__':
    test_code()
    
    