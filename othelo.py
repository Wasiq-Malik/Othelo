from graphics import *

# grid settings
rows = 10
cols = 10
wWidth = 800
wHeight = 800
cellWidth = wWidth // rows
cellHeight = wHeight // cols


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
    def __init__(self, local_grid, blacks, whites, is_black):
        self.grid = local_grid
        self.black_cords = blacks
        self.white_cords = whites
        self.black_score = len(blacks)
        self.white_score = len(whites)
        self.black_turn = is_black


def generate_valid_moves(state: State):
    # extract info from current state
    grid = state.grid
    row = len(grid)
    col = len(grid[0])
    black = state.black_turn

    valid_moves = []
    if black:
        for r, c in state.white_cords:
            # check vertical boundaries
            if r - 1 > -1 and r + 1 < row:
                # check vertical valid moves
                if grid[r - 1][c] is None and grid[r + 1][c] is black:
                    valid_moves.append((r - 1, c))

                if grid[r - 1][c] is black and grid[r + 1][c] is None:
                    valid_moves.append((r + 1, c))

            # check horizontal boundaries
            if c - 1 > -1 and c + 1 < col:
                # check horizontal valid moves
                if grid[r][c - 1] is None and grid[r][c + 1] is black:
                    valid_moves.append((r, c - 1))

                if grid[r][c - 1] is black and grid[r][c + 1] is None:
                    valid_moves.append((r, c + 1))

            # check diagonal boundaries
            if r - 1 > -1 and r + 1 < row and c - 1 > -1 and c + 1 < col:
                # check primary diagonal valid moves
                if grid[r - 1][c - 1] is None and grid[r + 1][c + 1] is black:
                    valid_moves.append((r - 1, c - 1))

                if grid[r - 1][c - 1] is black and grid[r + 1][c + 1] is None:
                    valid_moves.append((r + 1, c + 1))

                # check secondary diagonal valid moves
                if grid[r - 1][c + 1] is None and grid[r + 1][c - 1] is black:
                    valid_moves.append((r - 1, c + 1))

                if grid[r - 1][c + 1] is black and grid[r + 1][c - 1] is None:
                    valid_moves.append((r + 1, c - 1))
    # in case white player's turn
    else:
        for r, c in state.black_cords:
            # check vertical boundaries
            if r - 1 > -1 and r + 1 < row:
                # check vertical valid moves
                if grid[r - 1][c] is None and grid[r + 1][c] is not black:
                    valid_moves.append((r - 1, c))

                if grid[r - 1][c] is not black and grid[r + 1][c] is None:
                    valid_moves.append((r + 1, c))

            # check horizontal boundaries
            if c - 1 > -1 and c + 1 < col:
                # check horizontal valid moves
                if grid[r][c - 1] is None and grid[r][c + 1] is not black:
                    valid_moves.append((r, c - 1))

                if grid[r][c - 1] is not black and grid[r][c + 1] is None:
                    valid_moves.append((r, c + 1))

            # check diagonal boundaries
            if r - 1 > -1 and r + 1 < row and c - 1 > -1 and c + 1 < col:
                # check primary diagonal valid moves
                if grid[r - 1][c - 1] is None and grid[r + 1][c + 1] is not black:
                    valid_moves.append((r - 1, c - 1))

                if grid[r - 1][c - 1] is not black and grid[r + 1][c + 1] is None:
                    valid_moves.append((r + 1, c + 1))

                # check secondary diagonal valid moves
                if grid[r - 1][c + 1] is None and grid[r + 1][c - 1] is not black:
                    valid_moves.append((r - 1, c + 1))

                if grid[r - 1][c + 1] is not black and grid[r + 1][c - 1] is None:
                    valid_moves.append((r + 1, c - 1))

    return valid_moves


