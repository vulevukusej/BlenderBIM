def revit_types(type):
    if type == "OST_Walls":
        return "Wände"
    elif type == "OST_StructuralFraming":
        return "Skelletbau"
    elif type == "OST_GenericModel":
        return "Allgemeines Modell"
    elif type == "OST_Floors":
        return "Geschossdecken"
    elif type == "OST_StructuralFoundation":
        return "Fundamente"
    elif type == "OST_Roofs":
        return "Dächer"
    elif type == "OST_Columns":
        return "Stützen"
    elif type == "OST_StructuralColumns":
        return "Tragwerksstützen"
    elif type == "OST_Site":
        return "Grundstück"
    elif type == "OST_Windows":
        return "Fenster"
    elif type == "OST_Doors":
        return "Türen"
    elif type == "OST_StructConnections":
        return "Tragwerksverbindung"
    elif type == "OST_EdgeSlab":
        return "Plattenkante"