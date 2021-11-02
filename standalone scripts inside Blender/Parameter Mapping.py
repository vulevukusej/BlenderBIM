import bpy
import ifcopenshell
import ifcopenshell.util
from ifcopenshell.api import run
from blenderbim.bim.ifc import IfcStore
from ifcopenshell.api.pset.data import Data


ifc_file = IfcStore.get_file()

mapping_table ={
    "Ausführung":"Ausführung_New"
    }

allBuildingElements = ifc_file.by_type("IfcBuildingElement")
for element in allBuildingElements:
    
    for definition in element.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByProperties'):
            property_set = definition.RelatingPropertyDefinition
            try:
                for property in property_set.HasProperties:
                        if property.Name in mapping_table:
                            property.Name = mapping_table[property.Name]
                            
                            Data.load(IfcStore.get_file(), element.id())
            except:
                #property has no .HasProperties value
                #TODO - find out what this means, aka - when would a property not have this?
                pass

print("FINISHED")            
