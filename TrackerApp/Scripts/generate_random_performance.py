#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 15:34:21 2020

@author: jamie
"""
# %%
import plotly.graph_objects as go
import TrackerApp.ExerciseNetwork as TA
import importlib
import pandas as pd
from random import choices
from datetime import datetime, timedelta
import numpy as np

# %%
# Load the stored values
exercises = pd.read_csv(
    "/home/jamie/personal_work/TrackerApp/TrackerApp/stored_info/exercise_db_v1.csv")
performance = pd.DataFrame({"Date": [], "ExerciseID": [], "Performance": []})


# %%
# Simulate a session:
strength = 1
DATE = datetime(2020, 8, 25)
DAYS = 150
OneDay = timedelta(days=1)

for day in range(DAYS):
    do_workout = np.random.randint(0, 7) < 3
    if not do_workout:
        DATE += OneDay

    if do_workout:
        SessionExercises = np.random.choice(np.array(range(70, 100)), 5, False)
        for e in SessionExercises:
            reps = np.random.randint(5, 10, size=4)
            weight = np.random.randint(20, 40, size=4)*strength
            perf = ",".join([f"{a}@{b}" for a, b in zip(reps, weight)])
            performance = performance.append(
                {"Date": DATE, "ExerciseID": e, "Performance": perf}, ignore_index=True)

            update_strength = np.random.randint(0, 10) > 9
            if update_strength:
                strength += 0.1

            DATE += OneDay

print(performance)

# %%
# calculate volume of a given exercise performance
test_perf = np.array(performance.Performance)[0]


def VolumeFromPerf(perf_str):
    sets = perf_str.split(",")  # split into sets
    # split each set into reps and weight
    reps_and_weights = [s.split("@") for s in sets]
    # calc volume for each set and sum
    volume = sum(map(lambda x: int(x[0]) * int(x[1]), reps_and_weights))
    return volume


print(test_perf)
print(VolumeFromPerf(test_perf))
# %%
# load up exercise network

importlib.reload(TA)


EX = TA.ExerciseNetwork()
EX.file_to_graph(
    "/home/jamie/personal_work/TrackerApp/TrackerApp/stored_info/first_layer_exercise_chart.txt")

# %%
# get volume of all child nodes of a given node across all dates

label = "Back"
child_nodes = EX.get_children_of(label)
descendant_nodes = EX.get_descendants_of(label)
print(descendant_nodes)
nodes = EX.get_labels_of_nodes(descendant_nodes)
print(nodes)


def iso_to_date(y,w):
    """
    Take a date specified by the year and week number and return the Monday of that week
    """
    d = f"{y}-W{w}"
    return datetime.strptime(d+"-1", "%Y-W%W-%w")

def DescendantVolume(df, descendants):
    """
    For the descendants of an exercise return the volume of each of those exercises
    """
    df_desc = df.loc[df["ExerciseID"].isin(descendants)]
    df_desc["Volume"] = np.vectorize(VolumeFromPerf)(df_desc["Performance"])
    return df_desc

perf_group = DescendantVolume(performance, descendant_nodes)
child_dfs = [DescendantVolume(performance, EX.get_descendants_of(c)) for c in child_nodes[1]]

def VolumeTotals(df):
    """
    Sum the weekly volume of a node's descendants
    """
    df["Week"] = df["Date"].dt.week
    df["Year"] = df["Date"].dt.year

    df = df.groupby(["Year", "Week"])["Volume"].sum().reset_index()

    df["Date"] = df.apply(lambda x: iso_to_date(x["Year"], x["Week"]),axis = 1)
    return df

perf_total = VolumeTotals(perf_group)
child_totals = [VolumeTotals(c) for c in child_dfs]
# %%
# Plot this volume in a fill chart using plotly

fig = go.Figure()

i = 0
y = np.array([0]*len(child_totals[0]["Volume"]))
for c, name in zip(child_totals, child_nodes[1]):
    if i == 0:
        fill_to = "tozeroy"
    else:
        fill_to = "tonexty"

    fig.add_trace(go.Scatter(
        x = c["Date"],
        y = c["Volume"],
        stackgroup = "one",
        fill = fill_to,
        hoveron = "fills+points",
        text = name + " Volume",
        hoverinfo = "text+x+y",
        name = name
    ))

    i+=1

fig.update_layout(hovermode = 'x unified')
fig.show()


