# CPE 551-WS Fall 2023
# Ryan Potenza
# Final Project
#
# This program creates blackjack to be played from the terminal
# Basic rules of blackjack will apply
# 8 Decks will be played, dealer stands on 17 or above
# 
# Addiional goal is to add a card counting feature to show the current count in the deck
# to assist players in learning to count cards

import random

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    # Print card suit and value
    def __str__(self):
        return f"{self.val} of {self.suit}"

class Deck:
    def __init__(self, num_decks=8):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        # Create large playing deck of 8 full decks of cards by default. Can change by changing num_decks parameter
        self.cards = [Card(suit, val) for _ in range(num_decks) for suit in suits for val in vals] 

        #Shuffles decks
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)
        self.update_value()

    def update_value(self):
        self.value = sum(self.get_card_value(card) for card in self.cards)
        if self.value > 21 and any(card.val == 'A' for card in self.cards):
            self.value -= 10

    def get_card_value(self, card):
        if card.val in ['J', 'Q', 'K']:
            return 10
        elif card.val == 'A':
            return 11
        else:
            return int(card.val)

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def deal_initial_cards(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.draw_card())
            self.dealer_hand.add_card(self.deck.draw_card())

    def player_turn(self):
        while self.player_hand.value < 21:
            print(f"\nYour cards: {[str(card) for card in self.player_hand.cards]}, current value: {self.player_hand.value}")
            action = input("Do you want to hit or stand? ").lower()
            if action == 'hit':
                self.player_hand.add_card(self.deck.draw_card())
            elif action == 'stand':
                break

    def dealer_turn(self):
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.draw_card())

    def display_final_result(self):
        print(f"\nYour final hand: {[str(card) for card in self.player_hand.cards]}, final value: {self.player_hand.value}")
        print(f"Dealer's final hand: {[str(card) for card in self.dealer_hand.cards]}, final value: {self.dealer_hand.value}")

        if self.player_hand.value > 21:
            print("You went over. You lose!")
        elif self.dealer_hand.value > 21:
            print("Dealer went over. You win!")
        elif self.player_hand.value > self.dealer_hand.value:
            print("You win!")
        elif self.player_hand.value < self.dealer_hand.value:
            print("You lose!")
        else:
            print("It's a draw!")

    def play(self):
        print("Welcome to Blackjack!\n")
        self.deal_initial_cards()
        self.player_turn()
        if self.player_hand.value <= 21:
            self.dealer_turn()
            self.display_final_result()

if __name__ == "__main__":
    game = BlackjackGame()
    game.play()
