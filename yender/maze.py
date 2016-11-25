import argparse
import random

def position_to_index(pos, width):
    return int(pos[1]*width+pos[0])

def index_to_position(index, width):
    return (int(index%width), int(index/width))

def get_cluster_number(room_index, room_set):
    i = room_index
    while i != room_set[i]:
        i = room_set[i]
    room_set[i] = i ##速くなるはず
    return i

def connect_room(wall_pos, room_set, width):
    if wall_pos[1]%2 == 0:
        a = (wall_pos[0], wall_pos[1]+1)
        b = (wall_pos[0], wall_pos[1]-1)
    else:
        a = (wall_pos[0]+1, wall_pos[1])
        b = (wall_pos[0]-1, wall_pos[1])
    ai = position_to_index(a, width)
    bi = position_to_index(b, width)
    #print(a, ai, b, bi)
    assert 0 <= ai and 0 <= bi
    ac = get_cluster_number(ai, room_set)
    bc = get_cluster_number(bi, room_set)
    if ac == bc:
        return False, room_set
    if ac < bc:
        room_set[bc] = ac
    else:
        room_set[ac] = bc
    return True, room_set

def make_maze_source(size, wall_char="#", air_char="."):
    '''make map source of maze

    The clustering method is used to make maze.

    Args:
        size (tuple of two ints): maze size
        wall_char (string): wall charactor
        air_char (string): air charactor

    Returns:
        list of string: map source of maze
    '''
    width = size[0]
    height = size[1]
    assert width%2 == 1
    assert height%2 == 1

    source = []
    for _ in range(height):
        source.append([wall_char for _ in range(width)])

    room_list = []
    room_set = {}
    for x in range(width):
        for y in range(height):
            if x%2 == 1 and y%2 == 1:
                source[y][x] = "."
                room_list.append(position_to_index((x,y), width))
                room_set[room_list[-1]] = room_list[-1]
    #print(room_list)
    #print([index_to_position(i, width) for i in room_list])
    while True:
    #for i in range(100):
        room_index = random.choice(room_list)
        pos = index_to_position(room_index, width)
        wall_pos = random.choice([(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1)])
        if wall_pos[0] <= 0 or width-1 <= wall_pos[0] or wall_pos[1] <= 0 or height-1 <= wall_pos[1]:
            continue
        #print(wall_pos)
        #print(room_set)
        connected, room_set = connect_room(wall_pos, room_set, width)
        if connected:
            source[wall_pos[1]][wall_pos[0]] = air_char
        if len(list(set([get_cluster_number(i, room_set) for i in room_set.values()]))) == 1:
            break

    #room_list = list(range(int((width-1)/2*(height-1)/2)))
    #print(room_list)
    #source[1][2] = "."

    return ["".join(line) for line in source]


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-width", type=int, default=11)
    parser.add_argument("-height", type=int, default=11)
    args = parser.parse_args()

    for i in range(1000):
        maze_source = make_maze_source((args.width, args.height))
        for line in maze_source:
            print(line)

if __name__ == "__main__":
    main()
