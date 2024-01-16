from argparse import ArgumentParser
import re
import sys


LETTER_TO_NUMBER = {
    'A': '2',
    'B': '2',
    'C': '2',
    'D': '3',
    'E': '3',
    'F': '3',
    'G': '4',
    'H': '4',
    'I': '4',
    'J': '5',
    'K': '5',
    'L': '5',
    'M': '6',
    'N': '6',
    'O': '6',
    'P': '7',
    'Q': '7',
    'R': '7',
    'S': '7',
    'T': '8',
    'U': '8',
    'V': '8',
    'W': '9',
    'X': '9',
    'Y': '9',
    'Z': '9'
}
def letters_to_numbs(match): 
    """Changes letters to numbers.
    
    Args:
        match (str): a letter found in a phone number.
    
    Returns:
        str: the number associated with the letter.
    """
    return LETTER_TO_NUMBER[match[0]]

class PhoneNumber: 
    '''
    Represents a phone number using the North American Numbering Plan (NANP).
    
    Attributes:
        area_code (str): The area code of the phone number, the first 3 digits, occur after the optional country code.
        exchange_code (str): The exchange code of the phone number, the following 3 digits after the area code.
        line_number (str): The line number of the phone number, the last 4 digits of the phone number.
        number (str): The full phone number, excluding the country code.
    
    '''
    def __init__(self, pn): 
        '''
        Initializes a PhoneNumber object based on the provided number.
        
        Args:
            number (str or int): The phone number to be processed.
            
        Side effects: 
            Sets area_code, exchange_code, and line_number attributes.
            
        Raises:
            ValueError: If the phone number is invalid or in an incorrect format.
        '''
        if isinstance(pn, (str, int)): 
            pn_to_str = str(pn) 
        
        new = re.sub('[A-Z]', letters_to_numbs, pn_to_str)
        
        clean_nums = re.sub('\D', '', new)
        
        regex_pattern = r"(?:P<country_code>^\d{1})?(?P<area_code>\d{3})(?P<exchange_code>\d{3})(?P<line_number>\d{4}$)" 
        match = re.search(regex_pattern, clean_nums)
        #r'(?P<country_code>\d{1})?(?P<area_code>\d{3})(?P<exchange_code>\d{3})(?P<line_number>\d{4}$)'

        if match != None:
            if match['area_code'][0] in ['0', ['1']] or match['exchange_code'][-2:] == '11': 
                raise ValueError("Invalid phone number")
            elif match ['area_code'][-2:] == '11' or match['exchange_code'][-2] == '11':
                raise ValueError("Invalid phone number")
            else: 
                self.area_code = match['area_code']
                self.exchange_code = match['exchange_code']
                self.line_number = match['line_number']
                self.number = self.area_code + self.exchange_code + self.line_number
        else:
            raise ValueError("invalid phone number")

    def __int__(self):
        '''
        Converts the phone number string to an integer value.
        
        Returns:
            int: The integer representation of the phone number.
        '''
        return int(self.number)  
    def __repr__(self): 
        '''
        Returns a formal representation of the PhoneNumber object.
        
        Returns:
            str: A formal representation of the PhoneNumber object.
        '''
        return f"PhoneNumber('{self.area_code}{self.exchange_code}{self.line_number}')"
    def __str__(self): 
        '''
        Returns an informal representation of the PhoneNumber object.
        
        Returns:
            str: An informal representation of the PhoneNumber object.
        '''
        return f"({self.area_code}) {self.exchange_code}-{self.line_number}"
    def __lt__(self, other):
        '''
        Compares two PhoneNumber objects based on their numeric values.
        
        Args:
            other (PhoneNumber): The PhoneNumber object to compare.
            
        Returns:
            bool: True if self is less than other, False otherwise.
        '''
        if int(self.number) < int(other.number):
            return True 
        else: 
            return False     
    
        
def read_numbers(filepath):
    '''
    Reads names and phone numbers from a text file and processes them.
    
    Args:
        filepath (str): The path to the file containing names and phone numbers.
        
    Returns:
        list: A list of tuples containing names and PhoneNumber objects.
    '''
    with open(filepath, 'r', encoding = 'UTF-8') as f: 
        phone = []
        for line in f:
            name, number = line.strip().split('\t')
            num = re.sub(r'[^0-9A-Z]', lambda match: LETTER_TO_NUMBER.get(match.group(0)), number.upper())
            try: 
                phone_number = PhoneNumber(number)
                phone.append((name, phone_number))
            except ValueError:
                continue
        phone.sort(key= lambda p: p[1])
    return phone

            
def main(path):
    """Read data from path and print results.
    
    Args:
        path (str): path to a text file. Each line in the file should consist of
            a name, a tab character, and a phone number.
    
    Side effects:
        Writes to stdout.
    """
    for name, number in read_numbers(path):
        print(f"{number}\t{name}")


def parse_args(arglist):
    """Parse command-line arguments.
    
    Expects one mandatory command-line argument: a path to a text file where
    each line consists of a name, a tab character, and a phone number.
    
    Args:
        arglist (list of str): a list of command-line arguments to parse.
        
    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file of names and numbers")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)
