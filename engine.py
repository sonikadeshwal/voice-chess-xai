import chess

# Simple evaluation function values
PIECE_VALUES = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 900
}

def evaluate_board(board):
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        return 0
        
    score = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            value = PIECE_VALUES.get(piece.piece_type, 0)
            # Center control premium
            # e4, d4, e5, d5 are sq numbers 28, 27, 36, 35
            if sq in [27, 28, 35, 36]:
                value += 1
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
        
    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, depth=3):
    best_move = None
    maximizing_player = board.turn == chess.WHITE
    best_value = -float('inf') if maximizing_player else float('inf')
    
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, -float('inf'), float('inf'), not maximizing_player)
        board.pop()
        
        if maximizing_player:
            if board_value > best_value:
                best_value = board_value
                best_move = move
        else:
            if board_value < best_value:
                best_value = board_value
                best_move = move
                
    if best_move is None and list(board.legal_moves):
        best_move = list(board.legal_moves)[0]
        
    return best_move
