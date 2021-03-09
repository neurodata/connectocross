#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 14:52:56 2021

@author: pauladkisson

Purpose: Call worm_wiring to obtain graphs,
        validate graphs using validate_worm,
        and store worm_wiring graphs in file spec using graph_io
"""

from worm_wiring import worm_wiring as ww, validate_worm
from graph import GraphIO

graphs = ww.worm_wiring()
file_dfs = ww.pull_worm()
validate_worm(file_dfs, graphs)
for file in graphs:
    GraphIO.dump([graphs[file][0], graphs[file][1]], "%s.mgraph" % file)