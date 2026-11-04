import tkinter as tk
from tkinter import messagebox
import random

# Rangordnung: 10=Feldmarschall, 9=General, 8=Oberst, 7=Major, 6=Hauptmann,
# 5=Leutnant, 4=Unteroffizier, 3=Mineur, 2=Aufklärer, 1=Spion
# B=Bombe, F=Fahne
PIECES_COUNT = {
    '10': 1, '9': 1, '8': 2, '7': 3, '6': 4, '5': 4,
    '4': 4, '3': 5, '2': 8, '1': 1, 'B': 6, 'F': 1
}

class Piece:
    def __init__(self, rank, color):
        self.rank = rank
        self.color = color

    def is_movable(self):
        return self.rank not in ['B', 'F']

class StrategoGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stratego - Hotseat Multiplayer")
        self.geometry("650x700")
        self.board_size = 10
        self.cell_size = 60
        self.canvas = tk.Canvas(self, width=600, height=600, bg='#a2d149')
        self.canvas.pack(pady=10)
        self.info_label = tk.Label(self, text="", font=("Arial", 14, "bold"))
        self.info_label.pack()

        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        # Seen in der Mitte
        self.lakes = [(4,2),(4,3),(5,2),(5,3), (4,6),(4,7),(5,6),(5,7)]
        self.current_player = 'Rot' # Rot beginnt (Regel)
        self.state = 'intermission' # 'intermission', 'select', 'move'
        self.selected_pos = None

        self.setup_board()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def setup_board(self):
        def get_random_pieces(color):
            pieces = []
            for rank, count in PIECES_COUNT.items():
                pieces.extend([Piece(rank, color) for _ in range(count)])
            random.shuffle(pieces)
            return pieces

        blue_pieces = get_random_pieces('Blau')
        red_pieces = get_random_pieces('Rot')

        # Blau oben (Reihen 0-3), Rot unten (Reihen 6-9)
        i = 0
        for r in range(4):
            for c in range(10):
                self.board[r][c] = blue_pieces[i]
                i += 1

        i = 0
        for r in range(6, 10):
            for c in range(10):
                self.board[r][c] = red_pieces[i]
                i += 1

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(self.board_size):
            for c in range(self.board_size):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                if (r, c) in self.lakes:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#3b82f6', outline='black')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#a2d149', outline='gray')

                piece = self.board[r][c]
                if piece and self.state != 'intermission':
                    color_hex = '#ef4444' if piece.color == 'Rot' else '#2563eb'
                    if piece.color == self.current_player:
                        # Eigene Figuren aufdecken
                        self.canvas.create_rectangle(x1+4, y1+4, x2-4, y2-4, fill=color_hex, outline='black', width=2)
                        self.canvas.create_text(x1+30, y1+30, text=piece.rank, fill='white', font=('Arial', 14, 'bold'))
                    else:
                        # Gegnerische Figuren verdecken
                        self.canvas.create_rectangle(x1+4, y1+4, x2-4, y2-4, fill=color_hex, outline='black', width=2)
                        # Optional: Logo/Rückseite andeuten
                        self.canvas.create_text(x1+30, y1+30, text="S", fill='black', font=('Arial', 14))

        if self.selected_pos:
            r, c = self.selected_pos
            x1, y1 = c * self.cell_size, r * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='yellow', width=4)

        if self.state == 'intermission':
            self.canvas.create_rectangle(0, 0, 600, 600, fill='#333333')
            self.canvas.create_text(300, 250, text=f"Spieler {self.current_player} ist dran.", font=('Arial', 24, 'bold'), fill='white')
            self.canvas.create_text(300, 300, text="Klicke hier, um deine Figuren zu sehen", font=('Arial', 14), fill='lightgray')
            self.info_label.config(text="Bildschirm verdeckt - Spielerwechsel")
        else:
            self.info_label.config(text=f"Am Zug: Spieler {self.current_player}")

    def on_click(self, event):
        if self.state == 'intermission':
            self.state = 'select'
            self.draw_board()
            return

        c = event.x // self.cell_size
        r = event.y // self.cell_size

        if not (0 <= r < self.board_size and 0 <= c < self.board_size):
            return

        if self.state == 'select':
            piece = self.board[r][c]
            if piece and piece.color == self.current_player and piece.is_movable():
                self.selected_pos = (r, c)
                self.state = 'move'
                self.draw_board()
        elif self.state == 'move':
            if self.selected_pos == (r, c):
                self.selected_pos = None
                self.state = 'select'
                self.draw_board()
            elif self.is_valid_move(self.selected_pos, (r, c)):
                self.execute_move(self.selected_pos, (r, c))
            else:
                piece = self.board[r][c]
                if piece and piece.color == self.current_player and piece.is_movable():
                    self.selected_pos = (r, c)
                    self.draw_board()

    def is_valid_move(self, start, end):
        sr, sc = start
        er, ec = end

        if (er, ec) in self.lakes: return False
        piece = self.board[sr][sc]
        target = self.board[er][ec]

        if target and target.color == piece.color:
            return False # Darf keine eigenen Figuren schlagen

        # Aufklärer (2) dürfen orthogonal über freie Felder springen
        if piece.rank == '2':
            if sr != er and sc != ec: return False
            dr = 1 if er > sr else (-1 if er < sr else 0)
            dc = 1 if ec > sc else (-1 if ec < sc else 0)
            cr, cc = sr + dr, sc + dc
            while (cr, cc) != (er, ec):
                if self.board[cr][cc] is not None or (cr, cc) in self.lakes:
                    return False
                cr += dr
                cc += dc
            return True
        else:
            # Normale Figuren ziehen 1 Feld orthogonal
            if abs(sr - er) + abs(sc - ec) != 1:
                return False
            return True

    def execute_move(self, start, end):
        sr, sc = start
        er, ec = end
        attacker = self.board[sr][sc]
        defender = self.board[er][ec]

        if defender:
            msg = f"Angriff! Dein {attacker.rank} greift {defender.rank} an.\n"
            win = False
            draw = False

            if defender.rank == 'F':
                msg += "Die Fahne wurde erobert! DU GEWINNST!"
                messagebox.showinfo("Sieg", msg)
                self.quit()
                return
            elif defender.rank == 'B':
                if attacker.rank == '3':
                    win = True
                    msg += "Dein Mineur hat die Bombe erfolgreich entschärft!"
                else:
                    msg += "BUMM! Deine Figur ist in die Luft geflogen."
            elif attacker.rank == '1' and defender.rank == '10':
                win = True
                msg += "Spion greift an! Der gegnerische Feldmarschall ist geschlagen!"
            else:
                val_a = int(attacker.rank)
                val_d = int(defender.rank)
                if val_a > val_d:
                    win = True
                    msg += "Deine Figur ist stärker! Gegner geschlagen."
                elif val_a == val_d:
                    draw = True
                    msg += "Gleicher Rang! Beide Figuren scheiden aus."
                else:
                    msg += "Gegnerische Figur ist stärker. Du verlierst."

            messagebox.showinfo("Kampfbericht", msg)

            if win:
                self.board[er][ec] = attacker
                self.board[sr][sc] = None
            elif draw:
                self.board[er][ec] = None
                self.board[sr][sc] = None
            else:
                self.board[sr][sc] = None
        else:
            self.board[er][ec] = attacker
            self.board[sr][sc] = None

        self.selected_pos = None
        self.current_player = 'Blau' if self.current_player == 'Rot' else 'Rot'

        # Gewinnprüfung: Kann der aktuelle Spieler noch ziehen?
        if not self.has_movable_pieces(self.current_player):
            winner = 'Rot' if self.current_player == 'Blau' else 'Blau'
            messagebox.showinfo("Sieg", f"Spieler {self.current_player} kann sich nicht mehr bewegen.\n{winner} gewinnt!")
            self.quit()
            return

        self.show_intermission()

    def has_movable_pieces(self, color):
        for r in range(self.board_size):
            for c in range(self.board_size):
                p = self.board[r][c]
                if p and p.color == color and p.is_movable():
                    # Wir könnten hier noch prüfen, ob die Figur legal ziehen kann (nicht komplett blockiert),
                    # aber für diese Basisfassung reicht es, bewegliche Einheiten zu haben.
                    return True
        return False

    def show_intermission(self):
        self.state = 'intermission'
        self.draw_board()

if __name__ == '__main__':
    app = StrategoGame()
    app.mainloop()
