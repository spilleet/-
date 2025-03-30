import random

class TicTacToeGame:
    def __init__(self):
        # 3x3 보드를 공백으로 초기화합니다.
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = None  # 'X': 사용자, 'O': 컴퓨터

    def show_board(self):
        # 보드 상태를 출력합니다.
        print("\n    0   1   2")
        print("  -------------")
        for i, row in enumerate(self.board):
            print(f"{i} | " + " | ".join(row) + " |")
            print("  -------------")
        print("")

    def check_victory(self, marker):
        # 가로 줄 검사
        for row in self.board:
            if all(cell == marker for cell in row):
                return True
        # 세로 줄 검사
        for col in range(3):
            if all(self.board[row][col] == marker for row in range(3)):
                return True
        # 대각선 검사
        if all(self.board[i][i] == marker for i in range(3)):
            return True
        if all(self.board[i][2 - i] == marker for i in range(3)):
            return True
        return False

    def board_full(self):
        # 보드의 모든 칸이 채워졌는지 확인합니다.
        return all(cell != ' ' for row in self.board for cell in row)

    def get_empty_positions(self):
        # 빈 칸의 좌표를 리스트로 반환합니다.
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ' ']

    def human_turn(self):
        # 사용자가 올바른 좌표를 입력할 때까지 반복합니다.
        while True:
            try:
                move = input("당신의 턴입니다. 행과 열 번호를 띄어쓰기로 구분하여 입력하세요 (예: 0 1): ")
                r, c = map(int, move.split())
                if r not in range(3) or c not in range(3):
                    print("행과 열은 0부터 2 사이여야 합니다.")
                    continue
                if self.board[r][c] != ' ':
                    print("이미 선택된 칸입니다. 다른 칸을 골라주세요.")
                    continue
                self.board[r][c] = 'X'
                break
            except ValueError:
                print("입력이 올바르지 않습니다. 숫자 두 개를 입력해주세요.")

    def computer_turn(self):
        # 컴퓨터가 이길 수 있는 수가 있는지 확인
        for r, c in self.get_empty_positions():
            self.board[r][c] = 'O'
            if self.check_victory('O'):
                print("컴퓨터가 승리할 수 있는 수를 선택했습니다.")
                return
            self.board[r][c] = ' '  # 원상 복구
        
        # 사용자의 승리 가능성을 막는 수가 있는지 확인
        for r, c in self.get_empty_positions():
            self.board[r][c] = 'X'
            if self.check_victory('X'):
                self.board[r][c] = 'O'
                print("컴퓨터가 사용자의 승리 수를 막았습니다.")
                return
            self.board[r][c] = ' '
        
        # 중앙을 선점 (가능하면)
        if self.board[1][1] == ' ':
            self.board[1][1] = 'O'
            return
        
        # 코너 칸 중 하나 선택
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [pos for pos in corners if self.board[pos[0]][pos[1]] == ' ']
        if available_corners:
            r, c = random.choice(available_corners)
            self.board[r][c] = 'O'
            return
        
        # 남은 빈 칸 중에서 무작위로 선택
        r, c = random.choice(self.get_empty_positions())
        self.board[r][c] = 'O'

    def play(self):
        print("틱택토 게임을 시작합니다!")
        self.show_board()
        # 선 플레이어를 랜덤으로 결정합니다.
        self.current_player = random.choice(['X', 'O'])
        if self.current_player == 'X':
            print("당신이 먼저 시작합니다.")
        else:
            print("컴퓨터가 먼저 시작합니다.")
        
        while True:
            if self.current_player == 'X':
                self.human_turn()
            else:
                self.computer_turn()
            self.show_board()
            
            if self.check_victory('X'):
                print("당신이 승리했습니다!")
                break
            if self.check_victory('O'):
                print("컴퓨터가 승리했습니다.")
                break
            if self.board_full():
                print("무승부입니다!")
                break
            
            # 플레이어 전환
            self.current_player = 'O' if self.current_player == 'X' else 'X'

if __name__ == "__main__":
    game = TicTacToeGame()
    game.play()