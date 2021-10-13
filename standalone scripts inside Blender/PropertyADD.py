import ifcopenshell
from blenderbim.bim.ifc import IfcStore
from ifcopenshell.api import run
from ifcopenshell.api.pset.data import Data
import json



json_filepath = "C:/Users/vpaji/OneDrive/8. Porr/5. BlenderBIM/ParameterMapping/PORR Parameter/complete_translation.json"

def generatePropertyDict(json_filepath):
    """[generates a property dictionary from json_file]
    Args:
        json_file ([.json]): [A .json file containing a property schema]
    Returns:
        [Dictionary]: [Dictionary of property values: "propertyname":"propertyvalue"]
    """
    parameter_schema = open(json_filepath, encoding="utf-8")
    data = json.load(parameter_schema)
    
    psets = {} #empty dictionary where we will store all of our psets
    properties = []
    property_dict = {}
    for type in data:
        for structure in type["Structures"]:
            for property in structure["Properties"]:
                propertyname = property["Revitname"] #example: Tragendes Bauteil
                propertytype = property["Type"] #example: Text
                
                if propertytype in ("Text","Invalid","Material","Funktion"):
                    defaultvalue = ""
                elif propertytype in ("MassDensity","Length","Number","Area","Angle"):
                    defaultvalue = 0.0
                elif propertytype == "YesNo":
                    defaultvalue = False
                elif propertytype == "Integer":
                    defaultvalue = 0
                else:
                    continue
                
                property_dict[propertyname] = defaultvalue
    return property_dict

def bulkPropertyAdd(json_filepath):
    """[adds all the unique properties in the .json file to every object in the .ifc file]

    Args:
        json_filepath ([type]): [description]
        ifc_filepath ([type]): [description]
    """
    ifc_file = IfcStore.get_file()
    data = generatePropertyDict(json_filepath)
    allBuildingElements = ifc_file.by_type("IfcBuildingElement")
    psetname = "ePset_PORR"
    
    for element in allBuildingElements:
        pset = run("pset.add_pset", ifc_file, product=element, name=psetname)
        run("pset.edit_pset", ifc_file, pset=pset, properties=data)
        
        Data.load(IfcStore.get_file(), element.id())

    #ifc_file.write(ifc_filepath)
    print("FINISHED")
     
bulkPropertyAdd(json_filepath)



if __name__ == "__main__":
    pass