"""Blackjack

This script runs a simulation of a game of Blackjack
"""
from random import randint
card_remainder_set = 50
deck_number_set = 8
payout_rate_set = 1.5
shuffled_deck = []
discard_deck = []

class Player:
    """A class representing a player in a blackjack game and their moves"""
    card_values = dict([(i, i) for i in range(2,11)] + [(11, 10), (12, 10), (13, 10), (1, 11), (0, 0)])

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
            print("\nPlease select the option you would like to do: ")
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
                    print("You may not hit. You must stay.")
                    self.stay()

            # stay
            elif player_move_input in ["2", "s", "stay"]:
                print("\nYou stayed.\n")
                self.stay()
        self.stayed = False 

    def hit(self):
        """deal card to player hand"""
        global shuffled_deck
        global discard_deck
        if len(shuffled_deck) < card_remainder_set:
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
                print("\nYou busted.\n")
                self.lose_hand()
            else:
                print("\nDealer Busted\n")

    def stay(self):
        """pass turn to next player"""
        self.stayed = True

    def split(self):
        """separate matching cards to multiple hands"""
        pass

    def double_down(self):
        """validate play_cash for double wager_amount and receive one more card"""
        pass

    def win_hand(self):
        """win wager from dealer and discard hand"""
        self.play_cash += self.wager_amount
        self.play_cash += self.wager_amount * payout_rate_set
        self.wager_amount = 0
        self.discard()
        print("{}, you won!\n".format(self.name))

    def lose_hand(self):
        """lose wager to dealer and discard hand"""
        self.wager_amount = 0
        self.discard()
        print("{}, you lost.\n".format(self.name))

    def push_hand(self):
        """tie with dealer and discard hand"""
        self.play_cash += self.wager_amount
        self.wager_amount = 0
        self.discard()
        print("{}, you tied.\n".format(self.name))

    def discard(self):
        """empty hand to discard pile"""
        global discard_deck
        discard_deck += self.hand
        self.hand = [0]
        self.hand_value = [0]

    def print_player(self):
        """print player cash, wager, and current hand to screen"""
        print("\n")
        print(self.name)
        print("~" * 12)
        print("Cash:  ", self.play_cash)
        print("Wager: ", self.wager_amount)
        print("Hand: ", end = " ")
        if self.hand[0] != 0:
            print(self.card_values[self.hand[0]], end = "")
            for i in self.hand[1:]:
                print(", ", self.card_values[i], end = "")
        print("\nValue: ", self.hand_value[0])


class Dealer(Player):
    """class representing dealer in blackjack"""
    def print_dealer(self):
        """print dealer top card while leaving bottom card hidden"""
        print("\n\nDealer")
        print("~" * 12)
        print("Top Card: {}\n".format(self.card_values[self.hand[0]]))
        input("Press Enter to continue...")

        
    def show_hand(self):
        """print dealer hand"""
        print("\n\nDealer")
        print("~" * 12)
        print("Hand: ", end = " ")
        print(self.hand[0], end = "")
        for i in self.hand[1:]:
            print(", ", self.card_values[i], end="")
        print("\nValue: ", self.hand_value[0])
      

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
    dealer = Dealer("Dealer", -1)
    num_players = ""
    player_list = []
    player_quit_list = []
    cash_input = ""
    player_name_input = ""
    player_quit_input = ""
    global shuffled_deck
    global discard_deck

    # insert cards into shuffled_deck based on number of decks setting
    for i in range(1, 14):
        shuffled_deck += [i] * 4 * deck_number_set

    # allow selection for number of players from 1 to 7
    num_players = input("\nPlease select the number of players that would like to play (1-7): ")
    while num_players.strip().lower() not in ['1', '2', '3', '4', '5', '6', '7',
                                              'one', 'two', 'three', 'four', 'five',
                                              'six', 'seven']:
        num_players = input("Please input a valid number of players: ")

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
        player_list.append(Player(player_name_input, int(float(cash_input))))

    # show players and cash
    for player in player_list:
        player.print_player()
    input("\nPress Enter to continue...")
    print("-" * 70)

    # game loops while there are any players
    while player_list != []:
        for player in player_list:
            player.make_wager()

        # deal cards to players and dealer, shuffling if too few cards remain
        for i in range(2):
            for player in player_list:
                player.hit()
            dealer.hit()
        print("-" * 70)

        # show player hands and dealer's face up card
        for player in player_list:
            player.print_player()
        dealer.print_dealer()
        print("-" * 70)

        # if dealer has natural, show hand, and all players without blackjack lose
        if dealer.hand_value == 21:
            print("Dealer has 21\n")
            dealer.show_hand()
            for player in player_list:
                if player.hand_value == 21:
                    player.push_hand()
                else:
                    player.lose_hand()

        # dealer does not have natural, players take turns
        else:
            for player in player_list:
                player.prompt_move() 
                print("-" * 70)   
             
            # dealer turn
            dealer.show_hand()
            while dealer.hand_value[0] < 17 and not dealer.bust:
                dealer.hit()
                dealer.show_hand()
            input("\nPress Enter to continue...")
            print()

            # resolve player wagers after dealer turn
            for player in player_list:
                if dealer.bust and not player.bust:
                    player.win_hand()
                elif not player.bust:
                    if player.hand_value[0] > dealer.hand_value[0]:
                        player.win_hand()
                    elif player.hand_value[0] == dealer.hand_value[0]:
                        player.push_hand()
                    else:
                        player.lose_hand()

            # reset player bust
            for player in player_list:
                player.bust = False

        # print players after turn resolution
        for player in player_list:
            player.print_player()

        # exit player from game if cash is 0, prompt player if they would like to exit
        for i in range(0, len(player_list)):
            player_list[i].print_player()
            if player_list[i].play_cash == 0:
                input("{}, you have run out of money, you must leave the table.".format(player_list[i].name))
                player_quit_list.append(i)
            else:
                player_quit_input = input("{}, Press Enter to continue,\nor input '1' if you would like to quit... ".format(player_list[i].name))
                if player_quit_input.strip().lower() in ["1", "q", "quit", "exit", "leave", "done"]:
                    player_quit_list.append(i)
                    input("\nThank you for playing {}, goodbye.\n".format(player_list[i].name))
        if player_quit_list != []:
            for i in player_quit_list.reverse():
                player_list.pop(i)   
        player_quit_list = []


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

# TODO: add messages to win, lose, push
# TODO: write display_rules function
# TODO: update printing and hitting and card dict to accomodate suit

# TODO: write change_settings function
# TODO: Add options for double down and split
# TODO: payout rate changes in win for blackjack vs not


#UP: menu layout in main
#UP: player print function
