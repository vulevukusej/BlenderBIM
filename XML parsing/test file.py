from os import name
import json
import xml.etree.ElementTree as ET


porr_xml_file = "C:/Users/vpaji/OneDrive/1. Professional/9. Porr/PORR Parameter/LBH3.0.xml"
base = "{base}"

# create element tree object
tree = ET.parse(porr_xml_file)
# get root element
root = tree.getroot()

bauteilarten = root.findall("./{base}bauteilarten/{base}bauteilart")
mylist = {}

#define level 1
for i in bauteilarten.copy():
    header = i.get("header")
    name = i.get("name")
    id = i.get("id")

    if not header:
        mylist[id] = {"name":name, "items":{}}
        bauteilarten.remove(i)

#define level 2
for i in bauteilarten.copy():
    header = i.get("header")
    name = i.get("name")
    id = i.get("id")

    level1_bta = root.findall(f"./{base}bauteilarten/{base}bauteilart[@id='{header}'][@header='']")
    if level1_bta != []:
        level1_bta_name = level1_bta[0].get("name")
        mylist[header]["items"][id] = {"name":name, "items":{}}
        bauteilarten.remove(i)

#define level 3
for i in bauteilarten.copy():
    header = i.get("header")
    name = i.get("name")
    id = i.get("id")

    level2_bta = root.findall(f"./{base}bauteilarten/{base}bauteilart[@id='{header}']")
    level2_bta_name = level2_bta[0].get("name")
    level2_bta_header = level2_bta[0].get("header")

    level1_bta = root.findall(f"./{base}bauteilarten/{base}bauteilart[@id='{level2_bta_header}']")
    level1_bta_name = level1_bta[0].get("name")
    level1_bta_id = level1_bta[0].get("id")

    mylist[level1_bta_id]["items"][header]["items"][id] = {"name":name, "bauteile":{}}


bauteile = root.findall("./{base}bauteile/{base}bauteil")
parameters = root.findall("./{base}parameters/{base}parameter")
values =root.findall("./{base}werte/{base}wert")

for bauteil in bauteile:
    name = bauteil.get("name")
    bauteil_id = bauteil.get("id")

    for key1, value1 in mylist.items():
        for key2, value2 in value1["items"].items():
            for key3, value3 in value2["items"].items():
                    if bauteil.get("header") == key3:
                        mylist[key1]["items"][key2]["items"][key3]["bauteile"][bauteil_id] = {"name":name, "parameters":{}}
    
                        for parameter in parameters:
                            name = parameter.get("name")
                            parameter_id = parameter.get("id")
                            parent = parameter.get("bauteilid")

                            if parent == bauteil_id:
                                mylist[key1]["items"][key2]["items"][key3]["bauteile"][bauteil_id]["parameters"][parameter_id] = {"name":name, "values":[]}
                            
                                for value in values:
                                    name = value.get("name")
                                    parent = value.get("parameterid")

                                    if parent == parameter_id:
                                        mylist[key1]["items"][key2]["items"][key3]["bauteile"][bauteil_id]["parameters"][parameter_id]["values"].append(name)


with open("porr.json", "w") as outfile:
    json.dump(mylist, outfile)
