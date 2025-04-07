import pytest

from syntax.lambda_typed import parse, parse_type, TypedExpr

from solution import infer_types, InsufficientAnnotationsError, TypeMismatchError


def check_legal(expr: str, expected: TypedExpr) -> None:
    type_expr = infer_types(parse(expr))
    assert isinstance(type_expr, TypedExpr)
    assert type_expr == expected


def test_gift_0():
    check_legal(
        r"1",
        parse_type(r"int"),
    )


def test_gift_1():
    check_legal(
        r"\x: int . x",
        parse_type(r"int -> int"),
    )


def test_gift_2():
    check_legal(
        r"""\plus (lt : int -> int -> bool). lt ((\x. plus x x) 3) ((\x. plus 5 x) 9)""",
        parse_type(r"""(int -> int -> int) -> (int -> int -> bool) -> bool"""),
    )


def test_gift_3():
    check_legal(
        r"""\f g (a : real) (z : unreal). f (g a z) (f 5 a)""",
        parse_type(
            r"""(int -> real -> real) -> (real -> unreal -> int) -> real -> unreal -> real"""
        ),
    )


def test_insufficient_0():
    expr = parse(r"x")
    with pytest.raises(InsufficientAnnotationsError):
        infer_types(expr)


def test_type_mismatch_0():
    expr = parse(r"let x: bool = 1 in x")
    with pytest.raises(TypeMismatchError):
        infer_types(expr)
