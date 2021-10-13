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


class PropertiesToBeMapped(PropertyGroup):
    property_name: StringProperty()
    new_property_name: StringProperty()


