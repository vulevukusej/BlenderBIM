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

allElements = ifc.by_type("IfcElement")

for element in allElements:
    psets = ifcopenshell.util.element.get_psets(element)
    
    for pset in psets:        
        if "porr" not in pset:
            continue
        matchkey_list = {}
        type = pset.split("_")[1]
        bauteil = pset.split("_")[2]
        
        porr_parameters = porr_json[type]["bauteile"][bauteil]["parameters"]
        autoparameters = porr_json[type]["bauteile"][bauteil]["autoparameters"]
   
        for key, val in porr_parameters.items():
            setkey = val["setkey"]
            if setkey == "False":
                continue
            revit_name = val["revit_name"]
            prop_value = psets[pset].get(revit_name)
            sort = val["sort"]
            if revit_name == "ri:Ignore":
                matchkey = list(val["value:matchkey"].values())[0]
            else:
                matchkey = val["value:matchkey"][prop_value]
            matchkey_list[sort] = matchkey
            
        matchkey_order = sorted(matchkey_list)            
        cpiFitMatchKey_list = []

        for index in matchkey_order:
            cpiFitMatchKey_list.append(matchkey_list[index])
        
        properties_to_add = {
            "cpiFitMatchKey": "_".join(cpiFitMatchKey_list), 
            **{k:v for k,v in autoparameters.items()}
            }
        
        ifcopenshell.api.run("pset.edit_pset", ifc, pset=ifc.by_id(psets[pset]["id"]), properties=properties_to_add)
        Data.load(IfcStore.get_file(), element.id())

print("finished")
