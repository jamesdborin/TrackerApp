#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 15:34:21 2020

@author: jamie
"""
# %%
import plotly.graph_objects as go
import TrackerApp.ExerciseNetwork as TA
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# %%
# Simulate a session:

def simulate_workout_sessions(num_days = 150, 
                              strength_growth = 0.5, 
                              ex_range = (70,100)):

    performance = pd.DataFrame({"Date": [], "ExerciseID": [], "Performance": []})

    strength = 1
    DATE = datetime(2020, 8, 25)
    DAYS = num_days
    OneDay = timedelta(days=1)

    for _ in range(DAYS):
        do_workout = np.random.randint(0, 7) < 3
        if not do_workout:
            DATE += OneDay

        if do_workout:
            SessionExercises = np.random.choice(np.array(range(ex_range[0], ex_range[1])), 5, False)
            for e in SessionExercises:
                reps = np.round(np.random.randn(4) + 8,0)
                weight = np.round(1*np.random.randn(4) + (30*strength),1)
                perf = ",".join([f"{a}@{b}" for a, b in zip(reps, weight)])
                performance = performance.append(
                    {"Date": DATE, "ExerciseID": e, "Performance": perf}, ignore_index=True)

                update_strength = np.random.randint(0, 10) > 9
                if update_strength:
                    strength += strength_growth

                DATE += OneDay

    return performance
