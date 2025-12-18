r"""
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

from __future__ import annotations

from rich.console import Console
from rich.markup import escape
from rich.prompt import Prompt

import cards as cards_lib

con = Console()


def count_score(hand: list[cards_lib.Card]) -> int:
    """
    Score rules for "21" (очко):
    - 2..10 are face value
    - J=2, Q=3, K=4
    - A=11, but can be treated as 1 to avoid busting (best score <= 21)
    """
    face_values: dict[str, int] = {"J": 2, "Q": 3, "K": 4}

    total = 0
    aces = 0
    for card in hand:
        if card.value == "A":
            aces += 1
            continue
        if card.value in face_values:
            total += face_values[card.value]
        else:
            total += int(card.value)

    # Count aces as 11, then downgrade to 1 as needed
    total += 11 * aces
    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total

def banner() -> None:
    b = r""".------..------.
|2.--. ||1.--. |
| (\/) || :/\: |
| :\/: || (__) |
| '--'2|| '--'1|
`------'`------'"""
    con.print(f"[green b]{escape(b)}[/]")

def wait() -> None:
    con.input("[yellow]Press any key to continue...[/]")

def main() -> None:
    deck = cards_lib.Cards("standard")
    while True:
        con.clear()
        banner()
        con.print("21: Card game")
        if Prompt.ask("[green]Start game?[/]", choices=["y", "n"], default="y") != "y":
            continue

        deck.new_cards()
        deck.shuffle()

        try:
            hand = [deck.pick_card() for _ in range(2)]
        except ValueError:
            con.print("[red]Deck is empty. Restarting...[/]")
            wait()
            continue

        while True:
            con.print("•", ", ".join(map(str, hand)), style="cyan")
            score = count_score(hand)
            con.print(f"[cyan]• Your score: {score}[/]")
            con.print(f"[cyan]• Cards left: {deck.cards_left}[/]")

            if score > 21:
                con.print("[red]You lose![/]")
                wait()
                break
            if score == 21:
                con.print("[green]You win![/]")
                wait()
                break

            if Prompt.ask("[green]Pick a card?[/]", choices=["y", "n"], default="y") != "y":
                con.print("[green]The end[/]")
                wait()
                break

            try:
                card = deck.pick_card()
            except ValueError:
                con.print("[yellow]No cards left in the deck.[/]")
                wait()
                break
            hand.append(card)


if __name__ == "__main__":
    main()
            
