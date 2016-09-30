import copy

import .renderer

def map_to_ob(map_, pos, direction):
    look_dict = {}
    look_dict[(-1, 0)] = [
        np.asarray([-2,-1]), np.asarray([-2, 0]), np.asarray([-2, 1]),
        np.asarray([-1,-1]), np.asarray([-1, 0]), np.asarray([-1, 1]),
        np.asarray([ 0,-1]), np.asarray([ 0, 1]),
    ]
    look_dict[(0, -1)] = [
        np.asarray([1, -2]), np.asarray([0, -2]), np.asarray([-1, -2]),
        np.asarray([1, -1]), np.asarray([0, -1]), np.asarray([-1, -1]),
        np.asarray([1,  0]), np.asarray([-1, 0]),
    ]
    look_dict[(1, 0)] = [
        np.asarray([2,  1]), np.asarray([2,  0]), np.asarray([2, -1]),
        np.asarray([1,  1]), np.asarray([1,  0]), np.asarray([1, -1]),
        np.asarray([0,  1]), np.asarray([0, -1]),
    ]
    look_dict[(0, 1)] = [
        np.asarray([-1, 2]), np.asarray([0, 2]), np.asarray([1, 2]),
        np.asarray([-1, 1]), np.asarray([0, 1]), np.asarray([1, 1]),
        np.asarray([-1, 0]), np.asarray([1, 0]),
    ]

    blocks = []
    for look in look_dict[tuple(direction)]:
        block_id = map_.get_block(look+pos).block_id
        blocks.append(block_id)
    return blocks

