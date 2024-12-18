from collections import defaultdict

def parse_input(filename):
    with open(f'day18/{filename}') as f:
        lines = f.read().splitlines()
    data = [
        tuple(int(x) for x in line.split(','))
        for line in lines
    ]
    return data


class Search:
    def __init__(self, walls):
        self.walls = walls
        self.distances: dict[tuple[int, int], int] = defaultdict(lambda: 1e9)
        self.visited: dict[tuple[int, int], int] = defaultdict(lambda: False)
        self.start_pos = (0, 0)
        self.end_pos = (70, 70)

    def run(self):
        self.distances[self.start_pos] = 0
        queue = [self.start_pos]
        while queue:
            pos = queue.pop(0)
            self.visited[pos] = True
            for neighbour in [
                (pos[0] + 1, pos[1]), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1]), (pos[0], pos[1] - 1)
            ]:
                if self.is_oob(neighbour):
                    continue
                if neighbour in self.walls:
                    continue
                if self.visited[neighbour]:
                    continue
                distance = self.distances[pos] + 1
                self.distances[neighbour] = min(distance, self.distances[neighbour])
                if neighbour not in queue:
                    queue.append(neighbour)

    def is_oob(self, pos):
        return (
            pos[0] < self.start_pos[0] or pos[0] > self.end_pos[0]
            or pos[1] < self.start_pos[1] or pos[1] > self.end_pos[1]
        ) 

    def show_grid(self):
        for y in range(self.end_pos[1] + 1):
            line = ''
            for x in range(self.end_pos[0] + 1):
                if (x, y) in self.walls:
                    c = '#'
                elif self.visited[(x, y)]:
                    c = 'O'
                else:
                    c = '.'
                line += c
            print(line)


def main(filename):
    data = parse_input(filename)

    for i in range(len(data), -1, -1):
        # print(f'trying with {i} walls')
        search = Search(data[:i])
        search.run()
        if search.distances[search.end_pos] < 1e9:
            return data[:i + 1][-1]

r = main('input.txt')
print(f'answer: {r}')