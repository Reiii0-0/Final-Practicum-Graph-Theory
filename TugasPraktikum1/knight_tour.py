class KnightTourLogic:
    def __init__(self, board_size=8):
        self.n = board_size
        self.path = [] 
        self.current_step_index = -1 
        self.is_solved = False
        self.is_generating = False

    def is_valid_move(self, x, y, board):
        return 0 <= x < self.n and 0 <= y < self.n and board[y][x] == -1

    def get_legal_moves(self, x, y, board):
        moves = [
            (x + 1, y + 2), (x + 1, y - 2),
            (x - 1, y + 2), (x - 1, y - 2),
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 2, y + 1), (x - 2, y - 1)
        ]
        valid_moves = []
        for nx, ny in moves:
            if self.is_valid_move(nx, ny, board):
                valid_moves.append((nx, ny))
        return valid_moves

    def solve_tour(self, start_x, start_y):
        self.path = []
        self.current_step_index = 0
        self.is_solved = False
        
        # Board sementara untuk kalkulasi
        temp_board = [[-1 for _ in range(self.n)] for _ in range(self.n)]
        
        curr_x, curr_y = start_x, start_y
        temp_board[curr_y][curr_x] = 0
        self.path.append((curr_x, curr_y))
        
        step = 1
        keep_searching = True
        
        while keep_searching:
            moves = self.get_legal_moves(curr_x, curr_y, temp_board)
            if not moves:
                keep_searching = False
                break
            
            # Warnsdorff's Rule
            best_move = None
            min_degree = 9
            
            for mx, my in moves:
                degree = len(self.get_legal_moves(mx, my, temp_board))
                if degree < min_degree:
                    min_degree = degree
                    best_move = (mx, my)
            
            if best_move:
                curr_x, curr_y = best_move
                temp_board[curr_y][curr_x] = step
                self.path.append((curr_x, curr_y))
                step += 1
            else:
                keep_searching = False

        self.is_solved = True
        return len(self.path)

    # Navigasi
    def next_step(self):
        if self.current_step_index < len(self.path) - 1:
            self.current_step_index += 1

    def prev_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            
    def go_to_start(self):
        self.current_step_index = 0
        
    def go_to_end(self):
        self.current_step_index = len(self.path) - 1

    def get_current_state(self):
        return {
            "path": self.path,
            "current_idx": self.current_step_index,
            "is_solved": self.is_solved,
            "total_steps": len(self.path)
        }