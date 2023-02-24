# from ...exp_derive.ExpDerive.derive import evaluate
from ExpDerive.derive import evaluate
# evaluate = ExpDerive.derive.evaluate
from importlib import import_module

t1, t2 = evaluate.t1, evaluate.t2
# mod = import_module('exp_derive.ExpDerive.derive.evaluate')

def test1():
    assert t1(3) == 4

def test2():
    assert t2(4) == 6