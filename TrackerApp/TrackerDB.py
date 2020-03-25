#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from TrackerApp.ExerciseNetwork import ExerciseNetwork
import pandas as pd
from TrackerApp.Utils import get_exercise_names
file = 'stored_info/first_layer_exercise_chart.txt'
graph_db = ExerciseNetwork()
graph_db.file_to_graph(file)
graph_db.draw_graph()

node_names = get_exercise_names(graph_db)
ExerciseIDs = pd.DataFrame({'ExerciseID':range(len(node_names)), 'ExerciseName':node_names})

