""" 			  		 			     			  	   		   	  			  	
Test a learner.  (c) 2015 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
#Pass the file name of data file to run this from command line			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import math 			  		 			     			  	   		   	  			  	
import LinRegLearner as lrl 			  		 			     			  	   		   	  			  	
import sys
import util 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    if len(sys.argv) != 2: 			  		 			     			  	   		   	  			  	
        print "Usage: python testlearner.py <filename>" 			  		 			     			  	   		   	  			  	
        sys.exit(1)		  	

    if sys.argv[1] == 'Istanbul.csv':
	with util.get_learner_data_file(sys.argv[1]) as f: 			  		 			     
		data = np.genfromtxt(f,delimiter=',')
		data = data[1:,1:]
    else:
	inf = open('Data/'+sys.argv[1])
	data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()]) 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # compute how much of the data is training and testing 			  		 			     			  	   		   	  			  	
    train_rows = int(0.6* data.shape[0]) 			  		 			     			  	   		   	  			  	
    test_rows = data.shape[0] - train_rows 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # separate out training and testing data 			  		 			     			  	   		   	  			  	
    trainX = data[:train_rows,0:-1] 			  		 			     			  	   		   	  			  	
    trainY = data[:train_rows,-1] 			  		 			     			  	   		   	  			  	
    testX = data[train_rows:,0:-1] 			  		 			     			  	   		   	  			  	
    testY = data[train_rows:,-1] 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    print testX.shape 			  		 			     			  	   		   	  			  	
    print testY.shape 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # create a learner and train it 			  		 			     			  	   		   	  			  	
    learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner 			  		 			     			  	   		   	  			  	
    learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
    print learner.author() 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # evaluate in sample 			  		 			     			  	   		   	  			  	
    predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			     			  	   		   	  			  	
    print 			  		 			     			  	   		   	  			  	
    print "In sample results" 			  		 			     			  	   		   	  			  	
    print "RMSE: ", rmse 			  		 			     			  	   		   	  			  	
    c = np.corrcoef(predY, y=trainY) 			  		 			     			  	   		   	  			  	
    print "corr: ", c[0,1] 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # evaluate out of sample 			  		 			     			  	   		   	  			  	
    predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			     			  	   		   	  			  	
    print 			  		 			     			  	   		   	  			  	
    print "Out of sample results" 			  		 			     			  	   		   	  			  	
    print "RMSE: ", rmse 			  		 			     			  	   		   	  			  	
    c = np.corrcoef(predY, y=testY) 			  		 			     			  	   		   	  			  	
    print "corr: ", c[0,1] 	
	
    #experiment 1
    import DTLearner as dtl
    import matplotlib.pyplot as plt

    dt_rmse_in_sample = []
    dt_rmse_out_sample = []
    for i in range(20):	  	
        learner = dtl.DTLearner(leaf_size = i, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
	dt_rmse_in_sample.append(rmse)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
	dt_rmse_out_sample.append(rmse)
    
    dt_rmse_in_sample = np.array(dt_rmse_in_sample)
    dt_rmse_out_sample = np.array(dt_rmse_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), dt_rmse_in_sample, label = 'DT_in_sample_RMSE')
    plt.plot(np.arange(1,21), dt_rmse_out_sample, label = 'DT_out_of_sample_RMSE')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('RMSE')
    plt.legend(loc='lower right')
    plt.savefig('exp1_DecisionTree.png')
    plt.clf()

    #experiment 2
    import BagLearner as bl

    bl_rmse_in_sample = []
    bl_rmse_out_sample = []
    for i in range(20):
	kwargs_i = {'leaf_size':i, 'verbose':False}	  	
        learner = bl.BagLearner(dtl.DTLearner, kwargs = kwargs_i, bags = 20, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
	bl_rmse_in_sample.append(rmse)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
	bl_rmse_out_sample.append(rmse)
    
    bl_rmse_in_sample = np.array(bl_rmse_in_sample)
    bl_rmse_out_sample = np.array(bl_rmse_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), bl_rmse_in_sample, label = 'Bagging_in_sample_RMSE')
    plt.plot(np.arange(1,21), bl_rmse_out_sample, label = 'Bagging_out_of_sample_RMSE')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('RMSE')
    plt.legend(loc='lower right')
    plt.savefig('exp2_Bagging.png')
    plt.clf()

    #experiment 3
    import DTLearner as dtl
    import matplotlib.pyplot as plt

    dt_r_squared_in_sample = []
    dt_r_squared_out_sample = []
    for i in range(20):	  	
        learner = dtl.DTLearner(leaf_size = i, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	r_squared = 1-(((trainY - predY) ** 2).sum()/((trainY - np.mean(trainY)) ** 2).sum())
	dt_r_squared_in_sample.append(r_squared)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	r_squared = 1-(((testY - predY) ** 2).sum()/((testY - np.mean(testY)) ** 2).sum())
	dt_r_squared_out_sample.append(r_squared)
    
    dt_r_squared_in_sample = np.array(dt_r_squared_in_sample)
    dt_r_squared_out_sample = np.array(dt_r_squared_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), dt_r_squared_in_sample, label = 'DT_in_sample_R_Squared')
    plt.plot(np.arange(1,21), dt_r_squared_out_sample, label = 'DT_out_of_sample_R_Squared')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('R_Squared')
    plt.legend(loc='lower right')
    plt.savefig('exp3_DecisionTree.png')
    plt.clf()

    #experiment 4

    import BagLearner as bl

    bl_r_squared_in_sample = []
    bl_r_squared_out_sample = []
    for i in range(20):
	kwargs_i = {'leaf_size':i, 'verbose':False}	  	
        learner = bl.BagLearner(dtl.DTLearner, kwargs = kwargs_i, bags = 20, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	r_squared = 1-(((trainY - predY) ** 2).sum()/((trainY - np.mean(trainY)) ** 2).sum())
	bl_r_squared_in_sample.append(r_squared)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	r_squared = 1-(((testY - predY) ** 2).sum()/((testY - np.mean(testY)) ** 2).sum())
	bl_r_squared_out_sample.append(r_squared)
    
    bl_r_squared_in_sample = np.array(bl_r_squared_in_sample)
    bl_r_squared_out_sample = np.array(bl_r_squared_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), bl_r_squared_in_sample, label = 'Bagging_in_sample_R_Squared')
    plt.plot(np.arange(1,21), bl_r_squared_out_sample, label = 'Bagging_out_of_sample_R_Squared')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('R_Squared')
    plt.legend(loc='upper right')
    plt.savefig('exp4_Bagging.png')
    plt.clf()

 #experiment 5
    import DTLearner as dtl
    import matplotlib.pyplot as plt

    dt_mmre_in_sample = []
    dt_mmre_out_sample = []
    for i in range(20):	  	
        learner = dtl.DTLearner(leaf_size = i, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mmre = (np.abs(trainY - predY)/trainY).sum()
	dt_mmre_in_sample.append(mmre)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mmre = (np.abs(testY - predY)/testY).sum()
	dt_mmre_out_sample.append(mmre)
    
    dt_mmre_in_sample = np.array(dt_mmre_in_sample)
    dt_mmre_out_sample = np.array(dt_mmre_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), dt_mmre_in_sample, label = 'DT_in_sample_MMRE')
    plt.plot(np.arange(1,21), dt_mmre_out_sample, label = 'DT_out_of_sample_MMRE')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('MMRE')
    plt.legend(loc='upper right')
    plt.savefig('exp5_DecisionTree.png')
    plt.clf()

    #experiment 6

    import BagLearner as bl

    bl_mmre_in_sample = []
    bl_mmre_out_sample = []
    for i in range(20):
	kwargs_i = {'leaf_size':i, 'verbose':False}	  	
        learner = bl.BagLearner(dtl.DTLearner, kwargs = kwargs_i, bags = 20, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mmre = (np.abs(trainY - predY)/trainY).sum()
	bl_mmre_in_sample.append(mmre)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mmre = (np.abs(testY - predY)/testY).sum()
	bl_mmre_out_sample.append(mmre)
    
    bl_mmre_in_sample = np.array(bl_mmre_in_sample)
    bl_mmre_out_sample = np.array(bl_mmre_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), bl_mmre_in_sample, label = 'Bagging_in_sample_MMRE')
    plt.plot(np.arange(1,21), bl_mmre_out_sample, label = 'Bagging_out_of_sample_MMRE')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('MMRE')
    plt.legend(loc='upper right')
    plt.savefig('exp6_Bagging.png')
    plt.clf()	

 #experiment 5
    import DTLearner as dtl
    import matplotlib.pyplot as plt

    dt_mmre_in_sample = []
    dt_mmre_out_sample = []
    for i in range(20):	  	
        learner = dtl.DTLearner(leaf_size = i, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mmre = (np.abs(trainY - predY)/trainY).sum()
	dt_mmre_in_sample.append(mmre)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mmre = (np.abs(testY - predY)/testY).sum()
	dt_mmre_out_sample.append(mmre)
    
    dt_mmre_in_sample = np.array(dt_mmre_in_sample)
    dt_mmre_out_sample = np.array(dt_mmre_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), dt_mmre_in_sample, label = 'DT_in_sample_MMRE')
    plt.plot(np.arange(1,21), dt_mmre_out_sample, label = 'DT_out_of_sample_MMRE')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('MMRE')
    plt.legend(loc='upper right')
    plt.savefig('exp5_DecisionTree.png')
    plt.clf()

    #experiment 6

    import BagLearner as bl

    bl_mmre_in_sample = []
    bl_mmre_out_sample = []
    for i in range(20):
	kwargs_i = {'leaf_size':i, 'verbose':False}	  	
        learner = bl.BagLearner(dtl.DTLearner, kwargs = kwargs_i, bags = 20, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mmre = (np.abs(trainY - predY)/trainY).sum()
	bl_mmre_in_sample.append(mmre)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mmre = (np.abs(testY - predY)/testY).sum()
	bl_mmre_out_sample.append(mmre)
    
    bl_mmre_in_sample = np.array(bl_mmre_in_sample)
    bl_mmre_out_sample = np.array(bl_mmre_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), bl_mmre_in_sample, label = 'Bagging_in_sample_MMRE')
    plt.plot(np.arange(1,21), bl_mmre_out_sample, label = 'Bagging_out_of_sample_MMRE')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('MMRE')
    plt.legend(loc='upper right')
    plt.savefig('exp6_Bagging.png')
    plt.clf()	 
    			  	   		   	  			  	 	
    #experiment 7
    import DTLearner as dtl
    import matplotlib.pyplot as plt

    dt_mae_in_sample = []
    dt_mae_out_sample = []
    for i in range(20):	  	
        learner = dtl.DTLearner(leaf_size = i, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mae = (np.abs(trainY - predY)).sum()/trainY.shape[0]
	dt_mae_in_sample.append(mae)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mae = (np.abs(testY - predY)).sum()/testY.shape[0]
	dt_mae_out_sample.append(mae)
    
    dt_mae_in_sample = np.array(dt_mae_in_sample)
    dt_mae_out_sample = np.array(dt_mae_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), dt_mae_in_sample, label = 'DT_in_sample_MAE')
    plt.plot(np.arange(1,21), dt_mae_out_sample, label = 'DT_out_of_sample_MAE')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('MAE')
    plt.legend(loc='lower right')
    plt.savefig('exp7_DecisionTree.png')
    plt.clf()

    #experiment 2
    import BagLearner as bl

    bl_mae_in_sample = []
    bl_mae_out_sample = []
    for i in range(20):
	kwargs_i = {'leaf_size':i, 'verbose':False}	  	
        learner = bl.BagLearner(dtl.DTLearner, kwargs = kwargs_i, bags = 20, verbose = False) 			  	
        learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
	# evaluate in sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mae = (np.abs(trainY - predY)).sum()/trainY.shape[0]
	bl_mae_in_sample.append(mae)
				  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# evaluate out of sample 			  		 			     			  	   		   	  			  	
    	predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    	mae = (np.abs(testY - predY)).sum()/testY.shape[0]
	bl_mae_out_sample.append(mae)
    
    bl_mae_in_sample = np.array(bl_mae_in_sample)
    bl_mae_out_sample = np.array(bl_mae_out_sample)
    plt.clf()
    plt.figure()	
    plt.plot(np.arange(1,21), bl_mae_in_sample, label = 'Bagging_in_sample_MAE')
    plt.plot(np.arange(1,21), bl_mae_out_sample, label = 'Bagging_out_of_sample_MAE')
    plt.xlabel('No of Leaves')
    plt.xticks(np.arange(0,21,step=2))
    plt.ylabel('MAE')
    plt.legend(loc='lower right')
    plt.savefig('exp8_Bagging.png')
    plt.clf()
		  		 			     			  	   		   	  			 
