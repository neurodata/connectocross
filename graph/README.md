## GRAPH and METADATA FILE SPECIFICATION
author: Spencer Loggia

This document outlines the graph storage protocol used by the GraphIO class. The purpose of this file spec is to provide an easily
human-readable way to store arbitrarily large attributed graph and multi-graph data. The modular nature of the format allows
user to load only the necessary data at any given time.

A single graph is stored as a directory with name "graph_*ID*" where *ID* is an identifying number. 

### Edgelist
Inside a graph directory there must be a file called "edgelist.csv" which has a source node column, a target node column, and an optional weight column. Node identifiers must be strings or numeric types.

### Metadata
Each graph's attributes are stored as json files within a graph's directory. They are named and stored as follows:

**Edge attributes:** 

- **Nomenclature**: "edgeatt_*ATTR_NAME*.json" where *ATTR_NAME* is the name of this attribute type.
- **Content**: A json dump of a dictionary keyed by tuple of node identifier, with json representations of value 
  objects. Tuples are represented as strings for json compliance.
 
**Node attributes:**
- **Nomenclature**: "nodeatt_*ATTR_NAME*.json" where *ATTR_NAME* is the name of this attribute type.
- **content**: A json dump of a dictionary keyed by node identifier, with json representations of value objects.

**Graph attributes:**
- **Nomenclature**: "graphatt_*ATTR_NAME*.json" where *ATTR_NAME* is the name of this attribute type.
- **content**: json serialized object. No key is necessary.

### Reserved Names
certain names have special meaning and cannot not be used.
- **isDirected:** The file "graphatt_isDirected.json" must be present in each graph directory. It stores a single boolean variable representing whether a graph shout be interpreted as directed or undirected. The `isDirected` keyword cannot be set as a graph attribute by the user.
- **weight:** The `weight` edge attribute is used to specify edge weights as they appear in the edgelist for weighted graphs. Any networkx object with a weight edge attribute set is interpreted as weighted. Note that an "edgeatt_weight.json" file is never produced.

### Multigraphs
This storage format naturally extends to multigraphs. There can simply be multiple graph folders, each with its own
edgelist and metadata. An ordering of the graphs is maintained via the graph ID numbers. 

### Packaging
packaged as a zip archive that expands to a directory containing each graph folder.
