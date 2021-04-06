#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 17:08:02 2021

@author: pauladkisson

Purpose: Load worm_wiring graphs into list
"""

import os
from graph import GraphIO

def load_worm():
    worm_graphs = []
    script_dir = os.path.dirname(__file__)
    base_path = os.path.join(script_dir, "graphs")
    for file_folder in os.listdir(base_path):
        if file_folder.startswith("."):
            continue
        file_folder_path = os.path.join(base_path, file_folder)
        for graph_folder in os.listdir(file_folder_path):
            if graph_folder.startswith("."):
                continue
            graph_folder_path = os.path.join(file_folder_path, graph_folder)
            for graph_file in os.listdir(graph_folder_path):
                graph_file_path = os.path.join(graph_folder_path, graph_file)
                try:
                    graph, _, _, _ = GraphIO.load(graph_file_path)
                except TypeError: #to be fixed on GraphIO side
                    if file_folder == "syn_list":
                        continue
                    else:
                        print("file_folder =", file_folder)
                        raise TypeError
                worm_graphs.append(graph)
    return worm_graphs