from typing import List

import networkx as nx
from graspologic.models import SBMEstimator
from graspologic.plot import heatmap
from matplotlib import pyplot as plt
from graph import GraphIO

from itertools import chain, combinations


def fit_apriori_sbm(connectome: nx.DiGraph, group: List[str], plot_sbms=True):
    """
    Finds BIC, liklihhods for sbm fit to different attr groups.
    :param connectome:
    :param single_keys:
    :param plot_sbms:
    :return:
    """
    adj, node_atts, edge_atts = GraphIO.get_adjacency_representation(connectome)
    adj = adj / adj.mean()
    adj[adj > .01] = 1
    adj[adj <= .01] = 0

    group = list(group)
    groupby = node_atts.groupby(group)
    group_data = groupby.groups
    unq_keys = list(sorted(group_data.keys(), key=lambda x: str(x)))
    for i, key in enumerate(unq_keys):
        if type(key) is not tuple:
            unq_keys[i] = tuple([key])
    group_map = dict(zip(unq_keys, range(len(unq_keys))))
    if len(unq_keys) > 1:
        node_atts['_group'] = list(node_atts[group].itertuples(index=False, name=None))
    else:
        node_atts['_group'] = node_atts[group]
    node_atts["_group_id"] = node_atts["_group"].map(group_map)
    node_atts["_group_id"].fillna(max(node_atts["_group_id"]) + 1, inplace=True)

    Model = SBMEstimator
    estimator = Model(directed=True, loops=False)
    estimator.fit(adj, y=node_atts["_group_id"].values)

    if plot_sbms:
        _ = heatmap(adj,
                    inner_hier_labels=node_atts["_group_id"].values,
                    title="True adjacency " + str(group),
                    font_scale=.5,
                    sort_nodes=True)

        _ = heatmap(estimator.sample()[0],
                    inner_hier_labels=node_atts["_group_id"].values,
                    title="SBM fit " + str(group),
                    font_scale=.5,
                    sort_nodes=True)

        print(group_map)

    estimator.n_verts = len(adj)
    bic = estimator.bic(adj)
    liklihood = estimator.score(adj)
    n_params = estimator._n_parameters()
    row = {
        "bic": -bic,
        "liklihood": liklihood,
        "n_params": n_params,
        "estimator": estimator
    }
    return row