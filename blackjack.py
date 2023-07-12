"""Blackjack

This script runs a simulation of a game of Blackjack
"""
from random import randint
from textwrap import fill

card_remainder_set = 52
deck_number_set = 8
payout_rate_set = 1.5
shuffled_deck = []
discard_deck = []

class Player:
    """A class representing a player in a blackjack game and their moves"""
    card_values = dict([(i, i) for i in range(2,11)] + [(11, 10), (12, 10), (13, 10), (1, 11), (0, 0)])
    card_faces = dict([(i, "{}".format(i)) for i in range(2, 11)] + [(11, "J"), (12, "Q"), (13, "K"), (1, "A")])

    def __init__(self, name, input_cash = 100):
        self.hand = [0]
        self.play_cash = input_cash
        self.initial_cash = input_cash
        self.wager_amount = 0
        self.hand_value = [0]
        self.bust = False
        self.stayed = False
        self.name = name

    def make_wager(self):
        """prompt user for wager_amount, validate, and set"""
        self.print_player()
        wager_input = input("Input wager: ")
        while not is_int(wager_input) or float(wager_input) < 1 or float(wager_input) > self.play_cash:
            print("\nCurrent cash: ", self.play_cash)
            if not is_float(wager_input):
                print("Please input a valid wager amount: ", end = "")
            elif float(wager_input) < 1:
                print("That's not how we do wagers here, you must wager at least a dollar: ", end = "")
            elif float(wager_input) > self.play_cash:
                print("You may not wager more than you have, please make a new wager: ", end = "")
            else:
                print("Your wager has been rounded down to the nearest dollar.\n")
                break
            wager_input = input()
        self.play_cash -= int(float(wager_input))
        self.wager_amount = int(float(wager_input))

    def prompt_move(self):
        """prompt user for the move they would like to make on their turn"""
        while not self.stayed and not self.bust:
            self.print_player()
            print("\nPlease select your action: ")
            print("1. Hit")
            print("2. Stay")
            player_move_input = input()

            # input validation loop
            while player_move_input.strip().lower() not in ["1", "2", "h", "hit", "s", "stay"]:
                print("\nPlease input valid selection: ")
                print("1. Hit")
                print("2. Stay")
                player_move_input = input()
            player_move_input = player_move_input.strip().lower()

            # hit
            if player_move_input in ["1", "h", "hit"]:
                if self.hand_value[0] < 21:
                    self.hit()
                else:
                    input("You have 21. You may not hit. You must stay.")
                    self.stay()

            # stay
            elif player_move_input in ["2", "s", "stay"]:
                input("\nYou stayed.\n")
                self.stay()
        self.stayed = False 

    def hit(self):
        """deal card to player hand"""
        global shuffled_deck
        global discard_deck

        # shuffle discard into deck if too few cards remain
        if len(shuffled_deck) <= card_remainder_set:
            shuffled_deck += discard_deck
            discard_deck = []

        # choose random card in shuffled_deck
        deck_index = randint(0, len(shuffled_deck)-1)
        new_card = shuffled_deck[deck_index]
        shuffled_deck.pop(deck_index)

        # add new card to hand value. append if new card is ace
        for i in range(0, len(self.hand_value)):
            self.hand_value[i] += self.card_values[new_card]
        if new_card == 1:
            if len(self.hand_value) == 1:
                self.hand_value.append(0)
            self.hand_value[1] = self.hand_value[0] - 10
        if len(self.hand_value) == 2 and self.hand_value[0] > 21:
            self.hand_value.pop(0)

        # add new card to hand
        if self.hand[0] == 0:
            self.hand.pop(0)
        self.hand.append(new_card)

        # lose hand if bust
        if self.hand_value[0] > 21:
            self.bust = True
            if self.play_cash != -1:
                input("\nYou busted.")
                self.print_player()
                self.hand_resolution(-1)

    def stay(self):
        """pass turn to next player"""
        self.stayed = True

    def hand_resolution(self, outcome):
        """resolve wager with dealer and discard hand"""
        # win hand
        if outcome == 1:
            self.play_cash += self.wager_amount * 2
            self.wager_amount = 0
            self.discard()
            print("\n{} won!\n". format(self.name))
        
        # tie hand
        elif outcome == 0:
            self.play_cash += self.wager_amount
            self.wager_amount = 0
            self.discard()
            print("\n{} tied.\n".format(self.name))
        
        # lose hand
        elif outcome == -1:
            self.wager_amount = 0
            self.discard()
            print("\n{} lost.\n".format(self.name))

    def discard(self):
        """empty hand to discard pile"""
        global discard_deck
        discard_deck += self.hand
        self.hand = [0]
        self.hand_value = [0]

    def print_player(self):
        """print player cash, wager, and current hand to screen"""
        print()
        print(self.name)
        print("~" * 20)
        print("Cash:  ", self.play_cash)
        print("Wager: ", self.wager_amount)
        print("Hand: ", end = " ")
        if self.hand[0] != 0:
            print(self.card_faces[self.hand[0]], end = "")
            for i in self.hand[1:]:
                print(", ", self.card_faces[i], end = "")
        print("\nValue: ", self.hand_value[0])


