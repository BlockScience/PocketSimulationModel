from typing import NewType, TypedDict

StateType = NewType("State", TypedDict("State", {}))

ParamType = NewType("Params", TypedDict("Params", {}))

SystemParamsType = NewType("SystemParams", TypedDict("System Params", {}))
BehaviorParamsType = NewType("BehaviorParams", TypedDict("Behavior Params", {}))
FunctionalParamsType = NewType("FunctionalParams", TypedDict("Functional Params", {}))
