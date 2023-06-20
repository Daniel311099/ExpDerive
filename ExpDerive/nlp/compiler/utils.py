from .myTypes import Func, Phrase

def insertFuncDelimiters(phrase: str, funcLoc: tuple[int, int], start="@@", end="##") -> str:
    split = phrase.split(" ")
    # insert start and end delimiters
    split.insert(funcLoc[0], start)
    split.insert(funcLoc[1]+1, end)
    phrase = " ".join(split)
    return phrase

def insertArgDelimiters(phrase: str, argLocs: list[tuple[int, int]], start="@@", end="##") -> str:
    split = phrase.split(" ")
    out = split.copy()
    for i, argLoc in enumerate(argLocs):
        # insert start and end delimiters
        arg = split[argLoc[0]:argLoc[1]]
        # print(arg, argLoc)
        out[argLoc[0]+2*i:argLoc[1]+2*i] = [start] + arg + [end]
    # print(split)
    return " ".join(out)

def parseFunc(processed: str, start="@@", end="##"):
    # given a phrase with the function delimited by start and end, return a func object
    processed = processed.split(" ")
    print(processed)
    startIdx = listFind(processed, start)
    endIdx = listFind(processed, end)
    name = " ".join(processed[startIdx+1:endIdx])
    if startIdx == -1 or endIdx == -1:
        return None
    if startIdx == 0:
        t = 'prefix'
    elif endIdx == len(processed)-1:
        t = 'suffix'
    else:
        t = 'infix'
    return Func(name, t, None, (startIdx, endIdx - 1))

def parseArgs(processed: str, start="@@", end="##") -> list[str]:
    # given a phrase with a set of arguments delimited by start and end, return a list of strings of the arguments
    args = []
    startIdx = listFind(processed, start)
    endIdx = listFind(processed, end)
    while startIdx != -1 and endIdx != -1:
        args.append(processed[startIdx+len(start):endIdx].strip())
        processed = processed[endIdx+len(end):].strip()
        startIdx = listFind(processed, start)
        endIdx = listFind(processed, end)
    return args

def listFind(arr, item):
    try:
        return arr.index(item)
    except ValueError:
        return -1