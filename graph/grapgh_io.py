import itertools
import json
import os
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
    def _serializable_atts(atts: dict) -> dict:
        new_dict = dict()
        for key in list(atts.keys()):
            new_dict[str(key)] = atts[key]
        return new_dict

    @staticmethod
    def _get_att_from_json(json_path: str, evaluate_keys=False) -> dict:
        raw_att = json.load(open(json_path, "r"))
        if not evaluate_keys:
            return raw_att
        new_dict = dict()
        for key in list(raw_att.keys()):
            if type(key) is str:
                new_key = eval(key)
                new_dict[new_key] = raw_att[key]
            else:
                raise IOError("Not able to evaluate json.")
        return new_dict

    @staticmethod
    def _gen_graph(graph_dir: str) -> Union[nx.Graph, nx.DiGraph]:
        try:
            edgelist = pd.read_csv(os.path.join(graph_dir, "edgelist.csv"))
        except Exception:
            raise IOError("each graph must have an associated edgelist")
        try:
            with open(os.path.join(graph_dir, 'graphatt_isDirected.json'), 'r') as f:
                line = f.readline()
                if 'true' in line:
                    g = nx.from_pandas_edgelist(edgelist, create_using=nx.DiGraph)
                elif 'false' in line:
                    g = nx.from_pandas_edgelist(edgelist, create_using=nx.Graph)
                else:
                    raise IOError("Reserved graph attribute isDirected is corrupted.")
        except FileNotFoundError:
            raise IOError("isDirected graph attribute must exist and be set.")
        return g

    @staticmethod
    def infer_edge_attributes(graphs: List[Union[nx.Graph, nx.DiGraph]]):
        # find edge attributes names if not provided.
        edge_att_names = []
        for graph in graphs:
            edge_att_names.append(
                set(itertools.chain(*[list(graph.edges[n].keys()) for n in graph.edges()]))
            )
        return edge_att_names

    @staticmethod
    def infer_node_attributes(graphs: List[Union[nx.Graph, nx.DiGraph]]):
        # find edge attributes names if not provided.
        node_att_names = []
        for graph in graphs:
            node_att_names.append(
                set(itertools.chain(*[list(graph.nodes[n].keys()) for n in graph.nodes()]))
            )
        return node_att_names

    @staticmethod
    def infer_graph_attributes(graphs: List[Union[nx.Graph, nx.DiGraph]]):
        # find graph attributes names if not provided.
        graph_att_names = []
        for graph in graphs:
            graph_att_names.append(
                set(graph.graph.keys())
            )
        return graph_att_names

    @classmethod
    def dump(cls,
             graph: List[Union[nx.Graph, nx.DiGraph]],
             path: str, edge_att_names: List[set] = None,
             node_att_names: List[set] = None,
             graph_att_names: List[set] = None):
        """
        Write graph to disk at specified path.
        :param graph: the graph or list of graphs to dump
        :param path: path to write to, without extension
        :param edge_att_names: optional, provide edge attribute names to dump, else will infer
        :param node_att_names: optional, provide node attribute names to dump, else will infer
        :param graph_att_names: optional, provide graph attribute names to dump, else will infer
        :return: None
        """

        uuid = "{:4}".format(np.random.randint(0, 9999))
        tmpdir = "./tmp" + uuid
        os.mkdir(tmpdir)
        if edge_att_names is None:
            edge_att_names = cls.infer_edge_attributes(graph)
        if node_att_names is None:
            node_att_names = cls.infer_node_attributes(graph)
        if graph_att_names is None:
            graph_att_names = cls.infer_graph_attributes(graph)

        for i, g in enumerate(graph):
            gpath = os.path.join(tmpdir, "graph_" + str(i))
            os.mkdir(gpath)
            nx.to_pandas_edgelist(g)[["source", "target"]].to_csv(
                os.path.join(gpath, "edgelist.csv")
            )
            for n_att in node_att_names[i]:
                ndict = nx.get_node_attributes(g, n_att)
                json.dump(
                    ndict, open(os.path.join(gpath, "nodeatt_" + n_att + ".json"), "w")
                )
            for e_att in edge_att_names[i]:
                edict = cls._serializable_atts(nx.get_edge_attributes(g, e_att))
                json.dump(
                    edict, open(os.path.join(gpath, "edgeatt_" + e_att + ".json"), "w")
                )
            for g_att in graph_att_names[i]:
                g_val = g.graph[g_att]
                json.dump(
                    g_val, open(os.path.join(gpath, "graphatt_" + g_att + ".json"), "w")
                )
            # add required isDirected graph attribute
            json.dump(
                (type(g) is nx.DiGraph),
                open(os.path.join(gpath, "graphatt_isDirected.json"), "w")
            )
        shutil.make_archive(
            base_name=path, format="zip", root_dir=tmpdir, base_dir="./"
        )
        os.rename(path + '.zip', path)
        shutil.rmtree(tmpdir)

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
        uuid = "{:4}".format(np.random.randint(0, 9999))
        tmpdir = "./tmp" + uuid
        os.mkdir(tmpdir)

        try:
            shutil.unpack_archive(filename=path, extract_dir=tmpdir, format="zip")
        except Exception:
            raise IOError("Failed to read graph from disk.")

        # to return attribute names.
        e_att_names = []
        n_att_names = []
        g_att_names = []

        # to hold graphs
        graphs = []

        # be sure we read graphs in order
        for graph_dir in sorted(os.listdir(tmpdir)):
            g = cls._gen_graph(os.path.join(tmpdir, graph_dir))
            e_att_names.append(set())
            n_att_names.append(set())
            g_att_names.append(set())
            for file in os.listdir(os.path.join(tmpdir, graph_dir)):
                if file != "edgelist.csv":
                    attname = re.split("_|\.", file)[1]
                    if "edgeatt" in file:
                        att = cls._get_att_from_json(
                            os.path.join(tmpdir, graph_dir, file), evaluate_keys=True
                        )
                        nx.set_edge_attributes(g, att, attname)
                        e_att_names[-1].add(attname)
                    elif "nodeatt" in file:
                        att = cls._get_att_from_json(
                            os.path.join(tmpdir, graph_dir, file), evaluate_keys=True
                        )
                        nx.set_node_attributes(g, att, attname)
                        n_att_names[-1].add(attname)
                    elif "graphatt" in file:
                        att = cls._get_att_from_json(
                            os.path.join(tmpdir, graph_dir, file), evaluate_keys=False
                        )
                        g.graph[attname] = att
                        g_att_names[-1].add(attname)
            graphs.append(g)
        shutil.rmtree(tmpdir)
        return graphs, e_att_names, n_att_names, g_att_names