class Dealer(Player):
    """class representing dealer in blackjack"""
    def print_dealer(self):
        """print dealer top card while leaving bottom card hidden"""
        print()
        print("Dealer")
        print("~" * 20)
        print("Top Card: {}".format(self.card_faces[self.hand[0]]))
        
    def show_hand(self):
        """print dealer hand"""
        print()
        print("Dealer")
        print("~" * 20)
        print("Hand: ", end = " ")
        print(self.card_faces[self.hand[0]], end = "")
        for i in self.hand[1:]:
            print(", ", self.card_faces[i], end="")
        print("\nValue: ", self.hand_value[0])

      
def display_rules():
    """print the rules out to the screen"""
    print("\n", "Welcome to Blackjack!".center(70),"\n")
    string1 = ("This is a basic card game where all players make a bet, then are dealt two cards each"
               " (including the dealer), and then in clockwise order each player plays by hitting"
               " (receiving another card) or standing (keeping the current cards) with the goal of having"
               " a hand total closer than the dealer's to 21. A player may hit as many times in a round"
               " as they would like without going over 21; this is called a bust. Once all players have"
               " gone, it is the dealer's turn. The dealer hits until their hand totals at least 17."
               " Players whose hands total higher than the dealer's without going over 21 win the round,"
               " players whose hand total equaled the dealer's tie, and players whose hand total was "
               " lower than the dealer or over 21 lose.")

    print(fill(string1))
    
    print(("\nFor more in depth rules, visit:\n"
           "    \"https://bicyclecards.com/how-to-play/blackjack/\"\n"))
    
    print(("\nNotes about this program:\n"
          "    -You may change the number of decks used in settings\n"
          "    -You may change the reshuffle limit in settings\n"
          "    -Splitting and Doubling down are not included\n"
          "    -Insurance and Surrender are not included"))
    
    input()


