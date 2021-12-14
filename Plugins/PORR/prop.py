from os import name
import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    PointerProperty,
    StringProperty,
    EnumProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    CollectionProperty,
)

class PORR_Properties(PropertyGroup):
    porr_json: StringProperty(name="PORR JSON File")
    
        