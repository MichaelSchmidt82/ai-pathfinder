"""
MIT License

Copyright (c) 2019 Michael Schmidt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class State:

    def __init__(self, maze=None, state=None):
        self.__cost = 0
        self.__parent = None
        self.__maze = maze

        self.__enterance = {'X': -1, 'Y': -1}
        self.__exit = {'X': -1, 'Y': -1}
        self.__pos = dict({})

        if isinstance(state, State):
            self.__cost = state.__cost
            self.__parent = state
            self.__maze = [[value for value in row] for row in state.__maze]

            self.__enterance = state.__enterance
            self.__exit = state.__exit

            self.__pos['X'], self.__pos['Y'] = state.__pos['X'], state.__pos['Y']
        elif maze:
            for _r, row in enumerate(maze):
                for _c, value in enumerate(row):
                    if value == 'S':
                        self.__enterance['X'], self.__enterance['Y'] = _c, _r
                    elif value == 'E':
                        self.__exit['X'], self.__exit['Y'] = _c, _r

            self.__pos['X'], self.__pos['Y'] = self.__enterance['X'], self.__enterance['Y']

    def __str__(self):
        res = ''
        for _r, row in enumerate(self.__maze):
            for _c, value in enumerate(row):
                if _r == self.__pos['Y'] and _c == self.__pos['X']:
                    res = '{} o'.format(res)
                else:
                    res = '{} {}'.format(res, value)
            res = '{} {}'.format(res, '\n')
        return '{} {}'.format(res, '\n')

    def __repr__(self):
        res = str(self)
        return '{} {} {}\n'.format(res, self.__cost, self.__pos)

    def __lt__(self, other):
        if isinstance(other, State):
            return self.__cost < other.__cost

    def move(self, coords):
        if self.__maze[coords['Y']][coords['X']] in ('X', 'S', '.'):
            raise ValueError('Move not available')

        self.__maze[coords['Y']][coords['X']] = '.'
        self.__pos.update(coords)
        self.__cost += 1

    def heuristic(self):
        return ((self.__pos['X'] - self.__exit['X']) ** 2 +
                (self.__pos['Y'] - self.__exit['Y']) ** 2) ** 0.5

    def expand(self):

        frontier = []
        for _x in [-1, 1]:
            if 0 <= self.__pos['X'] + _x < len(self.__maze[self.__pos['Y']]):
                if self.__maze[self.__pos['Y']][self.__pos['X'] + _x] == ' ':
                    frontier.append({'X': self.__pos['X'] + _x, 'Y': self.__pos['Y']})

        for _y in [-1, 1]:
            if 0 <= self.__pos['Y'] + _y < len(self.__maze):
                if self.__maze[self.__pos['Y'] + _y][self.__pos['X']] == ' ':
                    frontier.append({'X': self.__pos['X'], 'Y': self.__pos['Y'] + _y})

        for index, entry in enumerate(frontier):
            coord = entry
            frontier[index] = State(state=self)
            frontier[index].move(coord)

        return frontier

    def solved(self):
        return self.__pos['X'] == self.__exit['X'] and self.__pos['Y'] == self.__exit['Y']

    @property
    def cost(self):
        return self.__cost
