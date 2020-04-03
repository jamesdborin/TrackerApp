import matplotlib.pyplot as plt
import networkx as nx
import json
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.readwrite.json_graph import node_link_data, node_link_graph

class ExerciseNetwork:    
    """
    Class to store and display the information on the relationship between exercises.
    ==================================
    Possible ways to initialise:
        - *NetworkX DiGraph*: pass initial_graph = <nx.DiGraph> object
        - *JSON file*: pass a dictionary loaded from a JSON file
        - *Nothing*: to initialise a new graph
        - *file_to_graph*: run this method with a filename to load a graph from a file
    
    
    Useful Methods:
    ==================================
    
    - add_branch / add_branches / add_branches_from_dict
    - get_children_of / get_parents_of
    - add_edge_from_name / add_edgess_from_dict
    - draw_graph
    - get_exercise_names
    """
    def __init__(self, initial_graph = None, json_graph = None):
        is_graph = isinstance(initial_graph, nx.DiGraph)
        is_dict = isinstance(json_graph, dict)
        if is_graph:
            self.graph = initial_graph
        elif is_dict:
            self.graph = node_link_graph(json_graph)
        else:
            self.graph = nx.DiGraph()

        
    @property
    def all_labels(self):
        return [node[1]['name'] for node in self.graph.nodes(data=True)]
    
    
    @staticmethod
    def get_common_elements(list1, list2):
        set1, set2 = set(list1), set(list2)
        common_elements = set1 & set2
        return common_elements

    
    @staticmethod
    def get_unique_elements(list1, list2):
        set1, set2 = set(list1), set(list2)
        unique_elements = set1 ^ set2
        return unique_elements
    
    
    def add_branch(self, new_labels, start_node_name):
        # check if any of the new labels are currently in the graph. No new node is added and a new edge is added.
        common_labels = self.get_common_elements(self.all_labels, new_labels)
        # Isolate new labels that are unique
        unique_labels = self.get_unique_elements(common_labels, new_labels)
        
        num = max(self.graph.nodes) + 1 # start labelling nodes from this number
        num_new_nodes = len(new_labels) - len(common_labels) # exclude new nodes from being added
        
        new_nodes = range(num, num+num_new_nodes)
        old_nodes = self.get_nodes_of_labels(list(common_labels)) # find the node # of the nodes already in the graph 
        
        labels = {node_num: {'name':label} for node_num, label in zip(list(new_nodes), unique_labels)}
        # add new nodes and give them attributes from new_labels
        self.graph.add_nodes_from(new_nodes)
        nx.set_node_attributes(self.graph, labels)

        # find node to branch edges from
        node = [x for x,y in self.graph.nodes(data = True) if y['name'] == start_node_name][0]
        
        edges = [(node, new_node) for new_node in new_nodes] + [(node, old_node) for old_node in old_nodes]
        # add edges to the new nodes, and the new edges to the old nodes
        self.graph.add_edges_from(edges)
    
    
    def add_branches(self, new_labels, start_node_names):
        for label, start in zip(new_labels, start_node_names):        
            self.add_branch(label, start)
       
    
    def add_branches_from_dict(self, exercise_dict):
        """
        Add branches from a dictionary with the structure:
        {start_node1:[end1, end2,...], start_node2:[end1, end2], ...}
        If an endpoint is specified twice then an edge is added to that node from all start nodes. 
        """
        for node in exercise_dict.keys():
            self.add_branch(exercise_dict[node], node)
    
    
    def get_labels_of_nodes(self, nodes):
        return [y['name'] for x,y in self.graph.nodes(data = True) 
                if x in nodes]
    
    
    def get_nodes_of_labels(self, labels):
        return [x for x,y in self.graph.nodes(data = True) if y['name'] 
                in labels]
     
    
    def get_children_of(self, name):
        start_node = self.get_nodes_of_labels(name)[0]
        child_nodes = list(self.graph.successors(start_node))
        child_names = self.get_labels_of_nodes(child_nodes)
        return child_nodes, child_names
    
    
    def get_parents_of(self, name):
        start_node = self.get_nodes_of_labels(name)[0]
        parent_nodes = list(self.graph.predecessors(start_node))
        parent_names = self.get_labels_of_nodes(parent_nodes)
        return parent_nodes, parent_names

    
    def add_edge_from_name(self, start_label, end_label):
        nodes = self.get_nodes_of_labels([start_label, end_label])
        edges = [(nodes[0], nodes[1])]
        self.graph.add_edges_from(edges)
    
    
    def add_edges_from_dict(self, edges_dict):
        """
        Add edges from a dictionary of nodes {from1:[dest1, dest2,...], from2:[dest1,dest2,...]}
        """
        for start_label in edges_dict.keys():
            for end_label in edges_dict[start_label]:
                self.add_edge_from_name(start_label, end_label)

    
    def draw_graph(self, size = (20,20)):
        pos = graphviz_layout(self.graph, prog='twopi', args = '')
        labels = {x:y['name'] for x,y in self.graph.nodes(data = True)}
        plt.figure(figsize = size)
        nx.draw(self.graph, pos, node_size=0, alpha=0.4, edge_color="r", font_size=8, with_labels=True, labels = labels)
    
    
    def get_exercise_names(self):
        end_nodes = []
        for node in self.graph.nodes():
            successors_exist = len(list(self.graph.successors(node))) > 0
            if successors_exist:
                pass
            else:
                end_nodes.append(node)
        return self.get_labels_of_nodes(end_nodes)

        
    def graph_to_json(self):
        return node_link_data(self.graph)
    
    
    def graph_to_file(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.graph_to_json(), outfile)
    
    
    def file_to_graph(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            self.graph = node_link_graph(data)
