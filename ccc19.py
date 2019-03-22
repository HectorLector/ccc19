import sys
import os


class CCC:

    def __init__(self, f_name):
        out_name = os.path.splitext(os.path.basename(f_name))[0] + '.out'
        self.out_name = 'out/' + out_name

        with open(f_name, 'r') as f:
            borders = f.readline()
            initial = f.readline()
            directions = f.readline()

            border_x, border_y = borders.rstrip().split(' ')
            self.border_x = int(border_x)
            self.border_y = int(border_y)

            x_init, y_init = initial.rstrip().split(' ')

            self.pos = int(x_init), int(y_init)

            job = directions.rstrip().split(' ')

            job, amount = job[::2], job[1::2]

            self.job = list(zip(job, amount))

            self.dir_current = 0  # 0, 1, 2, 3 => right, down, left, up

    def run(self):
        for j, steps in self.job:

            steps = int(steps)
            if j == 'F':
                self.pos = self.move(self.pos, self.dir_current, steps)

            elif j == 'T':
                self.dir_current = self.turn(self.dir_current, steps)

            else:
                raise NotImplementedError

        print(self.pos)
        self.write_out_file(*self.pos)

    def move(self, pos, cur_dir, steps):

        if cur_dir == 0:
            pos = pos[0] + steps, pos[1]

        elif cur_dir == 1:
            pos = pos[0], pos[1] + steps

        elif cur_dir == 2:
            pos = pos[0] - steps, pos[1]

        elif cur_dir == 3:
            pos = pos[0], pos[1] - steps

        else:
            raise NotImplementedError

        return pos

    def turn(self, cur_dir, steps):
        return (cur_dir + steps) % 4

    def write_out_file(self, x, y):
        outfile = open(self.out_name, "w+")
        outfile.write(str(x) + " " + str(y))
        outfile.close()


def main():

    ccc = CCC(sys.argv[1])
    ccc.run()

if __name__ == "__main__":
    main()
