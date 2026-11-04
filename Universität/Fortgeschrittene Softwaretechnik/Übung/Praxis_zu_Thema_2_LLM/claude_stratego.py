#!/usr/bin/env python3
"""Stratego für zwei Spieler an einem Bildschirm.

Start:  python3 claude_stratego.py

Die Datei besteht aus zwei klar getrennten Teilen:

* Spiellogik (``Game``): Regeln nach der Anleitung "Original Stratego"
  (Jumbo 498). Sie kommt ohne Oberfläche aus und lässt sich direkt testen.
* Oberfläche (``StrategoApp``): tkinter, ohne zusätzliche Pakete.

Festlegungen, die über den Wortlaut der Anleitung hinausgehen:

* Beide Aufstellungen werden zufällig erzeugt. Eine Aufstellung, bei der ein
  Spieler keinen einzigen Zug hätte, wird neu gemischt.
* Das Hin- und Herziehen zwischen zwei Feldern ist fünfmal hintereinander
  erlaubt. Ein Zug mit einer anderen Figur oder ein Angriff setzt die Zählung
  zurück.
* Wer noch bewegliche Figuren, aber keinen erlaubten Zug mehr hat, verliert.
* Haben beide Spieler keine beweglichen Figuren mehr, endet das Spiel
  unentschieden.
* Überlebende Figuren werden nach einem Kampf wieder verdeckt.
"""

from __future__ import annotations

import random
import sys
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, FrozenSet, List, Optional, Tuple

try:
    import tkinter as tk
    from tkinter import font as tkfont
except ImportError:  # Die Spiellogik bleibt auch ohne tkinter nutzbar.
    tk = None
    tkfont = None


# ---------------------------------------------------------------------------
# Spiellogik
# ---------------------------------------------------------------------------

BOARD_SIZE = 10
SETUP_ROWS = 4
MAX_SHUTTLE_MOVES = 5
COLUMN_NAMES = "ABCDEFGHIJ"
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))

Position = Tuple[int, int]  # (Zeile, Spalte), Zeile 0 liegt auf der Seite von Blau

LAKES: FrozenSet[Position] = frozenset(
    (row, col) for row in (4, 5) for col in (2, 3, 6, 7)
)


class Color(Enum):
    RED = "Rot"
    BLUE = "Blau"

    @property
    def opponent(self) -> "Color":
        return Color.BLUE if self is Color.RED else Color.RED

    @property
    def setup_rows(self) -> range:
        if self is Color.RED:
            return range(BOARD_SIZE - SETUP_ROWS, BOARD_SIZE)
        return range(SETUP_ROWS)


class Rank(Enum):
    """Name, kurzer Name, Stärke und Anzahl pro Spieler.

    Stärke 0 steht für unbewegliche Figuren.
    """

    MARSHAL = ("Feldmarschall", "Marschall", 10, 1)
    GENERAL = ("General", "General", 9, 1)
    COLONEL = ("Oberst", "Oberst", 8, 2)
    MAJOR = ("Major", "Major", 7, 3)
    CAPTAIN = ("Hauptmann", "Hauptm.", 6, 4)
    LIEUTENANT = ("Leutnant", "Leutnant", 5, 4)
    SERGEANT = ("Unteroffizier", "Unteroff.", 4, 4)
    MINER = ("Mineur", "Mineur", 3, 5)
    SCOUT = ("Aufklärer", "Aufklärer", 2, 8)
    SPY = ("Spion", "Spion", 1, 1)
    BOMB = ("Bombe", "Bombe", 0, 6)
    FLAG = ("Fahne", "Fahne", 0, 1)

    def __init__(self, label: str, short: str, strength: int, count: int) -> None:
        self.label = label
        self.short = short
        self.strength = strength
        self.count = count

    @property
    def movable(self) -> bool:
        return self.strength > 0


class Outcome(Enum):
    ATTACKER = "Angreifer gewinnt"
    DEFENDER = "Verteidiger gewinnt"
    BOTH = "Beide geschlagen"


class IllegalMove(Exception):
    """Ein Zug verstößt gegen die Regeln."""


class Piece:
    """Eine Spielfigur. Zwei Figuren gleichen Rangs bleiben unterscheidbar."""

    __slots__ = ("color", "rank")

    def __init__(self, color: Color, rank: Rank) -> None:
        self.color = color
        self.rank = rank

    def __repr__(self) -> str:
        return f"Piece({self.color.value}, {self.rank.label})"


@dataclass(frozen=True)
class Shuttle:
    """Zählt die Züge einer Figur zwischen genau zwei Feldern."""

    piece: Piece
    squares: FrozenSet[Position]
    count: int


@dataclass(frozen=True)
class MoveResult:
    """Ergebnis eines Zugs. Bei einem einfachen Zug fehlen die Kampfangaben."""

    color: Color
    src: Position
    dst: Position
    attacker: Rank
    defender: Optional[Rank] = None
    outcome: Optional[Outcome] = None

    @property
    def is_attack(self) -> bool:
        return self.defender is not None

    @property
    def text(self) -> str:
        if not self.is_attack:
            return f"Von {square_name(self.src)} nach {square_name(self.dst)} gezogen."
        return self._battle_text()

    def _battle_text(self) -> str:
        mover = self.color.value
        other = self.color.opponent.value
        attacker = f"{self.attacker.label} ({mover})"
        defender = f"{self.defender.label} ({other})"
        if self.defender is Rank.FLAG:
            return f"{attacker} erobert die Fahne von {other}."
        if self.defender is Rank.BOMB:
            if self.outcome is Outcome.ATTACKER:
                return f"{attacker} entschärft die Bombe von {other}."
            return f"Bumm! {attacker} läuft in die Bombe von {other} und ist geschlagen."
        if self.outcome is Outcome.BOTH:
            return f"Gleicher Rang: Beide {self.attacker.label} sind geschlagen."
        if self.outcome is Outcome.ATTACKER:
            return f"{attacker} schlägt {defender}."
        return f"{defender} schlägt {attacker}."


