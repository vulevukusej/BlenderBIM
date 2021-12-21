import ifcopenshell

ifc = ifcopenshell.file()

pset_template = ifc.create_entity(
    "IFCPROPERTYSETTEMPLATE",
    GlobalId=ifcopenshell.guid.new(), 
    Name="porr_OST_Walls_Metall-Zaeune", 
    Description="a porr pset", 
    TemplateType="PSET_TYPEDRIVENOVERRIDE",
    ApplicableEntity="IfcWallw,IfcWallStandardCase"
    )

prop_template = ifc.create_entity(
    "IFCSIMPLEPROPERTYTEMPLATE",
    GlobalId=ifcopenshell.guid.new(),
    Name="porr_Ganzzahl_E05",
    Description="Impraegnierung",
    TemplateType="P_ENUMERATEDVALUE",
    PrimaryMeasureType="IfcInteger",
)

prop_template2 = ifc.create_entity(
    "IFCSIMPLEPROPERTYTEMPLATE",
    GlobalId=ifcopenshell.guid.new(),
    Name="porr_Ganzzahl_E05",
    Description="Impraegnierung",
    TemplateType="P_ENUMERATEDVALUE",
    PrimaryMeasureType="IfcInteger",
)


if pset_template.HasPropertyTemplates:
    pset_template.HasPropertyTemplates = pset_template.HasPropertyTemplates+(prop_template,)
else:
    pset_template.HasPropertyTemplates = (prop_template,)



prop_enum = ifc.create_entity(
    "IFCPROPERTYENUMERATION",
    Name="Impraegnierung",
)

integer = ifc.create_entity("IfcInteger", 2)
label = ifc.create_entity("IfcLabel", "het ruimtenummer")
prop_enum.EnumerationValues = (integer,)


ifc.write('standalone scripts for ifcopenshell/news.ifc')
print("finished")