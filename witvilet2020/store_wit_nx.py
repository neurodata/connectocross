#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16

@author: pauladkisson

Purpose: Call witvilet2020_nx to obtain graphs,
        and store witvilet graphs as json files using networkx's native
        node_link_data functionality
"""

from witvilet2020 import witvilet2020_nx as wit
from networkx.readwrite import json_graph as jg
import json
import os

script_dir = os.path.dirname(__file__)

print("...Pulling Witvilet2020 Graphs...")
graphs = wit.witvilet2020_nx()

print("...Storing Graphs...")
for i, graph in enumerate(graphs):
    data = jg.node_link_data(graph)
    file_path = os.path.join(script_dir, "graphs/%s.json" % i)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f)
        