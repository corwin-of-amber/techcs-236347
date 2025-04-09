import pytest
from syntax.lambda_pure import parse, Id, Int, App, Lambda, Let, LambdaExpr
from syntax.utils import make_node
import syntax
print(syntax.utils.__file__)

def id(name: str) -> Id:
    return make_node(Id, name)


def num(n: int) -> Int:
    return make_node(Int, n)


def lam(var: str, body: LambdaExpr) -> Lambda:
    return make_node(Lambda, id(var), body)


def app(f: LambdaExpr, x: LambdaExpr) -> App:
    return make_node(App, f, x)


def let(v: str, defn: LambdaExpr, body: LambdaExpr) -> Let:
    return make_node(Let, id(v), defn, body)


@pytest.mark.parametrize(
    "program, expected",
    [
        # Identifiers
        ("x", id("x")),
        ("foo", id("foo")),
        # Numbers
        ("0", num(0)),
        ("42", num(42)),
        # Lambdas
        (r"\x. x", lam("x", id("x"))),
        (r"\x. 5", lam("x", num(5))),
        (r"\x. \y. x", lam("x", lam("y", id("x")))),
        # Application
        ("x y", app(id("x"), id("y"))),
        ("(x y) z", app(app(id("x"), id("y")), id("z"))),
        ("x (y z)", app(id("x"), app(id("y"), id("z")))),
        (r"(\y. y) 5", app(lam("y", id("y")), num(5))),
        (r"(\x. \y. x) 5", app(lam("x", lam("y", id("x"))), num(5))),
        (r"(\x. \y. x) a b", app(app(lam("x", lam("y", id("x"))), id("a")), id("b"))),
        # Let bindings
        ("let x = y in z", let("x", id("y"), id("z"))),
        ("let x = 5 in x", let("x", num(5), id("x"))),
        ("let x = \\y. y in x", let("x", lam("y", id("y")), id("x"))),
        ("let x = y in let y = z in x", let("x", id("y"), let("y", id("z"), id("x")))),
        # Combinations
        ("(\\x. x) 5", app(lam("x", id("x")), num(5))),
        (
            "let id = \\x. x in id 3",
            let("id", lam("x", id("x")), app(id("id"), num(3))),
        ),
        ("\\f. \\x. f x", lam("f", lam("x", app(id("f"), id("x"))))),
    ],
)
def test_parse_valid(program, expected):
    assert parse(program) == expected
