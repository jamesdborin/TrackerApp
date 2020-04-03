#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 13:08:40 2020

@author: jamie
"""

from TrackerApp.ExerciseNetwork import ExerciseNetwork
import pandas as pd
import networkx as nx
from TrackerApp.InformationEditors import ExerciseIdentifierCreator
n = ExerciseNetwork()

w = {
     'WorkoutID':[1,1,1,1,1,1],
     'ExerciseID':[19, 40, 32, 10, 43, 1],
     'Order':['1','2','3','4','5A','5B'],
     'Sets':[5,4,3,3,3,3],
     'Reps':['P5-10', '5/5/10/10', '10','10','10','F']
     }

work = pd.DataFrame(w)
work.to_csv("/home/jamie/TrackerApp/TrackerApp/stored_info/workouts.csv", index = False)