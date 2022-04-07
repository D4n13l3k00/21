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

from typing import *

from rich.console import Console
from rich.markup import escape
from rich.prompt import Prompt

import cards

con = Console()
c = cards.Cards('standart')


def count_score(cards: List[cards.Card]) -> int:
    _vals = {
        'J': 2,
        'Q': 3,
        'K': 4,
    }
    score = 0
    for crd in cards:
        if crd.value == 'A':
            score += 11 if score > 10 else 1
        elif crd.value in ['J', 'Q', 'K']:
            score += _vals[crd.value]
        else:
            score += int(crd.value)
    return score

def banner() -> None:
    b = """.------..------.
|2.--. ||1.--. |
| (\/) || :/\: |
| :\/: || (__) |
| '--'2|| '--'1|
`------'`------'"""
    con.print(f"[green b]{escape(b)}[/]")

def wait() -> None:
    con.input("[yellow]Press any key to continue...[/]")

while True:
    con.clear()
    banner()
    con.print("21: Card game")
    if Prompt.ask("[green]Start game?[/]", choices=['y', 'n'], default='y') == 'y':
        c.new_cards()
        c.shuffle()
        ur_cards = [c.pick_card() for _ in range(2)]
        while True:
            con.print('•', ', '.join(map(str, ur_cards)), style="cyan")
            con.print(f"[cyan]• Your score: {count_score(ur_cards)}[/]")
            con.print(f"[cyan]• Cards left: {c.cards_left}[/]")
            if Prompt.ask("[green]Pick a card?[/]", choices=['y', 'n'], default='y') == 'y':
                card = c.pick_card()
                ur_cards.append(card)
                score = count_score(ur_cards)
                if score > 21:
                    con.print(f"[red]You lose! The fatal card was {card}[/]")
                    wait()
                    break
                elif score == 21:
                    con.print(f"[green]You win! The winning card was {card}[/]")
                    wait()
                    break
            else:
                con.print("[green]The end[/]")
                wait()
                break
            
