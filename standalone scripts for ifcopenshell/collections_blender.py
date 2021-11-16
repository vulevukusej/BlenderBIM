import bpy
import ifcopenshell
import blenderbim.tool as tool
import ifcopenshell.util.element


pset = "Pset_Custom"
prop = "Bauteilkategorie"

if "Selection Sets" in bpy.data.collections:
    selection_sets = bpy.data.collections["Selection Sets"]  
else:
    selection_sets = bpy.data.collections.new("Selection Sets")
    selection_sets.color_tag = "COLOR_03"
   
   #ifctype 
if "Ifc Types" in bpy.data.collections:
    ifc_types = bpy.data.collections["Ifc Types"]
else:
    ifc_types = bpy.data.collections.new("Ifc Types")
    ifc_types.color_tag = "COLOR_03"
    selection_sets.children.link(ifc_types)
    
    #bauteilkategorie
if "Bauteilkategorie" in bpy.data.collections:
    bauteilkategorie = bpy.data.collections["Bauteilkategorie"]
else:
    bauteilkategorie = bpy.data.collections.new("Bauteilkategorie")
    bauteilkategorie.color_tag = "COLOR_03"
    selection_sets.children.link(bauteilkategorie)    

try:#Try to link the collection to the scene, do nothing if already linked
    bpy.context.scene.collection.children.link(selection_sets)
    bpy.context.scene.collection.children.link(selection_sets)
except:
    pass
    
objects = bpy.context.selectable_objects

for obj in objects:
    ifc_element = tool.Ifc.get_entity(obj)
    if obj.type != "MESH" or not ifc_element:
        continue
    
    ifc_type = ifc_element.is_a()
    psets = ifcopenshell.util.element.get_psets(ifc_element)
    
    #ifc_type
    if ifc_type in bpy.data.collections:
        ifc_type_collection = bpy.data.collections[ifc_type]
    else:
        ifc_type_collection = bpy.data.collections.new(f"{ifc_type}")
        ifc_type_collection.color_tag = "COLOR_03"
        ifc_types.children.link(ifc_type_collection)
    
    if obj.name not in bpy.data.collections[ifc_type].objects.keys():
        ifc_type_collection.objects.link(obj)        
        
        
    #custom
    if pset not in psets:
        continue
    if pset in psets:
        if prop in psets[pset]:
            propval = psets[pset][prop]
            
            if propval in bpy.data.collections:
                propval_collection = bpy.data.collections[propval]
            else:
                propval_collection = bpy.data.collections.new(f"{propval}")
                propval_collection.color_tag = "COLOR_03"
                bauteilkategorie.children.link(propval_collection)
        else:
            continue     
        
    if obj.name not in bpy.data.collections[propval].objects.keys():
        propval_collection.objects.link(obj)    
    
    
    
    


    

