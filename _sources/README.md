# Using the jupyter-book documentation
- Notebooks you want to add need to be already run (at the moment)
- Notebooks should just be dropped in the `docs` folder 
- Notebooks need to be added to `_toc.yml` in order for them to be rendered. See that
file for an example of how to create a "part" (section) with notebooks in it. 
- Your jupyter notebook MUST have a title as the first cell. This means you need to make
a markdown cell at the top of the notebook, and add a title (use # in markdown cell, 
whatever you write after that is the title).
- You can use markdown directives in the jupyter notebook to create sub headings for 
sections in the jupyter notebook, just like the above for the title. A sub heading is 
prefaced by ##, a sub-subheading by ###, etc.
- Don't touch anything in the `_config.yml` file without consulting @bdpedigo.
- You can build the docs locally from the root directory of the project by installing 
jupyter book and running `jupyter-book build docs` which will create the html and put it
in `_build` by default.
- If you have any questions, please consult 
[the jupyter books documentation](https://jupyterbook.org/intro.html) as it is heavily
documented and your questions will likely be answered there!