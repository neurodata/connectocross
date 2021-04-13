#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:53:58 2021

@author: pauladkisson
"""


from c_elegans.witvilet2020 import witvilet2020 as wit
from graph import GraphIO
import os

script_dir = os.path.dirname(__file__)

print("...Pulling Witvilet2020 Graphs...")
graphs = wit.witvilet2020()

print("...Storing Graphs...")
for i, graph in enumerate(graphs):
    file_path = os.path.join(script_dir, "graphs/%s.json" % i)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    GraphIO.dump(graph, file_path)