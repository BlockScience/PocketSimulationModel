from typing import Callable,List,NewType,TypedDict
# import pandas as pd

# from ..types import (
#     ParamType,
#     SystemParamsType,
#     BehaviorParamsType,
#     FunctionalParamsType,
# )

# ##############################################
# ## A method to take a SystemParamsType      ##
# ##  (defined in types/Config.py) and return ##
# ## a new SystemParamsType where each list   ##
# ## is updated individually according to a   ##
# ## specified method called `func`.          ##
# ##############################################

# def apply_list_function_to_sys_params_grid(
#     param_instance: SystemsParamType,
#     func: Callable[[List[float]], List[float]]
# ) -> SystemsParamType:
#     new_dict = {
#         key: func(value) if isinstance(value, list) else value
#         for key, value in custom_instance.items()
#     }
#     new_instance = SystemsParamType(**new_dict)
#     return new_instance


# # NOTE: Either List or list works for checking instances. 
# my_list = [1,2,3]
# print(f"{my_list} is an instance of list: {isinstance(my_list, list)}")
# print(f"{my_list} is an instance of List: {isinstance(my_list, List)}")

# MyType = NewType("MyType", int)
# print(f"MyType looks like {MyType}.")
# my_example = MyType(3)
# print(f"my_example looks like {my_example}")



# MockType = NewType(
#     "MockType",
#     TypedDict("MockTypedDict", {
#         "int_var_1": List[int],
#         "int_var_2": List[int],
#         "int_var_3": List[int],
#         "int_var_4": List[int],
#         "int_var_5": List[int],
#         "float_var_1": List[float],
#         "float_var_2": List[float],
#         "float_var_3": List[float],
#         "float_var_4": List[float],
#         "float_var_5": List[float],
#     })
# )

# my_first_mock_type = MockType(
#     { 
#         int_var_1=[1, 2, 3],
#         int_var_2=[4, 5, 6],
#         int_var_3=[7, 8, 9],
#         int_var_4=[10, 11, 12],
#         int_var_5=[13, 14, 15],
#         float_var_1=[1.1, 2.2, 3.3],
#         float_var_2=[4.4, 5.5, 6.6],
#         float_var_3=[7.7, 8.8, 9.9],
#         float_var_4=[10.10, 11.11, 12.12],
#         float_var_5=[13.13, 14.14, 15.15]
#     }
# )

def double_float_map(float_list: List[float]) -> List[float]:
    return [2*x for x in float_list ]

test_candidate = [1,2,3]
print(f"The result of applying double_float_map to {test_candidate} was {double_float_map(test_candidate)}")


