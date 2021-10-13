bl_info = {
    "name": "tester",
    "description": "",
    "author": "",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "3D View > Toolbox",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Test"
}

import bpy
import re
import math
from mathutils import Vector
from math import pi

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


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

def my_settings_callback(scene, context):

    items = [
        ('LOC', "Location", ""),
        ('ROT', "Rotation", ""),
        ('SCL', "Scale", ""),
    ]

    ob = context.object
    if ob is not None:
        if ob.type == 'LIGHT':
            items.append(('NRG', "Energy", ""))
            items.append(('COL', "Color", ""))

    return items

class MySettings(PropertyGroup):

    # apply values to LOC ROT SCL
    transform : EnumProperty(
        name="Apply Data to:",
        description="Apply Data to attribute.",
        items=my_settings_callback
        )


# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_my_panel(Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_context = "objectmode" 

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "transform", text="")


# ------------------------------------------------------------------------
#   Registration
# ------------------------------------------------------------------------

classes = (
    MySettings,
    OBJECT_PT_my_panel
)

def register():
    
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)

def unregister():
    
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
        
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()