class Fire():

    def __init__(self, x, y):
        '''
        Init Fire example with startin coord
        '''
        self.x = x
        self.y = y

    def update(self, level, fire):
        '''
        Updating fire sprites + logic of spreading
        '''
        if level[self.y][self.x] == '!':
            # front
            line = level[self.y]
            x = self.x
            y = self.y
            if self.x + 1 < len(line):
                if str(level[y][x + 1]) == '0' or str(level[y][x + 1]) == ' ':
                    level[y][x + 1] = '!'
                    fire.append([y, x + 1])

            if y + 1 < len(level):
                if str(level[y + 1][x]) == '0' or str(level[y + 1][x]) == ' ':
                    level[y + 1][x] = '!'
                    fire.append([y + 1, x])

            if x + 1 < len(line) and y + 1 < len(level):
                if str(level[y + 1][x + 1]
                       ) == '0' or str(level[y + 1][x + 1]) == ' ':
                    level[y + 1][x + 1] = '!'
                    fire.append([y + 1, x + 1])
            # back

            if x > 0:
                if str(level[y][x - 1]) == '0' or str(level[y][x - 1]) == ' ':
                    level[y][x - 1] = '!'
                    fire.append([y, x - 1])

            if y > 0:
                if str(level[y - 1][x]) == '0' or str(level[y - 1][x]) == ' ':
                    level[y - 1][x] = '!'
                    fire.append([y - 1, x])

            if y > 0 and x > 0:
                if str(level[y - 1][x - 1]
                       ) == '0' or str(level[y - 1][x - 1]) == ' ':
                    level[y - 1][x - 1] = '!'
                    fire.append([y - 1, x - 1])

            # diagonal
            if x > 0 and y + 1 < len(level):
                if str(level[y + 1][x - 1]
                       ) == '0' or str(level[y + 1][x - 1]) == ' ':
                    level[y + 1][x - 1] = '!'
                    fire.append([y + 1, x - 1])

            if y > 0 and x + 1 < len(line):
                if str(level[y - 1][x + 1]
                       ) == '0' or str(level[y - 1][x + 1]) == ' ':
                    level[y - 1][x + 1] = '!'
                    fire.append([y - 1, x + 1])
            level[y][x] = "&"
            fire.remove([y, x])


def show_matrix(matrix):
    char_border = '#'
    print(char_border * (int(len(matrix[0])) + 2))
    for _ in range(len(matrix)):
        print(char_border, end='')
        for i in range(len(matrix[_])):
            pp = str(matrix[_][i]).replace('0', ' ')
            pp = str(matrix[_][i]).replace('1', '#')
            print(pp, end="")
        print(char_border)
    print(char_border * (len(matrix[0]) + 2))


if __name__ == '__main__':
    level = [
        [0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0]]
    level[0][0] = "!"
    fire_list_coords = [[0, 0]]
    while fire_list_coords:
        for y, x in fire_list_coords:
            f = Fire(x, y)
            f.update(level, fire_list_coords)
            print()
            show_matrix(level)
            print(fire_list_coords)
