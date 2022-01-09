
# Defining different variables

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Defining a variable to indicate if the game is on
playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_cards = ' '
        for card in self.deck:
            deck_cards += '\n' + card.__str__()
        return "The deck has: " + deck_cards

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, new_card):
        self.cards.append(new_card)
        self.value += values[new_card.rank]
        if new_card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self, chip):
        self.total = chip # Setting the default initial chips of the player
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            print(f"You have {chips.total} chips.")
            chips.bet = int(input("Enter the number of chips you want to bet: "))

        except ValueError:
            print("You didn't enter valid integer! ")

        else:
            if chips.bet <= chips.total:
                print(f'Your bet is {chips.bet} chips.')
                break
            else:
                print("Your bet exceeds your number of chips!")


def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing
    while True:

        x = input("Do you want to hit or stand? ")

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player Stands, Dealer's turn!")
            playing = False

        else:
            print("Please enter h or s only!")
            continue
        break


def show_some(player, dealer):

    # show one of dealer's cards
    print("\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])

    # show all of player's cards
    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)


def show_all(player, dealer):

    # show all of dealer's hand
    print("\n Dealer's Hand: ")
    for card in dealer.cards:
        print(card)

    # showing value of dealer's cards
    print(f"Value of dealer's card is: {dealer.value}")

    # show all of player's cards
    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)

    # showing value of player's cards
    print(f"Value of player's card is: {player.value}")


def player_busts(chips):

    print("PLAYER BUSTS!")
    print("DEALER WINS!")
    chips.lose_bet()


def player_wins(chips):

    print("PLAYER WINS!")
    print("DEALER LOSES!")
    chips.win_bet()


def dealer_busts (chips):

    print("DEALER BUSTS!")
    print("PLAYER WINS!")
    chips.win_bet()


def dealer_wins(chips):

    print("DEALER WINS!")
    print("PLAYER LOSES!")
    chips.lose_bet()


def push():
    print("Dealer and Player TIE!")

chip = 100
# GAME LOGIC
while True:

    print("\n")
    print("<<<<<<<<<<<<<<<<<<< WELCOME TO BLACKJACK >>>>>>>>>>>>>>>>>>>")
    print("\n")
    print("<<<<<<<<<<<<<<<<<<<<<<< RULES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("1. Try to reach as close to 21 without going over!")
    print("2. Dealer hits until they reach players value.")



    # Creating a deck
    deck = Deck()

    # Shuffling the deck
    deck.shuffle()

    # Setting up player's hand
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # Setting up dealer's hand
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Setting up player's chips
    player_chips = Chips(chip)

    # Taking player's bet
    take_bet(player_chips)

    # Showing all player cards but only one dealer card
    show_some(player_hand, dealer_hand)

    # Player's turn
    while playing:

        # Prompt player to hit or stand
        hit_or_stand(deck, player_hand)

        # show player cards, keep one dealer card hidden
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_chips)
            break

        if player_hand.value == 21:
            print("Hooray! you reached 21!")
            break

    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)

        # show all cards
        show_all(player_hand, dealer_hand)

        # Running different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            push()

    # Informing Player of their chips
    print("\n Player's total chips are: {}".format(player_chips.total))

    # Asking if they want to continue
    new_game = input("Would you like to play again? ")

    if new_game[0].lower() == 'y':
        playing = True
        chip = player_chips.total
        continue
    else:
        print("THANK YOU FOR PLAYING!")

        break