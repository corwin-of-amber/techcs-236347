from os import linesep
from tempfile import NamedTemporaryFile

from syntax.tree import Tree


def dot_print(expr: Tree) -> None:
    from graphviz import Source

    temp = """digraph G{
edge [dir=forward]

"""
    nodes = {id(n): (i, n) for (i, n) in enumerate(expr.nodes)}
    edges = {(nodes[id(n)][0], nodes[id(s)][0]) for n in expr.nodes for s in n.subtrees}

    def translate_backslash(x):
        return str(x).replace("\\", "\\\\")

    nodes_string = linesep.join(
        [f'{i[0]} [label="{translate_backslash(i[1].root)}"]' for n, i in nodes.items()]
    )
    edges_string = linesep.join([f"{n} -> {s}" for (n, s) in edges])
    tmp_file = NamedTemporaryFile(delete=False)
    # s = Source(temp + nodes_string + linesep + edges_string + linesep + "}", filename=tmp_file.name)
    # s.view(filename=tmp_file.name)
