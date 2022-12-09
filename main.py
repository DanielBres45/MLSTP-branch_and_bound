# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 12:51:01 2022

@author: Daniel
"""
import csv
import os
import networkx as nx
import matplotlib.pyplot as plt
from typing import Type
from unionFind import union_find


def load_instances(file_path: str) -> list[list[list]]:
    """
    load_instances will load from a csv ith format specified by project assignment
    k
    edges, vertices
    u, v
    ....
    edges, vertices
    u, v
    ....

    Parameters
    ----------
    file_path : str
        csv path.

    Returns
    -------
    list[list[list]]
        list contains 
        number of instances
        number of edges
        edge [u, v].

    """
    instances = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        
        num_instances = next(reader)
        for instance in range(int(num_instances[0])):
            cur = next(reader)
            vertices, edges = cur[:2]
            current_instance = [[vertices, edges]]
            for i in range(int(edges)):
                current_instance.append(next(reader))
            instances.append(current_instance)
    
    return instances

def leaf_count(G: Type[nx.Graph]) -> int:
    """
    Counts number of leaves in a graph, vertices with degree 1

    Parameters
    ----------
    G : Type[nx.Graph]
        the graph, should be tree.

    Returns
    -------
    int
        number of leaves.

    """
    
    leaves = 0
    
    for vertex in list(G.nodes):
        if (G.degree[vertex] == 1):
            leaves += 1
            
    return leaves

def maximally_leafy_forest(G: Type[nx.Graph]) -> Type[union_find]:
    """
    maximally_leafy_forest generation for Lu-Ravi algorithm

    Parameters
    ----------
    G : Type[nx.Graph]
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    Subtrees = union_find(G)
    degrees = {}
    
    for vertex in list(G.nodes):
        T = nx.Graph()
        T.add_node(vertex)
        
        Subtrees.new_subtree(vertex, T, vertex)
        degrees[vertex] = 0
        
    for vertex in list(G.nodes):
        S_prime = []
        d_prime = 0
        
        for edge in G.edges(vertex):
            if((edge[1] not in Subtrees.get_subtree(vertex)) 
               and (Subtrees.getKey(edge[1]) not in S_prime)):
                d_prime = d_prime + 1
                
                #Insert subtrees[u] into S_prime
                S_prime.append(Subtrees.getKey(edge[1]))
                
        if (degrees[vertex] + d_prime >= 3):
            for subtree in S_prime:
                cur_subtree = Subtrees.get_subtree_from_key(subtree)
                
                # nx.draw_networkx(cur_subtree[0])
                # plt.show()
                
                Subtrees.merge(vertex, cur_subtree[1])
                degrees[vertex] = degrees[vertex] + 1
                degrees[cur_subtree[1]] = degrees[cur_subtree[1]] + 1
                

                # nx.draw_networkx(Subtrees.get_subtree(vertex))
                # plt.show()
    
    # print(Subtrees)
    
    return Subtrees

def combine_forest(F: Type[union_find], G: Type[nx.Graph], debug=False) -> Type[nx.Graph]:
    """
    Step 2 of Lu-Parv

    Parameters
    ----------
    F : Type[union_find]
        Outout of maximally leafy forest.
    G : Type[nx.Graph]
        Original graph for instance.
    debug : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    TYPE
        Tree of G.

    """
    
    root_key = F.get_largest_subtree()
    root_tree = F.get_subtree_from_key(root_key)[0]
     
    unmerged = True
    unmerged_key = None
    
    while unmerged:
                          
        for subtree in list(F.getKeys()):
            if (subtree == root_key):
                continue
            
            flag = False
            
            for node in F.get_subtree_from_key(subtree)[0].nodes:
                if (flag):
                    break
                for check_node in root_tree.nodes:
                    if G.has_edge(node, check_node) or G.has_edge(check_node, node):
                        # print("Edge: {} {}".format(node, check_node))
                        F.merge(check_node, node, root1=check_node, root2=node)
                        flag = True
                        break
                    
            if (flag == False):
                unmerged = True
                unmerged_key = subtree
        
        if len(list(F.getKeys())) <= 1:
            unmerged = False
        
        if unmerged:
            root_key = unmerged_key
            root_tree = F.get_subtree_from_key(root_key)[0]
    
    return F.get_subtree_from_key(list(F.getKeys())[0])[0]
    

