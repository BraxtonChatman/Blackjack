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
    card_values = dict([(i, i) for i in range(2,11)] + [(11, 10), (12, 10), (13, 10), (1, 11)])

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
        if len(shuffled_deck) < card_remainder_set:
            shuffled_deck += discard_deck
            discard_deck = []

        # choose random card in shuffled_deck
        deck_index = randint(0, len(shuffled_deck)-1)
        new_card = shuffled_deck[deck_index]
        shuffled_deck.pop(deck_index)

        # add new card to hand value list. append if new card is ace
        for i in range(0, len(self.hand_value) - 1):
            self.hand_value[i] += self.card_values[new_card]
        if new_card == 1:
            if i == 0:
                self.hand_value.append(0)
            self.hand_value[1] = self.hand_value[0] - 10
        if len(self.hand_value) == 2 and self.hand_value[0] > 21:
            self.hand_value.pop(0)

        # add new card to hand
        self.hand.append(new_card)

        # lose hand if bust
        if self.hand_value[0] > 21:
            self.bust = True
            self.lose_hand()

    def discard(self):
        """empty hand to discard pile"""
        discard_deck.append(self.hand.pop())

    def stay(self):
        """pass turn to next player"""
        self.stayed = True

    def split(self):
        """separate matching cards to multiple hands"""
        pass

    def double_down(self):
        """validate play_cash for double wager_amount and receive one more card"""
        pass

    def make_wager(self):
        """prompt user for wager_amount, validate, and set"""
        print(self.name, "please input the amount you would like to wager for the round: ")
        wager_input = input()
        while not is_int(wager_input) or float(wager_input) < 1 or float(wager_input) > self.play_cash:
            print("\Current cash: ", self.play_cash)
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
        self.wager_amount = int(float(wager_input))
        input("Press Enter to continue...")

    def print_player(self):
        """print player cash, wager, and current hand to screen"""
        pass


class Dealer(Player):
    """class representing dealer in blackjack"""
    def print_dealer(self):
        """print dealer top card while leaving bottom card hidden"""
        pass

    def show_hand(self):
        """print dealer hand"""
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
    dealer = Dealer(0)
    num_players = ""
    player_list = []
    player_quit_list = []
    cash_input = ""
    player_move_input = ""
    player_name_input = ""
    player_quit_input = ""
    wager_input = ""


    # allow selection for number of players from 1 to 7
    print("Please select the number of players that would like to play (1-7): ")
    num_players = input()
    while num_players.strip() not in ['1', '2', '3', '4', '5', '6', '7']:
        print("Please input a valid number of players: ")
        num_players = input()

    # insert cards into shuffled_deck based on number of decks setting
    for i in range(1, 14):
        shuffled_deck += [i] * deck_number_set

    # initialize each Player instance with prompted initial cash value and name into player list
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
    while player_list != []:
       
        # wager prompt and validation loop
        for player in player_list:
            player.make_wager()

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
                player.hit()
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
                for player in player_list:
                    player.stayed = False

            # dealer turn
            dealer.show_hand()
            while dealer.hand_value < 17:
                dealer.hit()
                dealer.show_hand()
            input("Press Enter to continue...")

            # resolve player wagers after dealer turn
            for player in player_list:
                # dealer busts
                if dealer.bust and not player.bust:
                    player.win_hand()
                
                # dealer doesn't bust
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
        for i in range(0, len(player_list)-1):
            player_list[i].print_player()
            if player_list[i].play_cash == 0:
                input("{}, you have run out of money, you must leave the table.".format(player_list[i].name))
                player_quit_list.append(i)
            else:
                player_quit_input = input("{}, Press Enter to continue, or input '1' if you would like to quit...".format(player_list[i].name))
                if player_quit_input.strip().lower() in ["1", "q", "quit", "exit", "leave", "done"]:
                    player_quit_list.append(i)
                    input("Thank you for playing {}.\nPress Enter to continue...".format(player_list[i].name))
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



# TODO: complete player Class methods
# TODO : move deck limit check to hit
# TODO: discard hands in lose, win, push



# TODO: write display_rules function
# TODO: write change_settings function
# TODO: update printing and hitting and card dict to accomodate suit
# TODO: Add options for double down and split

# UPDATE: fix quit option
# UPDATE: edit player hit method to check the deck card remainder limit
# UPDATE: player hit calls lose _hand mrthod if a bust occurs
# UPDATE: player.hit updates hand and bust value
# UPDATE: removed unneseccary Player methods
