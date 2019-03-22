import sys
import os


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

            nr_ticks = int(f.readline().rstrip())
            ticks = [tuple(int(c) for c in f.readline().rstrip().split(' ')) for _ in range(nr_ticks)]

            self.dir_current = 0  # 0, 1, 2, 3 => right, down, left, up

    def run(self):

        positions = [self.pos]
        print(positions[-1])

        for j, steps in self.job:

            steps = int(steps)
            if j == 'F':
                for _ in range(steps):
                    positions.append(self.move(positions[-1], self.dir_current, 1))
                    print(positions[-1])

            elif j == 'T':
                self.dir_current = self.turn(self.dir_current, steps)

            else:
                raise NotImplementedError

        self.write_out_file(positions)

    def move(self, pos, cur_dir, steps):

        if cur_dir == 0:
            pos = min(pos[0] + steps, self.border_x), pos[1]

        elif cur_dir == 1:
            pos = pos[0], min(pos[1] + steps, self.border_y)

        elif cur_dir == 2:
            pos = max(pos[0] - steps, 0), pos[1]

        elif cur_dir == 3:
            pos = pos[0], max(pos[1] - steps, 0)

        else:
            raise NotImplementedError

        return pos

    def turn(self, cur_dir, steps):
        return (cur_dir + steps) % 4

    def write_out_file(self, xy_list):
        with open(self.out_name, "w+") as outfile:
            outfile.write('\n'.join(f'{x} {y}' for x, y in xy_list))


def main():

    ccc = CCC(sys.argv[1])
    ccc.run()


if __name__ == "__main__":
    main()
