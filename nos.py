"""
Natural Operational Semantics (NOS) of statements

Implemented according to
http://www.daimi.au.dk/~bra8130/Wiley_book/wiley.pdf (the book).

"""

from while_ast import *
from expr import *

def nos(S, s):
    """
    Natural Operational Semantics (NOS) of statements

    Returns s' such that <S, s> --> s'

    Implements Table 2.1 from the book.

    --- MODIFY THIS FUNCTION QUESTIONS 1, 3 ---

    """

    if type(S) is Skip:
        return s

    elif type(S) is Assign:
        sp = s.copy()
        sp[S.lhs] = eval_arith_expr(S.rhs, s)
        return sp

    elif type(S) is Comp:
        sp = nos(S.S1, s)
        spp = nos(S.S2, sp)
        return spp

    elif type(S) is If and eval_bool_expr(S.b, s) is tt:
        sp = nos(S.S1, s)
        return sp

    elif type(S) is If and eval_bool_expr(S.b, s) is ff:
        sp = nos(S.S2, s)
        return sp

    elif type(S) is While and eval_bool_expr(S.b, s) is tt:
        sp = nos(S.S, s)
        spp = nos(While(S.b, S.S), sp)
        return spp

    elif type(S) is While and eval_bool_expr(S.b, s) is ff:
        return s

    elif type(S) is Repeat:
        sp = nos(S.S, s)
        if eval_bool_expr(S.b, sp) is tt:
            return sp
        elif eval_bool_expr(S.b, sp) is ff:
            spp = nos(Repeat(S.S, S.b), sp)
            return spp
        else:
            assert False # Error

    else:
        assert False # Error


if __name__ == '__main__':
    prog = Comp(Assign('y', ALit(1)),
                While(Not(Eq(Var('x'), ALit(1))),
                      Comp(Assign('y', Times(Var('y'), Var('x'))),
                           Assign('x', Minus(Var('x'), ALit(1))))))

    print nos(prog, {'x': 5})

    prog = Comp(Assign('a', ALit(84)),
           Comp(Assign('b', ALit(30)),
                While(Not(Eq(Var('b'), ALit(0))),
                      Comp(Assign('t', Var('b')),
                      Comp(Assign('b', Mod(Var('a'), Var('b'))),
                           Assign('a', Var('t'))))
                )))
    #print prog
    print nos(prog, {})

    # Repeat tests:
    prog = Comp(Assign('a', ALit(84)),
           Comp(Assign('b', ALit(30)),
                Repeat(
                      Comp(Assign('t', Var('b')),
                      Comp(Assign('b', Mod(Var('a'), Var('b'))),
                           Assign('a', Var('t')))),
                      # until
                      Eq(Var('b'), ALit(0))
                )))
    #print prog
    print nos(prog, {})

    prog = Repeat(#x := x - 10
                  Assign('x', Minus(Var('x'), ALit(10))),
                  #until x < 10
                  And(LE(Var('x'), ALit(10)), Not(Eq(Var('x'), ALit(10))))
                  )
    #print prog
    print nos(prog, {'x': 55})
    print nos(prog, {'x': 7})
