"""Assess a betting strategy. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
Student Name: Tucker Balch (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: dgadidasu3 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903457715 (replace with your GT ID) 			  		 			     			  	   		   	  			  	
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def author():		  		 			     			  	   		   	  			  	
        return 'dgadidasu3' # replace tb34 with your Georgia Tech username. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def gtid(): 			  		 			     			  	   		   	  			  	
	return 903457715 # replace with your GT ID number 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def get_spin_result(win_prob):	  			  	
	result = False   		   	  			  	
	if np.random.random() <= win_prob: 			  		 			     			  	   		   	  			  	
		result = True 			  		 			     			  	   		   	  			  	
	return result 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
#def test_code(): 			  		 			     			  	   		   	  			  	
#	win_prob = 0.60 # set appropriately to the probability of a win 			  		 			     			  	   		   	  			  	
#	np.random.seed(gtid()) # do this only once
#    #create_plots() 			  		 			     			  	   		   	  			  	
#	create_plots() print get_spin_result(win_prob) # test the roulette spin 	  		 			     			  	   		   	  			  	
# 			  		 			     			  	   		   	  			  	
#	# add your code here to implement the experiments

def test_code():
    win_prob = 0.47 # set appropriately to the probability of a win
    np.random.seed(gtid()) # do this only once
    create_plots()
    print get_spin_result(win_prob) # test the roulette spin
    
    # add your code here to implement the experiments

win_prob = 0.47

def experiment1(runs):
    winnings_e1 = np.zeros((runs,1001))
    
    for i in range(runs):
        episode_winnings = 0
        j = 0
        winnings_e1[i,0] = 0
        while episode_winnings < 80:
            won = False
            bet_amount = 1
            while not won:
                won = get_spin_result(win_prob)
                j = j+1
                if won == True:
                    episode_winnings = episode_winnings+bet_amount
                    winnings_e1[i,j] = episode_winnings
                else:
                    episode_winnings = episode_winnings-bet_amount
                    winnings_e1[i,j] = episode_winnings
                    bet_amount = bet_amount*2
        while j<1000:
            j = j+1
            winnings_e1[i,j] = 80
    return winnings_e1

def experiment2(runs):
    winnings_e2 = np.zeros((runs,1001))
    
    for i in range(runs):
        episode_winnings = 0
        j = 0
        winnings_e2[i,0] = 0
        while episode_winnings < 80 and episode_winnings > -256:
            won = False
            bet_amount = 1
            while not won and episode_winnings > -256:
                won = get_spin_result(win_prob)
                j = j+1
                if won == True:
                    episode_winnings = episode_winnings+bet_amount
                    winnings_e2[i,j] = episode_winnings
                else:
                    episode_winnings = episode_winnings-bet_amount
                    winnings_e2[i,j] = episode_winnings
                    if episode_winnings+256 >= bet_amount*2:
                        bet_amount = bet_amount*2
                    else:
                        bet_amount = episode_winnings+256
        while j<1000:
            j = j+1
            if episode_winnings >= 80:
                winnings_e2[i,j] = 80
            else:
                winnings_e2[i,j] = -256
    return winnings_e2

def create_plots():
    
    import matplotlib.pyplot as plt  
    
    e1_f1 = experiment1(10)
    
    plt.close()
    plt.figure()
    for i in range(10):
        plt.plot(e1_f1[i,:], label = 'sumulation_'+str(i+1))
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.title('e1_f1')
    plt.legend(loc = 'lower right')
    plt.xlabel('spins')
    plt.ylabel('episode_winnings')
    plt.savefig('e1_f1.png')
    plt.close()
    
    e1_f2_f3 = experiment1(1000)
    e1_f2_f3_mean = e1_f2_f3.mean(axis=0)
    e1_f2_f3_median = np.median(e1_f2_f3,axis=0)
    e1_f2_f3_std = e1_f2_f3.std(axis=0)
    
    plt.close()
    plt.figure()
    plt.plot(e1_f2_f3_mean, label = 'mean')
    plt.plot(e1_f2_f3_mean-e1_f2_f3_std, label = 'mean - std')
    plt.plot(e1_f2_f3_mean+e1_f2_f3_std, label = 'mean + std')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.title('e1_f2')
    plt.legend(loc = 'lower right')
    plt.xlabel('spins')
    plt.ylabel('episode_winnings')
    plt.savefig('e1_f2.png')
    plt.close()
    
    plt.close()
    plt.figure()
    plt.plot(e1_f2_f3_median, label = 'median')
    plt.plot(e1_f2_f3_median-e1_f2_f3_std, label = 'median - std')
    plt.plot(e1_f2_f3_median+e1_f2_f3_std, label = 'median + std')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.title('e1_f3')
    plt.legend(loc = 'lower right')
    plt.xlabel('spins')
    plt.ylabel('episode_winnings')
    plt.savefig('e1_f3.png')
    plt.close()
    
    e2_f4_f5 = experiment2(1000)
    e2_f4_f5_mean = e2_f4_f5.mean(axis=0)
    e2_f4_f5_median = np.median(e2_f4_f5,axis=0)
    e2_f4_f5_std = e2_f4_f5.std(axis=0)
    
    plt.close()
    plt.figure()
    plt.plot(e2_f4_f5_mean, label = 'mean')
    plt.plot(e2_f4_f5_mean-e2_f4_f5_std, label = 'mean - std')
    plt.plot(e2_f4_f5_mean+e2_f4_f5_std, label = 'mean + std')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.title('e2_f4')
    plt.legend(loc = 'lower left')
    plt.xlabel('spins')
    plt.ylabel('episode_winnings')
    plt.savefig('e2_f4.png')
    plt.close()
    
    plt.close()
    plt.figure()
    plt.plot(e2_f4_f5_median, label = 'median')
    plt.plot(e2_f4_f5_median-e2_f4_f5_std, label = 'median - std')
    plt.plot(e2_f4_f5_median+e2_f4_f5_std, label = 'median + std')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.title('e2_f5')
    plt.legend(loc = 'lower right')
    plt.xlabel('spins')
    plt.ylabel('episode_winnings')
    plt.savefig('e2_f5.png')
    plt.close()
      		 			    			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    test_code() 			  		 			     			  	   		   	  			  	