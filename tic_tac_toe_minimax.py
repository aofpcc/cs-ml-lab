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
            # print(divided)
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
    weight = 1
    if len(currentMove) > 0:
        last_move = currentMove[len(currentMove) - 1]
    else:
        last_move = -1
    e = check_game_end(currentMove)
    if len(samples) == 0 or e["result"]:
        if e["result"]:
            if e["winner"] - 1 == currentPlayer:
                return last_move, weight
            return last_move, -weight
        elif len(samples) == 0:
            return last_move, 0
    candidate = []
    # print(samples)
    for i in range(len(samples)):
        move = samples.pop(i)
        currentMove.append(move)
        last_move, weight = find_move(samples, currentMove, currentPlayer)
        candidate.append((last_move, weight))
        currentMove.pop()
        samples.insert(i, move)

    if (len(currentMove) + 1) % 2 == currentPlayer: # max
        sorted_candidate = sorted(candidate, key=lambda v: v[1], reverse=True)
    else: # min
        sorted_candidate = sorted(candidate, key=lambda v: v[1], reverse=False)
    candidate = list(filter(lambda x: x[1] == sorted_candidate[0][1], candidate))
    # print(samples)
    # print(str(currentPlayer) + ": ", end='')
    # print(str(currentMove) + ": ", end='')
    # print(candidate)
    random.shuffle(candidate)
    move = candidate.pop()
    # print(move)
    return move


def run_game(samples, currentMove):
    e = check_game_end(currentMove)
    # print(currentMove)
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
        return currentMove
    # random.shuffle(samples)
    # move = samples.pop()

    (move, weight) = find_move(samples.copy(), currentMove.copy(), len(currentMove) % 2)
    samples.remove(move)

    currentMove.append(move)
    return run_game(samples, currentMove)
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
        print( "Game# " + str(i))
        x = samples.copy()
        # run_game([1, 2, 8, 9], [3, 5, 4, 6, 7])
        last_move = run_game(x, [])
        print(last_move)

    done = time.time()
    print(win_count)
    elapsed = done - start
    print('%.4f' % elapsed, end=' seconds\n')
    win_count = [0, 0, 0, 0]

print('############')
last = time.time() - t_start
print('%.4f' % last, end=' seconds\n')
