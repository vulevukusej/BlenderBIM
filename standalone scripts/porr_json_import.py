import json

def load_json(self, filepath):
        #open Porr JSON file
        f = open(filepath)
        #return JSON object
        data = json.load(f)

        #create enumerator for dropdown
        list_of_categories = []
        index_of_category = []
        
        for index, element in enumerate(data):
            category = element["Name"]
            list_of_categories.append((category,category,category))
            
            #if category == bpy.context.scene.PorrObjektKategorie:
                #index_of_category = index

        #create scene enumerator
        bpy.types.Scene.PorrObjektKategorie = bpy.props.EnumProperty(items=list_of_categories,  name="")
        # Closing file
        f.close()