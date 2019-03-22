import sys
import os


def main():
    f_name = sys.argv[1]
    out_name = os.path.splitext(os.path.basename(f_name))[0] + '.out'


    with open(f_name, 'r') as f:
        initial = f.readline()
        directions = f.readline()

        x_init, y_init = initial.rstrip().split(' ')

        job = directions.rstrip().split(' ')

        job, amount = job[::2], job[1::2]

        job = list(zip(job, amount))

        pos = (int(x_init), int(y_init))
        dir_current = 0  # 0, 1, 2, 3 => right, down, left, up

        for j, steps in job:

            steps = int(steps)
            if j == 'F':
                pos = move(pos, dir_current, steps)

            elif j == 'T':
                dir_current = turn(dir_current, steps)

            else:
                raise NotImplementedError

        print(pos)
        write_out_file(out_name, *pos)


def move(pos, cur_dir, steps):

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


def turn(cur_dir, steps):
    return (cur_dir + steps) % 4


def write_out_file(file_name, x, y):
    outfile = open(file_name, "w+")
    outfile.write(str(x) + " " + str(y))
    outfile.close()

def write_out_file2(file_name, xy_list):
    outfile = open(file_name, "w+")
    for x,y in xy_list:
        outfile.write(str(x) + " " + str(y) + "\n")
    outfile.close()

if __name__ == "__main__":
    main()
