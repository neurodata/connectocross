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
from networkx.readwrite import json_graph as jg
from load_worm_nx import load_worm_nx

def read_graph(base_url, name):
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
    og_id2id = {}
    for node in graph.nodes:
        if node[:3] == "BWM": #convert ID to worm_wiring form 
            ID = node[4].lower() + "BWM" + node[5] + str(int(node[6:]))
        else:
            ID = node
        og_id2id[node] = ID
        graph.nodes[node]['original_id'] = node
        graph.nodes[node]['cell_type0'] = None
        graph.nodes[node]['cell_type1'] = None
        graph.nodes[node]['hemisphere'] = None
        graph.nodes[node]['dorsoventral'] = None
    graph = nx.relabel.relabel_nodes(graph, og_id2id)
    return graph


def load_witvilet_2020(datasets, base_url):
    graphs = [read_graph(base_url, d) for d in datasets]
    return graphs

def witvilet2020_nx():
    base_url = "http://nemanode.org/api/download-connectivity?datasetId=witvliet_2020_{}"
    datasets = list(range(1, 9))
    worm_graphs = load_worm_nx()
    wit_graphs = load_witvilet_2020(datasets, base_url)
    wit_worm = ww.make_consistent(wit_graphs+worm_graphs)
    wit_graphs = wit_worm[:len(wit_graphs)]
    return wit_graphs
