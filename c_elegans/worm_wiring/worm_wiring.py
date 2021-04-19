#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 2 20:34:38 2020

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
            'cellclass_connectome':"https://wormwiring.org/si/SI%207%20Cell%20class%20connectome%20adjacency%20matrices,%20corrected%20July%202020.xlsx",
            'nerve&ganglion':"https://wormwiring.org/si/Adult%20and%20L4%20nerve%20ring%20neighbors.xlsx"}
    file_dfs = {file : pull_xl_file(urls[file]) for file in urls}    
    return file_dfs

def fill_missing(df, df_is_cellclass=False):
    '''Fills in missing cell_type0 and cell_type1 information'''
    
    df = df.drop(df.tail(1).index) #drop the last row
    df = df.drop(df.columns[-1], axis=1) #drop the last column
    nans = df.isna()
    
    if df_is_cellclass:
        start_idx = 2
        special_fields = {'RIP', 'MNVC', 'MUBODY', 'CEPsh', 'GLR', 'CAN', 'exc_cell', 'exc_gl',
                          'hmc', 'hyp', 'int', 'mu_int', 'HSN', 'VC', 'mu_vul'} #IDs that don't have cell_type0's
        for i in range(start_idx, df.shape[0]):
            if(nans.iloc[i, 0]):
                if(df.iloc[i, 1] in special_fields):
                    df.iloc[i, 0] = None
                else:
                    df.iloc[i, 0] = df.iloc[i-1, 0]
        for j in range(start_idx, df.shape[1]):
            if(nans.iloc[0, j]):
                if(df.iloc[1, j] in special_fields):
                    df.iloc[0, j] = None
                else:
                    df.iloc[0, j] = df.iloc[0, j-1]
    else:
        start_idx = 3
        special_fields = {'OTHER END ORGANS', 'BODYWALL MUSCLES', 'SEX-SPECIFIC'} #cell_type1's that don't have cell_type0's
        for i in range(start_idx, df.shape[0]):
            if(nans.iloc[i, 0] and nans.iloc[i, 1]): #Both cell_type0 and cell_type1 are missing
                df.iloc[i, 0] = df.iloc[i-1, 0]
                df.iloc[i, 1] = df.iloc[i-1, 1]
            elif(nans.iloc[i, 0]): #Only cell_type0 is missing
                if(df.iloc[i, 1] in special_fields):
                    df.iloc[i, 0] = None
                else:
                    df.iloc[i, 0] = df.iloc[i-1, 0]
            elif(nans.iloc[i, 1]): #Only cell_type1 is missing
                df.iloc[i, 1] = None
        for j in range(start_idx, df.shape[1]):
            if(nans.iloc[0, j] and nans.iloc[1, j]): #Both cell_type0 and cell_type1 are missing
                df.iloc[0, j] = df.iloc[0, j-1]
                df.iloc[1, j] = df.iloc[1, j-1]
            elif(nans.iloc[0, j]): #Only cell_type0 is missing
                if(df.iloc[1,j] in special_fields):
                    df.iloc[0, j] = None
                else:
                    df.iloc[0, j] = df.iloc[0, j-1]
            elif(nans.iloc[1, j]): #Only cell_type1 is missing
                df.iloc[1, j] = None

    return df

def make_consistent(graphs):
    '''Ensures that each ID in the list of graphs has the same cell_type0 and cell_type1
        Note: Errs on the side of the first sheet'''
    ids = set()
    for g in graphs:
        for node in g.nodes:
            ids.add(node)
            
    for i in range(len(graphs)):
        for j in range(i+1, len(graphs)):
            g1 = graphs[i]
            g2 = graphs[j]
            meta_fields = ['cell_type0', 'cell_type1', 'hemisphere', 'dorsoventral']
            for meta in meta_fields:
                for ID in ids:
                    try:
                        g1_meta = g1.nodes[ID][meta]
                        g2_meta = g2.nodes[ID][meta]
                    except KeyError: #ID not present in one of the graphs
                        continue
                    if(g1_meta != g2_meta):
                        if(g1_meta == None):
                            graphs[i].nodes[ID][meta] = g2_meta
                        else:
                            graphs[j].nodes[ID][meta] = g1_meta
                        
    return graphs

