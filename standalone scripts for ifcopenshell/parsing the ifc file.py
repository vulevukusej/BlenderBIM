import ifcopenshell
from ifcopenshell.util.selector import Selector

selector = Selector()

filepath = "C:/Users/vpaji/OneDrive/Documents/Blender/Test Projects/test.ifc"
ifc = ifcopenshell.open(filepath)

# retrieve all columns (https://wiki.osarch.org/index.php?title=IfcOpenShell_code_examples)
columns = selector.parse(ifc, '.IfcColumn') # This is equivalent to ifc.by_type('IfcColumn')
print(columns[0])

# search by specific guid
test = selector.parse(ifc, '#3UHJKz$fXBCguXA7iDv$w3')
print(test)