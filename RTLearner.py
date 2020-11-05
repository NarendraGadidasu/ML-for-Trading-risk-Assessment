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
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	 
			  		 			     			  	   		   	  			  	
class RTLearner(object): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
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


        def build_tree(dataX, dataY, leaf_size, depth = 0):
	    
            if dataX.shape[0] == 1:
                return np.array([-1, dataY[0], -1, -1]).reshape(1,-1)
            elif len(np.unique(dataY)) == 1:
                return np.array([-1, dataY[0], -1, -1]).reshape(1,-1)
            elif len(dataY) <= leaf_size:
                return np.array([-1, np.mean(dataY), -1, -1]).reshape(1,-1)
            else:
                dataXY = np.ones([dataX.shape[0],dataX.shape[1]+1])
                dataXY[:,0:dataX.shape[1]]=dataX
                dataXY[:,dataX.shape[1]] = dataY
		
                i = np.random.randint(0, dataX.shape[1])
                split_val = np.median(dataX[:,i])
		ls = dataXY[dataXY[:,i]<=split_val, :-1].shape[0]
		if ls == 0 or ls == dataXY.shape[0]:
			return np.array([-1, np.mean(dataXY[:, -1]), -1, -1]).reshape(1,-1)
                left_tree = build_tree(dataXY[dataXY[:,i]<=split_val, :-1], dataXY[dataXY[:,i]<=split_val, -1], leaf_size, depth+1)
                right_tree = build_tree(dataXY[dataXY[:,i]>split_val, :-1], dataXY[dataXY[:,i]>split_val, -1], leaf_size, depth+1)
                root = np.array([i, split_val, 1, len(left_tree)+1]).reshape(1,-1)
                return np.concatenate((root, left_tree, right_tree), axis=0)
        
        
	leaf_size = self.leaf_size
        
        self.tree = build_tree(dataX, dataY, leaf_size)
        
        return self.tree
 			  		 			     			  	   		   	  			  	
    def query(self,points): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Estimate a set of test points given the model we built. 			  		 			     			  	   		   	  			  	
        @param points: should be a numpy array with each row corresponding to a specific query. 			  		 			     			  	   		   	  			  	
        @returns the estimated values according to the saved model. 			  		 			     			  	   		   	  			  	
        """
        
        points_u = np.ones([points.shape[0],points.shape[1]+2])
        points_u[:,0:points.shape[1]]=points
        points_u[:,points.shape[1]] = np.arange(0, points.shape[0])
        points_u[:,-1] = 0
        
        def make_query(tr, points, i=0):
            if int(float(tr[i,0])) >=0:
		col = int(float(tr[i,0]))
		val = tr[i, 1]
		if points[col] <= val:
                	return make_query(tr, points, i+int(float(tr[i, 2])))
		else:
	                return make_query(tr, points, i+int(float(tr[i, 3])))
            else:
                points[-1] = tr[i, 1]
                return points
        

	for i in range(points_u.shape[0]):
		points_u[i] = make_query(self.tree, points_u[i])
	
        res = points_u       
        res = res[res[:,-2].argsort()]
        return res[:, -1]
 			  		 			     			  	   		   	  			  	
if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    print "the secret clue is 'zzyzx'" 			  		 			     			  	   		   	  			  	
