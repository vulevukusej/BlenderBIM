import ifc_uuid
import json
from datetime import datetime

now = datetime.now()
timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")

#TODO Change these filepaths to relative file paths or integrate into Blender Plugin
ifc_filepath = "C:/Users/vpaji/AppData/Roaming/Blender Foundation/Blender/2.93/scripts/addons/blenderbim/bim/data/pset/porr.ifc"
json_filepath = "C:/Users/vpaji/OneDrive/1. Professional/9. Porr/PORR Parameter/complete_translation.json"

json_filepath

porr_json = open(json_filepath, encoding="utf-8")

#return JSON object
data = json.load(porr_json)

#initial row number for ifc file
row_index = 1
ifc_body = ""

#start looping through the Parameter Scheme
for category in data:
    kategorie = category["Name"]

    for element_type in category["Structures"]:
        element_typ = element_type["Name"]
        pset_name = "ePset_"+kategorie+"_"+element_typ
        pset_row_number = row_index
        pset_uuid = ifc_uuid.new()
        row_index += 1
        pset_row_references = ""
        ifc_pset_properties = ""

        for property in element_type["Properties"]:
            property_description = property["Name"]
            property_revitname = property["Revitname"]
            #property_name =property_description +" ("+property_revitname+(")")
            property_name =property_revitname

            property_type = property["Type"]
            property_row_number = row_index
            row_index += 1
            ifc_data_type = ""

            #TODO Check whether the assigned ifc_data_type actually makes sense
            if property_type in ("Text","Invalid","Material","Funktion"):
                ifc_data_type = "IfcLabel"
            elif property_type in ("MassDensity","Length","Number","Area","Angle"):
                ifc_data_type = "IfcReal"
            elif property_type == "YesNo":
                ifc_data_type = "IfcBoolean"
            elif property_type == "Integer":
                ifc_data_type = "IfcInteger"
            else:
                #Probably unnecessary, I added this just incase I missed some property types in the JSON file
                ifc_data_type = "IfcLabel"

            ifc_guid = ifc_uuid.new()
            #TODO #5 Check for duplicate properties so as not to bloat the ifc file
            ifc_pset_property = f"#{property_row_number}=IFCSIMPLEPROPERTYTEMPLATE('{ifc_guid}',$,'{property_name}','{property_description}',.P_SINGLEVALUE.,'{ifc_data_type}','',$,$,$,$,.READWRITE.);\n"
            ifc_pset_properties += ifc_pset_property
            pset_row_references += f"#{property_row_number},"


        ifc_pset = f"#{pset_row_number}=IFCPROPERTYSETTEMPLATE('{pset_uuid}',$,'{pset_name}','',.PSET_TYPEDRIVENOVERRIDE,'IfcObject',({pset_row_references}));\n" 
        ifc_body += ifc_pset
        ifc_body += ifc_pset_properties


# Closing file
porr_json.close()

ifc_header = f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION((),'2;1');
FILE_NAME('EPset_Porr.ifc','{timestamp}','BlenderBIM','PDE Integrale Planung','EPset_Porr','EPset_Porr',$);
FILE_SCHEMA(('IFC4'));
ENDSEC;
DATA;
"""

ifc_footer = """ 
ENDSEC;
END-ISO-10303-21;"""

#ugly code, but necessary(?) since ifc doesn't adopt UTF8 yet
#see: https://technical.buildingsmart.org/resources/ifcimplementationguidance/string-encoding/
ifc_body_formatted = ifc_body.replace("Ä","\\X2\\00C4\\X0\\")
ifc_body_formatted = ifc_body_formatted.replace("ä","\\X2\\00E4\\X0\\")
ifc_body_formatted = ifc_body_formatted.replace("Ü","\\X2\\00DC\\X0\\")
ifc_body_formatted = ifc_body_formatted.replace("ü","\\X2\\00FC\\X0\\")
ifc_body_formatted = ifc_body_formatted.replace("Ö","\\X2\\00D6\\X0\\")
ifc_body_formatted = ifc_body_formatted.replace("ö","\\X2\\00F6\\X0\\")
ifc_body_formatted = ifc_body_formatted.replace("ß","\\X2\\00DF\\X0\\")


f = open(ifc_filepath, "w")
f.write(ifc_header+ifc_body_formatted+ifc_footer)
f.close()

