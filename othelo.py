from graphics import *
import copy

# grid settings
rows = 8
cols = 8
total_cells = rows * cols
moves_made = 4
wWidth = 800
wHeight = 800
cellWidth = wWidth // rows
cellHeight = wHeight // cols

EMPTY = -1
BLACK = 1
WHITE = 0


# n-ary Tree Node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.parent = None
        self.children = []

    def add_child(self, child):
        child_node = TreeNode(child)
        child_node.parent = self
        self.children.append(child_node)

    def add_children(self, children):
        children_nodes = [TreeNode(x) for x in children]
        for j in children_nodes:
            j.parent = self

        self.children = children_nodes


class State:
    def __init__(self, local_grid, blacks, whites, is_black, move):
        self.grid = local_grid
        self.black_cords = blacks
        self.white_cords = whites
        self.black_score = len(blacks)
        self.white_score = len(whites)
        self.black_turn = is_black
        self.move = move
        self.valid_moves = generate_valid_moves(self)


def generate_valid_moves(state: State):
    # extract info from current state
    grid = state.grid
    row = len(grid)
    col = len(grid[0])
    black = state.black_turn

    valid_moves = set()
    if black:
        for r, c in state.white_cords:
            # check vertical boundaries
            if r - 1 > -1 and r + 1 < row:
                # check vertical valid moves
                if grid[r - 1][c] == EMPTY:
                    start_ptr = r + 1
                    while start_ptr < row - 1 and grid[start_ptr][c] == WHITE:
                        start_ptr += 1

                    if grid[start_ptr][c] == BLACK:
                        valid_moves.add((r - 1, c))

                if grid[r + 1][c] == EMPTY:
                    start_ptr = r - 1
                    while start_ptr > 0 and grid[start_ptr][c] == WHITE:
                        start_ptr -= 1
                    if grid[start_ptr][c] == BLACK:
                        valid_moves.add((r + 1, c))

            # check horizontal boundaries
            if c - 1 > -1 and c + 1 < col:
                # check horizontal valid moves
                if grid[r][c - 1] == EMPTY:
                    start_ptr = c + 1
                    while start_ptr < col - 1 and grid[r][start_ptr] == WHITE:
                        start_ptr += 1

                    if grid[r][start_ptr] == BLACK:
                        valid_moves.add((r, c - 1))

                if grid[r][c + 1] == EMPTY:
                    start_ptr = c - 1
                    while start_ptr > 0 and grid[r][start_ptr] == WHITE:
                        start_ptr -= 1

                    if grid[r][start_ptr] == BLACK:
                        valid_moves.add((r, c + 1))

            # check diagonal boundaries
            if r - 1 > -1 and r + 1 < row and c - 1 > -1 and c + 1 < col:
                # check primary diagonal valid moves
                if grid[r - 1][c - 1] == EMPTY:
                    start_r = r + 1
                    start_c = c + 1
                    while start_r < row - 1 and start_c < col - 1 and grid[start_r][start_c] == WHITE:
                        start_r += 1
                        start_c += 1

                    if grid[start_r][start_c] == BLACK:
                        valid_moves.add((r - 1, c - 1))

                if grid[r + 1][c + 1] == EMPTY:
                    start_r = r - 1
                    start_c = c - 1
                    while start_r > 0 and start_c > 0 and grid[start_r][start_c] == WHITE:
                        start_r -= 1
                        start_c -= 1

                    if grid[start_r][start_c] == BLACK:
                        valid_moves.add((r + 1, c + 1))

                # check secondary diagonal valid moves
                if grid[r - 1][c + 1] == EMPTY:
                    start_r = r + 1
                    start_c = c - 1
                    while start_r < row - 1 and start_c > 0 and grid[start_r][start_c] == WHITE:
                        start_r += 1
                        start_c -= 1

                    if grid[start_r][start_c] == BLACK:
                        valid_moves.add((r - 1, c + 1))

                if grid[r + 1][c - 1] == EMPTY:
                    start_r = r - 1
                    start_c = c + 1
                    while start_r > 0 and start_c < col - 1 and grid[start_r][start_c] == WHITE:
                        start_r -= 1
                        start_c += 1

                    if grid[start_r][start_c] == BLACK:
                        valid_moves.add((r + 1, c - 1))
    # in case white player's turn
    else:
        for r, c in state.black_cords:
            # check vertical boundaries
            if r - 1 > -1 and r + 1 < row:
                # check vertical valid moves
                if grid[r - 1][c] == EMPTY:
                    start_ptr = r + 1
                    while start_ptr < row - 1 and grid[start_ptr][c] == BLACK:
                        start_ptr += 1

                    if grid[start_ptr][c] == WHITE:
                        valid_moves.add((r - 1, c))

                if grid[r + 1][c] == EMPTY:
                    start_ptr = r - 1
                    while start_ptr > 0 and grid[start_ptr][c] == BLACK:
                        start_ptr -= 1

                    if grid[start_ptr][c] == WHITE:
                        valid_moves.add((r + 1, c))

            # check horizontal boundaries
            if c - 1 > -1 and c + 1 < col:
                # check horizontal valid moves
                if grid[r][c - 1] == EMPTY:
                    start_ptr = c + 1
                    while start_ptr < col - 1 and grid[r][start_ptr] == BLACK:
                        start_ptr += 1

                    if grid[r][start_ptr] == WHITE:
                        valid_moves.add((r, c - 1))

                if grid[r][c + 1] == EMPTY:
                    start_ptr = c - 1
                    while start_ptr > 0 and grid[r][start_ptr] == BLACK:
                        start_ptr -= 1

                    if grid[r][start_ptr] == WHITE:
                        valid_moves.add((r, c + 1))

            # check diagonal boundaries
            if r - 1 > -1 and r + 1 < row and c - 1 > -1 and c + 1 < col:
                # check primary diagonal valid moves
                if grid[r - 1][c - 1] == EMPTY:
                    start_r = r + 1
                    start_c = c + 1
                    while start_r < row - 1 and start_c < col - 1 and grid[start_r][start_c] == BLACK:
                        start_r += 1
                        start_c += 1

                    if grid[start_r][start_c] == WHITE:
                        valid_moves.add((r - 1, c - 1))

                if grid[r + 1][c + 1] == EMPTY:
                    start_r = r - 1
                    start_c = c - 1
                    while start_r > 0 and start_c > 0 and grid[start_r][start_c] == BLACK:
                        start_r -= 1
                        start_c -= 1

                    if grid[start_r][start_c] == WHITE:
                        valid_moves.add((r + 1, c + 1))

                # check secondary diagonal valid moves
                if grid[r - 1][c + 1] == EMPTY:
                    start_r = r + 1
                    start_c = c - 1
                    while start_r < row - 1 and start_c > 0 and grid[start_r][start_c] == BLACK:
                        start_r += 1
                        start_c -= 1

                    if grid[start_r][start_c] == WHITE:
                        valid_moves.add((r - 1, c + 1))

                if grid[r + 1][c - 1] == EMPTY:
                    start_r = r - 1
                    start_c = c + 1
                    while start_r > 0 and start_c < col - 1 and grid[start_r][start_c] == BLACK:
                        start_r -= 1
                        start_c += 1

                    if grid[start_r][start_c] == WHITE:
                        valid_moves.add((r + 1, c - 1))

    return valid_moves


