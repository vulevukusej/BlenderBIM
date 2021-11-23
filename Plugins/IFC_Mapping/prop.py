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


class PropertiesToMap(PropertyGroup):
    pset_name: StringProperty(name="Pset")
    existing_property_name: StringProperty(name="Existing Property Name")
    new_property_name: StringProperty(name="New Property Name")
    

class PropertiesToAddOrEdit(PropertyGroup):
    pset_name: StringProperty(name="Pset")
    property_name: StringProperty(name="Property")
    string_value: StringProperty(name="Value")
    bool_value: BoolProperty(name="Property Value")
    int_value: IntProperty(name="Property Value")
    float_value: FloatProperty(name="Property Value")
    value_type: EnumProperty(
        items=[
            ("String", "String", "" ),
            ("Boolean", "True/False", "" ),
            ("Integer", "Integer", "" ),
            ("Number", "Number", "" )],
        default="String"
    )
    
    
    
        