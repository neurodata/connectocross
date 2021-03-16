#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 14:52:56 2021

@author: pauladkisson

Purpose: Call worm_wiring to obtain graphs,
        validate graphs using validate_worm,
        and store worm_wiring graphs in file spec using graph_io
"""

from worm_wiring import worm_wiring as ww, validate_worm as vw
from graph import GraphIO

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
        GraphIO.dump(filegraphs[0], "worm_wiring/graphs/%s/Adult.mgraph" % file)
        GraphIO.dump(filegraphs[1], "worm_wiring/graphs/%s/L4.mgraph" % file)
    elif file == 'syn_list':
        continue #Waiting for Spencer's MultiDigraph --> list of DiGraphs code
    else:
        for i in range(len(filegraphs)):
            sex = filegraphs[i][0].graph['Sex']
            GraphIO.dump(filegraphs[i], "worm_wiring/graphs/%s/%s.mgraph" % (file, sex))
    