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

def format_hand(hand: list[cards_lib.Card]) -> str:
    return ", ".join(map(str, hand))

def safe_pick(deck: cards_lib.Cards) -> cards_lib.Card | None:
    try:
        return deck.pick_card()
    except ValueError:
        return None

def play_solo(deck: cards_lib.Cards) -> None:
    deck.new_cards()
    deck.shuffle()

    try:
        hand = [deck.pick_card() for _ in range(2)]
    except ValueError:
        con.print("[red]Deck is empty. Restarting...[/]")
        wait()
        return

    while True:
        con.print("•", format_hand(hand), style="cyan")
        score = count_score(hand)
        con.print(f"[cyan]• Your score: {score}[/]")
        con.print(f"[cyan]• Cards left: {deck.cards_left}[/]")

        if score > 21:
            con.print("[red]You lose![/]")
            wait()
            return
        if score == 21:
            con.print("[green]You win![/]")
            wait()
            return

        if Prompt.ask("[green]Pick a card?[/]", choices=["y", "n"], default="y") != "y":
            con.print("[green]The end[/]")
            wait()
            return

        card = safe_pick(deck)
        if card is None:
            con.print("[yellow]No cards left in the deck.[/]")
            wait()
            return
        hand.append(card)

def play_vs_dealer(deck: cards_lib.Cards) -> None:
    """
    Virtual dealer mode (blackjack-like):
    - player and dealer start with 2 cards
    - player hits/stands
    - dealer draws until score >= 17
    - closest to 21 wins (without busting)
    """
    deck.new_cards()
    deck.shuffle()

    try:
        player = [deck.pick_card() for _ in range(2)]
        dealer = [deck.pick_card() for _ in range(2)]
    except ValueError:
        con.print("[red]Deck is empty. Restarting...[/]")
        wait()
        return

    # Player turn
    while True:
        con.print(f"[magenta]• Dealer: {dealer[0]}, ??[/]")
        con.print("•", format_hand(player), style="cyan")
        p_score = count_score(player)
        con.print(f"[cyan]• Your score: {p_score}[/]")
        con.print(f"[cyan]• Cards left: {deck.cards_left}[/]")

        if p_score > 21:
            con.print("[red]You bust. Dealer wins.[/]")
            con.print(f"[magenta]• Dealer hand: {format_hand(dealer)} ({count_score(dealer)})[/]")
            wait()
            return
        if p_score == 21:
            break

        if Prompt.ask("[green]Pick a card?[/]", choices=["y", "n"], default="y") != "y":
            break

        card = safe_pick(deck)
        if card is None:
            con.print("[yellow]No cards left in the deck.[/]")
            wait()
            return
        player.append(card)

    # Dealer turn
    con.print(f"[magenta]• Dealer hand: {format_hand(dealer)}[/]")
    while True:
        d_score = count_score(dealer)
        if d_score >= 17:
            break
        card = safe_pick(deck)
        if card is None:
            break
        dealer.append(card)
        con.print(f"[magenta]• Dealer picks: {card}[/]")

    # Result
    p_score = count_score(player)
    d_score = count_score(dealer)
    con.print(f"[cyan]• Your final: {format_hand(player)} ({p_score})[/]")
    con.print(f"[magenta]• Dealer final: {format_hand(dealer)} ({d_score})[/]")

    if p_score > 21:
        con.print("[red]You lose.[/]")
    elif d_score > 21:
        con.print("[green]Dealer busts. You win![/]")
    elif p_score > d_score:
        con.print("[green]You win![/]")
    elif p_score < d_score:
        con.print("[red]You lose.[/]")
    else:
        con.print("[yellow]Draw.[/]")
    wait()

def main() -> None:
    deck = cards_lib.Cards("standard")
    while True:
        con.clear()
        banner()
        con.print("21: Card game")
        if Prompt.ask("[green]Start game?[/]", choices=["y", "n"], default="y") != "y":
            continue

        mode = Prompt.ask(
            "[green]Mode[/] ([cyan]solo[/] / [magenta]dealer[/])",
            choices=["solo", "dealer"],
            default="dealer",
        )
        con.clear()
        banner()
        if mode == "solo":
            play_solo(deck)
        else:
            play_vs_dealer(deck)


if __name__ == "__main__":
    main()
            
