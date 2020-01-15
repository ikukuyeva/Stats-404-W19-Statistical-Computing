#!/usr/bin/env python
# coding: utf-8

get_ipython().run_line_magic('pdb', '')
import os
ORIG_DIR = os.getcwd()
# # Introduction to Python

# Python and [Python Enhancement Proposals (PEPs)](https://docs.python-guide.org/intro/community/) "describe changes to Python itself, or the standards around it".

# [PEP 8](https://pep8.org/) = **The Style Guide for Python Code**
# 

# [PEP 20](https://www.python.org/dev/peps/pep-0020/) = **The Zen of Python**
# ```
# Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Complex is better than complicated.
# Flat is better than nested.
# Sparse is better than dense.
# Readability counts.
# Special cases aren't special enough to break the rules.
# Although practicality beats purity.
# Errors should never pass silently.
# Unless explicitly silenced.
# In the face of ambiguity, refuse the temptation to guess.
# There should be one-- and preferably only one --obvious way to do it.
# Although that way may not be obvious at first unless you're Dutch.
# Now is better than never.
# Although never is often better than *right* now.
# If the implementation is hard to explain, it's a bad idea.
# If the implementation is easy to explain, it may be a good idea.
# Namespaces are one honking great idea -- let's do more of those!
# ```

# Goal: Aim for `pythonic` code [[reference]](https://blog.startifact.com/posts/older/what-is-pythonic.html)

# ## Python Basics
#  Reference for further reading: https://automatetheboringstuff.com/chapter1/

# ### Expressions

# In[11]:


3 + 5


# In[17]:


3 + 'a'


# In[18]:


str(3) + 'a'


# In[19]:


f"3a"


# In[20]:


3 * 'a'


# ### Variable Assignment

# In[35]:


grade = 89.3


# In[30]:


grade


# In[36]:


grade += 5


# In[37]:


grade


# ## Comments
# **Tip**: Add an in-line comment to your code to explain 'why' that line of code is the way it is, esp. if it's not obvious from reading the code.
#   - EX: Explain "Magic numbers" in code
# 
# **Tip**: Keep comments up-to-date



# This is a one-line comment

# This is a multi-line
# comment


# ## Control Flow
# - NOTE: Booleans in Python are True and False, not TRUE and FALSE (as in R)
# - NOTE: Indentation, not {} indicate groups of lines in Python
# - Reference for further reading: https://automatetheboringstuff.com/chapter2/

# ### If-else Logic

# In[39]:


if 90 <= grade:
    print('A')
elif 80 <= grade < 90:
    print('B')
elif 70 <= grade < 80:
    print('C')
else:
    print('F')


# ### While Loop

# In[43]:


number_students_enrolled = 0

while number_students_enrolled < 30:
    number_students_enrolled += 1
else:
    # Prints after the while-loop finishes:
    print(number_students_enrolled)


# In[47]:


number_students_enrolled = 0

while True:
    number_students_enrolled += 1
    if number_students_enrolled == 30:
        break
else:
    print(number_students_enrolled)


# Why does the `print()` statement not get executed?

# ### For Loop

# In[53]:


for i in range(5):
    print(i * '*')
else:
    print("For-loop finished.")


# Note: `range()` includes lower bound, but *not* upper bound.

# In[54]:


for j in range(-5, 3, 2):
    print(j)


# ## Functions
# Reference for further reading: https://automatetheboringstuff.com/chapter3/

# ### Defining Functions

# In[61]:


def my_awesome_function():
    print("Hi!")
    print("How are you?")


# In[63]:


my_awesome_function()
my_awesome_function()


# In[68]:


def my_awesome_function(x):
    """Example of function with parameters."""
    print(f"Initial value: {x}")
    print(f"Previous value: {x - 1}")
    print(f"Next value: {x + 1}")


# In[67]:
# - `"""Example of function with parameters."""` is called a docstring, which can be turned into Python documentation (more on this below). 
# - Recommendation for what to include in a docstring: 
#   - description of function
#   - explanation of function arguments and return values
#   - example usage
# - Please see [PEP 257](https://www.python.org/dev/peps/pep-0257/) for Docstring Conventions.



my_awesome_function(3)


# In[69]:
# Python functions return `None` if no return statement is specified:

# Copied from previous slide to make comparison easier:
def my_awesome_function(x):
    """Example of function with parameters."""
    print(f"Initial value: {x}")
    print(f"Previous value: {x - 1}")
    print(f"Next value: {x + 1}")

result = my_awesome_function(3)
result is None


def my_awesome_function(x):
    """Example of function with parameters and return statement."""
    return x + 2


# In[70]:


result = my_awesome_function(7)
result


# Tip: Name functions to make it obvious to the next person (or you in 6 months) what the function does:
# `create_filename_with_timestamp()` vs `format_string()`.
# 
# What's a better name for `my_awesome_function()`?

