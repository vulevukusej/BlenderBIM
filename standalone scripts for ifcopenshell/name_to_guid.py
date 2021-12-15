import ifcopenshell

filepath = "C:/Users/vpaji/OneDrive/Documents/Blender/Test Projects/17-Brita CT1_Taunusstein-V7_Optimized"
ifc = ifcopenshell.open(f"{filepath}.ifc")

elements = ifc.by_type("IfcElement")

for element in elements:
    element.Name = element.GlobalId
    
gltf = f"{filepath}_edited_for_gltf"
ifc.write(f"{gltf}.ifc")

print("finished")

vukas = ifc.create_entity("IFCPROPERTYSETTEMPLATE")
test = vukas.get_info


