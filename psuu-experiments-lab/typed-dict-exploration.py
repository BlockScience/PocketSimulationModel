# Exploring Types and TypedDicts with Population-Level Operators

from typing import (Callable, Dict, List, NewType, TypedDict, Union)

# my_type = NewType("my_type", int)

# # NewType
# my_int = my_type(3)
# print(f"The value of my_int is {my_int}")

# #TypedDict inheriting from NewType

# MyTypedDict = TypedDict("MyTypedDict",
#                         {
#                             "int_var_1": int,
#                             "float_var_1": float  
#                         }
#                     )

# my_dict_example = MyTypedDict({"int_var_1" : 1, "float_var_1" : 3.1415})

# for k,v in my_dict_example.items():
#     print(f"The value of {k} is {v}.")

# # This allows a List which contains either ints or floats.
# # In practice, we are working with Lists that need to be one or the other. 
# NumberList = NewType("NumberList", List[Union[int, float]])

# def create_new_dict_from_old(old_dict:Dict[str, NumberList],
#                             dict_of_funcs_to_use: Dict[str, Callable[NumberList, NumberList]],
#                             ):
#     # TODO: Docstring for function
#     ####################################################
#     ## NOTE: For each key in the original dictionary, ##
#     ## we assume the value is a list that contains    ##
#     ## numbers (ints or floats).                      ##
#     ## Each key has a designated map that takes a     ##
#     ## list as input, and returns a list as output.   ##
#     ## The method applies the map to each list to     ##
#     ## create a new dictionary of number lists,       ##
#     ## updated based on the func_to_use.              ##
#     ####################################################

#     new_dict = {  dict_of_funcs_to_use.get(key)(val)
#                   for key,val in old_dict.items() 
#                }

# # TODO: Add conditions_to_meet as a dictionary of boolean functions to evaluate validity of 
# # produced NumberList. 

from typing import NewType, List, Union, Dict, Callable

# Define the NumberList type
NumberList = NewType("NumberList", List[Union[int, float]])

# Define the NumberListFuncDict type
NumberListFuncDict = NewType("NumberListFuncDict", Dict[str, Callable[[NumberList], NumberList]])

def apply(func, *args, **kwargs):
   """
   8 think Python may have this already, but couldn't find it.
   """
   return func(*args, **kwargs)


# Example usage
def process_numbers(numbers: NumberList) -> NumberList:
    # Example implementation
    new_numbers = [2*number for number in numbers]
    return new_numbers

# Creating a dictionary with the specified type hints
my_func_dict: NumberListFuncDict = {
    "example_function": process_numbers
}
my_number_list = NumberList([1, 2.5, 3])

# Using the dictionary
result = apply(my_func_dict["example_function"],NumberList([1, 2.5, 3]))

print(f"The result of calling my_funct_dict on the example is {result}")

# NOTE: We are basically there!

# Take the dictionary of functions
# Apply each function to the List to generate a new List. 
# Be sure the function works with an instance of a TypedDict. 
# Begin experimenting and profiling. 

# Determine whether apply vs. the dict[func](my_thing) performance degrades enough to 