def extract_listdata(df):
    '''Extracts graph data and metadata from given dataframe df that has list format'''
    #Metadata
    pre_ids = df.iloc[1:, 2]
    post1_ids = df.iloc[1:, 7]
    post2_ids = df.iloc[1:, 8]
    post3_ids = df.iloc[1:, 9]
    post4_ids = df.iloc[1:, 10]
    unique_ids = list(pd.concat((pre_ids, post1_ids, post2_ids, post3_ids, post4_ids)).dropna().unique())
    unique_pre_ids = list(pre_ids.unique())
    pre_ids = pd.Series(pre_ids.index.values, index=pre_ids) #flips pre_ids series so that each ID looks up a series of corresponding dataframe indices
    syn_ids = set()
    
    #Graph
    G = nx.MultiDiGraph()
    G.add_nodes_from(unique_ids)
    for pre_id in unique_pre_ids:
        indices = pd.Series(pre_ids[pre_id]).values
        for idx in indices:
            continNum = df.iat[idx, 0]
            EMseries = df.iat[idx, 1]
            synapse_type = df.iat[idx, 4]
            sections = df.iat[idx, 5]
            partner_num = df.iat[idx, 6]
            post1_id = df.iat[idx, 7]
            edge_key = "(%s, %s)" % (continNum, EMseries) #using string instead of tuple to avoid json error.
            while(edge_key in syn_ids): #duplicate synapse ID
                EMseries += "+"
                edge_key = "(%s, %s)" % (continNum, EMseries)
            edge_key = "(%s, %s)" % (continNum, EMseries)
            syn_ids.add(edge_key)
            try:
                G.add_edge(pre_id, post1_id, key=edge_key, sections=sections, synapse_type=synapse_type)
            except KeyError:
                if(np.isnan(post1_id)): #known missing data
                    continue
                else:
                    print("pre_id=", pre_id)
                    print("idx=", idx)
                    raise KeyError
            if partner_num >= 2:
                post2_id = df.iat[idx, 8]
                G.add_edge(pre_id, post2_id, key=edge_key, sections=sections, synapse_type=synapse_type)
                if partner_num >= 3:
                    post3_id = df.iat[idx, 9]
                    G.add_edge(pre_id, post3_id, key=edge_key, sections=sections, synapse_type=synapse_type)
                    if partner_num >= 4:
                        post4_id = df.iat[idx, 10]
                        try:
                            G.add_edge(pre_id, post4_id, key=edge_key, sections=sections, synapse_type=synapse_type)
                        except KeyError:
                            if(partner_num==5 or partner_num==6 or partner_num==9): #known typos
                                continue
                            else:
                                print("pre_id=", pre_id)
                                print("idx=", idx)
                                raise KeyError
    #Metadata
    for ID in unique_ids:
        G.nodes[ID]['original_id'] = ID
        
        j = 0
        while(ord(ID[-1-j]) >= 48 and ord(ID[-1-j]) <= 57): #last character is a digit 0-9
            j += 1
            
        if(ID[-1-j]=='L'):
            G.nodes[ID]['hemisphere'] = 'left'
            try:
                if(ID[-1-j-1]=='D' or ID[0]=='d'):
                    G.nodes[ID]['dorsoventral'] = 'dorsal'
                elif(ID[-1-j-1]=='V' or ID[0]=='v'):
                    G.nodes[ID]['dorsoventral'] = 'ventral'
                else:
                    G.nodes[ID]['dorsoventral'] = None
            except IndexError:
                G.nodes[ID]['dorsoventral'] = None
                
        elif(ID[-1-j]=='R'):
            G.nodes[ID]['hemisphere'] = 'right'
            
            try:
                if(ID[-1-j-1]=='D' or ID[0]=='d'):
                    G.nodes[ID]['dorsoventral'] = 'dorsal'
                elif(ID[-1-j-1]=='V' or ID[0]=='v'):
                    G.nodes[ID]['dorsoventral'] = 'ventral'
                else:
                    G.nodes[ID]['dorsoventral'] = None
            except IndexError:
                G.nodes[ID]['dorsoventral'] = None
        
        elif(ID[-1-j]=='D'):
            G.nodes[ID]['dorsoventral'] = 'dorsal'
        elif(ID[-1-j]=='V'):
            G.nodes[ID]['dorsoventral'] = 'ventral'
        else:
            G.nodes[ID]['hemisphere'] = None
            G.nodes[ID]['dorsoventral'] = None
        try: #using rows (column of IDs)
            G.nodes[ID]['cell_type0'] = None
        except KeyError: #use columns
            G.nodes[ID]['cell_type0'] = None
        try: #using columns (row of IDs)
            G.nodes[ID]['cell_type1'] = None
        except KeyError: #use rows
            G.nodes[ID]['cell_type1']  = None
    return G 


