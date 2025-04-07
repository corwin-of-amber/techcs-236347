from z3 import And

from syntax.while_lang import parse

from solution import verify, Env, Formula


def test_0() -> None:
    ast = parse(
        """
        a := b;
        while i < n do (
            a := a + 1;
            b := b + 1
        )
    """
    )
    assert ast is not None

    def linv(env: Env) -> Formula:
        return env["a"] == env["b"]

    def P(env: Env) -> Formula:
        return True

    def Q(env: Env) -> Formula:
        return And(env["a"] == env["b"], env["i"] >= env["n"])

    assert verify(P, ast, Q, linv)


def test_1() -> None:
    ast = parse(
        """
        y := 0 ;
        while y < i do (
            x := x + y;
            if (x * y) < 10
                then y := y + 1 
                else skip
        )
    """
    )
    assert ast is not None

    def linv(env: Env) -> Formula:
        return And(env["y"] >= 0, env["x"] > 0)

    def P(env: Env) -> Formula:
        return env["x"] > 0

    def Q(env: Env) -> Formula:
        return env["x"] > 0

    assert verify(P, ast, Q, linv)


def test_2() -> None:
    ast = parse(
        """
        while a != b do
            if a > b
                then a := a - b
                else b := b - a
    """
    )
    assert ast is not None

    def linv(env: Env) -> Formula:
        return env["a"] > 0

    def P(env: Env) -> Formula:
        return And(env["a"] > 0, env["b"] > 0)

    def Q(env: Env) -> Formula:
        return And(env["a"] > 0, env["a"] == env["b"])

    assert verify(P, ast, Q, linv)
