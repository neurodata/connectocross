#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:06:58 2021

@author: pauladkisson

Purpose: load witvilet2020 graphs into list
"""

import os
from graph import GraphIO

def load_wit():
    wit_graphs = []
    script_dir = os.path.dirname(__file__)
    base_path = os.path.join(script_dir, "graphs")
    for graph_file in os.listdir(base_path):
        path = os.path.join(base_path, graph_file)
        graph, _, _, _ = GraphIO.load(path)
        wit_graphs.append(graph)
    return wit_graphs