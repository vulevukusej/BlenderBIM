from os import name
from applicable_classes import applicable_classes
from revit_types import revit_types
import json
import xml.etree.ElementTree as ET


porr_xml_file = "C:/Users/vpaji/OneDrive/1. Professional/9. Porr/PORR Parameter/LBH3.0.xml"
base = "{base}"

# create element tree object
tree = ET.parse(porr_xml_file)
# get root element
root = tree.getroot()

templates = {}

typen = root.findall("./{base}typen/{base}typ")
for typ in typen:
    name = typ.get("name")
    typ_name = revit_types(name)
    templates[typ_name] = {
        "applicable_classes":applicable_classes(name),
        "bauteile":{}
        }
    typ_id = typ.get("id")
    bauteile = root.findall(f".//*[@type='{typ_id}']")
    
    for bauteil in bauteile:
        bauteil_name = bauteil.get("name")
        bauteil_id = bauteil.get("id")
        parameters = root.findall(f".//*[@bauteilid='{bauteil_id}']")
        templates[typ_name]["bauteile"][bauteil_name] = {
            "id": bauteil_id,
            "parameters":{},
            "autoparameters":{}
            }
        
        for parameter in parameters:
            parameter_name = parameter.get("name")
            parameter_id = parameter.get("id")
            revit_parameter_id = parameter.get("revitparameter")
            revit_parameter = root.findall(f".//*[@id='{revit_parameter_id}']")[0]
            revit_name = revit_parameter.get("name")
            
            templates[typ_name]["bauteile"][bauteil_name]["parameters"][parameter_name] = {
                "revit_name": revit_name,
                "parameter_type": revit_parameter.get("datentyp"),
                "setkey": parameter.get("setkey"),
                "sort": parameter.get("sort"), 
                "value:matchkey":{}
                }
            
            #get autoparameters
            werte = root.findall(f"./{base}werte/{base}wert[@parameterid='{parameter_id}']")
            if not werte:
                continue  
            for wert in werte:
                wert_id = wert.get("id")
                autoparameters = root.findall(f"./{base}autoparameters/{base}autoparameter[@name='{wert_id}']") 
                
                for ap in autoparameters:
                    ap_value = ap.get("value")
                    rp_id = ap.get("revitparameter")
                    rp = root.findall(f"./{base}revitparameters/{base}revitparameter[@id='{rp_id}']")
                    rp_name = rp[0].get("name")
                    if rp:
                        templates[typ_name]["bauteile"][bauteil_name]["autoparameters"][rp_name] = ap_value
                        
            values = root.findall(f".//*[@parameterid='{parameter_id}']")
            
            for value in values:
                if revit_parameter.get("datentyp") == "Integer":
                    #unfortunately the try/else below is necessary, because
                    # a) the values are stored as strings
                    # b) sometimes the values are not actually integers!
                    try:
                        value_name = int(value.get("name") if value.get("parameterwert") == "" else value.get("parameterwert"))
                    except:
                        value_name = 0
                
                else:
                    value_name = value.get("name") if value.get("parameterwert") == "" else value.get("parameterwert")
            
                value_bauteilname = value.get("bauteilname")
                value_id = value.get("id")
                matchkey = value.get("matchkey")               
                templates[typ_name]["bauteile"][bauteil_name]["parameters"][parameter_name]["value:matchkey"][value_name] = matchkey or value_bauteilname or value.get("name")
                
with open("porr_template.json", "w") as outfile:
    json.dump(templates, outfile)
print("finished")
