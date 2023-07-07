"""Blackjack

This script runs a simulation of a game of Blackjack
"""
from random import randint
shuffled_deck = []
discard_deck = []
card_remainder_set = 50
deck_number_set = 8


class Player:
    """A class representing a player in a blackjack game and their moves"""
    card_values = dict([(i, i) for i in range(1,11)] + [(11, 10), (12, 10), (13, 10)])

    def __init__(self, name, input_cash = 100):
        self.hand = []
        self.play_cash = input_cash
        self.initial_cash = input_cash
        self.wager_amount = 0
        self.hand_value = []
        self.bust = False
        self.stayed = False
        self.name = name

    def lose_hand(self):
        """lose wager to dealer and discard hand"""
        pass

    def win_hand(self):
        """win wager from dealer and discard hand"""
        pass

    def push_hand(self):
        """tie with dealer and discard hand"""
        pass

    def hit(self):
        """deal card to player hand"""
        deck_index = randint(0, len(shuffled_deck)-1)
        self.hand.append(shuffled_deck[deck_index])
        shuffled_deck.pop(deck_index)
        # TODO : update hand value and bust value

    def discard(self):
        """empty hand to discard pile"""
        discard_deck.append(self.hand.pop())

    def stay(self):
        """pass turn to next player"""
        self.stayed = True

    def is_bust(self):
        """determine if player hand is a bust"""
        pass

    def get_total(self):
        """calculate sum of hand factoring aces"""
        hand_sum = sum(self.card_values[i] for i in self.hand)

    def split(self):
        """separate matching cards to multiple hands"""
        pass

    def double_down(self):
        """validate play_cash for double wager_amount and receive one more card"""
        pass

    def make_wager(self):
        """prompt user for wager_amount, validate, and set"""
        pass

    def print_player(self):
        """print player cash, wager, and current hand to screen"""
        pass

    def set_wager(self, wager_amount):
        """take input: wager_amount, set wager attribute to that value, and subtract from total cash"""
        pass


class Dealer(Player):
    """class representing dealer in blackjack"""
    def print_dealer(self):
        """print dealer top card while leaving bottom card hidden"""
        pass

    def show_hand(self):
        """print dealer hand"""
        pass
      

def shuffle_discard(shuffled_deck, discard_deck):
    """Shuffles the cards from the discard pile and puts them into the deck"""
    pass


def display_rules():
    """print the rules out to the screen"""
    pass


def change_settings():
    """enter menu for user to change game settings or return to home menu"""
    pass
    # TODO: card remainder limit
    # TODO: surrender
    # TODO: Insurance
    # TODO: Splitting
    # TODO: payout level
    # TODO: deck number (relate to card remainder limit)


def is_float(string_value):
    """Determines if string can be converted to float value"""
    if string_value is None:
        return False
    try:
        float(string_value)
        return True
    except:
        return False
    

def is_int(string_value):
    """Determines if string represents rounded integer"""
    if is_float(string_value) and float(string_value) // 1 == float(string_value):
        return True
    else:
        return False


