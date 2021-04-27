#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 14:52:56 2021

@author: pauladkisson

Purpose: Call worm_wiring to obtain graphs,
        validate graphs using validate_worm,
        and store worm_wiring graphs in file spec using graph_io
"""

from c_elegans.worm_wiring import worm_wiring as ww, validate_worm as vw
from graph import GraphIO
import os

print("...Pulling WormWiring Dataframes...")
file_dfs = ww.pull_worm()
print("...Extracting Graphs...")
graphs = ww.worm_wiring()
print("...Validating Results...")
vw.validate_worm(file_dfs, graphs)

print("...Storing Graphs...")
script_dir = os.path.dirname(__file__)
base_path = script_dir.split("connectocross")[0]
base_path = os.path.join(base_path, "connectocross/json_connectomes")
for file in graphs:
    print("file =", file)
    filegraphs = graphs[file]
    if file == 'nerve&ganglion': #nerve&ganglion does not have separate hermaphrodite and male fields
        for i, graph in enumerate(filegraphs[0]):
            file_path = os.path.join(base_path, "worm_wiring/%s/Adult/%s.json" % (file, i))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            GraphIO.dump(graph, file_path)
        for i, graph in enumerate(filegraphs[1]):
            file_path = os.path.join(base_path, "worm_wiring/%s/L4/%s.json" % (file, i))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            GraphIO.dump(graph, file_path)
    else:
        for sex_graphs in filegraphs:
            sex = sex_graphs[0].graph['Sex']
            for i, sex_graph in enumerate(sex_graphs):
                file_path = os.path.join(base_path, "worm_wiring/%s/%s/%s.json" % (file, sex, i))
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                GraphIO.dump(sex_graph, file_path)
    