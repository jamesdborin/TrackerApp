#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:30:51 2020

@author: jamie
"""
from .ExerciseNetwork import ExerciseNetwork

def get_exercise_names(graph:ExerciseNetwork):
    end_nodes = []
    for node in graph.graph.nodes():
        successors_exist = len(list(graph.graph.successors(node))) > 0
        if successors_exist:
            pass
        else:
            end_nodes.append(node)
    return graph.get_labels_of_nodes(end_nodes)