# Why do we need functions?

# ### Loading Third-Party Functions/Modules

# Import whole module:



import random
random.seed(2019)
random.randint(0, 5)


# Import two functions from module:



from math import fabs, floor, pi, sin
print(fabs(-2))
print(floor(3.2))
print(sin(pi))


# Tip: Either format is valid; focus on what makes code more readable and understadable (esp. when bugs happen).

# ### Local and Global Scope

# Global scope cannot access local variables:

# In[77]:


def my_awesome_function(x):
    """Example of function where y is in local scope."""
    y = x + 2
    return y


# In[75]:


my_awesome_function(7)


# In[78]:


y


# Variables in different scopes can have same name:

# In[81]:


# y is in global and local scopes:
y = 3
print(my_awesome_function(7))
y


# Additional caveats about scoping:
# - A function's local scope *can* access variables defined in global scope. But it's not good practice to do so, because it's harder to debug.
# - A function's local scope *cannot* access variables defined in another function's local scope. 
# 

# ### Exception Handling

# In[84]:


def my_awesome_function(x):
    """Example of error handling."""
    try:
        y = x + 2
    except TypeError:
        print("Error: Invalid argument for x -- numeric input expected.")


# In[85]:


my_awesome_function('a')


# 10 minute break

# ## Python Types
# Reference for further reading: https://automatetheboringstuff.com/chapter4/ and https://data-flair.training/blogs/python-data-structures-tutorial/

# In[88]:


print(type(3))
print(type(3.0))


# ### Lists

# In[90]:


[1, 3, 'abc', True, [2, 3]]


# ![Slice notation explained](images/slice_notation_explained.jpg)
# 
# [Reference](https://stackoverflow.com/questions/509211/understanding-pythons-slice-notation)
# 
# Note/caution: range includes lower bound, but not upper bound -- and starts at 0 (!).
# 
# `Name = ['F', 'u', 'd', 'g', 'e']`

# In[147]:


Name = ['F', 'u', 'd', 'g', 'e']


# In[148]:


len(Name)


# In[149]:


Name[0] = 'Sm'
Name


# In[150]:


[Name[0]] + ['i'] + Name[2:5]


# In[151]:


# Recall: Name = ['Sm', 'u', 'd', 'g', 'e']
del Name[2]
Name


# In[152]:


for i in range(len(Name)):
    print(Name[i])


# In[153]:


for letter in Name:
    print(letter)


# In[154]:


'F' in Name


# In[155]:


'F' not in Name


# In[156]:


# 'Unpacking' list:
x1, x2, x3 = [1, 2, 3]
print(f"{x1} {x2} {x3}")


# In[157]:


# Recall: Name = ['Sm', 'u', 'g', 'e']
Name.index('g')


# In[158]:


Name.append('d')
Name


# In[159]:


Name.insert(2, 'd')
Name


# In[160]:


# Caution: only first value is removed, if duplicates are present:
Name.remove('d')
Name


# In[162]:


Name.sort()
Name


# In[163]:


Name.sort(key=str.lower)
Name


# **Caution:** `sort()` method sorts in-place, which means that the function returns `None`. A common bug is assigning output of `sort()` to another variable that you then operate on -- but it's value is now `None` (!).

print([3, 2, 1].sort())
print(sorted([3,2,1]))
# ### Strings

# In[165]:


Name_string = 'Fudge'


# In[168]:


Name_string[2:-1]


# In[169]:


"F" in Name_string


# In[170]:


for letter in Name_string:
    print(letter)


# Note: strings are **not mutable**, i.e. you can't update a string, but you can create a new one:

# In[171]:


Name_string[0] = "Sm"


# In[175]:


Name_string[0] + 'i' + Name_string[2:5] + 't'


# ### Tuples
# Tip: Use tuples to signal to someone reading your code that this variable will not change in the code base.

# In[176]:


Name_tuple = ('F', 'u', 'd', 'g', 'e')


# Note: tuples are also **not mutable**, i.e. you can't update a string, but you can create a new one:

# In[177]:


Name_tuple[0] = "Sm"


# In[180]:


print(type(('abc',)))


# In[184]:


tuple([1, 2, 3])


# In[182]:


# Recall: Name_string = 'Fudge'
tuple(Name_string)


# In[183]:


list(Name_tuple)


# In[210]:
# Unpacking tuples:


y1, y2, y3 = tuple([4, 5, 6])
print(f"{y1} {y2} {y3}")


def my_awesome_function(x):
    """Example of function with parameters."""
    return x, x-1, x+1

current_value, previous_value, next_value = my_awesome_function(3)
print(f"Current value: {current_value}, Previous value: {previous_value}, Next value: {next_value}")
# ### Sets
# Sets are **mutable** tuples with unique entries that allow set operations.

