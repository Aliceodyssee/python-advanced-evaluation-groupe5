#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
starter code for your evaluation assignment
"""

# Python Standard Library
import base64
import io
import json
from os import read
import pprint
from matplotlib import pyplot as plt

# Third-Party Libraries
import numpy as np
import PIL.Image  # pillow


def load_ipynb(filename):
    r"""
    Load a jupyter notebook .ipynb file (JSON) as a Python dict.

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> ipynb
        {'cells': [], 'metadata': {}, 'nbformat': 4, 'nbformat_minor': 5}

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> pprint.pprint(ipynb)
        {'cells': [{'cell_type': 'markdown',
                    'id': 'a9541506',
                    'metadata': {},
                    'source': ['Hello world!\n',
                               '============\n',
                               'Print `Hello world!`:']},
                   {'cell_type': 'code',
                    'execution_count': 1,
                    'id': 'b777420a',
                    'metadata': {},
                    'outputs': [{'name': 'stdout',
                                 'output_type': 'stream',
                                 'text': ['Hello world!\n']}],
                    'source': ['print("Hello world!")']},
                   {'cell_type': 'markdown',
                    'id': 'a23ab5ac',
                    'metadata': {},
                    'source': ['Goodbye! 👋']}],
         'metadata': {},
         'nbformat': 4,
         'nbformat_minor': 5}
    """
    file=open(filename)
    file_read=file.read()
    dict=json.loads(file_read)
    file.close()
    return dict

print(load_ipynb("samples/minimal.ipynb"))
print(type(load_ipynb("samples/minimal.ipynb")))

print(load_ipynb("samples/hello-world.ipynb"))


def save_ipynb(ipynb, filename):
    r"""
    Save a jupyter notebook (Python dict) as a .ipynb file (JSON)

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> ipynb
        {'cells': [], 'metadata': {}, 'nbformat': 4, 'nbformat_minor': 5}
        >>> ipynb["metadata"]["clone"] = True
        >>> save_ipynb(ipynb, "samples/minimal-save-load.ipynb")
        >>> load_ipynb("samples/minimal-save-load.ipynb")
        {'cells': [], 'metadata': {'clone': True}, 'nbformat': 4, 'nbformat_minor': 5}

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> save_ipynb(ipynb, "samples/hello-world-save-load.ipynb")
        >>> ipynb == load_ipynb("samples/hello-world-save-load.ipynb")
        True

    """
    file=open(filename,"w")
    file.write(json.dumps(ipynb))
    file.close()

ipynb=load_ipynb("samples/minimal.ipynb")
print(save_ipynb(ipynb, "samples/minimal.ipynb"))


def get_format_version(ipynb):
    r"""
    Return the format version (str) of a jupyter notebook (dict).

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> get_format_version(ipynb)
        '4.5'

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> get_format_version(ipynb)
        '4.5'
    """
    print(f"{ipynb['nbformat']}.{ipynb['nbformat_minor']}")

ipynb = load_ipynb("samples/minimal.ipynb")
get_format_version(ipynb)


def get_metadata(ipynb):
    r"""
    Return the global metadata of a notebook.

    Usage:

        >>> ipynb = load_ipynb("samples/metadata.ipynb")
        >>> metadata = get_metadata(ipynb)
        >>> pprint.pprint(metadata)
        {'celltoolbar': 'Edit Metadata',
         'kernelspec': {'display_name': 'Python 3 (ipykernel)',
                        'language': 'python',
                        'name': 'python3'},
         'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3},
                           'file_extension': '.py',
                           'mimetype': 'text/x-python',
                           'name': 'python',
                           'nbconvert_exporter': 'python',
                           'pygments_lexer': 'ipython3',
                           'version': '3.9.7'}}
    """
    return ipynb['metadata']

ipynb = load_ipynb("samples/metadata.ipynb")
metadata = get_metadata(ipynb)
pprint.pprint(metadata)

def get_cells(ipynb):
    r"""
    Return the notebook cells.

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> cells = get_cells(ipynb)
        >>> cells
        []

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> cells = get_cells(ipynb)
        >>> pprint.pprint(cells)
        [{'cell_type': 'markdown',
          'id': 'a9541506',
          'metadata': {},
          'source': ['Hello world!\n', '============\n', 'Print `Hello world!`:']},
         {'cell_type': 'code',
          'execution_count': 1,
          'id': 'b777420a',
          'metadata': {},
          'outputs': [{'name': 'stdout',
                       'output_type': 'stream',
                       'text': ['Hello world!\n']}],
          'source': ['print("Hello world!")']},
         {'cell_type': 'markdown',
          'id': 'a23ab5ac',
          'metadata': {},
          'source': ['Goodbye! 👋']}]
    """
    return ipynb['cells']

ipynb = load_ipynb("samples/hello-world.ipynb")
cells = get_cells(ipynb)
pprint.pprint(cells)


def to_percent(ipynb):
    r"""
    Convert a ipynb notebook (dict) to a Python code in the percent format (str).

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> print(to_percent(ipynb)) # doctest: +NORMALIZE_WHITESPACE
        # %% [markdown]
        # Hello world!
        # ============
        # Print `Hello world!`:
        # %%
        print("Hello world!")
        # %% [markdown]
        # Goodbye! 👋

        >>> notebook_files = Path(".").glob("samples/*.ipynb")
        >>> for notebook_file in notebook_files:
        ...     ipynb = load_ipynb(notebook_file)
        ...     percent_code = to_percent(ipynb)
        ...     with open(notebook_file.with_suffix(".py"), "w", encoding="utf-8") as output:
        ...         print(percent_code, file=output)
    """
    res=""
    for i in ipynb["cells"]:
        
        if i["cell_type"]=="markdown":
            res+="# %% [markdown] \n"
            for j in i["source"]:
                res+=f"# {j} \n"

        elif i["cell_type"]=="code":
            res+="# %% \n"
            for j in i["source"]:
                res+=f"# {j} \n"

    return res


ipynb = load_ipynb("samples/hello-world.ipynb")
print(to_percent(ipynb)) # doctest: +NORMALIZE_WHITESPACE


def starboard_html(code):
    return f"""
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Starboard Notebook</title>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <link rel="icon" href="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/favicon.ico">
        <link href="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/starboard-notebook.css" rel="stylesheet">
    </head>
    <body>
        <script>
            window.initialNotebookContent = {code!r}
            window.starboardArtifactsUrl = `https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/`;
        </script>
        <script src="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/starboard-notebook.js"></script>
    </body>
