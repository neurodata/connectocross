## GRAPH and METADATA FILE SPECIFICATION
author: Spencer Loggia

This document outlines the graph storage protocol used by the metagraph class.

A single graph is stored as a directory with name "graph_*UID*" where *UID* is an identifying number. 

### Edgelist
Inside a graph directory there must be a file called "edgelist.csv", which contains a index column, a source node column,
and a target node column. Node identifiers must be strings or integers.

### Metadata
Each graph's attributes are stored as json files within a graph's directory. They are named and stored as follows:

**Edge attributes:** 

- **Nomenclature**: "edgeatt_*ATTR_NAME*.json" where *ATTR_NAME* is the name of this attribute type.
- **Content**: A json dump of a dictionary keyed by tuple of node identifier, with json representations of value 
  objects. Tuples are represented as strings for json compliance.
 
**Node attributes:**
- **Nomenclature**: "nodeatt_*ATTR_NAME*.json" where *ATTR_NAME* is the name of this attribute type.
- **content**: A json dump of a dictionary keyed node identifier, with json representations of value objects.

### Multigraphs
This storage format naturally extends to multigraphs. There can simply be multiple graph folders, each with its own
edgelist and metadata. An ordering of the graphs is maintained via the graph UID numbers. 

### Packaging
packaged as a zip archive that expands to a directory containing each graph folder.
