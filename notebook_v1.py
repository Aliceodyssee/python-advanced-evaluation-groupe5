#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
an object-oriented version of the notebook toolbox
"""
from notebook_v0 import *
class CodeCell:
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.
        execution_count (int): number of times the cell has been executed.

    Usage:

        >>> code_cell = CodeCell({
        ...     "cell_type": "code",
        ...     "execution_count": 1,
        ...     "id": "b777420a",
        ...     'source': ['print("Hello world!")']
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """

    def __init__(self, ipynb):
        self.cell_type = ipynb['cell_type']
        self.execution_count = ipynb['execution_count']
        self.id = ipynb['id']
        self.source = ipynb['source']


class MarkdownCell:
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell({
        ...    "cell_type": "markdown",
        ...    "id": "a9541506",
        ...    "source": [
        ...        "Hello world!\n",
        ...        "============\n",
        ...        "Print `Hello world!`:"
        ...    ]
        ... })
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!\n', '============\n', 'Print `Hello world!`:']
    """

    def __init__(self, ipynb):
        self.cell_type = ipynb['cell_type']
        self.id = ipynb['id']
        self.source = ipynb['source']

markdown_cell = MarkdownCell({"cell_type": "markdown",
                                    "id": "a9541506",
                                    "source": ["Hello world!\n",
                                                "============\n",
                                                "Print `Hello world!`:"]
                            })



class Notebook:
    r"""A Jupyter Notebook.

    Args:
        ipynb (dict): a dictionary representing a Jupyter Notebook.

    Attributes:
        version (str): the version of the notebook format.
        cells (list): a list of cells (either CodeCell or MarkdownCell).

    Usage:

        - checking the verion number:

            >>> ipynb = toolbox.load_ipynb("samples/minimal.ipynb")
            >>> nb = Notebook(ipynb)
            >>> nb.version
            '4.5'

        - checking the type of the notebook parts:

            >>> ipynb = toolbox.load_ipynb("samples/hello-world.ipynb")
            >>> nb = Notebook(ipynb)
            >>> isinstance(nb.cells, list)
            True
            >>> isinstance(nb.cells[0], Cell)
            True
    """

    def __init__(self, ipynb):
        self.version = get_format_version(ipynb)
        self.cells = []

        for i in get_cells(ipynb):
            if i['cell_type'] == 'code':
                self.cells.append(CodeCell(i))
            elif i['cell_type'] == 'markdown':
                self.cells.append(MarkdownCell(i))

    @staticmethod
    def from_file(filename):
        r"""Loads a notebook from an .ipynb file.

        Usage:

            >>> nb = Notebook.from_file("samples/minimal.ipynb")
            >>> nb.version
            '4.5'
        """
        return Notebook(load_ipynb(filename))
         


    def __iter__(self):
        r"""Iterate the cells of the notebook.

        Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
        """
        return iter(self.cells)

nb = Notebook.from_file("samples/minimal.ipynb")
nb.version

nb = Notebook.from_file("samples/hello-world.ipynb")
for cells in nb:
    print(cells.id)

class PyPercentSerializer:
    r"""Prints a given Notebook in py-percent format.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:
            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> ppp = PyPercentSerializer(nb)
            >>> print(ppp.to_py_percent()) # doctest: +NORMALIZE_WHITESPACE
            # %% [markdown]
            # Hello world!
            # ============
            # Print `Hello world!`:
            <BLANKLINE>
            # %%
            print("Hello world!")
            <BLANKLINE>
            # %% [markdown]
            # Goodbye! 👋
    """
    def __init__(self, notebook):
        self.notebook = notebook

    def to_py_percent(self):
        r"""Converts the notebook to a string in py-percent format.
        """
        #on reprend globalement le code to_percent en l'adaptant aux classes définies 
        res=""
        for cell in self.notebook:
            if cell.cell_type is MarkdownCell:
                res+="# %% [markdown] \n"
                for j in cell.source:
                    res+=f" {j} \n"
                res += "\n<BLANKLINE> \n"

            elif cell.cell_type is CodeCell:
                res+="# %% \n"
                for j in cell.source:
                    res+=f"# {j} \n"
                res += "\n<BLANKLINE> \n"

        return res[:-14] #il faut enlever le dernier <BLANKLINE>

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = PyPercentSerializer(nb)
                >>> s.to_file("samples/hello-world-serialized-py-percent.py")
        """
        file = open(filename, 'w+')
        file.write(str(self.to_py_percent()))
        file.close()


