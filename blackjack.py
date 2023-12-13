# CPE 551-WS Fall 2023
# Ryan Potenza
# Final Project
#
# This program creates blackjack to be played from the terminal
# Basic rules of blackjack will apply
# 2 Decks will be played by default, dealer stands on 17 or above, no double down after hitting. 
# Blackjack pays 3-2 (Only if your first 2 cards add to 21, reaching 21 after hitting only counts as a win)
# 
# An additional feature to this card game is a card counting trainer. The point of this trainer is to display 
# the count at the end of each hand, so that you can stay on top of the count and adjust your strategies accordingly
# additionally, you have control of how many decks are to be played in the game -- so that you have additional
# flexibility when tailoring your practice environment.
# 
#
# How to play: When prompted with menu, press 1 to begin playing. Each session starts with a default 500$. Options offered are hit, stand, double down.
# To enable/disable card count assist, press 2 in the main menu, it is off by default.
# To change the number of decks being played, press 3 in the menu and then enter the number of desired decks.
# Current features that are left out of this game:
# Splitting
# Saving state outside out each session
# Surrendering 
# Side bets

import random
import os

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def __str__(self):
        return f"{self.val}"

class Deck:
    def __init__(self):
        self.suits = ['H', 'D', 'C', 'S']
        self.vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.count = 0 # Initialize count
        self.decks = 2 # Change this parameter to change the number of decks in play
        self.cards = self.generate_deck()
    
    # When the deck is "suffled" the object will be completely reset
    def generate_deck(self):
        self.cards = [Card(suit, val) for _ in range(self.decks) for suit in self.suits for val in self.vals]
        self.count = 0
        random.shuffle(self.cards)
        print(f"\nShuffled deck of {len(self.cards)} cards and {self.decks} decks. Set count to {self.count}")
        return self.cards
        

    def draw_card(self):
        # Check for empty deck and pop a card from the deck
        if not self.cards: 
            self.cards = self.generate_deck()
        card = self.cards.pop()
        
        # Logic for count -- 2-6 increases the count by 1, 7-9 doesn't change the count (hence it is left out of logic), 10-A decreases by 1
        if card.val in ['2','3','4','5','6']: 
            self.count += 1
        if card.val in ['10','J','Q','K','A']:
            self.count -= 1

        return card

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.bet = 0
        self.balance = 500 # Starting balance of $500

    def add_card(self, card):
        self.cards.append(card)
        self.update_value()

    def update_value(self):
        self.value = sum(self.get_card_value(card) for card in self.cards)
        if self.value > 21 and any(card.val == 'A' for card in self.cards):
            self.value -= 10

    def get_card_value(self, card):
        if card.val == 'A': #LOGIC FOR ACE
            return 11
        else:
            vals = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, "J": 10, "Q": 10, "K": 10}
            return vals[card.val]

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.countflag = 1 # Count display is off when countflag == 1, default

    def place_bet(self):
        while True:
            os.system('cls')
            print(f"Balance: ${self.player_hand.balance}")
            try:
                bet = int(input("Enter your bet: $"))
                if bet < 1: # Bet must be a posititve number and at least 1$
                    print("Invalid bet: Must bet at least 1$") 
                if bet <= self.player_hand.balance:  # Make sure player has enough money to play
                    self.player_hand.bet = bet
                    break
                else:
                    print("Invalid bet: Insufficient Funds")
                
            except ValueError:
                print("Invalid input: Please enter a valid number.")

    def deal_initial_cards(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.draw_card())
            self.dealer_hand.add_card(self.deck.draw_card())

    def player_turn(self):
        while self.player_hand.value < 21:
            print(f"\nYour cards: {[str(card) for card in self.player_hand.cards]}, current value: {self.player_hand.value}")
            print(f"\nDealer showing: {self.dealer_hand.cards[0]}")
            action = input("Press: \n1: Stand\n2: Hit\n3: Double Down\n")
            if action == "1":
                break
            elif action == "2":
                self.player_hand.add_card(self.deck.draw_card())
                while self.player_hand.value < 21:
                    print(f"\nYour cards: {[str(card) for card in self.player_hand.cards]}, current value: {self.player_hand.value}")
                    print(f"\nDealer showing: {self.dealer_hand.cards[0]}")
                    action2 = input("Press \n1: Stand\n2: Hit\n")
                    if action2 == "1":
                        break
                    elif action2 == "2":
                        self.player_hand.add_card(self.deck.draw_card())
                        continue
                    else:
                        print("Misinput: Standing")
                        break
                break

            elif action == "3":
                if self.player_hand.balance - self.player_hand.bet*2 >= 0:
                    self.player_hand.add_card(self.deck.draw_card())
                    self.player_hand.bet *= 2
                else:
                    print("Error: Insufficient funds to double down!")
                    continue
                break
            else:
                print("Invalid action. Please enter hit, stand, split, or double down.")

    def dealer_turn(self):
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.draw_card())

    def display_final_result(self):
        os.system('cls')
        print(f"\nYour final hand: {[str(card) for card in self.player_hand.cards]}, final value: {self.player_hand.value}")
        print(f"Dealer's final hand: {[str(card) for card in self.dealer_hand.cards]}, final value: {self.dealer_hand.value}")
        if self.countflag == 0:
            print(f"\nCount is: {self.deck.count}")

        if self.player_hand.value == 21 and len(self.player_hand.cards) == 2:
            print(f"Blackjack!: Win {(3*self.player_hand)/2}")
        if self.player_hand.value > 21:
            print(f"You bust: Lose ${self.player_hand.bet}")
            return -self.player_hand.bet
        elif self.dealer_hand.value > 21:
            print(f"Dealer bust: Win ${self.player_hand.bet}")
            return self.player_hand.bet
        elif self.player_hand.value > self.dealer_hand.value:
            print(f"Win ${self.player_hand.bet}")
            return self.player_hand.bet
        elif self.player_hand.value < self.dealer_hand.value:
            print(f"Lose ${self.player_hand.bet}")
            return -self.player_hand.bet
        else:
            print("Push, bet returned")
            return 0
        
    def clear_table(self):
        self.player_hand.cards = []
        self.dealer_hand.cards = []

    def play(self):
        decision = '0'
        while decision != '4':
            print(f"Welcome to Blackjack!\n\nRules:\nDealer hits below 17 - blackjack pays 3-2\n\nBalance: ${self.player_hand.balance}\n\nOptions:\n1: Play game\n2: Toggle Count helper display\n3: Set # of decks (default 2)\n4: Exit game")
            decision = input("What would you like to do?\n")
            if decision == '1':
                cont = '' # Reset cont flag for case user quits to menu and then resumes playing
                while cont == '':
                    os.system('cls')
                    if self.player_hand.balance == 0:
                        print("Sorry! You are out of cash! Restart the program to start again from scratch, and maybe turn on the count helper this time!")
                        _ = input("Press any key to continue: ")
                        break
                    self.place_bet()
                    if self.countflag == 0:
                        print(f"\nCount is: {self.deck.count}")
                    self.deal_initial_cards()
                    self.player_turn()
                    self.dealer_turn()
                    result = self.display_final_result() # Prints results and returns the amount to be added/subtracted
                    self.clear_table()
                    self.player_hand.balance += result
                    print(f"\nYour current balance: ${self.player_hand.balance}")
                    cont = input("Press enter to continue.\nPress any other key to exit.\n")
                os.system('cls')
            elif decision == '2':
                if self.countflag == 0:
                    self.countflag = 1
                    os.system('cls')
                    print("Count helper is OFF!")
                    _ = input("Press any key to continue: ")
                else:
                    self.countflag = 0
                    os.system('cls')
                    print("Count helper is ON!")
                    _ = input("Press any key to continue: ")
            elif decision == '3':
                deckcount = input("How many decks?: ")
                self.deck.decks = int(deckcount) # Update deck count
                self.deck.cards = self.deck.generate_deck() # Shuffle new deck
                _ = input("Press any key to continue: ")
        print("Exiting game: Thank you!")
                
if __name__ == "__main__":
    game = BlackjackGame()
    game.play()