</html>
"""


def to_starboard(ipynb, html=False):
    r"""
    Convert a ipynb notebook (dict) to a Starboard notebook (str)
    or to a Starboard HTML document (str) if html is True.

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> print(to_starboard(ipynb))
        # %% [markdown]
        Hello world!
        ============
        Print `Hello world!`:
        # %% [python]
        print("Hello world!")
        # %% [markdown]
        Goodbye! 👋

        >>> html = to_starboard(ipynb, html=True)
        >>> print(html) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        <!doctype html>
        <html>
        ...
        </html>

        >>> notebook_files = Path(".").glob("samples/*.ipynb")
        >>> for notebook_file in notebook_files:
        ...     ipynb = load_ipynb(notebook_file)
        ...     starboard_html = to_starboard(ipynb, html=True)
        ...     with open(notebook_file.with_suffix(".html"), "w", encoding="utf-8") as output:
        ...         print(starboard_html, file=output)
    """
    if html:
        code=""
        for i in ipynb["cells"]:
        
            if i["cell_type"]=="markdown":
                code+="# %% [markdown] \\n"
                for j in i["source"]:
                    code+=f"{j} \\n"

            elif i["cell_type"]=="code":
                code+="# %% [python] \\n"
                for j in i["source"]:
                    code+=f"{j} \\n" 
        return starboard_html(code)
    else:
        res=""
        for i in ipynb["cells"]:
        
            if i["cell_type"]=="markdown":
                res+="# %% [markdown] \n"
                for j in i["source"]:
                    res+=f"{j} \n"

            elif i["cell_type"]=="code":
                res+="# %% [python] \n"
                for j in i["source"]:
                    res+=f"{j} \n"

        return res


ipynb = load_ipynb("samples/hello-world.ipynb")
print(to_starboard(ipynb))

# Outputs
# ------------------------------------------------------------------------------
def clear_outputs(ipynb):
    r"""
    Remove the notebook cell outputs and resets the cells execution counts.

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> pprint.pprint(ipynb)
        {'cells': [{'cell_type': 'markdown',
                    'id': 'a9541506',
                    'metadata': {},
                    'source': ['Hello world!\n',
                               '============\n',
                               'Print `Hello world!`:']},
                   {'cell_type': 'code',
                    'execution_count': 1,
                    'id': 'b777420a',
                    'metadata': {},
                    'outputs': [{'name': 'stdout',
                                 'output_type': 'stream',
                                 'text': ['Hello world!\n']}],
                    'source': ['print("Hello world!")']},
                   {'cell_type': 'markdown',
                    'id': 'a23ab5ac',
                    'metadata': {},
                    'source': ['Goodbye! 👋']}],
         'metadata': {},
         'nbformat': 4,
         'nbformat_minor': 5}
        >>> clear_outputs(ipynb)
        >>> pprint.pprint(ipynb)
        {'cells': [{'cell_type': 'markdown',
                    'id': 'a9541506',
                    'metadata': {},
                    'source': ['Hello world!\n',
                               '============\n',
                               'Print `Hello world!`:']},
                   {'cell_type': 'code',
                    'execution_count': None,
                    'id': 'b777420a',
                    'metadata': {},
                    'outputs': [],
                    'source': ['print("Hello world!")']},
                   {'cell_type': 'markdown',
                    'id': 'a23ab5ac',
                    'metadata': {},
                    'source': ['Goodbye! 👋']}],
         'metadata': {},
         'nbformat': 4,
         'nbformat_minor': 5}
    """
    ipynb["cells"]["execution count"]=None
    ipynb["cells"]["outputs"]=[]




def get_stream(ipynb, stdout=True, stderr=False):
    r"""
    Return the text written to the standard output and/or error stream.

    Usage:

        >>> ipynb = load_ipynb("samples/streams.ipynb")
        >>> print(get_stream(ipynb)) # doctest: +NORMALIZE_WHITESPACE
        👋 Hello world! 🌍
        >>> print(get_stream(ipynb, stdout=False, stderr=True)) # doctest: +NORMALIZE_WHITESPACE
        🔥 This is fine. 🔥 (https://gunshowcomic.com/648)
        >>> print(get_stream(ipynb, stdout=True, stderr=True)) # doctest: +NORMALIZE_WHITESPACE
        👋 Hello world! 🌍
        🔥 This is fine. 🔥 (https://gunshowcomic.com/648)
    """


    res=''
    if stdout:
        
        for i in ipynb["cells"]:
            if i["outputs"]["name"]=='stdout':
                res+=i["outputs"]["text"][0]

    elif stderr:
        
        for i in ipynb["cells"]:
            if i["outputs"]["name"]=='stderr':
                res+=i["outputs"]["text"][0]
    return res

# ipynb = load_ipynb("samples/streams.ipynb")
# print(get_stream(ipynb))


def get_exceptions(ipynb):
    r"""
    Return all exceptions raised during cell executions.

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> get_exceptions(ipynb)
        []

        >>> ipynb = load_ipynb("samples/errors.ipynb")
        >>> errors = get_exceptions(ipynb)
        >>> all(isinstance(error, Exception) for error in errors)
        True
        >>> for error in errors:
        ...     print(repr(error))
        TypeError("unsupported operand type(s) for +: 'int' and 'str'")
        Warning('🌧️  light rain')
    """
    res=""
    for i in ipynb["cells"]:
        if i["outputs"]["output_type"]=='error':
            res+= f"{i['outputs']['ename']}({i['outputs']['evalue']}) \n"
    return res



def get_images(ipynb):
    r"""
    Return the PNG images contained in a notebook cells outputs
    (as a list of NumPy arrays).

    Usage:

        >>> ipynb = load_ipynb("samples/images.ipynb")
        >>> images = get_images(ipynb)
        >>> images # doctest: +ELLIPSIS
        [array([[[ ...]]], dtype=uint8)]
        >>> grace_hopper_image = images[0]
        >>> np.shape(grace_hopper_image)
        (600, 512, 3)
        >>> grace_hopper_image # doctest: +ELLIPSIS
        array([[[ 21,  24,  77],
                [ 27,  30,  85],
                [ 33,  35,  92],
                ...,
                [ 14,  13,  19]]], dtype=uint8)
    """
    res=[]
    for i in get_cells(ipynb):
        if i['outputs']!=[] and isinstance(i['outputs'][0]['data'],dict):
            for key, item in i['outputs'][0]['data'].items():
                if 'image' in key:
                    decode=base64.b64decode(item)
                    img=PIL.Image.open(io.BytesIO(decode))
    res.append(np.asarray(img))
    return res[0]

ipynb = load_ipynb("samples/images.ipynb")
print(get_images(ipynb)) 
plt.imshow(get_images(ipynb))
plt.show()

