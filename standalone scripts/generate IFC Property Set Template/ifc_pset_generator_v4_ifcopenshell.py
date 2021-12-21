import ifcopenshell
import json
from applicable_classes import applicable_classes
from api_request import get_blender_content

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
#json_filepath = "C:/Users/vpaji/OneDrive/1. Professional/9. Porr/PORR Parameter/parameters_template.json "
porr_json = get_blender_content()

#porr_json = open(json_filepath, encoding="utf-8")

#return JSON object
template = json.loads(porr_json)

#create an empty ifc file
ifc = ifcopenshell.file()

#start looping through the template json file
for typ in template:
    typ_name = typ["name"]
    applicable_entities = applicable_classes(typ_name)
    
    #loop through all bauteile
    for bauteil in typ["Elements"]:
        bauteil_name = bauteil["name"]
        pset_name = f"porr_{typ_name}_{bauteil_name}" 
        
        #create an IfcPropertySetTemplate instance
        pset_template = ifc.create_entity(
            "IFCPROPERTYSETTEMPLATE",
            GlobalId=ifcopenshell.guid.new(), 
            Name=pset_name, 
            TemplateType="PSET_TYPEDRIVENOVERRIDE",
            ApplicableEntity=",".join(applicable_entities)
        )
        
        #loop through all parameters
        for parameter in bauteil["parameters"]:
            prop_name = parameter["revitname"]
            revit_parameter_type = parameter["parametertype"]
            #prop_description = parameter["name"].replace("'", "&apos")
            prop_description = parameter["name"]
            if "ri:" in prop_name:
                continue
            if len(parameter["values"]) < 1 or revit_parameter_type == "YesNo":
                template_type = "P_SINGLEVALUE"
            else:
                template_type = "P_ENUMERATEDVALUE"
                
            revit_parameter_type = parameter["parametertype"]
            primary_measure_type = revit_ifc_type_mapping[revit_parameter_type]
            
            #create an IfcSimplePropertyTemplate instance
            prop_template = ifc.create_entity(
                "IFCSIMPLEPROPERTYTEMPLATE",
                GlobalId=ifcopenshell.guid.new(),
                Name=prop_name,
                Description=prop_description,
                TemplateType=template_type,
                PrimaryMeasureType=primary_measure_type,
            )
            
            #assign the property template to the pset template
            if pset_template.HasPropertyTemplates:
                pset_template.HasPropertyTemplates = pset_template.HasPropertyTemplates+(prop_template,)
            else:
                pset_template.HasPropertyTemplates = (prop_template,)
                
                
            if template_type == "P_ENUMERATEDVALUE":
                py_type = revit_py_type_mapping[revit_parameter_type]
                
                prop_enum = ifc.create_entity(
                    "IFCPROPERTYENUMERATION",
                    Name=f"{prop_description}_enum",
                    #EnumerationValues=tuple(ifc.create_entity(primary_measure_type, py_type(v['value'].replace('"','&quot;'))) for v in parameter["values"])
                    EnumerationValues=tuple(ifc.create_entity(primary_measure_type, py_type(v['value'])) for v in parameter["values"])
                )
                
                #assign the enumeration to the property template
                prop_template.Enumerators = prop_enum
 
# Closing json file
# porr_json.close()

#write ifc file
ifc.write(ifc_filepath)
print("Finished")
