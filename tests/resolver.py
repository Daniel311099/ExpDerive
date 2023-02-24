LATEX = {
    'a_': {
        'latex': 'x+\\frac{y}{2}',
        'name': 'a',
        'leaf': False,
    },
    'b_': {
        'latex': '\\mathit{gls}^2',
        'name': 'b',
        'leaf': False,
    },
    'x': {
        'latex': '\\mathit{ast}*2',
        'name': 'x',
        'leaf': False,
    },
    'y': {
        'latex': '\\mathit{pos}-5',
        'name': 'y',
        'leaf': False,
    },
    'gls': {
        'name': 'gls',
        'leaf': True,
    },
    'pos': {
        'name': 'pos',
        'leaf': True,
    },
    'ast': {
        'name': 'ast',
        'leaf': True,
    }
}

ALIASES = {
    'a': 'a_',
    'b': 'b_',
}

STATS = {
    'gls': {
        'pl1': 5,
        'pl2': 10,
        'pl3': 15,
    },
    'pos': {
        'pl1': 7,
        'pl2': 12,
        'pl3': 17,
    },
    'ast': {
        'pl1': 9,
        'pl2': 14,
        'pl3': 19,
    }
}

FUNCTIONS = {
    'f': {
        'latex': '\h\left(x\\right)-3',
        'params': ['x', 'y'],
    },
    'g': {
        'latex': '\\x + y',
        'params': ['x', 'y'],
    },
    'h': {
        'latex': 'm^2',
        'params': ['m'],
    },
    'm': {
        'latex': 'g\left(x\cdot 2, 4+\mathit{pos}\\right)+3',
        'params': ['x'],
    },
    'p': {
        'func': lambda x: x**2,
        'params': ['x'],
    }
}

def resolver(var, namespace=None):
    try:
        var = ALIASES[str(var)]
    except KeyError:
        pass
    lat = LATEX[str(var)]
    lat['namespace'] = None
    return lat


def eval_resolver(stat, subject):
    return STATS[str(stat)][subject]

def func_resolver(func):
    return FUNCTIONS[str(func)]