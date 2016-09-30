import time
import os
import copy
import numpy as np
import random

import scipy.misc as sm
import raytrace
import raytrace_cpp

directions = [np.asarray([-1, 0]), np.asarray([0, -1]), np.asarray([1, 0]), np.asarray([0, 1])]




def main():
    block_set = {}
    block_set["."] = Block(block_id=0, indicator=".", name="air", movable=True)
    block_set["#"] = Block(block_id=1, indicator="#", name="stone", color=(127, 127, 127), movable=False)
    block_set["R"] = Block(block_id=2, indicator="R", name="red_tile", block_type="tile", color=(255, 0, 0), movable=True)
    block_set["B"] = Block(block_id=3, indicator="B", name="blue_tile", block_type="tile", color=(0, 0, 255),
            movable=True)
    block_set["Y"] = Block(block_id=4, indicator="Y", name="yellow_tile", block_type="tile", color=(255, 255, 0),
            movable=True)
    block_set["G"] = Block(block_id=5, indicator="G", name="green_tile", block_type="tile", color=(0, 255, 0),
            movable=True)

    map_str = [
        "#######",
        "#2...3#",
        "###.###",
        "..#.#..",
        "..#.#..",
        "..#.#..",
        "###.###",
        "#..0.1#",
        "#######",
    ]
    map_data, positions = load_map(block_set, map_str)
    map_ = Map(*map_data)
    for pos in positions:
        map_.set_block(pos, block_set["."])
    action_set = [("move", 1), ("move", -1), ("turn", 1), ("turn", -1)]

    env = RogueEnv(action_set=action_set)
    indicator = "Y"#np.random.choice(("G", "Y"))
    map_.set_block(positions[2], block_set["B"])
    map_.set_block(positions[3], block_set["R"])
    map_.set_block(positions[1], block_set[indicator])
    env.reset(map_=map_, start_direction=np.asarray([-1,0]),
            start_position=np.asarray(positions[0]))
    print(env.agent_position)
    for step in range(5000):
        os.system("clear")
        env.print_map()

        if env.agent_direction[0] == -1 and env.agent_direction[1] == 0:
            direction = 180
        elif env.agent_direction[0] == 0 and env.agent_direction[1] == -1:
            direction = 90
        elif env.agent_direction[0] == 1 and env.agent_direction[1] == 0:
            direction = 0
        elif env.agent_direction[0] == 0 and env.agent_direction[1] == 1:
            direction = 270

        im = map_to_image((32, 32), map_, env.agent_position, direction)
        sm.imsave("test"+"{0:03d}".format(step)+".png", im)

        print(env.agent_position.dtype)
        print(env.agent_direction.dtype)
        topview = map_to_top_view_image((200, 200), map_)
        sm.imsave("topview"+"{0:03d}".format(step)+".png", topview)

        #ob = map_to_ob(map_, direction=env.agent_direction, pos=env.agent_position)
        #print_ob(ob)
        #hv = ob_to_hot_vectors(ob, block_type_num=6)
        #print_ob(hv)
        action = random.randrange(len(action_set))
        env.step(action)
        #time.sleep(0.1)
        input()
    m = Map()
    m.print()

if __name__ == "__main__":
    main()
