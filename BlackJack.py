import os
import random
import tkinter as tk


class BlackjackGame:
    def __init__(self, root):
        self.root = root
        root.title("Blackjack")
        root.geometry("520x430")
        root.resizable(False, False)
        root.configure(bg="#075b43")
        self.deck = []
        self.player = []
        self.dealer = []
        self.finished = True

        tk.Label(root, text="BLACKJACK", font=("Arial", 24, "bold"),
                 fg="#f5d76e", bg="#075b43").pack(pady=12)
        tk.Label(root, text="DEALER", font=("Arial", 13, "bold"),
                 fg="white", bg="#075b43").pack()
        self.dealer_view = tk.Label(root, font=("Arial", 22), height=2,
                                    fg="white", bg="#075b43")
        self.dealer_view.pack()
        self.dealer_total = tk.Label(root, fg="white", bg="#075b43")
        self.dealer_total.pack()
        self.status = tk.Label(root, text="Press Deal to start.", font=("Arial", 13),
                               fg="#f5d76e", bg="#075b43", height=2)
        self.status.pack(pady=8)
        tk.Label(root, text="YOUR HAND", font=("Arial", 13, "bold"),
                 fg="white", bg="#075b43").pack()
        self.player_view = tk.Label(root, font=("Arial", 22), height=2,
                                    fg="white", bg="#075b43")
        self.player_view.pack()
        self.player_total = tk.Label(root, fg="white", bg="#075b43")
        self.player_total.pack()

        controls = tk.Frame(root, bg="#075b43")
        controls.pack(pady=18)
        self.deal_button = tk.Button(controls, text="Deal", width=10, command=self.deal)
        self.deal_button.pack(side=tk.LEFT, padx=5)
        self.hit_button = tk.Button(controls, text="Hit", width=10, command=self.hit,
                                    state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT, padx=5)
        self.stand_button = tk.Button(controls, text="Stand", width=10, command=self.stand,
                                      state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT, padx=5)

    def new_deck(self):
        self.deck = [(rank, suit) for suit in "♠♥♦♣"
                     for rank in ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")]
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop()

    @staticmethod
    def score(hand):
        total = sum(11 if rank == "A" else 10 if rank in ("J", "Q", "K") else int(rank)
                    for rank, _ in hand)
        aces = sum(rank == "A" for rank, _ in hand)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    @staticmethod
    def display(hand):
        return "   ".join(f"[{rank}{suit}]" for rank, suit in hand)

    def update(self, reveal=True):
        self.player_view.config(text=self.display(self.player))
        self.player_total.config(text=f"Score: {self.score(self.player)}")
        shown = self.dealer if reveal else self.dealer[:1]
        self.dealer_view.config(text=self.display(shown) + ("   [?]" if not reveal else ""))
        self.dealer_total.config(text=f"Score: {self.score(self.dealer) if reveal else '?'}")

    def deal(self):
        self.new_deck()
        self.player = [self.draw(), self.draw()]
        self.dealer = [self.draw(), self.draw()]
        self.finished = False
        self.deal_button.config(state=tk.DISABLED)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.status.config(text="Your move: hit or stand.")
        self.update(reveal=False)
        if self.score(self.player) == 21:
            self.stand()

    def hit(self):
        if self.finished:
            return
        self.player.append(self.draw())
        self.update(reveal=False)
        if self.score(self.player) > 21:
            self.finish("You bust! Dealer wins.")

    def stand(self):
        if self.finished:
            return
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.status.config(text="Dealer's turn…")
        self.root.after(400, self.dealer_turn)

    def dealer_turn(self):
        if self.score(self.dealer) < 17:
            self.dealer.append(self.draw())
            self.update()
            self.root.after(400, self.dealer_turn)
            return
        player_score, dealer_score = self.score(self.player), self.score(self.dealer)
        if dealer_score > 21:
            result = "Dealer busts! You win!"
        elif player_score > dealer_score:
            result = "You win!"
        elif player_score < dealer_score:
            result = "Dealer wins."
        else:
            result = "It's a tie!"
        self.finish(result)

    def finish(self, result):
        self.finished = True
        self.update()
        self.status.config(text=result)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.deal_button.config(state=tk.NORMAL, text="Play again")


def create_deck():
    deck = [(rank, suit) for suit in "♠♥♦♣" for rank in ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")]
    random.shuffle(deck)
    return deck


def card_value(rank):
    if rank == "A":
        return 11
    if rank in ("J", "Q", "K"):
        return 10
    return int(rank)


def score(hand):
    total = sum(card_value(rank) for rank, _ in hand)
    aces = sum(1 for rank, _ in hand if rank == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def format_card(card, hidden=False):
    rank, suit = card if not hidden else ("?", "?")
    top = "┌─────┐"
    if hidden:
        middle = "│ ??  │"
    else:
        middle = f"│ {rank}{suit}  │"
    bottom = "├─────┤"
    body = [top, middle, bottom]
    return body


def display_hand(hand, hide_dealer=False):
    if hide_dealer and len(hand) > 1:
        cards = []
        for i, card in enumerate(hand):
            if i == 0:
                cards.append(format_card(card, hidden=False))
            else:
                cards.append(format_card(card, hidden=True))
        return cards

    cards = [format_card(card) for card in hand]
    return cards


def print_scoreboard(stats):
    print("\n┌──────────────────────────────────────┐")
    print("│         CASINO SCOREBOARD           │")
    print("├──────────────────────────────────────┤")
    print(f"│ WINS: {stats['wins']:>3}   LOSSES: {stats['losses']:>3}   TIES: {stats['ties']:>3} │")
    print("└──────────────────────────────────────┘")


def print_banner():
    print("\n" + "═" * 52)
    print("              HIGH ROLLERS CASINO")
    print("                  BLACKJACK")
    print("═" * 52)


def print_table_state(dealer, player, reveal_dealer=False, stats=None):
    if stats is not None:
        print_scoreboard(stats)

    print("\nDEALER")
    dealer_cards = display_hand(dealer, hide_dealer=not reveal_dealer)
    for line_index in range(3):
        line = "  ".join(card[line_index] for card in dealer_cards)
        print(f"  {line}")
    if reveal_dealer:
        print(f"  TOTAL: {score(dealer)}")

    print("\nPLAYER")
    player_cards = display_hand(player)
    for line_index in range(3):
        line = "  ".join(card[line_index] for card in player_cards)
        print(f"  {line}")
    print(f"  TOTAL: {score(player)}\n")


def print_menu():
    print("┌────────────────────────────────────────┐")
    print("│   [H]IT   [S]TAND   [Q]UIT           │")
    print("└────────────────────────────────────────┘")
    print("─" * 52)


def play_console_game():
    stats = {"wins": 0, "losses": 0, "ties": 0}
    print_banner()
    print("Welcome to the table. Place your bets and play.\n")

    while True:
        deck = create_deck()
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]

        print_table_state(dealer, player, reveal_dealer=False, stats=stats)
        print_menu()

        while True:
            choice = input("Your move: ").strip().lower()
            if choice in ("q", "quit"):
                print("\nCasino closing. Thanks for playing!\n")
                return
            if choice not in ("h", "hit", "s", "stand"):
                print("Please enter 'h' or 's'.")
                continue

            if choice in ("h", "hit"):
                player.append(deck.pop())
                print(f"\nDealer deals: {player[-1][0]}{player[-1][1]}")
                print_table_state(dealer, player, reveal_dealer=False, stats=stats)
                if score(player) > 21:
                    stats["losses"] += 1
                    print("\nPLAYER BUST! Dealer wins the hand.")
                    print("─" * 52)
                    break
                print_menu()
                continue

            if choice in ("s", "stand"):
                while score(dealer) < 17:
                    dealer.append(deck.pop())
                    print(f"Dealer draws: {dealer[-1][0]}{dealer[-1][1]}")

                dealer_total = score(dealer)
                player_total = score(player)
                print_table_state(dealer, player, reveal_dealer=True, stats=stats)

                if dealer_total > 21:
                    print("DEALER BUST! PLAYER WINS!")
                    stats["wins"] += 1
                elif player_total > dealer_total:
                    print("PLAYER WINS!")
                    stats["wins"] += 1
                elif player_total < dealer_total:
                    print("DEALER WINS.")
                    stats["losses"] += 1
                else:
                    print("PUSH — It's a tie!")
                    stats["ties"] += 1

                print("─" * 52)
                break

        again = input("Play another hand? [Y/N]: ").strip().lower()
        if again not in ("y", "yes"):
            print("\nCasino closing. Thanks for playing!\n")
            return
        print_banner()


if __name__ == "__main__":
    if os.environ.get("DISPLAY"):
        root = tk.Tk()
        BlackjackGame(root)
        root.mainloop()
    else:
        play_console_game()
    