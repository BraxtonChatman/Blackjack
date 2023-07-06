"""Blackjack

This script runs a simulation of a game of Blackjack
"""

class Player:
    """A class representing a player in a blackjack game and their moves"""
    def __init__(self, initial_cash = 100):
        self.hand = []
        self.play_cash = initial_cash
        self.wager_amount = 0
        self.hand_value = 0

    def hit(self):
        """deal card to player given that their hand doesn't total more than 20"""
        pass

    def stay(self):
        """pass turn to next player"""
        pass

    def is_bust(self):
        """determine if player hand is a bust"""
        pass

    def get_total(self):
        """calculate sum of hand factoring aces"""
        pass

    def split(self):
        """separate matching cards to multiple hands"""
        pass

    def double_down(self):
        """validate play_cash for double wager_amount and receive one more card"""
        pass

    def make_wager(self):
        """prompt user for wager_amount, validate, and set"""
        pass
        

def display_rules():
    pass


def play_game():
    pass


def main():  
    print("Welcome to Blackjack!")

    while True:  
        print()
        print("1. Play")
        print("2. Rules")
        print("3. Exit\n")
        
        selection_choice = ""
        selection_choice = input()
        while selection_choice.lower() not in ['1', '2', '3', 'p', 'play', 'r', 'rule', 'rules', 'e', 'exit']:
            print("Please make a valid selection...")
            selection_choice = input()
        
        if selection_choice.lower() in ['1', 'p', 'play']:
            play_game()
            selection_choice = ""
        
        if selection_choice.lower() in ['2', 'r', 'rule', 'rules']:
            display_rules()
            selection_choice = ""

        if selection_choice.lower() in ['3', 'e', 'exit']:
            print("Thank you for playing\n")
            exit()

   
if __name__ == '__main__':
    main()