import bpy
import ifcopenshell
import ifcopenshell.api
from ifcopenshell.api.pset.data import Data
from blenderbim.bim.ifc import IfcStore
import json

class PORR_OT_select_porr_json(bpy.types.Operator):
    bl_label = "Select file"
    bl_idname = "porr.select_porr_json"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty(default="*.json", options={"HIDDEN"})
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def execute(self, context):
        context.scene.PorrProperties.porr_json = self.filepath
        return {"FINISHED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

class PORR_OT_generate_autoparameters(bpy.types.Operator):
    bl_label = "Generate autoparameters"
    bl_idname = "porr.generate_autoparameters"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        json_filepath = context.scene.PorrProperties.porr_json    
        porr_json = json.load(open(json_filepath, encoding="utf-8"))
        file = IfcStore.get_file()
        IfcElements = file.by_type("IfcElement")
        
        for IfcElement in IfcElements:
            psets = ifcopenshell.util.element.get_psets(IfcElement)
            
            for pset in psets:        
                if "porr" not in pset:
                    continue
                matchkey_list = {}
                porr_type = pset.split("_")[1]
                porr_bauteil = pset.split("_")[2]
            
                porr_parameters = porr_json[porr_type]["bauteile"][porr_bauteil]["parameters"]
                autoparameters = porr_json[porr_type]["bauteile"][porr_bauteil]["autoparameters"]
                
                for key, val in porr_parameters.items():
                    setkey = val["setkey"]
                    if setkey == "False":
                        continue
                    revit_name = val["revit_name"]
                    prop_value = psets[pset].get(revit_name)
                    sort = val["sort"]
                    if revit_name == "ri:Ignore":
                        matchkey = list(val["value:matchkey"].values())[0]
                    else:
                        matchkey = val["value:matchkey"][prop_value]
                    matchkey_list[sort] = matchkey
            
                matchkey_order = sorted(matchkey_list) #this sorts the matchkey list according to setkey            
                cpiFitMatchKey_list = []

                for index in matchkey_order:
                    cpiFitMatchKey_list.append(matchkey_list[index])
                
                properties_to_add = {
                    "cpiFitMatchKey": "_".join(cpiFitMatchKey_list), 
                    **{k:v for k,v in autoparameters.items()}
                    }
                
                ifcopenshell.api.run("pset.edit_pset", file, pset=file.by_id(psets[pset]["id"]), properties=properties_to_add)
                Data.load(IfcStore.get_file(), IfcElement.id())
            
        return {"FINISHED"}

