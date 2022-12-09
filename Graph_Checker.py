# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 13:37:20 2022

@author: Daniel
"""

import networkx as nx
import re

def get_graphs(file):
    graphs = []
    with open(file, "r") as f:
        num_graphs = int(f.readline())
        for _ in range(num_graphs):
            l = f.readline()
            n,m = [int(x) for x in re.split(r'\s|,| , ', l) if x != '']
            # n, m = map(int, l.split(','))
            # Create a new graph
            G = nx.Graph()

            # Add all the vertices to the graph
            for j in range(n):
                G.add_node(j)
            for j in range(m):
                u,v = [int(x) for x in re.split(r'\s|,| , ', f.readline()) if x != '']
                G.add_edge(u, v)
            graphs.append(G)

    return graphs

def all_valid(in_file, out_file):
    in_graphs = get_graphs(in_file)
    out_graphs = get_graphs(out_file)
    failed = set()
    for i, (in_g, out_g) in enumerate(zip(in_graphs, out_graphs)):
        if not len(in_g.nodes()) == len(out_g.nodes()):
            print(f"Graph {i} has wrong number of nodes")
            failed.add(i)
        if not nx.is_tree(out_g):
            print(f"Graph {i} is not a tree")
            failed.add(i)
        if not all([in_g.has_edge(*edge) for edge in out_g.edges()]):
            print(f"Graph {i} has edges that are not in the input graph")
            failed.add(i)
    return failed

all_valid("Graph.csv", "all-solved.out")