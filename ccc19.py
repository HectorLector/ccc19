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

    def simulate(self):
        # get positions at query-ticks
        tick = 0
        while True:

            # move alien and check for alien win
            alien_pos = {}
            for alien in self.aliens.values():
                index = self.speed * (tick - alien.spawn_tick)

                # alien not spawned
                if index < 0:
                    continue

                if not alien.alive:
                    continue

                if index > len(alien.path)-1:
                    # alien wins
                    return tick, 'LOSS'

                point = alien.path[int(index)]
                alien_pos[alien.alien_id] = point

            if tick != 0:
                # simulate tower shots
                for t in self.towers:

                    # check tower locked and tower target valid = alive and in range
                    if (t.alien_locked and t.alien_locked.alien_id in alien_pos and
                            self.check_valid_target(t.alien_locked, alien_pos[t.alien_locked.alien_id], t)):
                        pass
                    else:
                        t.alien_locked = None
                        # check if in range
                        distances = {a_id: self.distance(a_pos, t) for a_id, a_pos in alien_pos.items()}

                        try:
                            min_dist = min(distances.items(), key=lambda v: v[1])
                            if min_dist[1] <= t.range:
                                t.alien_locked = self.aliens[min_dist[0]]
                            else:
                                t.alien_locked = None
                        except ValueError:
                            t.alien_locked = None

                for t in self.towers:
                    if t.alien_locked:
                        # shoot
                        t.alien_locked.health -= t.damage

                # check for dead aliens
                for a in self.aliens.values():
                    if a.health <= 0:
                        a.alive = False

                if (not any(a.alive for a in self.aliens.values()) and
                        not any(a.spawn_tick >= tick for a in self.aliens.values())):
                    # win
                    return tick, 'WIN'

            tick = tick + 1

    def check_valid_target(self, alien, a_pos, t):
        distance = self.distance(a_pos, t)
        return t.range >= distance and alien.alive

    def distance(self, a_pos, t):
        return((a_pos[0] - t.pos[0]) ** 2 + (a_pos[1] - t.pos[1]) ** 2) ** (1 / 2)

    def write_out_file(self, results):
        with open(self.out_name, "w+") as outfile:
            outfile.write('\n'.join(str(x) for x in results))

def main():

    ccc = CCC(sys.argv[1])
    ccc.run()
    res = ccc.simulate()
    print(res)
    ccc.write_out_file(res)


if __name__ == "__main__":
    main()