def square_name(pos: Position) -> str:
    """Feldname wie auf dem Brett, z. B. ``C4``."""
    row, col = pos
    return f"{COLUMN_NAMES[col]}{BOARD_SIZE - row}"


def on_board(pos: Position) -> bool:
    return 0 <= pos[0] < BOARD_SIZE and 0 <= pos[1] < BOARD_SIZE


def resolve_battle(attacker: Rank, defender: Rank) -> Outcome:
    """Entscheidet einen Kampf nach den Rängen der Anleitung."""
    if defender is Rank.FLAG:
        return Outcome.ATTACKER
    if defender is Rank.BOMB:
        return Outcome.ATTACKER if attacker is Rank.MINER else Outcome.DEFENDER
    if attacker is Rank.SPY and defender is Rank.MARSHAL:
        return Outcome.ATTACKER
    if attacker is defender:
        return Outcome.BOTH
    if attacker.strength > defender.strength:
        return Outcome.ATTACKER
    return Outcome.DEFENDER


def random_setup(color: Color, rng: random.Random) -> Dict[Position, Piece]:
    """Verteilt alle 40 Figuren zufällig auf die vier hinteren Reihen."""
    ranks = [rank for rank in Rank for _ in range(rank.count)]
    rng.shuffle(ranks)
    squares = [(row, col) for row in color.setup_rows for col in range(BOARD_SIZE)]
    return {pos: Piece(color, rank) for pos, rank in zip(squares, ranks)}