def extract_data(df, df_type):
    '''Extracts graph data and metadata from given dataframe df'''
    #Setup
    if df_type == 'syn_list':
        return extract_listdata(df)
    elif df_type == 'id_only':
        start_idx = 1
    elif df_type == "cellclass_connectome":
        df = fill_missing(df, True)
        start_idx = 2
    elif df_type == 'connectome':
        df = fill_missing(df)
        start_idx = 3
    cell_types = []
    for i in range(start_idx-1):
        cell_types.append((df.iloc[:, i], df.iloc[i, :]))
    ids = [df.iloc[:, start_idx-1], df.iloc[start_idx-1, :]]
    unique_ids = list(pd.concat((ids[0], ids[1])).dropna().unique())
    for i in range(len(ids)):
        ids[i] = pd.Series(ids[i].index.values, index=ids[i]) #flips id series so that each ID looks up a dataframe index
    
    #Graph
    G = nx.DiGraph()
    G.add_nodes_from(unique_ids)
    for idi in unique_ids:
        for idj in unique_ids:
            try:
                edge_weight = df.iat[ids[0][idi], ids[1][idj]]
            except KeyError:
                continue #skip misssing IDs
            if(not(np.isnan(edge_weight))):
                    G.add_edge(idi, idj, weight=edge_weight)

    #Metadata
    for ID in unique_ids:
        G.nodes[ID]['original_id'] = ID
        
        j = 0
        while(ord(ID[-1-j]) >= 48 and ord(ID[-1-j]) <= 57): #last character is a digit 0-9
            j += 1
            
        if(ID[-1-j]=='L'):
            G.nodes[ID]['hemisphere'] = 'left'
            try:
                if(ID[-1-j-1]=='D' or ID[0]=='d'):
                    G.nodes[ID]['dorsoventral'] = 'dorsal'
                elif(ID[-1-j-1]=='V' or ID[0]=='v'):
                    G.nodes[ID]['dorsoventral'] = 'ventral'
                else:
                    G.nodes[ID]['dorsoventral'] = None
            except IndexError:
                G.nodes[ID]['dorsoventral'] = None
                
        elif(ID[-1-j]=='R'):
            G.nodes[ID]['hemisphere'] = 'right'
            
            try:
                if(ID[-1-j-1]=='D' or ID[0]=='d'):
                    G.nodes[ID]['dorsoventral'] = 'dorsal'
                elif(ID[-1-j-1]=='V' or ID[0]=='v'):
                    G.nodes[ID]['dorsoventral'] = 'ventral'
                else:
                    G.nodes[ID]['dorsoventral'] = None
            except IndexError:
                G.nodes[ID]['dorsoventral'] = None
        
        elif(ID[-1-j]=='D'):
            G.nodes[ID]['dorsoventral'] = 'dorsal'
        elif(ID[-1-j]=='V'):
            G.nodes[ID]['dorsoventral'] = 'ventral'
        else:
            G.nodes[ID]['hemisphere'] = None
            G.nodes[ID]['dorsoventral'] = None
        for cell_idx in range(len(cell_types)):
            cell_type = cell_types[cell_idx]
            try: #using rows (column of IDs)
                G.nodes[ID]["cell_type"+str(cell_idx)] = cell_type[0][ids[0][ID]]
            except KeyError: #use columns
                G.nodes[ID]['cell_type'+str(cell_idx)] = cell_type[1][ids[1][ID]]
        max_start_idx = 3
        for cell_idx in range(max_start_idx - start_idx):
            try: #using rows (column of IDs)
                G.nodes[ID]['cell_type'+str(max_start_idx-cell_idx-2)] = None
            except KeyError: #use columns
                G.nodes[ID]['cell_type'+str(max_start_idx-cell_idx-2)] = None
    return G

