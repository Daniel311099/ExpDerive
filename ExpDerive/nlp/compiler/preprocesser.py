import json
from .myTypes import Phrase, ProcessedFunc, ProcessedArgs
from .utils import insertArgDelimiters, insertFuncDelimiters, parseArgs, parseFunc


def preprocessFunc(phrase: Phrase):
    funcLoc = phrase.root_func
    processed = insertFuncDelimiters(phrase.phrase, funcLoc)
    return processed


def preprocessArgs(phrase: Phrase):
    if phrase.type == "prefix":
        argLocs = []
        last = phrase.root_func[1] 
        for arg in phrase.args:
            argLocs.append([last, arg])
            last = arg
        # print(argLocs)
        if len(argLocs) == 0:
            argLocs.append([phrase.root_func[1], len(phrase.phrase.split(" "))])
        processed = insertArgDelimiters(phrase.phrase, argLocs)
        return processed
    
    elif phrase.type == "suffix":
        argLocs = []
        last = 0
        for arg in phrase.args:
            argLocs.append([last, arg])
            last = arg
        if len(argLocs) == 0:
            argLocs.append([0, phrase.root_func[0]])
        # print(argLocs)
        processed = insertArgDelimiters(phrase.phrase, argLocs)
        return processed
    
    elif phrase.type == "infix":
        argLocs = [
            [0, phrase.root_func[0]],
            [phrase.root_func[1], len(phrase.phrase.split(" "))]
        ]
        processed = insertArgDelimiters(phrase.phrase, argLocs)
        return processed
    

def preprocess():
    processedFuncList: list[ProcessedFunc] = []
    processedArgsList: list[ProcessedArgs] = []
    with open('/Users/danielfisaha/exp_derive/ExpDerive/training_data/training_data.json') as f:
        data = json.load(f)
        for phrase in [Phrase(**d) for d in data]:            
            processedFunc = preprocessFunc(phrase)
            processedFuncObj = ProcessedFunc(
                phrase.phrase,
                processedFunc,
            )
            processedFuncList.append(processedFuncObj)
            processedArgs = preprocessArgs(phrase)
            processedArgsObj = ProcessedArgs(
                phrase.phrase,
                processedArgs,
            )
            processedArgsList.append(processedArgsObj)

    print(processedFuncList)
    print(processedArgsList)
    # writeFuncs(processedFuncList)
    # writeArgs(processedArgsList)


def writeFuncs(
        funcs: list[ProcessedFunc], 
        template = "Annotate the root function from the following expression using @@ to mark the start and ## to mark the end: "
):
    with open("/Users/danielfisaha/exp_derive/ExpDerive/training_data/preparedFuncs.jsonl", "a") as funcF:
        for func in funcs:
            processedFunc = {
                "prompt": template + func.phrase,
                "completion": func.processed
            }
            # print(processedFunc)
            funcF.write(json.dumps(processedFunc) + "\n")

def writeArgs(
        args: list[ProcessedArgs], 
        template = "Annotate the arguments from the following expression using @@ to mark the start and ## to mark the end: "
):
    with open("/Users/danielfisaha/exp_derive/ExpDerive/training_data/preparedArgs.jsonl", "a") as argF:
        for arg in args:
            processedArgs = {
                "prompt": template + arg.phrase,
                "completion": arg.processed
            }
            # print(processedArgs)
            argF.write(json.dumps(processedArgs) + "\n")