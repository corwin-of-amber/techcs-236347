import typing
import operator

import z3

import syntax.while_lang as lang


type Formula = z3.Ast | bool
type PVar = str
type Env = dict[PVar, Formula]
type Invariant = typing.Callable[[Env], Formula]


OP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    "<=": operator.le,
    ">=": operator.ge,
    "=": operator.eq,
}


def mk_env(pvars: set[PVar]) -> Env:
    return {v: z3.Int(v) for v in pvars}


def upd(d: Env, k: PVar, v: Formula) -> Env:
    d = d.copy()
    d[k] = v
    return d


def verify(
    P: Invariant, ast: lang.Stmt, Q: Invariant, linv: Invariant = lambda _: True
) -> bool:
    """Verify a Hoare triple {P} c {Q}
    Where P, Q are assertions (see below for examples)
    and ast is the AST of the command c.
    Returns `True` iff the triple is valid.
    Also prints the counterexample (model) returned from Z3 in case
    it is not.
    """
    raise NotImplementedError


def main():
    # example program
    pvars = ["a", "b", "i", "n"]
    program = "a := b ; while i < n do ( a := a + 1 ; b := b + 1 )"
    P = lambda _: True
    Q = lambda d: d["a"] == d["b"]
    linv = lambda d: d["a"] == d["b"]

    ast = lang.parse(program)
    # Your task is to implement "verify"
    verify(P, ast, Q, linv=linv)


if __name__ == "__main__":
    main()
