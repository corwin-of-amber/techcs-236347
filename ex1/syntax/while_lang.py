import typing

from syntax.tree import Tree
from syntax.parsing.earley.earley import Grammar, Parser, ParseTrees
from syntax.parsing.silly import SillyLexer

__all__ = ["parse"]


class WhileParser:

    TOKENS = (
        r"(if|then|else|while|do|skip)(?![\w\d_]) "
        r"(?P<id>[^\W\d]\w*) "
        r"(?P<num>[+\-]?\d+) "
        r"(?P<op>[!<>]=|([+\-*/<>=])) "
        r"[();]  :=".split()
    )
    GRAMMAR = r"""
    S   ->   S1     |   S1 ; S
    S1  ->   skip   |   id := E   |   if E then S else S1   |   while E do S1
    S1  ->   ( S )
    E   ->   E0   |   E0 op E0
    E0  ->   id   |   num
    E0  ->   ( E )
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
        if t.root in ["γ", "S", "S1", "E", "E0"] and len(t.subtrees) == 1:
            return self.postprocess(t.subtrees[0])
        elif (
            t.root in ["S", "S1", "E"]
            and len(t.subtrees) == 3
            and t.subtrees[1].root in [":=", ";", "op"]
        ):
            return Tree(
                t.subtrees[1].subtrees[0].root,
                [self.postprocess(s) for s in [t.subtrees[0], t.subtrees[2]]],
            )
        elif len(t.subtrees) == 3 and t.subtrees[0].root == "(":
            return self.postprocess(t.subtrees[1])
        elif t.root == "S1" and t.subtrees[0].root in ["if", "while"]:
            return self.postprocess(Tree(t.subtrees[0].root, t.subtrees[1::2]))
        elif t.root == "num":
            return Tree(t.root, [Tree(int(t.subtrees[0].root))])  # parse ints

        return Tree(t.root, [self.postprocess(s) for s in t.subtrees])


def parse(program_text: str) -> typing.Optional[Tree]:
    return WhileParser()(program_text)