def generate_child(curr_state: State, move):
    # extract info from current state
    grid = curr_state.grid
    local_grid = copy.deepcopy(grid)
    row = len(grid)
    col = len(grid[0])
    black_balls = copy.deepcopy(curr_state.black_cords)
    white_balls = copy.deepcopy(curr_state.white_cords)
    black = curr_state.black_turn
    [r, c] = move

    if black:
        local_grid[r][c] = BLACK
        black_balls.append((r, c))

        # check up boundary
        if r - 1 > -1:
            # check above for white
            if grid[r - 1][c] == WHITE:
                start_ptr = r - 1
                while start_ptr > 0 and grid[start_ptr][c] == WHITE:
                    start_ptr -= 1

                if grid[start_ptr][c] == BLACK:
                    end_ptr = start_ptr
                    start_ptr = r - 1

                    while start_ptr != end_ptr:
                        local_grid[start_ptr][c] = BLACK
                        white_balls.remove((start_ptr, c))
                        black_balls.append((start_ptr, c))
                        start_ptr -= 1
        # check down boundary
        if r + 1 < row:
            # check below for white
            if grid[r + 1][c] == WHITE:
                start_ptr = r + 1
                while start_ptr < row - 1 and grid[start_ptr][c] == WHITE:
                    start_ptr += 1

                if grid[start_ptr][c] == BLACK:
                    end_ptr = start_ptr
                    start_ptr = r + 1

                    while start_ptr != end_ptr:
                        local_grid[start_ptr][c] = BLACK
                        white_balls.remove((start_ptr, c))
                        black_balls.append((start_ptr, c))
                        start_ptr += 1
        # check left boundary
        if c - 1 > -1:
            # check left for white
            if grid[r][c - 1] == WHITE:
                start_ptr = c - 1
                while start_ptr > 0 and grid[r][start_ptr] == WHITE:
                    start_ptr -= 1

                if grid[r][start_ptr] == BLACK:
                    end_ptr = start_ptr
                    start_ptr = c - 1

                    while start_ptr != end_ptr:
                        local_grid[r][start_ptr] = BLACK
                        white_balls.remove((r, start_ptr))
                        black_balls.append((r, start_ptr))
                        start_ptr -= 1
        # check right boundary
        if c + 1 < col:
            # check right for white
            if grid[r][c + 1] == WHITE:
                start_ptr = c + 1
                while start_ptr < col - 1 and grid[r][start_ptr] == WHITE:
                    start_ptr += 1

                if grid[r][start_ptr] == BLACK:
                    end_ptr = start_ptr
                    start_ptr = c + 1

                    while start_ptr != end_ptr:
                        local_grid[r][start_ptr] = BLACK
                        white_balls.remove((r, start_ptr))
                        black_balls.append((r, start_ptr))
                        start_ptr += 1
        # check upper left boundary
        if r - 1 > -1 and c - 1 > -1:
            # check upper left for white
            if grid[r - 1][c - 1] == WHITE:
                start_r = r - 1
                start_c = c - 1
                while start_r > 0 and start_c > 0 and grid[start_r][start_c] == WHITE:
                    start_r -= 1
                    start_c -= 1

                if grid[start_r][start_c] == BLACK:
                    end_r = start_r
                    end_c = start_c
                    start_r = r - 1
                    start_c = c - 1

                    while start_r != end_r and start_c != end_c:
                        local_grid[start_r][start_c] = BLACK
                        white_balls.remove((start_r, start_c))
                        black_balls.append((start_r, start_c))
                        start_r -= 1
                        start_c -= 1
        # check lower right boundary
        if r + 1 < row and c + 1 < col:
            # check lower right for white
            if grid[r + 1][c + 1] == WHITE:
                start_r = r + 1
                start_c = c + 1
                while start_r < row - 1 and start_c < col - 1 and grid[start_r][start_c] == WHITE:
                    start_r += 1
                    start_c += 1

                if grid[start_r][start_c] == BLACK:
                    end_r = start_r
                    end_c = start_c
                    start_r = r + 1
                    start_c = c + 1

                    while start_r != end_r and start_c != end_c:
                        local_grid[start_r][start_c] = BLACK
                        white_balls.remove((start_r, start_c))
                        black_balls.append((start_r, start_c))
                        start_r += 1
                        start_c += 1
        # check upper right boundary
        if r - 1 > -1 and c + 1 < col:
            # check upper right for white
            if grid[r - 1][c + 1] == WHITE:
                start_r = r - 1
                start_c = c + 1
                while start_r > 0 and start_c < col - 1 and grid[start_r][start_c] == WHITE:
                    start_r -= 1
                    start_c += 1

                if grid[start_r][start_c] == BLACK:
                    end_r = start_r
                    end_c = start_c
                    start_r = r - 1
                    start_c = c + 1

                    while start_r != end_r and start_c != end_c:
                        local_grid[start_r][start_c] = BLACK
                        white_balls.remove((start_r, start_c))
                        black_balls.append((start_r, start_c))
                        start_r -= 1
                        start_c += 1
        # check lower left boundary
        if r + 1 < row and c - 1 > - 1:
            # check lower left for white
            if grid[r + 1][c - 1] == WHITE:
                start_r = r + 1
                start_c = c - 1
                while start_r < row - 1 and start_c > 0 and grid[start_r][start_c] == WHITE:
                    start_r += 1
                    start_c -= 1

                if grid[start_r][start_c] == BLACK:
                    end_r = start_r
                    end_c = start_c
                    start_r = r + 1
                    start_c = c - 1

                    while start_r != end_r and start_c != end_c:
                        local_grid[start_r][start_c] = BLACK
                        white_balls.remove((start_r, start_c))
                        black_balls.append((start_r, start_c))
                        start_r += 1
                        start_c -= 1

    # in case its white's turn
    else:
        local_grid[r][c] = WHITE
        white_balls.append((r, c))
        # check up boundary
        if r - 1 > -1:
            # check above for black
            if grid[r - 1][c] == BLACK:
                start_ptr = r - 1
                while start_ptr > 0 and grid[start_ptr][c] == BLACK:
                    start_ptr -= 1

                if grid[start_ptr][c] == WHITE:
                    end_ptr = start_ptr
                    start_ptr = r - 1

                    while start_ptr != end_ptr:
                        local_grid[start_ptr][c] = WHITE
                        black_balls.remove((start_ptr, c))
                        white_balls.append((start_ptr, c))
                        start_ptr -= 1
        # check down boundary
        if r + 1 < row:
            # check below for black
            if grid[r + 1][c] == BLACK:
                start_ptr = r + 1
                while start_ptr < row - 1 and grid[start_ptr][c] == BLACK:
                    start_ptr += 1

                if grid[start_ptr][c] == WHITE:
                    end_ptr = start_ptr
                    start_ptr = r + 1

                    while start_ptr != end_ptr:
                        local_grid[start_ptr][c] = WHITE
                        black_balls.remove((start_ptr, c))
                        white_balls.append((start_ptr, c))
                        start_ptr += 1
        # check left boundary
        if c - 1 > -1:
            # check left for black
            if grid[r][c - 1] == BLACK:
                start_ptr = c - 1
                while start_ptr > 0 and grid[r][start_ptr] == BLACK:
                    start_ptr -= 1

                if grid[r][start_ptr] == WHITE:
                    end_ptr = start_ptr
                    start_ptr = c - 1

                    while start_ptr != end_ptr:
                        local_grid[r][start_ptr] = WHITE
                        black_balls.remove((r, start_ptr))
                        white_balls.append((r, start_ptr))
                        start_ptr -= 1
        # check right boundary
        if c + 1 < col:
            # check right for black
            if grid[r][c + 1] == BLACK:
                start_ptr = c + 1
                while start_ptr < col - 1 and grid[r][start_ptr] == BLACK:
                    start_ptr += 1

                if grid[r][start_ptr] == WHITE:
                    end_ptr = start_ptr
                    start_ptr = c + 1

                    while start_ptr != end_ptr:
                        local_grid[r][start_ptr] = WHITE
                        black_balls.remove((r, start_ptr))
                        white_balls.append((r, start_ptr))
                        start_ptr += 1
        # check upper left boundary
        if r - 1 > -1 and c - 1 > -1:
            # check upper left for black
            if grid[r - 1][c - 1] == BLACK:
                start_r = r - 1
                start_c = c - 1
                while start_r > 0 and start_c > 0 and grid[start_r][start_c] == BLACK:
                    start_r -= 1
                    start_c -= 1

                if grid[start_r][start_c] == WHITE:
                    end_r = start_r
                    end_c = start_c
                    start_r = r - 1
                    start_c = c - 1

                    while start_r != end_r and start_c != end_c:
                        local_grid[start_r][start_c] = WHITE
                        black_balls.remove((start_r, start_c))
                        white_balls.append((start_r, start_c))
                        start_r -= 1
                        start_c -= 1
        # check lower right boundary
        if r + 1 < row and c + 1 < col:
            # check lower right for black
            if grid[r + 1][c + 1] == BLACK:
                start_r = r + 1
                start_c = c + 1
                while start_r < row - 1 and start_c < col - 1 and grid[start_r][start_c] == BLACK:
                    start_r += 1
                    start_c += 1

                if grid[start_r][start_c] == WHITE:
                    end_r = start_r
                    end_c = start_c
                    start_r = r + 1
                    start_c = c + 1

                    while start_r != end_r and start_c != end_c:
                        local_grid[start_r][start_c] = WHITE
                        black_balls.remove((start_r, start_c))
                        white_balls.append((start_r, start_c))
                        start_r += 1
                        start_c += 1
        # check upper right boundary
        if r - 1 > -1 and c + 1 < col:
            # check upper right for black
            if grid[r - 1][c + 1] == BLACK:
                start_r = r - 1
                start_c = c + 1
                while start_r > 0 and start_c < col - 1 and grid[start_r][start_c] == BLACK:
                    start_r -= 1
                    start_c += 1

                if grid[start_r][start_c] == WHITE:
                    end_r = start_r
                    end_c = start_c
                    start_r = r - 1
                    start_c = c + 1

                    while start_r != end_r and start_c != end_c:
                        local_grid[start_r][start_c] = WHITE
                        black_balls.remove((start_r, start_c))
                        white_balls.append((start_r, start_c))
                        start_r -= 1
                        start_c += 1
        # check lower left boundary
        if r + 1 < row and c - 1 > - 1:
            # check lower left for black
            if grid[r + 1][c - 1] == BLACK:
                start_r = r + 1
                start_c = c - 1
                while start_r < row - 1 and start_c > 0 and grid[start_r][start_c] == BLACK:
                    start_r += 1
                    start_c -= 1

                if grid[start_r][start_c] == WHITE:
                    end_r = start_r
                    end_c = start_c
                    start_r = r + 1
                    start_c = c - 1

                    while start_r != end_r and start_c != end_c:
                        local_grid[start_r][start_c] = WHITE
                        black_balls.remove((start_r, start_c))
                        white_balls.append((start_r, start_c))
                        start_r += 1
                        start_c -= 1

    child_state: State = State(local_grid, black_balls, white_balls, not black, (r, c))

    return child_state


