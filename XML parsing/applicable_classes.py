def applicable_classes(revit_type):
    if revit_type == "OST_Walls":
        return ["IfcCurtainWall", "IfcWall", "IfcWallElementedCase", "IfcWallStandardCase"]
    
    if revit_type == "OST_StructuralFraming":
        return ["IfcElementAssembly", "IfcBeam", "IfcBeamStandardCase", ]
    
    if revit_type == "OST_GenericModel":
        return ["IfcValve", "IfcBuildingElementProxy", "IfcBuildingElementPart", "IfcRailing", "IfcSanitaryTerminal", "IfcSpace", "IfcStair"]
    
    if revit_type == "OST_Floors":
        return ["IfcCovering", "IfcSlab", "IfcSlabElementedCase", "IfcSlabStandardCase"]
    
    if revit_type == "OST_StructuralFoundation":
        return ["IfcFooting", "IfcPile", "IfcDeepFoundation", "IfcCaissonFoundation"]
    
    if revit_type == "OST_Roofs":
        return ["IfcCovering", "IfcRoof", ]
    
    if revit_type == "OST_Columns":
        return ["IfcColumn", "IfcColumnStandardCase"]
    
    if revit_type == "OST_StructuralColumns":
        return ["IfcColumn", "IfcColumnStandardCase"]
    
    if revit_type == "OST_Site":
        return ["IfcEarthworksFill", "IfcReinforcedSoil", "IfcKerb", "IfcPavement"]
    
    if revit_type == "OST_Windows":
        return ["IfcWindow", "IfcWindowStandardCase", ]
    
    if revit_type == "OST_Doors":
        return ["IfcDoor", "IfcDoorStandardCase"]
    
    if revit_type == "OST_StructConnections":
        return ["IfcStructuralCurveConnection", "IfcStructuralPointConnection", "IfcStructuralSurfaceConnection"]
    
    if revit_type == "OST_EdgeSlab":
        return []