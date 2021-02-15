#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 11:22:51 2021

@author: pauladkisson

Purpose: Validates results of worm_wiring.py
"""

import pandas as pd
import numpy as np
from worm_wiring import fill_missing

def validate_synlist(dfs, graphs):
    '''validates the synlist file graphs'''
    for i in range(len(graphs)): 
        g = graphs[i]
        df = dfs[i]
        pre_ids = df.iloc[1:, 2]
        post1_ids = df.iloc[1:, 7]
        post2_ids = df.iloc[1:, 8]
        post3_ids = df.iloc[1:, 9]
        post4_ids = df.iloc[1:, 10]
        unique_ids = list(pd.concat((pre_ids, post1_ids, post2_ids, post3_ids, post4_ids)).dropna().unique())
        id2node = {unique_ids[i]:i for i in range(len(unique_ids))}
        pre_ids = pd.Series(pre_ids.index.values, index=pre_ids)
        
        #Node Metadata
        for j in range(len(g.nodes)):
            if g.nodes[j]['Hemisphere'] == 'Left':
                assert g.nodes[j]['ID'][-1] == 'L'
            elif g.nodes[j]['Hemisphere'] == 'Right':
                assert g.nodes[j]['ID'][-1] == 'R'
        
        #Graph data and edge metadata
        for j in range(1, df.shape[0]):
            pre_id = df.iloc[j, 2]
            post1_id = df.iloc[j, 7]
            post2_id = df.iloc[j, 8]
            post3_id = df.iloc[j, 9]
            post4_id = df.iloc[j, 10]
            continNum = df.iloc[j, 0]
            EMseries = df.iloc[j, 1]
            synapse_type = df.iloc[j, 4]
            sections = df.iloc[j, 5]
            pre_node = id2node[pre_id]
            try:
                post1_node = id2node[post1_id]
                edge_id = (pre_node, post1_node)
                try:
                    assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge1 existence validation" %j
                    assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge1 synapse_type validation" %j
                    assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge1 sections validation" %j
                except AssertionError: #catching duplicates
                    EMseries += "+"
                    try:
                        assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge1 existence validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge1 synapse_type validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge1 sections validation" %j
                    except AssertionError: #catching triplicates
                        EMseries += "+"
                        assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge1 existence validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge1 synapse_type validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge1 sections validation" %j
            except KeyError:
                assert np.isnan(post1_id), "Index %s failed post1 validation" %j

            try:
                post2_node = id2node[post2_id]
                edge_id = (pre_node, post2_node)
                try:
                    assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge2 existence validation" %j
                    assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge2 synapse_type validation" %j
                    assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge2 sections validation" %j
                except AssertionError:
                    EMseries += "+"
                    try:
                        assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge2 existence validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge2 synapse_type validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge2 sections validation" %j
                    except AssertionError:
                        EMseries += "+"
                        assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge2 existence validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge2 synapse_type validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge2 sections validation" %j
            except KeyError:
                assert np.isnan(post2_id), "Index %s failed post2 validation" %j

            try:
                post3_node = id2node[post3_id]
                edge_id = (pre_node, post3_node)
                try:
                    assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge3 existence validation" %j
                    assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge3 synapse_type validation" %j
                    assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge3 sections validation" %j
                except AssertionError:
                    EMseries += "+"
                    try:
                        assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge3 existence validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge3 synapse_type validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge3 sections validation" %j
                    except AssertionError:
                        EMseries += "+"
                        assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge3 existence validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge3 synapse_type validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge3 sections validation" %j
            except KeyError:
                assert np.isnan(post3_id), "Index %s failed post3 validation" %j

            try:
                post4_node = id2node[post4_id]
                edge_id = (pre_node, post4_node)
                try:
                    assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge4 existence validation" %j
                    assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge4 synapse_type validation" %j
                    assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge4 sections validation" %j
                except AssertionError:
                    EMseries += "+"
                    try:
                        assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge4 existence validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge4 synapse_type validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge4 sections validation" %j
                    except AssertionError:
                        EMseries += "+"
                        assert g.has_edge(edge_id[0], edge_id[1], (continNum, EMseries)), "Index %s failed edge4 existence validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["synapse_type"] == synapse_type, "Index %s failed edge4 synapse_type validation" %j
                        assert g.edges[edge_id[0], edge_id[1], (continNum, EMseries)]["sections"] == sections, "Index %s failed edge4 sections validation" %j
            except KeyError:
                assert np.isnan(post4_id), "Index %s failed post4 validation" %j

def validate_connectome(g, cell_types, nodenums, ids, i, l):
    cell_type0 = cell_types[0]
    cell_type1 = cell_types[1]
    if cell_type0[l]:
        if g.nodes[nodenums[l]]['cell_type0'] == g.nodes[nodenums[l]]['cell_type1']: #Dealing with switched type/subtypes
            assert cell_type0[l] == g.nodes[nodenums[l]]['cell_type0'] or cell_type1[l] == g.nodes[nodenums[l]]['cell_type0'],\
            "Node %s in graph %s with ID %s failed cell_type0/1 validation" % (nodenums[l], i, ids[l])
        else:
            if g.nodes[nodenums[l]]['cell_type0'] == 'SEX SPECIFIC' or g.nodes[nodenums[l]]['cell_type0'] == 'SEX-SPECIFIC CELLS' or g.nodes[nodenums[l]]['cell_type0'] == 'SEX-SPECIFIC': #Aliases are ok
                assert cell_type0[l] == 'SEX SPECIFIC' or cell_type0[l] == 'SEX-SPECIFIC CELLS' or cell_type0[l]=='SEX-SPECIFIC',\
                "Node %s in graph %s with ID %s failed SEX SPECIFIC cell_type0 validation" % (nodenums[l], i, ids[l])
            else:
                if cell_type0[l] == 'SENSOSRY NEURONS': #catching typo
                    assert g.nodes[nodenums[l]]['cell_type0'] == 'SENSORY NEURONS',\
                    "Node %s in graph %s with ID %s failed cell_type0 validation" % (nodenums[l], i, ids[l])
                else:
                    assert cell_type0[l] == g.nodes[nodenums[l]]['cell_type0'],\
                    "Node %s in graph %s with ID %s failed cell_type0 validation" % (nodenums[l], i, ids[l])
        if cell_type1[l]:
            if g.nodes[nodenums[l]]['cell_type1'] == 'BODY MOTOR NEURONS' or g.nodes[nodenums[l]]['cell_type1'] =='VENTRAL CORD MOTOR NEURONS': #Aliases are ok
                assert cell_type1[l] == 'BODY MOTOR NEURONS' or cell_type1[l] == 'VENTRAL CORD MOTOR NEURONS',\
                "Node %s in graph %s with ID %s failed BODY MOTOR NEURONS cell_type1 validation" % (nodenums[l], i, ids[l])
            else:
                if ids[l]=='um2AL' or ids[l]=='um2AR': #These IDs have different cell_type1's in rows vs columns - either is fine
                    assert g.nodes[nodenums[l]]['cell_type1'] == 'MUSCLES' or g.nodes[nodenums[l]]['cell_type1'] == 'MOTOR NEURONS',\
                    "Node %s in graph %s with ID '%s' failed cell_type1 validation" % (nodenums[l], i, ids[l])
                elif ids[l] in {'HSNL', 'HSNR', 'VC01', 'VC02', 'VC03', 'VC04', 'VC05', 'VC06'}: #These IDs have different cell_type1's in rows vs columns - either is fine
                    assert g.nodes[nodenums[l]]['cell_type1'] in {'SEX-SPECIFIC', 'MOTOR NEURONS'},\
                    "Node %s in graph %s with ID '%s' failed cell_type1 validation" % (nodenums[l], i, ids[l])
                else:
                    assert cell_type1[l] == g.nodes[nodenums[l]]['cell_type1'],\
                    "Node %s in graph %s with ID '%s' failed cell_type1 validation" % (nodenums[l], i, ids[l])

def validate_cellclass(g, cell_types, nodenums, ids, i, l):
    cell_type0 = cell_types[0]
    if cell_type0[l]:
        try:
            assert cell_type0[l] == g.nodes[nodenums[l]]['cell_type0'],\
            "Node %s in graph %s with ID %s failed cell_type0 validation" % (nodenums[l], i, ids[l])
        except AssertionError:
            if ids[l]=='RIA': #known inconsistency
                assert g.nodes[nodenums[l]]['cell_type0'] == 'IN1', \
                    "Node %s in graph %s with ID %s failed RIA cell_type0 validation" % (nodenums[l], i, ids[l])
            elif ids[l] == 'SAB': #known typo
                assert g.nodes[nodenums[l]]['cell_type0'] == 'SMN', \
                "Node %s in graph %s with ID %s failed SAB cell_type0 validation" % (nodenums[l], i, ids[l])
            else:
                print("cell_type0[l]=", cell_type0[l])
                print("g.nodes[nodenums[l]]['cell_type0']=", g.nodes[nodenums[l]]['cell_type0'])
                raise AssertionError

def valid_worm(dfs, graphs, df_type):
    if df_type == 'syn_list':
        return validate_synlist(dfs, graphs)
    elif df_type == 'id_only':
        start_idx = 1
    for i in range(len(graphs)):
        #Setup
        g = graphs[i]
        df = dfs[i]
        if i==0 and df_type=="nerve&ganglion":
            df = df.drop(df.tail(1).index) #drop the last row
            df = df.drop(df.columns[-1], axis=1) #drop the last column
            start_idx = 1
        elif df_type == "cellclass_connectome":
            df = fill_missing(df, True)
            start_idx = 2
        elif df_type == 'connectome':
            df = fill_missing(df)
            start_idx = 3
        ids = [df.iloc[:, start_idx-1], df.iloc[start_idx-1, :]]
        unique_ids = list(pd.concat((ids[0], ids[1])).dropna().unique())
        id2nodenum = {unique_ids[i]:i for i in range(len(unique_ids))}
    
        for j in range(start_idx, df.shape[0]):
            for k in range(start_idx, df.shape[1]):
                ids = (df.iat[j, start_idx-1], df.iat[start_idx-1, k])
                cell_types = []
                for cell_idx in range(start_idx-1):
                    cell_types.append((df.iat[j, cell_idx], df.iat[cell_idx, k]))
                edge_weight = df.iat[j, k]
                nodenums = [id2nodenum[ids[l]] for l in range(2)]
                
                #df_type-specific metadata validation
                for l in range(2):
                    if df_type == "connectome":
                        validate_connectome(g, cell_types, nodenums, ids, i, l)
                    elif df_type == "cellclass_connectome":
                        validate_cellclass(g, cell_types, nodenums, ids, i, l)
                
                #Graph validation
                if np.isnan(edge_weight): #graph has no edge at test_idx
                    assert g.has_edge(nodenums[0], nodenums[1]) == False,\
                    "Node pair (%s, %s) in graph %s with IDs (%s, %s) failed edge existence validation" %(nodenums[0], nodenums[1], i, ids[0], ids[1])
                else:
                    assert g.has_edge(nodenums[0], nodenums[1]) == True,\
                    "Node pair (%s, %s) in graph %s with IDs (%s, %s) failed edge existence validation" %(nodenums[0], nodenums[1], i, ids[0], ids[1])
                    assert g.edges[nodenums[0], nodenums[1]]['weight'] == edge_weight,\
                    "Node pair (%s, %s) in graph %s with IDs (%s, %s) failed edge weight validation" %(nodenums[0], nodenums[1], i, ids[0], ids[1])
                        
        #Hemisphere validation
        for j in range(len(g.nodes)):
            if g.nodes[j]['Hemisphere'] == 'Left':
                assert g.nodes[j]['ID'][-1] == 'L'
            elif g.nodes[j]['Hemisphere'] == 'Right':
                assert g.nodes[j]['ID'][-1] == 'R'

def validate_worm(file_dfs, worm_graphs):
    '''Calls valid_worm() for each list of graphs in worm_graphs with the appropriate inputs'''
    for file, graph_pair in worm_graphs.items():
        dfs = file_dfs[file]
        if file in {"connectome", "cellclass_connectome"}:
            valid_worm(dfs[1:], graph_pair[0]+graph_pair[1], file)
        elif file == "nerve&ganglion":
            valid_worm(dfs, graph_pair[0]+graph_pair[1], file)
        elif file == 'syn_adj':
            valid_worm(dfs[:2], graph_pair[0], "connectome")
            valid_worm(dfs[2:4], graph_pair[1], "id_only")
        elif file == "syn_list":
            valid_worm(dfs[:-1], graph_pair[0]+graph_pair[1], file) 