def extract_filedata(dfs, df_type):
    '''
    Takes list of dataframes corresponding to a specific file and outputs a list of networkx
    graphs that contain adjacency matrices and associated metadata.
    '''
    graphs = []
    if df_type in {'connectome', 'cellclass_connectome'}:
        title_n_legend = dfs[0]
        title_info = title_n_legend.iat[0, 0]+"\n"+title_n_legend.iat[1, 0]
        for df in dfs[1:]:
            graphs.append(extract_data(df, df_type))
    elif df_type in {'syn_adj', 'syn_list'}:
        title_n_legend = dfs[-1]
        title_info = title_n_legend.iat[0, 0]
        if df_type == 'syn_adj':
            for df in dfs[:2]:
                graphs.append(extract_data(df, "connectome"))
            for df in dfs[2:-1]:
                graphs.append(extract_data(df, "id_only"))
        else: #syn_list
            for df in dfs[:-1]:
                graphs.append(extract_data(df, df_type))
    else: #nerve&ganglion
        for df in dfs:
            graphs.append(extract_data(df, 'id_only'))
    
    #Adding whole-graph attributes
    for i in range(len(graphs)):
        g = graphs[i]
        if df_type == 'nerve&ganglion':
            if i == 0:
                g.graph['Title'] = "Adult nerve ring neighbors"
            else:
                g.graph['Title'] = "L4 nerve ring neighbors"
        else:
            g.graph['Title'] = title_info
            if df_type in {'connectome', 'cellclass_connectome'}:
                num_sex = 3
            elif df_type == 'syn_adj':
                num_sex = 2
            elif df_type == 'syn_list':
                num_sex = 1
            if i < num_sex:
                g.graph['Sex'] = "Hermaphrodite"
            else:
                g.graph['Sex'] = "Male"
            if df_type != 'syn_list':
                if i % num_sex == 0:
                    g.graph['Synapse Type'] = "Chemical"
                elif df_type in {'connectome', 'cellclass_connectome'}:
                    if i == 1 or i == 4:
                        g.graph['Synapse Type'] = "Asymmetric Gap Junction"
                    else:
                        g.graph['Synapse Type'] = "Symmetric Gap Junction"
                else:
                    g.graph['Synapse Type'] = "Gap Junction"
    graphs = make_consistent(graphs)
    return graphs

def worm_wiring():
    file_dfs = pull_worm()
    graphs = []
    graph_lengths = {}
    for file, dfs in file_dfs.items():
        if file == "cellclass_connectome":
            continue
        filegraphs = extract_filedata(dfs, file)
        graph_lengths[file] = (len(graphs), len(filegraphs))
        graphs += filegraphs
    graphs = make_consistent(graphs)
    worm_graphs = {}
    for file in file_dfs:
        if file == "cellclass_connectome":
            continue
        i = graph_lengths[file][0]
        j = graph_lengths[file][1]
        worm_graphs[file] = (graphs[i:int(i+j/2)], graphs[int(i+j/2):(i+j)])
    cellclass_graphs = extract_filedata(file_dfs['cellclass_connectome'], "cellclass_connectome")
    worm_graphs["cellclass_connectome"] = (cellclass_graphs[:3], cellclass_graphs[3:])
    return worm_graphs