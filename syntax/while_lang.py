from dataclasses import dataclass
from functools import lru_cache

from lark import Lark, Transformer, v_args
from importlib_resources import files

from syntax.utils import _install_str_hook


type Expr = Id | Int | BinOp

type Stmt = Skip | Assign | Seq | If | While


@dataclass(frozen=True, slots=True)
class Id:
    name: str


@dataclass(frozen=True, slots=True)
class Int:
    value: int


@dataclass(frozen=True, slots=True)
class BinOp:
    op: str
    lhs: Expr
    rhs: Expr


@dataclass(frozen=True, slots=True)
class Skip:
    pass


SKIP = Skip()


@dataclass(frozen=True, slots=True)
class Assign:
    var: Id
    expr: Expr


@dataclass(frozen=True, slots=True)
class Seq:
    first: Stmt
    second: Stmt


@dataclass(frozen=True, slots=True)
class If:
    cond: Expr
    then_branch: Stmt
    else_branch: Stmt


@dataclass(frozen=True, slots=True)
class While:
    cond: Expr
    body: Stmt


@v_args(inline=True)
class NodeFactory(Transformer):
    def skip(self) -> Skip:
        return SKIP

    def assign(self, name_tok, expr) -> Assign:
        return Assign(var=Id(name=str(name_tok)), expr=expr)

    def if_(self, cond, then_branch, else_branch) -> If:
        return If(cond=cond, then_branch=then_branch, else_branch=else_branch)

    def while_(self, cond, body) -> While:
        return While(cond=cond, body=body)

    def seq(self, first, second) -> Seq:
        return Seq(first=first, second=second)

    def addsub(self, lhs, op, rhs) -> BinOp:
        return BinOp(op=op.value, lhs=lhs, rhs=rhs)

    def muldiv(self, lhs, op, rhs) -> BinOp:
        return BinOp(op=op.value, lhs=lhs, rhs=rhs)

    def cmp(self, lhs, op, rhs):
        return BinOp(op=op.value, lhs=lhs, rhs=rhs)

    def var(self, name_tok):
        return Id(name=str(name_tok))

    def neg(self, inner):
        if isinstance(inner, Int):
            return Int(-inner.value)
        else:
            return BinOp(op="-", lhs=Int(0), rhs=inner)

    def num(self, value_tok):
        return Int(value=int(value_tok))

    def group_expr(self, inner):
        return inner

    def block(self, inner):
        return inner


@lru_cache(maxsize=1)
def read_grammar():
    """Reads the grammar from the file."""
    grammar = (files("syntax") / "while_lang.lark").read_text()
    return Lark(grammar, parser="lalr", transformer=NodeFactory())


def parse(program_text: str) -> Stmt:
    """Parses a While-language program into a structured AST."""
    parser = read_grammar()
    return parser.parse(program_text)


@_install_str_hook(Skip, Assign, Seq, If, While)
def pretty(stmt: Stmt, indent: int = 0) -> str:
    """Pretty-prints a statement."""
    INDENT = "  "

    def p(e: Expr) -> str:
        match e:
            case Id(name):
                return name
            case Int(n):
                return str(n)
            case BinOp(op, lhs, rhs):
                left = p(lhs)
                right = p(rhs)
                return f"({left} {op} {right})"
            case _:
                raise ValueError(f"Unknown expr: {e!r} of type {type(e)}")

    def s(s_: Stmt, lvl: int) -> str:
        pad = INDENT * lvl
        match s_:
            case Skip():
                return f"{pad}skip"
            case Assign(Id(name), expr):
                return f"{pad}{name} := {p(expr)}"
            case Seq(s1, s2):
                return f"{s(s1, lvl)};\n{s(s2, lvl)}"
            case If(cond, then_branch, else_branch):
                cond_str = p(cond)
                then_str = s(then_branch, lvl + 1)
                else_str = s(else_branch, lvl + 1)
                return f"{pad}if {cond_str} then\n{then_str}\n" f"{pad}else\n{else_str}"
            case While(cond, body):
                cond_str = p(cond)
                body_str = s(body, lvl + 1)
                return f"{pad}while {cond_str} do\n{body_str}"
            case _:
                raise ValueError(f"Unknown stmt: {s_!r} of type {type(s_)}")

    return s(stmt, indent)
