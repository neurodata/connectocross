#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 13:22:08 2021

@author: pauladkisson
"""

import json
import os
from networkx.readwrite import json_graph as jg

def load_wit_nx():
    wit_graphs = []
    script_dir = os.path.dirname(__file__)
    base_path = os.path.join(script_dir, "witvilet2020/graphs")
    for graph_file in os.listdir(base_path):
        graph_file_path = os.path.join(base_path, graph_file)
        with open(graph_file_path) as f:
            data = json.load(f)
        graph = jg.node_link_graph(data)
        wit_graphs.append(graph)
    return wit_graphs