import ifc_uuid

class IfcRoot:
    def __init__(self, name, description):
        self.global_id = ifc_uuid.new()
        self.owner_history = '$'
        self.name = name
        self.description = description


class IfcPropertySetTemplate(IfcRoot):
    def __init__(self, name, description, template_type):
        super().__init__(name, description)
        self.template_type = template_type
        self.applicable_entity = set()
        self.has_property_templates = set()
        
    def assign_step_id(self, step_id):
        self.step_id = step_id
        
    def add_property_template(self, property_template):
        self.has_property_templates.add(f"#{property_template}")
    
    def add_applicable_entity(self, applicable_entities):
        self.applicable_entity.update(applicable_entities)
        
    def get_step_object(self):
        assert self.has_property_templates, 'The property set should have defined property templates!'
        return f"#{self.step_id}= IFCPROPERTYSETTEMPLATE('{self.global_id}',{self.owner_history},'{self.name}','{self.description}',{self.template_type},'{self.set_to_string(self.applicable_entity)}',({self.set_to_string(self.has_property_templates)}));\n"

    def set_to_string(self, set):
        list_of_strings = [str(s) for s in set]
        joined_string = ",".join(list_of_strings)    
        return joined_string
    

class IfcSimplePropertyTemplate(IfcRoot):
    def __init__(self, name, description, template_type, primary_measure_type):
        super().__init__(name, description)
        self.template_type = template_type
        self.primary_measure_type = primary_measure_type
        self.secondary_measure_type = '$'
        self.enumerators = '$'
        self.primary_unit = '$'
        self.secondary_unit = '$'
        self.expression = '$'
        self.access_state = ".READWRITE."
        
    def assign_step_id(self, step_id):
        self.step_id = step_id
        
    def assign_enumerator(self, enumerator):
        self.enumerators = f"#{enumerator}"
        
    def get_step_object(self):
        if self.template_type == ".P_ENUMERATEDVALUE.":
            assert self.enumerators , f'The #{self.step_id} property template should have an assigned enumerator!'
        return f"#{self.step_id}= IFCSIMPLEPROPERTYTEMPLATE('{self.global_id}',{self.owner_history},'{self.name}','{self.description}',{self.template_type},'{self.primary_measure_type}',{self.secondary_measure_type},{self.enumerators},{self.primary_unit},{self.secondary_unit},{self.expression},{self.access_state});\n"

    def set_to_string(self, set):
        list_of_strings = [str(s) for s in set]
        joined_string = ",".join(list_of_strings)    
        return joined_string


class IfcPropertyEnumeration:
    def __init__(self, name, unit='$'):
        self.name = name
        self.unit = unit
        self.enumeration_values = set()
        
    def assign_step_id(self, step_id):
        self.step_id = step_id
        
    def add_enumeration_values(self, enumeration_values):
        self.enumeration_values.update(enumeration_values)
        
    def set_to_string(self, set):
        list_of_strings = [str(s) for s in set]
        joined_string = ",".join(list_of_strings)    
        return joined_string
        
    def get_step_object(self):
        assert self.enumeration_values, 'The enumeration should have defined enumeration values!'
        return f"#{self.step_id}= IFCPROPERTYENUMERATION('{self.name}',({self.set_to_string(self.enumeration_values)}),{self.unit});\n" 


#the following are just some tests to check the classes work.  Should probably make these proper tests
custom_pset = IfcPropertySetTemplate("custom_pset","an example custom pset", ".PSET_TYPEDRIVENOVERRIDE.")
custom_pset.assign_step_id(1)
custom_pset.add_applicable_entity({"IfcWall","IfcStandardCase"})

imprägnierung = IfcSimplePropertyTemplate("Imprägnierung","blah blah",".P_ENUMERATEDVALUE.","IfcInteger")
imprägnierung.assign_step_id(2)
custom_pset.add_property_template(imprägnierung.step_id)


imprägnierung_enum = IfcPropertyEnumeration("test")
imprägnierung_enum.add_enumeration_values({"IfcInteger('1'),IfcInteger('2')"})
imprägnierung_enum.assign_step_id(3)
imprägnierung.assign_enumerator(imprägnierung_enum.step_id)


print(custom_pset.get_step_object()+imprägnierung.get_step_object()+imprägnierung_enum.get_step_object())

