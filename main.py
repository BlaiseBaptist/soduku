import pandas as pd
import time
import copy


class Sudoku:
    def __init__(self, board):
        for _ in range(9 - len(board)):
            board.append([None] * 9)
        for i in range(9):
            for j in range(9 - len(board[i])):
                board[i].append(None)
        self.board = board

    def __str__(self):
        str_board = ""
        vert_sep = "│"
        horz_sep = "─"
        for i in range(9):
            if i % 3 == 0:
                str_board += "\n"
                str_board += horz_sep * 19
            str_board += "\n"
            for j in range(9):
                if j % 3 == 0:
                    str_board += vert_sep
                else:
                    str_board += " "
                value = self.board[i][j]
                if value is None:
                    value = " "
                str_board += str(value)
            str_board += vert_sep
        str_board += "\n"
        str_board += horz_sep * 19
        return str_board

    def check(self):
        for i in range(9):
            horz_line = self[i]
            if not check_line(horz_line):
                return False
            vert_line = self[i:i + 1, ::]
            if not check_line(flatten(vert_line)):
                return False
            block = self[i % 3 * 3:i % 3 * 3 + 3, i // 3 * 3:i // 3 * 3 + 3]
            if not check_line(flatten(block)):
                return False
        return True

    def __getitem__(self, items):
        if isinstance(items, tuple):
            return list(map(lambda x: x[items[0]], self.board[items[1]]))
        return self.board[items]

    def __setitem__(self, key, value):
        self.board[key[1]][key[0]] = value

    def logic_solve(self):
        check = 0
        while not self.check():
            check += 1
            if check > 100:
                return self
            for y in range(9):
                for x in range(9):
                    if self[x:x + 1, y:y + 1][0][0] is not None:
                        continue
                    missing = self.get_missing(x, y)
                    if len(missing) == 1:
                        self.board[y][x] = missing.pop()
        return self

    def back_solve(self, cell=0):
        while self[cell % 9:cell % 9 + 1, cell // 9:, cell // 9 + 1][0][0] is not None:
            cell += 1
            if cell == 81:
                return True
        x = cell % 9
        y = cell // 9
        missing = self.get_missing(x, y)
        new_board = copy.deepcopy(self)
        for i in missing:
            new_board[x, y] = i
            if new_board.back_solve(cell):
                self.board = new_board.board
                return True
        return False

    def get_missing(self, x, y):
        horz = set(self[y])
        block = set(flatten(self[x // 3 * 3:x // 3 * 3 + 3, y // 3 * 3:y // 3 * 3 + 3]))
        vert = set(flatten(self[x:x + 1, 0:]))
        missing = set(range(1, 10))
        missing -= block
        missing -= horz
        missing -= vert
        return missing


def check_line(line):
    num = dict.fromkeys(line, None)
    test_case = dict.fromkeys(range(1, 10), None)
    return test_case == num


def flatten(xss):
    return [x for xs in xss for x in xs]


def parse(board):
    lines = []
    for y in range(9):
        line = []
        for x in range(9):
            num = board[9 * y + x]
            if num == '.':
                num = None
            else:
                num = int(num)
            line.append(num)
        lines.append(line)
    return lines


def main():
    data = pd.read_csv("sudoku-3m.csv")
    print(data.dtypes)
    boards = data["puzzle"]
    count = 1000
    for x in range(count, len(boards)):
        count += 1
        diff = data["difficulty"]
        b = Sudoku(parse(boards[x]))
        start = time.time()
        b.logic_solve()
        b.back_solve()
        out = "board " + str(count) + " took " + str(round(time.time() - start, 5)) + "s. difficulty was " + str(
            diff[x])
        print(out)


def test():
    a = parse("...81.....2........1.9..7...7..25.934.2............5...975.....563.....4......68.")
    s = parse("934817256728653419615942738176425893452398167389176542897564321563281974241739685")
    s = Sudoku(s)
    a = Sudoku(a)
    a.back_solve()
    print(s)
    print(s.check())


main()
