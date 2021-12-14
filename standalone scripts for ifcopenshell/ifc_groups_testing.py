import bpy
import ifcopenshell
from blenderbim.bim.ifc import IfcStore
import blenderbim.tool as tool
from ifcopenshell.api.group.data import Data
import cProfile
import pstats

# bpy.ops.bim.load_groups()
# bpy.ops.bim.add_group()
# bpy.context.scene.BIMGroupProperties.group_attributes[1].string_value = "Selection Set"
# bpy.ops.bim.edit_group()
# bpy.ops.bim.disable_group_editing_ui()

def test(): 
    objects = bpy.context.selectable_objects
    group_id = bpy.context.scene.BIMGroupProperties.groups["IfcWall"].ifc_definition_id
    file = IfcStore.get_file()

    for obj in objects:
        ifc_element = tool.Ifc.get_entity(obj)
        if  not ifc_element:
            continue
        
        ifc_type = ifc_element.is_a()
        if ifc_type == "IfcSlab":
            ifcopenshell.api.run(
                        "group.assign_group",
                        file,
                        **{
                            "product": file.by_id(obj.BIMObjectProperties.ifc_definition_id),
                            "group": file.by_id(group_id),
                        }
            )
    Data.load(file)

test()
with cProfile.Profile() as pr:
    test()
stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
#stats.print_stats()(
stats.dump_stats(filename="C:/Users/vpaji/OneDrive/Desktop/needs_profiling.prof")
print("vukas")