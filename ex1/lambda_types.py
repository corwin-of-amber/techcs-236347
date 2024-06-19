"""
Homework 1

Your task:
Implement type checking and type inference for simply-typed lambda calculus.
"""

from syntax.tree import Tree
from syntax.lambda_typed import parse, parse_type, pretty


class TypeMismatchError(TypeError):
    pass


class InsufficientAnnotationsError(TypeError):
    pass


def type_inference(expr: Tree) -> Tree:
    """
    Input: an expression.
    Output:
     * A tree representing the type of the whole expression (type Tree).
     * If encountered a unification error, raise TypeMismatchError
     * If some types cannot be inferred, raise InsufficientAnnotationsError
    """
    return None


def main():
    expr = parse(
        r"""
    let add2 = \x. plus x 2 in
    \f. succ (f True add2)
    """
    )

    if expr:
        print(">> Valid expression.")
        print(pretty(expr))
        print(type_inference(expr))
    else:
        print(">> Invalid expression.")


if __name__ == "__main__":
    main()
