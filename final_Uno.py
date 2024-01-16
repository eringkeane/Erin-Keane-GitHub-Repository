"""Play a game of Uno."""

import random
import argparse
import sys
import re

class Cards:
    """A class of Uno cards."""
    def __init__(self):
        """Initializes a Cards object.
        
        Side effects:
            Sets the 'colors', 'types', and 'wild' attributes.
        
        Primary author: Katy Lamb
        """
        self.colors = ["Red", "Yellow", "Blue", "Green"]
        self.types = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Reverse', 'Draw2', 'Skip']
        self.wild = ['Wild Card', 'Wild Draw4'] 

class Deck(Cards):
    """A class to make the deck of Uno cards."""
    def __init__(self):
        """Initializes a Deck object.
       
        Side effects:
            Inherits the 'colors', 'types', and 'wild' attributes from the Card class 
                using super() and sets the 'deck' attribute.
        
        Primary author: Katy Lamb
        Technique: Inheritance
        """
        self.deck = []
        super().__init__()
    
    def deck_info(self):
        """Creates an Uno deck.

        Side effects:
            Changes the value of the 'deck' attribute.

        Returns:
            list: the Uno cards.
        
        Primary author: Katy Lamb
        """
        for color in self.colors:
            for types in self.types:
                card_info = "{} {}".format(color, types)
                self.deck.append(card_info)
                if types != 0:
                    self.deck.append(card_info)
        self.deck.extend(self.wild * 4)
        return self.deck
   
    def shuffle_deck(self):
        """Shuffles the deck of cards.

        Side effects:
            Changes the value of the 'deck' attribute.

        Returns:
            list: the shuffled cards.
        
        Primary author: Erin Keane
        """
        random.shuffle(self.deck)
        return self.deck
    
    def __repr__(self):
        """ A formal representation of the Deck.
        
        Returns:
            str: the current Uno cards in the deck.
        
        Primary author: Erin Keane
        Technique: Magic method (__repr__)
        """
        return f"Deck: {self.deck!r}"

def deal(deck, num_cards=7):
    """Deals each player a hand of cards.
 
    Args:
        deck (list): a deck of Uno cards.
        num_cards (int): the number of cards to deal to each player.
     
    Returns:
        list: list of cards in the player's hand.
    
    Primary author: My Tran
    Technique: List comprehension
    """
    players_hand = [deck.pop(0) for i in range(num_cards)]
    return players_hand

def can_play_card(selected_card, top_of_discard):
    """Checks if any card in hand can be played given the card on top of the deck.
 
    Args:
        selected_card (str): the card the player wants to play.
        top_of_discard (str): the card on top of the discard pile.
 
    Returns:
        bool: True/ False depending on if the card can be played.
    
    Primary author: My Tran
    Technique: Sequence unpacking
    """
    Tcolor, Trank = top_of_discard.split(" ")
    if "Wild" in selected_card:
        return True
    else:
        Scolor, Srank = selected_card.split(" ")
        if Scolor == Tcolor:
            return True
        elif Srank == Trank:
            return True
        else:
            return False


def end_game(hands):
    """Calculates each player's final score.
 
    Args:
        hands (dict): the players' number (key) and
            their hand of cards (value, a list).
    
    Returns:
        list: list of tuples (player number, final score).
        
    Primary author: Katy Lamb
    Technique: Key function with sorted() command
    """
    final_scores = {player:len(hands[player]) for player in hands}
    ranks = sorted(final_scores.items(), key= lambda c: c[1])
    return ranks

def print_ranks(hands):
    """Prints out player place and their final score.
    
    Args:
        hands (dict): the players' number (key) and
            their hand of cards (value, a list).      
    
    Side effects:
        Prints to stdout.
    
    Primary author: Erin Keane
    Techique: f-string
    """
    final_ranks = end_game(hands)
    place = 0
    for player in final_ranks:
        place += 1
        print(f"{place}. Player {player[0] + 1} with {player[1]} points")

def draw(shuffled_deck, discards, hands, turn, num_players=2):
    """Draws a card from the deck.
    
    Args:
        shuffled_deck (list): a shuffled deck of Uno cards.
        discards (list): the cards in the discard pile.
        hands (dict): the players' number (key) and
            their hand of cards (value, a list).
        turn (int): an index that represents whose turn it is.
        num_players (int): number of players.
    
    Side effects:
        Prints to stdout.
    
    Primary author: Angela Boley
    Technique: Optional parameter
    """
    print("You now have to draw from the deck.")
    if len(shuffled_deck) == 0:
            if len(discards) == 1:
                cards = Cards()
                deck = Deck()
                unshuffled_deck = deck.deck_info()
                new_shuffled_deck = deck.shuffle_deck()
                shuffled_deck = shuffled_deck.extend(new_shuffled_deck)
                print(shuffled_deck)
            else:
                top_deck = discards.pop(0)
                random.shuffle(discards)
                shuffled_deck=shuffled_deck.extend(discards)
                discards.clear()
                discards.append(top_deck)
                print(f"Drew a {shuffled_deck[0]}")
                hands[turn].append(shuffled_deck.pop(0))
                turn = (turn + 1) % num_players
    else:
        print(f"Drew a {shuffled_deck[0]}")
        hands[turn].append(shuffled_deck.pop(0))
        turn = (turn + 1) % num_players
    
def choice(num_cards):
    """Validates the player's choice of playing or drawing a card.
    
    Args:
        num_cards (int): number of cards in a player's hand.
    
    Side effects:
        Prints to stdout.
    
    Returns:
        int: the number of the card the player wants to play.
    
    Primary author: Angela Boley
    """
    while True:
        card_number = input("What card would you like to play?\n"
            "Select the card number.If you can't play a card, input 'draw'.")
        if card_number == "draw":
            return card_number
        else:
            try:
                y = int(card_number)
            except ValueError:
                print("Please enter a number.")
                continue
            if 0 < y <= num_cards:
                return y
            else:
                print("Pick a number in the specified range.")

