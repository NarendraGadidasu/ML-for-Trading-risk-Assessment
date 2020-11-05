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

class Experiment2(object):

    def __init__(self, verbose=False):
        self.verbose = verbose
        
    def author(self):
        return 'dgadidasu3'
    
    def test_code(self, sd, ed, inout = 'insample', impc = [0.0005, 0.005, 0.05]):
        
        ms = ManualStrategy()
        trades_ms = ms.testPolicy(symbol = "JPM", sd=sd, ed=ed, sv = 100000)
        trades_bm = trades_ms.copy()
        trades_bm.loc[:,:] = 0
        trades_bm.loc[trades_bm.index.min(),:] = 1000
        
        fig = plt.figure(figsize=(9,9))
        
        ax1 = fig.add_subplot(111)
        
        colors = ['red', 'orange', 'green']
        
    #    metrics = pd.DataFrame({'cum_return_sl':0, 'std_daily_ret_sl':0, 'mean_daily_ret_sl':0, 'sharpe_ratio_sl':0,
    #                                'cum_return_bm':0, 'std_daily_ret_bm':0, 'mean_daily_ret_bm':0, 'sharpe_ratio_bm':0}, index = [0])
        
        metrics = pd.DataFrame(columns = ['cum_return_sl', 'std_daily_ret_sl', 'mean_daily_ret_sl', 'sharpe_ratio_sl',
                                    'cum_return_bm', 'std_daily_ret_bm', 'mean_daily_ret_bm', 'sharpe_ratio_bm'])
        metrics.to_csv('Experiment_2_{}.csv'.format(inout))
        
        trds_sl = []
        
        for i in range(len(impc)):
            
            imp = impc[i]
            
            portvals_bm = compute_portvals(orders_file = trades_bm, start_val = 100000, commission=0, impact=imp)
            portvals_bm = portvals_bm/portvals_bm.loc[portvals_bm.index.min()]
            
            portvals_bm.sort_index(inplace=True)
            
            ax1.plot(portvals_bm.index, portvals_bm, color = colors[i], label = 'Benchmark_{}'.format(imp), linestyle = 'dashed')
            
            sl = StrategyLearner(impact=imp)
            sl.addEvidence(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = 100000)
            
            trades_sl = sl.testPolicy(symbol = "JPM", sd=sd, ed=ed, sv = 100000)
            
            trds_sl.append(trades_sl)
            
            portvals_sl = compute_portvals(orders_file = trades_sl, start_val = 100000, commission=0, impact=imp)
            
            portvals_sl = portvals_sl/portvals_sl.loc[portvals_sl.index.min()]
            
            portvals_sl.sort_index(inplace=True)
            
            ax1.plot(portvals_sl.index, portvals_sl, color = colors[i], label = 'StrategyLearner_{}'.format(imp))  
            
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
            
            metrics = pd.DataFrame({'cum_return_sl':cum_return_sl, 'std_daily_ret_sl':std_daily_ret_sl, 'mean_daily_ret_sl':mean_daily_ret_sl, 'sharpe_ratio_sl':sharpe_ratio_sl,
                                    'cum_return_bm':cum_return_bm, 'std_daily_ret_bm':std_daily_ret_bm, 'mean_daily_ret_bm':mean_daily_ret_bm, 'sharpe_ratio_bm':sharpe_ratio_bm}, index = [imp])
            metrics.to_csv('Experiment_2_{}.csv'.format(inout), mode = 'a', header = False)
        
        ax1.legend()
        ax1.set_xlabel('dates')
        plt.xticks(rotation = 30)
        
        plt.savefig('Exeperiment_2_{}.png'.format(inout))
        plt.close()
        

        
        
if __name__ == '__main__':
    np.random.seed(23)
    e = Experiment2()
    e.test_code(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), inout = 'insample')
    e.test_code(dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31), inout = 'outsample')