def solve_instance(instance: list, draw=False, debug=True):
    """
    Calls all algorithms on instance

    Parameters
    ----------
    instance : list
        instance by edge.
    draw : TYPE, optional
        DESCRIPTION. The default is False.
    debug : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    Type[nx.Graph]
        Tree for instance.
    int
        Number of leavess.

    """
    
    G = nx.Graph()
    
    G.add_edges_from(instance[1:])
    
    if draw:
        nx.draw_networkx(G)
        plt.show()
    
    BFS_Tree = nx.bfs_tree(G, '1')
    BFS_leaves = leaf_count(BFS_Tree)
    
    F = maximally_leafy_forest(G)
    
    # if debug:
    #     for tree_key in F.getKeys():
    #         nx.draw_networkx(F.get_subtree_from_key(tree_key)[0])
    #         plt.show()
    
    F_tree = combine_forest(F, G)
    F_tree_leaves = leaf_count(F_tree)

    if draw:
        nx.draw_networkx(F_tree)
        plt.show()

        
    # Solis_tree = Solis(instance)
    # S_tree_leaves = leaf_count(Solis_tree)
    
    # print("BFS leaves: {}, Solis-Obis: {}".format(BFS_leaves,  S_tree_leaves))
    
    max_value = max((BFS_leaves, F_tree_leaves))
    
    # if(max_value == 99):
    #     print(G.edges)
    #     print(F_tree.edges)
            
        
    print("BFS leaves: {}, Lu-Parv leaves: {}".format(BFS_leaves, F_tree_leaves))
        
    if(BFS_leaves == max_value):
        return (BFS_Tree, BFS_leaves)
    elif(F_tree_leaves == max_value):
        return (F_tree, F_tree_leaves)
    
    return (BFS_Tree, BFS_leaves)
    
    
    # elif(S_tree_leaves == max_value):
    #     return (Solis_tree, S_tree_leaves)
    
    
    
def Solis(instance):
        G = nx.Graph()
        copyG = nx.Graph()
        node_num = 0
        edges_num = 0
        # build the input graph with nodes and edges
        for i in range(0,len(instance),1) :
            if i == 0:
                node_num = instance[i][0]
                edges_num = instance[i][1]
            else:
                copyG.add_edge(instance[i][0],instance[i][1])
                G.add_edge(instance[i][0],instance[i][1])
        
        
        
        #build a forest which is void at first
        F = []
        #while there is a vertex v of degree at least 3 do
        flag = 1
        while flag == 1:
            flag = 0
            vertex = None
            for v in G.nodes:
                if G.degree(v) > 2:
                    flag = 1
                    vertex = v
                    break
            if flag == 1:
                #Build a tree Ti with root v and leaves the neighbors of v
                T = nx.Graph()
                T.add_node(vertex)
                G,T = root_expand(G, vertex, T)
                F.append(T)
        

        
        for i in list(G.nodes):
            Ti = nx.Graph()
            if i in G.nodes:
                Ti,G = separateGNodes(G,i,Ti)
            if len(Ti.nodes) > 0:
                F.append(Ti)
        #for i in F:
        #    nx.draw(i, with_labels=True, font_weight='bold')
        #    plt.show() 
        #Connect the trees in F and all vertices not in F to form a spanning tree T .
        
        return connect(F,copyG)

def connect(F,G):
    C = nx.Graph()
    C.add_edges_from(F[0].edges)
    F.remove(F[0])

    
    while len(F) != 0:
        for node in C.nodes:
            flag = False
            for tree in F:
                for nodes in tree:
                    if (node,nodes) in G.edges:
                        C.add_edges_from(tree.edges)
                        C.add_edge(node,nodes)
                        flag = True
                        F.remove(tree)
                        break
                if flag == True:
                    break
            if flag == True:
                break
      
    
    
    return C
