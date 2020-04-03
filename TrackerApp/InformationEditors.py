#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from TrackerApp.ExerciseNetwork import ExerciseNetwork
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict

class DFBuilder(ABC):
    
    @abstractmethod
    def create_df(self, input_data):
        pass


class DFEditor(ABC):
    """
    Parent class for all classes that have the capability to build and alter
    DataFrames.
    """
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv(self.filename)
        self.graph = ExerciseNetwork()
        self.graphfile = "/home/jamie/TrackerApp/TrackerApp/stored_info/first_layer_exercise_chart.txt"
        self.graph.file_to_graph(self.graphfile)
    
    def save_df(self):
        self.df.to_csv(self.filename)
    
    @staticmethod
    def get_id_from_name(df, info):
        return df[df['ExerciseName'] == info['ExerciseName']]['ExerciseID']

        
    @abstractmethod
    def add_entry(self, df:pd.DataFrame, info):
        pass
    
    @abstractmethod
    def remove_entry(self, df:pd.DataFrame, info):
        pass
    
    @abstractmethod
    def edit_entry(self, df:pd.DataFrame, info):
        pass
    

class ExerciseIdentifierCreator(DFBuilder):
    
    def create_df(self, input_data):
        """
        Creates an ExerciseID df from a graph file
        """
        graph_db = ExerciseNetwork()
        graph_db.file_to_graph(input_data)
    
        node_names = graph_db.get_exercise_names()
        df = pd.DataFrame({'ExerciseID':range(len(node_names)), 
                           'ExerciseName':node_names})
        
        return df
    
    def save_df(self, input_graph, output_df):
        df = self.create_df(input_graph)
        df.to_csv(output_df, index = False)
        
        
class ExerciseIDEditor(DFEditor):
    """
    Class that will add, remove and edit exercise names.
    """
    def __init__(self):
        f = "./stored_info/exercise_db_example.csv"
        super().__init__(filename = f)
            
    def add_entry(self, info:Dict):
        """
        *df:* pandas DataFrame which will have an entry added
        *info:* Dict with keys ['ExerciseName', 'Parents']
        """
        
        new_index = self.df['ExerciseID'].max() + 1
        self.df = self.df.append({'ExerciseID':new_index, 'ExerciseName' :info['ExerciseName']}, 
                       ignore_index = True)
        
        self.save_df()
        
        parents = info['Parents'].split()
        self.graph.add_branches([info['ExerciseName']*len(parents), parents])
        self.graph.graph_to_file(self.graphfile)
        
    
    def remove_entry(self, info:Dict):
        """
        *df:* pandas DataFrame which will have an entry added
        *info:* Dict with keys ['ExerciseName']
        """
        
        self.df = self.df[self.df['ExerciseName'] != info['ExerciseName']]
        self.save_df()
    
    def edit_entry(self, info:Dict):
        """
        *df:* pandas DataFrame which will have an entry edited
        *info:* dictionary with ExerciseName and NewName keys
        """
                
        self.df.loc[self.df['ExerciseName'] == info['ExerciseName'], ['ExerciseName']] = info['NewName'] 
        self.save_df()
    
class ExercisePerformanceEditor(DFEditor):
    """
    Class that will add and edit data about performance about exercises
    """
    
    def __init__(self):
        f = "./stored_info/performance_db_example.csv"
        super().__init__(filename = f)
        self.alt_filename = "./stored_info/exercise_db_example.csv"
        self.id_df = pd.read_csv(self.alt_filename)
        
    def string_to_volume(self, st):
        """
        Take a string of the form:
            w1@r1,w2@r2, ... into a volume w1*r1 + w2*r2 ...
        """
        split_string = map(lambda s: s.split('@'), st.split(',')) 
        # Produce a list within lists as follows:
            # r1@w1,r2@w2 -> [['r1','w1'], ['r2','w2'], ... ]
            
        prod_sum = sum(map( lambda z: int(z[0]) * int(z[1]), split_string))
        # For each element multiply the rep by the weight and sum together 
        # to get volume
        
        return prod_sum
    
    def add_entry(self, info:Dict):
        """
        *df*: dataframe to append to
        *info*: dict with keys: 'Date', 'WorkoutID',
                "ExerciseName", "Performance" 
        """
        info['ExerciseID'] = self.get_id_from_name(self.id_df, info)
        info['Volume'] = self.string_to_volume(info['Performance'])
        self.df = self.df.append(info, ignore_index=True)
        
        self.save_df()
        
    
    def remove_entry(self, df:pd.DataFrame, info:Dict):
        """
        remove an entry by specifying the ExerciseID and the date
        
        *info*: Dict with keys 'ExerciseName' and 'Date'
        """
        
        info['ExerciseID'] = self.get_id_from_name(self.id_df, info)
        self.df = self.df[(self.df['ExerciseID'] != info['ExerciseID']) & 
                (self.df['Date'] != info['Date'])]
        
        self.save_df()
    
    def edit_entry(self, df:pd.DataFrame, info:Dict):
        """
        Change performance of a an exercise on a given date
        
        *info*: Dict with keys 'ExerciseID', 'Date', and 'Performance'
        """
        
        info['ExerciseID'] = self.get_id_from_name(self.id_df, info)
        self.df.loc[(self.df['Date'] == info['Date']) & (self.df['ExerciseID'] == info['ExerciseID']),
               ['Performance']] = info['Performance']
        # At the specified date and exerciseId, change the performance
        
        self.save_df()

class WorkoutEditor(DFEditor):
    """
    Edit the File containing information about a given workout
    """    
    def __init__(self):
        f = "./stored_info/workout_db_example.csv"
        super().__init__(filename = f)
        self.alt_filename = "./stored_info/exercise_db_example.csv"
        self.id_df = pd.read_csv(self.alt_filename)

    def add_entry(self, info:Dict):
        """
        *df*: DataFrame to append to
        *info*: Dict with keys: 'ExerciseID', 'Order', 'Sets', 'Reps'
        
        --On cmd user adds a workout and this creates and runs this method.
            Hence This will be called once per workout. In this function 
            increment workout ID by 1 each time.
        """
        
        num_entries = len(info['Order'])
        wkt_id = self.df['WorkoutID'].max() + 1
        info['WorkoutID'] = [wkt_id for _ in range(num_entries)]
        self.df = pd.concat([self.df, pd.DataFrame(info)], ignore_index = True)
        
        self.save_df()        
    
    def remove_entry(self, info:Dict):
        """
        remove an entire workout from the file.
        
         *info*: dictionary with key "WorkoutID"
        """
    
        self.df = self.df[self.df['WorkoutID'] != info['WorkoutID']]
        self.save_df()
    
    def edit_entry(self, info:Dict):
        """
        Replace an exercise with another one by specifying the order.
        
        *info*: Dict with keys: 'WorkoutID', "Order", "ExerciseID" 
        """
        
        info['ExerciseID'] = self.get_id_from_name(self.id_df, info)
        self.df.loc[(self.df['WorkoutID'] == info['WorkoutID']) & 
               (self.df['Order'] == info['Order']), 
               ['ExerciseID']] = info['ExerciseID']

        self.save_df()
    
        
    
    
    
    
    