def map_to_image(size, map_, pos, yaw, pitch=-30):
    block_triangles = []
    block_colors = []
    for y in range(map_.size[0]):
        for x in range(map_.size[1]):
            block = map_.get_block((y, x))
            if block.name != "air":
                triangles, colors = raytrace.block_to_triangles((x, y), block)
                block_triangles.extend([tri.tolist() for tri in triangles])
                block_colors.extend([list(c) for c in colors])
            else:
                #print("air")
                pass
    sky = 1000*np.asarray([
            [(-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, -1.0, 0.0)],
            [(1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (1.0, 1.0, 0.0)],
    ])+(0,0,1)
    sky_colors = [[127, 127, 127], [127, 127, 127]]
    block_triangles.extend(sky.tolist())
    block_colors.extend(sky_colors)

    ground = [
        [[-100.0, 100.0, 0.0], [-100.0, -100.0, 0.0], [100.0, 100.0, 0.0]],
        [[100.0, -100.0, 0.0], [100.0, 100.0, 0.0], [-100.0, -100.0, 0.0]],
    ]
    ground_colors = [[127, 127, 127], [127, 127, 127]]

    block_triangles.extend(ground)
    block_colors.extend(ground_colors)

    #block_triangles = np.concatenate(block_triangles)
    #print(block_triangles.shape)
    print(pos)
    image = raytrace_cpp.raytrace2(size[0], size[1],
            [pos[1]+0.5,pos[0]+0.5,0.85],
            20, yaw, pitch, block_triangles, block_colors)
    return np.asarray(image).astype(np.uint8)

def map_to_top_view_image(size, map_):
    block_triangles = []
    block_colors = []
    for y in range(map_.size[0]):
        for x in range(map_.size[1]):
            block = map_.get_block((y, x))
            if block.name != "air":
                triangles, colors = raytrace.block_to_triangles((x, y), block)
                block_triangles.extend([tri.tolist() for tri in triangles])
                block_colors.extend([list(c) for c in colors])
            else:
                #print("air")
                pass
    sky = 1000*np.asarray([
            [(-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, -1.0, 0.0)],
            [(1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (1.0, 1.0, 0.0)],
    ])+(0,0,1)
    sky_colors = [[127, 127, 127], [127, 127, 127]]
    block_triangles.extend(sky.tolist())
    block_colors.extend(sky_colors)

    ground = [
        [[-120.0, 120.0, 0.0], [-120.0, -120.0, 0.0], [120.0, 120.0, 0.0]],
        [[500.0, -100.0, 0.0], [500.0, 100.0, 0.0], [-5000.0, -100.0, 0.0]],
    ]
    ground_colors = [[100, 100, 100], [100, 100, 100]]

    block_triangles.extend(ground)
    block_colors.extend(ground_colors)

    #block_triangles = np.concatenate(block_triangles)
    #print(block_triangles.shape)
    image = raytrace_cpp.raytrace2(size[0], size[1],
            [0.5+int(map_.size[1]/2), 0.5+int(map_.size[0]/2), 100],
            1000, 180, -90, block_triangles, block_colors)
    return np.asarray(image).astype(np.uint8)

def print_ob(ob):
    for i in range(len(ob)):
        if i%3 == 0:
            print()
        if i == 7:
            print("^", end="")
        print(ob[i], end="")

def ob_to_hot_vectors(ob, block_type_num):
    hot_vectors = np.zeros((3*3-1, block_type_num), dtype=np.float32)
    for i in range(len(ob)):
        hot_vectors[i][ob[i]] = 1.0
    return hot_vectors

class RogueEnv:
    def __init__(self, action_set=[("move", 1), ("move", -1), ("turn", 1), ("turn", -1)]):
        self.action_set = action_set

    #    N=(-1,0)
    # W=(0,-1) E=(0,1)
    #    S=(1,0)
    def reset(self, map_, start_direction, start_position):
        self.map_ = map_
        self.agent_direction = start_direction
        self.agent_position = start_position

    def print_map(self):
        map_ = copy.deepcopy(self.map_)
        if self.agent_direction[0] == -1 and self.agent_direction[1] == 0:
            indicator = "^"
        elif self.agent_direction[0] == 0 and self.agent_direction[1] == -1:
            indicator = "<"
        elif self.agent_direction[0] == 1 and self.agent_direction[1] == 0:
            indicator = "v"
        elif self.agent_direction[0] == 0 and self.agent_direction[1] == 1:
            indicator = ">"
        map_.set_block(self.agent_position,
                Block(block_id=-1, indicator=indicator, name="agent", movable=False))
        map_.print()

    def step(self, action):
        if self.action_set[action] == ("move", 1):
            new_pos = self.agent_position + self.agent_direction
            if self.map_.get_block(new_pos).movable:
                self.agent_position = new_pos
        elif self.action_set[action] == ("move", -1):
            new_pos = self.agent_position - self.agent_direction
            if self.map_.get_block(new_pos).movable:
                self.agent_position = new_pos
        elif self.action_set[action] == ("turn", 1):
            if self.agent_direction[0] == -1 and self.agent_direction[1] == 0:
                self.agent_direction = np.asarray([0, -1])
            elif self.agent_direction[0] == 0 and self.agent_direction[1] == -1:
                self.agent_direction = np.asarray([1, 0])
            elif self.agent_direction[0] == 1 and self.agent_direction[1] == 0:
                self.agent_direction = np.asarray([0, 1])
            elif self.agent_direction[0] == 0 and self.agent_direction[1] == 1:
                self.agent_direction = np.asarray([-1, 0])
        elif self.action_set[action] == ("turn", -1):
            if self.agent_direction[0] == -1 and self.agent_direction[1] == 0:
                self.agent_direction = np.asarray([0, 1])
            elif self.agent_direction[0] == 0 and self.agent_direction[1] == -1:
                self.agent_direction = np.asarray([-1, 0])
            elif self.agent_direction[0] == 1 and self.agent_direction[1] == 0:
                self.agent_direction = np.asarray([0, -1])
            elif self.agent_direction[0] == 0 and self.agent_direction[1] == 1:
                self.agent_direction = np.asarray([1, 0])
        else:
            raise
