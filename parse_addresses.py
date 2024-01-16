from argparse import ArgumentParser
import re
import sys

class Address: 
    """ An Address
    
    Attributes: 
        address (str): the complete address.
        house_number (str): the house number of the address.
        street (str): the street name.
        city (str): the city.
        state (str): the state. 
        zip (str): the zip code. 
    """
    def __init__(self,address): 
        """Uses a regular expression to match the address, andinitializes an Address object.

        Args:
            address (str): a one line address from the text file.

        Raises:
            ValueError: The address string can not be parsed.
            
        Side effects: 
            Sets the attributes, such as house_number, street, city, state and zip by using a regular expression. 
        """
        regex_address = (r"(?P<house_number>^\S+)\s(?P<street>.+)\,\s(?P<city>[\w\s]+)\s(?P<state>[A-Z]{2})\s+(?P<zip>\d{5}$)")
        match = re.search(regex_address, address)
        if match is None: 
            raise ValueError
        else:
            self.address = match[0]
            self.house_number = match.group('house_number')
            self.street = match.group('street')
            self.city = match.group('city')
            self.state = match.group('state')
            self.zip = match.group('zip')
        
    def __repr__(self):
        """Return a formal representation of the Address object."""
        return (
            f"address:      {self.address}\n"
            f"house number: {self.house_number}\n"
            f"street:       {self.street}\n"
            f"city:         {self.city}\n"
            f"state:        {self.state}\n"
            f"zip:          {self.zip}"
         )

def read_addresses(filepath):
    """Creates and converts each line to a list of addresses objects. 

    Args:
        filepath (str): a path to a file that contains one address per line.

    Returns:
        a list with one instance of Address objects. 
    """
    with open(filepath, 'r', encoding = 'UTF-8') as f: 
            addresses = [Address(line) for line in f]
    return addresses

def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect one mandatory argument, the path to a file of addresses.
    
    Args:
        arglist (list of str): command-line arguments.
    
    Returns:
        namespace: an object with one attribute, file, containing a string.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file containing one address per line")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    for address in read_addresses(args.file):
        # the !r tells the f-string to use the __repr__() method to generate
        # a string version of the address object
        print(f"{address!r}\n")