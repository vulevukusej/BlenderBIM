import bpy
properties_to_map = bpy.context.scene.properties_to_map
for property in properties_to_map:
    if not "." in property.property_name:
        print("error")