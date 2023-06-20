from ExpDerive.derive import resolve
# from ExpDerive.derive.evaluate import ExpTree, Var

from tests.resolver import resolver

def test_build_tree():
    tree = resolve.ExpTree('x+\\frac{y}{2}', 'g', resolver)
    tree.build_expression()
    print('\n'+str(tree.tree.expression))
    print('/////////////')
    assert str(tree.tree.expression).replace(' ','') == 'ast*2+pos/2-5/2'