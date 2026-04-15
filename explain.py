import chess

def explain_move(board_before, move):
    """
    Generates a human-readable explanation for a given chess move.
    """
    piece = board_before.piece_at(move.from_square)
    if not piece:
        return "Unknown move reason."
        
    captured_piece = board_before.piece_at(move.to_square)
    is_castling = board_before.is_castling(move)
    is_en_passant = board_before.is_en_passant(move)
    
    explanation = []
    
    # 1. Castling
    if is_castling:
        explanation.append("The King castles to improve its safety and connect the Rooks.")
        return " ".join(explanation)
        
    # 2. Capture analysis
    if captured_piece:
        explanation.append(f"This move captures the opponent's {chess.piece_name(captured_piece.piece_type)}.")
    elif is_en_passant:
        explanation.append("This is an en passant capture, removing the opponent's pawn.")
        
    # 3. Check analysis
    board_after = board_before.copy()
    board_after.push(move)
    if board_after.is_checkmate():
        explanation.append("This is a checkmate move, winning the game!")
    elif board_after.is_check():
        explanation.append("The move puts the opponent's King in check, forcing a reaction.")
        
    # 4. Positional / Development
    if piece.piece_type in [chess.KNIGHT, chess.BISHOP] and chess.square_rank(move.from_square) in [0, 7]:
        explanation.append("It develops a minor piece from its starting square, increasing board influence.")
        
    # 5. Central control
    if move.to_square in [27, 28, 35, 36]: # e4, d4, e5, d5 squares
        explanation.append("The piece occupies the center, fighting for control of key squares.")
        
    if not explanation:
        explanation.append(f"The {chess.piece_name(piece.piece_type)} moves to a new square to improve its positional coordination.")
        
    return " ".join(explanation)
