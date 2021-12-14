from os import name
import xml.etree.ElementTree as ET

porr_xml_file = "C:/Users/vpaji/OneDrive/1. Professional/9. Porr/PORR Parameter/LBH3.0.xml"
base = "{base}"

# create element tree object
tree = ET.parse(porr_xml_file)
# get root element
root = tree.getroot()

#FINDALL
#parameter_id = "28"
bauteil_id = "3169"
#test =root.findall(f".//*[@id='{parameter_id}']")
test =root.findall(f".//*[@bauteilid='{bauteil_id}']")


for id in test:
    print(id.attrib["name"])