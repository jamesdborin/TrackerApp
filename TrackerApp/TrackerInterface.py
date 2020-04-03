#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:00:10 2020

@author: jamie
"""
import cmd
from TrackerApp.CommandLineFunctions import performance, exercise, workout, fromfile

class ProgressTracker(cmd.Cmd):
    
    intro = 'Welcome to the ProgressTracker shell.   Type help or ? to list commands.\n'
    prompt = '(proTrack) '

    def do_performance(self, arg):
        "Record, Edit, and Delete exercise performances"
        performance(arg)
        
    def do_workout(self, arg):
        "Record, Edit, and Delete workouts"
        workout(arg)
        
    def do_exercise(self, arg):
        "Record, Edit, and Delete individual exercises"
        exercise(arg)
    
    def do_bye(self, arg):
        print("Thank you for using ProTracker")
        return True
    
    def do_fromfile(self, arg):
        "Save progress ro a new workout from a text file"
        fromfile(arg)
    
    
if __name__ =="__main__":
    ProgressTracker().cmdloop()