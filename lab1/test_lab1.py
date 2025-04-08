import pytest

from syntax.lambda_pure import parse

import solution


@pytest.mark.parametrize(
    "program, expected",
    [
        pytest.param(r"(\x. x) a", "a", id="identity"),
        pytest.param(r"(\x. \y. x) a b", "a", id="const_first"),
        pytest.param(r"(\x. \y. y) a b", "b", id="const_second"),
        pytest.param(r"(\x. x) (\y. y)", r"\y. y", id="nested_identity"),
        pytest.param(r"((\x. x) (\y. y)) z", "z", id="applied_identity"),
        pytest.param(r"(\x. a) ((\x. x x) (\x. x x))", "a", id="ignore_divergent_arg"),
        pytest.param(r"(\x. f x)", r"\x. (f x)", id="eta_form_preserved"),
        pytest.param(r"let x = a in x", "a", id="let_identity"),
        pytest.param(r"let x = a in (\y. x)", r"\y. a", id="let_in_lambda"),
        pytest.param(r"let x = (\z. z) in x", r"\z. z", id="let_identity_fun"),
        pytest.param(r"let x = (\z. z) in x a", "a", id="let_apply_identity_fun"),
        pytest.param(
            r"let x = (\x. x x) (\x. x x) in a", "a", id="let_divergent_binding_unused"
        ),
        pytest.param(r"(\x. \y. \z. x) a b c", "a", id="redundant_lambdas"),
        pytest.param(r"(\x. (\x. x)) a", r"\x. x", id="shadowing"),
        pytest.param(r"(\x. x x) (\x. a)", "a", id="self_application_terminating"),
    ],
)
def test_normal_form(program: str, expected: str) -> None:
    expr = parse(program)
    assert expr is not None, f"Failed to parse: {program}"
    assert solution.interpret(expr) == parse(expected)
