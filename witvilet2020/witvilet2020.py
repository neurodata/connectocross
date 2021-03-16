#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:29:14 2021

@author: pauladkisson - Originally written by Benjamin Pedigo
2/23/20

Purpose: Pull graph data from  witvilet dataset
"""

import requests
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
from worm_wiring import worm_wiring as ww
from graph import GraphIO

base_url = "http://nemanode.org/api/download-connectivity?datasetId=witvliet_2020_{}"
datasets = list(range(1, 9))


def read_graph(name):
    url = base_url.format(name)
    r = requests.get(url)
    json_graph = r.content
    json_graph = json.loads(json_graph)
    edgelist = pd.DataFrame(json_graph)
    edgelist["weight"] = edgelist["synapses"]
    graph = nx.from_pandas_edgelist(
        edgelist,
        source="pre",
        target="post",
        edge_attr=True,
        create_using=nx.MultiDiGraph,
    )
    for node in graph.nodes:
        if node[:3] == "BWM": #convert ID to worm_wiring form 
            ID = node[4].lower() + "BWM" + node[5] + str(int(node[6:]))
        else:
            ID = node
        graph.nodes[node]['ID'] = ID
        graph.nodes[node]['cell_type0'] = None
        graph.nodes[node]['cell_type1'] = None
        graph.nodes[node]['Hemisphere'] = None
    return graph


def load_witvilet_2020():
    graphs = [read_graph(d) for d in datasets]
    return graphs

worm_graphs = []
base_path = "./worm_wiring/graphs"
for graph_folder in os.listdir(base_path):
    if graph_folder.startswith("."):
        continue
    graph_folder_path = base_path+"/"+graph_folder
    for graph_file in os.listdir(graph_folder_path):
        graph_file_path = graph_folder_path+"/"+graph_file
        graph, _, _, _ = GraphIO.load(graph_file_path)
        worm_graphs += graph
  
#ww_worm_graphs = ww.worm_wiring()

wit_graphs = load_witvilet_2020()
wit_worm = ww.make_consistent(wit_graphs+worm_graphs)
wit_graphs = wit_worm[:len(wit_graphs)]

print("worm_graphs[0] = ")
print(worm_graphs[0].nodes.data())
print("wit_graphs[0] = ")
print(wit_graphs[0].nodes.data())

for g in wit_graphs:
    plt.figure()
    nx.draw(g)
    print(g.graph)
    print(g.nodes.data())
