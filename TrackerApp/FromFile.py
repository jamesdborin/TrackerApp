#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:08:58 2020

@author: jamie
"""        
def performance_ff(filename):
    """
    Function to take a filename and return the performance of a 
    given workout.
    """
    results = []       
    with open(filename) as f:
        lines = f.readlines()
        
        info = {'ExerciseName':[], 'Performance':[]}
        j = 0
        for line in lines:
            l = line.split()
            if j == 0: info['Date'] = l;
            
            elif j == 1: info['WorkoutID'] = l;
            
            elif line == '\n': 
                j = 0
                results.append(info)
                info = {'ExerciseName':[], 'Performance':[]}
                continue
            
            else:
                info['ExerciseName'].append(l[0])
                info['Performance'].append(l[1])
            j+=1
    
    return results

def workout_ff(filename):
    """
    Function to take a file and return the workouts designed in the file
    """
    results = []
    with open(filename) as f:
        lines = f.readlines()
        info = {'ExerciseName':[], 'Order':[], 'Sets':[], 'Reps':[]}
        j = 0
        for line in lines:
            l = line.split()
            if j == 0: info ['WorkoutID'] = l;
                
            elif line == '\n':
                j = 0
                results.append(info)
                info = {'ExerciseName':[], 'Order':[], 'Sets':[], 'Reps':[]}
                continue
            
            else:
                info['ExerciseName'].append(l[0])
                info['Order'].append(l[1])
                info['Sets'].append(l[2])
                info['Reps'].append(l[3])
    
    return results 


         