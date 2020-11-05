# -*- coding: utf-8 -*-
"""

Student Name: Damodara Venkata Narendra, Gadidasu (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: dgadidasu3 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903457715 (replace with your GT ID) 

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from marketsimcode import compute_portvals
from ManualStrategy import ManualStrategy
from StrategyLearner import StrategyLearner

class Experiment1(object):
    
    def __init__(self, verbose = False):
        self.verbose = verbose

    def author(self):
        return 'dgadidasu3'
    
    def test_code(self, sd, ed, inout = 'insample', imp = 0.005):
        ms = ManualStrategy()
        trades_ms = ms.testPolicy(symbol = "JPM", sd=sd, ed=ed, sv = 100000)
        
        sl = StrategyLearner(impact=imp)
        sl.addEvidence(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = 100000)
        trades_sl = sl.testPolicy(symbol = "JPM", sd=sd, ed=ed, sv = 100000)
        
        
        trades_bm = trades_ms.copy()
        
    #    longs_ms = trades_ms[trades_ms['JPM']>0]
    #    shorts_ms = trades_ms[trades_ms['JPM']<0]
        
        trades_bm.loc[:,:] = 0
        trades_bm.loc[trades_bm.index.min(),:] = 1000
        
        portvals_ms = compute_portvals(orders_file = trades_ms, start_val = 100000, commission=0, impact=imp)
        portvals_sl = compute_portvals(orders_file = trades_sl, start_val = 100000, commission=0, impact=imp)
        portvals_bm = compute_portvals(orders_file = trades_bm, start_val = 100000, commission=0, impact=imp)
        
        portvals_ms = portvals_ms/portvals_ms.loc[portvals_ms.index.min()]
        portvals_sl = portvals_sl/portvals_sl.loc[portvals_sl.index.min()]
        portvals_bm = portvals_bm/portvals_bm.loc[portvals_bm.index.min()]
        
        fig = plt.figure(figsize=(9,9))
        
        ax1 = fig.add_subplot(111)
        
        portvals_ms.sort_index(inplace=True)
        portvals_sl.sort_index(inplace=True)
        portvals_bm.sort_index(inplace=True)
        
        ax1.plot(portvals_ms.index, portvals_ms, color = 'red', label = 'ManualStrategy')
        ax1.plot(portvals_sl.index, portvals_sl, color = 'orange', label = 'StrategyLearner')
        ax1.plot(portvals_bm.index, portvals_bm, color = 'green', label = 'Benchmark')
        
        ax1.legend()
        ax1.set_xlabel('dates')
        plt.xticks(rotation = 30)
        
    #    if inout == 'insample':
    #        for i in range(len(longs_ms.index)):
    #            ax1.axvline(x = longs_ms.index[i], color = 'blue')
    #            
    #        for j in range(len(shorts_ms.index)):
    #            ax1.axvline(x = shorts_ms.index[j], color = 'black')
        
        plt.savefig('Exeperiment_1_{}.png'.format(inout))
        plt.close()
        			  		 			     			  	   		   	  			  	
        daily_rets_ms = (portvals_ms / portvals_ms.shift(1)) - 1 			  		 			     			  	   		   	  			  	
        daily_rets_ms = daily_rets_ms[1:] 			  		 			     			  	   		   	  			  	
        mean_daily_ret_ms = daily_rets_ms.mean() 			  		 			     			  	   		   	  			  	
        std_daily_ret_ms = daily_rets_ms.std() 			  		 			     			  	   		   	  			  	
        sharpe_ratio_ms = np.sqrt(252) * daily_rets_ms.mean() / std_daily_ret_ms
        cum_return_ms = (portvals_ms[len(portvals_ms)-1]/portvals_ms[0])-1
        
        daily_rets_sl = (portvals_sl / portvals_sl.shift(1)) - 1 			  		 			     			  	   		   	  			  	
        daily_rets_sl = daily_rets_sl[1:] 			  		 			     			  	   		   	  			  	
        mean_daily_ret_sl = daily_rets_sl.mean() 			  		 			     			  	   		   	  			  	
        std_daily_ret_sl = daily_rets_sl.std() 			  		 			     			  	   		   	  			  	
        sharpe_ratio_sl = np.sqrt(252) * daily_rets_sl.mean() / std_daily_ret_sl
        cum_return_sl = (portvals_sl[len(portvals_sl)-1]/portvals_sl[0])-1
        
        daily_rets_bm = (portvals_bm / portvals_bm.shift(1)) - 1 			  		 			     			  	   		   	  			  	
        daily_rets_bm = daily_rets_bm[1:] 			  		 			     			  	   		   	  			  	
        mean_daily_ret_bm = daily_rets_bm.mean() 			  		 			     			  	   		   	  			  	
        std_daily_ret_bm = daily_rets_bm.std() 			  		 			     			  	   		   	  			  	
        sharpe_ratio_bm = np.sqrt(252) * daily_rets_bm.mean() / std_daily_ret_bm
        cum_return_bm = (portvals_bm[len(portvals_bm)-1]/portvals_bm[0])-1
        
        metrics = pd.DataFrame({'cum_return_ms':cum_return_ms, 'std_daily_ret_ms':std_daily_ret_ms, 'mean_daily_ret_ms':mean_daily_ret_ms, 'sharpe_ratio_ms':sharpe_ratio_ms,
                                'cum_return_sl':cum_return_sl, 'std_daily_ret_sl':std_daily_ret_sl, 'mean_daily_ret_sl':mean_daily_ret_sl, 'sharpe_ratio_sl':sharpe_ratio_sl,
                                'cum_return_bm':cum_return_bm, 'std_daily_ret_bm':std_daily_ret_bm, 'mean_daily_ret_bm':mean_daily_ret_bm, 'sharpe_ratio_bm':sharpe_ratio_bm}, index = ['0'])
        metrics.to_csv('Experiment_1_{}.csv'.format(inout))
    
if __name__ == '__main__':
    np.random.seed(23)
    e = Experiment1()
    e.test_code(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), inout = 'insample')