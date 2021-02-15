#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 11:33:23 2021

@author: pauladkisson

Purpose: Run worm_wiring and validate_worm
"""

from worm_wiring import worm_wiring
from validate_worm import validate_worm
from worm_wiring import pull_worm

graphs = worm_wiring()
file_dfs = pull_worm()
validate_worm(file_dfs, graphs)