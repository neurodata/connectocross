import itertools
import json
import os
import sys
import re
import shutil
from typing import List, Tuple, Union

import networkx as nx
import numpy as np
import pandas as pd


class GraphIO:
    """
    Class for IO with networkx `Graph` or `DiGraph` objects. Provides methods for writing to / loading from file.
    Limitations - networkx graph's nodes must be either int or string. Multigraphs are represented as lists of
    graphs.
    """

    @staticmethod
    def infer_edge_attributes(graph: Union[nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph]):
        # find edge attributes names if not provided.
        if type(graph) in [nx.MultiDiGraph, nx.MultiGraph]:
            edge_att_names = set(itertools.chain(*[list(graph.edges[n].keys()) for n in graph.edges(keys=True)]))
        else:
            edge_att_names = set(itertools.chain(*[list(graph.edges[n].keys()) for n in graph.edges()]))
        return edge_att_names

    @staticmethod
    def infer_node_attributes(graph: Union[nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph]):
        # find edge attributes names if not provided.
        node_att_names = set(itertools.chain(*[list(graph.nodes[n].keys()) for n in graph.nodes()]))
        return node_att_names

    @staticmethod
    def infer_graph_attributes(graph: Union[nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph]):
        graph_att_names = set(graph.graph.keys())
        return graph_att_names

    @staticmethod
    def convert_multigraph(mg: Union[nx.MultiDiGraph, nx.MultiGraph]) -> List[nx.DiGraph]:
        """
        Get a list of graphs specified by this multigraph
        """
        if type(mg) is nx.MultiGraph:
            g_class = nx.Graph
        elif type(mg) is nx.MultiDiGraph:
            g_class = nx.DiGraph
        else:
            raise TypeError("Must give a MultiGraph or MultiDiGraph to convert_multigraph")
        key_map = {}
        graphs = []
        for edge in mg.edges(data=True, keys=True):
            link = tuple(edge[:2])
            key = edge[2]
            data = edge[3]
            if key not in key_map:
                graphs.append(g_class())
                graphs[-1].add_nodes_from(mg.nodes(data=True))
                key_map[key] = len(graphs) - 1
            ind = key_map[key]
            graphs[ind].add_edge(link[0], link[1])
            for key in data:
                graphs[ind].edges[link][key] = data[key]
        return graphs

    @classmethod
    def dump(cls,
             graph: Union[nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph],
             path: str):
        """
        Write graph to disk at specified path.
        :param graph: the graph or list of graphs to dump
        :param path: path to write to, without extension
        :return: None
        """

        node_att_names = cls.infer_node_attributes(graph)
        edge_att_names = cls.infer_edge_attributes(graph)
        graph_att_names = cls.infer_graph_attributes(graph)
        all_att = node_att_names | edge_att_names | graph_att_names
        reserved = {'id', 'source', 'target', 'key'}

        if len(reserved.intersection(all_att)) > 0:
            raise KeyError("Keywords id, source, target, and key are reserved in this format. Any attributes using "
                           "these keywords must be renamed")

        if False in [type(n) == str for n in all_att]:
            print("WARNING: Non-string attribute names detected. "
                  "These will be converted to strings for json compliance", sys.stderr)
        try:
            node_link = nx.readwrite.node_link_data(graph)
        except nx.NetworkXError:
            raise KeyError("Node link map is corrupted")

        with open(path, 'w') as f:
            json.dump(node_link, f)

    @classmethod
    def load(cls, path: str) -> Tuple[List[Union[nx.Graph, nx.DiGraph]],
                                      List[set],
                                      List[set],
                                      List[set]]:
        """
        load metagraph from disk.
        :param path: location of graph file.

        :return (graph object, edge attributes, node attributes, graph attributes)
        """
        with open(path, 'r') as f:
            data_dict = json.load(f)

        try:
            graph = nx.readwrite.node_link_graph(data_dict)
        except nx.NetworkXError:
            raise IOError("Unable to graph. Make sure the file is not corrupted, and"
                          "uses the standard source, target, id, and key field names")

        e_att_names = cls.infer_edge_attributes(graph)
        n_att_names = cls.infer_node_attributes(graph)
        g_att_names = cls.infer_graph_attributes(graph)

        return graph, e_att_names, n_att_names, g_att_names
