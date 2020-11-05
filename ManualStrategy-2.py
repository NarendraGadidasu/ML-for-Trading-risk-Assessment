# -*- coding: utf-8 -*-
"""

Student Name: Damodara Venkata Narendra, Gadidasu (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: dgadidasu3 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903457715 (replace with your GT ID) 

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from util import get_data
import datetime as dt
from marketsimcode import compute_portvals
from indicators import gen_indicators

def author():
    return 'dgadidasu3'

class ManualStrategy:
    def __init__(self):
        pass
    
    def author(self):
        return 'dgadidasu3'

    def testPolicy(self, symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):
        prices = get_data([symbol], pd.date_range(sd, ed))
        prices = prices.loc[:,[symbol]]
        prices.ffill(inplace=True)
        prices.bfill(inplace=True)
        df_indicators = gen_indicators('JPM', sd, ed, sv, lb = 14)
        df_indicators['isgain'] = True
        df_indicators.loc[(df_indicators['sma_ratio']<1) & (df_indicators['bbp']<0) & (df_indicators['momentum']<0), 'isgain'] = True
        df_indicators.loc[(df_indicators['sma_ratio']>1) & (df_indicators['bbp']>0) & (df_indicators['momentum']>0), 'isgain'] = False
        
        
        isgain =  df_indicators.loc[:, ['isgain']]
        isgain.rename(columns={'isgain':symbol}, inplace=True)
        trades = isgain.copy()
        trades.loc[:,:] = 0
        
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

def test_code(sd, ed, inout = 'insample'):
    ms = ManualStrategy()
    trades_ms = ms.testPolicy(symbol = "JPM", sd=sd, ed=ed, sv = 100000)
    trades_bm = trades_ms.copy()
    longs_ms = trades_ms[trades_ms['JPM']>0]
    shorts_ms = trades_ms[trades_ms['JPM']<0]
    trades_bm.loc[:,:] = 0
    trades_bm.loc[trades_bm.index.min(),:] = 1000
    
    portvals_ms = compute_portvals(orders_file = trades_ms, start_val = 100000, commission=9.95, impact=0.005)
    portvals_bm = compute_portvals(orders_file = trades_bm, start_val = 100000, commission=9.95, impact=0.005)
    
    portvals_ms = portvals_ms/portvals_ms.loc[portvals_ms.index.min()]
    portvals_bm = portvals_bm/portvals_bm.loc[portvals_bm.index.min()]
    
    fig = plt.figure(figsize=(9,9))
    
    ax1 = fig.add_subplot(111)
    
    portvals_ms.sort_index(inplace=True)
    portvals_bm.sort_index(inplace=True)
    
    ax1.plot(portvals_ms.index, portvals_ms, color = 'red', label = 'ManualStrategy')
    ax1.plot(portvals_bm.index, portvals_bm, color = 'green', label = 'Benchmark')
    
    ax1.legend()
    ax1.set_xlabel('dates')
    plt.xticks(rotation = 30)
    
    if inout == 'insample':
        for i in range(len(longs_ms.index)):
            ax1.axvline(x = longs_ms.index[i], color = 'blue')
            
        for j in range(len(shorts_ms.index)):
            ax1.axvline(x = shorts_ms.index[j], color = 'black')
    
    plt.savefig('ManualStrategy_{}.png'.format(inout))
    plt.close()
    			  		 			     			  	   		   	  			  	
    daily_rets_ms = (portvals_ms / portvals_ms.shift(1)) - 1 			  		 			     			  	   		   	  			  	
    daily_rets_ms = daily_rets_ms[1:] 			  		 			     			  	   		   	  			  	
    mean_daily_ret_ms = daily_rets_ms.mean() 			  		 			     			  	   		   	  			  	
    std_daily_ret_ms = daily_rets_ms.std() 			  		 			     			  	   		   	  			  	
    sharpe_ratio_ms = np.sqrt(252) * daily_rets_ms.mean() / std_daily_ret_ms
    cum_return_ms = (portvals_ms[len(portvals_ms)-1]/portvals_ms[0])-1
    
    daily_rets_bm = (portvals_bm / portvals_bm.shift(1)) - 1 			  		 			     			  	   		   	  			  	
    daily_rets_bm = daily_rets_bm[1:] 			  		 			     			  	   		   	  			  	
    mean_daily_ret_bm = daily_rets_bm.mean() 			  		 			     			  	   		   	  			  	
    std_daily_ret_bm = daily_rets_bm.std() 			  		 			     			  	   		   	  			  	
    sharpe_ratio_bm = np.sqrt(252) * daily_rets_bm.mean() / std_daily_ret_bm
    cum_return_bm = (portvals_bm[len(portvals_bm)-1]/portvals_bm[0])-1
    
    metrics = pd.DataFrame({'cum_return_ms':cum_return_ms, 'std_daily_ret_ms':std_daily_ret_ms, 'mean_daily_ret_ms':mean_daily_ret_ms, 
                            'cum_return_bm':cum_return_bm, 'std_daily_ret_bm':std_daily_ret_bm, 'mean_daily_ret_bm':mean_daily_ret_bm}, index = ['0'])
    metrics.to_csv('ManualStrategy_{}.csv'.format(inout))
    
if __name__ == '__main__':
    test_code(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), inout = 'insample')
    test_code(dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31), inout = 'outsample')