# In[203]:


set([2, 1, 'abc', '4a', 2])


# In[221]:


Name_set = set(Name)
Name_set


# In[222]:


Name_set - set(list('Fudge'))


# In[223]:


Name_set.intersection(set(list('Fudge')))


# In[224]:


Name_set.union(set(list('Fudge')))


# In[225]:


# Drop the first element of set:
Name_set.pop()


# ### Dictionaries
# Dictionaries are:
# - Made of key-value pairs
# - Unordered, i.e. there's no "first" dictionary element
# - It's O(1) operation for accessing items in list, vs. O(n) for a list.
# 
# Reference for further reading: https://automatetheboringstuff.com/chapter5/

# In[231]:


dictionary1 = {'key1': 'value1',
               'key2': 'value2'
              }
dictionary2 = {'key2': 'value2',
               'key1': 'value1'
              }
dictionary1 == dictionary2


# In[233]:


course_information = {'name': 'Statistical Computing and Programming',
                      'number': 404,
                      'instructor': 'Irina Kukuyeva',
                      'TA': 'Theja Voora Naga Sree'
                     }


# In[234]:


course_information['name']


# In[236]:


course_information['Room'] = 'PAB 1749'


# In[240]:


f"Welcome to Stats {course_information['number']}: {course_information['name']}"


# In[241]:


course_information.keys()


# In[242]:


course_information.values()


# In[243]:


course_information.items()


# In[245]:


'names' in course_information.keys()


# In[238]:


course_information.get('names', 'Missing Name')


# ## Directories in Python



import os
print(os.getcwd())




os.chdir("..")
print(os.getcwd())




os.path.join(os.getcwd(), "file_name.csv")


# 10 minute break

# # Intermediate Python

# ## List, Typle and Dictionary Comprehension
# List/Tuple/Dictioary comprehension is an alternative to a for-loop that's a few lines long.



# List comprehension:
[(values, keys) for (keys, values) in course_information.items()]




# Dictionary comprehension:
{values: keys for (keys, values) in course_information.items()}


# What would `tuple` comprehension look like?

# ## Passing by Reference (Python) vs Passing by Value (R)
# **Note**: Common cause of bugs in code.
# 
# Reference: https://automatetheboringstuff.com/chapter4/
# 

# ### Lists

# In[226]:
# --- Example 1:
spam = [0, 1, 2, 3, 4, 5]
cheese = spam
print(f"spam: {spam} and cheese: {cheese}")


# ![Memory location of both variables](./images/pass_by_reference_init.jpg)


cheese[1] = 'Hello'
print(f"spam: {spam} and cheese: {cheese}")




# In[227]:
os.chdir(ORIG_DIR)


# ![Memory location of both variables](./images/pass_by_reference_after_update.jpg)
# --- Example 2:
import copy
spam = [0, 1, 2, 3, 4, 5]
# Make (shallow) copy of variable:
cheese = copy.copy(spam)
print(f"spam: {spam} and cheese: {cheese}")
cheese[1] = 'Hello'
print(f"spam: {spam} and cheese: {cheese}")


# In[228]:


# --- Example 3:
variable1 = [1, 3, [[2], 4]]
# Make shallow copy of variable:
variable2 = copy.copy(variable1)
# Make deep copy of variable:
variable3 = copy.deepcopy(variable1)
print(f"Variable 1: {variable1}") 
print(f"Variable 2: {variable2} <- copy.copy of variable 1")
print(f"Variable 3: {variable3} <- copy.deepcopy of variable 1")

variable1[2][0] = [-1]
print()
print("--- After updating an element in sub-list of variable 1:")
print(f"Variable 1: {variable1}") 
print(f"Variable 2: {variable2} <- copy.copy of variable 1")
print(f"Variable 3: {variable3}  <- copy.deepcopy of variable 1")


# ### Dictionaries

# In[247]:


# Example 1:
dictionary1 = {'key1': 'value1',
               'key2': 'value2'
              }
dictionary2 = dictionary1
print(f"Dictionary 1: {dictionary1}")
print(f"Dictionary 2: {dictionary2}")

dictionary2['key2'] = '2'
print()
print("--- After updating 'key2':")
print(f"Dictionary 1: {dictionary1}")
print(f"Dictionary 2: {dictionary2}")


# In[248]:


# Example 2:
dictionary1 = {'key1': 'value1',
               'key2': 'value2'
              }
dictionary2 = copy.deepcopy(dictionary1)
print(f"Dictionary 1: {dictionary1}")
print(f"Dictionary 2: {dictionary2}")

dictionary2['key2'] = '2'
print()
print("--- After updating 'key2':")
print(f"Dictionary 1: {dictionary1}")
print(f"Dictionary 2: {dictionary2}")


