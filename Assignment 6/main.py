import time
import random
# from curses import wrapper
import curses

# Generate the board
def generateBoard():
    arr = []

    rows, cols = (32, 62)
    arr.clear()
    for i in range(cols):
        col = []

        for j in range(rows):
            col.append(0)

        arr.append(col)

    return arr


def randomizeBoard(arr):
    for i in range(2, 30):
        lastresult = 0
        cumulation = 0.0
        for j in range(2, 60):
            result = random.randrange(10)
            if lastresult == 1:
                result -= 1
            else:
                result += 1
            result += cumulation

            if result < 2:
                arr[j][i] = 1
                lastresult = 1
                cumulation += 0.1
            else:
                arr[j][i] = 0
                lastresult = 0

    return arr


def drawScreen(stdscr, arr, rx, ry):
    for y in range(0, ry):
        for x in range(0, rx):
            try:
                if x == 0 or x == rx - 1:
                    if y == 0 or y == ry - 1:
                        stdscr.addstr(x, y, "+")
                    else:
                        stdscr.addstr(x, y, "-")
                elif y == 0 or y == ry - 1:
                    stdscr.addstr(x, y, "|")
                elif 0 < y < ry - 1:
                    stdscr.addstr(x, y, "#") if arr[y][x] == 1 else stdscr.addstr(x, y, " ")
            except curses.error:
                pass


def drawExtras(stdscr, rx, ry, icount):
    # Draw Iteration Counter
    stdscr.addstr(rx, 0, "| Iteration: " + str(icount))
    stdscr.addstr(rx, ry - 1, "|")
    for y in range(0, ry):
        if y == 0 or y == ry - 1:
            stdscr.addstr(rx + 1, y, "+")
        else:
            stdscr.addstr(rx + 1, y, "-")

    # Draw ESC exit help
    helptext = "Ctr + C to exit "
    stdscr.addstr(rx, ry - len(helptext) - 1, helptext)



def iterateBoard(arr, rx, ry):
    board = generateBoard()

    for y in range(1, ry - 1):
        for x in range(1, rx - 1):
            neighbors = 0
            # Above this cell
            neighbors += arr[y - 1][x - 1] + arr[y - 1][x] + arr[y - 1][x + 1]
            # On this cell's row
            neighbors += arr[y][x - 1] + arr[y][x + 1]
            # Below this cell
            neighbors += arr[y + 1][x - 1] + arr[y + 1][x] + arr[y + 1][x + 1]

            if arr[y][x] == 1:
                if 2 <= neighbors <= 3:
                    board[y][x] = 1
            else:
                if neighbors == 3:
                    board[y][x] = 1
    return board


# generateBoard()
# printBoard()
# print(len(arr))
# print(len(arr[0]))

def main(stdscr):
    # Generate Board
    board = randomizeBoard(generateBoard())

    count = 1

    # Print board
    drawScreen(stdscr, board, 32, 62)
    drawExtras(stdscr, 32, 62, count)

    stdscr.refresh()
    # stdscr.getkey()
    loop = True

    while loop:
        # key = stdscr.getch()
        # if key == 0x1b:
        #     loop = False
        #     break

        # Clear screen
        stdscr.clear()

        # Update Board
        board = iterateBoard(board, 32, 62)
        count += 1

        # Print board
        drawScreen(stdscr, board, 32, 62)
        drawExtras(stdscr, 32, 62, count)

        stdscr.refresh()
        # stdscr.getkey()

        time.sleep(0.1)


# generateBoard()
# printBoard()
# for _ in range(30):
#     count = iterateBoard(count)
#     printBoard()
#     print()

#     time.sleep(0.25)

curses.wrapper(main)
#curses.endwin()
