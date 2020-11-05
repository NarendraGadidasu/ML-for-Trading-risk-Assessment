"""MC2-P1: Market simulator. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
import os 			  		 			     			  	   		   	  			  	
from util import get_data, plot_data 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005): 			  		 			     			  	   		   	  			  	
    # this is the function the autograder will call to test your code 			  		 	 		     			  	   		   	  			  	
    # NOTE: orders_file may be a string, or it may be a file object. Your 			  		 			     			  	   		   	  			  	
    # code should work correctly with either input 			  		 			     			  	   		   	  			  	
    # TODO: Your code here 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # In the template, instead of computing the value of the portfolio, we just 			  		 			     			  	   		   	  			  	
    # read in the value of IBM over 6 months 		

    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
	  		 			     			  	   		   	  			  	
    start_date = orders_df.index.min()			  		 			     			  	   		   	  			  	
    end_date = orders_df.index.max() 			  		 			     			  	   		   	  			  	
    prices = get_data(list(orders_df['Symbol'].unique()), pd.date_range(start_date, end_date))
    prices['CASH'] = 1
    trades = prices.copy()
    trades.loc[:,:] = 0.0
    
    for index, row in orders_df.iterrows():
        if row['Order'] == 'BUY':
            trades.loc[index, row['Symbol']] = trades.loc[index, row['Symbol']] + row['Shares']
            trades.loc[index, 'CASH'] = trades.loc[index, 'CASH'] - (((1+impact)*row['Shares']*prices.loc[index, row['Symbol']]) + commission)
        else:
            trades.loc[index, row['Symbol']] = trades.loc[index, row['Symbol']] - row['Shares']
            trades.loc[index, 'CASH'] = trades.loc[index, 'CASH'] + ((1-impact)*row['Shares']*prices.loc[index, row['Symbol']]) - commission
            
    holdings = trades.copy()
    holdings.loc[:,:] = 0.0
    holdings.loc[start_date, 'CASH'] = start_val*1.0
    
    for index, row in holdings.iterrows():
        if index == start_date:
            holdings.loc[index, :] = holdings.loc[index, :] + trades.loc[index, :]
            prev_index = index
        else:
            holdings.loc[index, :] = holdings.loc[prev_index, :] + trades.loc[index, :]
            prev_index = index
            
    values = holdings.copy()
    values.loc[:,:] = 0.0
    
    values = prices*holdings
    
    values = values.sum(axis=1)
    
    portvals = values 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  			  		 			     			  	   		   	  			  	
    return portvals 	

def author():
    return 'dgadidasu3'		
	  	
def test_code():
    pass 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    test_code() 			  		 			     			  	   		   	  			  	
