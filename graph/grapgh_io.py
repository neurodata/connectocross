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
    Class for IO with networkx `Graph`,  `DiGraph`, `MultiGraph`, or `MultiDiGraph` objects. Provides functions for
    writing to / loading from JSON file, as well as for converting to other graph representations.
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
    def multigraph_to_list(mg: Union[nx.MultiDiGraph, nx.MultiGraph]) -> List[nx.DiGraph]:
        """
        Get a list of graphs specified by this multigraph.
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

    @staticmethod
    def list_to_multigraph(graphs: List[Union[nx.Graph, nx.DiGraph]]) -> Union[nx.MultiGraph, nx.MultiDiGraph]:
        """
        Get a nx MultiGraph or MultiDiGraph from list of nx Graphs or DiGraphs.
        """
        if type(all(graphs)) is nx.Graph:
            multi_graph = nx.MultiGraph
        elif type(all(graphs)) is nx.DiGraph:
            multi_graph = nx.MultiDiGraph
        else:
            raise TypeError
        nodes = [set(g.nodes(data=True)) for g in graphs]
        nodes = set.union(*nodes)
        multi_graph.add_nodes_from(nodes)
        for i, g in enumerate(graphs):
            for source, target, data in g.edges(data=True):
                multi_graph.add_edge(source, target, key=i, attr_dict=data)
        return multi_graph


    @classmethod
    def get_adjacency_representation(cls, graph: Union[nx.Graph, nx.DiGraph, nx.MultiDiGraph, nx.MultiGraph]):
        """
        Get the graph as an adjacency matrix, a list of node attribute DataFrames, and a list of edge attribute
        DataFrames. If a multigraph is passed, it will be converted to a list of graphs, and a list of each of those
        will be returned. Node labels are added to the node attribute DataFrame with attribute name
        `original_node_label`

        :param graph: nx.Graph, nx.DiGraph, nx.MultiDiGraph, nx.MultiGraph

        :return: If a Graph or Digraph is given:
                    return Tuple[adjacency: ndarray,
                                node_attributes: DataFrame,
                                edge_attributes: DataFrame]

                 If a MultiGraph or MultiDiGraph is given:
                    return Tuple[List[adjacency: ndarray, ...],
                                List[node_attributes: DataFrame, ...],
                                List[edge_attributes: DataFrame, ...]]

                node labels are added to the node_attribute DataFrame with attribute name `original_node_label`
        """
        adj_out = []
        node_out = []
        edge_out = []
        if type(graph) in [nx.MultiGraph, nx.MultiDiGraph]:
            graph = cls.multigraph_to_list(graph)
        else:
            graph = [graph]

        for g in graph:
            np_adj = nx.to_numpy_matrix(g, weight='weight')
            adj_out.append(np_adj)
            ids = g.nodes()
            g = nx.convert_node_labels_to_integers(g)
            edge_data = g.edges(data=True)
            edge_data = {tuple(e[:2]): e[2] for e in edge_data}
            node_data = g.nodes(data=True)
            node_data = {n[0]: n[1] for n in node_data}
            for n, i in enumerate(ids):
                node_data[i]['original_node_label'] = n
            node_out.append(pd.DataFrame.from_dict(node_data, orient='index'))
            edge_out.append(pd.DataFrame.from_dict(edge_data, orient='index'))

        if len(adj_out) == 1:
            return adj_out[0], node_out[0], edge_out[0]
        else:
            return adj_out, node_out, edge_out

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
    def load(cls, path: str) -> Tuple[Union[nx.Graph, nx.DiGraph], set, set, set]:
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


if __name__ == '__main__':
    g = nx.generators.star_graph(10)
    bb = nx.betweenness_centrality(g)
    nx.set_node_attributes(g, bb, "betweenness")
    att = {(0, 1): "red",
           (0, 2): "blue",
           (0, 5): "red",
           (0, 8): "blue"}
    nx.set_edge_attributes(g, att, "color")
    adj, node, edge = GraphIO.get_adjacency_representation(g)