class Game:
    """Vollständiger Spielzustand. Rot beginnt immer."""

    def __init__(
        self,
        rng: Optional[random.Random] = None,
        board: Optional[Dict[Position, Piece]] = None,
        current: Color = Color.RED,
    ) -> None:
        self.rng = rng or random.Random()
        self.current = current
        self.turn = 0
        self.finished = False
        self.winner: Optional[Color] = None
        self.end_reason = ""
        self._shuttles: Dict[Color, Shuttle] = {}
        self.board: Dict[Position, Piece] = {}
        if board is None:
            self._deal()
        else:
            self.board = dict(board)

    def _deal(self) -> None:
        while True:
            self.board = {
                **random_setup(Color.BLUE, self.rng),
                **random_setup(Color.RED, self.rng),
            }
            if self.has_legal_move(Color.RED) and self.has_legal_move(Color.BLUE):
                return

    # --- Abfragen ---------------------------------------------------------

    def check_move(self, src: Position, dst: Position) -> Optional[str]:
        """Liefert den Grund, warum ein Zug verboten ist, sonst ``None``."""
        if self.finished:
            return "Das Spiel ist beendet."
        return self._move_error(self.current, src, dst)

    def legal_targets(self, pos: Position) -> List[Position]:
        """Alle Felder, die die Figur auf ``pos`` erreichen oder angreifen darf."""
        piece = self.board.get(pos)
        if piece is None or not piece.rank.movable:
            return []
        return [
            target
            for target in self._line_squares(pos)
            if self._move_error(piece.color, pos, target) is None
        ]

    def has_legal_move(self, color: Color) -> bool:
        return any(
            self.legal_targets(pos)
            for pos, piece in self.board.items()
            if piece.color is color
        )

    def remaining(self, color: Color) -> Counter:
        """Figuren pro Rang, die für ``color`` noch im Spiel sind."""
        return Counter(
            piece.rank for piece in self.board.values() if piece.color is color
        )

    def has_mobile_pieces(self, color: Color) -> bool:
        return any(
            piece.color is color and piece.rank.movable
            for piece in self.board.values()
        )

    def blocked_return(self, pos: Position) -> Optional[Position]:
        """Freies Feld, das die Figur wegen des Hin-und-Her-Limits nicht betreten darf."""
        piece = self.board.get(pos)
        if piece is None:
            return None
        shuttle = self._shuttles.get(piece.color)
        if (
            shuttle is None
            or shuttle.piece is not piece
            or shuttle.count < MAX_SHUTTLE_MOVES
            or pos not in shuttle.squares
        ):
            return None
        other = next(iter(shuttle.squares - {pos}))
        return None if other in self.board else other

    # --- Zug ausführen ----------------------------------------------------

    def move(self, src: Position, dst: Position) -> MoveResult:
        """Führt einen erlaubten Zug aus und gibt den Spieler weiter."""
        reason = self.check_move(src, dst)
        if reason is not None:
            raise IllegalMove(reason)

        piece = self.board[src]
        target = self.board.get(dst)
        if target is None:
            result = self._walk(piece, src, dst)
        else:
            result = self._attack(piece, target, src, dst)

        self.turn += 1
        self.current = piece.color.opponent
        self._update_end_state(result)
        return result

    def _walk(self, piece: Piece, src: Position, dst: Position) -> MoveResult:
        del self.board[src]
        self.board[dst] = piece
        squares = frozenset((src, dst))
        shuttle = self._shuttles.get(piece.color)
        continues = (
            shuttle is not None
            and shuttle.piece is piece
            and shuttle.squares == squares
        )
        count = shuttle.count + 1 if continues else 1
        self._shuttles[piece.color] = Shuttle(piece, squares, count)
        return MoveResult(piece.color, src, dst, piece.rank)

    def _attack(
        self, piece: Piece, target: Piece, src: Position, dst: Position
    ) -> MoveResult:
        outcome = resolve_battle(piece.rank, target.rank)
        del self.board[src]
        if outcome is Outcome.ATTACKER:
            self.board[dst] = piece
        elif outcome is Outcome.BOTH:
            del self.board[dst]
        self._shuttles.pop(piece.color, None)
        return MoveResult(piece.color, src, dst, piece.rank, target.rank, outcome)

    def _update_end_state(self, result: MoveResult) -> None:
        mover = result.color
        other = mover.opponent
        if result.defender is Rank.FLAG:
            self._finish(mover, f"{mover.value} hat die Fahne von {other.value} erobert.")
            return

        mover_mobile = self.has_mobile_pieces(mover)
        other_mobile = self.has_mobile_pieces(other)
        if not mover_mobile and not other_mobile:
            self._finish(None, "Beide Spieler haben keine beweglichen Figuren mehr.")
        elif not other_mobile:
            self._finish(mover, f"{other.value} hat keine beweglichen Figuren mehr.")
        elif not mover_mobile:
            self._finish(other, f"{mover.value} hat keine beweglichen Figuren mehr.")
        elif not self.has_legal_move(other):
            self._finish(mover, f"{other.value} kann nicht mehr ziehen.")

    def _finish(self, winner: Optional[Color], reason: str) -> None:
        self.finished = True
        self.winner = winner
        self.end_reason = reason

    # --- Regelprüfung -----------------------------------------------------

    def _move_error(self, color: Color, src: Position, dst: Position) -> Optional[str]:
        piece = self.board.get(src)
        if piece is None or piece.color is not color:
            return "Wähle eine eigene Figur."
        if not piece.rank.movable:
            return f"{piece.rank.label} kann nicht gezogen werden."
        if not on_board(dst):
            return "Dieses Feld liegt außerhalb des Spielplans."
        if dst == src:
            return "Wähle ein anderes Feld."
        if dst in LAKES:
            return "Seen dürfen nicht betreten werden."

        row_delta = dst[0] - src[0]
        col_delta = dst[1] - src[1]
        if row_delta and col_delta:
            return "Figuren ziehen nur waagerecht oder senkrecht, niemals diagonal."

        distance = abs(row_delta) + abs(col_delta)
        if distance > 1 and piece.rank is not Rank.SCOUT:
            return "Nur Aufklärer ziehen weiter als ein Feld."

        step = ((row_delta > 0) - (row_delta < 0), (col_delta > 0) - (col_delta < 0))
        for index in range(1, distance):
            between = (src[0] + step[0] * index, src[1] + step[1] * index)
            if between in LAKES:
                return "Seen dürfen nicht übersprungen werden."
            if between in self.board:
                return "Figuren dürfen nicht übersprungen werden."

        target = self.board.get(dst)
        if target is not None and target.color is color:
            return "Auf jedem Feld darf nur eine Figur stehen."
        if target is None and self._shuttle_exhausted(piece, src, dst):
            return (
                "Hin- und Herziehen ist höchstens fünfmal hintereinander erlaubt. "
                "Ziehe auf ein drittes Feld oder bewege eine andere Figur."
            )
        return None

    def _shuttle_exhausted(self, piece: Piece, src: Position, dst: Position) -> bool:
        shuttle = self._shuttles.get(piece.color)
        return (
            shuttle is not None
            and shuttle.piece is piece
            and shuttle.squares == frozenset((src, dst))
            and shuttle.count >= MAX_SHUTTLE_MOVES
        )

    @staticmethod
    def _line_squares(pos: Position) -> List[Position]:
        row, col = pos
        squares = [(row, other) for other in range(BOARD_SIZE) if other != col]
        squares += [(other, col) for other in range(BOARD_SIZE) if other != row]
        return squares


# ---------------------------------------------------------------------------
# Oberfläche
# ---------------------------------------------------------------------------

BACKDROP = "#1E2A25"
PANEL = "#26352E"
PANEL_LINE = "#3D5046"
TEXT = "#F0E7CE"
TEXT_MUTED = "#AEB39B"
FIELD = "#BDBB8E"
FIELD_MIDDLE = "#CBC8A0"
GRID = "#8D8C63"
LAKE = "#4E7F92"
LAKE_CONTOUR = "#86B0BC"
BRASS = "#E2B33C"
MARK = "#FFF6DC"
HINT_ERROR = "#F2B6A0"

COLOR_STYLES = {
    Color.RED: {"face": "#A9281F", "edge": "#6E1712", "mark": "#7E1C15", "hover": "#BE3A30"},
    Color.BLUE: {"face": "#1F4C88", "edge": "#112D54", "mark": "#163966", "hover": "#2E62A8"},
}

FONT_FAMILIES = (
    "Georgia",
    "Palatino Linotype",
    "Book Antiqua",
    "Palatino",
    "DejaVu Serif",
    "Liberation Serif",
    "Times New Roman",
)

