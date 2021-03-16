#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 12:50:36 2021

@author: pauladkisson

Purpose: Load wormwiring graphs
"""
import requests
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
from worm_wiring import worm_wiring as ww
from networkx.readwrite import json_graph as jg


def load_worm_nx():
    worm_graphs = []
    script_dir = os.path.dirname(__file__)
    base_path = os.path.join(script_dir, "graphs")
    for file_folder in os.listdir(base_path):
        if file_folder.startswith(".") or file_folder=="syn_list":
            continue
        file_folder_path = os.path.join(base_path, file_folder)
        for graph_folder in os.listdir(file_folder_path):
            if graph_folder.startswith(".") or graph_folder.endswith(".mgraph"):
                continue
            graph_folder_path = os.path.join(file_folder_path, graph_folder)
            for graph_file in os.listdir(graph_folder_path):
                graph_file_path = os.path.join(graph_folder_path, graph_file)
                with open(graph_file_path) as f:
                    data = json.load(f)
                graph = jg.node_link_graph(data)
                worm_graphs.append(graph)
    return worm_graphs


