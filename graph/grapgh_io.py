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
    def _read_edgelist(graph_dir: str,
                       create_using=nx.Graph) -> Union[nx.Graph, nx.DiGraph]:
<<<<<<< HEAD
        path = os.path.join(graph_dir, 'edgelist.csv')
=======
        if os.path.isfile(os.path.join(graph_dir, 'edgelist.csv')):
            path = os.path.join(graph_dir, 'edgelist.csv')
        elif os.path.isfile(os.path.join(graph_dir, 'edgelist.symlink')):
            path = os.readlink(os.path.join(graph_dir, 'edgelist.symlink'))
        else:
            raise IOError("MGraph must contain an edgelist in each graph directory")
>>>>>>> 7b2e1195b2a0204f4e793d164e62ef246ae3605f
        try:
            g = nx.readwrite.read_weighted_edgelist(path,
                                                    create_using=create_using,
                                                    delimiter=',')
        except (ValueError, TypeError):
            g = nx.readwrite.read_edgelist(path, create_using=create_using,
                                           data=False,
                                           delimiter=',')
        return g


    @staticmethod
    def n_map(x: str):
        if type(x) is int or type(x) is float:
            return x
        if type(x) is str and x.isnumeric():
            try:
                x = int(x)
            except TypeError:
                x = float(x)
        return x

    @classmethod
    def _gen_graph(cls, graph_dir: str) -> Union[nx.Graph, nx.DiGraph]:
        try:
            with open(os.path.join(graph_dir, 'graphatt_isDirected.json'), 'r') as f:
                line = f.readline()
                if 'true' in line:
                    g = cls._read_edgelist(graph_dir, create_using=nx.DiGraph)
                elif 'false' in line:
                    g = cls._read_edgelist(graph_dir, create_using=nx.Graph)
                else:
                    raise IOError("Reserved graph attribute isDirected is corrupted.")
        except FileNotFoundError:
            raise IOError("isDirected graph attribute must exist and be set.")
        # convert any string representations of number
        g = nx.relabel_nodes(g, cls.n_map)
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

<<<<<<< HEAD

    @classmethod
    def dump(cls,
             graph: List[Union[nx.Graph, nx.DiGraph]],
=======
    @staticmethod
    def convert_multigraph(mg: Union[nx.MultiDiGraph, nx.MultiGraph]) -> List[nx.DiGraph]:
        key_map = {}
        graphs = []
        for edge in mg.edges(data=True, keys=True):
            link = tuple(edge[0][:2])
            key = edge[0][2]
            data = edge[1]
            if key not in key_map:
                graphs.append(nx.DiGraph())
                graphs[-1].add_nodes_from(mg.nodes(data=True))
                key_map[key] = len(graphs) - 1
            ind = key_map[key]
            graphs[ind].add_edge(link[0], link[1])
            for key in data:
                graphs[ind].edges(link)[key] = data[key]
        return graphs

    @classmethod
    def dump(cls,
             graph: List[Union[nx.Graph, nx.DiGraph, nx.MultiDiGraph]],
>>>>>>> 7b2e1195b2a0204f4e793d164e62ef246ae3605f
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
<<<<<<< HEAD
=======
        if type(graph) is nx.MultiDiGraph:
            graph = cls.convert_multigraph(graph)
>>>>>>> 7b2e1195b2a0204f4e793d164e62ef246ae3605f

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
            if 'weight' in edge_att_names[i]:
                nx.readwrite.write_weighted_edgelist(g,
                                                     os.path.join(gpath, "edgelist.csv"),
                                                     delimiter=',')
            else:
                nx.readwrite.write_edgelist(g,
                                            os.path.join(gpath, "edgelist.csv"),
                                            data=False,
                                            delimiter=',')
            for n_att in node_att_names[i]:
                ndict = nx.get_node_attributes(g, n_att)
                json.dump(
                    ndict, open(os.path.join(gpath, "nodeatt_" + n_att + ".json"), "w")
                )
            for e_att in edge_att_names[i]:
                if e_att == 'weight':
                    continue
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
<<<<<<< HEAD
                    attname = re.split("_|\.", file)[1]
                    if "edgeatt" in file:
                        att = cls._get_att_from_json(
                            os.path.join(tmpdir, graph_dir, file), evaluate_keys=True
=======
                    attname = ''.join(re.split("_|\.", file)[1:-1])
                    fpath = os.path.join(tmpdir, graph_dir, file)
                    if '.symlink' in file:
                        fpath = os.readlink(fpath)
                    if "edgeatt" in file:
                        att = cls._get_att_from_json(
                            fpath, evaluate_keys=True
>>>>>>> 7b2e1195b2a0204f4e793d164e62ef246ae3605f
                        )
                        nx.set_edge_attributes(g, att, attname)
                        e_att_names[-1].add(attname)
                    elif "nodeatt" in file:
                        att = cls._get_att_from_json(
<<<<<<< HEAD
                            os.path.join(tmpdir, graph_dir, file), evaluate_keys=True
=======
                            fpath, evaluate_keys=True
>>>>>>> 7b2e1195b2a0204f4e793d164e62ef246ae3605f
                        )
                        nx.set_node_attributes(g, att, attname)
                        n_att_names[-1].add(attname)
                    elif "graphatt" in file:
                        att = cls._get_att_from_json(
<<<<<<< HEAD
                            os.path.join(tmpdir, graph_dir, file), evaluate_keys=False
=======
                            fpath, evaluate_keys=False
>>>>>>> 7b2e1195b2a0204f4e793d164e62ef246ae3605f
                        )
                        g.graph[attname] = att
                        g_att_names[-1].add(attname)
            graphs.append(g)
        shutil.rmtree(tmpdir)
        return graphs, e_att_names, n_att_names, g_att_names
