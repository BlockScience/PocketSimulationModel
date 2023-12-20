from copy import deepcopy
from ..types import (
    ParamType,
    SystemParamsType,
    BehaviorParamsType,
    FunctionalParamsType,
)
from typing import Dict
from itertools import product

def do_something():
    my_list = [1,2,3]
    print(f"{my_list} is an instance of list: {isinstance(my_list, list)}")
    print(f"{my_list} is an instance of List: {isinstance(my_list, List)}")

def __main__():
    print("We are in main. Might as well do something.")
    do_something()

if __name__ == "__main__":
    main()