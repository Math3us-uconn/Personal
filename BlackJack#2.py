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


if __name__ == "__main__":
    root = tk.Tk()
    BlackjackGame(root)
    root.mainloop()