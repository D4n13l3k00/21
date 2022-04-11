"""
.------.------.------.------.------.------.------.------.------.------.
|D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
| :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
| (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
| '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
`------`------`------`------`------`------`------`------`------`------'
                    Copyright 2022 t.me/D4n13l3k00                     
          Licensed under the Creative Commons CC BY-NC-ND 4.0          
  
                   Full license text can be found at:                  
      https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode      
    
                          Human-friendly one:                          
           https://creativecommons.org/licenses/by-nc-nd/4.0           
"""

import random
from typing import *


class CardBase:
    def __init__(self) -> None:
        self.suits = {
            "H": "❤",
            "D": "♦",
            "C": "♠",
            "S": "♣",
            "JR": "🂿",
            "JB": "🃏",
        }


class Card(CardBase):
    def __init__(self, suit, value):
        super().__init__()
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value}{self.suits[self.suit]}"


class Cards(CardBase):
    def __init__(self, deck_type: Literal['standard', 'joker', 'fool', 'preference', 'thousand'] = 'joker') -> None:
        """
        Create a new deck of cards

        standard: standard 52 card deck
        joker: standard 52 card deck with 2 jokers
        fool: 36 cards (short deck, from sixes to aces)
        preference: 32 cards (small deck, from sevens to aces)
        thousand: 24 cards (from nines to aces)
        """

        super().__init__()
        self.cards = []
        self.deck_type = deck_type
        self.new_cards()

    def new_cards(self) -> None:
        """
        Create a new deck of cards
        """

        self.cards = []
        _values = ['J', 'Q', 'K', 'A']
        _start = 2
        if self.deck_type == 'fool':
            _start = 6
        elif self.deck_type == 'preference':
            _start = 7
        elif self.deck_type == 'thousand':
            _start = 9
        for suit in ['C', 'D', 'H', 'S']:
            self.cards.extend(Card(suit, value)
                              for value in list(range(_start, 11)) + _values)

        if self.deck_type == 'joker':
            self.cards.extend([Card('JR', 'JK'), Card('JB', 'JK')])

    @property
    def has_jokers(self) -> bool:
        """
        Return True if the hand has any jokers
        :return: A boolean value.
        """

        return any(card.value == 'JK' for card in self.cards)

    @property
    def cards_left(self) -> int:
        """
        Return the number of cards left in the deck
        :return: The number of cards left in the deck.
        """

        return len(self.cards)

    def shuffle(self) -> None:
        """
        Shuffle the cards in the deck
        """
        random.shuffle(self.cards)

    def pick_card(self, random_card: bool = True, remove_card_from_deck: bool = True) -> Card:
        """
        Pick a random card from the deck

        :param random_card: If True, the card will be picked randomly from the deck. If False, the first
        card in the deck will be picked, defaults to True
        :type random_card: bool (optional)
        :param remove_card_from_deck: If True, the card will be removed from the deck. If False, the
        card will remain in the deck, defaults to True
        :type remove_card_from_deck: bool (optional)
        :return: A card object.
        """

        if self.cards_left == 0:
            raise ValueError("No cards left in the deck")
        card = random.choice(self.cards) if random_card else self.cards[0]
        if remove_card_from_deck:
            self.cards.remove(card)
        return card

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
