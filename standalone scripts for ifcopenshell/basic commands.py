import ifcopenshell

filepath = "C:/Users/vpaji/OneDrive/Documents/Blender/Test Projects/test.ifc"
ifc = ifcopenshell.open(filepath)

print(ifc.by_type("IfcWallType"))




# # retrieve all objects that are part of IfcBuildingElement
# building_elements = ifc.by_type("IfcBuildingElement")

# # # print class type for each object
# # for object in building_elements:
# #     print(object.is_a())

# # print number of objects that inherit from IfcColumn
# columns = ifc.by_type('IfcColumn')

# # # access specific element attributes
# # print(columns[0].GlobalId)
# # print(columns[0].Name)
# # print(columns[0].id()) # STEP ID

# # get Psets for a particular element
# psets = ifcopenshell.util.element.get_psets(columns[0])
# base_quantities = psets["BaseQuantities"]


# # # find inverse attributes
# # print(columns[0].IsDefinedBy)

# # # find elements that are reference by the current element
# # print(ifc.traverse(columns[0]))
# # print(ifc.traverse(columns[0], max_levels=1)) # Or, let's just go down one level deep

# # generate a new GUID for the current element
# columns[0].GlobalId = ifcopenshell.guid.new()


# # # save the changes above to a new ifc file:
# # ifc.write(filepath)