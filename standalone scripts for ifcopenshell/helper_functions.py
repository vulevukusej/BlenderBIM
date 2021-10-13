from inspect import getmembers
from inspect import ismethod

def attributeExtractor(cls):
    # thanks to user for providing this code: https://stackoverflow.com/a/41737776/16028121
    for i in getmembers(cls):
        # Ignores anything starting with underscore 
        # (that is, private and protected attributes)
        if not i[0].startswith('_'):
            # Ignores methods
            if not ismethod(i[1]):
                print(i)