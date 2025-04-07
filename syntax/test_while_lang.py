import pytest
from syntax.while_lang import (
    parse,
    pretty,
    Id,
    Int,
    BinOp,
    SKIP,
    Assign,
    Seq,
    If,
    While,
    Expr,
    Stmt,
    Skip,
)
from syntax.utils import make_node


def id(name: str) -> Id:
    return make_node(Id, name)


def num(n: int) -> Int:
    return make_node(Int, n)


def binop(op: str, lhs: Expr, rhs: Expr) -> BinOp:
    return make_node(BinOp, op, lhs, rhs)


def assign(var: Id, expr: Expr) -> Assign:
    return make_node(Assign, var, expr)


def seq(s1: Stmt, s2: Stmt) -> Seq:
    return make_node(Seq, s1, s2)


def iff(cond: Expr, then: Stmt, els: Stmt) -> If:
    return make_node(If, cond, then, els)


def whil(cond: Expr, body: Stmt) -> While:
    return make_node(While, cond, body)


def skip() -> Skip:
    return SKIP


@pytest.mark.parametrize(
    "program, expected",
    [
        # Basic statements
        ("skip", skip()),
        ("x := 1", assign(id("x"), num(1))),
        ("x := y", assign(id("x"), id("y"))),
        ("x := x + 1", assign(id("x"), binop("+", id("x"), num(1)))),
        ("x := (x + 1)", assign(id("x"), binop("+", id("x"), num(1)))),
        # Multiplication binds tighter than addition
        (
            "x := 1 + 2 * 3",
            assign(id("x"), binop("+", num(1), binop("*", num(2), num(3)))),
        ),
        # Addition is left-associative
        (
            "x := 1 + 2 + 3",
            assign(id("x"), binop("+", binop("+", num(1), num(2)), num(3))),
        ),
        # Multiplication is left-associative
        (
            "x := 2 * 3 * 4",
            assign(id("x"), binop("*", binop("*", num(2), num(3)), num(4))),
        ),
        # Comparison after arithmetic
        (
            "x := 1 + 2 < 4",
            assign(id("x"), binop("<", binop("+", num(1), num(2)), num(4))),
        ),
        # Sequences
        ("x := 1; skip", seq(assign(id("x"), num(1)), skip())),
        ("skip; skip", seq(skip(), skip())),
        (
            "x := 1; y := 2; skip",
            seq(assign(id("x"), num(1)), seq(assign(id("y"), num(2)), skip())),
        ),
        # If-else
        # if binds tighter than ;
        (
            "if x < 0 then skip else skip; skip",
            seq(iff(binop("<", id("x"), num(0)), skip(), skip()), skip()),
        ),
        # Sequence in else branch (should NOT happen implicitly)
        (
            "if x < 0 then skip else skip; x := 1",
            seq(
                iff(
                    binop("<", id("x"), num(0)), skip(), skip()
                ),  # NOT: else (skip; x := 1)
                assign(id("x"), num(1)),
            ),
        ),
        # Force sequence inside else using parens
        (
            "if x < 0 then skip else (skip; x := 1)",
            iff(
                binop("<", id("x"), num(0)),
                skip(),
                seq(skip(), assign(id("x"), num(1))),
            ),
        ),
        (
            "if x = 2 then skip else skip",
            iff(binop("=", id("x"), num(2)), skip(), skip()),
        ),
        (
            "if x < 2 then skip else x := 3",
            iff(binop("<", id("x"), num(2)), skip(), assign(id("x"), num(3))),
        ),
        # While
        (
            "while x > 0 do x := x - 1",
            whil(
                binop(">", id("x"), num(0)),
                assign(id("x"), binop("-", id("x"), num(1))),
            ),
        ),
        # Nested control flow
        (
            "if x < 1 then while y > 0 do y := y - 1 else skip",
            iff(
                binop("<", id("x"), num(1)),
                whil(
                    binop(">", id("y"), num(0)),
                    assign(id("y"), binop("-", id("y"), num(1))),
                ),
                skip(),
            ),
        ),
        # 8. while binds tighter than ;
        (
            "while x < 5 do skip; x := x + 1",
            seq(
                whil(binop("<", id("x"), num(5)), skip()),
                assign(id("x"), binop("+", id("x"), num(1))),
            ),
        ),
        # 9. Grouping multiple statements under while
        (
            "while x < 5 do (x := x + 1; skip)",
            whil(
                binop("<", id("x"), num(5)),
                seq(assign(id("x"), binop("+", id("x"), num(1))), skip()),
            ),
        ),
        # Precedence and associativity
        (
            "x := 1 + 2 * 3",
            assign(id("x"), binop("+", num(1), binop("*", num(2), num(3)))),
        ),
        (
            "x := (1 + 2) * 3",
            assign(id("x"), binop("*", binop("+", num(1), num(2)), num(3))),
        ),
    ],
)
def test_parse_valid(program, expected):
    parsed = parse(program)
    assert parsed == expected
