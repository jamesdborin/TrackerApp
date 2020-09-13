import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
from functools import partial
from TrackerApp.PlotPerformance import PlotNode
from TrackerApp.ExerciseNetwork import ExerciseNetwork
from Scripts.generate_random_performance import simulate_workout_sessions
###############################################
# Load up the relevant data from stored_info
###############################################

Ex = ExerciseNetwork()
Ex.file_to_graph("/home/jamie/personal_work/TrackerApp/TrackerApp/stored_info/first_layer_exercise_chart.txt")
AllExercises = Ex.get_exercise_names()

###############################################
# Ex.graph.nodes(data=True) produces a list:
#   [(0, {'name':ExName1}),
#    (1, {'name':ExName2}),
#    ...
#    (50, {'name':ExName50})]
###############################################   
ExerciseOptions = [{"label":n[1]['name'], "value":n[0]} for n in Ex.graph.nodes(data = True)]
ExamplePerformance = simulate_workout_sessions()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@app.callback(Output(component_id = 'ex_performance_graph', component_property = 'figure'),
             [Input(component_id = 'select_node', component_property = 'value')])
def update_performance_chart(input_node):
    
    input_label = Ex.get_labels_of_nodes([input_node])[0]
    print(f"{input_node}:{input_label}")
    return PlotNode(Label = input_label, Ex=Ex, pdf=ExamplePerformance)


app.layout = html.Div([
    
    html.H4(children='Tracker App Display'),

    html.Div([
    html.Label("Select Parent Node"),
    dcc.Dropdown(
        id = "select_node",
        options = ExerciseOptions,
        value = 0
    )
    ]),

    html.Div([

        dcc.Graph(
            id = 'ex_performance_graph'
        )

    ])



])



if __name__ == '__main__':
    app.run_server(debug=True)