def change_settings():
    """enter menu for user to change game settings or return to home menu"""
    global deck_number_set
    global payout_rate_set
    global card_remainder_set

    setting_selection = ""
    setting_input = ""
    while setting_selection not in ["5", "q", "quit", "return", "exit", "main", "leave", "menu"]:
        print()
        print("-" * 70)
        print("Settings:\n")
        print("Decks:", deck_number_set)
        print("Blackjack Payout Rate:", payout_rate_set)
        print("Card Remainder:", card_remainder_set)
        print()
        print("1. Number of Decks")
        print("2. Blackjack Payout Rate")
        print("3. Card Remainder Before Shuffle")
        print("4. Restore to default")
        print("5. Return to Main Menu")
        setting_selection = input()

        # Number of Decks
        if setting_selection == "1":
            print("\nWARNING: This setting can break the game if improperly selected")
            setting_input =  input("Enter the number of decks to be used in the game (1-10):")
            while setting_input not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                setting_input = input("\nYou must select a number of decks between 1 and 10 (8 default): ")
            deck_number_set = int(setting_input)
            if setting_input == "1":
                input("Card remainder has been set to 0 by default")
                card_remainder_set = 0

        # Payout Rate
        elif setting_selection == "2":
            print("\nSelect the Blackjack Payout Rate you would like to play with\n1.  3/2\n2.  6/5")
            setting_input =  input()
            while setting_input not in ["1", "2"]:
                setting_input = input("\nYou must select either\n1.  3/2\n2.  6/5\n")
            if setting_input == "1":
                payout_rate_set = 3/2
            elif setting_input == "2":
                payout_rate_set = 6/5

        # Cut Card
        elif setting_selection == "3":
            print("\nWARNING: This setting can break the game if improperly selected")
            print("Enter the number of cards (0 - 100) left in draw before reshuffling")
            setting_input = input("or input \"exit\" to return: ")
            while not is_int(setting_input) or float(setting_input) > 100 or float(setting_input) < 0:
                if setting_input == "exit":
                    break
                setting_input = input("\nYou must input \"exit\" or a number 0-100: ")
            if is_int(setting_input):
                card_remainder_set = int(setting_input)
        
        # default settings
        elif setting_selection == "4":
            setting_input = input("\nAre you sure you would like to reset the settings? (y/n)")
            while setting_input.lower() not in ["y", "ye", "yes", "1", "n", "no", "0"]:
                setting_input = input("Please input (y/n), would you like to reset the settings?")
            if setting_input.lower() in ["1", "y", "ye", "yes"]:
                deck_number_set = 8
                payout_rate_set = 1.5
                card_remainder_set = 52
                input("Settings have been reset.")
                
        setting_input = ""


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
    dealer = Dealer("Dealer", -1)
    num_players = ""
    player_list = []
    player_quit_list = []
    cash_input = ""
    player_name_input = ""
    player_quit_input = ""
    global shuffled_deck
    global discard_deck
    global deck_number_set

    # insert cards into shuffled_deck based on number of decks setting
    shuffled_deck = []
    discard_deck = []
    for i in range(1, 14):
        shuffled_deck += [i] * 4 * deck_number_set

    # allow selection for number of players from 1 to 7
    num_players = input("\nPlease select the number of players that would like to play (1-7): ")
    while num_players.strip().lower() not in ['1', '2', '3', '4', '5', '6', '7',
                                              'one', 'two', 'three', 'four', 'five',
                                              'six', 'seven']:
        num_players = input("Please input a valid number of players: ")
    print()

    # initialize each Player instance with prompted initial cash value and name into player list
    for player_number in range(1, int(num_players)+1):
        player_name_input = input("Player {}, please input your name: ".format(player_number))
        cash_input = input("Player {}, please input the amount of cash you would like to play with: ".format(player_number))
        while not is_int(cash_input) or float(cash_input) < 1:
            if not is_float(cash_input):
                print("Please input a valid amount:", end = " ")
            elif float(cash_input) < 1:
                print("Sorry, we do not provide credit, please input a positive amount:", end = " ")
            else:
                print("We only play with whole dollars, please keep your change.")
                break
            cash_input = input()
        print()
        player_list.append(Player(player_name_input, int(float(cash_input))))
    print("-" * 70)
    print()

    # show players and cash
    for player in player_list:
        player.print_player()
        print()
    input("Press Enter to continue...")
    print("-" * 70)

    # game loops while there are any players
    while player_list != []:
        for player in player_list:
            print()
            player.make_wager()

        # deal cards to players and dealer, shuffling if too few cards remain
        for i in range(2):
            for player in player_list:
                player.hit()
            dealer.hit()
        print("-" * 70)
        print()

        # show player hands and dealer's face up card
        for player in player_list:
            player.print_player()
            if player.hand_value[0] == 21:
                print("You have a Blackjack!")
        dealer.print_dealer()
        input("\nPress Enter to continue...")
        print("-" * 70)

        # dealer checks for natural
        if dealer.hand[0] in [10, 11, 12, 13, 1]:
            print("\nDealer checks hole card for a Blackjack")
            input()
            if dealer.hand_value[0] != 21:
                print("Dealer does not have a Blackjack\n")
        if dealer.hand_value[0] == 21:
            input("Dealer has a Blackjack\n")
            dealer.show_hand()
            for player in player_list:
                if player.hand_value[0] == 21:
                    player.hand_resolution(0)
                else:
                    player.hand_resolution(-1)

        # dealer does not have natural
        else:
            # players take turns
            for player in player_list:
                dealer.print_dealer()
                if player.hand_value[0] == 21:
                    player.play_cash += player.wager_amount * (payout_rate_set - 1)
                    player.hand_resolution(1)
                    player.bust = True
                else:
                    player.prompt_move() 
                print("-" * 70)   
             
            # dealer turn only if some players don't bust
            all_bust = True
            for player in player_list:
                all_bust = all_bust and player.bust
            if not all_bust:
                dealer.show_hand()
                while dealer.hand_value[0] < 17 and not dealer.bust:
                    dealer.hit()
                    dealer.show_hand()
                if dealer.bust:
                    print("\nThe Dealer busted.")
                input("\nPress Enter to continue...")
                print("-" * 70)

            # resolve player wagers after dealer turn
            for player in player_list:
                if dealer.bust and not player.bust:
                    player.hand_resolution(1)
                elif not player.bust:
                    if player.hand_value[0] > dealer.hand_value[0]:
                        player.hand_resolution(1)
                    elif player.hand_value[0] == dealer.hand_value[0]:
                        player.hand_resolution(0)
                    else:
                        player.hand_resolution(-1)
            input("\nPress Enter to continue...")
            print("-" * 70)

            # reset player bust and dealer hand
            for player in player_list:
                player.bust = False
            dealer.bust = False
            dealer.discard()

        # print players after turn resolution
        for player in player_list:
            player.print_player()
        print("-" * 70)

        # exit player from game if cash is 0, prompt player if they would like to exit
        for i in range(0, len(player_list)):
            player_list[i].print_player()
            if player_list[i].play_cash < 1:
                input("\n{}, you have run out of money, you must leave the table.\n".format(player_list[i].name))
                player_quit_list.append(i)
            else:
                player_quit_input = input("\n{}, Press Enter to continue,\nor input 'quit' if you would like to quit... \n".format(player_list[i].name))
                if player_quit_input.strip().lower() in ["q", "quit", "exit", "leave", "done"]:
                    player_quit_list.append(i)
                    input("Thank you for playing {}, goodbye.".format(player_list[i].name))
        if player_quit_list:
            player_quit_list.reverse()
            for i in player_quit_list:
                player_list.pop(i)   
        player_quit_list = []
        print("-" * 70)


def main():  
    print("Welcome to Blackjack!")

    while True:  
        print()
        print("1. Play")
        print("2. Rules")
        print("3. Settings")
        print("4. Exit")
        
        selection_choice = ""
        selection_choice = input()
        while selection_choice.lower() not in ['1', '2', '3', '4', 'p', 'play',
                                               'r', 'rule', 'rules', 's', 'set',
                                               'setting', 'settings', 'e', 'exit']:
            print()
            print("Please make a valid selection...")
            print("1. Play")
            print("2. Rules")
            print("3. Settings")
            print("4. Exit")
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
            print("\nThank you for playing! Come back again!\n")
            exit()

   
if __name__ == '__main__':
    main()


# UP: display rules
# UP: corrected standard payout to 1:1 and blackjack to 3/2 or 6/5