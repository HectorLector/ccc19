import sys
import os


class Alien:

    def __init__(self, alien_id, spawn_pos, spawn_tick, health):
        self.alien_id = alien_id
        self.spawn_tick = spawn_tick
        self.path = [spawn_pos]
        # 0, 1, 2, 3 => right, down, left, up
        self.direction = 0
        self.alive = True
        self.health = health

    def move(self, border_x, border_y):
        pos = self.path[-1]
        if self.direction == 0:
            pos = min(pos[0] + 1, border_x), pos[1]
        elif self.direction == 1:
            pos = pos[0], min(pos[1] + 1, border_y)
        elif self.direction == 2:
            pos = max(pos[0] - 1, 0), pos[1]
        elif self.direction == 3:
            pos = pos[0], max(pos[1] - 1, 0)
        else:
            raise NotImplementedError
        self.path.append(pos)

    def turn(self, amount):
        self.direction = (self.direction + amount) % 4


class Tower:

    def __init__(self, pos, t_range, damage):
        self.pos = pos
        self.range = t_range
        self.damage = damage
        self.alien_locked = None


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

            health, speed = f.readline().rstrip().split(' ')
            health = float(health)
            self.speed = float(speed)

            nr_spawns = int(f.readline().rstrip())
            spawns = [int(f.readline().rstrip()) for _ in range(nr_spawns)]
            self.aliens = {i: Alien(i, self.pos, sp, health) for i, sp in enumerate(spawns)}

            t_damage, t_range = f.readline().rstrip().split(' ')
            t_damage = float(t_damage)
            t_range = float(t_range)

            nr_towers = int(f.readline().rstrip())
            tower_cords = [tuple(int(c) for c in f.readline().rstrip().split(' ')) for _ in range(nr_towers)]
            self.towers = [Tower(c, t_range, t_damage) for c in tower_cords]

    def run(self):

        # calculate paths
        for al in self.aliens.values():
            for j, steps in self.job:
                steps = int(steps)
                if j == 'F':
                    for _ in range(steps):
                        al.move(self.border_x, self.border_y)
                elif j == 'T':
                    al.turn(steps)
                else:
                    raise NotImplementedError

    # def query(self):
    #     # get positions at query-ticks
    #     res = []
    #     for q in self.queries:
    #         tick = q[0]
    #         alien_id = q[1]
    #         alien = self.aliens[alien_id]
    #
    #         index = self.speed * (tick - alien.spawn_tick)
    #         # print(index)
    #         if index > len(alien.path)-1:
    #             index = len(alien.path)-1
    #         point = alien.path[int(index)]
    #
    #         part = f'{tick} {alien_id} {point[0]} {point[1]}'
    #         res.append(part)
    #         print(part)
    #
    #     return res

    def write_out_file(self, results):
        with open(self.out_name, "w+") as outfile:
            outfile.write('\n'.join(results))

def main():

    ccc = CCC(sys.argv[1])
    ccc.run()
    #res = ccc.query()
    #ccc.write_out_file(res)


if __name__ == "__main__":
    main()
