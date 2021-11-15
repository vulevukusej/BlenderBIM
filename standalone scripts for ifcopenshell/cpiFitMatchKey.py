import bpy
import ifcopenshell
import ifcopenshell.api
from ifcopenshell.api.pset.data import Data
from blenderbim.bim.ifc import IfcStore
import json

filepath = "C:/Users/vpaji/OneDrive/Documents/Blender/Test Projects/itwo.ifc"
json_filepath = "C:/Users/vpaji/OneDrive/1. Professional/10. Programming/Python/XML parsing/porr_template.json"

#ifc = ifcopenshell.open(filepath)
ifc = IfcStore.get_file()
porr_json = json.load(open(json_filepath, encoding="utf-8"))


allBuildingElements = ifc.by_type("IfcBuildingElement")

for element in allBuildingElements:
    psets = ifcopenshell.util.element.get_psets(element)
    
    for pset in psets:
        if "porr" not in pset:
            continue
        matchkey_list = {}
        type = pset.split("_")[1]
        bauteil = pset.split("_")[2]
        
        json_parameters = porr_json[type]["bauteile"][bauteil]["parameters"]
        for parameter in json_parameters:
            setkey = json_parameters[parameter]["setkey"]
            if setkey == "False":
                continue
            revit_name = json_parameters[parameter]["revit_name"]
            sort = json_parameters[parameter]["sort"]
            
            if revit_name == "ri:Ignore":
                matchkey = json_parameters[parameter]["values"]["matchkeyonly"]
            else:
                obj_value = psets[pset][revit_name]
                matchkey = json_parameters[parameter]["values"][obj_value]["matchkey"]
                
            matchkey_list[sort] = matchkey
            
            matchkey_order = sorted(matchkey_list)            
            cpiFitMatchKey_list = []

            for key in matchkey_order:
                cpiFitMatchKey_list.append(matchkey_list[key]["matchkey"])
        
        
        ifcopenshell.api.run("pset.edit_pset", ifc, pset=ifc.by_id(psets[pset]["id"]), properties={"cpiFitMatchKey": "_".join(cpiFitMatchKey_list)})
        Data.load(IfcStore.get_file(), element.id())

