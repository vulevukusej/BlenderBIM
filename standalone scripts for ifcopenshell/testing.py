import ifcopenshell
from ifcopenshell.api import run
from helper_functions import attributeExtractor

filepath = "C:/Users/vpaji/AppData\Roaming/Blender Foundation/Blender/2.93/scripts/addons/blenderbim/bim/data/pset/Sample_Template.ifc"
ifc_file = ifcopenshell.open(filepath)


templates = ifc_file.by_type("IfcPropertySetTemplate")
for template in templates:
    applicable_entity = template.ApplicableEntity
    print(applicable_entity.split(","))

    vukas = "Vukas"
    print(vukas.split(","))
    #print(template.get_info)
    

"""for object in element:
    print(type(object.GlobalId))
    if object.GlobalId == "3bh96Fdg5ETg4ZzROUxK0m":
        print ("found it")"""

#print(element.__dict__.keys())
"""for element in ifcWall:
    pset = run("pset.add_pset", ifc_file, product=element, name="Your Property Set Name")
    ifcopenshell.api.run("pset.edit_pset", ifc_file, pset=pset, properties={"foo": False, "foo2": ""})

for definition in element.IsDefinedBy:
    # To support IFC2X3, we need to filter our results.
    if definition.is_a('IfcRelDefinesByProperties'):
        property_set = definition.RelatingPropertyDefinition
        print(property_set.Name)
        try:
            for property in property_set.HasProperties:
                if property_set.HasProperties:
                    #attributeExtractor(property)

                    print("---"+str(property.Name)+"="+str(property.NominalValue))
                pass
        except:
            pass"""

#ifc_file.write(filepath)
