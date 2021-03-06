import os, random, time
import yender
import numpy as np
import collections

block_set = collections.OrderedDict()
block_set["."] = yender.Block(char=".", name="air", visible=False)
block_set["#"] = yender.Block(char="#", name="stone", color=(127, 127, 127), movable=False)
block_set["R"] = yender.Block(char="R", name="red_tile", block_type="tile", color=(255, 0, 0))
block_set["B"] = yender.Block(char="B", name="blue_tile", block_type="tile", color=(0, 0, 255))
block_set["Y"] = yender.Block(char="Y", name="yellow_tile", block_type="tile", color=(255, 255, 0))
block_set["G"] = yender.Block(char="G", name="green_tile", block_type="tile", color=(0, 255, 0))

block_id_dict = {}
for i, block in enumerate(block_set.values()):
    block_id_dict[block.name] = i

def make_i_maze_map():
    map_source = [
        "#######",
        "#2...3#",
        "###.###",
        "###.###",
        "###.###",
        "#..0.1#",
        "#######",
    ]
    map_, place_holders = yender.load_map(block_set, map_source)

    # place goal tiles and an indicator tile
    start_pos = place_holders["0"]
    indicator_pos = place_holders["1"]
    blue_pos = place_holders["2"]
    red_pos = place_holders["3"]

    indicator_color = random.choice(("G", "Y"))
    map_.set_block(start_pos, block_set["."])
    map_.set_block(indicator_pos, block_set[indicator_color])
    map_.set_block(blue_pos, block_set["B"])
    map_.set_block(red_pos, block_set["R"])

    return map_, indicator_color, start_pos, blue_pos, red_pos

class I_MazeEnv:
    max_step = 50

    def __init__(self):
        self.rogue_env = yender.RogueEnv()

    def get_ob(self):
        block_ob = yender.map_to_block_ob(self.map_,
                direction=self.rogue_env.agent_direction,
                pos=self.rogue_env.agent_position,
                block_id_dict=block_id_dict,
                default_block=block_set["#"])
        ob = yender.block_ob_to_hot_vectors(block_ob, len(block_id_dict))
        return ob

    def reset(self):
        self.t = 0
        self.total_reward = 0.0
        self.map_, self.indicator, start_pos, self.blue_pos, self.red_pos = make_i_maze_map()
        start_direction = random.choice(list(self.rogue_env.DIRECTION_SET.values()))
        self.rogue_env.reset(self.map_, start_direction, start_pos)
        ob = self.get_ob()
        return ob

    def step(self, action):
        self.rogue_env.step(action)

        # reward and done check
        if self.rogue_env.map_.get_block(self.rogue_env.agent_position).name == "red_tile":
            done = True
            reward = 1.0 if self.indicator == "Y" else -1.0
        elif self.rogue_env.map_.get_block(self.rogue_env.agent_position).name == "blue_tile":
            done = True
            reward = 1.0 if self.indicator == "G" else -1.0
        elif self.t == self.max_step:
            done = True
            reward = -0.04
        else:
            done = False
            reward = -0.04

        # get observation
        ob = self.get_ob()

        self.t += 1
        self.total_reward += reward
        return ob, reward, done, self.rogue_env

    def render(self):
        self.rogue_env.print_map()
        print("total_reward {0:0.2f}".format(self.total_reward))

max_episode = 20
max_step = 50

def render(env, episode, t, ob, sleep_time, message=""):
    os.system("clear")
    print("episode", episode)
    print("step", t)
    env.render()
    print("ob", ob)
    time.sleep(sleep_time)
    print(message)

def main():
    env = I_MazeEnv()
    for episode in range(max_episode):
        ob = env.reset()
        for t in range(max_step):
            render(env, episode, t, ob, 0.1)
            action = random.choice(range(4)) # random agent
            ob, reward, done, info = env.step(action)

            if done:
                render(env, episode, t, ob, 10, "Episode finished after {} timesteps".format(t+1))
                break

if __name__ == "__main__":
    main()