def play_game():
    """play blackjack simulation"""
    num_players = ""
    player_list = []
    cash_input = ""
    dealer = Dealer(0)
    player_move_input = ""
    player_name_input = ""
    player_quit_input = ""

    # allow selection for number of players from 1 to 7
    print("Please select the number of players that would like to play (1-7): ")
    num_players = input()
    while num_players.strip() not in ['1', '2', '3', '4', '5', '6', '7']:
        print("Please input a valid number of players: ")
        num_players = input()
    

    # insert cards into shuffled_deck based on number of decks setting
    for i in range(1, 14):
        shuffled_deck += [i] * deck_number_set

    # initialize each Player instance with prompted initial cash value and add to player list
    for player_number in range(1, int(num_players)+1):
        player_name_input = input("Player {}, please input your name: ".format(player_number))
        cash_input = input("Player {}, please input the amount of cash you would like to play with: ".format(player_number))
        while not is_int(cash_input) or float(cash_input) < 1:
            if not is_float(cash_input):
                print("\nPlease input a valid amount:")
            elif float(cash_input) < 1:
                print("\nSorry, we do not provide credit, please input a positive amount:")
            else:
                print("\nWe only play with whole dollars, please keep your change.")
                break
            cash_input = input()
        player_list.append(Player(player_name_input, int(float(cash_input))))

    # show players and cash
    for player in player_list:
        player.print_player()
    print("Press Enter to continue...")
    input()

    # game loops while there are any players
    wager_input = ""
    while player_list != []:
       
        # wager prompt and validation loop
        for player in player_list:
            print("{}, please input the amount you would like to wager for the round: ".format(player.name))
            wager_input = input()
            while not is_int(wager_input) or float(wager_input) < 1 or float(wager_input) > player.play_cash:
                print("\Current cash: ", player.play_cash)
                if not is_float(wager_input):
                    print("Please input a valid wager amount: ", end = "")
                elif float(wager_input) < 1:
                    print("That's not how we do wagers here, you must wager at least a dollar: ", end = "")
                elif float(wager_input) > player.play_cash:
                    print("You may not wager more than you have, please make a new wager: ", end = "")
                else:
                    print("Your wager has been rounded down to the nearest dollar.\n")
                    break
                wager_input = input()
            player.set_wager(int(float(wager_input)))
            input("Press Enter to continue...")

        # deal cards to players and dealer, shuffling if too few cards remain
        for i in range(2):
            for player in player_list:
                if len(shuffled_deck) < card_remainder_set:
                    shuffle_discard(shuffled_deck, discard_deck)
                player.hit()
            if len(shuffled_deck) < card_remainder_set:
                shuffle_discard(shuffled_deck, discard_deck)
            dealer.hit()

        # show player hands and dealer's face up card
        for player in player_list:
            player.print_player()
        dealer.print_dealer()

        # if dealer has natural, show hand, and all players without blackjack lose
        if dealer.hand_value == 21:
            dealer.show_hand()
            for player in player_list:
                if player.hand_value == 21:
                    player.push_hand()
                else:
                    player.lose_hand()

        # TODO: Add options for double down and split
        # dealer does not have natural, players take turns
        else:
            for player in player_list:
                while not player.stayed and not player.bust:
                    print("{}: ".format(player.name))
                    player.print_player()
                    print("Please select the option you would like to do: ")
                    print("1. Hit")
                    print("2. Stay")
                    player_move_input = input()

                    # input validation loop
                    while player_move_input.strip().lower() not in ["1", "2", "h", "hit", "s", "stay"]:
                        print("Please input valid selection: ")
                        print("1. Hit")
                        print("2. Stay")
                        player_move_input = input()
                    player_move_input = player_move_input.strip().lower()

                    # hit
                    if player_move_input in ["1", "h", "hit"]:
                        if player.hand_value[0] < 21:
                            player.print_player()
                            player.hit()
                        else:
                            print("You may not hit. You must stay.")
                            player.stay()

                    # stay
                    elif player_move_input in ["2", "s", "stay"]:
                        print("You stayed.")
                        player.stay()     

            # dealer turn
            dealer.show_hand()
            while dealer.hand_value < 17:
                dealer.hit()
                dealer.show_hand()
                input("Press Enter to continue...")

            # resolve player wagers after dealer turn
            for player in player_list:
                if dealer.bust:
                    if player.bust:
                        player.lose_wager()
                    else:
                        player.win_wager()
                elif dealer.hand_value[0] == 21:
                    if player.hand_value[0] == 21 and len(player.hand) == 2:
                        player.win_wager()
                    else:
                        player.lose_wager()
                else:
                    if not player.bust and player.hand_value[0] > dealer.hand_value[0]:
                        player.win_wager()
                    elif not player.bust:
                        player.lose_wager()

            # print players after turn resolution
            for player in player_list:
                player.print_player()
            
            # exit player from game if cash is 0, prompt player if they would like to exit
            i = 0
            for player in player_list:
                player.print_player()
                if player.play_cash == 0:
                    input("{}, you have run out of money, you must leave the table.".format(player.name))
                    player_list.pop(i)
                else:
                    player_quit_input = input("{}, Press Enter to continue, or input '1' if you would like to quit...")
                    if player_quit_input.strip() == "1":
                        player_list.pop(i)
                        input("Thank you for playing {}.\nPress Enter to continue...".format(player.name))
                i += 1          

            
        



def main():  
    print("Welcome to Blackjack!")

    while True:  
        print()
        print("1. Play")
        print("2. Rules")
        print("3. Settings")
        print("4. Exit\n")
        
        selection_choice = ""
        selection_choice = input()
        while selection_choice.lower() not in ['1', '2', '3', '4', 'p', 'play',
                                               'r', 'rule', 'rules', 's', 'set',
                                               'setting', 'settings', 'e', 'exit']:
            print("Please make a valid selection...")
            selection_choice = input()
        
        if selection_choice.lower() in ['1', 'p', 'play']:
            play_game()
            selection_choice = ""
        
        if selection_choice.lower() in ['2', 'r', 'rule', 'rules']:
            display_rules()
            selection_choice = ""

        if selection_choice.lower() in ['3', 's', 'set', 'setting', 'settings']:
            change_settings()
            selection_choice = ""

        if selection_choice.lower() in ['4', 'e', 'exit']:
            print("Thank you for playing\n")
            exit()

   
if __name__ == '__main__':
    main()

# TODO: write play_game function
# TODO: complete player Class methods
# TODO : remove player if cash drops to 0

# TODO: write display_rules function
# TODO: update printing and hitting and card dict to accomodate suit

# TODO: write change_settings function
# TODO: print update message for player leaving game / don't allow player quits



# UPDATED: dealer turn
# UPDATED: round resolution
# UPDATED: add player names
# UPDATED: add player quit option