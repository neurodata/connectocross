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
| Data | [Link to overview](https://temca2data.org/) [Link to CATMAID](https://fafb.catmaid.virtualflybrain.org/)|
| Raw data location | CATMAID |
| # nodes |  |
| # edges |  | 
| # synapses | |
| # graphs | 1 |

### Playnerius larva full 
|  |  |
|-------|----------|
| Paper | [Link](https://www.biorxiv.org/content/10.1101/2020.08.21.260984v2) |
| Data | not yet available |
| Raw data location | CATMAID |
| # nodes | 2728 |
| # edges | 11437 | 
| # synapses | | 
| # graphs | 1 |


## Simple a priori models

### Density (ER)

### Left/right (SBM/DCSBM)
- Test different hypotheses about $\hat{B}$

### Left/right + any known metadata (SBM/DCSBM)
- If any putative cell types are known, use those

### General low rank (RDPG)
- Scree plots, estimation of rank (ZG2)

### Distribution of weights, degrees

## More complicated a priori models

### Homotypic

### Testing left vs right, quantify correlation, spectral similarity, GM performance, etc.

### Testing for gaia's directedness (or just quantifying to what extent it happens)
- degree of reciprocal feedback/

## A posteriori models

### Spectral clustering and estimating an SBM, DCSBM, DDSBM
- can try any of these with homotypic also... or correlation L/R

### Feedforward layout and proportion of feedforward edges

## Models with biological metadata

### Testing for Peter's rule via the contact graph
- is the adjacency a noisy version of the contact graph?
- how does rank change as we jitter xyz of synapses

### Spectral clustering that uses morphology

### Configuration models that swap synapses within an epsilon ball

### Can we cluster edges via connectivity + space? 

## Niche models that may not work for all data 

### Different hypotheses for a multilayer SBM-like model
- maggot data

## Matching FAFB and hemibrain or either to maggot
- could be spectral, could be GM
- results maybe bad?
- could use morphology, could not