PANEL_WIDTH = 300
COVER_ARM_MS = 600  # verhindert, dass ein Doppelklick das Brett sofort aufdeckt


def rounded_rect(
    canvas: "tk.Canvas", x0: float, y0: float, x1: float, y1: float, radius: float, **options
) -> int:
    points = [
        x0 + radius, y0, x0 + radius, y0, x1 - radius, y0, x1 - radius, y0,
        x1, y0, x1, y0 + radius, x1, y0 + radius, x1, y1 - radius,
        x1, y1 - radius, x1, y1, x1 - radius, y1, x1 - radius, y1,
        x0 + radius, y1, x0 + radius, y1, x0, y1, x0, y1 - radius,
        x0, y1 - radius, x0, y0 + radius, x0, y0 + radius, x0, y0,
    ]
    return canvas.create_polygon(points, smooth=True, **options)


def draw_sabres(
    canvas: "tk.Canvas", cx: float, cy: float, size: float, color: str, width: float
) -> None:
    """Gekreuzte Säbel als Rückseite der Figuren und Wappen der Trennwand."""
    half = size / 2
    for side in (-1, 1):
        canvas.create_line(
            cx + side * half, cy + half,
            cx + side * half * 0.1, cy + half * 0.12,
            cx - side * half * 0.86, cy - half,
            fill=color, width=width, smooth=True, capstyle="round",
        )
        guard_x = cx + side * half * 0.68
        guard_y = cy + half * 0.68
        reach = size * 0.09
        canvas.create_line(
            guard_x - reach, guard_y + side * reach,
            guard_x + reach, guard_y - side * reach,
            fill=color, width=width, capstyle="round",
        )


class FlatButton:
    """Schaltfläche, die auf Windows, macOS und Linux gleich aussieht."""

    def __init__(
        self,
        parent: "tk.Misc",
        text: str,
        command: Callable[[], None],
        font: tuple,
        bg: str = BRASS,
        fg: str = "#1E2A25",
        hover: str = "#F0C95F",
        padx: int = 22,
    ) -> None:
        self.command = command
        self.bg = bg
        self.fg = fg
        self.hover = hover
        self.disabled_bg = PANEL_LINE
        self.disabled_fg = TEXT_MUTED
        self.enabled = True
        self.label = tk.Label(
            parent, text=text, font=font, bg=bg, fg=fg, padx=padx, pady=11, cursor="hand2"
        )
        self.label.bind("<ButtonRelease-1>", lambda _event: self.invoke())
        self.label.bind("<Enter>", lambda _event: self._paint(self.hover))
        self.label.bind("<Leave>", lambda _event: self._paint(self.bg))

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled
        self.label.configure(cursor="hand2" if enabled else "arrow")
        self._paint(self.bg)

    def invoke(self) -> None:
        if self.enabled:
            self.command()

    def _paint(self, color: str) -> None:
        if self.enabled:
            self.label.configure(bg=color, fg=self.fg)
        else:
            self.label.configure(bg=self.disabled_bg, fg=self.disabled_fg)


class Phase(Enum):
    COVER = "Trennwand"
    TURN = "Zug"
    RESULT = "Kampfergebnis"
    OVER = "Spielende"


