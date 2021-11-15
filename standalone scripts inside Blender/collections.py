import bpy

selection_sets = bpy.data.collections.new("Selection Sets")
sub_collection1 = bpy.data.collections.new("sub_collection1")
sub_collection2 = bpy.data.collections.new("sub_collection2")


bpy.data.collections["Selection Sets"].children.link(sub_collection1)
bpy.data.collections["Selection Sets"].children.link(sub_collection2)

bpy.context.scene.collection.children.link(selection_sets)