#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deepseek_stratego.py
====================
Stratego für 2 Spieler – implementiert mit tkinter.

Regeln basierend auf der offiziellen Anleitung:
https://www.spiele4us.de/wp-content/uploads/2022/10/original-stratego-3498-gebraucht-g002301420.pdf

Start:  python deepseek_stratego.py
"""

import tkinter as tk
from tkinter import messagebox
import random
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict

# ---------------------------------------------------------------------------
# Konstanten
# ---------------------------------------------------------------------------
BOARD_SIZE = 10
LAKES = {(4, 2), (4, 3), (4, 6), (4, 7),
         (5, 2), (5, 3), (5, 6), (5, 7)}
BLUE_SETUP_ROWS = range(0, 4)      # obere Hälfte
RED_SETUP_ROWS  = range(6, 10)     # untere Hälfte

# (Name, Anzahl, Rang)
PIECE_DEFS = [
    ("Feldmarschall", 1, 10),
    ("General",       1,  9),
    ("Oberst",        2,  8),
    ("Major",         3,  7),
    ("Hauptmann",     4,  6),
    ("Leutnant",      4,  5),
    ("Unteroffizier", 4,  4),
    ("Mineur",        5,  3),
    ("Aufklärer",     8,  2),
    ("Spion",         1,  1),
    ("Bombe",         6,  0),
    ("Fahne",         1, -1),
]


# ---------------------------------------------------------------------------
# Datenmodell
# ---------------------------------------------------------------------------
@dataclass
class Piece:
    name: str
    rank: int
    owner: str
    revealed: bool = False

    def is_movable(self) -> bool:
        return self.name not in ("Bombe", "Fahne")


@dataclass
class GameState:
    board: List[List[Optional[Piece]]] = field(
        default_factory=lambda: [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    )
    current_player: str = "red"
    last_move_from: Optional[Tuple[int, int]] = None
    last_move_to:   Optional[Tuple[int, int]] = None
    two_square_piece:   Optional[Piece] = None   # Figur, die den Zähler „erzeugt“
    two_square_counter: int = 0
    game_over: bool = False


# ---------------------------------------------------------------------------
# Spiellogik
# ---------------------------------------------------------------------------
class StrategoGame:
    def __init__(self):
        self.state = GameState()
        self._place_random_armies()

    # ---- Aufstellung -----------------------------------------------------
    def _make_army(self, owner: str) -> List[Piece]:
        army = []
        for name, count, rank in PIECE_DEFS:
            for _ in range(count):
                army.append(Piece(name, rank, owner))
        return army

    def _place_random_armies(self):
        """Zufällige Aufstellung; die Fahne steht IMMER in der hintersten Reihe."""
        for owner, rows in (("blue", BLUE_SETUP_ROWS), ("red", RED_SETUP_ROWS)):
            army = self._make_army(owner)

            # Fahne separieren
            flag = next(p for p in army if p.name == "Fahne")
            army.remove(flag)

            # Hinterste eigene Reihe: Blau = 0, Rot = 9
            back_row = 0 if owner == "blue" else 9
            flag_pos = (back_row, random.randrange(BOARD_SIZE))
            self.state.board[flag_pos[0]][flag_pos[1]] = flag

            # Restliche Figuren zufällig auf freie Felder
            all_cells = [(r, c) for r in rows for c in range(BOARD_SIZE)]
            remaining = [cell for cell in all_cells if cell != flag_pos]
            random.shuffle(army)
            for piece, (r, c) in zip(army, remaining):
                self.state.board[r][c] = piece

    # ---- Hilfsfunktionen -------------------------------------------------
    def _in_bounds(self, r, c) -> bool:
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def _is_lake(self, r, c) -> bool:
        return (r, c) in LAKES

    def _own_piece(self, r, c) -> Optional[Piece]:
        p = self.state.board[r][c]
        return p if (p and p.owner == self.state.current_player) else None

    # ---- Bewegungsvalidierung -------------------------------------------
    def get_valid_moves(self, r: int, c: int) -> List[Tuple[int, int]]:
        piece = self._own_piece(r, c)
        if not piece or not piece.is_movable() or self.state.game_over:
            return []

        moves: List[Tuple[int, int]] = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        if piece.name == "Aufklärer":
            # Laut Anleitung: Aufklärer zieht beliebig weit in gerader Linie
            # und darf dabei (einmalig) angreifen. Der Zug endet nach dem
            # Angriff – das erzwingt bereits der anschließende Spielerwechsel.
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while self._in_bounds(nr, nc) and not self._is_lake(nr, nc):
                    target = self.state.board[nr][nc]
                    if target is None:
                        moves.append((nr, nc))
                    elif target.owner != piece.owner:
                        moves.append((nr, nc))
                        break                     # nach Angriff ist Schluss
                    else:
                        break                     # eigene Figur blockiert
                    nr += dr
                    nc += dc
        else:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if not self._in_bounds(nr, nc) or self._is_lake(nr, nc):
                    continue
                target = self.state.board[nr][nc]
                if target is None or target.owner != piece.owner:
                    moves.append((nr, nc))

        # Mehr-Feld-Regel: max. 5× hintereinander zwischen zwei Feldern
        # – nur anwenden, wenn dieselbe Figur den Zähler „erzeugt“ hat.
        if (self.state.two_square_piece is piece and
                self.state.last_move_from is not None and
                self.state.last_move_to is not None and
                (r, c) == self.state.last_move_to and
                self.state.last_move_from in moves and
                self.state.two_square_counter >= 5):
            moves = [m for m in moves if m != self.state.last_move_from]

        return moves

    # ---- Zug ausführen ---------------------------------------------------
    def move(self, fr: int, fc: int, tr: int, tc: int) -> Tuple[bool, str]:
        if self.state.game_over:
            return False, "Das Spiel ist bereits beendet."

        piece = self._own_piece(fr, fc)
        if not piece:
            return False, "Keine eigene Figur auf dem Startfeld."
        if not piece.is_movable():
            return False, f"{piece.name} kann nicht bewegt werden."
        if (tr, tc) not in self.get_valid_moves(fr, fc):
            return False, "Ungültiges Zielfeld."

        target = self.state.board[tr][tc]
        msg = ""

        # ---- Bewegung -----------------------------------------------------
        if target is None:
            self.state.board[tr][tc] = piece
            self.state.board[fr][fc] = None
            self._update_two_square_rule(piece, fr, fc, tr, tc)
            msg = f"{piece.name} zog nach ({tr},{tc})."

        # ---- Angriff ------------------------------------------------------
        else:
            piece.revealed = True
            target.revealed = True
            result = self._resolve_attack(piece, target)
            msg = result["message"]

            if result["winner"] == "attacker":
                self.state.board[tr][tc] = piece
                self.state.board[fr][fc] = None
            elif result["winner"] == "defender":
                self.state.board[fr][fc] = None
            else:
                self.state.board[tr][tc] = None
                self.state.board[fr][fc] = None

            self._update_two_square_rule(piece, fr, fc, tr, tc)

            if target.name == "Fahne" and result["winner"] == "attacker":
                self.state.game_over = True
                msg += f"\n🎉 {piece.owner.upper()} hat die Fahne erobert und gewinnt!"

        # Spielerwechsel – Bewegungsunfähigkeit wird NICHT hier geprüft,
        # sondern erst im GUI nach dem Handover-Dialog.
        if not self.state.game_over:
            self.state.current_player = (
                "blue" if self.state.current_player == "red" else "red"
            )

        return True, msg

    def check_current_player_has_moves(self) -> bool:
        """Wird vom GUI erst aufgerufen, wenn der Spieler tatsächlich am Zug ist."""
        return self._has_movable_pieces(self.state.current_player)

    # ---- interne Helfer --------------------------------------------------
    def _update_two_square_rule(self, piece, fr, fc, tr, tc):
        if (self.state.two_square_piece is piece and
                self.state.last_move_from == (tr, tc) and
                self.state.last_move_to == (fr, fc)):
            self.state.two_square_counter += 1
        else:
            # ANDERE Figur zieht → Zähler zurücksetzen
            self.state.two_square_counter = 0
            self.state.two_square_piece = piece
        self.state.last_move_from = (fr, fc)
        self.state.last_move_to = (tr, tc)

    def _resolve_attack(self, attacker: Piece, defender: Piece) -> Dict:
        if defender.name == "Fahne":
            return {"winner": "attacker", "message": "Die Fahne wurde erobert!"}
        if defender.name == "Bombe":
            if attacker.name == "Mineur":
                return {"winner": "attacker",
                        "message": "Der Mineur entschärft die Bombe!"}
            return {"winner": "defender",
                    "message": f"💥 Bumm! {attacker.name} wird von der Bombe zerstört."}
        if attacker.name == "Spion" and defender.name == "Feldmarschall":
            return {"winner": "attacker",
                    "message": "Der Spion besiegt den Feldmarschall!"}
        if attacker.rank > defender.rank:
            return {"winner": "attacker",
                    "message": f"{attacker.name} ({attacker.rank}) schlägt "
                               f"{defender.name} ({defender.rank})."}
        if attacker.rank < defender.rank:
            return {"winner": "defender",
                    "message": f"{defender.name} ({defender.rank}) schlägt "
                               f"{attacker.name} ({attacker.rank})."}
        return {"winner": "both",
                "message": f"Beide Figuren ({attacker.name}) haben denselben "
                           f"Rang und werden entfernt."}

    def _has_movable_pieces(self, owner: str) -> bool:
        saved = self.state.current_player
        self.state.current_player = owner
        try:
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    p = self.state.board[r][c]
                    if p and p.owner == owner and p.is_movable() and self.get_valid_moves(r, c):
                        return True
        finally:
            self.state.current_player = saved
        return False


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
class StrategoGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Stratego – 2 Spieler")
        self.root.resizable(False, False)

        self.game = StrategoGame()
        self.selected: Optional[Tuple[int, int]] = None
        self.valid_targets: List[Tuple[int, int]] = []

        self._build_widgets()
        self._refresh_board()

    # ---- Aufbau ----------------------------------------------------------
    def _build_widgets(self):
        self.status_var = tk.StringVar()
        status = tk.Label(self.root, textvariable=self.status_var,
                          font=("Arial", 12, "bold"), bg="#222", fg="white",
                          anchor="w", padx=8)
        status.pack(fill=tk.X)
        self.status_var.set("Rot beginnt. Klicke eine eigene Figur an.")

        # board_frame wird als Instanzvariable gespeichert,
        # damit das Handover-Fenster exakt darüber gelegt werden kann.
        self.board_frame = tk.Frame(self.root, bg="#333")
        self.board_frame.pack(padx=6, pady=6)

        self.buttons: List[List[tk.Button]] = []
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.board_frame, width=4, height=2,
                                font=("Arial", 10, "bold"),
                                command=lambda rr=r, cc=c: self._on_cell_click(rr, cc))
                btn.grid(row=r, column=c, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)

        tk.Button(self.root, text="Neues Spiel", font=("Arial", 10),
                  command=self._restart).pack(pady=4)

    # ---- Brett aktualisieren --------------------------------------------
    def _refresh_board(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = self.buttons[r][c]
                piece = self.game.state.board[r][c]

                if (r, c) in LAKES:
                    btn.config(text="≈", bg="#1e90ff", fg="white", state="disabled")
                    continue

                if r in BLUE_SETUP_ROWS:
                    bg = "#dbeafe"
                elif r in RED_SETUP_ROWS:
                    bg = "#fee2e2"
                else:
                    bg = "#f5f5f5"

                if piece:
                    if piece.owner == self.game.state.current_player or piece.revealed:
                        text = "⚑" if piece.name == "Fahne" else (
                               "💣" if piece.name == "Bombe" else str(piece.rank))
                    else:
                        text = "?"
                    btn.config(text=text, bg=bg, fg="black", state="normal")
                else:
                    btn.config(text="", bg=bg, state="normal")

                if self.selected == (r, c):
                    btn.config(bg="#facc15")
                elif (r, c) in self.valid_targets:
                    btn.config(bg="#86efac")

    # ---- Klick-Handler ---------------------------------------------------
    def _on_cell_click(self, r: int, c: int):
        if self.game.state.game_over:
            return

        # Zug ausführen, wenn Zielfeld gewählt
        if self.selected and (r, c) in self.valid_targets:
            fr, fc = self.selected
            ok, msg = self.game.move(fr, fc, r, c)
            if not ok:
                messagebox.showwarning("Ungültiger Zug", msg)
                return

            self.selected = None
            self.valid_targets = []
            self._refresh_board()

            # Sofort beendet: Fahne erobert
            if self.game.state.game_over:
                self.status_var.set("Spiel beendet.")
                messagebox.showinfo("Spielende", msg)
                return

            # Zwischenfenster, das den Spielplan verdeckt
            self._show_handover_dialog(msg)

            # ERST JETZT prüfen, ob der neue Spieler ziehen kann
            if not self.game.check_current_player_has_moves():
                winner = "blue" if self.game.state.current_player == "red" else "red"
                self.game.state.game_over = True
                self.status_var.set("Spiel beendet.")
                messagebox.showinfo(
                    "Spielende",
                    f"🏆 {winner.upper()} gewinnt, weil "
                    f"{self.game.state.current_player.upper()} keine "
                    f"beweglichen Figuren mehr hat!"
                )
            self._refresh_board()
            return

        # Eigene Figur auswählen
        piece = self.game.state.board[r][c]
        if piece and piece.owner == self.game.state.current_player:
            if not piece.is_movable():
                messagebox.showinfo("Nicht bewegbar",
                                    f"{piece.name} kann nicht gezogen werden.")
                return
            self.selected = (r, c)
            self.valid_targets = self.game.get_valid_moves(r, c)
            self._refresh_board()
            self.status_var.set(
                f"{piece.owner.upper()} – {piece.name} ausgewählt. Zielfeld wählen."
            )
        else:
            self.selected = None
            self.valid_targets = []
            self._refresh_board()
            self.status_var.set(
                f"{self.game.state.current_player.upper()} ist am Zug. "
                f"Klicke eine eigene Figur an."
            )

    # ---- Zwischenfenster -------------------------------------------------
    def _show_handover_dialog(self, last_msg: str):
        """Overlay exakt über dem Spielplan, modal – bis ‚Bereit‘ geklickt wird."""
        self.root.update_idletasks()
        x = self.board_frame.winfo_rootx()
        y = self.board_frame.winfo_rooty()
        w = self.board_frame.winfo_width()
        h = self.board_frame.winfo_height()

        dialog = tk.Toplevel(self.root)
        dialog.overrideredirect(True)          # keine Titelleiste, nicht verschiebbar
        dialog.configure(bg="#111")
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        dialog.grab_set()
        dialog.focus_force()

        next_player = self.game.state.current_player.upper()

        frame = tk.Frame(dialog, bg="#111")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text=last_msg, font=("Arial", 12),
                 bg="#111", fg="#ddd", wraplength=w - 40,
                 justify="center").pack(pady=(0, 12))

        tk.Label(frame, text=f"🔒  {next_player} ist am Zug",
                 font=("Arial", 20, "bold"),
                 bg="#111", fg="#facc15").pack(pady=6)

        tk.Label(frame, text="Bitte gib das Gerät weiter und klicke auf Bereit.",
                 font=("Arial", 11), bg="#111", fg="#aaa").pack(pady=(0, 14))

        def ready():
            dialog.destroy()

        tk.Button(frame, text="Bereit – Zug starten",
                  font=("Arial", 12, "bold"),
                  bg="#22c55e", fg="white", padx=25, pady=8,
                  command=ready).pack()

        dialog.protocol("WM_DELETE_WINDOW", ready)
        self.root.wait_window(dialog)

        self.status_var.set(
            f"{next_player} ist am Zug. Klicke eine eigene Figur an."
        )

    # ---- Neustart --------------------------------------------------------
    def _restart(self):
        self.game = StrategoGame()
        self.selected = None
        self.valid_targets = []
        self.status_var.set("Neues Spiel – Rot beginnt.")
        self._refresh_board()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    root = tk.Tk()
    StrategoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()