#Homework: Mortgage Calculator 
#Erin Keane 

"""Perform fixed-rate mortgage calculations."""

from argparse import ArgumentParser
import math
import sys

def get_min_payment(p, interest_rate, term_years = 30, payments_per_year = 12 ):
    """Computes the minimum monrthly mortgage payment using a formula.

    Args:
        p (float): called principle, represents the total amount of mortgage, a positive number.
        interest_rate (float): annual interest rate, a float between 0 and 1.
        term_years (int, optional): the term of mortgage in years, a positive integer. Defaults to 30.
        payments_per_year (int, optional): the number of payments per year, a positive integer. Defaults to 12.

    Returns:
        int: the minimum mortgage payment rounded to the next highest integer.
    """
    r = interest_rate / payments_per_year
    n = term_years * payments_per_year
    a_a= (p * r * (1 + r) ** n)/ ((1 + r) ** n - 1)
    a = math.ceil(a_a)
    return a


def interest_due(balance, interest_rate, payments_per_year = 12):
    """Computes the amount of interest due for the following payments.

    Args:
        balance (float): balance of mortgage, portion of principal amount that has not been paid back, positive number.
        interest_rate (float): annual interest rate, a float between 0 and 1.
        payments_per_year (int, optional): number of payments per year, positive integer. Defaults to 12.

    Returns:
        float: the amount of interest due the following payment.
    """
    r = interest_rate / payments_per_year
    i = r * balance
    return i 

def remaining_payments(balance, interest_rate, target_payment, payments_per_year = 12): 
    """ Calculate and return number of payments that is required to pay off the mortgage. 

    Args:
        balance (float): balance of mortgage, portion of principal amount that has not been paid back, positive number.
        interest_rate (flaot): annual interest rate, a float between 0 and 1.
        target_payment (float): the amount the customer should pay per month, a positive number.
        payments_per_year (int, optional): number of payments per year, positive integer. Defaults to 12.

    Returns:
        int: the number of payments that is required to pay off the mortgage.
    """
    counter = 0 
    while balance > 0: 
        interest_payment = interest_due(balance, interest_rate, payments_per_year)
        principal_payment = target_payment - interest_payment
        balance -= principal_payment 
        counter += 1
    return counter
    
def main(p, interest_rate, term_years = 30, payments_per_year = 12, target_payment = None):
    """ calculates and displays to the user what their mortgage paymet is and how many payments it will take to pay off their mortgage.

    Args:
        p (float): called principle, represents the total amount of mortgage, a positive number.
        interest_rate (float): annual interest rate, a float between 0 and 1.
        term_years (int, optional): the term of mortgage in years, a positive integer. Defaults to 30.
        payments_per_year (int, optional): number of payments per year, positive integer. Defaults to 12.
        target_payment (float, optional): the amount a user pays per payment, a positive number or None. Defaults to None.
    """
    minimum_payment = get_min_payment(p, interest_rate, term_years, payments_per_year)
    print (f" This is your minimum mortgage payment per month: ${minimum_payment}")
    if target_payment == None:
        target_payment = minimum_payment
        
    if target_payment < minimum_payment: 
        print("Your target payment is less than the minimum payment for this mortgage.")
    else: 
        total_payments = remaining_payments(p, interest_rate, payments_per_year, target_payment)
        print(f"If you make payments of ${target_payment}, you will pay off your mortgage in {total_payments} payments!")


def parse_args(arglist):
    """Parse and validate command-line arguments.
    
    This function expects the following required arguments, in this order:
    
        mortgage_amount (float): total amount of a mortgage
        annual_interest_rate (float): the annual interest rate as a value
            between 0 and 1 (e.g., 0.035 == 3.5%)
        
    This function also allows the following optional arguments:
    
        -y / --years (int): the term of the mortgage in years (default is 30)
        -n / --num_annual_payments (int): the number of annual payments
            (default is 12)
        -p / --target_payment (float): the amount the user wants to pay per
            payment (default is the minimum payment)
    
    Args:
        arglist (list of str): list of command-line arguments.
    
    Returns:
        namespace: the parsed arguments (see argparse documentation for
        more information)
    
    Raises:
        ValueError: encountered an invalid argument.
    """
    # set up argument parser
    parser = ArgumentParser()
    parser.add_argument("mortgage_amount", type=float,
                        help="the total amount of the mortgage")
    parser.add_argument("annual_interest_rate", type=float,
                        help="the annual interest rate, as a float"
                             " between 0 and 1")
    parser.add_argument("-y", "--years", type=int, default=30,
                        help="the term of the mortgage in years (default: 30)")
    parser.add_argument("-n", "--num_annual_payments", type=int, default=12,
                        help="the number of payments per year (default: 12)")
    parser.add_argument("-p", "--target_payment", type=float,
                        help="the amount you want to pay per payment"
                        " (default: the minimum payment)")
    # parse and validate arguments
    args = parser.parse_args()
    if args.mortgage_amount < 0:
        raise ValueError("mortgage amount must be positive")
    if not 0 <= args.annual_interest_rate <= 1:
        raise ValueError("annual interest rate must be between 0 and 1")
    if args.years < 1:
        raise ValueError("years must be positive")
    if args.num_annual_payments < 0:
        raise ValueError("number of payments per year must be positive")
    if args.target_payment and args.target_payment < 0:
        raise ValueError("target payment must be positive")
    
    return args


if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    main(args.mortgage_amount, args.annual_interest_rate, args.years,
         args.num_annual_payments, args.target_payment)
