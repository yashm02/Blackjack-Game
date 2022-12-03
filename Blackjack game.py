import random

suits=("Spades","Clubs","Hearts","Diamonds")
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:

    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        self.value=values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:

    def __init__(self):
        self.deck=[]

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_comp=''
        for card in self.deck:
            deck_comp+='\n'+card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self,name):
        self.name=name
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value+=values[card.rank]

        if card.rank == "Ace":
            self.aces+=1
    
    def adjust_for_ace(self):
        #IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
        #THEN CHANGE MY ACE TO 1 INSTEAD OF 11
        while self.value >21 and self.aces:
            self.value-=10
            self.aces-=1

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total+=self.bet
    
    def lose_bet(self):
        self.total-=self.bet

def take_bet(chips):

    while True:
        try:
            chips.bet=int(input("How many chips would you like to bet?: "))
        except:
            print("Sorry, please provide an integer")
        else:
            if chips.bet>chips.total:
                print(f"Sorry, you do not have enough money! You have: {chips.total}")
            else:
                break


def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

playing=True
def hit_or_stand(deck,hand):
    global playing

    while True:
        x=input("Hit or Stand? Enter h or s: ")

        if x[0].lower()=='h':
            print("\nAfter betting")
            hit(deck,hand)
        elif x[0].lower()=='s':
            print("\nAfter Standing")
            print(f"{hand.name.capitalize()} Stands, Dealer's Turn")
            playing=False
        else:
            print("Sorry, I did not understand that, please enter h or s only!")
            continue
        
        break

def show_some(player,dealer):
    # Show only one of the dealer's cards
    print("\nDealer's hand:")
    print("Card hidden")
    print(dealer.cards[1])

    # Show all (2 cards) of the player's cards
    print(f"\n{player.name.capitalize()}'s hand:")
    for card in player.cards:
        print(card)
    print()


def show_all(player,dealer):
    #show all the dealer's cards
    print("\nDealer's hand:")
    for card in dealer.cards:
        print(card)
    print()

    #calculate and display value
    print(f"Value of Dealer's hand is: {dealer.value}\n")

    #show all the player's cards
    print(f"{player.name.capitalize()}'s hand:")
    for card in player.cards:
        print(card)
    print()
    
    print(f"Value of {player.name.capitalize()}'s hand is: {player.value}\n")

def player_busts(player,dealer,chips):
    print("Player busts! Dealer wins!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts! Player wins!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print(f"Dealer and {player.name.capitalize()} tie! It's a push.")

while True:
    print('Welcome to BlackJack! \n\nGet as close to 21 as you can without going over!\n\
Dealer hits until she reaches 17. Aces count as 1 or 11.\n')

    deck=Deck()
    deck.shuffle()

    player=Hand(input("Enter your name: "))
    player.add_card(deck.deal())
    player.add_card(deck.deal())

    dealer=Hand("Dealer")
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())

    player_chips=Chips()

    take_bet(player_chips)

    show_some(player,dealer)
    playing =True
    while playing:

        hit_or_stand(deck,player)

        show_some(player,dealer)

        if player.value>21:
            show_all(player,dealer)
            player_busts(player,dealer,player_chips)
            break
    if player.value<=21:

        while dealer.value < 17:
            hit(deck,dealer)

        show_all(player,dealer)

        if dealer.value > 21:
            dealer_busts(player,dealer,player_chips)
        elif dealer.value > player.value:
            dealer_wins(player,dealer,player_chips)
        elif dealer.value < player.value:
            player_wins(player,dealer,player_chips)
        else:
            push(player,dealer)

    print(f"Total chips remaining with {player.name.capitalize()}: {player_chips.total}")
    print()

    new_game=input("Would you like to play another hand? y/n: ")
    
    if new_game[0].lower() == "y":
        playing=True
        continue
    else:
        print("Thank you for playing! ")
        break
