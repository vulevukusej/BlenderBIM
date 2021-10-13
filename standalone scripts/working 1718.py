# context.area: PROPERTIES
# ------------------------------------------------------------------------
#  IMPORT MODULES
# ------------------------------------------------------------------------
import bpy
import os
import json
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


#clear the console
os.system('cls||clear')

# ------------------------------------------------------------------------
#    User Interface
#  -----------------------------------------------------------------------    
class PORR(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "PORR Mapping Tool"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.operator("read.jsondata")
        
        # Create two columns, by using a split layout.
        split = layout.split(factor=0.3)   
        col = split.column()
        col.label(text="")
        col.operator("generate.enum")
        
        
        # Second column, aligned
        col = split.column()
        #col.label(text="Column Two:")
        col.prop(scene, "PorrObjektKategorie")
        #context.region.tag_redraw()
        col.prop(scene, "PorrObjektTypen")
        
        #comment the below
        data = bpy.types.Scene.PorrJSONdata
        category_index = -1
        type_index = -1
        
        for index, element in enumerate(data):
             category = element["Name"]
             if category == bpy.context.scene.PorrObjektKategorie:
                category_index = index
                for index, element in enumerate(data[index]["Structures"]):
                    type = element["Name"]
                    if type == bpy.context.scene.PorrObjektTypen:
                        type_index = index
                        break
             
        
        for parameter in data[category_index]["Structures"][type_index]["Properties"]:
            revitname = parameter["Name"]
            layout.label(text=revitname)
        
# ------------------------------------------------------------------------
#    Operators
#  -----------------------------------------------------------------------  

#class to open a fileselect window
class ReadJSONdata(Operator):
    '''Opens file-selection window in order to copy filepath of JSON'''
    bl_idname = "read.jsondata"
    bl_label = "Parameter-Schema auswählen (JSON)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    #opens the json file and generates enums
    def load_json(self, filepath):
        #open Porr JSON file
        f = open(filepath)
        #return JSON object
        data = json.load(f)
        bpy.types.Scene.PorrJSONdata = data
        #create enumerator for dropdown
        list_of_categories = []
        index_of_category = []
        
        for index, element in enumerate(data):
            category = element["Name"]
            list_of_categories.append((category,category,category))
            
            if category == bpy.context.scene.PorrObjektKategorie:
                index_of_category = index
            
        #create scene enumerator
        bpy.types.Scene.PorrObjektKategorie = bpy.props.EnumProperty(items=list_of_categories,  name="")
        # Closing file
        f.close()
    

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        file = open(self.filepath, 'r')
        bpy.types.Scene.PorrJSONfilepath = self.filepath
        self.load_json(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    
    
class GenerateEnum(Operator):
    bl_idname = "generate.enum"
    bl_label = "Menu aktualisieren"   
    
    def execute(self, context):
        data = bpy.types.Scene.PorrJSONdata
        index_of_category = -1
        list_of_types = []
        
        #find index of chosen category
        for index, element in enumerate(data):
            category = element["Name"]
            if category == bpy.context.scene.PorrObjektKategorie:
                index_of_category = index
                bpy.types.Scene.index_of_category = index
        
        #create enum for element types
        for type in data[index_of_category]["Structures"]:
            element_type = type["Name"]
            list_of_types.append((element_type,element_type,element_type))
            
        #create scene enumerator
        bpy.types.Scene.PorrObjektTypen = bpy.props.EnumProperty(items=list_of_types,  name="")
            
        return {'FINISHED'}
    
    
    
def register():
    bpy.utils.register_class(PORR)
    bpy.utils.register_class(ReadJSONdata)
    bpy.utils.register_class(GenerateEnum)

def unregister():
    bpy.utils.unregister_class(PORR)
    bpy.utils.unregister_class(ReadJSONdata)
    bpy.utils.unregister_class(GenerateEnum)

if __name__ == "__main__":
    register()