# ## Functional Programming
# Type of programming that takes an input and get output, similar to mathematical functions; for more information, see this [blog post](https://medium.com/@rohanrony/functional-programming-in-python-1-lambda-map-filter-reduce-zip-8739ea144186) and this [one](https://www.programiz.com/python-programming/anonymous-function)

# In[251]:
# ### lambda (functions)
# Lambda functions are anonymous functions, i.e. defined without a name. They are typically ~1-2 lines of code.



add_one_fcn = lambda x: x + 1
add_one_fcn(2)


# ### map
# `map()` requires a function and a list; it will apply the function specified to every item in the list.



list(map(add_one_fcn, [3, 6, -2]))




lower_fcn = lambda x: x.lower()
list(map(lower_fcn, course_information.keys()))


# ### zip
# `zip()` combines two objects (of same size) to create one new one



ex_list = [1, 'Hello', 5]
ex_tuple = ('abc', 3, 'bcd')

list(zip(ex_list, ex_tuple))


# # Understanding Errors, Fixing Bugs and Getting Help

# ## Common Bugs and Fixes

# ### Common Errors

# `TypeError: can only concatenate str (not "int") to str` 
# - **Possible cause**: trying to concatenate numbers and strings in a `print()` statement
# - **Possible solution**: use f-strings

# `SyntaxError: invalid syntax`
# - **Possible causes**: 
#   - Incorrect spelling (of the function, variable, etc.)
#   - Including a `>>>` when copying code from the Console
#   - Specifying an incorrect closing symbol (rather than a parenthesis) at the end of a function
#   - Having an extra bracket when subsetting

# Trailing `...`:
# - **Possible causes**: 
#   - Not closing a function call with a parenthesis
#   - Not closing brackets when subsetting

# `TypeError: unsupported operand type(s) for +: 'NoneType' and ` something else
# - **Possible cause**: 
#   - Performing an operation in-place (such as `sort()`) and assigning result to another variable; because the operation was done in-place, the new variable has a value of `None`
# - **Possible solution**: 
#   - Use `sorted(list_variable)` vs. `list_variable.sort()`

# ### Common Bugs
# - Python is 0 offset vs R is 1-offset
#   - e.g. especially when subsetting
# - Python ranges include lower bound but not upper bound
#   - e.g. especially when in a loop
# - Python passes by reference vs R by value
#   - e.g. using `copy.copy` vs `copy.deepcopy`
# - Python code blocks are indented vs R uses `{}`
# - Python functions return `None` if `return` is not explicitly specified 

# ## Debugger

# ![Debugging Cartoon](./images/debugging_cartoon.jpg)[[2]](https://www.reddit.com/r/ProgrammerHumor/comments/bwsfwy/fun_for_the_whole_team/)

# (Very brief) Overview of debugging in Python -- not via `print()` statements:
# 
# **1. Starting debugger**
# 
# Option 1: When executing a script:
# - Add line `import pdb` to your script
# - When running script from command line, call it as follows:
# `python -m pdb example.py`
# - If/when code breaks, you'll enter the code base at the break point
# 
# Option 2: When working in notebook, add `%pdb` to:
# - a cell you're interested in debugging, or 
# - at the top, to do interactive debugging any time an error is thrown

# **2. Adding breakpoints**
# You can add a breakpoint, to step into the code base at designated line, by:
# - Add line `import pdb` to your script
# - Add line `pdb.set_trace()` above the line you want to look into
# 
# **3. Exiting debugger**
# Type `q` to exit the debugger.
# 
# **4. References**
# Please see:
# - [pdb documentation](https://docs.python.org/3/library/pdb.html) for more debugger commands
# - Type `%lsmagic` to see all available magic methods and see [IPython documentation](https://ipython.readthedocs.io/en/stable/interactive/magics.html) for other notebook magic commands
# 



def my_awesome_function(x):
    """Example of error handling."""
    try:
        y = x + 2
    except TypeError as e:
        print("Error: Invalid argument for x -- numeric input expected.")
        raise e


# Note: It's better to `raise` an error thrown by function, than silently letting the function fail, via `print`ing the error.


get_ipython().run_line_magic('pdb', '')
my_awesome_function('a')


# ![Screenshot of debugger](images/pdb_image.png)

# ## Getting Help

# **Step 0**: Check internal documentation


get_ipython().run_line_magic('pinfo', 'randint')


get_ipython().run_line_magic('pinfo', 'my_awesome_function')


help(random.randint)


# **Step 1**: Check external documenation, e.g. Google your error

# EX: `TypeError: can only concatenate str (not "int") to str`

# **Step 2**: Reach out for help, per [Class 0 quidelines](http://bit.ly/2SPtCVi)
