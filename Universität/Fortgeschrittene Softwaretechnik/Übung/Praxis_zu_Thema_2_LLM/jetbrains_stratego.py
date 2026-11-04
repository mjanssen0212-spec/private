def random_setup(color: Color, rng: random.Random) -> Dict[Position, Piece]:
    """Erzeugt eine halbwegs sinnvolle zufällige Aufstellung.

    Strategie:
    - Fahne bevorzugt in die hinterste Reihe, häufig in eine Ecke oder nahe am Rand.
    - Bomben bevorzugt um die Fahne und ebenfalls eher hinten.
    - Bewegliche Figuren werden zufällig auf die restlichen Felder verteilt.
    """
    rows = list(color.setup_rows)
    back_row = rows[-1] if color is Color.BLUE else rows[0]

    setup_squares = [(row, col) for row in rows for col in range(BOARD_SIZE)]
    board: Dict[Position, Piece] = {}

    # Fahne eher geschützt hinten platzieren.
    preferred_flag_cols = [0, 9, 1, 8, 2, 7]
    flag_col = rng.choice(preferred_flag_cols)
    flag_pos = (back_row, flag_col)
    board[flag_pos] = Piece(color, Rank.FLAG)

    # Bomben bevorzugt um die Fahne herum platzieren.
    neighbour_candidates = []
    for dr, dc in DIRECTIONS:
        candidate = (flag_pos[0] + dr, flag_pos[1] + dc)
        if candidate in setup_squares and candidate not in board:
            neighbour_candidates.append(candidate)

    # Zusätzliche Bombenfelder hinten priorisieren.
    back_row_candidates = [
        (back_row, col)
        for col in range(BOARD_SIZE)
        if (back_row, col) in setup_squares and (back_row, col) not in board
    ]

    remaining_candidates = [
        pos for pos in setup_squares if pos not in board
    ]

    bomb_positions: List[Position] = []

    rng.shuffle(neighbour_candidates)
    rng.shuffle(back_row_candidates)
    rng.shuffle(remaining_candidates)

    for candidate_list in (neighbour_candidates, back_row_candidates, remaining_candidates):
        for pos in candidate_list:
            if len(bomb_positions) >= Rank.BOMB.count:
                break
            if pos not in board and pos not in bomb_positions:
                bomb_positions.append(pos)

    for pos in bomb_positions:
        board[pos] = Piece(color, Rank.BOMB)

    # Restliche Figuren zufällig verteilen.
    remaining_ranks = [
        rank
        for rank in Rank
        if rank not in (Rank.FLAG, Rank.BOMB)
        for _ in range(rank.count)
    ]
    rng.shuffle(remaining_ranks)

    free_squares = [pos for pos in setup_squares if pos not in board]
    rng.shuffle(free_squares)

    for pos, rank in zip(free_squares, remaining_ranks):
        board[pos] = Piece(color, rank)

    return board