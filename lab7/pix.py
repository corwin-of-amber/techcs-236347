from z3 import Int, Xor, BoolVal, Solver, sat
from functools import reduce

                                            #      |   | 1 |   | 1 |   |
rows = [[Int('r00'), 1, Int('r01'), 1],     #      | 1 | 1 | 1 | 1 | 1 |
        [],                                 # -----+---+---+---+---+---+
        [Int('r20'), 1, Int('r21'), 1],     #  1 1 |   |   |   |   |   |
        [Int('r30'), 3]]                    # -----+---+---+---+---+---+
cols = [[Int('c00'), 1],                    #      |   |   |   |   |   |
        [Int('c10'), 1, Int('c11'), 1],     # -----+---+---+---+---+---+
        [Int('c20'), 1],                    #  1 1 |   |   |   |   |   |
        [Int('c30'), 1, Int('c31'), 1],     # -----+---+---+---+---+---+
        [Int('c40'), 1]]                    #    3 |   |   |   |   |   |
                                            # -----+---+---+---+---+---+
nrows = len(rows)
ncols = len(cols)


def prefix_sum(l):
    """ Auxiliary function for computing the sums of all prefixes of a list l """
    return [sum(l[: i + 1]) for i in range(len(l))]


def xor_all(l):
    """ Auxiliary function for computing the xor of the elements of a list l """
    if not l:
        return BoolVal(False)
    return reduce(Xor, l)


def solve(formulas):
    """
    Solves a set of formulas using SMT; prints the outcome.
    Return model if SAT, None if not.
    """
    s = Solver()
    s.add(formulas)
    status = s.check()
    print(status)
    if status == sat:
        m = s.model()
        print(m)
        return m
