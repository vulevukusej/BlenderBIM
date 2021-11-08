import bpy


class MaterialSettings(bpy.types.PropertyGroup):
    my_int: bpy.props.IntProperty()
    my_float: bpy.props.FloatProperty()
    my_string: bpy.props.StringProperty()


bpy.utils.register_class(MaterialSettings)

bpy.types.Addon.my_settings = bpy.props.PointerProperty(type=MaterialSettings)

bpy.context.preferences.addons["blenderbim"].my_settings.my_int = 5
