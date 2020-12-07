# author Spencer Loggia
# NeuroData Lab
from typing import List, Tuple, Union

import networkx as nx
import numpy as np
import pandas as pd
import shutil, os, sys, json, itertools
import re


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


class Metagraph:
    """
    Wrapper for networkx `Graph` or `DiGraph` object. Provides methods for writing to / loading from file.
    Limitations - networkx graph's nodes must be either int or string. Multigraphs are represented as lists of
    graphs.
    """

    def __init__(
            self,
            graphs: List[Union[nx.Graph, nx.DiGraph]] = None,
            edge_att_names: List[set] = None,
            node_att_names: List[set] = None,
            interpolate_att = False,
    ):
        # nodes must be basic data types
        if graphs is None:
            self.nx_obj = []
            self.edge_att_names = []
            self.node_att_names = []
        else:
            self.nx_obj = graphs
            if edge_att_names is None and interpolate_att:
                # find edge attributes names if not provided.
                self.edge_att_names = []
                for graph in graphs:
                    self.edge_att_names.append(
                        set(itertools.chain(*[list(graph.edges[n].keys()) for n in graph.edges()]))
                    )
            else:
                self.edge_att_names = edge_att_names
            if node_att_names is None and interpolate_att:
                self.node_att_names = []
                for graph in graphs:
                    self.node_att_names.append(
                        set(itertools.chain(*[list(graph.nodes[n].keys()) for n in graph.nodes()]))
                    )
            else:
                self.node_att_names = node_att_names

    def _serializable_atts(self, atts: dict) -> dict:
        new_dict = dict()
        for key in list(atts.keys()):
            new_dict[str(key)] = atts[key]
        return new_dict

    def _clear(self):
        self.nx_obj = []
        self.edge_att_names = []
        self.node_att_names = []

    def get_adjacency(self, return_node_attributes=True, return_edge_attributes=True) -> \
            List[np.ndarray] or List[np.ndarray, dict] or List[np.ndarray, dict, dict]:
        """
        gets the dense representation of all graphs' adjacency matrices as list of numpy arrays, and provides lists of
        node / edge attributes mapped to indexes in adjacency matrix.
        :return: np.ndarray
        """
        adj_mats = []
        edge_atts = []
        node_atts = []
        for i in range(len(self.nx_obj)):
            graph = self.nx_obj[i]
            conv = nx.convert_node_labels_to_integers(graph, ordering="sorted")
            adj_mats.append(nx.to_numpy_array(conv, dtype=np.int32))
            if return_edge_attributes:
                edge_atts.append({})
                if self.edge_att_names is not None:
                    for eatt in self.edge_att_names[i]:
                        edge_atts[-1][eatt] = nx.get_edge_attributes(conv, eatt)
            if return_node_attributes:
                node_atts.append({})
                if self.node_att_names is not None:
                    for natt in self.node_att_names[i]:
                        node_atts[-1][natt] = nx.get_node_attributes(conv, natt)
        to_return = [adj_mats]
        if return_node_attributes:
            to_return.append(node_atts)
        if return_edge_attributes:
            to_return.append(edge_atts)
        return to_return

    def dump(self, path: str):
        """
        Write graph to disk at specified path.
        :param path: path to write to, without extension
        :return: None
        """

        uuid = "{:4}".format(np.random.randint(0, 9999))
        tmpdir = "./tmp" + uuid
        os.mkdir(tmpdir)
        index = 0
        for graph in self.nx_obj:
            gpath = os.path.join(tmpdir, "graph_" + str(index))
            os.mkdir(gpath)
            nx.to_pandas_edgelist(graph)[["source", "target"]].to_csv(
                os.path.join(gpath, "edgelist.csv")
            )
            if self.node_att_names is not None:
                for n_att in self.node_att_names[index]:
                    ndict = nx.get_node_attributes(graph, n_att)
                    json.dump(
                        ndict, open(os.path.join(gpath, "nodeatt_" + n_att + ".json"), "w")
                    )
            if self.edge_att_names is not None:
                for e_att in self.edge_att_names[index]:
                    edict = self._serializable_atts(nx.get_edge_attributes(graph, e_att))
                    json.dump(
                        edict, open(os.path.join(gpath, "edgeatt_" + e_att + ".json"), "w")
                    )
            index += 1
        shutil.make_archive(
            base_name=path, format="zip", root_dir=tmpdir, base_dir="./"
        )
        os.rename(path + '.zip', path)
        shutil.rmtree(tmpdir)

    def load(self, path: str):
        """
        load metagraph from disk.
        :param path: location of graph file.
        """
        uuid = "{:4}".format(np.random.randint(0, 9999))
        tmpdir = "./tmp" + uuid
        os.mkdir(tmpdir)
        # remove existing data
        self._clear()
        try:
            shutil.unpack_archive(filename=path, extract_dir=tmpdir, format="zip")
        except Exception:
            raise IOError("Failed to read graph from disk.")
        for graph_dir in sorted(os.listdir(tmpdir)):
            edgelist = pd.read_csv(os.path.join(tmpdir, graph_dir, "edgelist.csv"))
            g = nx.from_pandas_edgelist(edgelist)
            e_att_names = []
            n_att_names = []
            for file in os.listdir(os.path.join(tmpdir, graph_dir)):
                if file != "edgelist.csv":
                    attname = re.split("_|\.", file)[1]
                    if "edgeatt" in file:
                        att = _get_att_from_json(
                            os.path.join(tmpdir, graph_dir, file), evaluate_keys=True
                        )
                        nx.set_edge_attributes(g, att, attname)
                        e_att_names.append(attname)
                    elif "nodeatt" in file:
                        att = _get_att_from_json(
                            os.path.join(tmpdir, graph_dir, file), evaluate_keys=True
                        )
                        nx.set_node_attributes(g, att, attname)
                        n_att_names.append(attname)
            self.edge_att_names.append(set(e_att_names))
            self.node_att_names.append(set(n_att_names))
            self.nx_obj.append(g)
        shutil.rmtree(tmpdir)