def wildChoice(choices):
    """Player chooses which card they want to play when they have a wild card.
    
    Args:
        choices (int): the four color options the player can choose from.
        
    Side effects:
        Prints to stdout.
    
    Primary author: Angela Boley
    Technique: Regular expression
    """
    pattern = r"^[1-4]$"
    while True:
        choice = input("What color do you want to change to? Select the number.")
        if re.match(pattern, choice):
            y = int(choice)
            if y in choices:
                return y
            else:
                print("Invalid choice. Please select a valid number.")
        else:
            print("Pick a number in the specified range.")

def play(turn, hands, discards, direction, shuffled_deck, num_players):
    """Player taking a turn.
 
    Args:
        turn (int): an index that represents whose turn it is.
        hands (dict): the players' number (key) and
            their hand of cards (value, a list).
        discards (list): cards in the discard pile.
        direction (int): defines the direction the game moves among players.
        shuffled_deck (list): a shuffled deck of Uno cards.
        num_players (int): the number of players.
        
    Side effects:
        Prints to stdout.
    
    Primary author: Josie Whittington
    Technique: Conditional expression
    """
    while True:
        print(f"It's now Player {turn + 1}'s turn!")
        print(f"These are your cards:")
        i = 1
        for card in hands[turn]:
            print(f"{i}. {card}")
            i += 1
        print("\n")
        print(f"Top Card: {discards[-1]}")
        
        x = choice(len(hands[turn]))
        if x == "draw":
            draw(shuffled_deck,discards,hands,turn,num_players)
        else:
            selected_card = (hands[turn])[x-1]
            print(selected_card)
            if can_play_card(selected_card, discards[-1]) is True:
                if "Reverse" in selected_card:
                    direction *= -1
                    discards.append((hands[turn]).pop(int(x) -1))
                elif "Skip" in selected_card:
                    discards.append((hands[turn]).pop(int(x) -1))
                    turn = (turn + 2*direction) % num_players
                elif "Draw2" in selected_card:
                    next_player = (turn + direction) % num_players
                    for _ in range(2):
                        draw(shuffled_deck, discards, hands, next_player, num_players)
                    discards.append((hands[turn]).pop(int(x) -1))
                elif "Wild Card" in selected_card:
                    colors = {1:"Blue Wild", 2:"Red Wild", 3:"Green Wild", 4:"Yellow Wild"}
                    for i in colors:
                        print(f"{i}. {colors[i]}")
                        i += 1
                    t= wildChoice(colors)
                    (hands[turn]).pop(int(x) -1)
                    discards.append(colors[int(t)])
                elif "Wild Draw4" in selected_card:
                    colors = {1:"Blue Wild", 2:"Red Wild", 3:"Green Wild", 4:"Yellow Wild"}
                    for i in colors:
                        print(f"{i}. {colors[i]}")
                        i += 1
                    t = wildChoice(colors)
                    (hands[turn]).pop(int(x) -1)
                    discards.append(colors[int(t)])
                    next_player = (turn + direction) % num_players
                    for _ in range(4):
                        draw(shuffled_deck, discards, hands, next_player, num_players)
                else:
                    discards.append((hands[turn]).pop(int(x) -1))
                
                if len(hands[turn]) == 0:
                    print(f"Player {turn + 1} won!")
                    print_ranks(hands)
                    break
                
                print("Uno" if len(hands[turn]) == 1 else "The game continues...")
                
                if "Skip" not in selected_card:
                    turn = (turn + direction) % num_players
            else:
                print("You can't play that card. Please pick another card or draw.")
  
def main(num_players, num_cards):
    """Runs the Uno game.
    
    Args:
        num_players (int): the number of players for the Uno game.
    
    Side effects:
        Prints to stdout (see play() function).
    
    Primary author: Josie Whittington
    """
    while num_players < 2 or num_players > 4:
        num_players = int(input("Invalid. Please enter a number between 2-4. How many players? "))

    turn= 0
    direction = 1
    cards = Cards()
    deck = Deck()
    unshuffled_deck = deck.deck_info()
    shuffled_deck = deck.shuffle_deck()
    hands = {}
       
    print("Let's play Uno!")
    print("Before you begin, here's a brief overview of the rules:")
    print("1. Match your cards based on color or number.")
    print("2. Use a standard Uno deck:")
    print()
    print(repr(deck))
    print()
    print("3. If you can't play a card, draw until you get one you can play")
    print("4. Player who runs out of cards first wins!")
    print("Good luck!")
    print()
    
 
    for player in range(num_players):
        hands[player]=deal(shuffled_deck, num_cards=num_cards)
        
    discards = []
    discards.append(shuffled_deck.pop(0))
 
    if "Wild" in discards[0]:
        discards[0] = "Blue 4"
        
    play(turn, hands, discards, direction, shuffled_deck, num_players)

def parse_args(arglist):
    """Parse and validate command-line arguments for Uno game.
    
    Args:
        arglist (list of str): command-line arguments.
        
    Returns:
        namespace: parsed arguments.
    
    Primary author: Josie Whittington
    Technique: Instance of ArgumentParser() class
    """
    parser = argparse.ArgumentParser(description='Play a game of Uno.')
    parser.add_argument('--num_players', type=int, default=2, choices=range(2, 5),
                        help='Number of players (between 2 and 4, default: 2)')
    parser.add_argument('--num_cards', type=int, default=5,
                            help='Number of cards to deal to each player (default: 5)')
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.num_players, args.num_cards)