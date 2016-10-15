Quick Tutorial
========

Make your own environment to train your agent
---------------------------------------------

In this tutorial, we instruct how to make your own environment with the specific example: I-Maze.

Work out details: What is I-Maze?
---------------------------------

I-Maze is a spatial memory task inspired by `T-Maze <https://en.wikipedia.org/wiki/T-maze>`_ introduced `Control of Memory, Active Perception, and Action in Minecraft [Junhyuk 2016]  <https://arxiv.org/abs/1605.09128>`_.

In I-Maze, an agent must reach the correct goal depending on the color of the indicator tile.

The detail infomation is below:

+-+-+-+-+-+-+-+
|#|#|#|#|#|#|#|
+-+-+-+-+-+-+-+
|#|2|.|.|.|3|#|
+-+-+-+-+-+-+-+
|#|#|#|.|#|#|#|
+-+-+-+-+-+-+-+
|#|#|#|.|#|#|#|
+-+-+-+-+-+-+-+
|#|#|#|.|#|#|#|
+-+-+-+-+-+-+-+
|#|.|.|0|.|1|#|
+-+-+-+-+-+-+-+
|#|#|#|#|#|#|#|
+-+-+-+-+-+-+-+

* An agent starts at the point 0 directed randomly.
* For every step, an agent do one of four actions: go forward, go backward, turn left and turn right.
* A tile (called "indicator tile") is placed at the point 1 and painted yellow or green for every episode.
* Two tiles are placed at the point 2 and 3. One tile is painted red and the other is painted blue.
* Reaching the red tile, an agent get +1.0 reward if the indicator tile is yellow else -1.0.
* Reaching the blue tile, an agent get +1.0 reward if the indicator tile is green else -1.0.
* Agent get -0.04 reward every step.
* The time limit is 50 steps.

Make I-Maze environment
-----------------------

Firstly, we need to define a block_set that enumerates the blocks included in I-Maze.

.. code-block:: python

    block_set = {}
    block_set["."] = Block(block_id=0, indicator=".", name="air", movable=True)
    block_set["#"] = Block(block_id=1, indicator="#", name="stone", color=(127, 127, 127), movable=False)
    block_set["R"] = Block(block_id=2, indicator="R", name="red_tile", block_type="tile", color=(255, 0, 0), movable=True)
    block_set["B"] = Block(block_id=3, indicator="B", name="blue_tile", block_type="tile", color=(0, 0, 255), movable=True)
    block_set["Y"] = Block(block_id=4, indicator="Y", name="yellow_tile", block_type="tile", color=(255, 255, 0), movable=True)
    block_set["G"] = Block(block_id=5, indicator="G", name="green_tile", block_type="tile", color=(0, 255, 0), movable=True)

Next, we need to make I-Maze map. We can make it with a source code.

.. code-block:: python

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

Join them into one helper function: make_i_maze_map.

.. code-block:: python

    def make_i_maze_map():
        block_set = {}
        block_set["."] = Block(block_id=0, indicator=".", name="air", movable=True)
        ...

        map_source = [
            "#######",
        ...

        return map_, indicator_color, start_pos, blue_pos, red_pos

Now, let's make I_MazeEnv class.

.. code-block:: python

    class I_MazeEnv:
        def __init__(self):
            pass

RogueEnv manages agent states (position and direction) so compose it.

.. code-block:: python

    import yender

    class I_MazeEnv:
        def __init__(self):
            self.rogue_env = yender.RogueEnv()

For every episode, we want to reset environment, so let's add reset method.

.. code-block:: python

        def reset(self):
            self.total_reward = 0.0
            map_, self.indicator, start_pos, self.blue_pos, self.red_pos = make_i_maze_map()
            start_direction = random.choice(([1, 0], [-1, 0], [0, 1], [0, -1]))
            self.rogue_env.reset(map_, start_direction, start_pos)

For every step, we want to have our agent do some action in the environment, so let's add step method.
The step method should do three things:

* Change environemnt
* Check reward and done
* Get observation

.. code-block:: python

        def step(self, action):
            self.rogue_env.step(action)

            # reward and done check
            if self.rogue_env.map_.get_block(self.rogue_env.agent_position).name == "red_tile":
                done = True
                reward = 1.0 if self.indicator.name == "yellow_tile" else -1.0
            elif self.rogue_env.map_.get_block(self.rogue_env.agent_position).name == "blue_tile":
                done = True
                reward = 1.0 if self.indicator.name == "green_tile" else -1.0
            else:
                done = False
                reward = -0.04

            # get observation
            block_ob = yender.map_to_block_ob(map_, direction=env.agent_direction, pos=env.agent_position)
            ob = yender.block_ob_to_hot_vectors(block_ob)

            self.total_reward += reward
            return ob, reward, done, self.rogue_env

That's all... Oops! Don't forget render function.

.. code-block:: python

        def render(self):
            os.system("clear")
            self.rogue_env.print_map()
            print("total_reward", self.total_reward)

Run random agent
----------------

Let's run random agent in our I-Maze!

.. code-block:: python

    max_episode = 20
    max_step = 50

    def main():
        env = I_MazeEnv()
        for episode in range(max_eisode):
            ob = env.reset()
            for t in range(max_step):
                env.render()
                time.sleep(0.1)

                action = random.choice(range(4)) # random agent
                ob, reward, done, info = env.step(action)

                if done:
                    env.render()
                    print("Episode finished after {} timesteps".format(t+1))
                    time.sleep(2)
                    break

The full code is `tutorial/tutorial.py <https://github.com/okdshin/Yender/blob/master/tutorial/tutorial.py>`_.

If you need any help about Yender, ask us via github issues or email.
