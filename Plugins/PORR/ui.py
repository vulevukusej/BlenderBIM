import bpy

class PORR_PT_tools(bpy.types.Panel):
    bl_label = "PORR"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        pass

class PORR_PT_generate_autoparameters(bpy.types.Panel):
    bl_label = "Generate autoparameters"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "PORR_PT_tools"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 0
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.PorrProperties
    
        row = layout.row()
        row.prop(props, "porr_json")
        row.operator("porr.select_porr_json", icon="FILE_FOLDER",text="")
        
        row = layout.row()
        row.operator("porr.generate_autoparameters",text="Generate autoparameters")