class StrategoApp:
    """Führt zwei Spieler durch Trennwand, Zug und Kampfergebnis."""

    def __init__(self, root: "tk.Tk", rng: Optional[random.Random] = None) -> None:
        self.root = root
        self.rng = rng
        self.family = self._pick_family()
        self.game = Game(rng)
        self.phase = Phase.COVER
        self.viewer = Color.RED
        self.selected: Optional[Position] = None
        self.targets: List[Position] = []
        self.last_result: Optional[MoveResult] = None
        self.hint = ""
        self.hint_is_error = False
        self._arm_job: Optional[str] = None
        self.cell = 60
        self.origin = (0, 0)

        self._configure_window()
        self._build_game_screen()
        self._build_cover_screen()
        self.root.bind("<Return>", self._on_confirm_key)
        self.root.bind("<KP_Enter>", self._on_confirm_key)
        self.root.bind("<space>", self._on_confirm_key)
        self.new_game()

    # --- Aufbau -----------------------------------------------------------

    def _pick_family(self) -> str:
        available = set(tkfont.families(self.root))
        for family in FONT_FAMILIES:
            if family in available:
                return family
        return "TkDefaultFont"

    def _font(self, size: float, bold: bool = False) -> tuple:
        pixels = -max(8, int(round(size)))  # negative Werte bedeuten Pixel
        return (self.family, pixels, "bold") if bold else (self.family, pixels)

    def _configure_window(self) -> None:
        self.root.title("Stratego")
        self.root.configure(bg=BACKDROP)
        self.root.minsize(860, 620)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        height = max(620, min(screen_height - 120, 840))
        width = max(860, min(screen_width - 60, height + PANEL_WIDTH))
        left = max(0, (screen_width - width) // 2)
        top = max(0, (screen_height - height) // 3)
        self.root.geometry(f"{width}x{height}+{left}+{top}")

    def _build_game_screen(self) -> None:
        self.game_screen = tk.Frame(self.root, bg=BACKDROP)
        panel = tk.Frame(self.game_screen, bg=PANEL, width=PANEL_WIDTH)
        panel.pack(side="right", fill="y")
        panel.pack_propagate(False)

        self.canvas = tk.Canvas(self.game_screen, bg=BACKDROP, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._on_board_click)
        self.canvas.bind("<Configure>", lambda _event: self._draw_board())

        self.band = tk.Frame(panel, bg=PANEL)
        self.band.pack(fill="x")
        self.band_title = tk.Label(
            self.band, font=self._font(23, True), fg=TEXT, anchor="w", padx=20, pady=0
        )
        self.band_title.pack(fill="x", pady=(16, 0))
        self.band_detail = tk.Label(
            self.band, font=self._font(14), fg=TEXT, anchor="w", padx=20
        )
        self.band_detail.pack(fill="x", pady=(0, 14))

        body = tk.Frame(panel, bg=PANEL)
        body.pack(fill="both", expand=True, padx=20, pady=(14, 14))

        self.report_title = tk.Label(
            body, font=self._font(15, True), bg=PANEL, fg=TEXT, anchor="w"
        )
        self.report_title.pack(fill="x")
        self.report_canvas = tk.Canvas(
            body, width=PANEL_WIDTH - 40, height=66, bg=PANEL, highlightthickness=0
        )
        self.report_canvas.pack(fill="x", pady=(6, 4))
        self.report_text = tk.Label(
            body,
            font=self._font(15),
            bg=PANEL,
            fg=TEXT,
            anchor="nw",
            justify="left",
            wraplength=PANEL_WIDTH - 40,
        )
        self.report_text.pack(fill="x")

        self.hint_label = tk.Label(
            body,
            font=self._font(14),
            bg=PANEL,
            fg=TEXT_MUTED,
            anchor="nw",
            justify="left",
            wraplength=PANEL_WIDTH - 40,
        )

        self.actions = tk.Frame(body, bg=PANEL)
        self.actions.pack(fill="x", pady=(10, 0))
        self.end_turn_button = FlatButton(
            self.actions, "Zug beenden", self._end_turn, self._font(16, True)
        )
        self.new_game_button = FlatButton(
            self.actions, "Neues Spiel", self.new_game, self._font(16, True), padx=8
        )
        self.quit_button = FlatButton(
            self.actions,
            "Beenden",
            self.root.destroy,
            self._font(16),
            bg=PANEL_LINE,
            fg=TEXT,
            hover="#4E6459",
            padx=8,
        )

        self._build_count_table(body)

    def _build_count_table(self, parent: "tk.Frame") -> None:
        table = tk.Frame(parent, bg=PANEL)
        table.pack(side="bottom", fill="x")
        table.columnconfigure(0, weight=1)
        font = self._font(13)
        bold = self._font(13, True)
        tk.Label(
            table, text="Figuren im Spiel", font=bold, bg=PANEL, fg=TEXT, anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 3))
        for column, color in ((1, Color.RED), (2, Color.BLUE)):
            tk.Label(
                table, text=color.value, font=bold, bg=PANEL, fg=TEXT, width=4, anchor="e"
            ).grid(row=0, column=column, sticky="e")

        self.count_labels: Dict[Tuple[Rank, Color], "tk.Label"] = {}
        self.count_names: Dict[Rank, "tk.Label"] = {}
        for row, rank in enumerate(Rank, start=1):
            prefix = f"{rank.strength}  " if rank.movable else ""
            name = tk.Label(
                table, text=f"{prefix}{rank.label}", font=font, bg=PANEL, fg=TEXT,
                anchor="w", pady=0,
            )
            name.grid(row=row, column=0, sticky="w")
            self.count_names[rank] = name
            for column, color in ((1, Color.RED), (2, Color.BLUE)):
                label = tk.Label(
                    table, font=font, bg=PANEL, fg=TEXT, width=4, anchor="e", pady=0
                )
                label.grid(row=row, column=column, sticky="e")
                self.count_labels[(rank, color)] = label

    def _build_cover_screen(self) -> None:
        self.cover_screen = tk.Canvas(self.root, highlightthickness=0, bd=0)
        self.cover_screen.bind("<Configure>", lambda _event: self._draw_cover())
        self.cover_title = ""
        self.cover_text = ""
        self.cover_button = FlatButton(
            self.cover_screen, "Brett aufdecken", self.start_turn, self._font(19, True)
        )

    # --- Ablauf -----------------------------------------------------------

    def new_game(self) -> None:
        self.game = Game(self.rng)
        self.viewer = Color.RED
        self.last_result = None
        self.show_cover()

    def show_cover(self) -> None:
        """Verdeckt das Spiel vollständig, bis der nächste Spieler bestätigt."""
        self.phase = Phase.COVER
        self._clear_selection()
        self.game_screen.pack_forget()
        self.canvas.delete("all")
        self.report_canvas.delete("all")

        player = self.game.current
        waiting = player.opponent.value
        if self.last_result is None:
            self.cover_title = f"{player.value} beginnt"
            self.cover_text = (
                f"{waiting}, bitte schau weg. {player.value}, decke das Brett auf, "
                "sobald nur du auf den Bildschirm schaust."
            )
        else:
            self.cover_title = f"{player.value} ist am Zug"
            self.cover_text = (
                f"{waiting}, gib den Platz frei. {player.value}, decke das Brett auf, "
                "sobald nur du auf den Bildschirm schaust."
            )

        style = COLOR_STYLES[player]
        self.cover_screen.configure(bg=style["face"])
        self.cover_screen.pack(fill="both", expand=True)
        self.cover_button.disabled_bg = style["edge"]
        self.cover_button.disabled_fg = TEXT_MUTED
        self.cover_button.set_enabled(False)
        self._draw_cover()

        if self._arm_job is not None:
            self.root.after_cancel(self._arm_job)
        self._arm_job = self.root.after(COVER_ARM_MS, self._arm_cover)

    def _arm_cover(self) -> None:
        self._arm_job = None
        self.cover_button.set_enabled(True)

    def start_turn(self) -> None:
        if self.phase is not Phase.COVER:
            return
        self.phase = Phase.TURN
        self.viewer = self.game.current
        self._set_hint("Wähle eine eigene Figur.")
        self._show_game_screen()

    def _end_turn(self) -> None:
        if self.phase is Phase.RESULT:
            self.show_cover()

    def _show_game_screen(self) -> None:
        self.cover_screen.pack_forget()
        self.game_screen.pack(fill="both", expand=True)
        self.root.update_idletasks()
        self._render()

    def _finish_move(self, src: Position, dst: Position) -> None:
        self.last_result = self.game.move(src, dst)
        self._clear_selection()
        if self.game.finished:
            self.phase = Phase.OVER
            self._set_hint("")
            self._render()
        elif self.last_result.is_attack:
            self.phase = Phase.RESULT
            self._set_hint("")
            self._render()
        else:
            self.show_cover()

    # --- Eingaben ---------------------------------------------------------

    def _on_confirm_key(self, _event: "tk.Event") -> None:
        if self.phase is Phase.COVER:
            self.cover_button.invoke()
        elif self.phase is Phase.RESULT:
            self.end_turn_button.invoke()

    def _on_board_click(self, event: "tk.Event") -> None:
        if self.phase is not Phase.TURN:
            return
        pos = self._pixel_to_square(event.x, event.y)
        if pos is not None:
            self._select_square(pos)
            self._render()

    def _select_square(self, pos: Position) -> None:
        piece = self.game.board.get(pos)
        own_piece = piece is not None and piece.color is self.viewer

        if pos == self.selected:
            self._clear_selection()
            self._set_hint("Wähle eine eigene Figur.")
        elif own_piece:
            self._choose_piece(pos, piece)
        elif self.selected is None:
            self._set_hint("Wähle zuerst eine eigene Figur.", error=True)
        else:
            reason = self.game.check_move(self.selected, pos)
            if reason is None:
                self._finish_move(self.selected, pos)
            else:
                self._set_hint(reason, error=True)

    def _choose_piece(self, pos: Position, piece: Piece) -> None:
        if not piece.rank.movable:
            self._clear_selection()
            self._set_hint(f"{piece.rank.label} kann nicht gezogen werden.", error=True)
            return
        self.selected = pos
        self.targets = self.game.legal_targets(pos)
        blocked = self.game.blocked_return(pos)
        if blocked is not None:
            self._set_hint(
                f"{square_name(blocked)} ist gesperrt: Hin- und Herziehen ist "
                "höchstens fünfmal hintereinander erlaubt.",
                error=True,
            )
        elif self.targets:
            self._set_hint(f"{piece.rank.label} gewählt. Klicke auf ein markiertes Feld.")
        else:
            self._set_hint(
                f"{piece.rank.label} hat gerade kein Zielfeld. Wähle eine andere Figur.",
                error=True,
            )

    def _clear_selection(self) -> None:
        self.selected = None
        self.targets = []

    def _set_hint(self, text: str, error: bool = False) -> None:
        self.hint = text
        self.hint_is_error = error

    # --- Koordinaten ------------------------------------------------------

    def _flip(self, pos: Position) -> Position:
        """Dreht das Brett, sodass die eigene Seite immer unten liegt.

        Die Drehung um 180 Grad ist ihre eigene Umkehrung und gilt daher für
        beide Richtungen: Spielfeld zu Ansicht und Ansicht zu Spielfeld.
        """
        if self.viewer is Color.BLUE:
            return (BOARD_SIZE - 1 - pos[0], BOARD_SIZE - 1 - pos[1])
        return pos

    def _square_origin(self, pos: Position) -> Tuple[int, int]:
        view_row, view_col = self._flip(pos)
        return (
            self.origin[0] + view_col * self.cell,
            self.origin[1] + view_row * self.cell,
        )

    def _pixel_to_square(self, x: int, y: int) -> Optional[Position]:
        view_col = (x - self.origin[0]) // self.cell
        view_row = (y - self.origin[1]) // self.cell
        view = (view_row, view_col)
        return self._flip(view) if on_board(view) else None

    # --- Zeichnen ---------------------------------------------------------

    def _render(self) -> None:
        if self.phase is Phase.COVER:
            return
        self._draw_board()
        self._update_panel()

    def _draw_cover(self) -> None:
        canvas = self.cover_screen
        canvas.delete("all")
        width = max(canvas.winfo_width(), 1)
        height = max(canvas.winfo_height(), 1)
        player = self.game.current
        style = COLOR_STYLES[player]
        center_x = width / 2
        center_y = height / 2

        title_size = max(44, min(width / 10, 92))
        crest_size = title_size * 1.15
        draw_sabres(
            canvas, center_x, center_y - title_size * 2.25, crest_size,
            TEXT, max(3, crest_size * 0.035),
        )
        canvas.create_text(
            center_x, center_y - title_size * 0.8,
            text=self.cover_title, fill=TEXT, font=self._font(title_size, True),
        )
        canvas.create_text(
            center_x, center_y + 18,
            text=self.cover_text, fill=TEXT, font=self._font(20),
            width=min(width - 80, 560), justify="center",
        )
        canvas.create_window(center_x, center_y + 112, window=self.cover_button.label)

    def _draw_board(self) -> None:
        canvas = self.canvas
        if self.phase is Phase.COVER:
            canvas.delete("all")
            return

        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        cell = max(24, min(width, height) // 11)
        self.cell = cell
        self.origin = ((width - cell * BOARD_SIZE) // 2, (height - cell * BOARD_SIZE) // 2)

        self._draw_terrain()
        self._draw_coordinates()
        self._draw_last_move()
        self._draw_pieces()
        self._draw_selection()

    def _draw_terrain(self) -> None:
        canvas = self.canvas
        cell = self.cell
        left, top = self.origin
        for row in range(BOARD_SIZE):
            fill = FIELD_MIDDLE if row in (4, 5) else FIELD
            for col in range(BOARD_SIZE):
                x = left + col * cell
                y = top + row * cell
                canvas.create_rectangle(
                    x, y, x + cell, y + cell, fill=fill, outline=GRID
                )
        for col in (2, 6):
            x0 = left + col * cell + 2
            y0 = top + 4 * cell + 2
            x1 = x0 + 2 * cell - 4
            y1 = y0 + 2 * cell - 4
            rounded_rect(canvas, x0, y0, x1, y1, cell * 0.28, fill=LAKE, outline=GRID)
            for depth in (0.16, 0.34, 0.52):
                inset = cell * depth
                rounded_rect(
                    canvas, x0 + inset, y0 + inset, x1 - inset, y1 - inset,
                    cell * 0.2, fill="", outline=LAKE_CONTOUR,
                )
        canvas.create_rectangle(
            left, top, left + BOARD_SIZE * cell, top + BOARD_SIZE * cell,
            outline=TEXT_MUTED, width=2,
        )

    def _draw_coordinates(self) -> None:
        cell = self.cell
        left, top = self.origin
        font = self._font(cell * 0.22)
        offset = max(11, cell * 0.24)
        for index in range(BOARD_SIZE):
            column_x, _ = self._square_origin((0, index))
            _, row_y = self._square_origin((index, 0))
            self.canvas.create_text(
                column_x + cell / 2, top + BOARD_SIZE * cell + offset,
                text=COLUMN_NAMES[index], fill=TEXT_MUTED, font=font,
            )
            self.canvas.create_text(
                left - offset, row_y + cell / 2,
                text=str(BOARD_SIZE - index), fill=TEXT_MUTED, font=font,
            )

    def _draw_last_move(self) -> None:
        result = self.last_result
        if result is None:
            return
        cell = self.cell
        inset = 3
        for pos, dash in ((result.src, (6, 4)), (result.dst, None)):
            x, y = self._square_origin(pos)
            self.canvas.create_rectangle(
                x + inset, y + inset, x + cell - inset, y + cell - inset,
                outline=MARK, width=3, dash=dash,
            )

    def _draw_pieces(self) -> None:
        reveal_all = self.phase is Phase.OVER
        for pos, piece in self.game.board.items():
            visible = reveal_all or piece.color is self.viewer
            x, y = self._square_origin(pos)
            self._draw_token(
                self.canvas, x, y, self.cell, piece.color,
                piece.rank if visible else None,
            )

    def _draw_token(
        self,
        canvas: "tk.Canvas",
        x: float,
        y: float,
        size: float,
        color: Color,
        rank: Optional[Rank],
    ) -> None:
        """Zeichnet einen Spielstein. Ohne ``rank`` zeigt er nur seine Rückseite."""
        style = COLOR_STYLES[color]
        inset = size * 0.075
        x0, y0 = x + inset, y + inset
        x1, y1 = x + size - inset, y + size - inset
        radius = size * 0.13
        rounded_rect(canvas, x0, y0 + size * 0.035, x1, y1 + size * 0.03, radius, fill=style["edge"])
        rounded_rect(canvas, x0, y0, x1, y1 - size * 0.01, radius, fill=style["face"])

        center_x = x + size / 2
        center_y = y + size / 2
        if rank is None:
            draw_sabres(
                canvas, center_x, center_y, size * 0.42, style["mark"], max(2, size * 0.04)
            )
            return

        symbol_y = center_y - size * 0.11
        if rank is Rank.BOMB:
            self._draw_bomb(canvas, center_x, symbol_y, size)
        elif rank is Rank.FLAG:
            self._draw_flag(canvas, center_x, symbol_y, size)
        else:
            canvas.create_text(
                center_x, symbol_y,
                text="S" if rank is Rank.SPY else str(rank.strength),
                fill=TEXT, font=self._font(size * 0.37, True),
            )
        canvas.create_text(
            center_x, center_y + size * 0.24,
            text=rank.short, fill=TEXT, font=self._font(size * 0.15),
        )

    @staticmethod
    def _draw_bomb(canvas: "tk.Canvas", x: float, y: float, size: float) -> None:
        radius = size * 0.15
        canvas.create_oval(
            x - radius, y - radius * 0.8, x + radius, y + radius * 1.2,
            fill=TEXT, outline="",
        )
        canvas.create_line(
            x + radius * 0.6, y - radius * 0.65,
            x + radius * 1.05, y - radius * 1.2,
            x + radius * 1.5, y - radius * 1.0,
            fill=TEXT, width=max(2, size * 0.03), smooth=True,
        )
        spark = size * 0.035
        canvas.create_oval(
            x + radius * 1.5 - spark, y - radius - spark,
            x + radius * 1.5 + spark, y - radius + spark,
            fill=BRASS, outline="",
        )

    @staticmethod
    def _draw_flag(canvas: "tk.Canvas", x: float, y: float, size: float) -> None:
        pole_x = x - size * 0.14
        top = y - size * 0.19
        bottom = y + size * 0.19
        canvas.create_line(
            pole_x, top, pole_x, bottom, fill=TEXT, width=max(2, size * 0.035), capstyle="round"
        )
        canvas.create_polygon(
            pole_x, top,
            x + size * 0.21, top + size * 0.09,
            pole_x, top + size * 0.2,
            fill=BRASS, outline="",
        )

    def _draw_selection(self) -> None:
        if self.selected is None:
            return
        canvas = self.canvas
        cell = self.cell
        x, y = self._square_origin(self.selected)
        canvas.create_rectangle(
            x + 2, y + 2, x + cell - 2, y + cell - 2, outline=BRASS, width=4
        )
        for target in self.targets:
            x, y = self._square_origin(target)
            center_x = x + cell / 2
            center_y = y + cell / 2
            if target in self.game.board:
                radius = cell * 0.46
                canvas.create_oval(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    outline=BRASS, width=4,
                )
            else:
                radius = cell * 0.14
                canvas.create_oval(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    fill=BRASS, outline=BACKDROP,
                )

    def _update_panel(self) -> None:
        self._update_band()
        self._update_report()
        self.hint_label.configure(
            text=self.hint, fg=HINT_ERROR if self.hint_is_error else TEXT_MUTED
        )
        if self.hint:
            self.hint_label.pack(fill="x", pady=(10, 0), before=self.actions)
        else:
            self.hint_label.pack_forget()
        self._update_actions()
        self._update_counts()

    def _update_band(self) -> None:
        if self.phase is Phase.OVER:
            winner = self.game.winner
            color = winner.value if winner else None
            title = f"{color} gewinnt" if color else "Unentschieden"
            background = COLOR_STYLES[winner]["face"] if winner else PANEL_LINE
            moves = self.game.turn
            detail = f"Nach {moves} {'Zug' if moves == 1 else 'Zügen'}"
        else:
            background = COLOR_STYLES[self.viewer]["face"]
            if self.phase is Phase.RESULT:
                title = f"{self.viewer.value} greift an"
                detail = f"Zug {self.game.turn}"
            else:
                title = f"{self.viewer.value} ist am Zug"
                detail = f"Zug {self.game.turn + 1}"
        self.band.configure(bg=background)
        self.band_title.configure(text=title, bg=background)
        self.band_detail.configure(text=detail, bg=background)

    def _update_report(self) -> None:
        result = self.last_result
        self.report_canvas.delete("all")
        if self.phase is Phase.OVER:
            title = "Spielende"
            body = self.game.end_reason
            if result is not None and result.defender is Rank.FLAG:
                body = result.text
            elif result is not None and result.is_attack:
                body = f"{result.text} {body}"
        elif result is None:
            title = "Eröffnung"
            body = "Rot beginnt. Gezogen wird immer nur eine Figur pro Zug."
        elif self.phase is Phase.RESULT:
            title = "Dein Angriff"
            body = result.text
        else:
            title = f"Angriff von {result.color.value}" if result.is_attack else f"Zug von {result.color.value}"
            body = result.text

        self.report_title.configure(text=title)
        self.report_text.configure(text=body)
        if result is not None and result.is_attack:
            self.report_canvas.configure(height=66)
            self._draw_token(self.report_canvas, 0, 0, 62, result.color, result.attacker)
            self.report_canvas.create_text(
                90, 31, text="gegen", fill=TEXT_MUTED, font=self._font(14)
            )
            self._draw_token(
                self.report_canvas, 118, 0, 62, result.color.opponent, result.defender
            )
        else:
            self.report_canvas.configure(height=1)

    def _update_actions(self) -> None:
        for button in (self.end_turn_button, self.new_game_button, self.quit_button):
            button.label.pack_forget()
        if self.phase is Phase.RESULT:
            self.end_turn_button.label.pack(fill="x")
        elif self.phase is Phase.OVER:
            self.new_game_button.label.pack(side="left", fill="x", expand=True)
            self.quit_button.label.pack(side="left", fill="x", expand=True, padx=(8, 0))

    def _update_counts(self) -> None:
        remaining = {color: self.game.remaining(color) for color in Color}
        for (rank, color), label in self.count_labels.items():
            count = remaining[color][rank]
            label.configure(text=str(count), fg=TEXT if count else TEXT_MUTED)
        for rank, label in self.count_names.items():
            alive = remaining[Color.RED][rank] + remaining[Color.BLUE][rank]
            label.configure(fg=TEXT if alive else TEXT_MUTED)


def main() -> int:
    if tk is None:
        print(
            "tkinter fehlt. Unter Debian/Ubuntu lässt es sich mit "
            "'sudo apt install python3-tk' installieren.",
            file=sys.stderr,
        )
        return 1
    root = tk.Tk()
    StrategoApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
