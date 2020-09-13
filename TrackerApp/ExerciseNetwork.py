import matplotlib.pyplot as plt
import networkx as nx
import json
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.readwrite.json_graph import node_link_data, node_link_graph
from collections import deque 

class ExerciseNetwork:    
    """
    Class to store and display the information on the relationship between exercises.
    ==================================
    Possible ways to initialise:
        - *NetworkX DiGraph*: pass initial_graph = <nx.DiGraph> object
        - *JSON file*: pass a dictionary loaded from a JSON file
        - *Nothing*: to initialise a new graph
        - *file_to_graph*: run this method with a filename to load a graph f ExerciseNEtworkrom a file
    
    
    Useful Methods:
    ==================================
    
    - add_branch / add_branches / add_branches_from_dict
    - get_children_of / get_parents_of
    - add_edge_from_name / add_edges_from_dict
    - draw_graph
    - get_exercise_names
    """
    
    def __init__(self, initial_graph = None, json_graph = None):
        """
        Initialise an exercise network, either from a network X object or with
        a graph defined as a dictionary
        
        *initial_graph*: Given a DiGraph, load this as an exercise network
        
        *json_graph*: Given a dictionary defining a graph, load this as the 
        Exercise Network
        
        --------------
        N.B. To load from a file you do the following.
        E.g. Ex = ExerciseNetwork() 
        Ex.file_to_graph(filename)
        """
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
        """
        Return the names of every node in the graph
        """
        return [node[1]['name'] for node in self.graph.nodes(data=True)]
    
    
    @staticmethod
    def get_common_elements(list1, list2):
        """
        Given two lists return the common elements as a set
        """
        set1, set2 = set(list1), set(list2)
        common_elements = set1 & set2
        return common_elements

    
    @staticmethod
    def get_unique_elements(list1, list2):
        """
        Given two lists return any elements that are unique to either set
        """
        set1, set2 = set(list1), set(list2)
        unique_elements = set1 ^ set2
        return unique_elements
    
    
    def add_branch(self, new_labels, start_node_name):
        """
        Add a branch to the Exercise Network:
            0. Specify the Parent node name and any child node that the parent 
                is to connect to
            
            1. Identify nodes in new branches that already exist in the 
                Network
                
            2. Add any nodes that dont already exist in the graph to the 
                graph
                
            3. Add edges from the parent nodes to the new nodes
            
            4. Any nodes that already exist must have an edge pointing towards
                them added to the network
                
        """
        # check if any of the new labels are currently in the graph. 
        #   No new node is added and a new edge is added.
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
        """
        For a list of start nodes add new labels to those nodes.
        
        *New Labels*: [[A1, A2, A3, ...], [B1, B2, ...], ...]
        *Start_Node_Labels*: [A_New, B_New, ...]
        """
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
        """
        Input: A list of node numbers
        
        Output: The names of exercises on those nodes
        """
        return [y['name'] for x,y in self.graph.nodes(data = True) 
                if x in nodes]
    
    
    def get_nodes_of_labels(self, labels):
        """
        Input: List of Exercise Names
        
        Output: List of node numbers that belong to those exercises
        """
        return [x for x,y in filter(lambda x: x[1]['name'] in labels, self.graph.nodes(data = True))]
     
    
    def get_children_of(self, name):
        """
        Given a node label find the children of that node.
        
        Input: Label of the node you want the children of
        
        Ouput: [Child Node Numbers, Child Node Names]
        """
        start_node = self.get_nodes_of_labels(name)[0]
        child_nodes = list(self.graph.successors(start_node))
        child_names = self.get_labels_of_nodes(child_nodes)
        return child_nodes, child_names
    

    def is_leaf_node(self, label):
        """
        Given a label, we want to check if this node is a root node (has > 0 successors), or if it is a leaf node (has 0 successors)
        """

        nodes = self.get_nodes_of_labels([label])
        successors_exist = len(list(self.graph.successors(nodes[0]))) > 0
        return not successors_exist


    def get_descendants_of(self, name):
        """
        Given a node label, find all end nodes that descend from this node

        Input: Label of the node you want the children of

        Output: [Descendant Node Numbers, Descendant Node Names]
        """

        end_nodes = []
        start_node = self.get_nodes_of_labels([name])[0]
        q = deque()
        q.append(start_node)
        
        while len(q) > 0:
            node = q.popleft()
            node_label = self.get_labels_of_nodes([node])
            children = self.get_children_of(node_label)
            
            for child in children[0]:
                successors_exist = ( len(list(self.graph.successors(child))) > 0 )
                if successors_exist:
                    q.appendleft(child)

                else:
                    end_nodes.append(child)
        
        return end_nodes

    
    def is_parent(self, name):
        """
        Given a node label check is this node is a parent or not
        """
        node_num = self.get_nodes_of_labels(name)[0]
        return len(list(self.graph.successors(node_num))) > 0


    def get_parents_of(self, name):
        """
        Given a node label find the parents of that node
        """
        start_node = self.get_nodes_of_labels(name)[0]
        parent_nodes = list(self.graph.predecessors(start_node))
        parent_names = self.get_labels_of_nodes(parent_nodes)
        return parent_nodes, parent_names

    
    def add_edge_from_name(self, start_label, end_label):
        """
        Add an edge between two node names
        """
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

    def delete_branch(self, delete_name):
        """
        We want to delete an entire branch from the network if necessary.
        
        Recursively delete a branch and its child nodes. Pray to the gods it
        doesnt delete something you want to keep.
        """
        node_num = self.get_nodes_of_labels([delete_name])
        child_nodes = self.get_children_of([delete_name])
        
        if len(child_nodes[0]) > 0:
            for node in child_nodes[1]:
                self.delete_branch(node)
            
        self.graph.remove_node(node_num[0])
        

    def draw_graph(self, size = (20,20)):
        pos = graphviz_layout(self.graph, prog='twopi', args = '')
        labels = {x:y['name'] for x,y in self.graph.nodes(data = True)}
        plt.figure(figsize = size)
        nx.draw(self.graph, pos, node_size=0, alpha=0.4, edge_color="r", 
                font_size=8, with_labels=True, labels = labels)
    
    
    def get_exercise_names(self):
        """
        Return all of the nodes in the graph
        """
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
            
            
if __name__ == "__main__":
    EX = ExerciseNetwork()
    EX.file_to_graph("./stored_info/first_layer_exercise_chart.txt")
    EX.add_branches_from_dict({"Bicep Curls":["Hammer Curls"], "Grip Strength": ["Grip Curls"], "Grip Curls": ["Hammer Curls"]})
    EX.graph_to_file("./stored_info/first_layer_exercise_chart.txt")
    EX.draw_graph()