def generate_child(curr_state: State, move):
    # extract info from current state
    grid = curr_state.grid.copy()
    row = len(grid)
    col = len(grid[0])
    black_balls: list = curr_state.black_cords.copy()
    white_balls: list = curr_state.white_cords.copy()
    black = curr_state.black_turn
    [r, c] = move

    if black:
        grid[r][c] = black
        black_balls.append((r, c))

        # check up boundary
        if r - 1 > -1:
            # check above for white
            if grid[r - 1][c] is not black:
                start_ptr = r - 1
                while start_ptr > -1 and grid[start_ptr][c] is not black:
                    start_ptr -= 1

                if grid[start_ptr][c] is black:
                    end_ptr = start_ptr
                    start_ptr = r - 1

                    while start_ptr is not end_ptr:
                        grid[start_ptr][c] = black
                        white_balls.remove((start_ptr, c))
                        black_balls.append((start_ptr, c))
                        start_ptr -= 1
        # check down boundary
        if r + 1 > row:
            # check below for white
            if grid[r + 1][c] is not black:
                start_ptr = r + 1
                while start_ptr < row and grid[start_ptr][c] is not black:
                    start_ptr += 1

                if grid[start_ptr][c] is black:
                    end_ptr = start_ptr
                    start_ptr = r + 1

                    while start_ptr is not end_ptr:
                        grid[start_ptr][c] = black
                        white_balls.remove((start_ptr, c))
                        black_balls.append((start_ptr, c))
                        start_ptr += 1
        # check left boundary
        if c - 1 > -1:
            # check left for white
            if grid[r][c - 1] is not black:
                start_ptr = c - 1
                while start_ptr > -1 and grid[r][start_ptr] is not black:
                    start_ptr -= 1

                if grid[r][start_ptr] is black:
                    end_ptr = start_ptr
                    start_ptr = c - 1

                    while start_ptr is not end_ptr:
                        grid[r][start_ptr] = black
                        white_balls.remove((r, start_ptr))
                        black_balls.append((r, start_ptr))
                        start_ptr -= 1
        # check right boundary
        if c + 1 < col:
            # check right for white
            if grid[r][c + 1] is not black:
                start_ptr = c + 1
                while start_ptr < col and grid[r][start_ptr] is not black:
                    start_ptr += 1

                if grid[r][start_ptr] is black:
                    end_ptr = start_ptr
                    start_ptr = c + 1

                    while start_ptr is not end_ptr:
                        grid[r][start_ptr] = black
                        white_balls.remove((r, start_ptr))
                        black_balls.append((r, start_ptr))
                        start_ptr += 1


   # else:


def generate_successors(parent: TreeNode):
    curr_state: State = parent.val

    valid_moves = generate_valid_moves(curr_state)


def updateColors(grid):
    return grid


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
    win = GraphWin("w", wWidth, wHeight)
    win.setBackground('white')
    for i in range(cols):
        Line(Point(i * cellWidth, 0), Point(i * cellWidth, wHeight)).draw(win)
        Line(Point(0, i * cellHeight), Point(wHeight, i * cellHeight)).draw(win)
    grid = [[None for i in range(cols)] for j in range(rows)]
    grid[(rows // 2) - 1][(cols // 2) - 1] = 1
    grid[(rows // 2)][(cols // 2)] = 1
    grid[(rows // 2)][(cols // 2) - 1] = 0
    grid[(rows // 2) - 1][(cols // 2)] = 0

    circles = []
    for i in range(cols):
        circles.append([])
        for j in range(rows):
            midPoint = Point((cellWidth / 2) + cellWidth * i, (cellHeight / 2) + cellHeight * j)
            newCircle = Circle(midPoint, cellHeight * 0.8 / 2)
            newCircle.draw(win)
            circles[i].append(newCircle)
    updateGraphics(grid, circles)
    prevGrid = grid

    blackTurn = True
    while win.checkKey() != 'Escape':
        mouseClick = win.getMouse()
        if type(mouseClick) == Point:
            r, c = mouseToGrid(mouseClick)
            grid = move(grid, r, c, int(blackTurn))
            updateGraphics(grid, circles)
            blackTurn = not blackTurn

    win.close()


main()
