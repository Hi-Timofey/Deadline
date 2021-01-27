from random import randint, seed, random
from copy import deepcopy


def show_matrix(matrix):
    for _ in range(len(matrix)):
        for i in range(len(matrix[_])):
            pp = str(matrix[_][i]).replace('0', ' ')
            pp = str(matrix[_][i]).replace('1', '#')
            # print(pp, end="")
        # print()


def check_lvl(lvl):
    flag = True
    for i in range(0, len(lvl), 2):
        if not flag:
            break
        for j in range(0, len(lvl[0]), 2):
            if lvl[i][j] == 1:
                flag = False
                break
    return flag


def generate(matrix, num):
    flag = True
    x, y, e = 0, 0, 0
    while flag:
        e += 1
        seed(num)
        step = randint(-2, 2)
        matrix[0][0] = 0
        old_matrix = deepcopy(matrix)
        if step == 2:
            if 0 <= x + 2 < len(matrix[y]):
                if matrix[y][x + 2] == 0 and matrix[y][x + 1] == 0:
                    x += 2
                elif matrix[y][x + 2] != 0 and matrix[y][x + 1] != 0:
                    matrix[y][x + 2] = 0
                    matrix[y][x + 1] = 0
                    x += 2
        elif step == -2:
            if 0 <= x - 2 < len(matrix[y]):
                if matrix[y][x - 2] == 0 and matrix[y][x - 1] == 0:
                    x -= 2
                elif matrix[y][x - 2] != 0 and matrix[y][x - 1] != 0:
                    matrix[y][x - 2] = 0
                    matrix[y][x - 1] = 0
                    x -= 2
        elif step == 1:
            if 0 <= y + 2 < len(matrix[y]):
                if matrix[y + 2][x] == 0 and matrix[y + 1][x] == 0:
                    y += 2
                elif matrix[y + 2][x] != 0 and matrix[y + 1][x] != 0:
                    matrix[y + 2][x] = 0
                    matrix[y + 1][x] = 0
                    y += 2
        elif step == -1:
            if 0 <= y - 2 < len(matrix[y]):
                if matrix[y - 2][x] == 0 and matrix[y - 1][x] == 0:
                    y -= 2
                elif matrix[y - 2][x] != 0 and matrix[y - 1][x] != 0:
                    matrix[y - 2][x] = 0
                    matrix[y - 1][x] = 0
                    y -= 2
        if check_lvl(matrix):
            flag = False

        num += 1
    return matrix


def ended(maze, height, width):
    b = True
    for i in range(1, (height - 1), 2):
        for j in range(1, width - 1, 2):
            if maze[i][j] == 1:
                b = False
    return b


def restruct(matrix):
    char_border = '#'
    char_space = " "
    width = len(matrix[0])
    matrix.insert(0, [char_border for i in range(width + 2)])
    for _ in range(1, len(matrix)):
        matrix[_].insert(0, char_border)
        for i in range(len(matrix[_])):
            if matrix[_][i] == 1 or matrix[_][i] == "1" or matrix[_][i] == "#":
                matrix[_][i] = char_border
        matrix[_].append(char_border)
    matrix.append([char_border for i in range(width + 2)])
    matrix[1][0] = "C"
    matrix[len(matrix) - 2][len(matrix[0]) - 1] = "E"
    matrix[1][2], matrix[1][3], matrix[1][4] = 0, 0, 0
    matrix[2][1], matrix[2][2], matrix[2][3],  matrix[1][4] = 0, 0, 0, 0
    print(matrix)
    return matrix


def create_level(x_size, y_size, key, callback=None):
    matrix_labirinth = [[1 for i in range(x_size)] for _ in range(y_size)]
    show_matrix(matrix_labirinth)
    matrix = generate(matrix_labirinth, int(key))
    matrix = restruct(matrix)
    if callback is not None:
        callback()
    return matrix


if __name__ == '__main__':
    x_size = int(input('Задайте ширину лабиринта: '))
    y_size = int(input('Задайте длину лабиринта: '))
    matrix_labirinth = [[1 for i in range(x_size)] for _ in range(y_size)]
    matrix = generate(matrix_labirinth, int(input()))
    matrix = restruct(matrix)
    show_matrix(matrix)
