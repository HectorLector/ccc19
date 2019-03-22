import sys
import os
import math


class Alien:

    def __init__(self, alien_id, speed, spawn_pos, spawn_tick):
        self.alien_id = alien_id
        self.speed = speed
        self.spawn_pos = spawn_pos
        self.spawn_tick = spawn_tick
        self.history = [self.spawn_pos]
        self.direction = 0

    def get(self, tick):
        return self.history[tick]

    def move(self, border_x, border_y):

        pos = self.history[-1]

        if self.direction == 0:
            pos = min(pos[0] + self.speed, border_x), pos[1]

        elif self.direction == 1:
            pos = pos[0], min(pos[1] + self.speed, border_y)

        elif self.direction == 2:
            pos = max(pos[0] - self.speed, 0), pos[1]

        elif self.direction == 3:
            pos = pos[0], max(pos[1] - self.speed, 0)

        else:
            raise NotImplementedError

        self.history.append(pos)

    def turn(self, steps):
        self.direction = (self.direction + steps) % 4


class CCC:

    def __init__(self, f_name):
        out_name = os.path.splitext(os.path.basename(f_name))[0] + '.out'
        self.out_name = 'out/' + out_name

        with open(f_name, 'r') as f:
            borders = f.readline()
            border_x, border_y = borders.rstrip().split(' ')
            self.border_x = int(border_x) - 1
            self.border_y = int(border_y) - 1

            initial = f.readline()
            x_init, y_init = initial.rstrip().split(' ')
            self.pos = int(x_init), int(y_init)

            directions = f.readline()
            job = directions.rstrip().split(' ')
            job, amount = job[::2], job[1::2]
            self.job = list(zip(job, amount))

            speed = float(f.readline().rstrip())
            nr_spawns = int(f.readline().rstrip())

            spawns = [int(f.readline().rstrip()) for _ in range(nr_spawns)]

            self.aliens = {i: Alien(i, speed, self.pos, sp) for i, sp in enumerate(spawns)}

            nr_ticks = int(f.readline().rstrip())
            self.queries = [tuple(int(c) for c in f.readline().rstrip().split(' ')) for _ in range(nr_ticks)]

            self.dir_current = 0  # 0, 1, 2, 3 => right, down, left, up

    def run(self):

        for a in self.aliens.values():
            print(f'{a.alien_id}:{a.history[-1]}')

        for j, steps in self.job:

                steps = int(steps)
                if j == 'F':
                    for _ in range(steps):
                        for a in self.aliens.values():
                            a.move(self.border_x, self.border_y)
                            print(f'{a.alien_id}:{a.history[-1]}')

                elif j == 'T':
                    for a in self.aliens.values():
                        a.turn(steps)

                else:
                    raise NotImplementedError

    def query(self):
        results = []
        for tick, alien_id in self.queries:
            pos = self.aliens[alien_id].get(tick)
            pos = [int(math.floor(x)) for x in pos]
            results.append(f'{tick} {alien_id} {pos[0]} {pos[1]}')

        return results

    def write_out_file(self, results):
        with open(self.out_name, "w+") as outfile:
            outfile.write('\n'.join(results))


def main():

    ccc = CCC(sys.argv[1])
    ccc.run()
    res = ccc.query()
    ccc.write_out_file(res)


if __name__ == "__main__":
    main()
