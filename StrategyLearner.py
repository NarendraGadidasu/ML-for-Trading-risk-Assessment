""" 			  		 			     			  	   		   	  			  	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			     			  	   		   	  			  	
Atlanta, Georgia 30332 			  		 			     			  	   		   	  			  	
All Rights Reserved 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Template code for CS 4646/7646 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			     			  	   		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			     			  	   		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			     			  	   		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			     			  	   		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			     			  	   		   	  			  	
or edited. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			     			  	   		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			     			  	   		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			     			  	   		   	  			  	
GT honor code violation. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
-----do not edit anything above this line--- 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Student Name: Damodara Venkata Narendra, Gadidasu (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: dgadidasu3 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903457715 (replace with your GT ID) 			  		 			     			  	   		   	  			  	
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import datetime as dt
import numpy as np 			  		 			     			  	   		   	  			  	
import pandas as pd 			  		 			     			  	   		   	  			  	
import util as ut 			  		 			     			  	   		   	  			  	
import RTLearner as rt	
import BagLearner as bl	
from indicators import gen_indicators	  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
class StrategyLearner(object): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # constructor 			  		 			     			  	   		   	  			  	
    def __init__(self, verbose = False, impact=0.0): 			  		 			     			  	   		   	  			  	
        self.verbose = verbose 			  		 			     			  	   		   	  			  	
        self.impact = impact
        self.impact_z = impact
        self.policy = 0
        self.trades = 0

    #author method
    def author(self):
        return 'dgadidasu3'

    # this method should create a QLearner, and train it for trading 			  		 			     			  	   		   	  			  	
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 			  		 			     			  	   		   	  			  	
    			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        # example usage of the old backward compatible util function 			  		 			     			  	   		   	  			  	
        syms=[symbol] 			  		 			     			 
        n = 20 	   		   	  			  	
        dates = pd.date_range(sd-pd.to_timedelta(n*2, unit = 'd'), ed) 			  		 			     			  	   		   	  			  	
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY 			  		 			     			  	   		   	  			  	
        prices = prices_all[syms]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
        #prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        
        prices_shifted = prices.shift(-n)
        
        prices_shifted.dropna(inplace = True)

        pct_chg = prices_shifted.loc[:, symbol].pct_change(n)

        pct_chg.dropna(inplace=True)
        		  		 			     			  	   		   	  			  		  		 			     			  	   		   	  			  	
        ind  = gen_indicators(symbol, sd, ed, sv, lb = 14)
        
        pct_chg = pct_chg.loc[ind.index.min():pct_chg.index.max()]
        
        ind = ind.loc[ind.index.min():pct_chg.index.max()]
        
        ind = ind[['sma_ratio', 'momentum', 'bbp']]
        
        pct_chg = (pct_chg - pct_chg.mean())/pct_chg.std()
        
        self.impact_z = (self.impact - pct_chg.mean())/pct_chg.std() 
        
        b = bl.BagLearner(learner=rt.RTLearner, kwargs={'leaf_size' : 5}, bags = 20, boost = False, verbose = False)
        
        b.addEvidence(ind.values, pct_chg.values)
        
        self.policy = b
        
        return b
		  		 			     			  	   		   	  			  	
    # this method should use the existing policy and test it against new data 			  		 			     			  	   		   	  			  	
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        # here we build a fake set of trades 			  		 			     			  	   		   	  			  	
        # your code should return the same sort of data 
#        dates = pd.date_range(sd, ed) 			  		 			     			  	   		   	  			  	
#        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY 			  		 			     			  	   		   	  			  	
#        
#        syms=[symbol] 			  		 			     			    		   	  			  	
#        dates = pd.date_range(sd, ed) 			  		 			     			  	   		   	  			  	
#        prices_all = ut.get_data(syms, dates)  # automatically adds SPY 			  		 			     			  	   		   	  			  	
#        prices = prices_all[syms]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
#        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        		  		 			     			  	   		   	  			  		  		 			     			  	   		   	  			  	
        ind  = gen_indicators(symbol, sd, ed, sv, lb = 14)
        
        df_indicators = ind[['sma_ratio', 'momentum', 'bbp']]
        
        df_indicators['nday_ret'] = self.policy.query(df_indicators.values)
        
        df_indicators['nday_ret'] = df_indicators['nday_ret'] - self.impact_z
        
        df_indicators.loc[:, 'dec'] = 0
        
        p = np.percentile(df_indicators['nday_ret'].values, [80, 20])
        
        df_indicators.loc[df_indicators['nday_ret']>p[0], 'dec'] = 1
        
        df_indicators.loc[df_indicators['nday_ret']<p[1], 'dec'] = -1
        
        isgain =  df_indicators.loc[:, ['dec']]
        isgain.rename(columns={'dec':symbol}, inplace=True)
        trades = isgain.copy()  
        trades.loc[:,:] = 0
        
        holdings = 0
        
        for index, row in isgain.iterrows():
            if holdings == 0 and row[symbol] == 1:
                trades.loc[index, symbol] = 1000
                holdings += 1000
            elif holdings == -1000 and row[symbol] == 1:
                trades.loc[index, symbol] = 2000
                holdings += 2000
            elif holdings == 1000 and row[symbol] == 1:
                trades.loc[index, symbol] = 0
                holdings += 0
            elif holdings == 0 and row[symbol] == -1:
                trades.loc[index, symbol] = -1000
                holdings -= 1000
            elif holdings == -1000 and row[symbol] == -1:
                trades.loc[index, symbol] = 0
                holdings += 0
            elif holdings == 1000 and row[symbol] == -1:
                trades.loc[index, symbol] = -2000
                holdings -= 2000  
            else:
                pass
        
        trades.loc[trades.index.max(), symbol] = 0
        
        return trades		  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__=="__main__":
    
    print "One does not simply think up a strategy" 			  		 			     			  	   		   	  			  	
