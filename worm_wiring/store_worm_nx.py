#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13

@author: pauladkisson

Purpose: Call worm_wiring to obtain graphs,
        validate graphs using validate_worm,
        and store worm_wiring graphs as json files using networkx's native
        node_link_data functionality
"""

from worm_wiring import worm_wiring as ww, validate_worm as vw
from networkx.readwrite import json_graph as jg
import json
import os

script_dir = os.path.dirname(__file__)

print("...Pulling WormWiring Dataframes...")
file_dfs = ww.pull_worm()
print("...Extracting Graphs...")
graphs = ww.worm_wiring()
print("...Validating Results...")
vw.validate_worm(file_dfs, graphs)

print("...Storing Graphs...")
for file in graphs:
    print("file =", file)
    filegraphs = graphs[file]
    if file == 'nerve&ganglion': #nerve&ganglion does not have separate hermaphrodite and male fields
        for i, graph in enumerate(filegraphs[0]):
            data = jg.node_link_data(graph)
            file_path = os.path.join(script_dir, "graphs/%s/Adult/%s.json" % (file, i))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(data, f)
        for i, graph in enumerate(filegraphs[1]):
            data = jg.node_link_data(graph)
            file_path = os.path.join(script_dir, "graphs/%s/L4/%s.json" % (file, i))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(data, f)
    else:
        for i in range(len(filegraphs)):
            sex = filegraphs[i][0].graph['Sex']
            for j, graph in enumerate(filegraphs[i]):
                data = jg.node_link_data(graph)
                file_path = os.path.join(script_dir, "graphs/%s/%s/%s.json" % (file, sex, j))
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    json.dump(data, f)
    