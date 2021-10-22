import bpy
from blenderbim.bim.module.pset_template.prop import getPsetTemplates

class IFCPsetEditor(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "IFC Pset Editor"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        pass

class IFCParameterMapping(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Rename existing parameters"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "IFCPsetEditor"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        #object = context.object
        props = context.scene.properties_to_map

        layout.operator("ifc_mapping.add_property_to_be_mapped")
        row = layout.row(align=True)

        if props:
            row.label(text="Existing property name: (PsetName.Property)")
            row.label(text="New property name:")
            for index, property in enumerate(props):
                row = layout.row()
                row.operator("ifc_mapping.remove_property_to_be_mapped",icon="PANEL_CLOSE", text="").index = index
                row.prop(property, "property_name", text="")
                row.prop(property, "new_property_name", text="")
                #row.operator("bim.remove_csv_attribute", icon="X", text="").index = index        
            row = layout.row()
            row.operator("ifc_mapping.clear_list")
            row.operator("ifc_mapping.apply_mapping")

class IFCBulkPropertyAdd(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Add Psets to selected objects"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "IFCPsetEditor"
    bl_options = {"DEFAULT_CLOSED", "DRAW_BOX"}
    bl_order = 1

    def draw(self, context):
        props = context.scene.BIMPsetTemplateProperties
        layout = self.layout
        layout.prop(props, "pset_template_files", text="")
        layout.prop(props, "pset_templates", text="", icon="COPY_ID")
        
        row = self.layout.row(align=True)
        op = row.operator("ifc_mapping.add_pset_to_selected", icon="ADD")
        op.pset = self.getPsetName(context, props.pset_templates)
        
    def getPsetName(self, context, pset_id):
        pset_enum = [pset_tuple for pset_tuple in getPsetTemplates(self,context)]
        for pset in pset_enum:
            if pset[0] == pset_id:
                return pset[1]

        