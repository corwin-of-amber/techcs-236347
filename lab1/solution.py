from syntax.lambda_pure import LambdaExpr, App, Lambda, Let, Id


def normal_form(expr: LambdaExpr, max_steps: int = 100_000):
    """
    Keep performing normal-order reduction step until you reach normal form, detect divergence or run out of fuel.
    """
    raise NotImplementedError
