import bpy
from bpy.types import VIEW3D_PT_tools_grease_pencil_brush_stabilizer
import ifcopenshell
from ifcopenshell.api import run
from blenderbim.bim.ifc import IfcStore
from blenderbim.bim.module.pset_template.prop import getPsetTemplates
from ifcopenshell.api.pset.data import Data
import ifcopenshell.api.root.data as ObjectData
import blenderbim.tool as tool
import blenderbim.bim.schema

class AddPropertyToBeMapped(bpy.types.Operator):
    bl_label = "Add new row"
    bl_idname = "ifc_mapping.add_property_to_be_mapped"
    bl_options = {"REGISTER", "UNDO"}
    type: bpy.props.StringProperty()

    def execute(self, context):
        if self.type == "properties_to_map":
            props = context.scene.properties_to_map
            props.add()
        elif self.type == "properties_to_add_or_edit":
            props = context.scene.properties_to_add_or_edit
            props.add()         
        return {"FINISHED"}

class RemovePropertyToBeMapped(bpy.types.Operator):
    bl_label = "Remove property to be mapped"
    bl_idname = "ifc_mapping.remove_property_to_be_mapped"
    bl_options = {"REGISTER", "UNDO"}
    index: bpy.props.IntProperty()
    type: bpy.props.StringProperty()

    def execute(self, context):
        if self.type == "properties_to_map":
            props = context.scene.properties_to_map
            props.remove(self.index)
        if self.type == "properties_to_add_or_edit":
            props = context.scene.properties_to_add_or_edit
            props.remove(self.index)
        return {"FINISHED"}

class ClearList(bpy.types.Operator):
    bl_label = "Clear list of properties"
    bl_idname = "ifc_mapping.clear_list"
    bl_options = {"REGISTER", "UNDO"}
    type: bpy.props.StringProperty()
    
    def execute(self, context):
        if self.type == "properties_to_map":
            props = context.scene.properties_to_map
            props.clear()
        if self.type == "properties_to_add_or_edit":
            props = context.scene.properties_to_add_or_edit
            props.clear()
        return {"FINISHED"}

class ApplyMapping(bpy.types.Operator):
    bl_label = "Apply mapping"
    bl_idname = "ifc_mapping.apply_mapping"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Rename parameters that are subclasses of IfcBuildingElement"

    def execute(self, context):
        return IfcStore.execute_ifc_operator(self, context)

    def _execute(self, context):
        props_to_map = context.scene.properties_to_map
        ifc_file = IfcStore.get_file()
        all_building_elements = ifc_file.by_type("IfcBuildingElement")

        for element in all_building_elements:
            for definition in element.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    prop_set = definition.RelatingPropertyDefinition

                    if hasattr(prop_set, "HasProperties"):
                        self.rename_property(prop_set, props_to_map, element)
                    elif hasattr(prop_set, "Quantities"):
                        self.rename_property(prop_set, props_to_map, element)

        self.report({'INFO'}, 'Finished applying changes')
        return {"FINISHED"}
                                    
    def rename_property(self, property_set, properties_to_map, element):
        for obj_prop in property_set.HasProperties:
            for prop2map in properties_to_map:
                if not prop2map.pset_name:
                    self.report({'ERROR'}, f'Missing PSET!')
                    return
                if prop2map.pset_name != property_set.Name:
                    #wrong pset
                    continue
                if prop2map.existing_property_name in obj_prop.Name:
                    obj_prop.Name = prop2map.new_property_name
                    Data.load(IfcStore.get_file(), element.id())


class AddEditCustomProperty(bpy.types.Operator):
    bl_label = "Add or edit a custom property"
    bl_idname = "ifc_mapping.add_edit_custom_property"
    bl_options = {"REGISTER", "UNDO"}
    index: bpy.props.IntProperty()

    def execute(self, context):
        return IfcStore.execute_ifc_operator(self, context)

    def _execute(self, context):
        self.file = IfcStore.get_file()
        selected_objects = context.selected_objects
        props = context.scene.PropertiesToAddOrEdit     

        for object in selected_objects:
            ifc_definition_id = object.BIMObjectProperties.ifc_definition_id
            if not ifc_definition_id:
                continue
            ifc_element = tool.Ifc.get().by_id(ifc_definition_id)
            psets = ifcopenshell.util.element.get_psets(ifc_element)
            for prop in props:
                if prop.value_type == "String":
                    value = prop.string_value
                elif prop.value_type == "Boolean":
                    value = prop.bool_value
                elif prop.value_type == "Integer":
                    value = prop.int_value
                elif prop.value_type == "Number":
                    value = prop.float_value
                    
                if prop.pset_name not in psets:
                    new_pset = ifcopenshell.api.run("pset.add_pset", self.file, product=ifc_element, name=prop.pset_name)
                    ifcopenshell.api.run("pset.edit_pset", self.file, pset=new_pset, properties={prop.property_name:value})
                    
                else:#1) delete the existing property first, in case the value type has also been changed, and then
                    #2) re-add the property
                    self.delete_ifc_property(ifc_element, prop)
                    ifcopenshell.api.run("pset.edit_pset", self.file, pset=self.file.by_id(psets[prop.pset_name]["id"]), properties={prop.property_name:value})
        
        self.report({'INFO'}, 'Finished applying changes')
        return {"FINISHED"}

    def delete_ifc_property(self, element, property):
        for definition in element.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                prop_set = definition.RelatingPropertyDefinition
                if prop_set.Name != property.pset_name:
                    continue
                for hasprop in prop_set.HasProperties:
                    if hasprop.Name != property.property_name:
                        continue
                    self.file.remove(hasprop)
                    Data.load(IfcStore.get_file(), element.id())
                    return
                    
