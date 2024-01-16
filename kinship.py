#Erin Keane 
"""Determines if two people are related through a model of family relationships."""
from argparse import ArgumentParser
import json 
import sys 
import relationships

class Person():
    """ Represents a person in a family. 
    
        Attributes: 
            name (str): A person's name. 
            gender (str): The person's gender, either female, male, or nonbinary.
            parents (list of Person objects): could be empty, list of a person's parents.
            spuse (Person): the person's spouse, could not be applicable and will return None.
    """
    def __init__(self, name, gender):
        """Initalizes the Person object.

        Args:
            name (str): A persons name.
            gender (str): The persons gender, either female, male, or nonbinary.
            
        Side effects: 
            Sets the attributes of the person object, such as name, gender, parents, and spouse.
        """
        self.name = name 
        self.gender = gender 
        self.parents = []
        self.spouse = None 
        
    def add_parent(self, parent):
        """Adds a parent to the attribute
        
            Side effects: 
                Modifies the self.parents by adding to the list.
        """
        self.parents.append(parent)
        
    def set_spouse(self, spouse):
        """Adds a spouse to the attribute.
        """
        self.spouse = spouse
         
    def connections(self): 
        """ Identify connections between possible relatives

        Returns:
            dict: a dictionary 
        """
        cdict = {self: ''} 
        queue = [self]
        while queue: 
            person = queue.pop(0) 
            personpath = cdict[person]
            
            for parent in person.parents: 
                if parent not in cdict: 
                    parentpath = personpath + "P"
                    cdict[parent] = parentpath 
                    queue.append(parent)
                    
            if 'S' not in personpath and person.spouse and person.spouse not in cdict: 
                spousepath = personpath + "S"
                cdict[person.spouse] = spousepath
                queue.append(person.spouse)
        return cdict
    
    def relation_to(self,person):
        """_summary_

        Args:
            person (Person): person is an instance of the Person class.

        Returns:
            str: describes the relationship between the two individuals.
        """
        person_dict = person.connections() 
        self_dict = self.connections() 
        combined_paths = set(self_dict).intersection(set(person_dict))
        
        if not combined_paths: 
            return None 
        else: 
           lcr = min(combined_paths, key = lambda p: len(f"{self_dict[p]} : {person_dict[p]}"))
           lcr_path = f"{self_dict[lcr]}:{person_dict[lcr]}"
           if lcr_path in relationships.relationships: 
               return relationships.relationships[lcr_path][self.gender]
           else: 
               return 'distant relative' 
           
class Family(): 
    """ Keeps track of the Person instances, each instance is a person.
    
    Attributes: 
        people (dict): each key is the name of a person and the value is a corresponding Person object.
    """
    def __init__(self, familydict):
        """_summary_

        Args:
            familydict (dict): This dictionary has 3 sub containers:
            individuals (dict) - Persons name and their gender.
            parents (dict) - Persons name and their parents.
            couples (list of str) - Contains a married couple of two names.
            
        Side Effects: 
            Sets the people attribute, modifies the spouse and parent attribute.
        """
        self.people = {} 
        
        for individual in familydict ['individuals']: 
            other_person = Person(individual, familydict['individuals'] [individual])
            self.people[other_person.name] = other_person      
            
        for individual in familydict['parents']:
            human_obj = self.people[individual]
            for parent in familydict ['parents'][individual]:
                parent_obj = self.people[parent]
                human_obj.add_parent(parent_obj)
            
        for couple in familydict['couples']: 
            person1 = self.people[couple[0]]
            person2 = self.people[couple[1]]
            person1.set_spouse(person2)
            person2.set_spouse(person1)
            
    def relation(self, name1, name2): 
        """Returns the determined relationship between two individuals.

        Args:
            name1 (str): Name of a person in the family tree 
            name2 (str): Name of a second person in the family tree

        Returns:
            None or str: a kindship term
        """
        name1_object = self.people[name1]
        name2_object = self.people[name2]
        
        return name1_object.relation_to(name2_object)
    
        
def main(filepath, name1, name2): 
    """Finalizes the relationship between two individuals using the specified file.

    Args:
        filepath (str): The path to the JSON file.
        name1 (str): The name of a person located in the JSON file.
        name2 (str): The name of a second person located in the JSON file.
        
    Side effects: 
        Prints to the consule. 
    """
    with open(filepath, "r", encoding = "utf-8") as f: 
        familydata = json.load(f)
        family_connection = Family(familydata)
        family_connection.relation(name1, name2)
        if family_connection.relation(name1, name2) == None: 
            print(f"{name1} is not related to {name2}")
        else: 
            print(f"{name1} is {name2}'s {family_connection.relation(name1,name2)}")

def parse_args(argslist): 
    """Parse command-line arguments.

    Args:
        argslist (list of str): Arguments from the command line.

    Returns:
        A namespace: The parsed arguments as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("filepath", help = "a filepath to the json file")
    parser.add_argument("name1", help = "a first name defined in the json file")
    parser.add_argument("name2", help = "a second name defined in the json file")
    
    return parser.parse_args(argslist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filepath, args.name1, args.name2)