def generate_successors(parent: TreeNode):
    curr_state: State = parent.val

    valid_moves = generate_valid_moves(curr_state)

    children = [generate_child(curr_state, (r, c)) for r, c in valid_moves]

    parent.add_children(children)


def evaluation(curr_state: State):
    return curr_state.black_score - curr_state.white_score


def mini_max(root: TreeNode, depth, alpha, beta, maximizing_player):

    if depth == 0:
        return evaluation(root.val), root.val

    generate_successors(root)

    if maximizing_player:
        max_eval = float('-inf')
        next_move_state = None
        for child in root.children:
            [curr_eval, _] = mini_max(child, depth - 1, alpha, beta, not maximizing_player)
            if curr_eval > max_eval:
                max_eval = curr_eval
                next_move_state = child.val

            alpha = max(alpha, curr_eval)
            if beta <= alpha:
                break
        return max_eval, next_move_state
    else:
        min_eval = float('inf')
        next_move_state = None
        for child in root.children:
            [curr_eval, _] = mini_max(child, depth - 1, alpha, beta, not maximizing_player)
            if curr_eval < min_eval:
                min_eval = curr_eval
                next_move_state = child.val

            beta = min(beta, curr_eval)
            if beta <= alpha:
                break

        return min_eval, next_move_state


