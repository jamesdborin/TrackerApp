#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:22:17 2020

@author: jamie
"""
from TrackerApp.InformationEditors import ExerciseIDEditor as ExID, ExercisePerformanceEditor as PerEd, WorkoutEditor as WkEd
from TracketApp.FromFile import performance_ff, workout_ff



def get_inputs(info_needed):
    info = {}
    for x in info_needed:
        i = input(f"Enter {x}: ")
        info[x] = i
    return info


def performance(s):
    """
    s is a string with the three options:
        
        1) "add" = use add_entry method
        2) "edit" = use edit_entry method
        3) "remove" = use remove_entry method
    
    """
    
    # load relevant files:
    editor = PerEd()
    if s == 'add':
        info = get_inputs(['Date', 'WorkoutID','ExerciseName', 'Performance' ])
        editor.add_entry(info)
        
    elif s == 'edit':
        info = get_inputs(['Date', 'ExerciseName', 'Performance'])
        editor.edit_entry(info)

    elif s == 'remove':
        info = get_inputs(['Date', 'ExerciseName'])
        editor.edit_entry(info)
    

def exercise(s):
    """
    s is a string with the three options:
        
        1) "add" = use add_entry method
        2) "edit" = use edit_entry method
        3) "remove" = use remove_entry method
    
    """
    # load relevant files:
    editor = ExID()
    if s == 'add':
        info = get_inputs(['ExerciseName', 'Parents'])              
        editor.add_entry(info)
        
    elif s == 'edit':
        info = get_inputs(['ExerciseName', 'NewName'])
        editor.edit_entry(info)

    elif s == 'remove':
        info = get_inputs(['ExerciseName'])        
        editor.edit_entry(info)


def workout(s):
    """
    s is a string with the three options:
        
        1) "add" = use add_entry method
        2) "edit" = use edit_entry method
        3) "remove" = use remove_entry method
    
    """
    # load relevant files:
    editor = WkEd()
    if s == 'add':
        inputs = ['ExerciseName', 'Order', 'Sets', 'Reps']
        info = get_inputs(inputs)
        
        for i in inputs:
            info[i] = info[i].split()
            
        editor.add_entry(info)
            
    elif s == 'edit':
        info = get_inputs(['WorkoutID', 'ExerciseName', 'Order'])
        editor.edit_entry(info)

    elif s == 'remove':
        info = get_inputs(['WorkoutID'])
        editor.edit_entry(info)
        

def fromfile(s):
    INPUT_INFO_SOURCE = "./stored_info/input_info/"

    if s == "w":
        editor = WkEd()
        f = workout_ff
        
    if s == "p":
        editor = PerEd()
        f = performance_ff
        
    f = input('Filename: ')
    filename = INPUT_INFO_SOURCE + f
    inputs = f(filename)
    for w in inputs:
        editor.add_entry(w)
        
