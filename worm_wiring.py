#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 20:34:38 2020

@author: pauladkisson

Purpose: Pulls Data from WormWiring Site and stores as NetworkX objects.
"""
import requests
import json
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def pull_xl_file(url):
    '''
    Takes a url to an excel file and outputs a list of pandas dataframes.
    Each dataframe corresponds to a sheet in the excel file.
    '''
    r = requests.get(url)
    with open('temp.xlsx', 'wb') as x:
        x.write(r.content)

    ww_file = pd.ExcelFile('temp.xlsx')
    dfs = []
    for sheet in ww_file.sheet_names:
        dfs.append(ww_file.parse(sheet, header=None))
    return dfs

def pull_worm():
    '''
    Pulls all the excel files from the Worm Wiring website
    outputs a dictionary, where the keys are the names of the excel files and
    the values are lists of pandas dataframes corresponding to the sheets
    from that file.
    '''
    urls = {'connectome':"https://wormwiring.org/si/SI%205%20Connectome%20adjacency%20matrices,%20corrected%20July%202020.xlsx",
            'syn_adj':"https://wormwiring.org/si/SI%202%20Synapse%20adjacency%20matrices.xlsx",
            'syn_list':"https://wormwiring.org/si/SI%203%20Synapse%20lists.xlsx",
            'cell_lists':"https://wormwiring.org/si/SI%204%20Cell%20lists.xlsx",
            'cell_class':"https://wormwiring.org/si/SI%206%20Cell%20class%20lists.xlsx",
            'class_connectome':"https://wormwiring.org/si/SI%207%20Cell%20class%20connectome%20adjacency%20matrices,%20corrected%20July%202020.xlsx",
            'nerve&ganglion':"https://wormwiring.org/si/Adult%20and%20L4%20nerve%20ring%20neighbors.xlsx"}
    file_dfs = {file : pull_xl_file(urls[file]) for file in urls}    
    return file_dfs

def fill_missing(df, start_idx=0):
    '''Fills in missing type and subtype information'''
    df = df.drop(df.tail(1).index) #drop the last row
    df = df.drop(df.columns[-1], axis=1) #drop the last column
    nans = df.isna()
    for i in range(start_idx, df.shape[0]):
        for j in range(2):
            if(nans.iloc[i, j]):
                df.iloc[i, j] = df.iloc[i-1, j]
    for i in range(start_idx, df.shape[1]):
        for j in range(2):
            if(nans.iloc[j, i]):
                df.iloc[j, i] = df.iloc[j, i-1]
    return df

def extract_data(df):
    '''Extracts graph data and metadata for a single sheet'''
    #Metadata
    df = fill_missing(df, 3)
    types = (df.iloc[:, 0], df.iloc[0, :])
    subtypes = (df.iloc[:, 1], df.iloc[1, :])
    ids = [df.iloc[:, 2], df.iloc[2, :]]
    
    unique_ids = list(pd.concat((ids[0], ids[1])).dropna().unique())
    id_dict = {i:unique_ids[i] for i in range(len(unique_ids))}
    for i in range(len(ids)):
        ids[i] = pd.Series(ids[i].index.values, index=ids[i]) #flips id series so that each ID looks up a dataframe index
    
    type_dict = {}
    subtype_dict = {}
    for i in id_dict:
        try: #using rows (column of IDs)
            type_dict[i] = types[0][ids[0][id_dict[i]]]
        except KeyError: #use columns
            type_dict[i] = types[1][ids[1][id_dict[i]]]
        try: #using columns (row of IDs)
            subtype_dict[i] = subtypes[1][ids[1][id_dict[i]]]
        except KeyError: #use rows
            subtype_dict[i]  = subtypes[0][ids[0][id_dict[i]]]
    
    #Graph
    G = nx.DiGraph()
    G.add_nodes_from(range(len(id_dict)))
    for i, idi in id_dict.items():
        for j, idj in id_dict.items():            
            try:
                edge_weight = df.iat[ids[0][idi], ids[1][idj]]
            except KeyError:
                continue #skip misssing IDs
            if(not(np.isnan(edge_weight))):
                    G.add_edge(i, j, weight=edge_weight)
    
    for node in id_dict:
        G.nodes[node]['ID'] = id_dict[node]
        G.nodes[node]['Type'] = type_dict[node]
        G.nodes[node]['Subtype'] = subtype_dict[node]
    return (G)

def extract_connectome(connectome_dfs):
    '''
    Takes the connectome list of dataframes and outputs a list of networkx objects with adjacency matrix and metadata
    '''
    title_n_legend = connectome_dfs[0]
    title_info = title_n_legend.iat[0, 0]+"\n"+title_n_legend.iat[1, 0]
    graphs = []
    for df in connectome_dfs[1:]:
        graphs.append(extract_data(df))

    #Adding whole-graph attributes
    for i in range(len(graphs)):
        g = graphs[i]
        g.graph['Title'] = title_info
        if i < 3:
            g.graph['Sex'] = "Hermaphrodite"
        else:
            g.graph['Sex'] = "Male"
        if i % 3 == 0:
            g.graph['Synapse Type'] = "Chemical"
        elif i == 1 or i == 4:
            g.graph['Synapse Type'] = "Asymmetric Gap Junction"
        else:
            g.graph['Synapse Type'] = "Symmetric Gap Junction"
    
    return graphs

def worm_wiring():
    file_dfs = pull_worm()
    extracted_connectome = extract_connectome(file_dfs['connectome'])
    
    #displaying results
    for graph in extracted_connectome:
        print(graph.graph)
        print(graph.nodes.data())
        plt.figure()
        nx.draw(graph)
    return extracted_connectome
        
    
worm_wiring()
