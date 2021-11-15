import bpy
import ifcopenshell
import blenderbim.tool as tool
import ifcopenshell.util.element


if "Selection Sets" in bpy.data.collections:
    selection_sets = bpy.data.collections["Selection Sets"]  
else:
    selection_sets = bpy.data.collections.new("Selection Sets")
    selection_sets.color_tag = "COLOR_03"
    
if "Ifc Types" in bpy.data.collections:
    ifc_types = bpy.data.collections["Ifc Types"]
else:
    ifc_types = bpy.data.collections.new("Ifc Types")
    ifc_types.color_tag = "COLOR_03"
    selection_sets.children.link(ifc_types)

try:#Try to link the collection to the scene, do nothing if already linked
    bpy.context.scene.collection.children.link(selection_sets)
except:
    pass
    
objects = bpy.context.selectable_objects

for obj in objects:
    ifc_element = tool.Ifc.get_entity(obj)
    if obj.type != "MESH" or not ifc_element:
        continue
    
    ifc_type = ifc_element.is_a()
    if ifc_type in bpy.data.collections:
        ifc_type_collection = bpy.data.collections[ifc_type]
    else:
        ifc_type_collection = bpy.data.collections.new(f"{ifc_type}")
        ifc_type_collection.color_tag = "COLOR_03"
        ifc_types.children.link(ifc_type_collection)
    
    if obj.name in bpy.data.collections[ifc_type].objects.keys():
        continue    
    bpy.data.collections[ifc_type].objects.link(obj)
    


    