def show_hints(valid_moves, circles):
    for point in valid_moves:
        circles[point[1]][point[0]].setFill(color_rgb(100, 0, 0))


def remove_hints(valid_moves, circles):
    for point in valid_moves:
        circles[point[1]][point[0]].setFill(color_rgb(255, 255, 255))


def move(grid, r, c, player):
    grid[r][c] = player
    return grid


def updateGraphics(grid, circles):
    for idx, col in enumerate(grid):
        for jdx, cell in enumerate(col):
            if cell == 1:
                circles[jdx][idx].setFill(color_rgb(0, 0, 0))
            elif cell == 0:
                circles[jdx][idx].setFill(color_rgb(100, 100, 100))
    update()


def mouseToGrid(mouse_click):
    return int(mouse_click.getY() / cellWidth), int(mouse_click.getX() / cellWidth)


def main():
    # setup initial grid
    global moves_made
    win = GraphWin("w", wWidth, wHeight)
    win.setBackground('white')
    for i in range(cols):
        Line(Point(i * cellWidth, 0), Point(i * cellWidth, wHeight)).draw(win)
        Line(Point(0, i * cellHeight), Point(wHeight, i * cellHeight)).draw(win)
    grid = [[EMPTY for i in range(cols)] for j in range(rows)]
    grid[(rows // 2) - 1][(cols // 2) - 1] = 1
    grid[(rows // 2)][(cols // 2)] = 1
    grid[(rows // 2)][(cols // 2) - 1] = 0
    grid[(rows // 2) - 1][(cols // 2)] = 0

    circles = []
    for i in range(cols):
        circles.append([])
        for j in range(rows):
            mid_point = Point((cellWidth / 2) + cellWidth * i, (cellHeight / 2) + cellHeight * j)
            new_circle = Circle(mid_point, cellHeight * 0.8 / 2)
            new_circle.draw(win)
            circles[i].append(new_circle)
    updateGraphics(grid, circles)
    prev_grid = grid

    blacks = [((rows // 2) - 1, (cols // 2) - 1), (rows // 2, (cols // 2))]
    whites = [(rows // 2, (cols // 2) - 1), ((rows // 2) - 1, cols // 2)]
    black_turn = True
    initial_move = (None, None)
    initial_state: State = State(grid, blacks, whites, black_turn, initial_move)

    while win.checkKey() != 'Escape':
        if len(initial_state.valid_moves) == 0:
            break
        if initial_state.black_turn:  # Ai's turn
            [state_cost, next_state] = mini_max(TreeNode(initial_state), 3, float('-inf'), float('inf'), black_turn)
            initial_state = next_state
            if len(initial_state.valid_moves) == 0:
                initial_state.black_turn = not initial_state.black_turn
                initial_state.valid_moves = generate_valid_moves(initial_state)
            updateGraphics(initial_state.grid, circles)
        else:

            show_hints(initial_state.valid_moves, circles)
            mouse_click = win.checkMouse()
            if type(mouse_click) == Point:
                r, c = mouseToGrid(mouse_click)

                if (r, c) in initial_state.valid_moves:
                    remove_hints(initial_state.valid_moves, circles)

                    initial_state = generate_child(initial_state, [r, c])
                    if len(initial_state.valid_moves) == 0:
                        initial_state.black_turn = not initial_state.black_turn
                        initial_state.valid_moves = generate_valid_moves(initial_state)

                    updateGraphics(initial_state.grid, circles)
                # black_turn = black_turn

    print(initial_state.black_score)
    print(initial_state.white_score)
    win.getKey()
    win.close()


main()
