import typing
from functools import reduce

from syntax.tree import Tree
from syntax.parsing.earley.earley import Grammar, Parser, ParseTrees
from syntax.parsing.silly import SillyLexer


__all__ = ["parse", "pretty"]


class LambdaParser:
    TOKENS = (
        r"(let|in)(?![\w\d_])   (?P<id>[^\W\d]\w*)   (?P<num>\d+)   [\\.()=]".split()
    )
    GRAMMAR = r"""
    E    ->  \. | let_    |   E1  |  E1'
    E1   ->  @            |   E0
    E1'  ->  @'           |   E0
    E0   ->  id | num     |  ( E )
    \.   ->  \ L . E 
    @    ->  E1 E0
    @'   ->  E1 \.
    L    ->  id L |
    let_ ->  let id = E in E
    """

    def __init__(self) -> None:
        self.tokenizer = SillyLexer(self.TOKENS)
        self.grammar = Grammar.from_string(self.GRAMMAR)

    def __call__(self, program_text: str) -> typing.Optional[Tree]:
        tokens = list(self.tokenizer(program_text))

        earley = Parser(grammar=self.grammar, sentence=tokens, debug=False)
        earley.parse()

        if earley.is_valid_sentence():
            trees = ParseTrees(earley)
            assert len(trees) == 1
            return self.postprocess(trees.nodes[0])
        else:
            return None

    def postprocess(self, t: Tree) -> Tree:
        if t.root in ["γ", "E", "E0", "E1", "E1'"] and len(t.subtrees) == 1:
            return self.postprocess(t.subtrees[0])
        elif t.root == "E0" and t.subtrees[0].root == "(":
            return self.postprocess(t.subtrees[1])
        elif t.root == r"\.":
            args = t.subtrees[1].split()
            t = reduce(lambda t, a: Tree("\\", [a, t]), reversed(args), t.subtrees[3])
        elif t.root == "@'":
            t = Tree("@", t.subtrees)
        elif t.root == "L":
            t = Tree(".", t.split())

        return Tree(t.root, [self.postprocess(s) for s in t.subtrees])


def parse(program_text: str) -> typing.Optional[Tree]:
    parser = LambdaParser()
    return parser(program_text)


def pretty(expr: Tree) -> str:
    """Formats an expression for pretty printing."""

    def pretty(expr: Tree, parent: tuple[str, int] = (".", 0), follow: str = "") -> str:
        if expr.root in ["id", "num"]:
            return expr.subtrees[0].root
        if expr.root == "\\":
            tmpl = r"\%s. %s"
            if parent == ("@", 0) or parent[0] == follow == "@":
                tmpl = "(%s)" % tmpl
        elif expr.root == "@":
            tmpl = "%s %s"
            if parent == ("@", 1):
                tmpl = "(%s)" % tmpl
        else:
            return str(expr)

        n = len(expr.subtrees)
        return tmpl % tuple(
            pretty(s, (expr.root, i), expr.root if i < n - 1 else follow)
            for i, s in enumerate(expr.subtrees)
        )

    return pretty(expr)
