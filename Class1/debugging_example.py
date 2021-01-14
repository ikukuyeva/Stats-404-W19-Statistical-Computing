""" Example of debugging and breakboints.
    
    To try it, run it from command line as:
    python3 -m pdb example.py
"""

import pdb 


def my_awesome_function(x):
    """Example of error handling."""
    try:
        pdb.set_trace()
        y = x + 2
        pdb.set_trace()
        y += 3
        print(y)
        pdb.set_trace()
    except TypeError as e:
        raise e


if __name__ == '__main__':
	my_awesome_function(3)
	my_awesome_function('a')
