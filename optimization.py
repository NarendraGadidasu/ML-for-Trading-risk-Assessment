"""MC1-P2: Optimize a portfolio. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import pandas as pd 			  		 			     			  	   		   	  			  	
import matplotlib.pyplot as plt 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
from util import get_data, plot_data 				  		 			     			  	   		   	  			  	
# This is the function that will be tested by the autograder 			  		 			     			  	   		   	  			  	
# The student must update this code to properly implement the functionality 			  		 			     			  	   		   	  			  	
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Read in adjusted closing prices for given symbols, date range 			  		 			     			  	   		   	  			  	
    dates = pd.date_range(sd, ed) 			  		 			     			  	   		   	  			  	
    prices_all = get_data(syms, dates)  # automatically adds SPY 			  		 			     			  	   		   	  			  	
    prices = prices_all[syms]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # find the allocations for the optimal portfolio 			  		 			     			  	   		   	  			  	
    # note that the values here ARE NOT meant to be correct for a test case 

        			  		 			     			  	   		   	  			  	
    allocs_init = (np.ones(len(syms)))*(1.0/len(syms)) # add code here to find the allocations

    def metrics(allcs, prcs):
        prcs = prcs/prcs.iloc[0,:]
        prcs.fillna(method = 'ffill', inplace = True)
        prcs.fillna(method = 'bfill', inplace = True)
        port_prcs = prcs.dot(np.array(allcs).T)
        dr = (port_prcs/port_prcs.shift(1))-1
        dr = dr.iloc[1:]
        cr = (port_prcs[len(port_prcs)-1]/port_prcs[0])-1
        adr = dr.mean()
        sddr = dr.std()
        sr = np.sqrt(252)*(adr/sddr)
        return port_prcs, cr, adr, sddr, sr
        
    def error(allcs, prcs):
        return -1*metrics(allcs, prcs)[4]
        
    import scipy.optimize as spo

    cons = ({'type': 'eq', 'fun': lambda x:  1 - np.sum(x)})

    l = [(0,1)]*len(syms)

    bnds = tuple(l)
    
    alloc_result = spo.minimize(error, allocs_init, args = (prices,), method = 'SLSQP', constraints = cons, bounds = bnds, options = {'disp':False})

    allocs = alloc_result.x

    final_metrics = metrics(allocs, prices)
		  		 			     			  	   		   	  			  	
    cr, adr, sddr, sr = final_metrics[1:]# add code here to compute stats 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Get daily portfolio value 			  		 			     			  	   		   	  			  	
    port_val = final_metrics[0] # add code here to compute daily portfolio values 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Compare daily portfolio value with SPY using a normalized plot 			  		 			     			  	   		   	  			  	
    if gen_plot: 			  		 			     			  	   		   	  			  	
        # add code to plot here 			  		 			     			  	         
	df_temp = pd.concat([port_val, prices_SPY/prices_SPY[0]], keys=['Portfolio', 'SPY'], axis=1)
        import matplotlib.pyplot as plt
        df_temp.plot()
        plt.savefig('optimized.pdf')		  		 			     			  	   		   		  	
    return allocs, cr, adr, sddr, sr 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def test_code(): 			  		 			     			  	   		   	  			  	
    # This function WILL NOT be called by the auto grader 			  		 			     			  	   		   	  			  	
    # Do not assume that any variables defined here are available to your function/code 			  		 			     			  	   		   	  			  	
    # It is only here to help you set up and test your code 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Define input parameters 			  		 			     			  	   		   	  			  	
    # Note that ALL of these values will be set to different values by 			  		 			     			  	   		   	  			  	
    # the autograder! 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    start_date = dt.datetime(2009,1,1) 			  		 			     			  	   		   	  			  	
    end_date = dt.datetime(2010,1,1) 			  		 			     			  	   		   	  			  	
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM'] 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Assess the portfolio 			  		 			     			  	   		   	  			  	
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False) 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Print statistics 			  		 			     			  	   		   	  			  	
    print "Start Date:", start_date 			  		 			     			  	   		   	  			  	
    print "End Date:", end_date 			  		 			     			  	   		   	  			  	
    print "Symbols:", symbols 			  		 			     			  	   		   	  			  	
    print "Allocations:", allocations 			  		 			     			  	   		   	  			  	
    print "Sharpe Ratio:", sr 			  		 			     			  	   		   	  			  	
    print "Volatility (stdev of daily returns):", sddr 			  		 			     			  	   		   	  			  	
    print "Average Daily Return:", adr 			  		 			     			  	   		   	  			  	
    print "Cumulative Return:", cr 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    # This code WILL NOT be called by the auto grader 			  		 			     			  	   		   	  			  	
    # Do not assume that it will be called 			  		 			     			  	   		   	  			  	
    test_code() 			  		 			     			  	   		   	  			  	