def root_expand(G, v, T):
    for root in list(G.adjacency()):
        if root[0] == v:
            #add neighbor into Ti
            #neighbors = []
            for neighbor in root[1]:
                #print(v+" "+neighbor)
                T.add_node(neighbor)
                if T.degree(neighbor) == 0:
                    T.add_edge(*(v,neighbor))
            #after adding v to T and find all neighbor of v, remove it
            G.remove_node(v)
            #calculate T.nodes priorty
            for t_node in list(T.nodes):
               t = 0
               for r in list(G.adjacency()):
                   if r[0] == t_node:
                       for neigh in r[1]:
                           if neigh in T.nodes:
                               t+=1
               if type(G.degree(t_node)) == (int) and G.degree(t_node)-t== 2:
                   #color blue means priorty 1
                   color = "blue"
               elif type(G.degree(t_node)) == (int) and G.degree(t_node)-t> 2:
                    #color green means priorty 2
                    color = "green"
               else:
                    color = "NULL"
                    if t_node in G.nodes:
                        G.remove_node(t_node)
            
               T.nodes[t_node]['color'] = color
            #expand the highest priorty in the T tree
            for t_node in list(T.nodes):
                if T.nodes[t_node]['color'] == "green":
                    t = 0
                    for r in list(G.adjacency()):
                        if r[0] == t_node:
                            for neigh in r[1]:
                                if neigh in T.nodes:
                                    t+=1
                        if type(G.degree(t_node)) == (int) and G.degree(t_node)-t >= 2:
                            G,T = root_expand(G,t_node,T)
                        else:
                            if t_node in G.nodes:
                                G.remove_node(t_node)
                            
            for t_node in list(T.nodes):
                if T.nodes[t_node]['color'] == "blue":
                    t = 0
                    for r in list(G.adjacency()):
                        if r[0] == t_node:
                            for neigh in r[1]:
                                if neigh in T.nodes:
                                    t+=1
                        
                    if type(G.degree(t_node)) == (int) and G.degree(t_node)-t >= 2:
                        G,T = root_expand(G,t_node,T)
                        
                    else:
                        if t_node in G.nodes:
                            G.remove_node(t_node)
                        
    return(G,T)

def separateGNodes(G,root,Ti):
    """
    Turn disjoint subtrees into an array, easier to work with

    Parameters
    ----------
    G : TYPE
        DESCRIPTION.
    root : TYPE
        DESCRIPTION.
    Ti : TYPE
        DESCRIPTION.

    Returns
    -------
    Ti : TYPE
        DESCRIPTION.
    G : TYPE
        DESCRIPTION.

    """
    flag = False
    if root not in Ti.nodes:
        Ti.add_node(root)
    for edge in G.edges:
        if root in edge:
            flag = True
    if flag == False:
        if root in G.nodes:                    
            G.remove_node(root)
        return Ti,G
    
    for adj in list(G.adjacency()):
        if adj[0] == root:
            if(len(adj[1]) == 0):
                break
            for neighbor in list(adj[1]):
                Ti.add_edge(root,neighbor)
                G.remove_edge(root,neighbor)
                separateGNodes(G,neighbor,Ti)
    if root in G.nodes:                    
        G.remove_node(root)
    return Ti,G
        
    

def run_instances(instances, file_name="all-solved.out"):
    for i, instance in enumerate(instances):
        
        print("Start instance: {}".format(i))
        try:
            T, leaves = solve_instance(instance)
            
            outlist = []
            
            head = [leaves, 0]
            
            for edge in T.edges:
                outlist.append(list(map(int, edge)))
                head[1] += 1
                
            outlist = sorted(outlist, key=lambda x: x[0])
            
            outlist = [head] + outlist
            
            with open(file_name, "a", newline='') as f:
               writer = csv.writer(f, delimiter=' ')
               
               writer.writerows(outlist)

        except (KeyError):
            print("Error with instance: {}".format(i))
            exit(1)
        
        print("Finished instance: {}".format(i))
    
    
def check_instances(instances) -> list:
    
    instance_out = []
    
    for i, instance in enumerate(instances):
        G = nx.Graph()
        
        G.add_edges_from(instance[1:])
        
        if (nx.is_connected(G)):
            instance_out.append(instance)
        else:
            print("Failure to load instance #{}".format(i))
    
    return instance_out

if __name__=="__main__":
    
    instances = load_instances(os.path.join(os.getcwd(), "all-hard.txt"))
    
    instances = check_instances(instances)
    
    run_instances(instances)
    
    
    
    
    
    
    
    
    