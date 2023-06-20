from dataclasses import dataclass
from typing import Optional, Union, Literal

@dataclass
class Func:
    name: str
    type: str
    custom: Optional[bool]
    loc: tuple[int, int]

@dataclass
class Phrase:
    phrase: str
    type: Union[Literal["infix"], Literal["prefix"], Literal["suffix"]]
    root_func: tuple[int, int]
    args: list[int]

@dataclass
class ProcessedFunc:
    phrase: str
    processed: str

@dataclass
class ProcessedArgs:
    phrase: str
    processed: str