""" 			  		 			     			  	   		   	  			  	
Template for implementing QLearner  (c) 2015 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
import random as rand 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
class QLearner(object):

    def author(self):
        return 'dgadidasu3'
			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 200, \
        verbose = False): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
         			  					     			  	   		   	  			  	
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.verbose = verbose		 			     			  	   		   	  			  	
        self.s = 0 			  		 			     			  	   		   	  			  	
        self.a = 0

        self.Q = np.zeros([num_states,num_actions]).tolist()
        self.E = []
                
 			  		 			     			  	   		   	  			  	
    def querysetstate(self, s): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Update the state without updating the Q-table 			  		 			     			  	   		   	  			  	
        @param s: The new state 			  		 			     			  	   		   	  			  	
        @returns: The selected action
        set s to s
        roll the dice to decide if you need to take random action or not
        if random action, choose the randome action and update a with that 	
        if not randome action go to the Q-table and find which action has maximum q value and choose that action and update a accordingly
        return a		  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        self.s = s
        
        if rand.uniform(0.0, 1.0)<=self.rar:
    	 	action = rand.randint(0, self.num_actions-1)
        else:
            action = self.Q[self.s].index(max(self.Q[self.s]))
        
        self.a = action

        return action 			  		 			     	 		  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def query(self,s_prime,r): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Update the Q table and return an action 			  		 			     			  	   		   	  			  	
        @param s_prime: The new state 			  		 			     			  	   		   	  			  	
        @param r: The ne state 			  		 			     			  	   		   	  			  	
        @returns: The selected action 
        update the q table with tuple <s, a, sprime, r>			  		 			     			  	   		   	  			  	
        q(s,a) = (1-alpha)*q(s,a) + alpha*(immrew + gamma*futurereward)
        roll the dice to decide if you need to take random action or not
        if random action, choose the randome action and update a with that
        update rar = rar*radr
        if not randome action go to the Q-table and find which action has maximum q value and choose that action and update a accordingly
        set s to sprime
        return a
        location is column ties 10 plus the row
        """ 	
        
        if rand.uniform(0.0, 1.0)<=self.rar:
    	 	action = rand.randint(0, self.num_actions-1)
        else:
            action = self.Q[s_prime].index(max(self.Q[s_prime]))

        		  		 			     			  	   		   	  			  	
        self.Q[self.s][self.a] = ((1-self.alpha)*self.Q[self.s][self.a])+self.alpha*(r+((self.gamma)*(self.Q[s_prime][action])))
        
        self.E.append([self.s, self.a, s_prime, r])
        
        dyna = self.dyna
        
        while dyna>0:
            i  = rand.randint(0, len(self.E)-1)
            n = self.E[i]
            act = self.Q[n[2]].index(max(self.Q[n[2]]))
            self.Q[n[0]][n[1]] = ((1-self.alpha)*self.Q[n[0]][n[1]])+self.alpha*(n[3]+((self.gamma)*(self.Q[n[2]][act])))
            dyna = dyna-1
        
        
        self.rar = self.rar*self.radr

        self.s = s_prime
        self.a = action	  
		 			     			  	   		   	  			  	
        return action		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    print "Remember Q from Star Trek? Well, this isn't him" 			  		 			     			  	   		   	  			  	
