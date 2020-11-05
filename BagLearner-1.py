""" 			  		 			     			  	   		   	  			  	
A simple wrapper for linear regression.  (c) 2015 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
import numpy as np

import RTLearner as rt		  		 			     			  	   		   	 
			  		 			     			  	   		   	  			  	
class BagLearner(object): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def __init__(self, learner=rt.RTLearner, kwargs={'leaf_size' : 5}, bags = 20, boost = False, verbose = False):
        self.base_learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose			  		 			     			  	   		   	  			  	
        pass # move along, these aren't the drones you're looking for 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def author(self): 			  		 			     			  	   		   	  			  	
        return 'dgadidasu3' # replace tb34 with your Georgia Tech username 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def addEvidence(self,dataX,dataY): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Add training data to learner 			  		 			     			  	   		   	  			  	
        @param dataX: X values of data to add 			  		 			     			  	   		   	  			  	
        @param dataY: the Y training values 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        # slap on 1s column so linear regression finds a constant term 			  		 			     			  	   		   	  			  	
#        newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1]) 			  		 			     			  	   		   	  			  	
#        newdataX[:,0:dataX.shape[1]]=dataX 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  		      
        # build and save the model 	

        self.learners = []
	
    	for i in range(0,self.bags):
    		sample_temp = np.random.choice(dataX.shape[0],dataX.shape[0])
    		dataX_temp = dataX[sample_temp]
    		dataY_temp = dataY[sample_temp]
    		kwargs = self.kwargs
    		learner_temp = self.base_learner(**kwargs)
    		learner_temp.addEvidence(dataX_temp, dataY_temp)
    		self.learners.append(learner_temp)
        
        return self.learners
 			  		 			     			  	   		   	  			  	
    def query(self,points): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Estimate a set of test points given the model we built. 			  		 			     			  	   		   	  			  	
        @param points: should be a numpy array with each row corresponding to a specific query. 			  		 			     			  	   		   	  			  	
        @returns the estimated values according to the saved model. 			  		 			     			  	   		   	  			  	
        """
        res = np.zeros(points.shape[0])

    	for l in self.learners:
            res = res+l.query(points)

    	res = res/(self.bags*1.0)

        return res
 			  		 			     			  	   		   	  			  	
if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    print "the secret clue is 'zzyzx'" 			
