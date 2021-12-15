import ifc_uuid
import json
from datetime import datetime
from applicable_classes import applicable_classes
from class_templates import (
    IfcRoot,
    IfcPropertySetTemplate, 
    IfcSimplePropertyTemplate, 
    IfcPropertyEnumeration
)

now = datetime.now()
timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")

#mapping dictionary to convert revit data types to ifc data types
revit_ifc_type_mapping = {
    **dict.fromkeys(["Text","Invalid","Material","Funktion"], "IfcLabel"),
    **dict.fromkeys(["MassDensity","Length","LENGTH","Number","Area","Angle"], "IfcReal"),
    "YesNo":"IfcBoolean",
    "Integer":"IfcInteger"
}

#mapping dictionary to convert revit data types to python data types
revit_py_type_mapping = {
    **dict.fromkeys(["Text","Invalid","Material","Funktion"], str), 
    **dict.fromkeys(["MassDensity","Length","LENGTH","Number","Area","Angle"], float),
    "YesNo":bool,
    "Integer":int
}

#I should change these filepaths to relative file paths or integrate into Blender Plugin
ifc_filepath = "C:/Users/vpaji/AppData/Roaming/Blender Foundation/Blender/3.0/scripts/addons/blenderbim/bim/data/pset/porr.ifc"
json_filepath = "C:/Users/vpaji/OneDrive/1. Professional/9. Porr/PORR Parameter/parameters_template.json "

porr_json = open(json_filepath, encoding="utf-8")

#return JSON object
template = json.load(porr_json)
x = 2
#initial step_id for ifc file
step_id = 1
ifc_body = dict()

#start looping through the template json file
for typ in template:
    typ_name = typ["name"]
    applicable_entities = applicable_classes(typ_name)
    
    #loop through all bauteile
    for bauteil in typ["Elements"]:
        bauteil_name = bauteil["name"]
        pset_name = f"porr_{typ_name}_{bauteil_name}" 
        
        #instantatiate an IfcPropertySetTemplate class
        pset_template = ifc_body[step_id] = IfcPropertySetTemplate(pset_name, "", ".PSET_TYPEDRIVENOVERRIDE.")
        pset_template.add_applicable_entity(applicable_entities)    
        pset_template.assign_step_id(step_id)
        step_id += 1
        
        #loop through all parameters
        for parameter in bauteil["parameters"]:
            prop_name = parameter["revitname"]
            if prop_name == "ri:Ignore":
                continue
            prop_description = parameter["name"]
            if len(parameter["values"]) < 2:
                template_type = ".P_SINGLEVALUE."
            else:
                template_type = ".P_ENUMERATEDVALUE."
                
            revit_parameter_type = parameter["parametertype"]
            primary_measure_type = revit_ifc_type_mapping[revit_parameter_type]
            
            #instantatiate an IfcSimplePropertyTemplate class
            prop_template = ifc_body[step_id] = IfcSimplePropertyTemplate(prop_name, prop_description, template_type, primary_measure_type)
            prop_template.assign_step_id(step_id)
            step_id += 1
            pset_template.add_property_template(prop_template.step_id)
            
            if template_type == ".P_ENUMERATEDVALUE.":
                py_type = revit_py_type_mapping[revit_parameter_type]
                enum_values = {f"{primary_measure_type}({py_type(v['value'])})" for v in parameter["values"]} 
                
                #instantatiate an IfcPropertyEnumeration class
                prop_enum = ifc_body[step_id] = IfcPropertyEnumeration(prop_name)
                prop_enum.add_enumeration_values(enum_values)
                prop_enum.assign_step_id(step_id)
                step_id += 1
                prop_template.assign_enumerator(prop_enum.step_id)
                
    
ifc_header = f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION('PORR Property Set Template','2;1');
FILE_NAME('EPset_Porr.ifc','{timestamp}','Vukas Pajic, vukas.pajic@pde-porr.com','PDE Integrale Planung','','','PDE Integrale Planung');
FILE_SCHEMA(('IFC4'));
ENDSEC;
DATA;
"""

ifc_body_string = ""
for i in ifc_body.values():
    ifc_body_string += i.get_step_object()


#ugly code, but necessary(?) since ifc doesn't adopt UTF8 yet
#see: https://technical.buildingsmart.org/resources/ifcimplementationguidance/string-encoding/
ifc_body_string = ifc_body_string.replace("Ä","\\X2\\00C4\\X0\\")
ifc_body_string = ifc_body_string.replace("ä","\\X2\\00E4\\X0\\")
ifc_body_string = ifc_body_string.replace("Ü","\\X2\\00DC\\X0\\")
ifc_body_string = ifc_body_string.replace("ü","\\X2\\00FC\\X0\\")
ifc_body_string = ifc_body_string.replace("Ö","\\X2\\00D6\\X0\\")
ifc_body_string = ifc_body_string.replace("ö","\\X2\\00F6\\X0\\")
ifc_body_string = ifc_body_string.replace("ß","\\X2\\00DF\\X0\\")

# ifc_body_formatted = ifc_body.replace("Ä","AE")
# ifc_body_formatted = ifc_body_formatted.replace("ä","ae")
# ifc_body_formatted = ifc_body_formatted.replace("Ü","UE")
# ifc_body_formatted = ifc_body_formatted.replace("ü","ue")
# ifc_body_formatted = ifc_body_formatted.replace("Ö","OE")
# ifc_body_formatted = ifc_body_formatted.replace("ö","oe")
# ifc_body_formatted = ifc_body_formatted.replace("ß","ss")
# ifc_body_formatted = ifc_body_formatted.replace("'delete'","")
#ifc_body_formatted = ifc_body.encode("iso-8859-1")

ifc_footer = """ 
ENDSEC;
END-ISO-10303-21;"""

f = open(ifc_filepath, "w")
f.write(ifc_header+ifc_body_string+ifc_footer)
f.close()
print("finished")

# Closing file
porr_json.close()