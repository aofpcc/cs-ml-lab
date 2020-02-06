import time
import random

# samples = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 ]
samples = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# wins = [ [1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [1, 5, 9, 13],
# [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16], [1, 6, 11, 16], [4, 7, 10, 13] ]

wins = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9],
        [1, 5, 9], [7, 5, 3]]

win_count = [0, 0, 0, 0]

def divide(currentMove):
    if len(currentMove) > 0:
        return [currentMove[::2], currentMove[1::2]]
    return [currentMove[::2], []]


def check_win(divided):
    first = divided[0]
    second = divided[1]

    for win in wins:
        first_win = all(e in first for e in win)
        second_win = all(e in second for e in win)
        if first_win or second_win:
            return [first_win, second_win]

    return [first_win, second_win]


def check_game_end(currentMove):
    divided = divide(currentMove)
    who_win = check_win(divided)
    if who_win[0] or who_win[1]:
        if who_win[0]:
            winner = 1
        else:
            winner = 2
        return {'result': True, 'winner': winner}

    return {'result': False}


def find_move(samples, currentMove, currentPlayer):
    weight = 2 ** ( 9 - len(currentMove))
    if len(currentMove) > 0:
        last_move = currentMove[len(currentMove) - 1]
    else:
        last_move = -1
    e = check_game_end(currentMove)
    if len(samples) == 0 or e["result"]:
        if e["result"]:
            if e["winner"] - 1 == currentPlayer:
                return ( last_move, weight)
            return (last_move, -weight)
        elif len(samples) == 0:
            return (last_move, 0)
    max = -1024
    for i in range(len(samples)):
        move = samples.pop(i)
        currentMove.append(move)
        last_move, weight = find_move(samples, currentMove, currentPlayer)
        if weight > max:
            max = weight
        currentMove.pop()
        samples.insert(i, move)
    return (last_move, max)

def run_game(samples, currentMove):
    e = check_game_end(currentMove)
    if len(samples) == 0 or e["result"]:
        if e["result"]:
            # print(*currentMove, end=" ")
            # print(": Winner is ", end=" ")
            # print(e["winner"])
            win_count[e["winner"] - 1] += 1
        elif len(samples) == 0:
            # print(*currentMove, end=" ")
            # print(": !!! No Winner")
            win_count[2] += 1
        win_count[3] += 1
        return
    # random.shuffle(samples)
    # move = samples.pop()

    (move, weight) = find_move(samples.copy(), currentMove.copy(), len(currentMove) % 2)
    samples.remove(move)

    currentMove.append(move)
    run_game(samples, currentMove)
    # for i in range(len(samples)):
    #   move = samples.pop(i)
    #   currentMove.append(move)
    #   runGame(samples, currentMove)
    #   currentMove.pop()
    #   samples.insert(i, move)

t_start = time.time()

for x in range(1):
    if x != 0:
        print('-------------------------')
    start = time.time()

    for i in range(100):
        x = samples.copy()
        run_game(x, [])

    done = time.time()
    print(win_count)
    elapsed = done - start
    print('%.4f' % elapsed, end=' seconds\n')
    win_count = [0, 0, 0, 0]

print('############')
last = time.time() - t_start
print('%.4f' % last, end=' seconds\n')
