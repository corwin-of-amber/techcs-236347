import pytest

from syntax.lambda_typed import parse, parse_type
from syntax.tree import Tree

from lambda_types import type_inference, InsufficientAnnotationsError, TypeMismatchError


def check_legal(expr: str, expected: Tree) -> None:
    type_expr = type_inference(parse(expr))
    assert isinstance(type_expr, Tree)
    assert type_expr == expected


def test_gift_0():
    check_legal(
        r"1",
        parse_type(r"nat"),
    )


def test_gift_1():
    check_legal(
        r"\x: nat . x",
        parse_type(r"nat -> nat"),
    )


def test_gift_2():
    check_legal(
        r"""\plus (lt : nat -> nat -> bool). lt ((\x. plus x x) 3) ((\x. plus 5 x) 9)""",
        parse_type(r"""(nat -> nat -> nat) -> (nat -> nat -> bool) -> bool"""),
    )


def test_gift_3():
    check_legal(
        r"""\f g (a : real) (z : unreal). f (g a z) (f 5 a)""",
        parse_type(
            r"""(nat -> real -> real) -> (real -> unreal -> nat) -> real -> unreal -> real"""
        ),
    )


def test_insufficient_0():
    expr = parse(r"x")
    with pytest.raises(InsufficientAnnotationsError):
        type_inference(expr)


def test_type_mismatch_0():
    expr = parse(r"let x: int = \y: bool. y in x")
    with pytest.raises(TypeMismatchError):
        type_inference(expr)
