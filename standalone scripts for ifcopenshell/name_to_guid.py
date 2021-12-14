import ifcopenshell

filepath = "C:/Users/vpaji/OneDrive/Documents/Blender/Test Projects/17-Brita CT1_Taunusstein-V7_Optimized.ifc"
ifc = ifcopenshell.open(filepath)

elements = ifc.by_type("IfcElement")

for element in elements:
    element.Name = element.GlobalId
    
gltf = "C:/Users/vpaji/OneDrive/Documents/Blender/Test Projects/17-Brita CT1_Taunusstein-V7_Optimized_gltf.ifc"
ifc.write(gltf)