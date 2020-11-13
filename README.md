# Connectocross: statistical characterizations and comparisons of nanoscale connectomes across taxa

## Datasets
---

### C. elegans male and hermaphrodite, full body
|  |  |
|-------|----------|
| Paper | [Link](https://www.nature.com/articles/s41586-019-1352-7) |
| Data | [Link](https://wormwiring.org/) |
| Raw data location |  |
| # nodes | ~300 |
| # edges |  | 
| # synapses | | 
| # graphs | 2 |

Notes 
- has chemical and gap junction graphs

### C. elegans timeseries, nerve ring
|  |  |
|-------|----------|
| Paper | [Link](https://www.biorxiv.org/content/10.1101/2020.04.30.066209v2) |
| Data |  |
| Raw data location |  |
| # nodes | ~50 - 150 per graph?|
| # edges | | 
| # synapses | | 
| # graphs | 8 |

Notes
- time series of graphs (though from different animals)
- 2 animals at the last timepoint
- I have code to pull data

### Drosophila larva brain
|  |  |
|-------|----------|
| Paper | not yet available |
| Data | we have it |
| Raw data location | CATMAID |
| # nodes | 2971 |
| # edges | ~100k | 
| # synapses ~300k | 
| # graphs | 1 |

### Drosophila adult brain chunk (hemibrain)
|  |  |
|-------|----------|
| Paper | [Link](https://www.biorxiv.org/content/10.1101/2020.01.21.911859v1) |
| Data | [Link](https://www.janelia.org/project-team/flyem/hemibrain) |
| Raw data location | neuPrint |
| # nodes | 20 - 25k, 67k more small objects |
| # edges |  | 
| # synapses | 64M | 
| # graphs | 1 |

### Drosophila adult brain sparse (FAFB)
|  |  |
|-------|----------|
| Paper | [Link](https://www.cell.com/cell/fulltext/S0092-8674(18)30787-6) |
| Data | [Link to overview,](https://temca2data.org/) [Link to CATMAID](https://fafb.catmaid.virtualflybrain.org/)|
| Raw data location | CATMAID |
| # nodes |  |
| # edges |  | 
| # synapses | |
| # graphs | 1 |

### Playnerius larva full 
|  |  |
|-------|----------|
| Paper | [Link](https://www.biorxiv.org/content/10.1101/2020.08.21.260984v2) |
| Data | not yet available (I think) |
| Raw data location | CATMAID |
| # nodes | 2728 |
| # edges | 11437 | 
| # synapses | | 
| # graphs | 1 |

### MiCRONS
| | | 
|-------|--------|

### Bryan Jones Retina 

### Cionia intestinalis
| | |
|-------|--------|
| Paper | [Link](https://elifesciences.org/articles/16962) |
| Data | |
| # nodes | ~200? |
| # edges | |
| # synapses | |
| # graphs | | 




## Simple a priori models
a.k.a. look at the data, more or less

### Simplest statistics
Things that we always want to know about a graph. Usually: 
- Number of nodes
- Number of edges
- For a connectome, maybe number of actual synapses

### Density (ER)
- compute the density (p) for each connectome, can simply plot each.

### Left/right (SBM/DCSBM)
- Test different hypotheses about $\hat{B}$ (see statistical connectomics) 
   - is it more densely connected within block than between? To what extent?
      - maybe can compare this for many of the connectomes. probably not all
   - core-periphery
   - etc.

### Left/right + any known metadata (SBM/DCSBM)
- If any putative cell types are known, use those
- now we get a more refined SBM than the above, maybe interesting, maybe not? 
   - cell type data may not be available for all of the above
- can do similar tests, results may or may not be different

### General low rank (RDPG)
- Scree plots
- estimation of rank (ZG2)
- not sure that this will be interesting to compare across connectome or not. would
  have to normalize for the number of nodes somehow, i'd think.

### Distribution of weights, degrees
- Can just look at distribution of edge weight for each, i guess where weight is number of synapses
- in/out degree distribution, marginals and joint, is easy enough to plot.
   - again, don't know whether it'll be meaningful to compare across connectome or not

## More complicated a priori models

### Homotypic affinity
- can test for whether cell pairs (or blocks?) are more likely than chance to connect (homotypic affinity)
- requires having cell pairs
   - probably only maggot and c. elegans

### Testing left vs right, quantify correlation, spectral similarity, GM performance, etc.

### Testing for gaia's directedness (or just quantifying to what extent it happens)
- degree of reciprocal feedback? had thought about something along the lines of testing 
  for the difference between left and right latent positions. but maybe a simpler first
  statistic to compute is: P(edge from j to i | edge from i to j) 

## A posteriori models

### Spectral clustering and estimating an SBM, DCSBM, DDSBM
- can try to incorporate homotypic affinity also... or correlation L/R

### Feedforward layout and proportion of feedforward edges

## Models with biological metadata

### Testing for Peter's rule via the contact graph
- is the adjacency a noisy version of the contact graph?
- how does rank change as we jitter xyz of synapses
- could we also just swap synapses in an epsilon ball and see how structure changes?

### Spectral clustering that uses morphology

### Configuration models that swap synapses within an epsilon ball

### Can we cluster edges via connectivity + space? 
- had talked about trying to cluster the line graph 
- spectral embedding of the line graph looked bad when I tried it. Need to follow up.

## Niche models that may not work for all data 

### Different hypotheses for a multilayer SBM-like model
- maggot data

### Matching FAFB and hemibrain or either to maggot
- could be spectral, could be GM
- results maybe bad?
- could use morphology, could not

### Spectral coarsening between maggot and adult

