import ifc_uuid
import json
from datetime import datetime

now = datetime.now()
timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")

#I should change these filepaths to relative file paths or integrate into Blender Plugin
ifc_filepath = "C:/Users/vpaji/AppData/Roaming/Blender Foundation/Blender/3.0/scripts/addons/blenderbim/bim/data/pset/porr.ifc"
json_filepath = "C:/Users/vpaji/OneDrive/1. Professional/10. Programming/Python/XML parsing/porr_template.json"

porr_json = open(json_filepath, encoding="utf-8")

#return JSON object
template = json.load(porr_json)

#initial step_id for ifc file
step_id = 1
ifc_body = ""

#start looping through the template json file
for typ, typ_dict in template.items():
    pset_applicable_entity = ",".join(ifc_class for ifc_class in typ_dict["applicable_classes"])

    for bauteil, bauteil_dict in typ_dict["bauteile"].items():
        pset_name = f"porr_{typ}_{bauteil}" #Optional name
        pset_step_id = step_id
        step_id += 1
        pset_global_id = ifc_uuid.new()
        pset_has_property_templates = "" #Set of IfcPropertyTemplate's that are defined within the scope of the IfcPropertySetTemplate.
        pset_properties = "" #Stores the IFCSIMPLEPROPERTYTEMPLATE's

        for parameter, parameter_dict in bauteil_dict["parameters"].items():
            prop_name = parameter_dict["revit_name"]
            if prop_name == "ri:Ignore":
                continue
            prop_description = parameter.replace("'", "&apos")
            property_type = parameter_dict["parameter_type"]
            prop_step_id = step_id
            step_id += 1
            prop_global_id = ifc_uuid.new()
            prop_primary_measure_type = ""

            #TODO Check whether the assigned ifc_data_type actually makes sense
            if property_type in ("Text","Invalid","Material","Funktion"):
                prop_primary_measure_type = "IfcLabel"
            elif property_type in ("MassDensity","Length","Number","Area","Angle"):
                prop_primary_measure_type = "IfcReal"
            elif property_type == "YesNo":
                prop_primary_measure_type = "IfcBoolean"
            elif property_type == "Integer":
                prop_primary_measure_type = "IfcInteger"
            else:
                #just incase I missed some property types in the JSON file
                prop_primary_measure_type = "IfcLabel"

            #User is able to enter the property value freely:
            if not parameter_dict["value:matchkey"] or prop_primary_measure_type in  ["IfcReal", "IfcBoolean"] :
                ifc_simple_property_template = f"#{prop_step_id}=IFCSIMPLEPROPERTYTEMPLATE('{prop_global_id}',$,'{prop_name}','{prop_description}',.P_SINGLEVALUE.,'{prop_primary_measure_type}',$,$,$,$,$,.READWRITE.);\n"
                pset_properties += ifc_simple_property_template
                
            #User has to choose from a list, we need to create an enumeration:
            else:
                if property_type == "Integer":
                    enum_values = tuple((f"{prop_primary_measure_type}({int(value)})'delete'" for value in parameter_dict["value:matchkey"].keys()))
                    
                else:
                    enum_values = [value.replace('"','&quot') for value in parameter_dict["value:matchkey"].keys()] #TODO clean this up, im doing this because some values include " 
                    enum_values = tuple((f"{prop_primary_measure_type}('{value}')" for value in enum_values))
                enum_step_id = step_id
                step_id += 1
                ifc_property_enumeration = f"#{enum_step_id}=IFCPROPERTYENUMERATION('{prop_description}',{enum_values},$);\n".replace('"','')
                ifc_simple_property_template = f"#{prop_step_id}=IFCSIMPLEPROPERTYTEMPLATE('{prop_global_id}',$,'{prop_name}','{prop_description}',.P_ENUMERATEDVALUE.,'{prop_primary_measure_type}',$,#{enum_step_id},$,$,$,.READWRITE.);\n"
                
                pset_properties += ifc_simple_property_template
                pset_properties += ifc_property_enumeration
                
            
            pset_has_property_templates += f"#{prop_step_id},"


        ifc_property_set_template = f"#{pset_step_id}=IFCPROPERTYSETTEMPLATE('{pset_global_id}',$,'{pset_name}',$,.PSET_TYPEDRIVENOVERRIDE.,'{pset_applicable_entity}',({pset_has_property_templates}));\n" 
        ifc_body += ifc_property_set_template
        ifc_body += pset_properties
    
for i in 


ifc_header = f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION((),'2;1');
FILE_NAME('EPset_Porr.ifc','{timestamp}','BlenderBIM','PDE Integrale Planung','EPset_Porr','EPset_Porr',$);
FILE_SCHEMA(('IFC4'));
ENDSEC;
DATA;
"""

#ugly code, but necessary(?) since ifc doesn't adopt UTF8 yet
#see: https://technical.buildingsmart.org/resources/ifcimplementationguidance/string-encoding/
# ifc_body_formatted = ifc_body.replace("Ä","\\X2\\00C4\\X0\\")
# ifc_body_formatted = ifc_body_formatted.replace("ä","\\X2\\00E4\\X0\\")
# ifc_body_formatted = ifc_body_formatted.replace("Ü","\\X2\\00DC\\X0\\")
# ifc_body_formatted = ifc_body_formatted.replace("ü","\\X2\\00FC\\X0\\")
# ifc_body_formatted = ifc_body_formatted.replace("Ö","\\X2\\00D6\\X0\\")
# ifc_body_formatted = ifc_body_formatted.replace("ö","\\X2\\00F6\\X0\\")
# ifc_body_formatted = ifc_body_formatted.replace("ß","\\X2\\00DF\\X0\\")
ifc_body_formatted = ifc_body.replace("Ä","AE")
ifc_body_formatted = ifc_body_formatted.replace("ä","ae")
ifc_body_formatted = ifc_body_formatted.replace("Ü","UE")
ifc_body_formatted = ifc_body_formatted.replace("ü","ue")
ifc_body_formatted = ifc_body_formatted.replace("Ö","OE")
ifc_body_formatted = ifc_body_formatted.replace("ö","oe")
ifc_body_formatted = ifc_body_formatted.replace("ß","ss")
ifc_body_formatted = ifc_body_formatted.replace("'delete'","")
#ifc_body_formatted = ifc_body.encode("iso-8859-1")

ifc_footer = """ 
ENDSEC;
END-ISO-10303-21;"""

f = open(ifc_filepath, "w")
f.write(ifc_header+ifc_body_formatted+ifc_footer)
f.close()
print("finished")

# Closing file
porr_json.close()