"""

Semantics of arithmetic and boolean expressions.

Implemented according to
http://www.daimi.au.dk/~bra8130/Wiley_book/wiley.pdf (the book).

"""

from while_ast import *


tt = 'tt'
ff = 'ff'


def eval_arith_expr(e, s):
    """
    Semantics of arithmetic expressions.

    Implements Table 1.1 from the book.

    --- MODIFY THIS FUNCTION IN QUESTION 1 ---

    """

    if type(e) is ALit:
        return e.value

    elif type(e) is Var:
        return s[e.var_name]

    elif type(e) is Plus:
        return eval_arith_expr(e.a1, s) + eval_arith_expr(e.a2, s)

    elif type(e) is Times:
        return eval_arith_expr(e.a1, s) * eval_arith_expr(e.a2, s)

    elif type(e) is Minus:
        return eval_arith_expr(e.a1, s) - eval_arith_expr(e.a2, s)

    elif type(e) is Div:
        return eval_arith_expr(e.a1, s) / eval_arith_expr(e.a2, s)

    elif type(e) is Mod:
        return eval_arith_expr(e.a1, s) % eval_arith_expr(e.a2, s)

    else:
        assert False # Error


def eval_bool_expr(e, s):
    """
    Semantics of arithmetic expressions

    Implements Table 1.2 from the book.

    --- MODIFY THIS FUNCTION IN QUESTION 1 ---

    """

    # Note: This could have been written in more concisely,
    # but I chose to follow the definitions in Table 1.2 in the book strictly,
    # in the same style of nos.py, sos.py.
    if type(e) is BLit and e.value is True:
        return tt

    elif type(e) is BLit and e.value is False:
        return ff

    elif type(e) is Eq and eval_arith_expr(e.a1, s) == eval_arith_expr(e.a2, s):
        return tt

    elif type(e) is Eq and eval_arith_expr(e.a1, s) != eval_arith_expr(e.a2, s):
        return ff

    elif type(e) is LE and eval_arith_expr(e.a1, s) <= eval_arith_expr(e.a2, s):
        return tt

    elif type(e) is LE and eval_arith_expr(e.a1, s) > eval_arith_expr(e.a2, s):
        return ff

    elif type(e) is Not and eval_bool_expr(e.b, s) is ff:
        return tt

    elif type(e) is Not and eval_bool_expr(e.b, s) is tt:
        return ff

    elif type(e) is And and eval_bool_expr(e.b1, s) is tt and eval_bool_expr(e.b2, s) is tt:
        return tt

    elif type(e) is And and eval_bool_expr(e.b1, s) is ff or eval_bool_expr(e.b2, s) is ff:
        return ff

    elif type(e) is Or and eval_bool_expr(e.b1, s) is tt or eval_bool_expr(e.b2, s) is tt:
        return tt

    elif type(e) is Or and eval_bool_expr(e.b1, s) is ff and eval_bool_expr(e.b2, s) is ff:
        return ff

    else:
        return ff # Error


if __name__ == '__main__':
    # (x + 1) * (x - 1)
    a = Times(Plus(Var('x'), ALit(1)), Minus(Var('x'), ALit(1)))

    print a
    print eval_arith_expr(a, {'x':10})
    print

    b = And(LE(ALit(1), ALit(2)),
            Not(BLit(False)))

    print b
    print eval_bool_expr(b, {'x':10})
    print

    c = Div(Var('x'), Var('y'))
    print c
    print eval_arith_expr(c, {'x': 5, 'y': 3})
    print

    d = Mod(Var('x'), Var('y'))
    print d
    print eval_arith_expr(d, {'x': 5, 'y': 3})
    print

