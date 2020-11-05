# -*- coding: utf-8 -*-
"""

@author: A103932
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from util import get_data
import datetime as dt
from marketsimcode import compute_portvals

def author():
    return 'dgadidasu3'

class TheoreticallyOptimalStrategy:
    def __init__(self):
        pass
    
    def author(self):
        return 'dgadidasu3'

    def testPolicy(self, symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):
        prices = get_data([symbol], pd.date_range(sd, ed))
        prices = prices.loc[:,[symbol]]
        prices.ffill(inplace=True)
        prices.bfill(inplace=True)
        isgain = prices<prices.shift(-1)
        isgain.sort_index(inplace=True)
        trades = isgain.copy()
        
        holdings = 0
        
        for index, row in isgain.iterrows():
            if holdings == 0 and row[symbol] == True:
                trades.loc[index, symbol] = 1000
                holdings += 1000
            elif holdings == -1000 and row[symbol] == True:
                trades.loc[index, symbol] = 2000
                holdings += 2000
            elif holdings == 1000 and row[symbol] == True:
                trades.loc[index, symbol] = 0
                holdings += 0
            elif holdings == 0 and row[symbol] == False:
                trades.loc[index, symbol] = -1000
                holdings -= 1000
            elif holdings == -1000 and row[symbol] == False:
                trades.loc[index, symbol] = 0
                holdings += 0
            elif holdings == 1000 and row[symbol] == False:
                trades.loc[index, symbol] = -2000
                holdings -= 2000  
            else:
                pass
        
        trades.loc[trades.index.max(), symbol] = 0
        
        self.trades = trades
        return trades

def test_code():
    tos = TheoreticallyOptimalStrategy()
    in_sd = dt.datetime(2008, 1, 1)
    in_ed = dt.datetime(2009, 12, 31)
    trades_tos = tos.testPolicy(symbol = "JPM", sd=in_sd, ed=in_ed, sv = 100000)
    trades_bm = trades_tos.copy()
    trades_bm.loc[:,:] = 0
    trades_bm.loc[trades_bm.index.min(),:] = 1000
    
    portvals_tos = compute_portvals(orders_file = trades_tos, start_val = 100000, commission=0.0, impact=0.0)
    portvals_bm = compute_portvals(orders_file = trades_bm, start_val = 100000, commission=0.0, impact=0.0)
    
    portvals_tos = portvals_tos/portvals_tos.loc[portvals_tos.index.min()]
    portvals_bm = portvals_bm/portvals_bm.loc[portvals_bm.index.min()]
    
    fig = plt.figure(figsize=(9,9))
    
    ax1 = fig.add_subplot(111)
    
    portvals_tos.sort_index(inplace=True)
    portvals_bm.sort_index(inplace=True)
    
    ax1.plot(portvals_tos.index, portvals_tos, color = 'red', label = 'TheoreticallyOptimalStrategy')
    ax1.plot(portvals_bm.index, portvals_bm, color = 'green', label = 'Benchmark')
    
    ax1.legend()
    ax1.set_xlabel('dates')
    plt.xticks(rotation = 30)
    
    plt.savefig('TheoreticallyOptimalStrategy.png')
    plt.close()
    			  		 			     			  	   		   	  			  	
    daily_rets_tos = (portvals_tos / portvals_tos.shift(1)) - 1 			  		 			     			  	   		   	  			  	
    daily_rets_tos = daily_rets_tos[1:] 			  		 			     			  	   		   	  			  	
    mean_daily_ret_tos = daily_rets_tos.mean() 			  		 			     			  	   		   	  			  	
    std_daily_ret_tos = daily_rets_tos.std() 			  		 			     			  	   		   	  			  	
    sharpe_ratio_tos = np.sqrt(252) * daily_rets_tos.mean() / std_daily_ret_tos
    cum_return_tos = (portvals_tos[len(portvals_tos)-1]/portvals_tos[0])-1
    
    daily_rets_bm = (portvals_bm / portvals_bm.shift(1)) - 1 			  		 			     			  	   		   	  			  	
    daily_rets_bm = daily_rets_bm[1:] 			  		 			     			  	   		   	  			  	
    mean_daily_ret_bm = daily_rets_bm.mean() 			  		 			     			  	   		   	  			  	
    std_daily_ret_bm = daily_rets_bm.std() 			  		 			     			  	   		   	  			  	
    sharpe_ratio_bm = np.sqrt(252) * daily_rets_bm.mean() / std_daily_ret_bm
    cum_return_bm = (portvals_bm[len(portvals_bm)-1]/portvals_bm[0])-1
    
    metrics = pd.DataFrame({'cum_return_tos':cum_return_tos, 'std_daily_ret_tos':std_daily_ret_tos, 'mean_daily_ret_tos':mean_daily_ret_tos, 
                            'cum_return_bm':cum_return_bm, 'std_daily_ret_bm':std_daily_ret_bm, 'mean_daily_ret_bm':mean_daily_ret_bm}, index = ['0'])
    metrics.to_csv('TheoreticallyOptimalStrategy_metrics.csv')
    
if __name__ == '__main__':
    test_code()