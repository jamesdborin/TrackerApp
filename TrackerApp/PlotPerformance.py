import plotly.graph_objects as go
import TrackerApp.ExerciseNetwork as TA
import importlib
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import sys
from Scripts.generate_random_performance import simulate_workout_sessions
from importlib import reload
reload(TA)

def iso_to_date(y,w):
    """
    Take a date specified by the year and week number and return the Monday of that week
    """
    d = f"{y}-W{w}"
    return datetime.strptime(d+"-1", "%Y-W%W-%w")


def VolumeFromPerf(perf_str):
    """
    Give the volume of a performance string
    """
    sets = perf_str.split(",")  # split into sets
    # split each set into reps and weight
    reps_and_weights = [s.split("@") for s in sets]
    # calc volume for each set and sum
    volume = sum(map(lambda x: np.round(float(x[0]),1) * np.round(float(x[1]),1), reps_and_weights))
    return float(volume)


def PlotChildPerformance(child_totals, child_names):
    """
    Plot a stacked area chart for the weekly volume totals of the children of a given node.

    Inputs:

    *child_totals*: Pandas.DataFrame object containing the total weekly volume scores of all children
    of a given node.

    *child_nodes*: The names and node numbers of the children nodes
    """

    fig = go.Figure()

    for c, name in zip(child_totals, child_names):
        fig.add_trace(go.Scatter(
            x = c["Date"],
            y = c["Volume"],
            stackgroup = "one",
            fill = "tonexty",
            hoveron = "fills+points",
            text = name + " Volume",
            hoverinfo = "text+x+y",
            name = name
        ))

    fig.update_layout(
        hovermode = 'x unified',
        xaxis_title = "Date",
        yaxis_title = "Weekly Volume (kgs)")

    return fig


def all_dates(df):
    """
    produce all daily dates between the start and end date in a dataframe
    """
    start_date = df.Date.min()
    end_date = df.Date.max()
    delta = (end_date - start_date).days
    all_dates = [start_date + n*timedelta(days=1) for n in range(delta)]
    all_dates_df = pd.DataFrame({"Date":all_dates})
    return all_dates_df

def WeekylPerformanceOfNodes(performance_df, nodes):
    """
    Input: noeds: List of node numbers. 
    Sum the weekly volume of each node in nodes and present this on all 
    weeks to be plotted
    """


    # select just the node numbers in nodes
    perf_df = performance_df.loc[performance_df["ExerciseID"].isin(nodes)]

    # check if there are any entries. If there are none then return the all 0s for all dates.
    noEntries = len(perf_df) == 0
    # if there are no entries set the plot_df to the all zeros all_dates_df, then
    #   use this to gorup and sum over week so formatting still works.
    if noEntries:
        all_dates_df = all_dates(performance_df)

        plot_df = all_dates_df
        plot_df["Volume"] = [0]*len(plot_df)
        plot_df["Week"] = plot_df["Date"].dt.week
        plot_df["Year"] = plot_df["Date"].dt.year

        plot_df = plot_df.groupby(by = ["Year", "Week"]).sum().reset_index()

        plot_df["Date"] = np.vectorize(iso_to_date)(plot_df["Year"], plot_df["Week"])
        return plot_df

    # calculate the volumes of these exercises
    perf_df["Volume"] = np.vectorize(VolumeFromPerf)(perf_df["Performance"])
    
    # merge with all dates in the range to get all possible weeks
    all_dates_df = all_dates(perf_df)
    plot_df = all_dates_df.merge(perf_df, how = "left", on = "Date")

    # Group on the weeks and months and then sum
    plot_df["Week"] = plot_df["Date"].dt.week
    plot_df["Year"] = plot_df["Date"].dt.year

    plot_df = plot_df.groupby(by = ["Year", "Week"]).sum().reset_index()

    # Set the date to the monday of each week
    plot_df["Date"] = np.vectorize(iso_to_date)(plot_df["Year"], plot_df["Week"])
    return plot_df


def PlotNode(pdf, Ex, Label):
    """
    inputs; 
    *pdf*: A DataFrame object with the performances on given dates of all exercises
    *Ex*: Exercise network graph
    *Label*: 
    """
    isLeaf = Ex.is_leaf_node(Label)
    label_node = Ex.get_nodes_of_labels([Label])
    
    if isLeaf:
        # get the summed volume for that single exercise
        plot_df = WeekylPerformanceOfNodes(pdf, label_node)

        # plot this weekly volume total
        fig = PlotChildPerformance([plot_df], [Label])
        
        return fig

    else:
        # find the child nodes of the target label. There are what we are going to be plotting.
        _, child_names = Ex.get_children_of(Label)
        
        # For each of these nodes we want to get all of their descendants
        descendant_nodes = [Ex.get_descendants_of(name) for name in child_names]
        
        # Create dataframes for each of the sets of descendatn nodes
        descendant_dfs = [WeekylPerformanceOfNodes(pdf, d) for d in descendant_nodes]

        fig = PlotChildPerformance(descendant_dfs, child_names)
        
        return fig


if __name__ == "__main__":
    """
    What we want is that when a label is provided, 
        if the label is a root node then we just plot the volume of this exercise.
    Otherwise we calculate the descendatn volume of each of the direct children, and plot these.
    """

    Label = "Retro Dips"
    Ex = TA.ExerciseNetwork()
    Ex.file_to_graph("/home/jamie/personal_work/TrackerApp/TrackerApp/stored_info/first_layer_exercise_chart.txt")
    pdf = simulate_workout_sessions()
    
    fig = PlotNode(pdf, Ex, Label)
    fig.show()
        