import bpy
import os
from ifcopenshell.api import run
from blenderbim.bim.ifc import IfcStore
from blenderbim.bim.module.pset_template.prop import getPsetTemplates
from ifcopenshell.api.pset.data import Data
import ifcopenshell.api.root.data as ObjectData

class AddPropertyToBeMapped(bpy.types.Operator):
    bl_label = "Add Property to be mapped"
    bl_idname = "ifc_mapping.add_property_to_be_mapped"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.properties_to_map
        props.add()
        return {"FINISHED"}

class RemovePropertyToBeMapped(bpy.types.Operator):
    bl_label = "Remove Property to be mapped"
    bl_idname = "ifc_mapping.remove_property_to_be_mapped"
    bl_options = {"REGISTER", "UNDO"}
    index: bpy.props.IntProperty()

    def execute(self, context):
        props = context.scene.properties_to_map
        props.remove(self.index)
        return {"FINISHED"}

class ClearList(bpy.types.Operator):
    bl_label = "Clear list of properties"
    bl_idname = "ifc_mapping.clear_list"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.properties_to_map
        props.clear()
        return {"FINISHED"}

class ApplyMapping(bpy.types.Operator):
    bl_label = "Apply parameter mapping"
    bl_idname = "ifc_mapping.apply_mapping"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Rename paramters that are subclasses of IfcBuildingElement"

    def execute(self, context):
        return IfcStore.execute_ifc_operator(self, context)

    def _execute(self, context):
        properties_to_map = context.scene.properties_to_map
        ifc_file = IfcStore.get_file()
        allBuildingElements = ifc_file.by_type("IfcBuildingElement")

        self.apply_mapping(properties_to_map, allBuildingElements)

        self.report({'INFO'}, 'Finished applying changes')
        return {"FINISHED"}

    def apply_mapping(self, properties_to_map, allBuildingElements):
        
        for element in allBuildingElements:
            for definition in element.IsDefinedBy:
                #print(definition)
                if definition.is_a('IfcRelDefinesByProperties'):
                    property_set = definition.RelatingPropertyDefinition
                    try:
                        for prop in property_set.HasProperties:
                                for property in properties_to_map:

                                    if not "." in property.property_name:
                                        self.report({'ERROR'}, f'Property: {property.property_name} is missing Pset prefix')
                                        return

                                    if property.property_name.split(".")[0] != property_set.Name:
                                        #Property name correct, but wrong pset
                                        continue

                                    if property.property_name.split(".")[1] in prop.Name:
                                        prop.Name = property.new_property_name
                                        Data.load(IfcStore.get_file(), element.id())
                    except:
                        #property has no .HasProperties value
                        #TODO - find out what this means
                        pass
class BulkAddPsets(bpy.types.Operator):
    bl_label = "Add Pset to selected objects"
    bl_idname = "ifc_mapping.add_pset_to_selected"
    bl_options = {"REGISTER", "UNDO"}
    obj: bpy.props.StringProperty()
    obj_type: bpy.props.StringProperty()
    pset: bpy.props.StringProperty()
    

    def getApplicableEntities(self, context):
        templates = IfcStore.pset_template_file.by_type("IfcPropertySetTemplate")

        for template in templates:
            pset_name = template.Name

            if pset_name == self.pset:
                return template.ApplicableEntity.split(",")

    def execute(self, context):
        #print(getPsetTemplates(self,context))
        return IfcStore.execute_ifc_operator(self, context)
        
    def _execute(self, context):
        self.file = IfcStore.get_file()
        selected_objects = context.selected_objects
        applicable_entities = self.getApplicableEntities(context)

        for object in selected_objects:
            props = object.BIMObjectProperties
            try:
                data = ObjectData.Data.products[props.ifc_definition_id]
            except:
                print(f"IFC Element:{props.ifc_definition_id} not found")
                continue
            object_ifc_class = data["type"]            
            ifc_definition_id = object.BIMObjectProperties.ifc_definition_id

            #there must be a better way of doing this?
            if object_ifc_class in applicable_entities or "IfcObject" in applicable_entities:
                run(
                "pset.add_pset",
                self.file,
                **{
                    "product": self.file.by_id(ifc_definition_id),
                    "name": self.pset,
                }
                )
                Data.load(IfcStore.get_file(), ifc_definition_id)
            else:
                print(f"{self.pset} was not added to to object:{ifc_definition_id} since {object_ifc_class} is not an applicable entity for this Pset")

        self.report({'INFO'}, 'Finished applying changes')
        return {"FINISHED"}