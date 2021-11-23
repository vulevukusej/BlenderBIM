import bpy

class IfcPropertyEditor(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "IFC Property Editor"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        pass

class RenameParameters(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Rename all building elements"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "IfcPropertyEditor"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 0
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.properties_to_map
  
        if props:          
            for index, property in enumerate(props):
                row = layout.row()
                row.prop(property, "pset_name", text="")
                row.prop(property, "existing_property_name", text="")
                row.prop(property, "new_property_name", text="")
                op = row.operator("ifc_mapping.remove_property_to_be_mapped",icon="PANEL_CLOSE", text="")
                op.index = index
                op.type = "properties_to_map"
                
        row = layout.row()
        row.label()
        op = row.operator("ifc_mapping.add_property_to_be_mapped", icon="ADD",text="")
        op.type = "properties_to_map"
        
        if props:  
            row = layout.row()
            clear = row.operator("ifc_mapping.clear_list")
            clear.type = "properties_to_map"
            row.operator("ifc_mapping.apply_mapping")


class AddPropertiesOrEditValues(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Add/Edit Custom Properties and Values (to selected objects)"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "IfcPropertyEditor"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        props = context.scene.properties_to_add_or_edit 
        
        if props:
            for index, property in enumerate(props):
                    row = layout.row()
                    row.prop(property, "pset_name", text="")
                    row.prop(property, "property_name", text="")
                    if property.value_type == "String":
                        row.prop(property, "string_value", text="")
                    elif property.value_type == "Boolean":
                        row.prop(property, "bool_value", text="")
                    elif property.value_type == "Integer":
                        row.prop(property, "int_value", text="")
                    elif property.value_type == "Number":
                        row.prop(property, "float_value", text="")
                    row.prop(property, "value_type", text="")
                    op = row.operator("ifc_mapping.remove_property_to_be_mapped",icon="PANEL_CLOSE", text="")
                    op.index = index
                    op.type = "properties_to_add_or_edit"
        
        row = layout.row()
        row.label()
        op = row.operator("ifc_mapping.add_property_to_be_mapped", icon="ADD",text="")
        op.type = "properties_to_add_or_edit"
        
        if props:
            row = layout.row()
            clear = row.operator("ifc_mapping.clear_list")
            clear.type = "properties_to_add_or_edit"
            op = row.operator("ifc_mapping.add_edit_custom_property",icon="ADD", text="Apply Changes")
            op.index = index
        

        