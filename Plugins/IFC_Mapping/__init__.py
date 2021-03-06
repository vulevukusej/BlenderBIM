# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
from bpy.props import StringProperty
from . import ui, prop, operators

bl_info = {
    "name" : "IFC Bulk Property Editor",
    "author" : "Vukas Pajic",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

classes = (
    prop.PropertiesToMap,
    prop.PropertiesToAddOrEdit,
    ui.IfcPropertyEditor, 
    ui.RenameParameters,
    ui.AddPropertiesOrEditValues,
    operators.AddPropertyToBeMapped,
    operators.RemovePropertyToBeMapped,
    operators.ClearList,
    operators.ApplyMapping,
    operators.AddEditCustomProperty
    )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.properties_to_map = bpy.props.CollectionProperty(type=prop.PropertiesToMap)
    bpy.types.Scene.properties_to_add_or_edit = bpy.props.CollectionProperty(type=prop.PropertiesToAddOrEdit)


def unregister():
    del bpy.types.Scene.properties_to_map
    del bpy.types.Scene.properties_to_add_or_edit

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
   