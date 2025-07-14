import numpy as np

class FourQueensGame:
    def __init__(self):
        self.board = np.zeros((4, 4), dtype=int)
        self.current_player = 1  
    
    def is_valid_move(self, row, col):
        if self.board[row, col] != 0:
            return False
        
        for i in range(4):
            if self.board[row, i] != 0 or self.board[i, col] != 0:
                return False
        
        for i in range(-3, 4):
            if 0 <= row + i < 4 and 0 <= col + i < 4 and self.board[row + i, col + i] != 0:
                return False
            if 0 <= row + i < 4 and 0 <= col - i < 4 and self.board[row + i, col - i] != 0:
                return False
        
        return True
    
    def get_legal_moves(self):
        return [(r, c) for r in range(4) for c in range(4) if self.is_valid_move(r, c)]
    
    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row, col] = self.current_player
            self.current_player *= -1
            return True
        return False
    
    def is_game_over(self):
        return len(self.get_legal_moves()) == 0
    
    def evaluate(self):
        return len(self.get_legal_moves()) * self.current_player
    
    def minimax(self, depth, alpha, beta, maximizing):
        if self.is_game_over() or depth == 0:
            return self.evaluate(), None
        
        best_move = None
        legal_moves = self.get_legal_moves()
        
        if maximizing:
            max_eval = -float('inf')
            for move in legal_moves:
                self.make_move(*move)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board[move] = 0  
                self.current_player *= -1
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                self.make_move(*move)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board[move] = 0 
                self.current_player *= -1
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move
    
    def get_ai_move(self):
        _, best_move = self.minimax(4, -float('inf'), float('inf'), True)
        return best_move
    
    def print_board(self):
        print(self.board)
    

game = FourQueensGame()
while not game.is_game_over():
    game.print_board()
    if game.current_player == 1:
        row, col = map(int, input("Enter row and col: ").split())
    else:
        row, col = game.get_ai_move()
    if not game.make_move(row, col):
        print("Invalid move. Try again.")

game.print_board()
print("Game Over! Winner: Player", "1" if game.current_player == -1 else "2")