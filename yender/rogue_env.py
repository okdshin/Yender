import copy
import numpy as np

from yender.renderer import raytrace
from yender.block import Block
from yender.map import Map

def map_to_block_ob(map_, pos, direction, block_id_dict, default_block):
    '''Make block observations from map
    TODO image

    Args:
        map_ (Map): target map
        pos (tuple of two ints): agent position
        direction (tuple of two ints): agent direction
        block_id_dict (dict of str key and int value): dict of block name key and block id value
        default_block (Block): default block out of area

    Returns:
        list of int: block id list
    '''
    assert isinstance(map_, Map)
    look_dict = {}
    look_dict[(-1, 0)] = [
        np.asarray([-2,-1]), np.asarray([-2, 0]), np.asarray([-2, 1]),
        np.asarray([-1,-1]), np.asarray([-1, 0]), np.asarray([-1, 1]),
        np.asarray([ 0,-1]), np.asarray([ 0, 0]), np.asarray([ 0, 1]),
    ]
    look_dict[(0, -1)] = [
        np.asarray([1, -2]), np.asarray([0, -2]), np.asarray([-1, -2]),
        np.asarray([1, -1]), np.asarray([0, -1]), np.asarray([-1, -1]),
        np.asarray([1,  0]), np.asarray([0,  0]), np.asarray([-1, 0]),
    ]
    look_dict[(1, 0)] = [
        np.asarray([2,  1]), np.asarray([2,  0]), np.asarray([2, -1]),
        np.asarray([1,  1]), np.asarray([1,  0]), np.asarray([1, -1]),
        np.asarray([0,  1]), np.asarray([0,  0]), np.asarray([0, -1]),
    ]
    look_dict[(0, 1)] = [
        np.asarray([-1, 2]), np.asarray([0, 2]), np.asarray([1, 2]),
        np.asarray([-1, 1]), np.asarray([0, 1]), np.asarray([1, 1]),
        np.asarray([-1, 0]), np.asarray([0, 0]), np.asarray([1, 0]),
    ]

    blocks = []
    for look in look_dict[tuple(direction)]:
        block_id = block_id_dict[map_.safe_get_block(look+pos, default_block).name]
        blocks.append(block_id)
    return blocks

def map_to_scene_image(size, map_, pos, yaw, pitch=-30):
    '''make scene image from map

    Args:
        size (tuple of two ints): result image size
        map_ (Map): target map
        pos (tuple of two ints): camera position
        yaw (float): camera yaw
        pitch (float): camera pitch

    Returns:
        numpy.ndarray: scene image
    '''
    block_triangles = []
    block_colors = []
    for y in range(map_.size[0]):
        for x in range(map_.size[1]):
            block = map_.get_block((y, x))
            if block.visible:
                triangles, colors = block_to_triangles(block, (x, y))
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
    #print(pos)
    image = raytrace(size, [pos[1]+0.5,pos[0]+0.5,0.85],
            20, yaw, pitch, block_triangles, block_colors)
    return np.asarray(image).astype(np.uint8)

def block_to_triangles(block, pos):
    '''Make triangles of a block (i.e. box or tile with position)

    Args:
        block (Block): block to be converted
        pos (list of three floats): block position

    Returns:
        tuple: tuple of triangles and colors
    '''
    assert isinstance(block, Block)
    if block.block_type == "block":
        triangles, colors = box_triangles(block.color)
    elif block.block_type == "tile":
        triangles, colors = tile_triangles(block.color)
    return triangles+(pos[0], pos[1], 0), colors

def map_to_top_view_image(size, map_):
    block_triangles = []
    block_colors = []
    for y in range(map_.size[0]):
        for x in range(map_.size[1]):
            block = map_.get_block((y, x))
            if block.name != "air":
                triangles, colors = block_to_triangles((x, y), block)
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

def print_block_ob(ob):
    for i in range(len(ob)):
        if i%3 == 0:
            print()
        if i == 7:
            print("^", end="")
        print(ob[i], end="")

def block_ob_to_hot_vectors(block_ob, block_type_num):
    '''make hot vector list from block observations

    Args:
        block_ob (list of Block): target block observations
        block_type_num (int): the number of block types

    Returns:
        numpy.ndarray: hot vector list
    '''
    hot_vectors = np.zeros((3*3, block_type_num), dtype=np.float32)
    for i in range(len(block_ob)):
        hot_vectors[i][block_ob[i]] = 1.0
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
            agent_char = "^"
        elif self.agent_direction[0] == 0 and self.agent_direction[1] == -1:
            agent_char = "<"
        elif self.agent_direction[0] == 1 and self.agent_direction[1] == 0:
            agent_char = "v"
        elif self.agent_direction[0] == 0 and self.agent_direction[1] == 1:
            agent_char = ">"
        map_.set_block(self.agent_position, Block(char=agent_char, name="agent", movable=False, visible=False))
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