class Serializer:
    r"""Serializes a Jupyter Notebook to a file.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:

        >>> nb = Notebook.from_file("samples/hello-world.ipynb")
        >>> s = Serializer(nb)
        >>> pprint.pprint(s.serialize())  # doctest: +NORMALIZE_WHITESPACE
            {'cells': [{'cell_type': 'markdown',
                'id': 'a9541506',
                'medatada': {},
                'source': ['Hello world!\n',
                           '============\n',
                           'Print `Hello world!`:']},
               {'cell_type': 'code',
                'execution_count': 1,
                'id': 'b777420a',
                'medatada': {},
                'outputs': [],
                'source': ['print("Hello world!")']},
               {'cell_type': 'markdown',
                'id': 'a23ab5ac',
                'medatada': {},
                'source': ['Goodbye! 👋']}],
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5}
        >>> s.to_file("samples/hello-world-serialized.ipynb")
    """

    def __init__(self, notebook):
        self.notebook = notebook

    def serialize(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        dict = {}

        dict["cells"]=[]
        for cell in self.notebook:
            if isinstance(cell, MarkdownCell):
                dict["cells"].append({'cell_type': 'markdown' , 'id': cell.id, 'metadata': {}, 'source': cell.source})
            elif isinstance(cell, CodeCell):
                dict["cells"].append({'cell_type': 'code' , 'execution_count': cell.execution_count, 'id': cell.id, 'metadata': {}, 'source': cell.source})
        
        dict["metadata"] = {}

        dict["nbformat"] = str(self.notebook.version)[0]

        dict["nbformat_minor"] = str(self.notebook.version)[-1]

        return dict
        

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = Serializer(nb)
                >>> s.to_file("samples/hello-world-serialized.ipynb")
                >>> nb = Notebook.from_file("samples/hello-world-serialized.ipynb")
                >>> for cell in nb:
                ...     print(cell.id)
                a9541506
                b777420a
                a23ab5ac
        """
        file = open(filename, 'w+')
        file.write(str(self.serialise()))
        file.close()

class Outliner:
    r"""Quickly outlines the strucure of the notebook in a readable format.

    Args:
        notebook (Notebook): the notebook to outline.

    Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> o = Outliner(nb)
            >>> print(o.outline()) # doctest: +NORMALIZE_WHITESPACE
                Jupyter Notebook v4.5
                └─▶ Markdown cell #a9541506
                    ┌  Hello world!
                    │  ============
                    └  Print `Hello world!`:
                └─▶ Code cell #b777420a (1)
                    | print("Hello world!")
                └─▶ Markdown cell #a23ab5ac
                    | Goodbye! 👋
    """
    def __init__(self, notebook):
        self.notebook = notebook

    def outline(self):
        r"""Outlines the notebook in a readable format.

        Returns:
            str: a string representing the outline of the notebook.
        """
        nb = Serializer(self.notebook).serialize()
        res = f"Jupyter Notebook v {self.notebook.version} \n"
        for cell in nb['cells']:
            if cell['cell_type'] == 'markdown':
                res += f"└─▶ Markdown cell #  {cell['id']}   \n"
                if len(cell['source']) >= 2:
                    res += f"    ┌   {cell['source'][0]}" 
                    for line in cell['source'][1:-1]:
                        res += f"    │  {line}"
                    res += f"    └   {cell['source'][-1]}  \n"
                else:
                    res += f"    │    {cell['source'][0]}   \n"
            else:
                res += f"└─▶ Code cell #   {cell['id']}  ({cell['execution_count']}) \n"
                if len(cell['source']) >= 2:
                    res += f"    ┌     {cell['source'][0]} "
                    for line in cell['source'][1:-1]:
                        res += f"    │     {line}" 
                    res += f"    └    {cell['source'][-1]} \n"
                else:
                    res += f"    │    {cell['source'][0]} \n"
        return res

nb = Notebook.from_file("samples/hello-world.ipynb")
o = Outliner(nb)
print(o.outline())

